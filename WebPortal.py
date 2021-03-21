NN_SETTINGS_NAME = "WebPortal"

from flask import Flask, Markup, request, session, redirect

def SETTINGS_READ_PARAMETER(key):
    PATH = '/home/pi/settings/settings'
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


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def main():
    return Markup("<h1>Work in progress...</h1>")



if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(SETTINGS_READ_PARAMETER("port")), threaded=True)

