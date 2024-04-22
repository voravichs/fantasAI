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
                    "text": "What's in this image? Describe the image as whimsically as possible as if you were a Disney character."
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
            {'role': 'system', 'content': "Rewrite the description to be an image prompt for Dall-E. Specify that the image must be in the style of early Disney 2D animated movies, inspired by the style of Fantasia. Specify that no text should be in the image at all."},
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
            {'role': 'system', 'content': "You are an assistant to generate JSONs of imaginary virtual pets. Given a description of an image, imagine the subject of the image as a virtual pet with a certain personality. Use the following format, and return the result as a JSON string:\npet = {\n    \"identity\": {\n        \"name\": str,\n        \"physical_details\": str,\n    },\n    \"personality\": {\n      \"general_personality_desc\": str (lowercase, one word to describe their personality),\n      \"cheerful\": True/False,\n      \"talkative\": True/False,\n      \"voice\": int from 0 - 6,\n      \"fav_color\": [blue, yellow, red, green],\n      \"competitive\": True/False,\n      \"likes_sweet\": True/False,\n      \"quickly_hungry\": True/False,\n    },\n}"},
            {'role': 'user', 'content': desc}  
        ] 
        
        response = self.helicone_client.chat.completions.create(
            model='gpt-3.5-turbo-16k',
            messages=messages,
            temperature=1,
            max_tokens=500,
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
    
if __name__ == '__main__':
    petGen = PetGeneration()
    os.chdir('../')
    description = petGen.describe_image('client/src/assets/images/redpanda.jpg')
    # json_prompt = petGen.generate_json(description)
    # augmented_prompt = petGen.augment_prompt(json_prompt)
    # img_dict = petGen.generate_image(augmented_prompt)
    print(description)