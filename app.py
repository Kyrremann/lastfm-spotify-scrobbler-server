from flask import Flask, redirect, render_template, request, session
import os
from spotify_connect_scrobbler.lastfm import LastfmClient
from spotify_connect_scrobbler.spotify import SpotifyClient

app = Flask(__name__)
app.secret_key = 'no so secret' # TODO: Pass key with env variable.

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
LASTFM_API_SECRET = os.environ['LASTFM_API_SECRET']
lastfm_client = LastfmClient(LASTFM_API_KEY, LASTFM_API_SECRET)

import task

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/steps/1")
def enter_email():
    # Direct user to authentication Spotify URL.
    # TODO: Set different redirect url.
    auth_url = spotify_client.request_authorization()
    return render_template("step.html", auth_url=auth_url)

@app.route("/steps/2")
def capture_spotify_token():
    # Retrieve Spotify credentials.
    code = request.args.get('code', '')
    spotify_credentials = spotify_client.request_access_token(code)
    session['spotify_credentials'] = spotify_credentials

    # Direct user to authentication Last.fm URL.
    # TODO: Set different redirect url.
    auth_url = lastfm_client.request_authorization()
    return "<a href='{}'>Authenticate Last.fm</a>".format(auth_url)

@app.route("/steps/3")
def capture_lastfm_token():
    # Retrieve Last.fm credentials.
    token = request.args.get('token', '')
    lastfm_credentials = lastfm_client.request_access_token(token)

    spotify_credentials = session['spotify_credentials']
    # TODO: Save credentials to MongoDB
    return "Last.fm credentials: {}\nSpotify credentials: {}".format(spotify_credentials)

@app.route("/scrobble")
def manual_scrobbling():
    task.start_scrobbling()
    return redirect("/")

if __name__ == "__main__":
    app.run(port=4000)
