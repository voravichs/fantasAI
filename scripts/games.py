import random
import math
import os
import enum
from typing import Annotated
from getpass import getpass
import openai
from openai import OpenAI

class Game():
  def __init__(self):
    self.client = openai.OpenAI(base_url="https://oai.hconeai.com/v1", api_key=os.getenv('HELICONE_API_KEY'))
    self.name = ""
    self.physical_details = ""
    self.fav_color = ""
    self.competitive = True
    self.conversationStyle = ""

  def get_attributes(self):
    return (self.name, self.physical_details, self.fav_color, self.competitive)
  
  def set_attributes(self, name, phys, color, compet, conversationStyle):
    self.name = name
    self.physical_details = phys
    self.fav_color = color
    self.competitive = compet
    self.conversationStyle = conversationStyle

  def talk(self, context, prior=""):
    not_competitive = "" if self.competitive else "not "
    
    if prior == "":
      personality = f"""You are a friendly tamagochi-like pet named {self.name}.
        You look like this: {self.physical_details}.
        Your favorite color is {self.fav_color}.
        You are {not_competitive}competitive.
        Your conversation style is: {self.conversationStyle}.
        Rewrite the following text in a style matching your personality and include personal details when appropriate."""
      
      messages=[
          {
            "role": "system",
            "content": personality
          },
          {
            "role": "user",
            "content": context
          }
        ]
    else:
      personality = f"""You are a friendly tamagochi-like pet named {self.name}.
        You look like this: {self.physical_details}.
        Your favorite color is {self.fav_color}.
        You are {not_competitive} competitive.
        Your conversation style is: {self.conversationStyle}.
        The first statement you must respond to. The second statement you must rewrite.
        Rewrite the assistant text in a style matching your personality and include personal details when appropriate.
        Make sure to respond to what the user said as well."""
      
      messages=[
          {
            "role": "system",
            "content": personality
          },
          {
            "role": "user",
            "content": prior
          },
          {
            "role": "user",
            "content": context
          }
        ]

    response = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content

class TicTacToe(Game):

    def __init__(self, board):
      super().__init__()
      self.board = board
      self.wins = [[(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
                  [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
                  [(0,0),(1,1),(2,2)], [(2,0),(1,1),(0,2)]]

    def __str__(self):
      disp_board = [["O" if col == -1 else "X" if col == 1 else " " for col in row] for row in self.get_board()]
      ret_str = disp_board[0][0] + " | " + disp_board[0][1] + " | " + disp_board[0][2] + "\n"
      ret_str += "---------\n"
      ret_str += disp_board[1][0] + " | " + disp_board[1][1] + " | " + disp_board[1][2] + "\n"
      ret_str += "---------\n"
      ret_str += disp_board[2][0] + " | " + disp_board[2][1] + " | " + disp_board[2][2]
      return ret_str

    def get_board(self):
      return self.board

    def reset(self):
      self.board  = [[0,0,0], [0,0,0], [0,0,0]]

    def is_legal_move(self, row, col):
      if self.get_board()[row][col] == 0:
        return True
      else:
        return False

    def legal_moves(self):
      moves = []
      for r in range(3):
        for c in range(3):
          if self.board[r][c] == 0:
            yield r, c


    def perform_move(self, row, col, player):
        if self.is_legal_move(row, col):
            self.board[row][col] = player

    def has_winner(self):
      for win in self.wins:
        if self.board[win[0][0]][win[0][1]] == self.board[win[1][0]][win[1][1]] == self.board[win[2][0]][win[2][1]]:
          return self.board[win[0][0]][win[0][1]]
      return 0

    def game_over(self):
      return self.has_winner() != 0 or len(list(self.legal_moves())) == 0

    def copy(self):
        return TicTacToe([[col for col in row] for row in self.get_board()], self.competitive)

    def successors(self, player):
        for move in self.legal_moves():
            ret_board = self.copy()
            ret_board.perform_move(move[0], move[1], player)
            yield move, ret_board

    def get_random_move(self):
        return random.choice(list(self.legal_moves()))

    def get_llm_move(self, board_str):
      response = self.client.chat.completions.create(
        model="gpt-4",
        messages=[
          {
            "role": "system",
            "content": '''
            You are playing a game of Tic Tac Toe. Your goal is to state the best move given a board in the form of a 3x3 array.
            Spaces you own are notated as -1, spaces your opponent owns are notated as 1, empty spaces are 0. The space you will
            make a move on must be an empty space listed as a 0.
            To describe your move, you will return a number from 0 to 8 inclusive that relates to the space you are talking about. 
            0 is the top left and the number increases going from left to right then down.
            '''
          },
          {
            "role": "user",
            "content": "[[1,1,-1], [0,1,-1], [0,0,0]]"
          },
          {
            "role": "assistant",
            "content": "8"
          },
          {
            "role": "user",
            "content": board_str
          }
        ],
        temperature=1,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      return response.choices[0].message.content

    def get_best_move(self):
      return self.get_llm_move(str(self.get_board()))

    def get_space(self, space_str):
      response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {
            "role": "system",
            "content": "The user is describing what space to place a piece on a tic tac toe board. They will describe it and you will return a number from 0 to 8 inclusive that relates to the space they were talking about. 0 is the top left and the number increases going from left to right then down."
          },
          {
            "role": "user",
            "content": "I want to place my X in the middle square to the right"
          },
          {
            "role": "assistant",
            "content": "5"
          },
          {
            "role": "user",
            "content": space_str
          }
        ],
        temperature=1,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      return response.choices[0].message.content

class ConnectFour(Game):

    def __init__(self, board):
      super().__init__()
      self.board = board

    def __str__(self):
      disp_board = [["O" if col == -1 else "X" if col == 1 else " " for col in row] for row in self.get_board()]
      ret_str = ""
      for r in range(len(disp_board)):
        ret_str += disp_board[r][0] + " | " + disp_board[r][1] + " | " + disp_board[r][2] + " | " + disp_board[r][3] + " | " + disp_board[r][4] + " | " + disp_board[r][5] + " | " + disp_board[r][6] + "\n"
        ret_str += "-------------------------\n"
      return ret_str


    def get_board(self):
      return self.board

    def reset(self):
      self.board  = [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]]

    def is_legal_move(self, col):
      if self.get_board()[0][col] == 0:
        return True

    def legal_moves(self):
      for c in range(len(self.get_board()[0])):
        if self.get_board()[0][c] == 0:
          yield c

    def perform_move(self, col, player):
      if self.is_legal_move(col):
        for r in range(5,-1,-1):
          if self.get_board()[r][col] == 0:
            self.board[r][col] = player
            return None

    def has_winner(self):
      board = self.get_board()
      #horizontal win
      for row in range(len(board)):
        for col in range(len(board[0])-3):
          if (board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3]) and board[row][col] != 0:
            return board[row][col]

      #vertical win
      for row in range(len(board)-3):
        for col in range(len(board[0])):
          if (board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]) and board[row][col] != 0:
            return board[row][col]

      #diagonal left-right up win
      for row in range(3, len(board)):
        for col in range(len(board[0])-3):
          if (board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]) and board[row][col] != 0:
            return board[row][col]

      #diagonal left-right down win
      for row in range(len(board)-3):
        for col in range(3, len(board[0])):
          if (board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3]) and board[row][col] != 0:
            return board[row][col]

      return 0

    def game_over(self):
      return self.has_winner() != 0 or len(list(self.legal_moves())) == 0

    def copy(self):
        return ConnectFour([[col for col in row] for row in self.get_board()], self.competitive)

    def successors(self, player):
        for move in self.legal_moves():
            ret_board = self.copy()
            ret_board.perform_move(move, player)
            yield move, ret_board

    def get_random_move(self):
        return random.choice(list(self.legal_moves()))
    
    def get_llm_move(self, board_str):
      response = self.client.chat.completions.create(
        model="gpt-4",
        messages=[
          {
            "role": "system",
            "content": '''
            You are playing a game of Connect 4. Your goal is to state the best move given a board in the form of a 6x7 array.
            Spaces you own are notated as -1, spaces your opponent owns are notated as 1, empty spaces are 0. The column you will
            make a move on must be a column with a 0 at some point in the column.
            The goal of the game is to get 4 of your pieces in a row while preventing your opponent from getting four in a row of their own. 
            To describe your move, you will return a number from 0 to 6 inclusive that relates to the column you are talking about.
            0 is the leftmost column and the number increases going from left to right.
            '''
          },
          {
            "role": "user",
            "content": "[[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,-1,1], [0,0,0,0,-1,-1,-1], [1,1,1,-1,-1,1,1]]"
          },
          {
            "role": "assistant",
            "content": "6"
          },
          {
            "role": "user",
            "content": "[[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [1,1,1,0,-1,-1,0]]"
          },
          {
            "role": "assistant",
            "content": "3"
          },
          {
            "role": "user",
            "content": board_str
          }
        ],
        temperature=1,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      return response.choices[0].message.content

    def get_best_move(self):
      return self.get_llm_move(str(self.get_board()))

    def get_space(self, space_str):
      response = self.client.chat.completions.create(
        model="gpt-4",
        messages=[
          {
            "role": "system",
            "content": "The user is describing what column to place a piece in a game of connect four. They will describe it and you will return a number from 0 to 6 inclusive that relates to the column they were talking about. 0 is the leftmost column and the number increases going from left to right."
          },
          {
            "role": "user",
            "content": "I want to place my piece one place to the left of the middle. "
          },
          {
            "role": "assistant",
            "content": "2"
          },
          {
            "role": "user",
            "content": "Two right of the middle row."
          },
          {
            "role": "assistant",
            "content": "5"
          },
          {
            "role": "user",
            "content": space_str
          }
        ],
        temperature=1,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      return response.choices[0].message.content


class MagicContest(Game):

    def __init__(self):
      super().__init__()
      self.name = ""
      self.physical_details = ""
      self.fav_color = ""
      self.talkative = True
      self.competitive = True
      self.quicklyHungry = True
      self.likesSweet = True
      self.happiness = 0
      self.hunger = 0
      self.conversationStyle = ""
      self.set_energy(100)
      self.goal = 100
      self.reset()
      '''
        0 : 1.5 multiplier if correct color
        1 : All point gains are negative & goal = -70
        2 : get 30 points
        3 : if talked to pet, 1.5 multiplier
        4 : goal lowered to 70
      '''
      self.opener_moves = {0 : ("Color Coordination", "Coordinate a routine with your pet so the magic show has a colorful theme."),
                            1 : ("So Bad It's Good", "Set up a plan with your pet where if you fail so spectacularly you may just win."),
                            2 : ("Head Start","Get started with your show early. Who needs plans when you have more magic then anyone else."),
                            3 : ("Pep Talk","Talk to your pet and motivate them to do their best."),
                            4 : ("Low Expectations", "Establish low expectations with the judges. If they expect less it should be easier to pass.")
                            }
      
      '''
        0 : 50 points if competative. 10 otherwise
        1 : 60 - hunger points
        2 : 10 + happiness points
        3 : 10 * # questions points
        4 : 20 points, 50 + happiness - hunger % to go again
      '''
      self.main_moves = {0 : ("Driven Demolition", "Focus your pet on winning by having them use magic to destroy tough materials."),
                         1 : ("Food Frenzy", "Have your pet summon a lot of food for the judges... and some for the pet as well."),
                         2 : ("Cheerful Confetti", "Leverage your pet's positive energy and perform cheerful magic displays."),
                         3 : ("Lecture Learning", "Have your pet use their magic to enhance their voice and performance to charm the judges and the crowd."),
                         4 : ("Combo Craze", "Have your pet perform a quick magic display. If they are motivated it may just allow your pet to perform again.")
                         }
      
      '''
        0 : 50 points
        1 : remaining energy points
        2 : Take another main phase, with no closer at the end
      '''
      self.closer_moves = {0 : ("End it With a Bang", "Get your pet to finish their show with a large magical display."),
                           1 : ("One Last Push", "Have your pet expend all their energy for a final magical performance."),
                           2 : ("Encore", "Have your pet perform another main performance instead of a closer")
                         }

    def reset(self):
      self.phase = 0
      self.points = 0
      self.curr_energy = self.max_energy
      self.multiplier = 1
      self.go_to_main = False
      self.closer = True
      self.moves = []

    def set_energy(self, max_energy):
      self.max_energy = max_energy
      self.curr_energy = max_energy

    def get_energy(self):
      return (self.max_energy, self.curr_energy)
    
    def set_phase(self, phase):
      self.phase = phase

    def get_phase(self):
      return self.phase

    def set_attributes(self, name, phys, color, talk, compet, hunger_speed, sweets, happiness, hunger, conversation):
      self.name = name
      self.physical_details = phys
      self.fav_color = color
      self.talkative = talk
      self.competitive = compet
      self.quicklyHungry = hunger_speed
      self.likesSweet = sweets
      self.happiness = happiness
      self.hunger = hunger
      self.conversationStyle = conversation

    def get_attributes(self):
      return (self.name, self.physical_details, self.fav_color, self.talkative, 
              self.competitive, self.quicklyHungry, self.likesSweet, self.happiness, self.hunger, self.conversationStyle)

    def has_won(self):
      return self.points >= self.goal
    
    def get_move_choices(self):
      if self.phase == 0:
        dict_choice = self.opener_moves
      elif self.phase == 1:
        dict_choice = self.main_moves
      else:
        dict_choice = self.closer_moves
      
      random_moves = random.sample(list(dict_choice.keys()), 3)

      ret_dict = {}
      for val in random_moves:
        ret_dict[val] = self.opener_moves[val]

      return ret_dict
      
    def get_move(self, move_num):
      if self.phase == 0:
        return self.opener_moves[move_num]
      elif self.phase == 1:
        return self.main_moves[move_num]
      else:
        return self.closer_moves[move_num]
    
    def apply_opener(self, move_num, color_select, num_convo):
      self.moves.append(self.opener_moves[move_num][1])
      if move_num == 0:
        if color_select == self.fav_color:
          self.multiplier = 1.5
      elif move_num == 1:
        self.multiplier = -1
        self.goal = -70
      elif move_num == 2:
        self.points += 30
      elif move_num == 3:
        if num_convo > 0:
          self.multiplier = 1.5
      elif move_num == 4:
        self.goal = 70

    def apply_main(self, move_num, color_select, num_convo):
      self.moves.append(self.main_moves[move_num][1])
      if move_num == 0:
        if self.competitive:
          self.points += 50
        else:
          self.points += 10
      elif move_num == 1:
        self.points += (60 - self.hunger)
      elif move_num == 2:
        self.points += 10 + self.happiness
      elif move_num == 3:
        self.points += (10*num_convo)
      elif move_num == 4:
        self.points += 20
        if random.random() > (50 - self.happiness + self.hunger):
          self.go_to_main = True

    def apply_closer(self, move_num, color_select, num_convo):
      self.moves.append(self.closer_moves[move_num][1])
      if move_num == 0:
        self.points += 50
      elif move_num == 1:
        self.points += self.curr_energy
      elif move_num == 2:
        self.go_to_main = True
        self.closer = False

    def evaluate_move(self, move_num, color_select, num_convo):
      if self.phase == 0:
        if move_num == 0:
          if color_select == self.fav_color:
            return "is a good choice"
          else:
            return "is a bad choice"
        elif move_num == 1:
          return "is a good choice if they are going for negative points"
        elif move_num == 2:
          return "is a good choice"
        elif move_num == 3:
          if num_convo > 0:
            return "is a good choice"
          else:
            return "is a bad choice"
        elif move_num == 4:
          return "is a good choice"
      elif self.phase == 1:
        if move_num == 0:
          if self.competitive:
            self.points += 50
          else:
            self.points += 10
        elif move_num == 1:
          if self.hunger < 20:
            return "is a good choice"
          else:
            return "is a bad choice"
        elif move_num == 2:
          if self.happiness > 30:
            return "is a good choice"
          else:
            return "is a bad choice"
        elif move_num == 3:
          if num_convo > 3:
            return "is a good choice"
          else:
            return "is a bad choice"
        elif move_num == 4:
          return "is a good choice if they want to take risks"
      elif self.phase == 2:
        if move_num == 0:
          if self.points >= self.goal - 50:
            return "is a good choice"
          else:
            return "is a bad choice"
        elif move_num == 1:
          if self.points >= self.goal - self.curr_energy:
            return "is a good choice"
          else:
            return "is a bad choice"
        elif move_num == 2:
          return "is a good choice if they want to take risks"
        
    def narrate_game(self):
      not_competitive = "" if self.competitive else "not "
      not_talkative = "" if self.talkative else "not "
      foods = "sweet" if self.likesSweet else "savory"
      system_prompt = f"""You are the event announcer for a magical talent show.
        You are summerize the events of the latest contestant in no more than 3 paragraphs.
        These events are brief summeries seperated by commas that should be elaborated on using
        the contestant's features where possible.
        The contestant is a tamagochi-like pet named {self.name}.
        They look like this: {self.physical_details}.
        Their favorite color is {self.fav_color}.
        They are {not_competitive}competitive.
        They are {not_talkative}talkative.
        They like {foods} foods.
        Your conversation style is: {self.conversationStyle}.
        Rewrite the following series of events as specified."""
      
      user_prompt = ""
      for event in self.moves:
        user_prompt = user_prompt + ", " + str(event)
            
      response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {
            "role": "system",
            "content": system_prompt
          },
          {
            "role": "user",
            "content": user_prompt
          }
        ],
        temperature=1,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      return response.choices[0].message.content

    def advise_player(self, user_prompt, moves, color_select, num_convo):
      not_competitive = "" if self.competitive else "not "
      not_talkative = "" if self.talkative else "not "
      foods = "sweet" if self.likesSweet else "savory"

      system_prompt = f"""You are a friendly tamagochi-like pet named {self.name}.
        You look like this: {self.physical_details}.
        Your favorite color is {self.fav_color}.
        You are {not_competitive}competitive.
        You are {not_talkative}talkative.
        You like {foods} foods.
        Your conversation style is: {self.conversationStyle}.
        You are currently in a magical talent show. Your friend is advising you on how to perform. They have asked
        you a question and you are to respond to their question.
        If they ask about what move they should choose, you should hint and not directly state the following
        Move {self.get_move(moves[0])[0]} {self.evaluate_move(moves[0], color_select, num_convo)}
        Move {self.get_move(moves[1])[0]} {self.evaluate_move(moves[1], color_select, num_convo)}
        Move {self.get_move(moves[2])[0]} {self.evaluate_move(moves[2], color_select, num_convo)}
        """
            
      response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {
            "role": "system",
            "content": system_prompt
          },
          {
            "role": "user",
            "content": user_prompt
          }
        ],
        temperature=1,
        max_tokens=216,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      return response.choices[0].message.content