import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
import requests
import json
import re
import httpx

class PetGeneration:
    def __init__(self):
        load_dotenv()
        self.helicone_client = OpenAI(base_url="https://oai.hconeai.com/v1", api_key=os.getenv('HELICONE_API_KEY'))
        self.cv_client = OpenAI()
        self.http = httpx.Client()
        
    # Encode image in base64
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
             
    # Describe the Image   
    def describe_image(self, url) -> str:
        api_key = os.getenv('OPENAI_API_KEY')
        base64_image = self.encode_image(url)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "gpt-4-turbo",
            "messages": [
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "What's in this image?"
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                    }
                ]
                }
            ],
            "max_tokens": 300
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        description = response.json().get("choices")[0].get("message").get("content")
        return description
    
    # Augment prompt for image generation
    def augment_prompt(self, initial_description) -> str:
        augmented_prompt = ""
        messages = [
            {'role': 'system', 'content': "Rewrite the description to be an image prompt for Dall-E. Specify that the image must be in the style of early Disney 2D animated movies, inspired by the style of Fantasia. Specify that no text should be in the image at all. Do not generate a reference sheet. If the subject of the image is an object, anthropomorphize them in a cartoony way."},
            {'role': 'user', 'content': initial_description},
        ]
        
        client = OpenAI(base_url="https://oai.hconeai.com/v1", api_key=os.environ['HELICONE_API_KEY'])
        
        response = client.chat.completions.create(
            model='gpt-4',
            messages=messages,
            temperature=1,
            max_tokens=1028,
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0
        )
        augmented_prompt = response.choices[0].message.content
        return augmented_prompt
    
    # Generate a JSON from the image description
    def generate_json(self, desc):
        messages = [
            {'role': 'system', "content": "You are an assistant to generate JSONs of imaginary virtual pets. Given a description of an image, imagine the subject of the image as a virtual pet with a certain personality. Try to anthropomorphize the pet in a cartoon-like manner. Use the following format, and return the result as a JSON string:\npet = {\n    \"identity\": {\n        \"name\": str (a proper noun, give a new name if a name is not mentioned, give them a new name if the description describes an already existing character),\n        \"physical_details\": str (a description of the main subject of the image, limit to 1 sentence or phrase to describe it),\n        \"full_description:\" str (write a description to describe a virtual pet that would be generated from the original prompt)\n    },\n    \"personality\": {\n      \"conversationStyle\": str (lowercase, some personality type or archetype to describe their personality when they are speaking),\n      \"talkative\": true/false,\n      \"voice\": int from 0 - 6,\n      \"fav_color\": str (choose one of the common colors, red, green, yellow, orange, violet),\n      \"competitive\": true/false,\n      \"likes_sweet\": true/false,\n      \"quickly_hungry\": true/false,\n    }\n}\nHave an equal chance of generating conversation styles that are positive or negative. For instance, a pet can be mean or sarcastic if the description fits it. Avoid common conversation styles like cheerful, or energetic, use more specific and varied words."},
            {'role': 'user', 'content': desc}  
        ] 
        
        response = self.helicone_client.chat.completions.create(
            model='gpt-3.5-turbo-16k',
            messages=messages,
            temperature=1,
            max_tokens=750,
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content;
    
    # Make a safe filename for the image
    def make_safe_filename(self, name, ext=".png"):
        """Ensure that a filename is safe to save to disk (replace any non-alphanumeric characters with an underscore)."""
        name = re.sub(r"[^a-zA-Z0-9-]+", "_", name)
        name = name[:100]
        return f"{name}{ext}"

    # generate an image from a prompt
    def generate_image(self, prompt):
        # generate the image using the OpenAI API
        resp = self.cv_client.images.generate(
            prompt=prompt,
            model="dall-e-3",
            response_format="url",
            quality="standard",  # feel free to change to "standard" for some cost savings
            size="1024x1024",  # also try "1024x1792" for portrait or "1792x1024" for landscape
            style="vivid",  # "vivid" or "natural"
        )
        image = resp.data[0]

        # download the generated image from URL (expires after 60m)
        fp = f"pet_generation_images/dalle/{self.make_safe_filename(image.revised_prompt)}"
        with open(fp, "wb") as f:
            with self.http.stream("GET", image.url) as r:
                for data in r.iter_bytes():
                    f.write(data)

        return {"image_path": fp, "original_prompt": prompt, "revised_prompt": image.revised_prompt}
    
        # generate an image from a prompt, but don't download, just return link
    def generate_image_link(self, prompt):
        # generate the image using the OpenAI API
        resp = self.cv_client.images.generate(
            prompt=prompt,
            model="dall-e-3",
            response_format="url",
            quality="standard",  # feel free to change to "standard" for some cost savings
            size="1024x1024",  # also try "1024x1792" for portrait or "1792x1024" for landscape
            style="vivid",  # "vivid" or "natural"
        )
        image = resp.data[0]

        return {image.url}
    
if __name__ == '__main__':
    petGen = PetGeneration()
    description = petGen.describe_image('src/assets/images/burningelmo.jpg')
    # json_prompt = petGen.generate_json(description)
    # augmented_prompt = petGen.augment_prompt(json_prompt)
    # img_link = petGen.generate_image_link(augmented_prompt)
    print(description)