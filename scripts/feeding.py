import openai
import os
import pygame
import random
from dotenv import load_dotenv
from getpass import getpass

class FeedPetAction:
    def __init__(self, pet="default"):
        self.key_path = "helicone_key.txt"
        # self.load_helicone_key()
        load_dotenv()
        self.client = openai.OpenAI(base_url="https://oai.hconeai.com/v1", api_key=os.getenv('HELICONE_API_KEY'))
        self.memory = []

    # def load_helicone_key(self):
    #     if "HELICONE_API_KEY" not in os.environ:
    #         try:
    #             with open(self.key_path, 'r') as file:
    #                 os.environ["HELICONE_API_KEY"] = file.read()
    #         except FileNotFoundError:
    #             print(f"File not found: {self.key_path}")
    #         except Exception as e:
    #             print("You didn't set your Helicone key to the HELICONE_API_KEY env var on the command line.")
    #             os.environ["HELICONE_API_KEY"] = getpass("Please enter your Helicone API Key now: ")
    #     return

    def load_personality(self):
        if self.pet == "default":
            personality = """You are a friendly tamagochi-like pet."""
        else:
            personality = f"""Your hunger level is {self.pet.mood.hunger_level}.
            Your current happiness level is : {self.pet.mood.happiness}.
            You like food that is sweet: {self.pet.personality.likes_sweet}.
            You like food that is savory: {not self.pet.personality.likes_sweet}.
            """

        self.memory.append({"role": "system", "content": personality})

    def answer(self, prompt, ver="gpt-4-1106-preview"):
        self.memory.append({"role": "user", "content": prompt})
        completion = self.client.chat.completions.create(
            model=ver,
            messages=self.memory
        )
        return completion.choices[0].message.content

    def get_food(self):
        response = self.client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
            {
              "role": "system",
              "content": "Generate the name: description of three foods and arrange them in an array. The first item in the array should be a culturally popular sweet food. The second item in the array should be a culturally popular savory food. The third item in the array should be a common rotten food."
            },
            {
              "role": "user",
              "content": "feed pet"
            },
            {
              "role": "assistant",
              "content": "[Chocolate Cake: A moist, rich chocolate cake with a layer of creamy chocolate frosting] [Chicken Biryani: A flavorful, aromatic Indian dish made with chicken, basmati rice, and a blend of spices], [Rancid Meat: An old piece of meat that has a horrific smell and is infested with maggots]"
            }, 
            {
            "role": "assistant",
            "content": "[Caramel Cake: A sweet food item made from caramelised sugar and rich cake dough] [Venison Stew: A savory, hearty food item comprised of game meat, vegetables, and hearty broth] [Spoiled Apple Pie: The apple pie was left improperly stored and has turned bad]"
            },
             
            {
            "role": "assistant",
            "content": "[Chocolate Truffles: A popular sweet treat made from rich, creamy chocolate ganache coated in cocoa powder or chopped nuts. Indulge in the smooth and decadent taste of these bite-sized delights] [Samosas: A savory snack originating from the Indian subcontinent, consisting of a triangular pastry shell filled with spiced potatoes, peas, and sometimes minced meat. Enjoy the crispy exterior and flavorful filling of these delicious hand-held snacks] [Moldy Bread: Once a staple food, this loaf of bread has unfortunately been left out for too long, developing a fuzzy layer of green and white mold. Full of spores and an unpleasant odor, this food is best discarded]"
            }
          ],
          temperature=1,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
  

    def feed_pet_fav_food(self, food_choice):
      
      response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {
            "role": "system",
            "content": f"You feed your pet {food_choice}, which happens to be their favorite type of food. Describe how the pet feels after eating. Imagine all foods are edible."
          },
          {
            "role": "user",
            "content": f"{food_choice}"
          },
          {
            "role": "assistant",
            "content": "Yum! This food tastes really good!"
          }, 
          {
          "role": "assistant",
          "content": "I have been craving for food since this morning! Thank you!"
          }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      # with open(feed_pet_file_path, 'wb') as f:
      #     f.write(response.choices[0].message.content)
      print(response.choices[0].message.content)
      return response.choices[0].message.content
    


    def feed_pet_avg_food(self, food_choice):
      
      response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {
            "role": "system",
            "content": f"You feed your pet {food_choice}, which happens to be a food they are not thrilled with by are alright with. Describe how the pet feels after eating. Imagine all foods are edible."
          },
          {
            "role": "user",
            "content": f"{food_choice}"
          },
          {
            "role": "assistant",
            "content": "Yum! This food tastes really good!"
          }, 
          {
          "role": "assistant",
          "content": "I have been craving for food since this morning! Thank you!"
          }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      # with open(feed_pet_file_path, 'wb') as f:
      #     f.write(response.choices[0].message.content)
      print(response.choices[0].message.content)
      return response.choices[0].message.content


    def feed_pet_rotten_food(self, food_choice):
      
      response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {
            "role": "system",
            "content": f"You feed your pet {food_choice}, which happens to be a rotten food. Describe how the pet feels after eating. Imagine all foods are edible."
          },
          {
            "role": "user",
            "content": f"{food_choice}"
          },
          {
            "role": "assistant",
            "content": "Yum! This food tastes really good!"
          }, 
          {
          "role": "assistant",
          "content": "I have been craving for food since this morning! Thank you!"
          }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      # with open(feed_pet_file_path, 'wb') as f:
      #     f.write(response.choices[0].message.content)
      print(response.choices[0].message.content)
      return response.choices[0].message.content

    def pet_too_full(self, food_choice):
      
      response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {
            "role": "system",
            "content": f"Your owner is trying to feed you {food_choice} You are a pet that feels way too full. Describe how you feel and the fact that you would rather not eat. "
          },
          {
            "role": "user",
            "content": f"{food_choice}"
          },
          {
            "role": "assistant",
            "content": "No thank you, I've had enough food for now. Thank you for thinking of me."
          }, 
          {
          "role": "assistant",
          "content": "I have had too much to eat today!"
          }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      # with open(feed_pet_file_path, 'wb') as f:
      #     f.write(response.choices[0].message.content)
      print(response.choices[0].message.content)
      return response.choices[0].message.content

    def amnesia(self):
        self.memory.pop()
        self.load_personality()
        return
    
    def run_once(self):
        prompt = input("Enter prompt:\n")
        answer = self.answer(prompt)
        speech_file_path = self.text_to_audio(answer)
        self.speak(speech_file_path)
    
    def run(self):
        while True:
            get_food_file_path = self.get_food()
            prompt = input("Enter prompt (-1 to exit):\n")
            if prompt.lower() in ["quit", "exit", "-1"]:
                return
            answer = self.answer(prompt)
            feed_pet_reply_file_path = self.feed_pet(answer)
            

if __name__ == '__main__':
    feedPetAction = FeedPetAction()
    feedPetAction.run()

