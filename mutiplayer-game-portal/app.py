import streamlit as st
from pymongo import MongoClient


MONGO_URI = "mongodb+srv://admin:admin123@cluster0.cfb53hp.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)


db = client["multiplayer_game_db"]
collection = db["players"]
game_collection = db["game"]


st.title("🎮 Multiplayer Online Game ")

menu = st.sidebar.selectbox("Menu", 
["Add Player", "View Players",
 "Add Game", "View Games",
 "View Leaderboard"])

if menu == "Add Player":
    st.subheader("Add New Player")
    
    username = st.text_input("Username")
    game = st.text_input("Game Name")
    score = st.number_input("Score", min_value=0)

    if st.button("Add Player"):
        collection.insert_one({
            "username": username,
            "game": game,
            "score": score
        })
        st.success("Player added successfully!")

elif menu == "View Players":
    st.subheader("All Players")
    players = collection.find()
    for player in players:
        st.write(player)

elif menu == "Add Game":
    st.subheader("Add New Game")

    game_name = st.text_input("Game Name")
    description = st.text_input("Description")
    item_type = st.text_input("Game Type")

    if st.button("Add Game"):
        game_collection.insert_one({
            "game_name": game_name,
            "description": description,
            "type": item_type
        })
        st.success("Item added successfully!")

elif menu == "View Games":
    st.subheader("All Games")

    games = list(game_collection.find())

    st.write("Number of games found:", len(games))

    if len(games) == 0:
        st.warning("No games available in database.")
    else:
        for game in games:
            st.write(game)

elif menu == "View Leaderboard":
    st.subheader("🏆 Leaderboard")

    # Get players sorted by score (highest first)
    players = list(collection.find().sort("score", -1))

    if len(players) == 0:
        st.warning("No players available.")
    else:
        rank = 1
        for player in players:
            st.write(f"Rank {rank}")
            st.write(f"Username: {player['username']}")
            st.write(f"Game: {player['game']}")
            st.write(f"Score: {player['score']}")
            st.write("----------------------------")
            rank += 1

