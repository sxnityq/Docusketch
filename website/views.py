from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

from flask import Blueprint, jsonify, request

from mongoInit import coll
from .settings import requiredHardFields, requiredRamFields, mongoDocumentFieldLis
from .utils import DataValidator, MongoJSONEncoder


views = Blueprint('views', __name__)


@views.route('/task', methods=['GET'])
def get():
    tasks = []
    for i in coll.find():
        tasks.append(i)
    return jsonify( MongoJSONEncoder().encode(tasks) )


@views.route('/task', methods=['POST'])
def create():
    
    if not request.data or not request.is_json:
        return jsonify(
            {
                "error" : "provided request is incorrect ot empty"
            }
        )
    
    HardMemo = request.json.get("HardMemo", '')
    RAM = request.json.get("RAM", '')
    
    if not HardMemo or not RAM:
        return jsonify(
            {
                "error" : "please provide RAM or HardMemo headers"
            }
        )
    
    reqValidator = DataValidator()
    errorsHard = reqValidator.collectErrors(request=HardMemo, reqFields=requiredHardFields)
    errorsRam = reqValidator.collectErrors(request=RAM, reqFields=requiredRamFields)
    
    if errorsHard or errorsRam:
        return jsonify(
                {
                    "Hard errors" : errorsHard,
                    "RAM errors" : errorsRam
                })
    
    res = request.json
    res['time'] = datetime.now()
    coll.insert_one(res)
    return jsonify( MongoJSONEncoder().encode(res) )


@views.route('/task', methods=['PUT'])
def update():
    
    if not request.data or not request.is_json:
        return jsonify(
            {
                "error" : "provided request is incorrect or empty"
            }
        )
        
    if not request.json.get("_id", ""):
        return jsonify(
            {
                "error" : "incorrect request. Are you specified _id header?"
            }
        )
            
    HardMemo = request.json.get("HardMemo", '')
    RAM = request.json.get("RAM", '')
    reqValidator = DataValidator()
    isNotValidReq = reqValidator.updateFieldsChecker(request=request.json.keys(),
                                     reqFields=mongoDocumentFieldLis)
    
    if isNotValidReq:
       return jsonify(
           {
               "error" : isNotValidReq
           }
       )
    
    errorsHard = reqValidator.updateFieldsChecker(request=HardMemo, reqFields=requiredHardFields)
    errorsRam = reqValidator.updateFieldsChecker(request=RAM, reqFields=requiredRamFields)
    
    if errorsHard or errorsRam:
        return jsonify(
                {
                    "Hard errors" : errorsHard,
                    "RAM errors" : errorsRam
                })
    
    try:
        reqId = ObjectId(request.json.get('_id'))
    except InvalidId as ex:
        return jsonify(
            {
                "invalid _id" : f"{ex}"
            })
    
    req = request.json
    req.pop("_id")
    convertedRequest = reqValidator.convertNestedRequest(req)
    query = {"_id" : reqId}
    newValue = {"$set" : convertedRequest}
    coll.update_many(query, newValue)
    
    result = coll.find_one( reqId )
    return jsonify( MongoJSONEncoder().encode(result) )
        
    