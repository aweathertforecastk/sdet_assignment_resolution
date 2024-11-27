class ResponseValidator:
    """
    A class to validate the status code and response data of an HTTP response.
    
    """

    def __init__(self, response):
        if isinstance(response, dict) and 'status_code' in response:
            self.is_mock_response = True
            self.response = response
        else:
            self.is_mock_response = False
            self.response = response


    def validate_status_code(self, expected_status):
        """
        Validates that the HTTP response status code matches the expected status code.

        This method checks the response's status code (from either a mock response or an actual response) 
        and compares it with the expected status code. If they do not match, an assertion error is raised.

        """
        if self.is_mock_response:
            status_code = self.response.get('status_code', 500)  
        else:
            status_code = self.response.status_code  

        assert status_code == expected_status, (
            f"Expected status {expected_status}, got {status_code}"
        )


    def validate_response_data(self, expected_coords, expected_patches):
        """
        Validates the response data by checking if the 'coords' and 'patches' match the expected values.

        This method is only executed if the response is not a mock response and the HTTP status code is 200. 
        It checks that the 'coords' and 'patches' values in the response match the expected values.

        """
        if self.is_mock_response:
            return

        if self.response.status_code == 200:
            actual_response = self.response.json()
            assert actual_response["coords"] == expected_coords, (
                f"Expected coords {expected_coords}, got {actual_response['coords']}"
            )
            assert actual_response["patches"] == expected_patches, (
                f"Expected patches {expected_patches}, got {actual_response['patches']}"
            )
