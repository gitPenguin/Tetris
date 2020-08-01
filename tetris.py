import random

shapes = {'i': {'color': 'aqua',
                'name': 'i',
                'shape': [[0, 0, 0, 0],
                          [1, 1, 1, 1],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]},
          'j': {'color': 'blue',
                'name': 'j',
                'shape': [[1, 0, 0],
                          [1, 1, 1],
                          [0, 0, 0]]},
          'l': {'color': 'orange',
                'name': 'l',
                'shape': [[0, 0, 1],
                          [1, 1, 1],
                          [0, 0, 0]]},
          'o': {'color': 'yellow',
                'name': 'o',
                'shape': [[1, 1],
                          [1, 1]]},
          's': {'color': 'green',
                'name': 's',
                'shape': [[0, 1, 1],
                          [1, 1, 0],
                          [0, 0, 0]]},
          't': {'color': 'purple',
                'name': 't',
                'shape': [[0, 1, 0],
                          [1, 1, 1],
                          [0, 0, 0]]},
          'z': {'color': 'red',
                'name': 'z',
                'shape': [[1, 1, 0],
                          [0, 1, 1],
                          [0, 0, 0]]}}

offset_data = {'i': [[]]}

def overlap(list1, list2):
    shortest_width = len(list1) if len(list1) > len(list2) else len(list2)

    shortest_height = len(list1[0]) if len(list1[0]) > len(list2[0]) else len(list2[0])

    for i in range(0, shortest_width):
        for j in range(0, shortest_height):
            if list1[i][j] != None and list2[i][j] != None:
                return True
    
    return False

def movable(board, dir):
    x, y = dir
    if y == 1:
        for i in range(len(board)):
            if board[i][-1] != None:
                return False

    elif x == 1:
        for i in range(len(board[0])):
            if board[-1][i] != None:
                return False

    elif x == -1:
        for i in range(len(board[0])):
            if board[0][i] != None:
                return False

    return True

def piece_board(p, pos, spin):
    temp = [[None for i in range(board.height)] for i in range(board.width)]
    x, y = pos

    s = p['shape']

    for _ in range(spin):
        s = rotate(s)

    for i in range(len(s)):
        for j in range(len(s)):
            abs_x = int(x - (i - len(s) / 2))
            abs_y = int(y - (j - len(s) / 2))
            
            if not (abs_x < 0 or abs_y < 0 or abs_x >= len(temp) or abs_y >= len(temp[0])):
                if (s[i][j] == 1):
                    temp[abs_x][abs_y] = p['color']

    return temp

def rotate(arr):
    new = [[0 for i in range(len(arr))] for i in range(len(arr))]

    for i in range(len(arr)):
        for j in range(len(arr[0])):
            new[i][j] = arr[len(arr) - 1 - j][i]

    return new

class board:
    width = 10
    height = 24
    board = [[]]
    current = None
    pos = None
    spin = 0
    bag = []
    startpos = (5, 0)

    score = 0
    level = 0
    totat_lines = 0

    def init(self):
        self.board = [[None for i in range(self.height)] for i in range(self.width)]
        self.gen_piece()

    def move(self, dir):
        x1, y1 = self.pos
        x2, y2 = dir
        if not overlap(self.board, piece_board(self.current, (x1 + x2, y1 + y2), self.spin)) and movable(self.piece_board(), dir): 
            self.pos = (x1 + x2, y1 + y2) 

    def force_move(self, dir):
        x1, y1 = self.pos
        x2, y2 = dir

        self.pos = (x1+x2, y1+y2)

    def rotate(self, clockwise = True):
        if clockwise:
            self.spin += 3
        else:
            self.spin += 1

        self.spin = self.spin % 4

    def offset(self, p, pos):
        pass

    def check_clip():
        pass

    def hard_drop(self):
        while True:
            x, y = self.pos
            if overlap(self.board, piece_board(self.current, (x, y + 1), self.spin)) or not movable(self.piece_board(), (0, 1)):
                self.land()
                break
            else:
                self.move((0, 1))

    def gen_piece(self):
        if (len(self.bag) == 0):
            for key, value in shapes.items():
                self.bag.append(key)
            random.shuffle(self.bag)

        self.current = shapes[self.bag[0]]
        self.bag.pop(0)
        self.pos = (5, 0)

    def piece_board(self):
        return piece_board(self.current, self.pos, self.spin)

    def piece_to_board(self):
        temp = self.piece_board()

        for i in range(self.width):
            for j in range(self.height):
                if temp[i][j] != None:
                    self.board[i][j] = temp[i][j]
    
    def check_line(self):
        combo = 0

        for j in range(self.height):
            complete = True
            for i in range(self.width):
                if self.board[i][j] == None:
                    complete = False

            if complete:
                self.remove_line(j)
                combo += 1 

    def remove_line(self, row):
        for j in range(row - 1, 0, -1):
            print(j)
            for i in range(self.width):
                self.board[i][j + 1] = self.board[i][j]

        for i in range(self.width):
            self.board[i][0] = None

    def land(self):
        #score += 10 * (level + 1)
        self.piece_to_board()
        self.gen_piece()
        self.check_line()
    
    def cycle(self):
        x, y = self.pos

        if overlap(self.board, piece_board(self.current, (x, y + 1), self.spin)) or not movable(self.piece_board(), (0, 1)):
            self.land()

        else:
            self.move((0, 1))
    
    def get_board(self):
        return [self.board, self.piece_board()]

thisboard = board()
thisboard.init()
thisboard.get_board()