from flask import Flask, request, jsonify, flash, redirect, url_for, render_template, send_file, make_response, session 
from os.path import join, dirname, realpath
import random



# import os


UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'upload_folder')
ALLOWED_EXTENSIONS = {'csv'}


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/test')
def test():
    session.clear()

    return "testing test"


@app.route('/game_over')
def game_over():

    score = request.args.get('score', type=int)
    print("game_over score:", score)
    session['latest_score'] = score
    
    # Do something with the score, for example, store it in the session
    if score is not None and (score > session['high_score']) :
        session['high_score'] = score
    
    return render_template('game_over.html', score=score)

@app.route("/", methods=['post', 'get'])
def main():

    # if not session.get('high_score'):
    if 'high_score' not in session:
        print("initialising session score")
        session['high_score'] = 0
        session['latest_score'] = 0

    
    high_score = session['high_score']
    latest_score = session['latest_score']

    # print("===in main method===")
    if request.method == 'POST':
        # print("in main method but post called")
        operation = request.form.get('mathOperation')
        # print("Operation:", operation)
        # print("redirecting..")
        # return url_for("game", operation = operation)
        return redirect(url_for('game', operation=operation))

    return render_template('choose_game.html', high_score=high_score, latest_score=latest_score)

#assign URLs to have a particular route 
global seen_list
seen_list = []
@app.route("/game", methods=['post', 'get'])
def game():
    message = ''

    if request.method == 'POST':
        print("POST METHOD CALLED FOR GAME")
        operation = request.form['mathOperation']
        session['operation'] = operation
        print("operation in /game:", operation)
    else:
        operation = session['operation']
        print("current session['operation']:", operation)

    print("seen_list:", seen_list)
    while True:
        number1, number2 = generate_pair()
        # print("number1:", number1)
        # print("number2:", number2)
        if (number1, number2) not in seen_list:
            seen_list.append((number1,number2))
            break

    ## check if pair has appeared, if not appeared then add to list and continue, else if appeared then keep re-roll:
    if operation == "all":
        operator = '+-X÷'
        chosen_operator = operator[random.randint(0,3)]
        print("chosen_operator:", chosen_operator)
        try:
            if chosen_operator == '+':
                answer = number1+number2
            elif chosen_operator == '-':
                answer = number1-number2
            elif chosen_operator == 'X':
                answer = number1*number2
            elif chosen_operator == '÷':
                answer = number1/number2
                answer = round(answer,2)
        except:
            ## catch divided by 0 error
            chosen_operator = operator[random.randint(0,2)]
            if chosen_operator == '+':
                answer = number1+number2
            elif chosen_operator == '-':
                answer = number1-number2
            elif chosen_operator == 'X':
                answer = number1*number2
        # print("answer:", answer)
                
        # return render_template('game.html', number1=number1, number2=number2, chosen_operator=chosen_operator, answer=answer)

    elif operation =="addition":
        answer = number1+number2
        chosen_operator = "+"
    
    elif operation =="subtraction":
        answer = number1-number2
        chosen_operator = '-'

    elif operation == "multiplication":
        answer = number1*number2
        chosen_operator = 'X'

    elif operation =="division":
        chosen_operator = '÷'
        try:
            answer = round(number1/number2,2)
        except:
            while True:
                number1, number2 = generate_pair()
                if (number1, number2) not in seen_list:
                    seen_list.append((number1,number2))
                    
                    try: 
                        answer = round(number1/number2,2)
                        break
                    except:
                        continue

    print('answer:', answer)
    return render_template('game.html', number1=number1, number2=number2, chosen_operator=chosen_operator, answer=answer, operation=operation)

def generate_pair():
    number1 = random.randint(0, 12)
    number2 = random.randint(0, 12)
    return number1, number2




if __name__ == "__main__":

    app.run(debug=True, use_reloader=True, port=5000, threaded=True)
