NN_SETTINGS_NAME = "WebPortal"

from flask import Flask, Markup, request, session, redirect, render_template
import requests
from threading import Thread
import time
import os
import json

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
    ["Java", [
                ["Socket Programming", [
                    ["What is socket programming?", "Socket programming means setting up an server behind a specific port on a server so that other socket can connect to it and transfer information over the internet.", False],
                    ["Where did you use socket programming before?", """I used Sockets for almost every project, that needs to communicate directly over the Internet. <br>
                    That means that all my online Games like CardGame, ModGame or NoNameGame are built with this method. 
                    Additionally i used this in some other projects like the <a href='https://github.com/noname28439/MinecraftRemoteController' class='textlink hvr-grow'>Minecraft Remote Controller Mod</a> 
                    or my <a href='https://github.com/noname28439/DeviceController' class='textlink hvr-grow'>Local IOT Server</a>.
                    """, False]
                ]],
                ["Graphical 2D Applications", [
                    ["Examples for 2D Apps you created?", """
                    <img style='height: 200px; float: right; margin-right: 10%;' src='/static/public/graphics/CardGame.PNG' title='CardGame' onclick="showFullScreen(this);" class='mousepointer'>
                    So of course all my Games are Graphical Applications. For example here is a picture of CardGame<br> 
                    I also built some Graphical Apps to for example display data. <br>
                    An example for kind of an app would be <a href='https://github.com/noname28439/File-Navigame' class='textlink hvr-grow'>File NaviGame</a>. """, False]
                ]],
                ["Online Games", [
                    ["What are online games?", """Online games are basically just 2D Games.<br> But the Content, that is shown in the game is syncronized over the internet. 
                    So you can play online with other people. """, False],
                    ["How much experience do you have with this topic?", """I have a lot of experience with the concept of syncronizing Games over the internet. 
                    But I just built three or four large online games, becuase they are always a lot of work.<br>
                    """, False],
                    ["Which online Games have you built before?", """
                    <p style='font-family: "Oswald";'><u>CardGame</u></p>
                    <p>
                    In CardGame you get Cards and then use them to damage your opponents. And finally knock them out, to that they can't do anything anymore. <br>
                    <img style='height: 150px; float: right; margin-right: 10%;' src='/static/public/graphics/CG_Stammbaum.png' onclick="showFullScreen(this);" class='mousepointer'>
                    But you can also use many special tactics in the game for example you can combind some cards to even stronger ones to deal more damage. 
                    And there are a bunch of special effects Cards that can be used to for example see or steal your opponents cards.
                    You can also work in teams and give Cards to a player or revive him if he is down. 
                    </p>
                    
                    <br>
                    <p style='font-family: "Oswald";'><u>ModGame</u></p>
                    <p>
                    Mod Game is a really unconventional game. Because it's basically just a Server. And every player builds his own client.<br>
                    That means the game can look very different from player to player, because its the users choice how to disply the information the Server provides him. <br>
                    <img style='height: 200px; float: right; margin-right: 10%;' src='/static/public/graphics/ModGame_0.png' title='My own testing client' onclick="showFullScreen(this);" class='mousepointer'>
                    And the Goal of the Game is to develop better stragegies and a better and faster reacing client thant the other players to defeat them in Combat. 
                    And often the players event dont 'play' themselves anymore and let the computer handle all the actions, because the computer is just faster.
                    Then they just give tactical commands to the computer. 
                    <img style='height: 200px; float: right; margin-right: 10%;' src='/static/public/graphics/ModGame_3.png' title='My own testing client' onclick="showFullScreen(this);" class='mousepointer'>
                    This Game also features a live <a href='http://nonamenetwork.hopto.org:25568/io_app' class='textlink hvr-grow'>Website</a>, on which you can see the scores and a live map of the Game. 
                    </p>
                    """, False]
                ], "openclickExample"],
                ["Minecraft Plugins", [
                    ["What is Minecraft?", """Minecraft is one of the most successful Games ever created. <br>You can find more information about in on 
                    <a href='https://www.google.de/search?q=minecraft&sxsrf=ALeKk01tfLTh44nJJm02n_LBBARcmTDJlg%3A1617894984060&source=hp&ei=SB5vYJLKAfKYjLsPs7qpmAY&iflsig=AINFCbYAAAAAYG8sWL6-RbNG_WMChlv0
                    O4jyh31a4vYL&oq=minecraft&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgjECcyBAgjECcyBwguELEDEEM6CAgAELEDEIMBOgQIABAKOgcIABAKEMsBOgUIABCxAzoECAAQQ1C-CFiuLGDKLmgAcAB4AIABTogBhQqSAQIyNpgBAKABAaoBB2
                    d3cy13aXo&sclient=gws-wiz&ved=0ahUKEwiSjrq--O7vAhVyDGMBHTNdCmMQ4dUDCAk&uact=5' class='textlink hvr-grow'>Google</a>
                    , in the unlikely case you haven't heard about it before. 
                    """, False],
                    ["What is a Minecraft Plugin?", "A Minecraft Plugin means a small java app, that is used to write scripts for Minecraft multiplayer servers.", False],
                    ["Which Minecraft Plugins have you built before? ", """I build a lot of Minecraft plugins, because i started programming with this topic. 
                    In the past i built some of my own versions with improvements of existing minigames like Bedwars. <br>
                    But in the last time i mainly focused on creating my own minigame ideas. For example <a href='https://github.com/noname28439/MinecraftFireWar' class='textlink hvr-grow'>FireFight</a>. 
                    """, False]
                ]],
                ["Discord Bots", [
                    ["What is Discord?", "Discord is an app, where you can talk or write with other people just like an online meeting.", False],
                    ["What is a Discord bot?", """A discord bot is a program that connects to the discord server and remote controlls an account over the Java Discord API (JDA).<br>
                    This remotely controlled account can then perform actions to manage the users.""", False]
                ]]
             ]
    ],["Pyton", [
                ["Flask WebServers", [
                    ["What is a WebServer?", "A WebServer is just a program that runs on a server and makes a website available to users.", False],
                    ["What is a Flask?", "Flask is a simple Python library used to create WebServers in Python.", False],
                    ["Where did you use PythonFlask WebServers before?", """Almost all of the websites I currently host are made with Python and Flask.<br><br>
                    For example Project like this Page, The FileStorageServer or the ODIN-Projectare completely made in Python and mostly with Flask.<br>
                    But you can find python flask also In a lot of my other Projects, like the Temperature Logger or the ModGame WebServer.
                    """, False]
                ]],
                ["Selenium", [
                    ["What is a Selenium?", "Selenium is a python library that can be used to automatically perform actions in a WebBrowser.", False],
                    ["What have you built with Selenium before?", """For example i built an Account manager for Instagram accounts, that automatically signs you in in an incognito tab on the press of a button. <br>
                    or a programm that can automatically send or read Whatsapp message and other things over Whatsapp Web. """, False]
                ]],
                ["Basic Python", [
                    ["What do you mean with basic Python?", "By basic python i mean python libraries that are included like requests, time, sys, threading...", False]
                ]]
              ]
     ],
    ["Web Development", [
                ["JavaScript", [
                    ["What is JavaScript?", "JavaScript is a programming language, that can be executed by browsers to modify the page.", False],
                    ["Where did you use JavaScript before?", """JavaScript is part of almost every webpage.
                    
                    For example its uesd to write the online and ofline text that you can see when you load the page. <br>
                    But JavaScript can also be used for much bigger projects. For example in <a href='https://github.com/noname28439/OntimeLogger2.0/blob/main/WebServer/static/scripts/chartScript.js' class='textlink hvr-grow'>showing charts</a>. 
                    <br>
                    <img style='height: 100px; margin-left: 50px; margin-top: 25px;' src='/static/public/graphics/Chart0.png' onclick="showFullScreen(this);" class='mousepointer'>
                    <img style='height: 100px; margin-left: 50px; margin-top: 25px;' src='/static/public/graphics/Chart1.png' onclick="showFullScreen(this);" class='mousepointer'>
                    
                    """, False],
                    ["Interesting example", "<button onclick='trigger_easteregg(true); if(this.innerText==\"Click me!\"){rewrite(this);}'>Click me!</button>", False]
                ]],
                ["html", [
                    ["What is html?", "HTML is markup language, used to create the basic structure of websites.", False]
                ]],
                ["css", [
                    ["What is css?", "CSS is used to define very precise, how a HTML elemet should look.", False],
                    ["Example", "without css: <span>TEST</span> <br> with css: <span style='color: red; border-style:solid; border-radius: 5px; background-color:orange;'>TEST</span>", False]
                ]],
                ["SQL", [
                    ["What is SQL?", "SQL is a very popular database type. You use databases to store user infomation like accounts and passwords.", False]
                ]]
              ]
    ],
    ["Microcontroller Programming", [
                ["Arduino", []],
                ["ESP32", []]
              ]
     ]
]

if os.path.exists("./text-config.json"):
    exec("DROPDOWN_LIST="+open("./text-config.json", "r").read())
    print("loaded DropdownList from external file [\"./text-config.json\"]")

#Syntax: Name, onRequestAdress
serviceList = [
    ["NWCKeys", "https://odin-project.hopto.org:25570/nwck/viewer/"],
    ["ModGame", "https://nonamenetwork.hopto.org:25572"],
    ["DemoServer", "http://nonamenetwork.hopto.org:187/"],
    ["ODIN", "https://odin-project.hopto.org:25570/"],
    ["DownloadServer", "http://nonamenetwork.hopto.org:34567/"],
    ["LCD Messanger", "http://nonamenetwork.hopto.org:25571/"]
]


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
