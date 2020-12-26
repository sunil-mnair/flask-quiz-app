from flask import Flask,render_template,request,url_for,redirect,session,flash
from datetime import datetime

import json


# Load the JSON File into a dictionary
with open('quiz.json') as file:
    quizapp = json.load(file)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'



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

        # Pick the First Question from the selected theme
        session["current_question"] = [game for game in session["game"][session["theme"]]][session["current_question_id"]-1]

        return render_template("start_quiz.html",
        game = session["current_question"])

    return render_template("quiz.html",
    quizapp = quizapp)


@app.route('/start_quiz',methods=['GET','POST'])
def start_quiz():
    
    if request.method == "POST":
        
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

    return render_template("start_quiz.html",
    game = session["current_question"])

if __name__ == "__main__":
    app.run(debug=True)