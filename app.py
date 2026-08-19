from flask import Flask, render_template
import os
import requests

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("webSOS.html")

@app.route("/sos", methods=["POST"])
def sos():
    print("🚨 SOS RECEIVED!")
    webhook_url = os.environ.get("POCKET_ALERT_WEBHOOK")

    try:
        response = requests.post(
            webhook_url,
            json={
                "level": "high" 
            },
            timeout=10  )
        print("Pocket Alert response:", response.status_code)
        print(response.text)

        return "SOS received!", 200

    except Exception as e:
        print("Pocket Alert error:", e)
        return "SOS received, but notification failed.", 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
