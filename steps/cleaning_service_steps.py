from behave import given, when, then
from api.cleaning_service_helper import CleaningServiceHelper


helper = CleaningServiceHelper()

@given("the cleaning service is running")
def verify_service_running(context):
    helper.service_page.ensure_service_is_active()


@when("I send a request with the following data")
def send_data_request(context): 
    row = context.table[0].as_dict()  
    payload = helper.create_payload(row)
    context.response = helper.send_request(payload)


@then("the server should respond with")
def validate_server_response(context): 
    row = context.table[0].as_dict()  
    helper.validate_response(row)
    
