
import json
from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
import requests
from cdmsapp.models import pincodeModel

from cdmsapp.schemas import IndiaPincodeSchema


blp = Blueprint("external", "externals", description="Operations on external apis")

@blp.route("/external/pincode")
class IndiaPincode(MethodView):
    @blp.arguments(IndiaPincodeSchema)
    def post(self, _payload):
        url = "https://pincode.p.rapidapi.com/"
        payload = pincodeModel()
        payload.searchby = "pincode"
        payload.value = _payload['value']
        json_payload = {
            "searchBy": payload.searchby,
            "value": payload.value
        }

        headers = {
            "content-type": "application/json",
            "Content-Type": "application/json",
            "X-RapidAPI-Key": "c4b7a5db43msh73ce9d48e29aaa6p1de149jsnfccde7fc5c45",
            "X-RapidAPI-Host": "pincode.p.rapidapi.com"
        }
        #first check in the our own database and return
    # write code here for checking in the local database */
    # if it is not available in the database check from rapid api
        try:
            response = requests.request("POST", url, json=json_payload, headers=headers)
            return_json = json.loads(response.text)
            print(response.text)
            # write code for inserting  the dictionary in the local database
            # for loop to iterate through each data
        except:
            return {"message":"failure"}

        return return_json[0]

# home url = "https://rapidapi.com/navii/api/pin-codes-india"