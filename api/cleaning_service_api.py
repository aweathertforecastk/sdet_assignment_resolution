import requests
from service_management.config import BASE_URL, ROOM_SIZE, COORDS, PATCHES, INSTRUCTIONS


class CleaningServiceAPI:
    """
    This class provides methods for sending cleaning requests to the API and verifying if the service is running.

    """
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url


    def send_request(self, payload):
       
        url = f"{self.base_url}/v1/cleaning-sessions"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        return response
 

    def verify_service_is_running(self):
       
        url = f"{self.base_url}/v1/cleaning-sessions"
        test_payload = {
            ROOM_SIZE: [5, 5],
            COORDS: [1, 2],
            PATCHES: [[1, 0], [2, 2], [2, 3]],
            INSTRUCTIONS: "NNESEESWNWW"
        }
        return self.send_request(test_payload)
