# backend/app.py
from flask import Flask, jsonify, request
from chatbot import Chatbot
from feeding import FeedPetAction
import os
from flask_cors import CORS
import threading
import re

app = Flask(__name__)
CORS(app)
chatbot = Chatbot()  # Instantiate your Chatbot class
feedPetAction = FeedPetAction()

# Define the path to the React build folder
react_build_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')

# Serve the static files from the React build folder
@app.route('/')
def index():
    return app.send_static_file(react_build_path + 'index.html')

@app.route('/api/food', methods=['POST'])
def generate_food_options():

    answer = feedPetAction.get_food()
    food_type = ["sweet", "savory", "rotten"]
    food_names = re.findall(r'\[([^:]+):', answer)

    food_pair = {}
    for idx, food in enumerate(food_names):
        pattern = r'\[([^\[\]]*?):]'
        matches = re.findall(pattern, food)
        food_pair[food] = food_type[idx]

    # Extract key-value pairs using regular expression
    pattern = r'\[([^\[\]]*?):\s*([^\[\]]*?)\]'
    matches = re.findall(pattern, answer)

    # Construct the dictionary
    food_dict = {name.strip(): des.strip() for name, des in matches}

    narration = feedPetAction.open_fridge()

    return jsonify({"food": food_dict, "food_type": food_pair, "narration": narration})

@app.route('/api/feed', methods=['POST'])
def generate_feed_pet():

    data = request.json
    food_choice = data.get("food")
    food_type = data.get("food_type")
    hunger_level = data.get('hunger_level')
    happiness_level = data.get('happiness_level')
    likes_sweet = data.get('likes_sweet')
    cheerful = data.get('cheerful')
    talkative = data.get('talkative')

    if hunger_level < 0:
        describe = feedPetAction.pet_too_full(food_choice)
        pet_answer = feedPetAction.pet_answer("full", False, food_choice, talkative, cheerful)

    if food_type == "rotten":
        hunger_level = hunger_level - 1
        happiness_level = happiness_level - 2
        describe = feedPetAction.feed_pet_rotten_food(food_choice)
        # nature of conversation, fav_food, food_choice, talkative, cheerful
        pet_answer = feedPetAction.pet_answer("rotten", False, food_choice, talkative, cheerful)
    elif (likes_sweet and food_type == "sweet") or (not likes_sweet and food_type == "savory"):
        hunger_level = hunger_level - 2
        happiness_level = happiness_level + 3
        describe = feedPetAction.feed_pet_fav_food(food_choice)
        # nature of conversation, fav_food, food_choice, talkative, cheerful
        pet_answer = feedPetAction.pet_answer("thank", True, food_choice, talkative, cheerful)
    else:
        hunger_level = hunger_level - 2
        happiness_level = happiness_level + 1
        describe = feedPetAction.feed_pet_avg_food(food_choice)
        # nature of conversation, fav_food, food_choice, talkative, cheerful
        pet_answer = feedPetAction.pet_answer("thank", False, food_choice, talkative, cheerful)

    return jsonify({"describe": describe, "pet_answer": pet_answer, "happiness": happiness_level, "hunger": hunger_level})


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
