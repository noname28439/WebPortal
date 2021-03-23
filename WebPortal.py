NN_SETTINGS_NAME = "WebPortal"

from flask import Flask, Markup, request, session, redirect, render_template

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









@app.route("/", methods=["POST", "GET"])
def main():
    return render_template("index.html")



if __name__ == "__main__":
    port = 25565
    if SETTINGS_READ_PARAMETER("port") != None:
        port = int(SETTINGS_READ_PARAMETER("port"))
    app.run(debug=True, host="0.0.0.0", port=port, threaded=True)

