from flask import Flask, request

app = Flask(__name__)


@app.route("/sos", methods=["POST"])
def sos():
    print("🚨 SOS RECEIVED!")

    return "SOS received!", 200


@app.route("/")
def home():
    return "Miaesha Addun from 9-DARWIN, SJCSHS. Hello, world!"
    return "SOS backend is running! May God bless you."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
