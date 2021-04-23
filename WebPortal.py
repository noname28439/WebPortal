NN_SETTINGS_NAME = "WebPortal"

from flask import Flask, Markup, request, session, redirect, render_template
import requests
from threading import Thread
import time
import os
import json
from pathlib import Path

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
DROPDOWN_LIST = []
serviceList = []




with open(Path.joinpath(Path(__file__).parent.absolute(), "data.json"), "r", encoding="utf-8") as content_file:
    content = content_file.read().replace("\n", "")
    data = json.loads(content)
    DROPDOWN_LIST = data["DropdownList"]
    serviceList = data["Services"]


#Syntax: Name, onRequestAdress

def buildDropdowns(item_list):
    outputHTML = ""
    for language_block in item_list:
        language_block_header = language_block[0]
        language_block_skills = language_block[1]

        outputHTML += f"""<p><u class="Uheader">{language_block_header}</u></p>"""

        for skill in language_block_skills:
            skill_block_header = skill[0]
            skill_block_faq = skill[1]


            extraclasses = "noextras"
            #print(str(language_block_skills) + str(len(language_block_skills)) + "\n\n")

            if len(skill) == 3:
                extraclasses += " " + str(skill[2])


            effectclasses = "mousepointer hvr-grow"
            afterbr = "<br>"
            if len(skill_block_faq) == 0:
                effectclasses = ""
                afterbr = ""
            skill_opening_section_id = f"Section_{language_block_header}_{skill_block_header}".replace(' ', '').replace("?", "").replace(".", "").replace(",", "").replace("/", "")
            outputHTML += f"""
            <p data-toggle="collapse" data-target="#{skill_opening_section_id}" class="hideheader {effectclasses} {extraclasses}"><u>{skill_block_header}</u></p>{afterbr}
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

state_on = "🍏online"#✔
state_off = "🍎offline"#❌
state_loading = "⏱loading..."


def listServiceStates():
    toReturn = ""
    for item in serviceList:
        name = item[0]
        url = item[1]
        innerBuild = ""
        innerBuild += "<li>"
        innerBuild += f"<span class='hvr-shrink'><a href='{url}' class='ProjectName'>{name}</a></span><br>"
        msg = ""
        color = ""
        if url in reachability_list:
            if reachability_list[url]:
                msg = state_on
                color = "green"
            else:
                msg = state_off
                color = "red"
        else:
            msg = state_loading
            color = "grey"
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

    port = 25566
    if SETTINGS_READ_PARAMETER("port") != None:
        port = int(SETTINGS_READ_PARAMETER("port"))

    read_debug_mode = SETTINGS_READ_PARAMETER("debug")
    is_debug = True
    if read_debug_mode is not None:
        if read_debug_mode == "False":
            is_debug = False
        else:
            is_debug = True
    print(f"Red --> Debug: {is_debug} | port: {port}")
    app.run(debug=bool(is_debug), host="0.0.0.0", port=port, threaded=True)
