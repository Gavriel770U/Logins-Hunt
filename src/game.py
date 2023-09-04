import pygame

ROWS: int = 3
COLS: int = 3
DEC: int = 1
BOARD_DRAW_RATIO: int = 2
BOARD_PLAYER_CHARS: list = ['X', 'O']
MAX_PLAYERS: int = 2

'''
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|    

                     _____   ___  ___  ___ _____   ___________   ___ _____ _____ _____ 
                    |  __ \ / _ \ |  \/  ||  ___| |  _  | ___ \ |_  |  ___/  __ \_   _|
                    | |  \// /_\ \| .  . || |__   | | | | |_/ /   | | |__ | /  \/ | |  
                    | | __ |  _  || |\/| ||  __|  | | | | ___ \   | |  __|| |     | |  
                    | |_\ \| | | || |  | || |___  \ \_/ / |_/ /\__/ / |___| \__/\ | |  
                     \____/\_| |_/\_|  |_/\____/   \___/\____/\____/\____/ \____/ \_/ 

'''

class Game:
    def __init__(self, multiplayer=False, board=None) -> None:
        self.multiplayer = multiplayer
        self.board = [' ' for _ in range(COLS)] * ROWS
        self.player_turn = 0 # 0 -> first player, 1 -> second player
        self.player_char = BOARD_PLAYER_CHARS[self.player_turn]

    def print_board(self) -> None:
        # for DEBUG
        for i in range(ROWS):
            for j in range(COLS):
                if j != COLS-DEC:
                    print(self.board[j], end = '|')
                else:
                    print(self.board[j])
            if i != ROWS-DEC:
                print('-' * (COLS*BOARD_DRAW_RATIO))
            else:
                print('')

'''
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|  '''