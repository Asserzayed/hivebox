#!/usr/bin/env python3

import argparse
from flask import Flask, jsonify
from jsonpath_ng.ext import parse
from datetime import datetime
import requests


app = Flask(__name__)

# Tool version
TOOL_VERSION = "1.0.0"
# API Base Endpoint referenced from OpenSenseMap Docs.
EXTERNAL_API_BASE_ENDPOINT = "https://api.opensensemap.org/boxes/"
# 3 Closely Selected SenseBoxes (as per rubric)
SENSEBOX_IDS = ['5fb7de317a70a5001c6af2da','65ccf440ece12100080f938b','64a6860b9ecd2b0007e82b26']


@app.route('/temperature', methods=['GET'])
def get_readings():  
    results = []
    try:
        for SENSEBOX_ID in SENSEBOX_IDS:
            api_endpoint = f"{EXTERNAL_API_BASE_ENDPOINT}/{SENSEBOX_ID}?format=json"
            response = requests.get(api_endpoint, timeout=100)

            # Raise exception for HTTP errors
            response.raise_for_status()

            # Parse response as JSON python object == dict == json.loads(response.text)
            data = response.json()
            # Expression tested on https://jsonpath.com/ on a response sample (get reading from all temp sensors)
            jsonpath_expression = parse('$.sensors[?(@.unit=="°C")].lastMeasurement')

            # Other way to match jsonpath_ng.ext.match('$.sensors[?(@.unit=="°C")].lastMeasurement', json_obj) #OR# matches = [match.value for match in jsonpath_expression.find(data)]
            for match in jsonpath_expression.find(data):
                last_measurment = match.value
                created_at = last_measurment.get('createdAt','')
                # get matches with up-to-date readings (discard non-working temperature sensors)
                if created_at:
                    created_at_fmt = created_at[:10]  #  the date portion (YYYY-MM-DD)
                    if created_at_fmt == datetime.now().strftime('%Y-%m-%d'):
                        results.append(match.value)  # Keep the match if it is from today to the result
                        # Console log for matched results
                        print(f'Matched lines {match.value}')
        print(results)
        return jsonify(results), 200
    
    except requests.RequestException as e:
        # Handle API request issues
        return jsonify({"error": "Failed to fetch data from external API", "details": str(e)}), 500

    except KeyError as e:
        # Handle unexpected data structure
        return jsonify({"error": f"Missing expected data in response: {str(e)}"}), 500

    except Exception as e:
        # Catch all other errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@app.route('/version', methods=['GET'])
def get_version():
    return jsonify({"version": f"{TOOL_VERSION}"})  

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(debug=True)
