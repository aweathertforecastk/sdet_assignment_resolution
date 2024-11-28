import requests
from service_management.config import COORDS, PATCHES, INSTRUCTIONS, STATUS_CODE


class ResponseValidator:
    """
    A class to validate the status code and response data of an HTTP response.

    """

    def __init__(self, response):
        self.response = response


    def validate_status_code(self, expected_status):
        """
        Validates that the HTTP response status code matches the expected status code.
        
        """
        if isinstance(self.response, dict):
            status_code = self.response.get(STATUS_CODE, 400)  

        elif isinstance(self.response, requests.Response):
            status_code = self.response.status_code
       
        assert status_code == expected_status, (
            f"Expected status {expected_status}, got {status_code}"
        )
 
    def is_valid_instructions(self, instructions, valid_instructions):
            """
            Validates that all characters in the instructions string are in the set of valid instructions.

            """
            return bool(instructions) and all(char in valid_instructions for char in instructions)

    def validate_response_data(self, expected_coords, expected_patches):
        """
        Validates the response data received from the cleaning service API.
           
        This method performs the following checks:
        1. Verifies that the `instructions` field contains only valid characters ('E', 'W', 'N', 'S').
        2. If the status code is 200, asserts that the `coords` and `patches` fields match the expected values.
        3. Differentiates between actual API responses and mock responses, handling both appropriately.
        4. Logs an error message and skips further validation if the status code is not 200.
                
        """
        valid_instructions = {"E", "W", "N", "S"}

        if isinstance(self.response, requests.Response):
            status_code = self.response.status_code
            actual_response = self.response.json()  
            instructions = actual_response.get(INSTRUCTIONS, "")

        elif isinstance(self.response, dict):  
            status_code = self.response.get(STATUS_CODE, 400)  
            actual_response = self.response  
            instructions = actual_response.get(INSTRUCTIONS, "")

        if not self.is_valid_instructions(instructions, valid_instructions):
                return {
                    STATUS_CODE: 400,
                    "error": "Bad Request",
                    "message": "Invalid instructions provided"
                }
        if status_code == 200:
            assert actual_response.get(COORDS) == expected_coords, (
                f"Expected coords {expected_coords}, got {actual_response.get(COORDS)}"
            )
            assert actual_response.get(PATCHES) == expected_patches, (
                f"Expected patches {expected_patches}, got {actual_response.get(PATCHES)}"
            )
        else:
            print(f"Error: Received status code {status_code}, cannot validate data")
