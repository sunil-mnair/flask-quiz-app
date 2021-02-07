from flask import Flask,render_template,request,url_for,redirect,session,flash
from datetime import datetime

import json


# Load the JSON File into a dictionary
with open('quiz.json') as file:
    quizapp = json.load(file)

with open('players.json') as file:
    players = json.load(file)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'


@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        session["player"] = request.form["player"].title()

        return redirect(url_for('quiz'))

    return render_template('index.html')

@app.route("/quiz",methods=['GET','POST'])
def quiz():

    if request.method == 'POST':
        
        # Store the theme in a session variable
        session["theme"] = request.form["theme"]

        # Store all the questions, choices and correct answer for the selected theme
        session["game"] = [{theme:questions} for (theme,questions) in quizapp.items() if theme==session["theme"]][0]
        
        # Sum of questions for the selected theme
        session["total_questions"] = len(session["game"][session["theme"]])

        # Starting ID for 1st question
        session["current_question_id"] =  1

        # Starting Score
        session["score"] = 0
        session["status"] = 1

        # Pick the First Question from the selected theme
        session["current_question"] = [game for game in session["game"][session["theme"]]][session["current_question_id"]-1]

        return render_template("start_quiz.html",
        game = session["current_question"])


    return render_template("quiz.html",
    quizapp = quizapp)


@app.route('/start_quiz',methods=['GET','POST'])
def start_quiz():
    
    if request.method == "POST" and session["status"]==1:
        
        # Gather the answer provided by the player
        given_answer = request.form["given_answer"]

        # If Condition to check the answer
        if given_answer == session["current_question"]["answer"]:
            flash("Correct Answer","correct")
            session["score"] += 1
        else:
            flash("Incorrect Answer","wrong")


        # Proceed to next question
        if session["total_questions"] > session["current_question_id"]:
            session["current_question_id"] += 1
            session["current_question"] = [game for game in session["game"][session["theme"]]][session["current_question_id"]-1]
        else:
            flash("Quiz Completed. Try another Theme","completed")
            
            session["status"] = 0

            # Store the Player details to the JSON File
            # Player does not exist, add the new player with their score
            if not session["player"] in [player['name'] for player in players]: 
                player_details = {'name' : session["player"],
                    'score' : session["score"],
                    'theme' : session["theme"]}

                players.append(player_details)
            # Player Exists then update their score if greater than previous attempt
            else:
                for player in players:
                    if player["name"] == session["player"] and player["theme"] == session["theme"]: 
                        if player["score"] < session["score"]: player["score"] = session["score"]

            # Sort the JSON File in the order of highest score
            with open('players.json','w') as file:
                players.sort(key=lambda k: k['score'],reverse = True) 
                json.dump(players,file,indent = 2)

    return render_template("start_quiz.html",
    game = session["current_question"],
    players=[p for p in players if p["theme"]==session["theme"]])

if __name__ == "__main__":
    app.run(debug=True)