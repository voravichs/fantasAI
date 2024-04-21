import openai
import os
import pygame
import random
from dotenv import load_dotenv
from getpass import getpass
import re

class FeedPetAction:
    def __init__(self):
        self.key_path = "helicone_key.txt"
        # self.load_helicone_key()
        load_dotenv()
        self.client = openai.OpenAI(base_url="https://oai.hconeai.com/v1", api_key=os.getenv('HELICONE_API_KEY'))
        self.memory = []
        self.fridge = []

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

    def load_personality(self, talkative, cheerful, likes_sweet):

      if talkative:
          words_used = 80
      else:
          words_used = 30

      if cheerful:
        speak_manner = "positive"
      else:
        speak_manner = "negative"

      personality = f"""You are a talking pet. Each of your speech contains around {words_used} words.
      In terms of food preferences, you like sweet food: {likes_sweet}, and you like savory food: {not likes_sweet}
      Speak in a manner way that has a {speak_manner} vibe. Be cute overall.
      """

      self.memory.append({"role": "system", "content": personality})

    # def answer(self, prompt, ver="gpt-4-1106-preview"):
    #     self.memory.append({"role": "user", "content": prompt})
    #     completion = self.client.chat.completions.create(
    #         model=ver,
    #         messages=self.memory
    #     )
    #     return completion.choices[0].message.content

    # def open_fridge(self):
    #     response = self.client.chat.completions.create(
    #       model="gpt-3.5-turbo",
    #       messages=[
    #         {
    #           "role": "system",
    #           "content": f"Generate a narration that a fridge was opened"
    #         },
    #         {
    #           "role": "user",
    #           "content": "open fridge"
    #         },
    #         {
    #           "role": "assistant",
    #           "content": "You open the fridge and was surprised to find exciting items."
    #         }, 
    #         {
    #         "role": "assistant",
    #         "content": "You skipped towards the fridge and with a strong pull opened the door to find new possibilties"
    #         }
    #       ],
    #       temperature=1,
    #       max_tokens=256,
    #       top_p=1,
    #       frequency_penalty=0,
    #       presence_penalty=0
          
    #     )
        
    #     return response.choices[0].message.content
  


    def get_food(self):
        response = self.client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages= [ 
            {
              "role": "system",
              "content": f"Generate the name: description of three foods and arrange them in an array. The first item in the array should be a culturally popular sweet food. The second item in the array should be a culturally popular savory food. The third item in the array should be a common rotten food. Do not repeat food in {self.fridge}"
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
        
        food_names = re.findall(r'\[([^:]+):', response.choices[0].message.content)

        for idx, food in enumerate(food_names):
            self.fridge.append(food)
        print(self.fridge)
        return response.choices[0].message.content
  

    def pet_answer(self, nature, fav_food, food_choice, talkative, cheerful, describe, likes_sweet):
          
          self.load_personality(talkative, cheerful, likes_sweet)
          
          self.memory.append({"role": "user", "content": describe})
          if talkative:
            max_tokens = 300
          else:
            max_tokens = 100

          pet_personality = f"You are a talking pet. Your replies are {max_tokens} number of words. Your personality is cheerful: {cheerful}."

          if nature == "full":
            content = pet_personality + f" You are too full to eat so you rejected your owner's {food_choice}. Reply in pet language in first-person converstion style."
          elif nature == "thank":
            content = pet_personality + f" Your owner fed you {food_choice} and you ate it. It is your favorite food: it {fav_food}. Thank your owner in pet language in first-person converstion style."
          elif nature == "rotten":
            content = pet_personality + f" Your owner fed you {food_choice} and you ate it. It is rotten food. You reply that you ate it but are angry in pet language in first-person converstion style."

          response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.memory + [
              {
                "role": "system",
                "content": content
              },
              {
                "role": "user",
                "content": f"{food_choice}"
              },
            ],
            temperature=1,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
          )
          self.memory.append({"role": "assistant", "content": response.choices[0].message.content})
          return response.choices[0].message.content

    def pet_too_full_answer(self, fav_food, food_choice, talkative, cheerful, describe, likes_sweet):
          
          self.load_personality(talkative, cheerful, likes_sweet)
          
          self.memory.append({"role": "user", "content": describe})
          if talkative:
            max_tokens = 300
          else:
            max_tokens = 100

          pet_personality = f"You are a talking pet. Your replies are {max_tokens} number of words. Your personality is cheerful: {cheerful}."

          content = pet_personality + f" You are too full to eat so you rejected your owner's {food_choice}. Reply in pet language in first-person converstion style."
          
          response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.memory + [
              {
                "role": "system",
                "content": content
              },
              {
                "role": "user",
                "content": f"{food_choice}"
              },
            ],
            temperature=1,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
          )
          self.memory.append({"role": "assistant", "content": response.choices[0].message.content})
          return response.choices[0].message.content

    def talk_to_pet(self, description, likes_sweet, talkative, cheerful):
      
      self.load_personality(talkative, cheerful, likes_sweet)

      response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= self.memory + [
          {
            "role": "user",
            "content": f"{description}"
          },
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
      )
      self.memory.append({"role": "assistant", "content": response.choices[0].message.content})
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

