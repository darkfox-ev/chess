# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:53:02 2019

@author: dyeadon
"""

import re

## helper functions ##################################
def square_name(_file,_rank):
    return chr(_file + 97) + str(_rank + 1)     #chr(97) = 'a'

def square_coord(name):
    return ord(name[0]) - 97, int(name[1]) - 1

###################################################### 

class Piece:
    def __init__(self, colour, position = None):
        self.position = position # tuple(file, rank)
        self.colour = colour # white = 0, black = 1

    def set_position(self, position):
        self.position = position
        
    def get_position(self, use_notation = False):
        if not self.position:
            return 'not placed'
        if use_notation:
            return square_name(*self.position)
        else:
            return self.position
        
class Pawn(Piece):
    def __init__(self, colour, position = None):
        Piece.__init__(self,colour,position)
        self.name = 'P' if self.colour == 0 else 'p'
    def moves(self):
        _moves = []
        offset = 1 - self.colour * 2
        if not self.position:
            return None
        _file = self.position[0]
        _rank = self.position[1]

        if self.colour == 0 and _rank == 1:
            _moves.append((_file, 3))
        if self.colour == 1 and _rank == 6:
            _moves.append((_file, 4))
        if _rank + offset >= 0 and _rank + offset <= 7:
            _moves.append((_file, _rank + offset))
            if _file == 0:
                _moves.append((_file+1,_rank + offset))
            elif _file == 7:
                _moves.append((_file-1,_rank+offset))
            else:
                _moves.append((_file+1, _rank+offset))
                _moves.append((_file-1, _rank+offset))
        return _moves

class Bishop(Piece):
    def __init__(self, colour, position = None):
        Piece.__init__(self,colour,position)
        self.name = 'B' if self.colour == 0 else 'b'
        
    def moves(self):
        _moves = []
        if not self.position:
            return None
        _file = self.position[0]
        _rank = self.position[1]
        
        for i,j in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            k = 1
            while _file + k*i >= 0 and \
                  _file + k*i <= 7 and \
                  _rank + k*j >= 0 and \
                  _rank + k*j <= 7:
                _moves.append((_file + k*i, _rank + k*j))
                k = k+1
        return _moves
        
class Knight(Piece):
    def __init__(self, colour, position = None):
        Piece.__init__(self,colour,position)
        self.name = 'N' if self.colour == 0 else 'n'
        
    def moves(self):
        _moves = []
        if not self.position:
            return None
        _file = self.position[0]
        _rank = self.position[1]
        
        for i,j in [(2,1),(-2,1),(2,-1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)]:
            if _file + i >= 0 and _file + i <=7 and \
               _rank + j >= 0 and _rank + j <=7:
                _moves.append((_file + i, _rank + j))
        return _moves

class Rook(Piece):
    def __init__(self, colour, position = None):
        Piece.__init__(self,colour,position)
        self.name = 'R' if self.colour == 0 else 'r'

    def moves(self):
        _moves = []
        if not self.position:
            return None
        _file = self.position[0]
        _rank = self.position[1]
        
        for i,j in [(1,0),(-1,0),(0,1),(0,-1)]:
            k = 1
            while _file + k*i >= 0 and \
                  _file + k*i <= 7 and \
                  _rank + k*j >= 0 and \
                  _rank + k*j <= 7:
                _moves.append((_file + k*i, _rank + k*j))
                k = k+1
        return _moves
       
class Queen(Piece):
    def __init__(self, colour, position = None):
        Piece.__init__(self,colour,position)
        self.name = 'Q' if self.colour == 0 else 'q'

    def moves(self):
        _moves = []
        if not self.position:
            return None
        _file = self.position[0]
        _rank = self.position[1]
        
        for i,j in [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]:
            k = 1
            while _file + k*i >= 0 and \
                  _file + k*i <= 7 and \
                  _rank + k*j >= 0 and \
                  _rank + k*j <= 7:
                _moves.append((_file + k*i, _rank + k*j))
                k = k+1
        return _moves
        
class King(Piece):
    def __init__(self, colour, position = None):
        Piece.__init__(self,colour,position)
        self.name = 'K' if self.colour == 0 else 'k'

    def moves(self):
        _moves = []
        if not self.position:
            return None
        _file = self.position[0]
        _rank = self.position[1]
        
        for i,j in [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]:
            if _file + i >= 0 and _file + i <=7 and \
               _rank + j >= 0 and _rank + j <=7:
                _moves.append((_file + i, _rank + j))
        return _moves

class Square:
    def __init__(self, _file, _rank):
        self.file = _file
        self.rank = _rank
        self.name = square_name(_file, _rank)
        self.piece = None
    
    
class Board:
    def __init__(self):
        self.squares = []
        for i in range(8):
            temp = []
            for j in range(8):
                sq = Square(i,j)
                temp.append(sq)
            self.squares.append(temp)

    def place_piece(self, piece, position):
        _file, _rank = position
        self.squares[_file][_rank].piece = piece
        piece.set_position(position)
                
    def setup(self):
        for i in range(8):
            for j in range(8):
                if self.squares[i][j].piece:
                    self.squares[i][j].piece = None
        
        for i in range(2):
            for j in range(8):
                self.place_piece(Pawn(i),(j, 1 + i*5))
                
            self.place_piece(Rook(i), (0, 0 + i*7))
            self.place_piece(Rook(i), (7, 0 + i*7))
            self.place_piece(Knight(i), (1, 0 + i*7))
            self.place_piece(Knight(i), (6, 0 + i*7))
            self.place_piece(Bishop(i), (2, 0 + i*7))
            self.place_piece(Bishop(i), (5, 0 + i*7))
            self.place_piece(Queen(i), (3, 0 + i*7))
            self.place_piece(King(i), (4, 0 + i*7))
            
        self.print_board()
        return self
            
    def print_board(self):
        
        TOP_LEFT = u'\u2554'
        TOP_RIGHT = u'\u2557'
        HORIZ = u'\u2550'
        VERT = u'\u2551'
        BOT_LEFT = u'\u255a'
        BOT_RIGHT = u'\u255d'
        
        
        print TOP_LEFT + 17 * HORIZ + TOP_RIGHT
        for j in range(7,-1,-1): #rank
            temp = VERT + ' '
            for i in range(8): #file
                if self.squares[i][j].piece:
                    temp = temp + self.squares[i][j].piece.name + ' '
                else:
                    temp = temp + '_' + ' '
            print temp + VERT + ' ' + str(j+1)
        print BOT_LEFT + 17 * HORIZ + BOT_RIGHT
        print '  a b c d e f g h'
        
    def get_piece(self, position):
        _file, _rank = position
        P = self.squares[_file][_rank].piece
        if P:
            self.squares[_file][_rank].piece = None
            P.set_position(None)
            return P
        else:
            return None
        

    def move_piece(self, from_pos, to_pos):
        P = self.get_piece(from_pos)
        if not P:
            raise ValueError('From position is not occupied')
        
        P2 = self.get_piece(to_pos)
        self.place_piece(P,to_pos)
        self.print_board()
        return True
    
    def find_piece(self, piece_name):
        #returns list of squares containing piece
        result = []
        for i in range(8):
            for j in range(8):
                try:
                    if self.squares[i][j].piece.name == piece_name:
                        result.append((i,j))
                except AttributeError:
                    pass
        return result
    
    def isblocked(self,from_pos, to_pos):
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        temp_pos = from_pos
        if dx == 0 and dy == 0:
            # no move therefore not blocked
            return False
        elif dx == 0 or dy == 0 or dx == dy or dx == -dy:
            #moving along the rank or file
            xdirection = 0
            ydirection = 0
            if dy > 0 and dx == 0:
                ydirection = 1
            elif dy < 0 and dx == 0:
                ydirection = -1
            elif dx > 0 and dy == 0:
                xdirection = 1
            elif dx < 0 and dy == 0:
                xdirection = -1
            elif dx == dy and dx > 0:
                xdirection = 1
                ydirection = 1
            elif dx == dy and dx < 0:
                xdirection = -1
                ydirection = -1
            elif dx == -dy and dx < 0:
                xdirection = -1
                ydirection = 1
            else:
                xdirection = 1
                ydirection = -1
            
            while temp_pos != to_pos:
                
                temp_pos = (temp_pos[0] + xdirection,temp_pos[1] + ydirection)
                print from_pos, to_pos, temp_pos, xdirection, ydirection
                if self.squares[temp_pos[0]][temp_pos[1]].piece and temp_pos != to_pos:
                    return True
            return False
        
        elif dx == dy or dx == -dy:
            #moving diganonally
            pass
        else:
            #Knight move, therefore not blocked
            return False
    
    def find_moves(self, from_pos):
        #return a list of possible destination sqaures given starting square
        P = self.squares[from_pos[0]][from_pos[1]].piece
        #moves = [dest for dest in P.moves() if True]
        moves = [dest for dest in P.moves() if not self.isblocked(from_pos,dest)]
        
        return moves
    
    def move_parser(self, colour, move):
        """ parse from Algebraic chess notation to coordinate system
        
        1. pawn move e.g. e4 (first character is lower case a through h)
        2. pawn capture e.g. exd5
        3. other piece move e.g. Nf6
        4. other piece move with clarifcation e.g. Rad1
        etc... """
        
        patterns = {'pawn': '^[a-h]{1}[1-8]{1}[+#]{0,1}$',
                    'pawn takes': '^[a-h]{1}x[a-h]{1}[1-8]{1}[+#]{0,1}$',
                    'non-pawn': '^[KQRBN]{1}[a-h]{1}[1-8]{1}[+#]{0,1}$',
                    'non-pawn w f': '^[KQRBN]{1}[a-h]{1}[a-h]{1}[1-8]{1}[+#]{0,1}$',
                    'non-pawn w r': '^[KQRBN]{1}[1-8]{1}[a-h]{1}[1-8]{1}[+#]{0,1}$',
                    'non-pawn w fr': '^[KQRBN]{1}([a-h][1-8]){1}[a-h]{1}[1-8]{1}[+#]{0,1}$',
                    'non-pawn takes': '^[KQRBN]{1}x[a-h]{1}[1-8]{1}[+#]{0,1}$',
                    'non-pawn w f takes': '^[KQRBN]{1}[a-h]{1}x[a-h]{1}[1-8]{1}[+#]{0,1}$',
                    'non-pawn w r takes': '^[KQRBN]{1}[1-8]{1}x[a-h]{1}[1-8]{1}[+#]{0,1}$',
                    'non-pawn w fr takes': '^[KQRBN]{1}([a-h][1-8]){1}x[a-h]{1}[1-8]{1}[+#]{0,1}$'
                    }
        
        label = None
        for key,value in patterns.items():
            if re.match(value,move):
                label = key
        
        if not label:
            raise ValueError('Not a valid expression')
        
        offset = colour * 2 - 1 #now white = -1, black = 1
        
        
        if label == 'pawn':
            to_pos = square_coord(move)
            
            for offset in (offset, offset * 2):
                if to_pos[1] + offset > 7 or to_pos[1] + offset < 0:
                    raise ValueError('Not a valid move')
                P = self.squares[to_pos[0]][to_pos[1] + offset].piece
                if not P or P.name.upper() != 'P':
                    continue
                from_pos = to_pos[0], to_pos[1] + offset
            if not from_pos:
                raise ValueError('Not a valid move')
                    
        if label == 'pawn takes':
            to_pos = square_coord(move[2:])
            offset = colour * 2 - 1
            from_file = ord(move[0]) - 97
            P = self.squares[from_file][to_pos[1] + offset].piece
            if not P or P.name.upper() != 'P':
                raise ValueError('Not a valide move')
            from_pos = from_file, to_pos[1] + offset
        
        if label == 'non-pawn' or label == 'non-pawn takes':
            piece_name = move[:1].lower() if colour == 1 else move[:1].upper()
            if label == 'non-pawn':
                to_pos = square_coord(move[1:3])
            else:
                to_pos = square_coord(move[2:4])
            
            for i in range(8):
                for s in self.squares[i]:
                    if s.piece and s.piece.name == piece_name:
                        if to_pos in self.find_moves(s.piece.get_position()):
                            from_pos = s.piece.get_position()
                        
                
            #need to scan through squares and look for particular piece that can make move
            #pass
            
        return (from_pos, to_pos)
                
    def move(self, colour, move):
        from_pos, to_pos = self.move_parser(colour, move)
        self.move_piece(from_pos, to_pos)
            
if __name__ == '__main__':
    B = Board().setup()
    B.move(0,'e4')
    B.move(1,'e5')
    #B.move(0,'Nf6')
    
    