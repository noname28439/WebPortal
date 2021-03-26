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


#Syntax: "header", "classes", opened on website load
DROPDOWN_LIST = [
    ["Pyton", [
                ["Flask WebServers", []],
                ["Selenium", []],
                ["Basic Python", []]
              ]
     ],
    ["Java", [
                ["Socket Programming", [
                    ["What is socket programming?", "Sockets are a way of transferring information over the Internet with the TCP protocol.", False],
                    ["Where did you use socket programming before?", "In some projects you little shit!", False]
                ]],
                ["2D Games", [
                    ["Examples for games you created?", "CardGame, ModGame, NoNameGame", False]
                ]],
                ["Discord Bots", [
                    ["What is Discord?", "Discord is an app, where you can talk or write with other people just like an online meeting.", False],
                    ["What is a Discord bot?", """A discord bot is a program that connects to the discord server and remote controlls an account over the Java Discord API (JDA).<br>
                                                    This remotely controlled account can then perform actions to manage the users.""", False]
                ]]
             ]
    ],
    ["Web Development", [
                ["JavaScript", [
                    ["Examples", "Chart JS --> OnTimeLogger/TempLogger", False]
                ]],
                ["html", [
                    ["What is html?", "HTML is markup language, used to create the basic structure fo websites.", False]
                ]],
                ["css", [
                    ["What is css?", "CSS is used to define, how a HTML elemet should look.", False],
                    ["Interesting example", "without css: <span>TEST</span> <br> with css: <span style='color: red; border-style:solid; border-radius: 5px; background-color:orange;'>TEST</span>", False]
                ]],
                ["SQL", [
                    ["What is SQL?", "SQL is a database type that is very popular. You use databases to store user infomation like accounts and passwords.", False]
                ]]
              ]
    ],
    ["Microcontroller Programming", [
                ["Arduino", []],
                ["ESP32", []]
              ]
     ]
]


#Syntax: Name, onRequestAdress
serviceList = [["ModGame", "http://nonamenetwork.hopto.org:25568"], ["DemoServer", "http://nonamenetwork.hopto.org:187/"], ["ODIN", "http://nonamenetwork.hopto.org:25569/"]]


def buildDropdowns(item_list):
    outputHTML = ""
    for language_block in item_list:
        language_block_header = language_block[0]
        language_block_skills = language_block[1]

        outputHTML += f"""<p><u class="Uheader">{language_block_header}</u></p>"""

        for skill in language_block_skills:
            skill_block_header = skill[0]
            skill_block_faq = skill[1]
            effectclasses = "mousepointer hvr-grow"
            afterbr = "<br>"
            if len(skill_block_faq) == 0:
                effectclasses = ""
                afterbr = ""
            skill_opening_section_id = f"Section_{language_block_header}_{skill_block_header}".replace(' ', '').replace("?", "").replace(".", "").replace(",", "").replace("/", "")
            outputHTML += f"""
            <p data-toggle="collapse" data-target="#{skill_opening_section_id}" class="hideheader {effectclasses}"><u>{skill_block_header}</u></p>{afterbr}
            <div class="infoText collapse openSection" id="{skill_opening_section_id}">
            """

            for faq_block in skill_block_faq:
                faq_block_question = faq_block[0]
                faq_block_answer = faq_block[1]
                faq_block_show = faq_block[2]
                if len(skill_block_faq) == 1:
                    faq_block_show = True
                show_string = ""
                if faq_block_show:
                    show_string = "in"
                faq_opening_section_id = f"Section_{language_block_header}_{skill_block_header}_{faq_block_question}".replace(' ', '').replace("?", "").replace(".", "").replace(",", "").replace("/", "")
                outputHTML += f"""
                <p data-toggle="collapse" data-target="#{faq_opening_section_id}" class="hvr-grow mousepointer"><u>{faq_block_question}</u></p><br>
                <div id="{faq_opening_section_id}" class="collapse {show_string} answer">{faq_block_answer}<br></div>
                """

            outputHTML += "</div>"


    return outputHTML

#print("BuiltHTML: "+buildDropdowns(DROPDOWN_LIST))


def thread_requesting():
    while True:
        for item in serviceList:
            url = item[1]
            reachability_list[url] = website_on(url)
        #print(reachability_list)
        time.sleep(30)

state_on = "🍏online"
state_off = "🍎offline"


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
    return render_template("index.html", PY_ON_SERVICES=Markup(listServiceStates()), PY_EXPERIENCE_SECTION=Markup(buildDropdowns(DROPDOWN_LIST)))



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

