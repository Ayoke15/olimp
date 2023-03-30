from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import random
app = Flask(__name__)
api = Api(app)
groups = []
class Participant:
    def __init__(self,id,name,wish,recipient):
        self.id= id
        self.name = name
        self.wish=wish
        self.recipient = recipient
    # def __init__(self,id,name,wish):
    #     self.id =id
    #     self.name = name
    #     self.wish =wish
    def serialize_rec(self):
        return {"id":self.id,
                "name":self.name,
                "wish":self.wish,}
    def serialize(self):
        return {"id":self.id,
                "name":self.name,
                "wish":self.wish,
                "recipient":self.recipient.serialize_rec()}


class Group:
   # participant = []
    def __init__(self,id,name,description,participants):
        self.id = id
        self.name = name
        self.description = description
        self.participants = participants
    def participants_list(self,participants):
        new_par =[]
        for participant in participants:
            new_par.append(participant.serialize())
        return new_par
    def count_par(self):
       num = 0
       for participant in self.participants:
           num += 1
       return num
    def serialize(self):
        return{"id": self.id,
               "name":self.name,
               "description": self.description,
               "participants":self.participants_list(self.participants)
               }
group1= Group(0,"1","present",[Participant(0,"john","teddy",[]),Participant(1,"Ann","toy",[]),Participant(2,"Jim","toy",[])])
group2= Group(1,"3354","two",[Participant(0,"john","teddy",Participant(1,"ann","","")),Participant(1,"Ann","toy",Participant(0,"john","teddy",""))])

groups.append(group1)
groups.append(group2)
@app.route('/group', methods=['POST'])
def add():
    data = request.get_json()
    id = 0
    for group in groups:
        id += 1
    groups.append(Group(id,data["name"],data["description"],[]))
    return jsonify({"id":groups[id].id})
@app.route('/groups', methods=['GET'])
def list():
    group_list =[]
    for group in groups:
        group_list.append([group.id,group.name,group.description])
    return jsonify(group_list)
@app.route('/group/<id>',methods=['GET'])
def get_(id):
    for group in groups:
        if (group.id == int(id)):
            return jsonify(group.serialize())
    return "404"
@app.route('/group/<id>',methods=['PUT'])
def new(id):
    data = request.get_json()
    for group in groups:
        if (group.id == int(id)):
            group[id].name = data["name"]
            group[id].description = data["description"]
    return "404"
@app.route('/group/<id>',methods=['DELETE'])
def delete(id):
    for group in groups:
        if (group.id == int(id)):
            groups.remove(group)
            return "200"
        else:
            return "404"
@app.route('/group/<id>/participant',methods=['POST'])
def add_par(id):
    data = request.get_json()
    for group in groups:
        if (group.id == int(id)):
            idp=0
            for participants in group.participants:
                idp +=1
            group.participants.append(Participant(idp,data["name"],data["wish"],""))
            return str(idp)
        else:
            return "404"
@app.route('/group/<groupId>/participant/<participantId>',methods=['DELETE'])
def delete_mem(groupId,participantId):
    for group in groups:
        if (group.id == int(groupId)):
            for participants in group.participants:
                if (participants.id == int(participantId)):
                    group.participants.remove(participants)
                    return "200"
    return "404"
@app.route('/group/<id>/toss',methods=['POST'])
def rand(id):
    for group in groups:
        if (group.id == int(id)):
            num = group.count_par()
            if (num >= 2):
                array =[]
                for i in range(0,num):
                    array.append(i)
                for participant in group.participants:
                    nid = random.choice(array)
                    # while (nid == participant.id ):
                    #     nid = random.choice(num)
                    participant.recipient = group.participants[nid]
                    array.remove(nid)
                return "200"
            else:
                return "409"
        else:
            return"409"
@app.route('/group/<groupId>/participant/<participantId>/recipient',methods=['GET'])
def group(groupId,participantId):
    for group in groups:
        if (group.id == int(groupId)):
            for participant in group.participants:
                if (participant.id == int(participantId)):
                    return jsonify(participant.recipient.serialize_rec())



app.run(host='0.0.0.0', port=8080)