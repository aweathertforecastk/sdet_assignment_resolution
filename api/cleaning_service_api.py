import json
import requests
from service_management.config import BASE_URL, ROOM_SIZE, COORDS, PATCHES, INSTRUCTIONS, STATUS_CODE


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
                STATUS_CODE: 400,
                "error": "Bad Request",
                "message": "Missing or invalid data"
            }
            return mock_response 

        url = f"{self.base_url}/v1/cleaning-sessions"
        headers = {"Content-Type": "application/json"}
        return requests.post(url, json=payload, headers=headers)


    def parse_json(self, data):
        """
    Attempts to parse the provided data into a list or dictionary. If the data is a valid JSON string, 
    it is parsed and returned as the appropriate Python data type (list or dict). 

    If the data is already a list or dictionary, it is returned as is. If the data cannot be parsed 
    as JSON, appropriate error responses are returned indicating the failure.

        """
    
        if isinstance(data, (list, dict)): 
            return data

        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            return {
                STATUS_CODE: 400,
                "error": "Bad Request",
                "message": "Invalid JSON format",
                "details": str(e)
            }
        except (TypeError, NameError) as e:
            return {
                STATUS_CODE: 400,
                "error": "Bad Request",
                "message": "Invalid data type or name error",
                "details": str(e)
            }
      

    def is_invalid_payload(self, payload):
        """
         
    Validates the structure and content of the provided cleaning session payload.

    This function checks if the essential fields ('roomSize', 'coords', 'patches', and 'instructions') 
    in the payload are present and correctly formatted. It returns 'True' if any field is missing, 
    incorrectly formatted, or invalid. Otherwise, it returns 'False'.

        """

        if payload.get(ROOM_SIZE) is None or len(payload[ROOM_SIZE]) != 2 or payload.get(ROOM_SIZE) == [0, 0]:
            return True
        if payload.get(COORDS) is None or len(payload[COORDS]) != 2:
            return True
        if not isinstance(payload.get(PATCHES, []), list):
            return True
        instructions = payload.get(INSTRUCTIONS, "")
        valid_instructions = {"E", "W", "N", "S"}
    
        if not instructions or not isinstance(instructions, str):
            return True
    
        if any(char not in valid_instructions for char in instructions):
            return True
        return False


    def verify_service_is_running(self):
        """
        Sends a test request to check if the cleaning service API is up and running.

        The method sends a sample cleaning session request and returns the response from the service.

        """

        url = f"{self.base_url}/v1/cleaning-sessions"
        test_payload = {
            ROOM_SIZE: [5, 5],
            COORDS: [1, 2],
            PATCHES: [[1, 0], [2, 2], [2, 3]],
            INSTRUCTIONS: "NNESEESWNWW"
        }
        return self.send_request(test_payload)
