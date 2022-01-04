import pymongo
from flask import session, request

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

users_db = myclient["users"]

teams_db = myclient["teams"]

tiers_db = myclient["tiers"]

#users = {
    #"matt@example.com":{"password":"hello",
                        # "first_name":"Matthew",
                         #"last_name":"Lim"},
#}

#teams = {
    #{"code":NumberInt(100),"name":"Acend","Region":"EU", "Achievements":"VCT 2021 Champions", "Record":"99-1"},
    #{"code":NumberInt(200),"name":"Sentinels","Region":"NA", "Achievements":"VCT Masters Winners", "Record":"23-7"},
    #{"code":NumberInt(300),"name":"Team Secret","Region":"SEA", "Achievements":"VCT SEA Playoffs Winners", "Record":"7-2"},
#}

#tiers = {
    #{"code":NumberInt(100),"name":"Team", "price":500},
    #{"code":NumberInt(200),"name":"Organization", "price":1000},
#}

def get_user(username):
    profile_coll = users_db['profile']
    user = profile_coll.find_one({"username":username})
    return user

def get_password(username):
    return get_user(username)["password"]

def change_password(username,newpassword):
    profile_coll = users_db["profile"]
    changepassword = profile_coll.update_one({"username":username}, {"$set":{"password":newpassword}})
    return changepassword

def create_posts(posts):
    messages_coll = users_db['messages']
    messages_coll.insert(posts)

def view_message_history():
    history = []
    messages_coll = users_db['messages']
    curruser = messages_coll.find({'username':session["user"]["username"]})
    for username in curruser:
        for o in username["messages"]:
            history.append(o)
    return history

def get_team(code):
    teams_coll = teams_db['team']
    team = teams_coll.find_one({"code":code})
    return team

def get_teams():
    team_list = []
    teams_coll = teams_db['team']

    for t in teams_coll.find({}):
        team_list.append(t)

    return team_list

def get_tier(code):
    tiers_coll = tiers_db["tier"]
    tier = tiers_coll.find_one({"code":code})
    return tier

def get_tiers():
    tier_list = []
    tiers_coll = tiers_db["tier"]

    for r in tiers_coll.find({}):
        tier_list.append(r)

    return tier_list

def create_purchase(purchase):
    purchase_coll = users_db['purchase']
    purchase_coll.insert(purchase)

def view_purchase_history():
    history = []
    purchase_coll = users_db['purchase']
    curruser = purchase_coll.find({'username':session["user"]["username"]})
    for username in curruser:
        for o in username["details"]:
            history.append(o)
    return history

def get_user_tier(username):
    return get_user(username)["tier"]

def update_user_tier(username,newtier):
    profile_coll = users_db["profile"]
    update_tier = profile_coll.update_one({"username":username}, {"$set":{"tier":newtier}})
    return update_tier
