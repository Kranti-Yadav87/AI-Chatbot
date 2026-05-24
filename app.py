from flask import Flask, render_template, request, jsonify
from chatbot import get_chatbot_response
from database import save_log

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get-response", methods=["POST"])
def bot_reply():
    payload = request.get_json(silent=True) or {}

    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid request payload."}), 400

    user_msg = payload.get("message")
    if not isinstance(user_msg, str) or not user_msg.strip():
        return jsonify({"error": "Please type a message."}), 400

    user_msg = user_msg.strip()

    try:
        bot = get_chatbot_response(user_msg)
    except Exception:
        return jsonify({"error": "Could not generate a response right now."}), 503

    try:
        save_log(user_msg, bot)
    except Exception:
        pass

    return jsonify({"response": bot})


if __name__ == "__main__":
    app.run(debug=True)