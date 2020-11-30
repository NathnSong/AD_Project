#20203084 송나단

import random
from copy import deepcopy

class Card:

    def __init__(self, line):
        self.board = [[0 for x in range(line)] for y in range(line)]
        self.all_Xnumber = 0 #총 x카드의 개수를 구하기 위해서 self.all_Xnumber를 새로 만든다
        for i in range(line -1):
            x_num = 0
            for j in range(line-1):
                if x_num > 4: #한 줄에 x가 4개 이상이 되지 않도록 한다
                    break
                if random.random()< 0.3:#x카드일 확률은 3/10으로 한다
                    self.board[i][j] = 'x'
                    x_num += 1

        for i in range(line-1):#가로 줄에서 'x'의 개수와 숫자의 합을 구한다.
            x_count = 0
            number = 0
            for j in range(line-1):
                if self.board[i][j] != 'x':
                    self.board[i][j] = "".join(map(str, random.choices(range(1, 4), weights=[4, 2, 1])))
                    number += int(self.board[i][j])
                else:
                    x_count+= 1
                    self.all_Xnumber +=1#총 x카드의 개수에 +1 한다
            self.board[i][line-1] = f' {number} | ☠{x_count}'#가로줄 끝에 구한 값이 들어가도록 한다.

        for i in range(line-1):#세로 줄에서 x의 개수와 숫자의 합을 구한다.
            x_count = 0
            number = 0
            for j in range(line-1):
                if self.board[j][i] != 'x':
                    number += int(self.board[j][i])
                else:
                    x_count+= 1
            self.board[line-1][i] = f'{number} | ☠{x_count}'#세로줄 끝에 구한 값이 들어가도록 한다.

        self.board[line - 1][line - 1] = '합 | x개수'
        self.secretcard = deepcopy(self.board)#리스트 board를 deepcopy하여 리스트 secretcard를 만든다.