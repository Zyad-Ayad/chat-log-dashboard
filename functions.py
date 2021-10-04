from flask import redirect, render_template, request, session
import requests


def apology(message, user = None):
    return render_template("error.html", message=message, user=user)



url = 'https://discord.com/api/oauth2/token'
CLIENT_ID = '879273611603619881'
CLIENT_SECRET = 'HNvZD6ymlx8b5-BFtLvv8LTihQT8CNQw'
REDIRECT_URI = 'https://chat-log-dashboard.herokuapp.com/loggedin'
bot_token = "ODc5MjczNjExNjAzNjE5ODgx.YSNVXQ.KiKNaFWWQRvq0Q5zNLy_b7Z41ZA"



def auth(code):

    data = {
      'client_id': CLIENT_ID,
      'client_secret': CLIENT_SECRET,
      'grant_type': 'authorization_code',
      'code': code,
      'redirect_uri': REDIRECT_URI
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    auth_data = ''
    try:
        r = requests.post(url, data=data, headers=headers)
        r.raise_for_status()
        auth_data = r.json()
    except:
        return "ERROR: 1"
    return(f'{auth_data["token_type"]} {auth_data["access_token"]}')

    
    
    
def get_user_data(auth_key):

    
    headers = {
       'authorization': auth_key
      }
   
    try:
        r = requests.get("https://discord.com/api/users/@me", headers=headers)
        r.raise_for_status()
        return r.json()
    except:
        return "ERROR: 2"

def get_user_guilds(auth_key):
    headers = {
       'authorization': auth_key
      }

    all_guilds = {}
    try:
        r = requests.get("https://discord.com/api/users/@me/guilds", headers=headers)
        r.raise_for_status()
        all_guilds = r.json()
    except:
        return "ERROR: 3"

    a_m_guilds = admin_mutual_guilds(all_guilds)

    return a_m_guilds

        
    
def admin_mutual_guilds(guilds):
    headers = {
       'authorization': f"Bot {bot_token}"
      }

    mutual_guilds = []

    for guild in guilds:
        try:
            r = requests.get(f"https://discord.com/api/guilds/{guild['id']}", headers=headers)
            r.raise_for_status()
            mutual_guilds.append(guild)
        except:
            pass
    
    admin_guilds = {}

    for guild in mutual_guilds:
        if (guild['permissions'] & 0x8) == 0x8:
            admin_guilds[guild['id']] = guild

    return admin_guilds




def get_channels(server_id):
    headers = {
       'authorization': f"Bot {bot_token}"
    }

    channels = {}
    text_channels = {}

    try:
        r = requests.get(f"https://discord.com/api/guilds/{server_id}/channels", headers=headers)
        r.raise_for_status()
        channels = r.json()
    except:
        pass

    for channel in channels:
        if channel["type"] == 0:
            text_channels[channel["id"]] = channel

    return text_channels
            



