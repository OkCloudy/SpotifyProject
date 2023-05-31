import requests
import os
from dotenv import load_dotenv
import base64
import json

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

def dumpJson(jsonResponse):
    print(json.dumps(jsonResponse,indent=2))

def requestAccessToken():
    url = "https://accounts.spotify.com/api/token"
    # concate our client id and secret to correct format
    client_info = f"{client_id}:{client_secret}"
    # encode client info into base64
    client_info64 = base64.b64encode(client_info.encode()).decode()
    headers = {
        "Authorization": "Basic " + client_info64,
        "Content-type": "application/x-www-form-urlencoded"
    }
    body = {
        "grant_type": "client_credentials"
    }
    json = requests.post(url,headers=headers,data=body)
    response_data = json.json()
    return response_data["access_token"]

def tokenHeader(token):
    return {"Authorization": "Bearer " + token}

def getTopTracks(tokenHeader, artistID):
    url = f"https://api.spotify.com/v1/artists/{artistID}/top-tracks?country=US"
    json_response = requests.get(url, headers=tokenHeader)
    response_data = json_response.json()
    tracks = response_data["tracks"]
    for track in tracks:
        print(track["name"])

# returns meta data of artist
def searchArtist(tokenHeader,artist):
    url = f"https://api.spotify.com/v1/search?q={artist}&type=artist"
    json_response = requests.get(url,headers=tokenHeader)
    response_data = json_response.json()
    searchedArtist = response_data["artists"]["items"][0]
    return searchedArtist
    #print(dumpJson(response_data))

def get_users_playlists(user_id):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    
def get_current_userID(tokenHeader):
    url = "https://api.spotify.com/v1/me"
    json_response = requests.get(url, headers=tokenHeader)
    print(json_response)
    response_data = json_response.json()

def request_auth_code():
    url = "https://accounts.spotify.com/authorize?"
    payload = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-read-email user-read-private"
    }
    json_response = requests.get(url, payload)
    print("AUTH CODE",json_response)
    response_data = json_response.json()
    #print(dumpJson(response_data))


accessToken = requestAccessToken()
tokenH = tokenHeader(accessToken)
artist = searchArtist(tokenH, "Kanye West")
artistID = artist["uri"].split(":")[2]
print(artistID)
getTopTracks(tokenH, artistID)
request_auth_code()