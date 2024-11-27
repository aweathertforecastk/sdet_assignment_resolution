import json
import requests
from service_management.config import BASE_URL


class CleaningServiceAPI:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url


    def send_request(self, payload):
        if self.is_invalid_payload(payload):
            mock_response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": "Missing or invalid data"
            }
            return mock_response 

        url = f"{self.base_url}/v1/cleaning-sessions"
        headers = {"Content-Type": "application/json"}
        return requests.post(url, json=payload, headers=headers)


    def parse_json(self, data):
        if not data:
            return []
        if isinstance(data, (list, dict)):
            return data
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return []


    def is_invalid_payload(self, payload):
        if not payload.get('roomSize') or len(payload['roomSize']) != 2:
            return True
        if not payload.get('coords') or len(payload['coords']) != 2:
            return True
        if not isinstance(payload.get('patches', []), list):
            return True
        if not payload.get('instructions') or not isinstance(payload['instructions'], str):
            return True
        return False


    def verify_service_is_running(self):
        url = f"{self.base_url}/v1/cleaning-sessions"
        test_payload = {
            "roomSize": [5, 5],
            "coords": [1, 2],
            "patches": [[1, 0], [2, 2], [2, 3]],
            "instructions": "NNESEESWNWW"
        }
        return self.send_request(test_payload)
