from copy import deepcopy
"""

history description:
gameState, stateMoves, stateBoard, stateGroups, stateScore =  [[],] * 5

stateMoves.append(self.moveNumber)

stateBoard.append(self.readable(self.board))
stateBoard.append(self.color)

stateGroups.append(self.wGroups)
stateGroups.append(self.bGroups)

stateScore.append(self.wScore)
stateScore.append(self.bScore)

gameState.append([stateMoves, stateBoard, stateGroups, stateScore])

self.gameStateHistory.append(gameState)

"""


class Logic():
    """
    Takes:
    coord = coords of stone placed
    rules = J -> 1; Ch -> 2
    history = for opening files
    
    Returns:
    hist = new game history

    """
    def __init__(self, rules=1, handicap=0, komi=5.5, history=[]):
        print ("__init__")
        self.rules = rules
        self.handicap = handicap
        self.wScore = komi
        self.bScore = 0
        self.wHasCaptured = 0
        self.bHasCaptured = 0
        self.color = "#"
        self.bGroups = []
        self.wGroups = []
        self.temp_wGroups = []
        self.temp_bGroups = []

        self.board = [["-"] * 19 for _ in range (19)]
        self.makeHistory()
    
    def __del__(self):
        print ("__del__")
    
############    main game logic
        
    def makeHistory(self):
        
        self.history, self.gameState, self.stateMoves, self.stateGroups, self.stateScore =  [[],] * 5
        self.history = 4*[[]]
        self.updateHistory()
        
    def updateHistory(self):
        self.history[0].append([self.stateMoves])
        self.history[1].append([self.board])
        self.history[2].append([self.stateGroups])
        self.history[3].append([self.stateScore])    
        
    def play(self, coords):
        #self.board = self.history[-1][1][0]
        #self.color = self.history[-1][1][1]
        
        #steal all the history ↑
        
        self.temp_board = deepcopy(self.board)
        if False not in [self.alreadyPlacedCheck(self.board,coords)]:
            #, self.koCheck(self.board, self.history[1])
            #print (self.history[1])             # rep ko check
            self.temp_board[coords[0]][coords[1]] = self.color

            if self.color == "#":
                self.temp_bGroups = self.makeGroups(self.color, coords, deepcopy(self.bGroups))
            else:
                self.temp_wGroups = self.makeGroups(self.color, coords, deepcopy(self.wGroups))

            if self.color == "#":
                self.temp_wGroups = self.capture(deepcopy(self.wGroups), 1)
            else:
                self.temp_bGroups = self.capture(deepcopy(self.bGroups), 1)
#↓

            suicide = self.checkSuicide(deepcopy(self.temp_bGroups) if self.color == "#" else deepcopy(self.temp_wGroups))
            print (suicide)
#↑
            #inscribe into history ↓
            if not suicide:
                self.board = deepcopy(self.temp_board)
                print (3)
                self.bGroups = deepcopy(self.temp_bGroups)
                self.wGroups = deepcopy(self.temp_wGroups)
                
                self.updateHistory()
                
                self.color = self.colorChange(self.color)
                
############    game rules
    
    def colorChange(self, color):
        if color == "#":
            return "O"
        return "#"
    
    
    def removeFromBoard(self, group):         #removes group from board
        for stone in group:
            self.temp_board[stone[0]][stone[1]] = "-"
            if self.color == "O":
                self.wHasCaptured+=1
            if self.color == "#":
                self.bHasCaptured+=1

                
    def makeGroups(self, color, coords, groups = []):
        groups.append([[coords[0],coords[1]]])
        return self.joinGroups(groups)
    
        
    def findSpaceRow(self, coords):         ### not imp
        x = coords.split()[0]
        if x == 19:
            return None        

                        
    def findSpace(self, coords):            ### not imp
        x = coords.split()[0]
        y = coords.split()[1]
        if y == 0:
            if x == 0:
                return [[x+1,y+1]]
            elif x == 18:
                [[x-1,y+1]]
            else:
                return [[x-1,y+1],[x+1,y+1]]
        elif y == 18:
            if x == 18:
                return [[x-1,y-1]]
            elif x == 0:
                [[x+1,y-1]]
            else:
                [[x-1,y-1],[x+1,y-1]]
        elif x == 0:
            return [[x+1,y-1],[x+1,y+1]]
        elif x == 18:
            return [[x-1,y-1],[x-1,y+1]]
        return [[x-1,y-1],[x+1,y-1],[x-1,y+1],[x+1,y+1]]
            
    
    def joinGroups(self, arr):     #arr = current array; app = appending array
            """ !! Note: coord != index !! """ # ← coodr tak není záporný ↓
            for arrGroup in arr:
                for appGroup in arr:        #projde skupiny kamenů
                    if appGroup == arrGroup:break       #přeskočí sama sebe, aby se nevkládala do sebe
                    for arrStone in arrGroup:       #projde kameny
                        for appStone in appGroup:
                            if (                    #porovná, jestly nějaké kameny ve skupině sousedí
                                    (appStone[0]-1 == arrStone[0] and appStone[1] == arrStone[1]
                                        ) or (
                                    appStone[0]+1 == arrStone[0] and appStone[1] == arrStone[1]                                    
                                        ) or (                                    
                                    appStone[1]-1 == arrStone[1] and appStone[0] == arrStone[0]
                                    ) or (    
                                    appStone[1]+1 == arrStone[1] and appStone[0] == arrStone[0])
                                ):
                                for addStone in appGroup:
                                    arrGroup.append(addStone)
                                arr.remove(appGroup)
                                return self.joinGroups(arr)
            return arr 
    

    def capture(self, colorGroup, purpose = 1):
        """
        colorGroup = oddělává se (jestli capture)
        
         purpose = 1 -> pro capture
        Zjistí jestli skupina má alespoň jednu Lib,
        jestli ne tak ji odstraní(nedá ji do nové groupy).
        Vždy se použije jen na protivníka,
        protože nejde suicide.
        Vrátí upravenou groupu & jako global předělá board.
         
         purpose == 2 -> pro validity check
        Zjistí jestli má skupina alepoň jednu Lib,
        jestli ne tak ji odstraní(nedá ji do nové groupy).
        """
        NewColGroup = []
        board = deepcopy(self.temp_board)

        for arrGroup in colorGroup:
            for arrStone in arrGroup:
                if arrStone[0] == 0:            # ← zjistí jestli souřadnice existuje
                    if board[arrStone[0]+1][arrStone[1]] == "-":
                        NewColGroup.append(arrGroup)
                        break
                else:
                    if board[arrStone[0]-1][arrStone[1]] == "-":
                        NewColGroup.append(arrGroup)
                        break
                
                
                if arrStone[0] == 18:
                    if board[arrStone[0]-1][arrStone[1]] == "-":
                        NewColGroup.append(arrGroup)
                        break
                else:
                    if board[arrStone[0]+1][arrStone[1]] == "-":
                        NewColGroup.append(arrGroup)
                        break
                
                
                if arrStone[1] == 0:
                    if board[arrStone[0]][arrStone[1]+1] == "-":
                        NewColGroup.append(arrGroup)
                        break
                else:
                    if board[arrStone[0]][arrStone[1]-1] == "-":
                        NewColGroup.append(arrGroup)
                        break
                
                
                if arrStone[1] == 18:
                    if board[arrStone[0]][arrStone[1]-1] == "-":
                        NewColGroup.append(arrGroup)
                        break
                else:
                    if board[arrStone[0]][arrStone[1]+1] == "-":
                        NewColGroup.append(arrGroup)
                        break
                
                
                if arrStone == arrGroup[-1]:
                    if purpose == 1:
                        self.removeFromBoard(arrGroup)                 # pokud skupina nemá Libs oddělá ji z board
                    if purpose == 2:
                        return True
        print ("NewcolGroup: ",NewColGroup)
        return NewColGroup
    
    def checkSuicide(self, colorGroup):           # true jestli sui je
        if self.capture(colorGroup, 2) is True:
            return True
        return False
    
############    checking
    
    def alreadyPlacedCheck(self, board, coords):
        if board[coords[0]][coords[1]] != "-":
            return False
        return True
    

    def koCheck(self, board, boardHistory):
        if board in boardHistory:
            return False
        return True
    
