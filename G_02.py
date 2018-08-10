import sys
import Logic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import *

import random


"""     to do
Board   X
Place   X
Hist    X
groups  X
capture X
noSuicide  X
libertyCount X


ko 
rules (CH / J)
win
komi
estimCount
"""


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.onStart()
        self.makeBoard()
        self.nGame()
        self.makeStat()
        self.runMain()


    def onStart(self):
        
        self.setGeometry(1, 35, 1100, 980)
        self.setWindowTitle('T͚̣̬̱̙̣̻̻ͩ͌̿̉ͥ̀̕͟ͅh̜̤̖̥̳̀͐̔ͩ̓̅̋͛̐͜e̍͒̎҉̬͔̖͉ ̸̬̭͓͓̥̟̱͑̔̅̾̔̆ͨ͞ͅG͗̏ͪ҉̼̺̩̝͍̹͞a̤̬̻̰̙̦̭͒ͩ͢͞m͓͎̣͎͎̙̀͐̓́͟͠e̷̸̳̫̻̭̞̽ͭ͑̌̈ͩ́')

        self.bColl = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(230, 140, 80))
        gradient.setColorAt(1.0, QColor(250, 180, 120))
        self.bColl.setBrush(QPalette.Window, QBrush(gradient))
 
        self.setPalette(self.bColl)
        
        # Menu
        bar = self.menuBar()
        
        bar_hra = bar.addMenu ('Hra')
        bar_nas = bar.addMenu ('Nastavení')
        
        bar_Nhra = bar_hra.addMenu ('Nová hra')
        bar_Shra = bar_hra.addMenu ('Uložit hru')
        bar_Ohra = bar_hra.addMenu ('Otevřít hru')
        
        
        bar_Stat = QAction('Statistiky', bar_hra, checkable = True)
        bar_Stat.setChecked(False)
        bar_Stat.triggered.connect(self.statClick)
        bar_hra.addAction(bar_Stat)
        
        
        bar_pvp = bar_Nhra.addAction ('Hráč proti hráči')                      #
        bar_pve = bar_Nhra.addAction ('Hráč proti počítači')
        bar_eve = bar_Nhra.addAction ('Počítač proti počítači')
        bar_free = bar_Nhra.addAction ('Volná hra')
        
        bar_pvp.triggered.connect(self.nGamePvP)
        bar_pve.triggered.connect(self.nGamePvE)
        bar_eve.triggered.connect(self.nGameEvE)
        bar_free.triggered.connect(self.nGameFree)
        
        bar_look = bar_nas.addAction ('Vzhled')

        
        ######################################### + on hover & on click style
        # tlačítka
        self.btn_resign = QPushButton(self)
        self.btn_resign.setIcon(QIcon(r"C:/Users/Dankovičová/Desktop/fun/computer/Py/projects/GUI/btn_resign.png"))
        self.btn_resign.setIconSize(QSize(60,60))
        self.btn_resign.setStyleSheet("border-style: groove; border-color: grey; border-width: 7px;")
        #self.btn_resign.s              # on hover event
        self.btn_resign.setGeometry(1000,100,60,60)
        
        self.btn_pass = QPushButton(self)
        self.btn_pass.setIcon(QIcon(r"C:/Users/Dankovičová/Desktop/fun/computer/Py/projects/GUI/btn_resign.png"))
        self.btn_pass.setIconSize(QSize(60,60))
        self.btn_pass.setStyleSheet("border-style: groove; border-color: mediumSeaGreen; border-width: 7px;")
        self.btn_pass.setGeometry(1000,200,60,60)        

        self.btn_force = QPushButton(self)
        self.btn_force.setIcon(QIcon(r"C:/Users/Dankovičová/Desktop/fun/computer/Py/projects/GUI/btn_resign.png"))
        self.btn_force.setIconSize(QSize(60,60))
        self.btn_force.setStyleSheet("border-style: groove; border-color: coral; border-width: 7px;")
        self.btn_force.setGeometry(1000,300,60,60)
        
        self.wHasCapturedLabel = QLabel(self)
        self.bHasCapturedLabel = QLabel(self)
        
        self.wHasCapturedLabel.move(1000,450)
        self.bHasCapturedLabel.move(1000,550)

    def nGamePvP(self):
        self.nGame()
        
    def nGamePvE(self):
        self.nGame()
        
    def nGameEvE(self):
        self.nGame()
        
    def nGameFree(self):
        self.nGame()
    
    def statClick(self, state):
        if state:
            self.WindStat.show()
        else:
            self.WindStat.hide()
    
    
    def makeStat(self):        
        self.WindStat = QWidget()
        self.WindStat.setGeometry(1101, 95, 800, 800)
        
        self.moves = QLabel(self.WindStat)
        self.valueMove = None
        self.moves.setText(f'''
                               <span style = "font-size:12pt; font-weight:600; color:#aa0000;">
                                   Move: &nbsp;&nbsp;&nbsp;{self.valueMove}
                               </span>
                               ''')
        self.moves.move(20, 50)

        self.time = QLabel(self.WindStat)
        self.valueTime= None
        self.time.setText(f'''
                              <span style = "font-size:12pt; font-weight:600; color:#aa0000;">
                                  Time: &nbsp;&nbsp;&nbsp;&nbsp;{self.valueTime}
                              </span>
                              ''')
        self.time.move(20, 100)
        
        self.estimPoints = QLabel(self.WindStat)
        self.valueEstimPoints_B = None
        self.valueEstimPoints_W = None
        self.estimPoints.setText(f'''
                                     <span style = "font-size:12pt; font-weight:600; color:#aa0000;">
                                         Estimated points:
                                     </span>
                                     &nbsp;&nbsp;&nbsp;<span style = "font-size:12pt; font-weight:600; color:#000000;">
                                         Black: {self.valueEstimPoints_B}
                                     </span>
                                     &nbsp;&nbsp;&nbsp;<span style = "font-size:12pt; font-weight:600; color:#FFFFFF;">
                                         White: {self.valueEstimPoints_W}
                                     </span>
                                     ''')
        self.estimPoints.move(20, 150)
        
        self.captured = QLabel(self.WindStat)
        self.valueCapturedStones_B = None
        self.valueCapturedStones_W = None
        self.captured.setText(f'''
                                     <span style = "font-size:12pt; font-weight:600; color:#aa0000;">
                                         Captured stones:
                                     </span>
                                     &nbsp;&nbsp;&nbsp;<span style = "font-size:12pt; font-weight:600; color:#000000;">
                                         Black: {self.valueCapturedStones_B}
                                     </span>
                                     &nbsp;&nbsp;&nbsp;<span style = "font-size:12pt; font-weight:600; color:#FFFFFF;">
                                         White: {self.valueCapturedStones_W}
                                     </span>
                                     ''')
        self.captured.move(20, 200)
        
        self.bGroupsStat = QLabel(self.WindStat)
        self.wGroupsStat = QLabel(self.WindStat)
        
        self.bGroupsStat.setText(f"black group: {self.game.bGroups}")
        self.wGroupsStat.setText(f"white group: {self.game.wGroups}")

        self.bGroupsStat.setGeometry(20,250,800,50)
        self.wGroupsStat.setGeometry(20,300,800,50)

    def runMain(self):
        self.show()
        
        for j in range (19):
            for i in range (19):
                self.btn[i][j].clicked.connect(lambda: self.place())
        
        
    def makeBoard(self):
        self.Gboard = QLabel(self)                       #whole
        self.Gboard.setPixmap(QPixmap(r"C:/Users/Dankovičová/Desktop/fun/computer/Py/projects/GUI/drawing_.png").scaledToWidth(850))
        self.Gboard.setGeometry(100,0,1000,1000)
        
        self.btn = [(["-"]*19) for _ in range(19)]
        self.stn = [(["-"]*19) for _ in range(19)]
        
        self.a = 0

        for j in range (19):            
            for i in range (19):                        # stones
                self.stn[i][j] = QLabel(self)
                self.stn[i][j].setGeometry(80 + 42.5*(i + 1),902 - 42.5*(j + 1),40,40)
     
                self.btn[i][j] = QPushButton(self)        # buttons
                self.btn[i][j].setGeometry(80 + 42.5*(i + 1),902 - 42.5*(j + 1),41,41)
                self.btn[i][j].setText(f'\n\n\n{i} {j}')
                self.btn[i][j].setStyleSheet("background-color:transparent;border:0")

    def place(self):
        self.a += 1 
        sender = self.sender()
        TheSender = sender.text()
        print (f'click {self.a}'.ljust(10, " ") + f'coord {TheSender.split()}')
        i = int(TheSender.split()[0])
        j = int(TheSender.split()[1])

        self.game.play([i, j])

        if self.game.color == "O":
            QApplication.setOverrideCursor(QCursor(QPixmap(r"C:/Users/Dankovičová/Desktop/fun/computer/Py/projects/GUI/stone_w.png").scaledToWidth(25), -1, -1))
        else:
            QApplication.setOverrideCursor(QCursor(QPixmap(r"C:/Users/Dankovičová/Desktop/fun/computer/Py/projects/GUI/stone_b.png").scaledToWidth(25), -1, -1))

            # conds ↑
            # move  ↓

                   #place on board
        self.updateBoard()


        self.bGroupsStat.setText(f"black group: {self.game.bGroups}")
        self.wGroupsStat.setText(f"white group: {self.game.wGroups}")

        #self.printBoard (self.game.board)
        
        self.moveNumber+=1

################################################
    def updateBoard(self):
        for j in range (19):
            for i in range (19):
                if self.game.board[i][j] == "#":
                    self.stn[i][j].setPixmap(QPixmap(r"C:/Users/Dankovičová/Desktop/fun/computer/Py/projects/GUI/stone_b.png").scaledToWidth(40))
                elif self.game.board[i][j] == "O":
                    self.stn[i][j].setPixmap(QPixmap(r"C:/Users/Dankovičová/Desktop/fun/computer/Py/projects/GUI/stone_w.png").scaledToWidth(40))
                else:
                    self.stn[i][j].setPixmap(QPixmap(r"C:/Users/Dankovičová/Desktop/fun/computer/Py/projects/GUI/empty.png"))
        
        self.wHasCapturedLabel.setText(f"W: {self.game.wHasCaptured}")
        self.bHasCapturedLabel.setText(f"B: {self.game.bHasCaptured}")
        
        print ("bHasCaptured",self.game.bHasCaptured)
        print ("wHasCaptured",self.game.wHasCaptured)
        
    def readable(self, board):
        readThis = ''
        readThis += '<<'
        for row in board:
            for element in row:
                readThis += element
        readThis += '>>'
        return readThis
    
    def printBoard(self, board):      #dá board do konzole
        for i in board:
            print ("")
            for j in i:
                print (j, end = " ")
        print ("\n\n")

################################################

    def nGame(self):
        
        QApplication.setOverrideCursor(QCursor(QPixmap(r"C:/Users/Dankovičová/Desktop/fun/computer/Py/projects/GUI/stone_b.png").scaledToWidth(25), -1, -1))
        self.gameOn = True
        self.gameStateHistory = []

        self.game = Logic.Logic()         #pro import hru doplnit parametry
        self.moveNumber = 0

        self.updateBoard()                

    def endGame(self):
            #zhodnocení; okno výsledků
        pass
    
    # potom import AI -> aiNet(color, hist, board)
    #                       return x,y
    
    #                    thinking(bot):         # later on
    #                       return [[x,y,%],[x,y,%],..]    

# =============================================================================
app = QApplication(sys.argv)
run = Main()
sys.exit(app.exec_())    
# =============================================================================

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


class Aii():
    def radon1(self):
        return [random.randint(0, 19), random.randint(0, 19)]

    def radon2(self, board):
        pass

    def radon0(self, board):
        pass

    def neet(self, board):
        pass


