# coding=utf-8
#referencia: https://raw.githubusercontent.com/omegadeep10/tic-tac-toe/master/game.py
import random
import sys


class TicTacToe:

    def __init__(self):
        """Initialize with empty board"""
        self.board = [" ", " ", " ", 
                      " ", " ", " ", 
                      " ", " ", " "]

    def show(self):
        """Format and print board"""
        result = """
          {} | {} | {}
         -----------
          {} | {} | {}
         -----------
          {} | {} | {}
        """.format(*self.board)
        print(result)
        return self.board

    def clearBoard(self):
        self.board = [" ", " ", " ", 
                      " ", " ", " ", 
                      " ", " ", " "]

    def whoWon(self):
        if self.checkWin() == "X":
            return "X"
        elif self.checkWin() == "O":
            return "O"
        elif self.gameOver() == True:
            return "Nobody"

    def availableMoves(self):
        """Return empty spaces on the board"""
        moves = []
        for i in range(0, len(self.board)):
            if self.board[i] == " ":
                moves.append(i)
        return moves

    def getMoves(self, player):
        """Get all moves made by a given player"""
        moves = []
        for i in range(0, len(self.board)):
            if self.board[i] == player:
                moves.append(i)
        return moves

    def makeMove(self, position, player):
        """Make a move on the board"""
        self.board[position] = player

    def checkWin(self):
        """Return the player that wins the game"""
        combos = ([0, 1, 2], [3, 4, 5], [6, 7, 8],
                  [0, 3, 6], [1, 4, 7], [2, 5, 8],
                  [0, 4, 8], [2, 4, 6])

        for player in ("X", "O"):
            positions = self.getMoves(player)
            for combo in combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player

    def gameOver(self):
        """Return True if X wins, O wins, or draw, else return False"""
        if self.checkWin() != None:
            return True
        for i in self.board:
            if i == " ":
                return False
        return True



    def minimax(self, node, depth, player):
        """
        Recursively analyze every possible game state and choose
        the best move location.

        node - the board
        depth - how far down the tree to look
        player - what player to analyze best move for (currently setup up ONLY for "O")
        """
        if depth == 0 or node.gameOver():
            if node.checkWin() == "X":
                return 0
            elif node.checkWin() == "O":
                return 100
            else:
                return 50

        #The max player, the computer
        if player == "O":
            bestValue = 0
            for move in node.availableMoves():
                node.makeMove(move, player)
                moveValue = self.minimax(node, depth-1, changePlayer(player))
                node.makeMove(move, " ")
                bestValue = max(bestValue, moveValue)
            return bestValue
        
        #The min player, you
        if player == "X":
            worstValue = 100
            for move in node.availableMoves():
                node.makeMove(move, player)
                moveValue = self.minimax(node, depth - 1, changePlayer(player))
                node.makeMove(move, " ")
                worstValue = min(worstValue, moveValue)
            return worstValue

    def expectimax(self, node, depth, player):
        """
        code based on this pseucode:
        function expectiminimax(node, depth)
    if node is a terminal node or depth = 0
        return the heuristic value of node
    if the adversary is to play at node
        // Return value of minimum-valued child node
        let α := +∞
        foreach child of node
            α := min(α, expectiminimax(child, depth-1))
    else if we are to play at node
        // Return value of maximum-valued child node
        let α := -∞
        foreach child of node
            α := max(α, expectiminimax(child, depth-1))
    else if random event at node
        // Return weighted average of all child nodes' values
        let α := 0
        foreach child of node
            α := α + (Probability[child] * expectiminimax(child, depth-1))
    return α
    from wikipedia
        """
        if depth == 0 or node.gameOver():
            if node.checkWin() == "X":
                return 0
            elif node.checkWin() == "O":
                return 100
            else:
                return 50

        # The max player, the computer
        if player == "O":
            bestValue = -float('inf')
            for move in node.availableMoves():
                node.makeMove(move, player)
                moveValue = self.expectimax(node, depth - 1, changePlayer(player))
                node.makeMove(move, " ")
                bestValue = max(bestValue, moveValue)
            return bestValue

        # The min player, you
        if player == "X":
            value = 0
            for move in node.availableMoves():


                node.makeMove(move, player)
                if node.checkWin() == "X":
                    moveValue = 0
                elif node.checkWin() == "O":
                    moveValue =  100
                else:
                    moveValue = 50
                node.makeMove(move, " ")
                prob=(1/(len(node.availableMoves()))) #change de probability acoding to the number of free spaces in the board
                value = value + (moveValue*prob)
            return value

    def alphaBetaPruning(self, node, depth, player,alpha,beta):


        """
        code based on this pseudocode:
        function alphabeta(node, depth, α, β, maximizingPlayer) is
        if depth = 0 or node is a terminal node then
        return the heuristic value of node
        if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
            α := max(α, value)
            if α ≥ β then
                break (* β cut-off *)
        return value
        else
        value := +∞
        for each child of node do
            value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
            β := min(β, value)
            if α ≥ β then
                break (* α cut-off *)
          return value
          from wikipidia
        """

        if depth == 0 or node.gameOver():
            if node.checkWin() == "X":
                return 0
            elif node.checkWin() == "O":
                return 100
            else:
                return 50

        # The max player, the computer
        if player == "O":
            Value = -float('inf')
            for move in node.availableMoves():
                node.makeMove(move, player)
                moveValue = self.alphaBetaPruning(node, depth - 1, changePlayer(player),alpha,beta)
                node.makeMove(move, " ")

                Value = max(Value,moveValue)
                if Value >= beta:
                    return Value
                alpha = max(alpha, Value)
            return Value

        # The min player, you
        elif player == "X":
            Value = float('inf')
            for move in node.availableMoves():
                node.makeMove(move, player)
                moveValue = self.alphaBetaPruning(node, depth - 1, changePlayer(player),alpha,beta)
                node.makeMove(move, " ")

                Value = min(Value,moveValue)
                if Value <= alpha:
                    return Value
                beta = min(beta, Value)
            return Value



def changePlayer(player):
    """Returns the opposite player given any player"""
    if player == "X":
        return "O"
    else:
        return "X"

def tipe (arg,board,depth,player,alpha,beta): #funtion to choose the inteligence of the game


    if arg == "min": #minimax
        return  board.minimax(board, depth - 1, changePlayer(player))
    elif arg == "max": #expectimax
        return board.expectimax(board, depth - 1, changePlayer(player))
    elif arg == "alpha": #alpha beta
        return board.alphaBetaPruning(board, depth - 1, changePlayer(player), alpha, beta)


def make_best_move(board, depth, player):
    """
    Controllor function to initialize minimax and keep track of optimal move choices

    board - what board to calculate best move for
    depth - how far down the tree to go
    player - who to calculate best move for (Works ONLY for "O" right now)
    """
    neutralValue = 50
    choices = []
    avaliable = board.availableMoves()
    for move in avaliable:
        board.makeMove(move, player)
        alpha = -float('inf')
        beta = float('inf')
        moveValue=tipe(sys.argv[1],board,depth,player,alpha,beta)
        board.makeMove(move, " ")

        if moveValue > neutralValue:
            choices = [move]
            break
        elif moveValue == neutralValue:
            choices.append(move)
    print("choices: ", choices)

    if len(choices) > 0:
        return random.choice(choices)
    else:
        return random.choice(board.availableMoves())





if __name__ == '__main__':
    print("Tipo de ia = "+ sys.argv[1])
    game = TicTacToe()
    game.show()


    while game.gameOver() == False:
        while True:
            person_move = int(input("You are X: Choose number from 1-9: "))-1
            if person_move in game.availableMoves():
                game.makeMove(person_move, "X")

                break
            else:
                print(str(person_move) + " is not a valid move. Try again :v\n\n")


        if game.gameOver() == True:
            break

        print("Computer choosing move...")
        ai_move = make_best_move(game, -1, "O")
        game.makeMove(ai_move, "O")
        game.show()


    print("Game Over. " + game.whoWon() + " Wins")
    game.show()

