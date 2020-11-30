#20203084 송나단

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QToolButton, QComboBox
from PyQt5.QtWidgets import QSizePolicy, QPushButton
from PyQt5.QtWidgets import QGridLayout, QMessageBox
from card import Card

class Button(QToolButton):#버튼을 만드는 class를 만든다.

    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 80)
        size.setWidth(max(size.width(), size.height()))
        return size

class CardGame(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.line = 6
        self.number_count = 0
        #print(self.card.board)

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.setWindowTitle('X카드 뒤집기')#윈도우 창의 Title을 설정한다.

        self.newgameButton = QToolButton()#newgame버튼을 만든다 -> 누르면 새로운 게임을 시작할 수 있도록
        self.newgameButton.setText('New Game')
        self.newgameButton.clicked.connect(self.newStart)
        self.newStart()
        self.mainLayout.addWidget(self.newgameButton, 0, 0)
        self.ChangeButton()

    def ChangeButton(self):

        self.changeLayout = QGridLayout()
        self.keyCombo = QComboBox(self)
        self.keyCombo.addItem("4*4")
        self.keyCombo.addItem("5*5")
        self.keyCombo.addItem("6*6")

        self.changeLayout.addWidget(self.keyCombo, 0,0)
        self.changeButton = QPushButton("Change", self)
        self.changeButton.clicked.connect(self.changeButtonClicked)
        self.changeLayout.addWidget(self.changeButton, 0,1)
        self.mainLayout.addLayout(self.changeLayout, 0, 1)

    def changeButtonClicked(self):
        keyline = self.keyCombo.currentText()
        if keyline == "4*4":
            self.line = 5
            self.newStart()
        elif keyline == "5*5":
            self.line = 6
            self.newStart()
        elif keyline == "6*6":
            self.line = 7
            self.newStart()

    def cardButton(self):#card버튼을 만들어서 card가 클릭되면 이벤트가 실행되도록 한다.
        self.card = Card(self.line)
        #print(self.card.board)

        for x in range(self.line):
            for y in range(self.line):
                if x == self.line-1 or y == self.line-1: #가로끝, 세로끝인 경우에는 리스트안의 값 그대로 버튼을 설정
                    self.card.board[x][y] = Button(str(self.card.board[x][y]), self.buttonClicked)
                elif x != self.line-1 and y != self.line-1: #가로끝, 세로끝이 '아닌' 경우에는 리스트의 index를 포함한 card이름을 새롭게 설정
                    self.card.board[x][y] = Button(str(self.card.board[x][y]), self.buttonClicked)
                    self.card.board[x][y].setText("card"+ str(x) + str(y))
        self.cardLayout = QGridLayout()

        # 각각의 위치(리스트 index에 해당하는 위치)에 card버튼이 들어가도록 한다.
        for x in range(self.line):
            for y in range(self.line):
                self.cardLayout.addWidget(self.card.board[x][y], x, y)

        self.cardLayout.setSpacing(0)#카드 사이의 간격을 조정한다.
        self.mainLayout.addLayout(self.cardLayout, 1, 0)#Main레이아웃에 Card레이아웃을 넣는다.


    def newStart(self):#새로운 게임을 시작할 수 있도록 한다.
        self.cardButton()#새로운 cardButton을 설정할 수 있다.

    def buttonClicked(self):

        button = self.sender()
        key = button.text()

        for x in range(self.line):
            for y in range(self.line):
                if key == "card"+ str(x) + str(y):#클릭한 카드를 찾는다.
                    if self.card.secretcard[x][y] == 'x':#클릭한 카드가 'x'카드일 경우에 해당
                        self.card.board[x][y].setText(self.card.secretcard[x][y])
                        self.GameOverMessage('Fail!')#실패했다는 메세지창을 띄운다.
                    else: #클릭한 카드가 숫자카드일 경우에 해당
                        self.card.board[x][y].setText(self.card.secretcard[x][y])
                        self.number_count += 1

        # 현재 뒤집은 숫자카드의 개수가 총 숫자카드 개수와 같을 경우 성공했다는 메세지창 띄운다.
        if self.number_count == ((self.line-1)*(self.line-1) -self.card.all_Xnumber):
            self.GameOverMessage('Success!')

    def GameOverMessage(self, message):#게임이 끝났을때(Success or Fail) 메세지 창이 뜨도록 한다

        reply = QMessageBox.information(self
                                         , '게임 종료'
                                         , f'{message} \n다시 시작?'
                                         , QMessageBox.Yes | QMessageBox.No)

        # Yes버튼을 누르면 새로운 게임을 시작할 수 있도록 한다.
        if reply == QMessageBox.Yes:
            self.newStart()

        # No버튼을 누르면 게임이 끝나도록 한다.
        else:
            self.close()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    game = CardGame()
    game.show()
    sys.exit(app.exec_())
