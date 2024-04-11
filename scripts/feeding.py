# pet json
import json
import datetime
import time
import os
from getpass import getpass
from d20 import roll
from kani import Kani, ai_function, ChatMessage
from kani import chat_in_terminal
# Set up a GPT-4 engine using the Helicone proxy
from kani.engines.openai import OpenAIEngine

import dataclasses
from dataclasses import dataclass

class DiceKani(Kani):
    @ai_function()
    def roll(self, dice: str):
        """
        dice: Annotated[str, AIParam("what type of dice to roll for d20, e.g. 3d6kh2")]
        """
        roll_dice = roll(dice)
        result = roll_dice.total
        return result

@dataclass
class Food:
    # structured food attributes
    sweet: bool
    rotten: bool
    name: str

    # LLM-generated
    description: str = ""

class FoodCreatorKani(DiceKani):

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.food = dict()

    @ai_function()
    def generate_food_sweet(
        self,
        sweet: bool,
        rotten: bool,
        name: str,
        description: str,
    ):
        """
        This method will use the input parameters to create a new Food object. GPT
        does not need to give any additional inputs as all required inputs are in the
        function input arguments.
        """
        self.food[name] = Food(
            sweet=sweet,
            rotten=rotten,
            name=name,
            description=description,
        )

    @ai_function()
    def generate_food_savory(
        self,
        sweet: bool,
        rotten: bool,
        name: str,
        description: str,
    ):
        """
        This method will use the input parameters to create a new Food object. GPT
        does not need to give any additional inputs as all required inputs are in the
        function input arguments.
        """
        self.food[name] = Food(
            sweet=sweet,
            rotten=rotten,
            name=name,
            description=description,
        )

    @ai_function()
    def generate_food_rotten(
        self,
        sweet: bool,
        rotten: bool,
        name: str,
        description: str,
    ):
        """
        This method will use the input parameters to create a new Food object. GPT
        does not need to give any additional inputs as all required inputs are in the
        function input arguments.
        """

        self.food[name] = Food(
            sweet=sweet,
            rotten=rotten,
            name=name,
            description=description,
        )

# food_selection

class UpdateStats(DiceKani):

    def __init__(self, *args, pet: dict, **kwargs):
        super().__init__(*args, **kwargs)
        self.pet = pet


    @ai_function()
    def update_stats(self):

      """
        This function updates the self.pet["mood"]["last_updated"] and self.pet["mood"]["hunger_level"] attributes.
        It returns an array. The first item in the array (array[0]) represents the hunger_level
        of the pet. The second item in the array (array[1]) represents the happiness level of the pet.
      """

      now = datetime.datetime.now()
      last_updated = self.pet["mood"]["last_updated"]
      last_updated_time = datetime.datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S.%f")

      diff = now.minute - last_updated_time.minute

      if self.pet["personality"]["quickly_hungry"]:
        change_to_hunger = diff // 5
      else:
        change_to_hunger = diff // 10

      self.pet["mood"]["hunger_level"] = self.pet["mood"]["hunger_level"] + change_to_hunger

      if self.pet["personality"]["introversion"]:
        self.pet["mood"]["social_battery"] = self.pet["mood"]["social_battery"] + (diff // 3)
      else:
        self.pet["mood"]["social_battery"] = self.pet["mood"]["social_battery"] - (diff // 3)

      self.pet["mood"]["last_updated"] = str(now)

      return [self.pet["mood"]["hunger_level"], self.pet["mood"]["happiness"], self.pet["mood"]["social_battery"]]


class FeedPet(FoodCreatorKani, UpdateStats):
    # This Kani should reference your mouse - let's pass it in the constructor.
    def __init__(self, *args, pet: dict, **kwargs):
        super().__init__(*args, pet=pet, **kwargs)
        self.pet = pet

    @ai_function()
    def feed_pet(
        self,
        sweet: bool,
        rotten: bool,
        name: str,
        description: str,
    ):
        """
        This function accepts as input arguments hunger_fulfilled of the food, sweet of the food,
        rotten of the food, name of the food, and description of the food. It first checks if the
        pet's hunger level is more than zero. If it is not, it will feed the pet and update the hunger_level
        and happiness level of the self.pet. The function returns a boolean which corresponds to whether
        the pet was fed (True) or not (False). The self.pet object is also updated.
        """

        if self.pet["mood"]["hunger_level"] <= 0:
          return False

        if not rotten:
          new_hunger_level = max(0, self.pet["mood"]["hunger_level"] - 2)
          self.pet["mood"]["hunger_level"] = new_hunger_level
          if self.pet["personality"]["likes_sweet"] and sweet:
            self.pet["mood"]["happiness"] = self.pet["mood"]["happiness"] + 2
          elif not self.pet["personality"]["likes_sweet"] and not sweet:
            self.pet["mood"]["happiness"] = self.pet["mood"]["happiness"] + 2
          else:
            self.pet["mood"]["happiness"] = self.pet["mood"]["happiness"] + 1

        else:
          self.pet["mood"]["happiness"] = self.pet["mood"]["happiness"] - 1

        return True
    



if __name__ == '__main__':

  # Set up your Helicone API key here
  if "HELICONE_API_KEY" not in os.environ:
      print("You didn't set your Helicone key to the HELICONE_API_KEY env var on the command line.")
      os.environ["HELICONE_API_KEY"] = getpass("Please enter your Helicone API Key now: ")

  engine = OpenAIEngine(api_key=os.environ["HELICONE_API_KEY"], model="gpt-4", api_base="https://oai.hconeai.com/v1")

  pet = {
    "identity": {
        "name": "Hot Pot",
        "physical_details": "A living kettle",
    },
    "personality": {
      "cheerful": True,
      "talkative": True,
      "voice": 0,
      "fav_color": "blue",
      "competitive": True,
      "likes_sweet": True,
      "quickly_hungry": True,
      # new field
      "introversion": True,
      # new field
      "hobby": "hiking",
    },

    "mood": {
        "hunger_level": 0,
        "happiness": 5,
        "social_battery": 5,
        "last_updated": timeStart
    }
  }
  
  FEED_PET_PROMPT = """
  First, use the generate_food_sweet() method in FoodCreatorKani class to generate the name and description of a culturally popular sweet food. With this name and description, use the generate_food_sweet() function in the FoodCreatorKani class to create a food that is sweet and rotten is False.
  Do not show the user the details of this generation.
  Next, use generate_food_savory() method in the FoodCreatorKani class to generate the name and description of a culturally popular savory food. With this name and description, use the generate_food_savory() function in the FoodCreatorKani class to create a food that is savory and rotten is False.
  Do not show the user the details of this generation.
  Next, use generate_food_rotten() GPT to generate the name, sweet or savory, and description of a common rotten food. With this name and description, use the generate_food_rotten() function in the FoodCreatorKani class to create a food that rotten is True.
  Do not show the user the details of this generation.
  Next use the update_stats function within the UpdateStats class. Once done, find out the current
  mood of the pet by accessing self.pet and getting the self.pet["mood"]["hunger"] and self.pet["mood"]["happiness"] stats.
  Display the information of the food generated and ask the user which of these three foods the user would like to feed the pet.
  Using the input of the user, use the feed_pet() function in the FeedPet class to update the information of the pet. Use the sweet, rotten, name, description of the food
  chosen as inputs for the feed_pet() function. If the feed_pet() function returns False, the pet declined to eat
  because the pet is not hungry. If the feed_pet() function returns True, the pet did not decline the food, but
  might not have eaten if the food is rotten.
  Create a description to describe the event. If a pet is fed rotten food, it would not eat and happiness goes down.
  """
  feed_pet_ai = FeedPet(engine, pet=pet, system_prompt=FEED_PET_PROMPT)
  chat_in_terminal(feed_pet_ai, stopword="!stop", verbose=False)
  # feed_pet_ai.save(f"feed_pet-{int(time.time())}.json")

  print(pet)
