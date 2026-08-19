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

    if not discord_url:
        print("❌ Discord webhook URL is missing!")
        return "SOS received, but Discord is not configured.", 500

    try:
        response = requests.post(
            discord_url,
            json={
                "content": "🚨 **SOS ALERT!**\nThe emergency button has been pressed!"
            },
            timeout=10
        )

        print("Discord response:", response.status_code)

        if response.status_code == 204:
            print("✅ Discord notification sent! Yippee! ✅✅✅")
            return "SOS received!", 200

        elif response.status_code == 429:
            print("⚠️⚠️⚠️ Discord rate limit reached.")
            return "SOS received, but Discord is rate limited.", 429

        else:
            print("❌❌❌❌ Discord returned:", response.text)
            return "SOS received, but Discord notification failed. Awh so sad", 500

    except requests.exceptions.RequestException as e:
        print("❌ Discord connection error:❌❌❌", e)
        return "SOS received, but Discord could not be reached.", 500

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
    
@app.route("/discord-test")
def discord_test():
    try:
        response = requests.get(
            "https://discord.com",
            timeout=10
        )

        print("Discord homepage status:", response.status_code)

        return f"Discord reachable: {response.status_code}", 200

    except Exception as e:
        print("Discord connection error:", repr(e))
        return "Could not reach Discord.", 500

@app.route("/discord-test-webhook")
def discord_test_webhook():
    webhook_url = os.environ.get("https://discord.com/api/webhooks/1539635541803278416/ua99UwHH3dddDLKxSFD68c8uK1WijdH3shiS4OdRfW1mLiV73tx_4t4Z4u5irYefoaFe")

    if not webhook_url:
        return "Webhook URL missing", 500

    try:
        response = requests.post(
            webhook_url,
            json={
                "content": "🧪 Discord connection test!"
            },
            timeout=15
        )

        print("Webhook status:", response.status_code)
        print("Webhook response:", response.text)

        return f"Webhook returned: {response.status_code}", 200

    except Exception as e:
        print("Webhook error:", repr(e))
        return "Webhook connection failed.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
