from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage
from math import inf


class TicTacToe:

    # constructor
    def __init__(self, player1, player2, alpha_beta=True):
        self.move_number = 0

        # initializing players
        self.player1 = player1
        self.player2 = player2

        # initializing the start player
        self.start = player1

        # tic tac toe board
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.alpha_beta = alpha_beta

    # prints tic tac toe board
    def print_board(self):
        x = 0
        for i in range(3):
            print("|", end=" ")
            for j in range(3):
                print(self.board[x], "|", end=" ")
                x += 1
            print()

    # returns true if game is draw, false otherwise
    def game_draw(self):
        return self.move_number == 9

    # returns:
    # player1: if player1 is winning
    # player2: if player2 is winning
    # tie: if game is draw
    # None: if the game is neiter draw not any player has won yet
    def check_winner(self):
        winner_mark = None

        # mapping of board position in matrix to an array location
        def loc(i, j):
            return i * 3 + j

        # checking horizontally
        for i in range(3):
            if self.board[loc(i, 0)] == self.board[loc(i, 1)] == self.board[loc(i, 2)]:
                winner_mark = self.board[loc(i, 0)]
                break

        # checking vertically
        if not winner_mark:
            for j in range(3):
                if (
                    self.board[loc(0, j)]
                    == self.board[loc(1, j)]
                    == self.board[loc(2, j)]
                ):
                    winner_mark = self.board[loc(0, j)]
                    break

        # checking diagonally
        if not winner_mark:
            # diagonal 1
            if self.board[0] == self.board[4] == self.board[8]:
                winner_mark = self.board[0]

            # diagonal 2
            elif self.board[2] == self.board[4] == self.board[6]:
                winner_mark = self.board[2]

        if winner_mark == self.player1.mark:
            return self.player1
        elif winner_mark == self.player2.mark:
            return self.player2
        elif self.game_draw():
            return "tie"
        else:
            return None


# player class
class Player(Agent):

    # constructor
    def __init__(self, aid, mark):
        super().__init__(aid)
        self.game = None
        self.opponent = None
        self.mark = mark

    def on_start(self):
        super().on_start()

        # if the start player is the player itself
        if self.game.start == self:
            self.next_move()

    # adding game to the player
    # so that player can access game properties
    def join_game(self, game):
        self.game = game

        # adding opponent member
        self.opponent = (
            self.game.player1 if (self != self.game.player1) else self.game.player2
        )

    # invoked after the opponent makes a turn
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


# subclass of Player
class HumanPlayer(Player):
    def __init__(self, aid, mark):
        super().__init__(aid, mark)

    def next_move(self):
        self.game.print_board()
        display_message(self.aid.localname, self.aid.localname + "'s turn")
        cell = int(input("Enter cell number: "))
        self.game.board[cell - 1] = self.mark  # marking cell
        self.game.move_number += 1

        winner = self.game.check_winner()
        if winner == "tie":
            self.game.print_board()
            print("Game Draw!!!")
            return

        elif winner == self:
            self.game.print_board()
            print(self.aid.localname + " Won!!!")
            return

        self.send_message()


# subclass of Player
class ComputerPlayer(Player):

    # constructor
    def __init__(self, aid, mark):
        super().__init__(aid, mark)

    def next_move(self):
        self.game.print_board()
        display_message(self.aid.localname, self.aid.localname + "'s turn")

        # if alpha beta pruning is enabled
        if self.game.alpha_beta:
            # alpha = -inf, beta = inf
            _, cell = self.minimax_with_alpha_beta_pruning(0, -inf, inf, True)

        # if alpha beta pruning is disabled
        else:
            _, cell = self.minimax(0, True)

        # making move
        self.game.board[cell - 1] = self.mark
        self.game.move_number += 1
        print(self.aid.localname + " marked cell:", cell)
        winner = self.game.check_winner()
        if winner == "tie":
            self.game.print_board()
            print("Game Draw!!!")
            return

        elif winner == self:
            self.game.print_board()
            print(self.aid.localname + " Won!!!")
            return
        self.send_message()

    # calculates the utility of a final state(leaf node)
    def find_score(self, result, depth):

        # if the final state is a tie
        if result == "tie":
            return 0

        # if the maximizing player is winning
        elif result == self:
            return 10 - depth

        # if the minimizing player is winning
        else:
            return -(10 - depth)

    # checks if a board position(cell) is empty
    def is_empty(self, cell):
        return isinstance(cell, int)

    # minimax withour alpha-beta pruning
    # returns bestScore, bestMove
    def minimax(self, depth, maximizingPlayer):
        result = self.game.check_winner()

        # base case i.e. leaf node
        # player wins or opponent wins or tie
        if result:
            score = self.find_score(result, depth)
            return score, None

        # if its maximizing player's turn
        if maximizingPlayer:
            bestScore = -inf
            bestMove = None

            for i in range(9):
                if self.is_empty(self.game.board[i]):

                    # marking cell
                    self.game.board[i] = self.mark
                    self.game.move_number += 1

                    score, _ = self.minimax(depth + 1, False)

                    # unmarking cell
                    self.game.board[i] = i + 1
                    self.game.move_number -= 1

                    # updating bestScore if we get a score better than the current score
                    if score > bestScore:
                        bestScore = score
                        bestMove = i + 1

            return bestScore, bestMove

        # if its minimizing player's turn
        else:
            bestScore = inf
            bestMove = None

            for i in range(9):
                if self.is_empty(self.game.board[i]):
                    self.game.board[i] = self.opponent.mark
                    self.game.move_number += 1

                    score, _ = self.minimax(depth + 1, True)

                    self.game.board[i] = i + 1
                    self.game.move_number -= 1

                    if score < bestScore:
                        bestScore = score
                        bestMove = i + 1

            return bestScore, bestMove

    # minimax with alpha beta pruning
    def minimax_with_alpha_beta_pruning(self, depth, alpha, beta, maximizingPlayer):
        result = self.game.check_winner()

        # base case
        if result:
            score = self.find_score(result, depth)
            return score, None

        # if its maximizing player's turn
        if maximizingPlayer:
            bestScore = -inf
            bestMove = None

            for i in range(9):
                if self.is_empty(self.game.board[i]):
                    self.game.board[i] = self.mark
                    self.game.move_number += 1

                    score, _ = self.minimax_with_alpha_beta_pruning(
                        depth + 1, alpha, beta, False
                    )

                    self.game.board[i] = i + 1
                    self.game.move_number -= 1

                    if score > bestScore:
                        bestScore = score
                        bestMove = i + 1

                    # updating alpha
                    alpha = max(alpha, score)

                    # pruning step
                    if alpha >= beta:
                        break

            return bestScore, bestMove

        # if its minimizing player's turn
        else:
            bestScore = inf
            bestMove = None

            for i in range(9):
                if self.is_empty(self.game.board[i]):
                    self.game.board[i] = self.opponent.mark
                    self.game.move_number += 1

                    score, _ = self.minimax_with_alpha_beta_pruning(
                        depth + 1, alpha, beta, True
                    )

                    self.game.board[i] = i + 1
                    self.game.move_number -= 1

                    if score < bestScore:
                        bestScore = score
                        bestMove = i + 1

                    beta = min(beta, score)
                    if alpha >= beta:
                        break

            return bestScore, bestMove


if __name__ == "__main__":
    human = HumanPlayer(AID("human"), "X")
    computer = ComputerPlayer(AID("computer"), "O")
    print("1. Minimax with alpha-beta pruning")
    print("2. Minimax without alpha-beta pruning")

    option = int(input("Enter your choice: "))

    if option == 1:
        game = TicTacToe(human, computer, alpha_beta=True)
    else:
        game = TicTacToe(human, computer, alpha_beta=False)

    print("\n1. Human first")
    print("2. Computer first")
    option = int(input("Enter your choice: "))
    if option == 1:
        game.start = human
    else:
        game.start = computer

    human.join_game(game)
    computer.join_game(game)
    print("\nHuman's mark: ", "X")
    print("Computer's marks: ", "O\n")
    agents = [human, computer]
    start_loop(agents)