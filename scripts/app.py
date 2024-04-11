# backend/app.py
from flask import Flask, jsonify, request
from chatbot import Chatbot
from feeding import FeedPet
import os
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)
chatbot = Chatbot()  # Instantiate your Chatbot class
feedpet = FeedPet()

# Define the path to the React build folder
react_build_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')

# Serve the static files from the React build folder
@app.route('/')
def index():
    return app.send_static_file(react_build_path + 'index.html')


@app.route('/api/feed', methods=['POST'])
def feed_pet():
    # WIP
    data = request.json
    print(data)
    # prompt = data.get('description')
        
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

@app.route('/api/pet', methods=['POST'])
def generate_meditation():
    data = request.json
    voice = data.get('voice')
    prompt = data.get('description')
        
    # Process the prompt using your chatbot
    answer = chatbot.answer(prompt)
    #answer = "test"

    # Turn the reponse into audio and then play it
    audio_thread = threading.Thread(target=play_audio_async, args=(answer, voice))
    audio_thread.start()

    # Render the index.html template with the response
    return jsonify({"petText": answer})

def play_audio_async(answer, voice="random"):
    # Turn the response into audio and then play it
    speech_file_path = chatbot.text_to_audio(answer, voice)
    chatbot.speak(speech_file_path)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
