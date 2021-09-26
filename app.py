import uuid

from flask import Flask, render_template, request, url_for, redirect

import mongodb

app = Flask(__name__)


@app.route("/")
def displayQuestion():
    return redirect("/viewQ/" + str(1))


@app.route("/viewQ/<id>/")
def viewAllQuestion(id=0):
    try:
        result = mongodb.displayQuestions(int(id))
        return render_template("index.html", questions=list(result), pre=getPre(int(id)), next=int(id) + 1,
                               current=int(id), maxPage=10)
    except Exception as ex:
        print("*******************")
        print(ex)
        print("*******************")


def getPre(current):
    if current != 1:
        return current - 1
    else:
        return 1


@app.route("/question", methods=["POST"])
def addQuestion():
    try:
        if request.method == "POST":
            question = request.form["question"]
            qid = str(uuid.uuid1())
            questionDict = {"qid": qid, "question": question, "ans": []}
            mongodb.addQuestion(questionDict)
            return redirect(url_for("displayQuestion"))
    except Exception as ex:
        print("*******************")
        print(ex)
        print("*******************")


@app.route("/update", methods=["GET", "POST"])
def updateQuestion():
    try:
        if request.method == "POST":
            qid = request.form["qid"]
            question = request.form["question"]
            mongodb.updateQuestion(qid, question)
            return redirect(url_for("displayQuestion"))
    except Exception as ex:
        print("*******************")
        print(ex)
        print("*******************")


@app.route("/question/<id>/", methods=["GET", "DELETE"])
def deleteQuestion(id):
    try:
        mongodb.deleteQuestion(id)
        return redirect(url_for("displayQuestion"))
    except Exception as ex:
        print("*******************")
        print(ex)
        print("*******************")


@app.route("/view-answer/<qid>/", methods=["GET", "POST"])
def ViewAnswer(qid):
    try:
        result = mongodb.displayAnswer(qid)
        return render_template("answers.html", answers=result[0], qid=qid)
    except Exception as ex:
        print("*******************")
        print(ex)
        print("*******************")


@app.route("/insertanswer", methods=["POST"])
def insertanswer():
    try:
        if request.method == "POST":
            answer = request.form["answer"]
            qid = request.form["qid"]
            aid = str(uuid.uuid1())
            answerObj = {"qid": qid, "answerid": aid, "answer": answer}
            mongodb.addAnswer(answerObj)

            return redirect("/view-answer/" + qid)
    except Exception as ex:
        print("*******************")
        print(ex)
        print("*******************")


@app.route("/updateanswer", methods=["GET", "POST"])
def updateanswer():
    try:
        if request.method == "POST":
            qid = request.form["qid"]
            aid = request.form["aid"]
            answer = request.form["answer"]
            answerDict = {"qid": qid, "answerid": aid, "answer": answer}
            mongodb.updateAnswer(answerDict)

            return redirect("/view-answer/" + qid)
    except Exception as ex:
        print("*******************")
        print(ex)
        print("*******************")


@app.route("/delete-a/<qid>/<aid>/", methods=["GET", "POST"])
def deleteAnswer(qid, aid):
    try:
        answerDict = {"qid": qid, "answerid": aid}
        mongodb.deleteAnswer(answerDict)
        return redirect("/view-answer/" + qid)
    except Exception as ex:
        print("*******************")
        print(ex)
        print("*******************")


if __name__ == "__main__":
    app.run(debug=True)
