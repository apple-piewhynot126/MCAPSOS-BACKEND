from flask import Flask, render_template, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)

# so we write notes using the hashtag!
sos_active = False
sos_time = None


@app.route("/")
def home():
    return render_template("webSOS.html")


@app.route("/sos", methods=["POST"])
def sos():
    global sos_active, sos_time

    print("🚨 SOS RECEIVED!")

    sos_active = True
    sos_time = datetime.now().strftime("%H:%M:%S")

    discord_url = os.environ.get("POCKEYWEB")

    try:
        response = requests.post(
            discord_url,
            json={
                "content": "🚨 **SOS ALERT!**\nThe emergency button has been pressed!"
            },
            timeout=10
        )

        print("Discord response:", response.status_code)
        print(response.text)

        if response.status_code == 204:
            return "SOS received!", 200
        else:
            return "SOS received, but Discord notification failed.", 500

    except Exception as e:
        print("Discord error:", e)
        return "SOS received, but Discord notification failed.", 500


@app.route("/status")
def status():
    return jsonify({
        "sos": sos_active,
        "time": sos_time
    })


@app.route("/reset", methods=["POST"])
def reset():
    global sos_active, sos_time

    sos_active = False
    sos_time = None

    print("SOS STATUS RESET")

    return "SOS reset!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
