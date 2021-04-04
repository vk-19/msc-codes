from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage
from itertools import combinations
import random


class TicTacToe:

    # constructor
    def __init__(self, player1, player2, start):
        self.move_number = 0

        # initializing players
        self.player1 = player1
        self.player2 = player2

        # initializing the start player
        self.start = start

        # tic tac toe board
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		
        # magic square board: mapping from tic tac toe board to magic square board
        self.magic_square = {1: 8, 2: 1, 3: 6, 4: 3, 5: 5, 6: 7, 7: 4, 8: 9, 9: 2}

        # magic square board: mapping from magic square board to tic tac toe board
        self.magic_square_inv = {8: 1, 1: 2, 6: 3, 3: 4, 5: 5, 7: 6, 4: 7, 9: 8, 2: 9}

    # prints tic tac toe board
    def print_board(self):
        x = 0
        for i in range(3):
            for j in range(3):
                print(self.board[x], end=" ")
                x += 1
            print()

    # checks if the player has won the game
    def player_won(self, player):
        comb = combinations(player.marked_cells, 3)
        for i in comb:
            if sum(i) == 15:
                return True
        return False


class Player(Agent):
    def __init__(self, aid, mark):
        super().__init__(aid)
        self.game = None
        self.opponent = None
        self.marked_cells = []
        self.mark = mark

    def on_start(self):
        super().on_start()

        if self.game.start == self:
            self.next_move()

    def join_game(self, game):
        self.game = game

        # adding opponent member
        self.opponent = (
            self.game.player1 if (self != self.game.player1) else self.game.player2
        )

    def react(self, message):
        super().react(message)
        self.next_move()

    # sends "your turn" message to opponent
    def send_message(self):
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.set_content("Your turn")
        message.add_receiver(self.opponent.aid)
        self.agentInstance.table[self.opponent.aid.localname] = self.opponent.aid

        self.call_later(1, self.send, message)


class HumanPlayer(Player):
    def __init__(self, aid, mark):
        super().__init__(aid, mark)

    def next_move(self):
        self.game.print_board()
        display_message(self.aid.localname, self.aid.localname + "'s turn")
        cell = int(input("Enter cell number: "))
        self.game.board[cell - 1] = self.mark #marking cell
        self.marked_cells.append(self.game.magic_square[cell]) #appending corresponding magic number in the 																list
        self.game.magic_square.pop(cell) #removing the cell from the magic board

        self.game.move_number += 1

        # checks if human has won the game
        if self.game.player_won(self):
            self.game.print_board()
            print(self.aid.localname + " Won!!!")
            return

        # checks if the game is over and no one wins
        if self.game.move_number == 9: #board is full
            self.game.print_board()
            print("Game Draw!!!")
            return

        self.send_message()


class ComputerPlayer(Player):
    def __init__(self, aid, mark):
        super().__init__(aid, mark)

    def next_move(self):
        self.game.print_board()
        display_message(self.aid.localname, self.aid.localname + "'s turn")
        cell = None
        won = False
        # finding own chance to win
        comb = combinations(self.marked_cells, 2)
        for i in comb:
            required = 15 - sum(i)
            if required in self.game.magic_square.values():
                cell = self.game.magic_square_inv[required]
                won = True
                break

        # findng opponent's chance to win
        if not won:
            comb = combinations(self.opponent.marked_cells, 2)
            for i in comb:
                required = 15 - sum(i)
                if required in self.game.magic_square.values():
                    cell = self.game.magic_square_inv[required]
                    self.marked_cells.append(self.game.magic_square[cell])
                    self.game.magic_square.pop(cell)
                    break

        # randomly choosing a move in case above two cases don't apply
        if not won and cell == None:
            cell = random.choice(list(self.game.magic_square.keys()))
            self.marked_cells.append(self.game.magic_square[cell])
            self.game.magic_square.pop(cell)

        self.game.board[cell - 1] = self.mark
        display_message(
            self.aid.localname, "{} marked cell: {}".format(self.aid.localname, cell)
        )

        self.game.move_number += 1

        # checks if computer has won the game
        if won:
            self.game.print_board()
            print(self.aid.localname + " Won!!!")
            return

        # check if the game is over and no one wins
        if self.game.move_number == 9: #board is full
            self.game.print_board()
            print("Game Draw!!!")
            return

        self.send_message()


if __name__ == "__main__":

    print("1. Human vs Computer")
    print("2. Computer vs Computer")

    option = int(input("Enter your option: "))

    if option == 1:
        human = HumanPlayer(AID("human"), "X")
        computer = ComputerPlayer(AID("computer"), "O")
        print("1. Human first")
        print("2. Computer first")
        option = int(input("Enter your option: "))
        if option == 1:
            game = TicTacToe(human, computer, start=human)
        else:
            game = TicTacToe(human, computer, start=computer)

        human.join_game(game)
        computer.join_game(game)
        print("\nHuman's mark: ", "X")
        print("Computer's marks: ", "O\n")
        agents = [human, computer]
        start_loop(agents)

    else:
        computer1 = ComputerPlayer(AID("computer1"), "X")
        computer2 = ComputerPlayer(AID("computer2"), "O")
        game = TicTacToe(computer1, computer2, computer1)
        computer1.join_game(game)
        computer2.join_game(game)
        agents = [computer1, computer2]
        start_loop(agents)
