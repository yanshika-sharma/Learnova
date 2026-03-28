from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

feedback_list = []
study_progress = {}



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/planner", methods=["POST"])
def planner():

    data = request.json

    days = int(data["days"])
    subjects = data["subjects"].split(",")

    subjects = [s.strip() for s in subjects]

    start_date = datetime.today()

    plan = []

    subject_index = 0

    for i in range(days):

        date = start_date + timedelta(days=i)

        subject = subjects[subject_index]

        
        if i < 2:
            hours = 6
        elif i < 5:
            hours = 5
        else:
            hours = 4

        plan.append({
            "date": date.strftime("%d %B"),
            "subject": subject,
            "hours": hours
        })

        subject_index += 1

        if subject_index >= len(subjects):
            subject_index = 0

    return jsonify(plan)



@app.route("/feedback", methods=["POST"])
def feedback():

    data = request.json

    comment = data["comment"]

    feedback_list.append(comment)

    return jsonify(feedback_list)



@app.route("/progress", methods=["POST"])
def progress():

    data = request.json

    subject = data["subject"]
    hours = int(data["hours"])

    if subject in study_progress:
        study_progress[subject] += hours
    else:
        study_progress[subject] = hours

    return jsonify(study_progress)



@app.route("/quiz", methods=["POST"])
def quiz():

    data = request.json

    answer = data["answer"]

    if answer == "-1":
        result = "Correct! i² = -1"
    else:
        result = "Wrong Answer. Try again. We know you can do better buddy!"

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
