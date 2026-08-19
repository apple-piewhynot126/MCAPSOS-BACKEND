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

    # Turn the website's SOS status ON
    sos_active = True
    sos_time = datetime.now().strftime("%H:%M:%S")

    # Send notification to Pocket Alert
    webhook_url = os.environ.get("POCKEYWEB")

    try:
        response = requests.post(
            webhook_url,
            json={
                "level": "high"
            },
            timeout=10
        )

        print("Pocket Alert response:", response.status_code)
        print(response.text)

        return "SOS received!", 200
    except Exception as e:
        print("Pocket Alert error:", e)

        # The website still knows about the SOS
        # even if Pocket Alert fails.
        return "SOS received, but notification failed.", 500


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
