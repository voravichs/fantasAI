# backend/app.py
from flask import Flask, jsonify, request
from chatbot import Chatbot
from feeding import FeedPetAction
from games import TicTacToe
from games import ConnectFour
from games import MagicContest
from petgen import PetGeneration
import os
from flask_cors import CORS
import threading
import re
import math
import random

app = Flask(__name__)
CORS(app)
chatbot = Chatbot()  # Instantiate your Chatbot class
feedPetAction = FeedPetAction()
ttt = TicTacToe([[0,0,0], [0,0,0], [0,0,0]])
connect4 = ConnectFour([[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]])
contest = MagicContest()
petGen = PetGeneration()

# Define the path to the React build folder
react_build_path = os.path.join(os.path.dirname(__file__), '..', 'client', 'build')

# Serve the static files from the React build folder
@app.route('/')
def index():
    return app.send_static_file(react_build_path + 'index.html')

@app.route('/api/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    desc = petGen.describe_image(data.get("url"))
    json_prompt = petGen.generate_json(desc)
    augmented_prompt = petGen.augment_prompt(json_prompt)
    link = petGen.generate_image_link(augmented_prompt)
    response = jsonify({"link" : list(link)[0], "json": json_prompt})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/setup_games', methods=['POST'])
def setup_games():
    data = request.json
    name = data.get("name")
    physical_details = data.get("physical_details")
    fav_color = data.get("fav_color")
    competitive = data.get("competitive")
    ttt.set_attributes(name, physical_details, fav_color, competitive)
    connect4.set_attributes(name, physical_details, fav_color, competitive)
    return ""

@app.route('/api/setup_contest', methods=['POST'])
def setup_contest():
    data = request.json
    name = data.get("name")
    physical_details = data.get("physical_details")
    fav_color = data.get("fav_color")
    talkative = data.get("talkative")
    competitive = data.get("competitive")
    quicklyHungry = data.get("quicklyHungry")
    likesSweet = data.get("likesSweet")
    happiness = data.get("happiness")
    hunger = data.get("hunger")
    contest.set_attributes(name, physical_details, fav_color, talkative, competitive, quicklyHungry, likesSweet, happiness, hunger)
    contest.set_energy(100-(2*hunger))
    return jsonify({"maxEnergy" : contest.get_energy()[0], "currEnergy" : contest.get_energy()[1]})

@app.route('/api/new_ttt', methods=['POST'])
def new_ttt():
    ttt.reset()
    return jsonify({"board" : ttt.get_board()})

@app.route('/api/new_c4', methods=['POST'])
def new_c4():
    connect4.reset()
    return jsonify({"board" : connect4.get_board()})  

@app.route('/api/new_contest', methods=['POST'])
def new_contest():
    contest.reset()
    return jsonify({"currEnergy" : contest.get_energy()[1]})  

@app.route('/api/get_ttt', methods=['POST'])
def get_ttt():
    return jsonify({"board" : ttt.get_board()})

@app.route('/api/move_ttt', methods=['POST'])
def move_ttt():
    if ttt.has_winner():
        response = ttt.talk("The game is already over! Press the button to start a new game!")
        return jsonify({"board" : ttt.get_board(), "response" : response})
    
    data = request.json
    move = ttt.get_space(data.get("move"))
        
    response = ""

    if move.isnumeric():
        if -1<int(move)<9:
            row = math.floor(int(move) / 3)
            col = int(move) % 3
            if ttt.is_legal_move(row, col):
                ttt.perform_move(row, col, 1)
                
                if not ttt.game_over():
                    if ttt.get_attributes()[3]:
                        move = ttt.get_best_move()
                        if move.isnumeric():
                            move = (math.floor(int(move) / 3), int(move) % 3)
                        else:
                            move = ttt.get_random_move()
                        if random.random() > 0.9 or not ttt.is_legal_move(move[0], move[1]):
                            move = ttt.get_random_move()
                    else:
                        move = ttt.get_random_move()
                    ttt.perform_move(move[0], move[1], -1)
                
                if ttt.has_winner() == 1:
                    response = ttt.talk('The game is over! I lost!')
                elif ttt.has_winner() == -1:
                    response = ttt.talk('The game is over! I won!')
                else:
                    response = ttt.talk(f'Nice Move! I made a move as well!', prior=data.get("move"))
        
            else:
                response = ttt.talk("You can't make that move. Choose a different one!")
        else:
            response = ttt.talk("That isn't a valid number. Choose a different one!")
    else:
        response = ttt.talk("That isn't a number. Choose a different one!")

    return jsonify({"board" : ttt.get_board(), "response" : response})


@app.route('/api/move_c4', methods=['POST'])
def move_c4():
    if connect4.has_winner():
        response = connect4.talk("The game is already over! Press the button to start a new game!")
        return jsonify({"board" : connect4.get_board(), "response" : response})
    
    data = request.json
    move = connect4.get_space(data.get("move"))
        
    response = ""
    if move.isnumeric():
        if -1<int(move)<7:
            if connect4.is_legal_move(int(move)):
                connect4.perform_move(int(move), 1)
                
                if not connect4.game_over():
                    if connect4.get_attributes()[3]:
                        move = connect4.get_best_move()
                        if not move.isnumeric() or random.random() > 0.8 or not connect4.is_legal_move(int(move)):
                            move = connect4.get_random_move()
                    else:
                        move = connect4.get_random_move()
                    connect4.perform_move(int(move), -1)
                
                if connect4.has_winner() == 1:
                    response = connect4.talk('The game is over! I lost!')
                elif connect4.has_winner() == -1:
                    response = connect4.talk('The game is over! I won!')
                else:
                    response = connect4.talk('Nice Move! I made a move as well!', prior=data.get("move"))
        
            else:
                response = connect4.talk("You can't make that move. Choose a different one!")
        else:
            response = connect4.talk("That isn't a valid number. Choose a different one!")
    else:
        response = connect4.talk("That isn't a number. Choose a different one!")

    return jsonify({"board" : connect4.get_board(), "response" : response})

@app.route('/api/contest_moves', methods=['POST'])
def contest_moves():
    moves = contest.get_move_choices()
    key_list = list(moves.keys())
    ret_dict = {}
    ret_dict['m1Num'] = key_list[0]
    ret_dict['m1Name'] = moves[key_list[0]][0]
    ret_dict['m1Desc'] = moves[key_list[0]][1]
    ret_dict['m2Num'] = key_list[1]
    ret_dict['m2Name'] = moves[key_list[1]][0]
    ret_dict['m2Desc'] = moves[key_list[1]][1]
    ret_dict['m3Num'] = key_list[2]
    ret_dict['m3Name'] = moves[key_list[2]][0]
    ret_dict['m3Desc'] = moves[key_list[2]][1]
    return jsonify(ret_dict)

@app.route('/api/contest_pet_talk', methods=['POST'])
def pet_talk():
    data = request.json
    user_prompt = data.get("discussion")
    moves = [data.get("m1Num"), data.get("m2Num"), data.get("m3Num")]

    return jsonify({"response": contest.advise_player(user_prompt, moves)})

@app.route('/api/run_contest', methods=['POST'])
def run_contest():
    pass


@app.route('/api/feed_talk_to_pet', methods=['POST'])
def generate_convo_with_pet():

    data = request.json
    likes_sweet = data.get("likes_sweet")
    description = data.get("description")
    talkative = data.get("talkative")
    conversation_style = data.get("conversationStyle")

    answer = feedPetAction.talk_to_pet(description, likes_sweet, talkative, conversation_style)

    return jsonify({"answer": answer})


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

    narration = "You use your magical powers to summon some food."

    return jsonify({"food": food_dict, "food_type": food_pair, "narration": narration})

@app.route('/api/feed', methods=['POST'])
def generate_feed_pet():

    data = request.json
    name = data.get("name")
    food_choice = data.get("food")
    food_type = data.get("food_type")
    hunger_level = data.get('hunger_level')
    happiness_level = data.get('happiness_level')
    likes_sweet = data.get('likes_sweet')
    conversation_style = data.get('conversationStyle')
    talkative = data.get('talkative')
    
    describe = f"You feed your pet {food_choice}."  
    
    if hunger_level < 0:
        pet_answer = feedPetAction.pet_too_full_answer(False, food_choice, talkative, conversation_style, describe, likes_sweet)

    elif food_type == "rotten":
        hunger_level = hunger_level - 1
        happiness_level = happiness_level - 2  
        # nature of conversation, fav_food, food_choice, talkative, conversation_style
        pet_answer = feedPetAction.pet_answer("rotten", False, food_choice, talkative, conversation_style, describe, likes_sweet)
    elif (likes_sweet and food_type == "sweet") or (not likes_sweet and food_type == "savory"):
        hunger_level = hunger_level - 2
        happiness_level = happiness_level + 3
        # nature of conversation, fav_food, food_choice, talkative, conversation_style
        pet_answer = feedPetAction.pet_answer("thank", True, food_choice, talkative, conversation_style, describe, likes_sweet)
    else:
        hunger_level = hunger_level - 2
        happiness_level = happiness_level + 1
        # nature of conversation, fav_food, food_choice, talkative, conversation_style
        pet_answer = feedPetAction.pet_answer("thank", False, food_choice, talkative, conversation_style, describe, likes_sweet)

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

@app.route('/api/pet_load_chat', methods=['POST'])
def load_pet_for_chat():
    data = request.json
    pet = data.get('pet')
        
    chatbot.load_personality(pet)
    feedPetAction.load_personality(pet)
    ttt.set_attributes(
        pet.get("identity").get("name"), 
        pet.get("identity").get("physical_details"), 
        pet.get("personality").get("fav_color"), 
        pet.get("personality").get("competitive"),
        pet.get("personality").get("conversationStyle"))
    connect4.set_attributes(
        pet.get("identity").get("name"), 
        pet.get("identity").get("physical_details"), 
        pet.get("personality").get("fav_color"), 
        pet.get("personality").get("competitive"),
        pet.get("personality").get("conversationStyle"))
    
    return jsonify({"response": "good"})

def play_audio_async(answer, voice="random"):
    # Turn the response into audio and then play it
    speech_file_path = chatbot.text_to_audio(answer, voice)
    chatbot.speak(speech_file_path)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
