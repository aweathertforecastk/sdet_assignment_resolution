from api.cleaning_service_api import CleaningServiceAPI


class CleaningServicePage:
    """
    A class to interact with the cleaning service API, providing higher-level methods for ensuring service 
    availability, generating request payloads, and submitting cleaning requests.

    This class acts as a wrapper for 'CleaningServiceAPI' and provides convenience methods for checking if 
    the cleaning service is running, creating cleaning session requests, and sending these requests.
    
    """

    def __init__(self):
        self.api = CleaningServiceAPI()


    def ensure_service_is_active(self):
        """
        Verifies if the cleaning service is active by calling the 'verify_service_is_running' method 
        from 'CleaningServiceAPI'

        """
        return self.api.verify_service_is_running()


    def generate_request_payload(self, data):
        """
        Generates the payload needed for a cleaning request based on the provided data.

        """
        return {
            "roomSize": self.api.parse_json(data.get("roomSize")),
            "coords": self.api.parse_json(data.get("coords")),
            "patches": self.api.parse_json(data.get("patches")),
            "instructions": data.get("instructions"),
        }


    def submit_cleaning_request(self, payload):
        """
        Sends the generated cleaning request payload to the cleaning service via the 'send_request' method 
        from the 'CleaningServiceAPI' class.

        """

        return self.api.send_request(payload)
