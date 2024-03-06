from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = {1: " ", 2: " ", 3: " ",
         4: " ", 5: " ", 6: " ",
         7: " ", 8: " ", 9: " "}
turn = "x"
game_end = False
mode = "singlePlayer"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    global turn, game_end
    if game_end:
        return jsonify({'status': 'Game ended'})
    position = int(request.form['position'])
    if board[position] == " ":
        if turn == "x":
            board[position] = turn
            if check_for_win(turn):
                game_end = True
            turn = "o"
            if mode == "singlePlayer" and not game_end:
                play_computer()
                if check_for_win(turn):
                    game_end = True
                turn = "x"
        else:
            board[position] = turn
            if check_for_win(turn):
                game_end = True
            turn = "x"
        return jsonify({'status': 'success', 'board': board})
    else:
        return jsonify({'status': 'invalid move'})

def check_for_win(player):
    # Check rows
    if (board[1] == board[2] == board[3] == player or
            board[4] == board[5] == board[6] == player or
            board[7] == board[8] == board[9] == player or
            # Check columns
            board[1] == board[4] == board[7] == player or
            board[2] == board[5] == board[8] == player or
            board[3] == board[6] == board[9] == player or
            # Check diagonals
            board[1] == board[5] == board[9] == player or
            board[3] == board[5] == board[7] == player):
        return True
    return False

def check_for_draw():
    for i in board.keys():
        if board[i] == " ":
            return False
    return True

def play_computer():
    best_score = -10
    best_move = 0
    for key in board.keys():
        if board[key] == " ":
            board[key] = "o"
            score = minimax(board, False)
            board[key] = " "
            if score > best_score:
                best_score = score
                best_move = key
    board[best_move] = "o"

def minimax(board, is_maximizing):
    if check_for_win("o"):
        return 1
    if check_for_win("x"):
        return -1
    if check_for_draw():
        return 0
    if is_maximizing:
        best_score = -1
        for key in board.keys():
            if board[key] == " ":
                board[key] = "o"
                score = minimax(board, False)
                board[key] = " "
                if score > best_score:
                    best_score = score
        return best_score
    else:
        best_score = 1
        for key in board.keys():
            if board[key] == " ":
                board[key] = "x"
                score = minimax(board, True)
                board[key] = " "
                if score < best_score:
                    best_score = score
        return best_score

if __name__ == '__main__':
    app.run(debug=True)
