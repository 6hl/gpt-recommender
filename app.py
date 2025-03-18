import logging

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from consultant import Consultant

load_dotenv()

app = Flask(__name__)

consultant = Consultant("cfg/base.oai.yaml")


@app.route("/")
def ping():
    return "", 200


@app.route("/reset")
def reset():
    consultant.update_config(reset=True)
    return jsonify({"message": "Config reset"}), 200


@app.route("/config", methods=["POST"])
def update_config():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if data.get("config", False):
        # If config is provided, load it
        config = data.get("config")
        consultant.update_config(config)
        return jsonify({"message": "Config updated"}), 200
    return jsonify({"error": "No config provided"}), 400


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    if not data:
        data = {}

    try:
        response = consultant(
            data.get("query", None),
            skip_profile_recommendations=data.get(
                "skip_profile_recommendations", False
            ),
        )
        return jsonify(response.model_dump()), 200
    except Exception as e:
        logging.error(f"Error in recommendation: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    try:
        logging.info("Starting Flask app...")

        app.run(host="0.0.0.0", port=8080)
    except Exception as e:
        logging.error(e, exc_info=True)
