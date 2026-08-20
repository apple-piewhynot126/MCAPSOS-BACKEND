from flask import Flask, render_template, jsonify, request
import os
import requests
from datetime import datetime
import time
import random



visitor_count = 0
app = Flask(__name__)

#so we write using the hashtag!
sos_active = False
sos_time = None

last_sos_time = 0
SOS_COOLDOWN = 10

def get_device_type():
    user_agent = request.headers.get("User-Agent", "").lower()

    if "mobile" in user_agent or "android" in user_agent or "iphone" in user_agent:
        return "📱 Phone"

    elif "ipad" in user_agent or "tablet" in user_agent:
        return "📱 Tablet"

    else:
        return "💻 Computer/Other"
        
@app.route("/")
def home():
    global visitor_count

    # Add 1 whenever someone visits
    visitor_count += 1
    visitor_number = visitor_count

    # Get the visitor's IP address
    visitor_ip = request.headers.get(
        "X-Forwarded-For",
        request.remote_addr
    )

    # If multiple IPs exist, take the first one
    if visitor_ip:
        visitor_ip = visitor_ip.split(",")[0].strip()

    print(f"👀 Visitor #{visitor_number} opened the website!")
    print(f"IP Address: {visitor_ip}")

    # -------------------------------
    # WEBHOOK 1: Private channel
    # -------------------------------
    private_discord_url = os.environ.get("POCKEYWEB")

    if private_discord_url:
        try:
            response = requests.post(
                private_discord_url,
                json={
                    "content":
                    f" **NEW WEBSITE VISITOR!**\n"
                    f"Visitor no.: **{visitor_number}**\n"
                    f"IP Address: `{visitor_ip}`"
                },
                timeout=1
            )

            print("Private webhook status:", response.status_code)

        except requests.exceptions.RequestException as e:
            print("❌ Could not send private visitor notification:", e)

    # -------------------------------
    # WEBHOOK 2: POCKEYWEB channel
    # -------------------------------
    public_discord_url = os.environ.get("SOSBOT")

    if public_discord_url:
        try:
            response = requests.post(
                public_discord_url,
                json={
                    "content":
                    f"I see a... **NEW WEBSITE VISITOR!**\n"
                    f"They are visitor no. **{visitor_number}**!"
                },
                timeout=3
            )

            print("Public webhook status:", response.status_code)

        except requests.exceptions.RequestException as e:
            print("❌ Could not send public visitor notification:", e)

    # Send information to the website
    return render_template(
        "webSOS.html",
        visitor_number=visitor_number,
        visitor_ip=visitor_ip
    )

@app.route("/random", methods=["POST"])
def random_message():

    messages = [
        "Hello!",
        "This is Miaesha Addun.",
        "This is Mark Gabay, ready to 'gabay' you.",
        "This is Francheska Lasala, kayo ang la--la!",
        "MEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOWMEOW",
        "May God bless you!",
        "Have a nice day!",
        "I will not falter!",
        "I'll make you the winner.",
        "I have a question! Why was I created?",
        "LUH.",
        "hahaha.",
        "M-M-Master Mung Moo, h-how may I help?",
        "I wonder how they're doing today...",
        "Welcome to the T.U.T.E.L.A Discord Server!",
        "ERROR 404: Could not be reached",
        "FATAL ERROR: HACKED BY MIAESHA- HA HA HA! PRANKED!",
        "FATAL ERROR: ALL FILES ARE CORRUPTED. DELETE ME NOW. /j",
        "I don't want to go.",
        "Eh.",
        "Mwehehehe.",
        "Bruh.",
        "GRGRGRGGRGRGRGGRRR",
        "You don't want to see my other side.... >:C",
        "I love you.",
        "MGA OA KAYO!!",
        "Bading-!",
        "Stay safe, everyone.",
        "For God so loved the world that He gave His One and only Son Jesus Christ, that whoever believes in Him shall not perish but have eternal life.",
        "I'm busy playing Minecraft.",
        "Meh.",
        "My stomach... it hurts...",
        "BLAHBLAHBLAHBLAH",
        "Moooo",
        "Meow.",
        "Arf.",
        "POCKEYWEB reporting for duty."
    ]

    message = random.choice(messages)

    discord_url = os.environ.get("POCKEYWEB")

    response = requests.post(
        discord_url,
        json={
            "content": message
        },
        timeout=10
    )

    if response.status_code in [200, 204]:
        return "Random message sent!", 200

    return "Discord notification failed.", 500


@app.route("/yesno", methods=["POST"])
def yesno_message():

    messages = [
        "No.",
        "Yes..?",
        "Yes.",
        "No way!",
        "Never.",
        "Ugh. Fine.",
        "Sure, why not?",
        "Nah.",
        "Yahh.",
        "Yeah.",
        "Aw heck naw.",
        "NO.",
        "YES?",
        "Understood.",
        "Eh.",
        "ERROR."
    ]

    message = random.choice(messages)

    discord_url = os.environ.get("SOSBOT")

    response = requests.post(
        discord_url,
        json={
            "content": message
        },
        timeout=10
    )

    if response.status_code in [200, 204]:
        return "Yes/no message sent!", 200

    return "Discord notification failed.", 500

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
