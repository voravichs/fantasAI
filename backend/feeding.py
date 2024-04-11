# pet json
import json
import datetime
import time

pip install -q d20 'kani[openai]' openai

now = datetime.datetime.now()
timeStart = str(now)

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

pet_json = json.dumps(pet)

print(pet_json)

reload_pet = json.loads(pet_json)

print(reload_pet["mood"])

import os
from getpass import getpass

# Set up your Helicone API key here
if "HELICONE_API_KEY" not in os.environ:
    print("You didn't set your Helicone key to the HELICONE_API_KEY env var on the command line.")
    os.environ["HELICONE_API_KEY"] = getpass("Please enter your Helicone API Key now: ")

# Set up a GPT-4 engine using the Helicone proxy
from kani.engines.openai import OpenAIEngine

engine = OpenAIEngine(api_key=os.environ["HELICONE_API_KEY"], model="gpt-4", api_base="https://oai.hconeai.com/v1")

from d20 import roll

from kani import Kani, ai_function, ChatMessage

from kani import chat_in_terminal

class DiceKani(Kani):
    @ai_function()
    def roll(
        self,
        dice: str
    ):
        """
        dice: Annotated[str, AIParam("what type of dice to roll for d20, e.g. 3d6kh2")]
        """
        roll_dice = roll(dice)
        result = roll_dice.total
        return result

import dataclasses
from dataclasses import dataclass

@dataclass
class Food:
    # structured food attributes
    sweet: bool
    rotten: bool
    name: str

    # LLM-generated
    description: str = ""


# Here's an example Food:
matcha_cake = Food(
    name="Matcha Cake",
    sweet=True,
    rotten=False,
    description=(
        "Matcha Cake boasts a tender crumb, kissed with the captivating hue of vibrant green tea. Delicately moist and infused with the essence of premium matcha powder, each slice reveals a harmonious balance of subtle sweetness and earthy undertones. Topped with a smooth matcha frosting, it's a visually stunning treat that promises a symphony of flavor with every bite."
    ),
)

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

FOOD_SELECTION_CREATOR_PROMPT = """
Use GPT to generate the name and description of a culturally popular sweet food. With this name and description, use the generate_food_sweet() function in the FoodCreatorKani class to create a food that is sweet and rotten is False.
Use GPT to generate the name and description of a culturally popular savory food. With this name and description, use the generate_food_savory() function in the FoodCreatorKani class to create a food that is savory and rotten is False.
Use GPT to generate the name, sweet or savory, and description of a common rotten food. With this name and description, use the generate_food_rotten() function in the FoodCreatorKani class to create a food that rotten is True.
"""

food_creator_ai = FoodCreatorKani(engine, always_included_messages=[ChatMessage.user(FOOD_SELECTION_CREATOR_PROMPT)])

# import time

# chat_in_terminal(food_creator_ai, stopword="!stop", verbose=True)
# food_creator_ai.save(f"creator-{int(time.time())}.json")

import json

food_selection = food_creator_ai.food
food_selection_json = dict()
print(food_selection)

for food_name, food in food_selection.items():
  food_dict = dataclasses.asdict(food)
  food_selection_json[food_name] = food_dict

with open("food-selection.json", "w") as f:
    json.dump(food_selection_json, f, indent=2)

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

UPDATE_STATS_PROMPT = """
Use the update_stats function within the UpdateStats class. Once done, find out the current
mood of the pet by accessing self.pet and getting the self.pet["mood"]["hunger"], self.pet["mood"]["happiness"],
and self.pet["mood"]["social_battery"] stats.
"""

update_stats_ai = UpdateStats(engine, pet=pet, system_prompt=UPDATE_STATS_PROMPT)

chat_in_terminal(update_stats_ai, stopword="!stop", verbose=False)
update_stats_ai.save(f"update_stats-{int(time.time())}.json")

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
feed_pet_ai.save(f"feed_pet-{int(time.time())}.json")

print(pet)

class TextChat(UpdateStats):

    def __init__(self, *args, pet: dict, **kwargs):
        super().__init__(*args, pet=pet, **kwargs)
        self.pet = pet

    @ai_function()
    def check_social_battery(
          self
      ):
          """
          This function first checks if the pet is introversion. If yes, it will return True
          if the pet's social battery is higher than zero, else it returns False.
          If the pet is not introversion, it will return True.
          """

          if self.pet["personality"]["introversion"]:
            if self.pet["mood"]["social_battery"] > 0:
              return True
            else:
              return False

          return True

    @ai_function()
    def pick_topic(
          self
      ):
          """
          This function rolls a dice to determine the string that it returns.
          """

          dice_ai = self.roll("1d6")

          if (dice_ai == 1) or (dice_ai == 2):
            return self.pet["personality"]["hobby"]

          elif (dice_ai == 3) or (dice_ai == 4):
            return "ask how user is doing"

          else:
            return "random topic"

    @ai_function()
    def update_social_battery(
          self
      ):
          """
          This function reduces the social battery of a pet if introversion is True,
          and increases the social battery of a pet if introversion is False.
          """
          if self.pet["personality"]["introversion"]:
            self.pet["mood"]["social_battery"] = self.pet["mood"]["social_battery"] - 1
            if self.pet["mood"]["social_battery"] == 0:
              return False
          else:
            self.pet["mood"]["social_battery"] = self.pet["mood"]["social_battery"] + 1
            return True

TEXT_CHAT_PROMPT = """
You are a talking pet and you will be conversing with your owner in first person voice.
Use the update_stats function within the UpdateStats class. Do this in silence without revealing the details.
Once done, list out the integers for self.pet["mood"]["hunger"], self.pet["mood"]["happiness"] stats, self.pet["mood"]["social_battery"] stats.
Use the check_social_battery function within the TextChat class. If the result is False, tell the user
that you are an introvert and you need time to recharge your social battery. Try back later.
If the result is True, use the pick_topic function within the TextChat class to find out what topic you would like
to talk about. Do this in silence without revealing the details.
Using the output string from pick_topic function, start state an interesting fact about the topic and start a conversation, conversing with
a personality that corresponds to self.pet["personality"]["talkative"] and self.pet["personality"]["cheerful"].
After every paragraph, prompt user for input to continue conversation and repeat.
After every two rounds of input from user, use the update_social_battery function within the TextChat class, check if the return
is True or False. If True, continue the conversation, checking the social batter after another two rounds.
If False, tell user that pet is tired and can no longer chat. End the whole conversation and exit using !stop.
"""

text_chat_ai = TextChat(engine, pet=pet, system_prompt=TEXT_CHAT_PROMPT)

chat_in_terminal(text_chat_ai, stopword="!stop", verbose=False)
text_chat_ai.save(f"text_chat-{int(time.time())}.json")

print(pet)
