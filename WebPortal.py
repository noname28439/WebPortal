NN_SETTINGS_NAME = "WebPortal"

from flask import Flask, Markup, request, session, redirect, render_template
import requests
from threading import Thread
import time

def SETTINGS_READ_PARAMETER(key):
    PATH = '/home/pi/settings/settings'
    try:
        with open(PATH, 'r') as file:
            read = file.read().replace(' ', '').split('\n')
            content = []
            for line in read:
                if not line == '':
                    content.append(line)
            section = ''
            for line in content:
                if line.startswith('--'):
                    section = line.replace('--', '')
                    pass
                if section == NN_SETTINGS_NAME:
                    if line.split(':')[0] == key:
                        return line.split(':')[1]
    except Exception:
        return None


app = Flask(__name__)



def website_on(link):
    try:
        requests.get(link)
    except requests.exceptions.ConnectionError:
        return False
    else:
        return True

reachability_list = {}


def thread_requesting():
    while True:
        for item in serviceList:
            url = item[1]
            reachability_list[url] = website_on(url)
        #print(reachability_list)
        time.sleep(30)

state_on = "🍏online"
state_off = "🍎offline"

#Syntax: Name, onRequestAdress
serviceList = [["ModGame", "http://nonamenetwork.hopto.org:25568"], ["AccessCore", "http://nonamenetwork.hopto.org:187/"], ["ODIN", "http://nonamenetwork.hopto.org:25569/"]]
def listServiceStates():
    toReturn = ""
    for item in serviceList:
        name = item[0]
        url = item[1]
        innerBuild = ""
        innerBuild += "<li>"
        innerBuild += f"<span class='hvr-shrink'><a href='{url}' class='ProjectName'>{name}</a></span><br>"
        if url in reachability_list:
            on = reachability_list[url]
        else:
            on = False
        color = ""
        msg = ""
        if on:
            color = "green"
            msg = state_on
        else:
            color = "red"
            msg = state_off
        innerBuild += f"<span class='retype onstate' style='color: {color};'>{msg}</span>"
        innerBuild += "</li>"

        toReturn += innerBuild
    return toReturn


@app.route("/", methods=["POST", "GET"])
def main():
    return render_template("index.html", PY_ON_SERVICES=Markup(listServiceStates()))



if __name__ == "__main__":
    requester = Thread(target=thread_requesting)
    requester.daemon = True
    requester.start()

    port = 25565
    if SETTINGS_READ_PARAMETER("port") != None:
        port = int(SETTINGS_READ_PARAMETER("port"))

    debug = True
    if SETTINGS_READ_PARAMETER("debug") != None:
        print("found...")
        debug = SETTINGS_READ_PARAMETER("debug")
    print(f"Red --> Debug: {debug} | port: {port}")
    app.run(debug=debug, host="0.0.0.0", port=port, threaded=True)

