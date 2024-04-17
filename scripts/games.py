import random
import math
import os
import enum
from typing import Annotated
from getpass import getpass
import openai
from openai import OpenAI

class Game():
  def __init__(self, cheerful, talkative, competitive):
    self.cheerful = cheerful
    self.talkative = talkative
    self.competitive = competitive
    self.client = openai.OpenAI(base_url="https://oai.hconeai.com/v1", api_key=os.getenv('HELICONE_API_KEY'))

  def get_attributes(self):
    return (self.cheerful, self.talkative, self.competitive)

  def talk(self, context):
    print(context)

class TicTacToe(Game):

    def __init__(self, board, cheerful, talkative, competitive):
      super().__init__(cheerful, talkative, competitive)
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
        return TicTacToe([[col for col in row] for row in self.get_board()], self.cheerful, self.talkative, self.competitive)

    def successors(self, player):
        for move in self.legal_moves():
            ret_board = self.copy()
            ret_board.perform_move(move[0], move[1], player)
            yield move, ret_board

    def get_random_move(self):
        return random.choice(list(self.legal_moves()))

    def alpha_beta_max(self, player, alpha, beta):

        if self.game_over():
            curr_val = len(list(self.legal_moves()))
            return None, curr_val, 1

        curr_val = -math.inf
        curr_leaves = 0
        curr_move = None

        for next_move, next_board in self.successors(player):
            best_move, best_val, total_leaves = next_board.alpha_beta_min(player * -1, alpha, beta)
            curr_leaves += total_leaves
            if best_val > curr_val:
                curr_val, curr_move = best_val, next_move
                alpha = max(alpha, curr_val)
            if curr_val >= beta:
                return curr_move, curr_val, curr_leaves
        return curr_move, curr_val, curr_leaves

    def alpha_beta_min(self, player, alpha, beta):
        if self.game_over():
            curr_val = len(list(self.legal_moves()))
            return None, curr_val, 1

        curr_val = math.inf
        curr_leaves = 0
        curr_move = None

        for next_move, next_board in self.successors(player):
            best_move, best_val, total_leaves = next_board.alpha_beta_max(player * -1, alpha, beta)
            curr_leaves += total_leaves
            if best_val < curr_val:
                curr_val, curr_move = best_val, next_move
                beta = min(beta, curr_val)
            if curr_val <= alpha:
                return curr_move, curr_val, curr_leaves
        return curr_move, curr_val, curr_leaves

    def get_best_move(self, player):
        return self.alpha_beta_max(player,-math.inf, math.inf)

    def get_space(self, space_str):
      response = client.chat.completions.create(
        model="gpt-4",
        messages=[
          {
            "role": "system",
            "content": "The user is describing what space to place a piece on a tic tac toe board. They will describe it and you will return a number from 0 to 8 inclusive that relates to the space they were talking about. 0 is the top left and the number increases going from left to right then down."
          },
          {
            "role": "user",
            "content": "I want to place my X in the middle square to the "
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
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      return response.choices[0].message.content

class ConnectFour(Game):

    def __init__(self, board, cheerful, talkative, competitive):
      super().__init__(cheerful, talkative, competitive)
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
        return ConnectFour([[col for col in row] for row in self.get_board()], self.cheerful, self.talkative, self.competitive)

    def successors(self, player):
        for move in self.legal_moves():
            ret_board = self.copy()
            ret_board.perform_move(move, player)
            yield move, ret_board

    def get_random_move(self):
        return random.choice(list(self.legal_moves()))

    #TODO
    def alpha_beta_max(self, player, limit, alpha, beta):

        if self.game_over() or limit == 0:
            curr_val = len(list(self.legal_moves()))
            return None, curr_val, 1

        curr_val = -math.inf
        curr_leaves = 0
        curr_move = None

        for next_move, next_board in self.successors(player):
            best_move, best_val, total_leaves = next_board.alpha_beta_min(player * -1, limit - 1, alpha, beta)
            curr_leaves += total_leaves
            if best_val > curr_val:
                curr_val, curr_move = best_val, next_move
                alpha = max(alpha, curr_val)
            if curr_val >= beta:
                return curr_move, curr_val, curr_leaves
        return curr_move, curr_val, curr_leaves

    #TODO
    def alpha_beta_min(self, player, limit, alpha, beta):
        if self.game_over() or limit == 0:
            curr_val = len(list(self.legal_moves()))
            return None, curr_val, 1

        curr_val = math.inf
        curr_leaves = 0
        curr_move = None

        for next_move, next_board in self.successors(player):
            best_move, best_val, total_leaves = next_board.alpha_beta_max(player * -1, limit - 1, alpha, beta)
            curr_leaves += total_leaves
            if best_val < curr_val:
                curr_val, curr_move = best_val, next_move
                beta = min(beta, curr_val)
            if curr_val <= alpha:
                return curr_move, curr_val, curr_leaves
        return curr_move, curr_val, curr_leaves

    def get_best_move(self, limit, player):
        #return self.get_random_move()
        return self.alpha_beta_max(player, limit, -math.inf, math.inf)

    def get_space(self, space_str):
      response = client.chat.completions.create(
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
            "content": space_str
          }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      return response.choices[0].message.content
    
class GameManager():
    def create_tictactoe_game(self, cheerful, talkative, competitive):
        return TicTacToe([[0,0,0], [0,0,0], [0,0,0]], cheerful, talkative, competitive)

    def create_connectfour_game(self, cheerful, talkative, competitive):
        return ConnectFour([[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]], cheerful, talkative, competitive)1    
    
    def playTicTacToe(self, cheerful, talkative, competitive):
        game = self.create_tictactoe_game(cheerful, talkative, competitive)

        game.talk("Time to start playing. You are X's, I am O's. You go first!")
        player = 1

        while not game.game_over():
            if player == 1:
                valid_choice = False
                while not valid_choice:
                    if not valid_choice:
                        game.talk('Ok, the board now looks like this:\n' + str(game))
                        game.talk('What square do you want to choose?: ')
                        val = game.get_space(input())
                        if val.isnumeric():
                            if -1<int(val)<9:
                                row = math.floor(int(val) / 3)
                                col = int(val) % 3
                                if game.is_legal_move(row, col):
                                    game.perform_move(row, col, player)
                                    valid_choice = True
                                else:
                                    game.talk("You can't make that move. Choose a different one!")
                            else:
                                game.talk("That isn't a valid number. Choose a different one!")
                        else:
                            game.talk("That isn't a number. Choose a different one!")
            else:
                game.talk('Ok, My turn!')
                if game.get_attributes()[2]:
                    move = game.get_best_move(player)[0]
                    if random.random() > 0.8 or move == None:
                        move = game.get_random_move()
                    else:
                        move = game.get_random_move()
                game.perform_move(move[0], move[1], player)

            player = player * -1

            if game.has_winner() == 1:
                winner = "You"
            elif game.has_winner() == -1:
                winner = "I"
            else:
                winner = "It's a tie, so nobody"
                game.talk('The game is over! ' + winner + " won!")
                game.talk('The final board looks like this:\n' + str(game))

    def playTicTacToe(self, cheerful, talkative, competitive):
        game = self.create_connectfour_game(cheerful, talkative, competitive)

        game.talk("Time to start playing. You are X's, I am O's. You go first!")
        player = 1

        while not game.game_over():
          if player == 1:
            valid_choice = False
            while not valid_choice:
              if not valid_choice:
                game.talk('Ok, the board now looks like this:\n' + str(game))
                game.talk('What row do you want to choose?: ')
                val = game.get_space(input())
                if val.isnumeric():
                  if -1<int(val)<7:
                    if game.is_legal_move(int(val)):
                      game.perform_move(int(val), player)
                      valid_choice = True
                    else:
                      game.talk("You can't make that move. Choose a different one!")
                  else:
                    game.talk("That isn't a valid number. Choose a different one!")
                else:
                  game.talk("That isn't a number. Choose a different one!")
          else:
            game.talk('Ok, My turn!')
            if game.get_attributes()[2]:
              move = game.get_best_move(10, player)[0]
              if random.random() > 0.8 or move == None:
                move = game.get_random_move()
            else:
              move = game.get_random_move()
            game.perform_move(move, player)

          player = player * -1

        if game.has_winner() == 1:
          winner = "You"
        elif game.has_winner() == -1:
          winner = "I"
        else:
          winner = "It's a tie, so nobody"
        game.talk('The game is over! ' + winner + " won!")
        game.talk('The final board looks like this:\n' + str(game))