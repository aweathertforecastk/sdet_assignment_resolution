from features.steps.cleaning_service_api import CleaningServiceAPI


class CleaningServicePage:
    def __init__(self):
        self.api = CleaningServiceAPI()


    def ensure_service_is_active(self):
        return self.api.verify_service_is_running()


    def generate_request_payload(self, data):
        return {
            "roomSize": self.api.parse_json(data.get("roomSize")),
            "coords": self.api.parse_json(data.get("coords")),
            "patches": self.api.parse_json(data.get("patches")),
            "instructions": data.get("instructions"),
        }


    def submit_cleaning_request(self, payload):
        return self.api.send_request(payload)
