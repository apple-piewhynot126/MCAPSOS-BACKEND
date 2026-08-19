from flask import Flask, render_template, jsonify
import os
import requests
from datetime import datetime
import time

app = Flask(__name__)

#so we write using the hashtag!
sos_active = False
sos_time = None

last_sos_time = 0
SOS_COOLDOWN = 10


@app.route("/")
def home():
    return render_template("webSOS.html")

@app.route("/sos", methods=["POST"])
def sos():
    global sos_active, sos_time, last_sos_time

    print("🚨 SOS RECEIVED!")

    current_time = time.time()

    # Check whether we're still in the cooldown period
    if current_time - last_sos_time < SOS_COOLDOWN:
        print("⚠️ SOS ignored because cooldown is active.")

        sos_active = True

        return "SOS already active.", 200

    # Record this SOS
    last_sos_time = current_time
    sos_active = True
    sos_time = datetime.now().strftime("%H:%M:%S")

    discord_url = os.environ.get("POCKEYWEB")

    if not discord_url:
        print("❌ Discord webhook URL is missing!")
        return "SOS received, but Discord is not configured.", 500

    try:
        response = requests.post(
            discord_url,
            json={
                "content":
                "🚨 **SOS ALERT!**\n"
                "The emergency button has been pressed!"
            },
            timeout=10  )
        print("Discord response:", response.status_code)

        if response.status_code == 204:
            print("✅ Discord notification sent!")
            return "SOS received!", 200

        elif response.status_code == 429:
            print("⚠️ Discord rate limit reached.")

            try:
                retry_after = response.json().get("retry_after")
                print("⏳ Discord says retry after:", retry_after, "seconds")
            except Exception:
                print("Could not determine retry time.")

            return "SOS received, but Discord is rate limited.", 429

        else:
            print("❌ Discord returned:", response.text)
            return "SOS received, but Discord notification failed.", 500

    except requests.exceptions.RequestException as e:
        print("❌ Discord connection error:❌❌❌", e)
        return "SOS received, but Discord could not be reached. SO SADD", 500

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
