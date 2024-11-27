class ResponseValidator:
    def __init__(self, response):
        if isinstance(response, dict) and 'status_code' in response:
            self.is_mock_response = True
            self.response = response
        else:
            self.is_mock_response = False
            self.response = response


    def validate_status_code(self, expected_status):
        if self.is_mock_response:
            status_code = self.response.get('status_code', 500)  
        else:
            status_code = self.response.status_code  

        assert status_code == expected_status, (
            f"Expected status {expected_status}, got {status_code}"
        )


    def validate_response_data(self, expected_coords, expected_patches):
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
