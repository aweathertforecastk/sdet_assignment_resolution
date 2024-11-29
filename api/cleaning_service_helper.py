from pages.cleaning_service_page import CleaningServicePage
from service_management.config import EXPECTED_COORDS, EXPECTED_PATCHES, EXPECTED_STATUS, ROOM_SIZE, PATCHES, INSTRUCTIONS, COORDS


class CleaningServiceHelper:
    def __init__(self):
        self.service_page = CleaningServicePage()
        self.response = None


    def create_payload(self, row):
        """
        Creates the request payload from the data provided in the scenario table.

        """
        payload = {
            ROOM_SIZE: self.service_page.parse(row.get(ROOM_SIZE)), 
            COORDS: self.service_page.parse(row.get(COORDS)),
            PATCHES: self.service_page.parse(row.get(PATCHES)),
            INSTRUCTIONS: row.get(INSTRUCTIONS),  
        }
        return payload


    def send_request(self, payload):
        """
        Sends the actual cleaning request and stores the response in the helper class.

        """
        self.response = self.service_page.submit_cleaning_request(payload)


    def validate_response(self, row):
        """
        Validates the service response by comparing it with expected values.

        """
        expected_coords = self.service_page.parse(row.get(EXPECTED_COORDS))
        expected_patches = self.service_page.parse(row.get(EXPECTED_PATCHES))
        expected_status = int(row.get(EXPECTED_STATUS))

        assert self.response.status_code == expected_status, (
            f"Expected status code {expected_status}, but got {self.response.status_code}"
        )

        if self.response.status_code == 200:
            response_json = self.response.json()

            if expected_coords:
                assert response_json.get("coords") == expected_coords, (
                    f"Expected coords {expected_coords}, but got {response_json.get('coords')}"
                )

            if expected_patches:
                assert response_json.get("patches") == expected_patches, (
                    f"Expected patches {expected_patches}, but got {response_json.get('patches')}"
                )

