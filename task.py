from spotify_connect_scrobbler import scrobbler
import sys, os, json

def create_tmp_config_file():
    data = {}
    data["lastfm"] = { "session_key" : os.environ['LASTFM_SESSION_KEY'] }
    data["spotify"] = { "access_token": os.environ['SPOTIFY_ACCESS_TOKEN'],
                        "token_type": "Bearer",
                        "refresh_token": os.environ['SPOTIFY_REFRESH_TOKEN'],
                        "scope": "user-read-recently-played" }
    with open('scrobbler.config', 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

def start_scrobbling():
    sys.argv = ["task.py", "scrobbler.config"]
    scrobbler.main()

if __name__ == "__main__":
    create_tmp_config_file()
    start_scrobbling()
