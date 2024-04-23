import random
import math
import os
import enum
from typing import Annotated
from getpass import getpass
import openai
from openai import OpenAI

class Game():
  def __init__(self, competitive):
    self.competitive = competitive
    self.client = openai.OpenAI(base_url="https://oai.hconeai.com/v1", api_key=os.getenv('HELICONE_API_KEY'))

  def get_attributes(self):
    return [self.competitive]

  def talk(self, context):
    return context

class TicTacToe(Game):

    def __init__(self, board, competitive):
      super().__init__(competitive)
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

    def __init__(self, board, competitive):
      super().__init__(competitive)
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
        model="gpt-3.5-turbo",
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
