#!/usr/bin/env python3
'''Flask mini web-app made as part of DevOps self-study End-to-End Project HiveBox'''
from config import API_VERSION
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify
from jsonpath_ng.ext import parse
from dateutil import parser as createdAt_parser
import requests

@dataclass
class TemperatureInfo:
    createdAt: str
    valid: bool
    value: float

    @classmethod
    def from_dict(cls, data: dict) -> "TemperatureInfo":
        # Expression tested on https://jsonpath.com/ on a response sample (get reading from all temp sensors)
        jsonpath_expression = parse('$.sensors[?(@.unit=="°C")].lastMeasurement')
        valid = False
        value = 0.0
        for match in jsonpath_expression.find(data):
            created_at = match.value.get('createdAt','')
            if created_at:
                # parse into datetime object for easy comparison
                created_at_fmt = createdAt_parser.isoparse(created_at)
                if created_at_fmt > (datetime.now(timezone.utc) - timedelta(hours=1)):
                    valid = True
                    value = float(match.value.get('value',''))
                    break
        return cls(
            createdAt=created_at,
            value=value,
            valid=valid
        )

def create_app(testing=False):
    '''Creating Flask app instance.'''
    app = Flask(__name__)

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
                
                # Extract temperature info
                temperature_info = TemperatureInfo.from_dict(data)

                # Calculate average
                results.append(temperature_info.value)
            return jsonify({"Average temperature": f"{sum(results)/len(results)}"}), 200
        
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
        return jsonify({"version": f"{API_VERSION}"})  

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
