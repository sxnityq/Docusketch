from bson import ObjectId
from datetime import datetime
import json


class DataValidator:
    
    @staticmethod
    def collectErrors(request: dict, reqFields: list) -> dict: 
        _errors = {}
        for field in reqFields:
            if request.get(field, None) is None:
                _errors[field] = f"{field} is required"
        return _errors
    
    @staticmethod
    def updateFieldsChecker(request: dict, reqFields: list) -> dict:
        _errors = {}
        for field in request:
            if field not in reqFields:
                _errors[field] = f"unknown field {field}"
        return _errors

    @staticmethod
    def convertNestedRequest(request: dict) -> dict:
        _convertedRequest = {}
        for outerKey, outerValue in request.items():
            for innerKey, innerValue in outerValue.items():
                _convertedRequest[f"{outerKey}.{innerKey}"] = innerValue
        return _convertedRequest


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)