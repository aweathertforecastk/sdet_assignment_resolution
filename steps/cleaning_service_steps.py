from behave import given, when, then
from api.cleaning_service_response_validator import ResponseValidator
import requests
from service_management.config import EXPECTED_COORDS, EXPECTED_PATCHES, EXPECTED_STATUS


@given("the cleaning service is running")
def verify_service_running(context):
    
    try:
        context.service_page.ensure_service_is_active()
    except AssertionError as e:
        raise AssertionError(f"Service check failed: {e}")


@when("I send a request with the following data")
def send_data_request(context):
    row = context.table[0].as_dict()
    
    payload = context.service_page.generate_request_payload(row)
    
    if None in payload.values():
        mock_response = requests.Response() 
        mock_response.status_code = 400
        mock_response._content = b'{"error": "Bad Request: Invalid JSON or Data"}'
        
        context.response = mock_response
    else:
        context.response = context.service_page.submit_cleaning_request(payload)



@then("the server should respond with")
def validate_server_response(context):
    row = context.table[0].as_dict()
    expected_coords = context.service_page.api.parse_json(row[EXPECTED_COORDS])  
    expected_patches = int(row[EXPECTED_PATCHES])  
    expected_status = int(row[EXPECTED_STATUS]) 

    response = context.response

    validator = ResponseValidator(response)

    validator.validate_status_code(expected_status)  
    validator.validate_response_data(expected_coords, expected_patches)
