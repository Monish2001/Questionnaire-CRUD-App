import pymongo

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
except:
    print("ERROR - Cannot connect to DB")

mydb = myclient["questionnaire-app"]

mycol = mydb["questions"]


def displayQuestions(id):
    skipper = 0
    limit = 10
    if id != 1:
        skipper = (id - 1) * limit

    # mycol.find().skip(skipper).limit(limit)

    result = (
        mycol.find({}, {"_id": 0, "qid": 1, "question": 1}).skip(skipper).limit(limit)
    )
    return result


def findTotalDocuments():
    totalDocuments = mycol.find({})
    return len(list(totalDocuments))


def addQuestion(questionDict):
    mycol.insert_one(questionDict)


def updateQuestion(qid, question):
    mycol.update_one({"qid": qid}, {"$set": {"question": question}})


def deleteQuestion(qid):
    mycol.delete_one({"qid": qid})


def displayAnswer(qid, pid):
    skipper = 0
    limit = 10
    if pid != 1:
        skipper = (pid - 1) * limit

    result = mycol.find(
        {"qid": qid},
        {"_id": 0, "qid": 1, "question": 1, "ans": {"$slice": [skipper, limit]}},
    )
    return result


def findTotalAnsDocuments(qid):
    totalDocuments = mycol.find(
        {"qid": qid}, {"_id": 0, "qid": 1, "question": 1, "ans": 1}
    )
    return len(list(totalDocuments[0]["ans"]))


def addAnswer(answerDict):
    qid = answerDict["qid"]
    answerObj = {"answerid": answerDict["answerid"], "answer": answerDict["answer"]}
    mycol.update_one({"qid": qid}, {"$push": {"ans": answerObj}})


def updateAnswer(answerDict):
    qid = answerDict["qid"]
    answerid = answerDict["answerid"]
    answer = answerDict["answer"]

    mycol.update_one(
        {"qid": qid, "ans.answerid": answerid}, {"$set": {"ans.$.answer": answer}}
    )


def deleteAnswer(answerDict):
    qid = answerDict["qid"]
    answerid = answerDict["answerid"]

    mycol.update_one({"qid": qid}, {"$pull": {"ans": {"answerid": answerid}}})
