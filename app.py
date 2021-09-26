import uuid
from flask_paginate import Pagination, get_page_parameter
import pymongo
from flask import Flask, render_template, request, url_for, redirect

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
except:
    print("ERROR - Cannot connect to DB")
mydb = myclient["questionnaire-app"]
mycol = mydb["questions"]
app = Flask(__name__)


@app.route("/")
def displayQuestion():
    result = mycol.find({}, {"_id": 0, "qid": 1, "question": 1})
    return render_template("index.html", questions=list(result))


@app.route("/view-answer/<id>/", methods=["GET", "POST"])
def ViewAnswer(id):
    result = mycol.find({"qid": id}, {"_id": 0, "qid": 1, "question": 1, "ans": 1})
    return render_template("answers.html", answers=result[0], qid=id)


@app.route("/question", methods=["POST"])
def addQuestion():
    if request.method == "POST":
        question = request.form["question"]
        qid = str(uuid.uuid1())
        questionDict = {"qid": qid, "question": question, "ans": []}
        mycol.insert_one(questionDict)
        return redirect(url_for("displayQuestion"))


@app.route("/insertanswer", methods=["POST"])
def insertanswer():
    if request.method == "POST":
        answer = request.form["answer"]
        qid = request.form["qid"]
        aid = str(uuid.uuid1())
        answerObj = {"answerid": aid, "answer": answer}

        mycol.update_one({"qid": qid}, {"$push": {"ans": answerObj}})

        return redirect("/view-answer/" + qid)


@app.route("/question/<id>/", methods=["GET", "DELETE"])
def deleteQuestion(id):
    mycol.delete_one({"qid": id})
    return redirect(url_for("displayQuestion"))


@app.route("/delete-a/<qid>/<aid>/", methods=["GET", "POST"])
def deleteAnswer(qid, aid):
    mycol.update_one({"qid": qid}, {"$pull": {"ans": {"answerid": aid}}})
    return redirect("/view-answer/" + qid)


@app.route("/update", methods=["GET", "POST"])
def updateQuestion():
    if request.method == "POST":
        print(request.form["qid"])
        mycol.update_one(
            {"qid": request.form["qid"]},
            {"$set": {"question": request.form["question"]}},
        )
        return redirect(url_for("displayQuestion"))


@app.route("/updateanswer", methods=["GET", "POST"])
def updateanswer():
    if request.method == "POST":
        qid = request.form["qid"]
        aid = request.form["aid"]
        answer = request.form["answer"]
        print(qid)
        print(aid)
        print(answer)

        # mycol.update_one({"qid": request.form['qid']}, {"$set": {"question": request.form['question']}})

        return redirect("/view-answer/" + qid)


if __name__ == "__main__":
    app.run(debug=True)
