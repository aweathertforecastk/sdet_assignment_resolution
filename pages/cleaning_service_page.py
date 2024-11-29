from api.cleaning_service_api import CleaningServiceAPI
import json

class CleaningServicePage:
    """
    A class to interact with the cleaning service API, providing higher-level methods for ensuring service 
    availability, parsing input data, and submitting cleaning requests.

    This class acts as a wrapper for 'CleaningServiceAPI' and provides convenience methods for checking if 
    the cleaning service is running, parsing input data, and sending requests with the 
    given payloads.

    """

    def __init__(self):
        self.api = CleaningServiceAPI()


    def ensure_service_is_active(self):
        """
        Verifies if the cleaning service is active by calling the 'verify_service_is_running' method 
        from 'CleaningServiceAPI'.

        This method checks the availability of the cleaning service and raises an error if the service 
        is not running.

        """
        return self.api.verify_service_is_running()

    
    def parse(self,value):
        """
          Tries to convert a string value into a Python object if the string represents JSON data.
          If the string is valid JSON, it returns the parsed object (e.g., list, dict). If the string 
          is not valid JSON, it returns the string as-is.

        """
    
        if isinstance(value, str):
            try:
                return json.loads(value) 
            except json.JSONDecodeError:
               
                return value
        return value


    def submit_cleaning_request(self, payload):
        """
        Sends the generated cleaning request payload to the cleaning service via the 'send_request' method 
        from the 'CleaningServiceAPI' class.

        """

        return self.api.send_request(payload)

