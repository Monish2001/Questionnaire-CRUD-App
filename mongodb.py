import pymongo
from pymongo import MongoClient

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
except:
    print("ERROR - Cannot connect to DB")

mydb = myclient["questionnaire-app"]

mycol = mydb["questions"]


def displayQuestions():
    result = mycol.find({}, {"_id": 0, "qid": 1, "question": 1})
    return list(result)


def addQuestion(questionDict):
    mycol.insert_one(questionDict)
    result = mycol.find({}, {"_id": 0, "qid": 1, "question": 1})
    # print(list(result))
    # for i in mycol.find({}, {"_id": 0, "qid": 1, "question": 1}):
    #     print(i)
    return list(result)


def updateQuestion(qid, question):
    dbResponse = mycol.update_one({"qid": qid}, {"$set": {"question": question}})
    result = mycol.find({}, {"_id": 0, "qid": 1, "question": 1})
    return list(result)


def deleteQuestion(qid):
    mycol.delete_one({"qid": qid})
    result = mycol.find({}, {"_id": 0, "qid": 1, "question": 1})
    return list(result)


def addAnswer(answerDict):
    qid = answerDict["qid"]
    # answerid = answerDict["answerid"]
    # answer = answerDict["answer"]
    answerObj = {"answerid": answerDict["answerid"], "answer": answerDict["answer"]}
    mycol.update_one({"qid": qid}, {"$push": {"ans": answerObj}})
    result = mycol.find({"qid": qid}, {"_id": 0})
    return list(result)


def updateAnswer(answerDict):
    qid = answerDict["qid"]
    answerObj = {"answerid": answerDict["answerid"], "answer": answerDict["answer"]}
    answerid = answerDict["answerid"]
    answer = answerDict["answer"]

    mycol.update_one(
        query={"qid": qid, "ans": {"$elemMatch": {"answerId": answerDict["answerid"]}}},
        update={
            "$set": {
                "ans.$.answerId": answerObj.answerId,
                "ans.$.answer": answerObj.answer,
            }
        },
    )
    # mycol.findOneAndUpdate(
    #     {"qid": qid, "ans.answerid": answerid}, {"$set": {"ans.answer": answer}}
    # )

    # mycol.update({"qid":qid},{"$set":{}})

    # mycol.update_one({"qid": qid}, {"$pull": {"ans": {"answerid": answerid}}})
    # mycol.update_one({"qid": qid}, {"$push": {"ans": answerObj}})

    # mycol.find_and_modify(
    #     query={"qid": qid, "answer.answerid": answerDict["answerid"]},
    #     update={"$set": answerObj},
    # )
    # mycol.update_one({"qid": qid}, {"$push": {"ans": {"answerid":answerDict["answerid"]}}})

    #     db.demo553.findOneAndUpdate(
    # ...    { id:101,
    # ...       "midExamDetails.SubjectName":"MongoDB"
    # ...    },
    # ...    { $set:{
    # ...       'midExamDetails.$.Marks': 97
    # ...    }
    # ... }
    # ... );
    result = mycol.find({"qid": qid}, {"_id": 0})
    return list(result)


def deleteAnswer(answerDict):
    qid = answerDict["qid"]
    answerid = answerDict["answerid"]

    mycol.update_one({"qid": qid}, {"$pull": {"ans": {"answerid": answerid}}})
    result = mycol.find({"qid": qid}, {"_id": 0})
    return list(result)


def displayQuestionAndAnswer(qid):
    result = mycol.find({"qid": qid}, {"_id": 0})
    return list(result)
