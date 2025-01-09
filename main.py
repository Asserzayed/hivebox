#!/usr/bin/env python3
'''Flask mini web-app made as part of DevOps self-study End-to-End Project HiveBox'''
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
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

# Load environent variables
load_dotenv()
SENSEBOX_IDS = os.getenv('SENSEBOX_IDS', '').split(',')
API_VERSION = os.getenv('API_VERSION', '0.0.0')

def status_assess(avg_temp):
    if avg_temp <= 10.0 :
        return 'Too Cold'
    elif avg_temp > 10.0 and avg_temp <= 36.0:
        return 'Good'
    else:
        return 'Too Hot'


def create_app(testing=False):
    '''Creating Flask app instance.'''
    app = Flask(__name__)

    # Initialize Prometheus metrics
    metrics = PrometheusMetrics(app)

    # API Base Endpoint referenced from OpenSenseMap Docs.
    EXTERNAL_API_BASE_ENDPOINT = "https://api.opensensemap.org/boxes/"

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

                # Accumulate readings
                results.append(temperature_info.value)
            return jsonify({"Average temperature": f"{sum(results)/len(results)}", "Status": f"{status_assess(sum(results)/len(results))}"}), 200
        
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
