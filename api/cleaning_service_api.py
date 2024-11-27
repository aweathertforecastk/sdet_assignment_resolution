import json
import requests
from service_management.config import BASE_URL


class CleaningServiceAPI:
    """
    A class to interact with the cleaning service API, providing methods for sending requests,
    parsing JSON data, and verifying the service status.

    """
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url


    def send_request(self, payload):
        """
        Sends a cleaning session request to the API with the provided payload.

        This method checks if the payload is valid. If invalid, a mock error response is returned.
        Otherwise, it sends the request to the API endpoint and returns the response.

        """

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
        """
        Validates the structure and content of the provided cleaning session payload.

        Checks for the presence and correct format of essential fields: 'roomSize', 'coords', 'patches', 
        and 'instructions'. 

        """

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
        """
        Sends a test request to check if the cleaning service API is up and running.

        The method sends a sample cleaning session request and returns the response from the service.

        """

        url = f"{self.base_url}/v1/cleaning-sessions"
        test_payload = {
            "roomSize": [5, 5],
            "coords": [1, 2],
            "patches": [[1, 0], [2, 2], [2, 3]],
            "instructions": "NNESEESWNWW"
        }
        return self.send_request(test_payload)
