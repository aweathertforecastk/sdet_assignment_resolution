import json
import requests
from behave import given, when, then


def send_request(payload):
    url = "http://localhost:8080/v1/cleaning-sessions"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response


@given("the cleaning service is running")
def verify_service_running(context):
    url = "http://localhost:8080/health"
    try:
        requests.get(url)
    except requests.exceptions.RequestException as e:
        raise AssertionError(f"Error checking service status: {e}")


@when("I send a request with the following data")
def send_data_request(context):
    if hasattr(context, "table") and context.table:
        data_rows = [row.as_dict() for row in context.table]
        row = data_rows[0] 

        try:
            payload = {
                "roomSize": json.loads(row["room_size"]) if row["room_size"] else [],
                "coords": json.loads(row["coords"]) if row["coords"] else [],
                "patches": json.loads(row["patches"]) if row["patches"] else [],
                "instructions": row["instructions"] if row["instructions"] else ""
            }
        except json.JSONDecodeError as e:
            print(f"Error parsing input data: {e}")
            context.response = type('Response', (object,), {'status_code': 400, 'text': f"Error parsing input data: {e}"})
            return

        response = send_request(payload)
        context.response = response 

        actual_status = response.status_code

        if actual_status == 200:
            try:
                actual_response = response.json() 
                print("Success Response:", actual_response)
            except json.JSONDecodeError as e:
                raise AssertionError(f"Error parsing response as JSON: {e}")
        elif actual_status == 400:
            actual_message = response.text
            print(f"Bad Request Error: {actual_message}")
        else:
            actual_message = response.text if response.text else "No response content"
            print(f"Unexpected error! Status code: {actual_status}. Response: {actual_message}")
            

@then("the server should respond with")
def validate_server_response(context):
    if hasattr(context, "table") and context.table:
        expected_rows = [row.as_dict() for row in context.table]
        expected = expected_rows[0]

        expected_status = int(expected["expected_status"])
        expected_coords = json.loads(expected["expected_coords"]) if expected["expected_coords"] else []
        expected_patches = int(expected["expected_patches"]) if expected["expected_patches"] else 0

        actual_status = context.response.status_code

        if actual_status == expected_status:
            if actual_status == 200:
                try:
                    actual_response = context.response.json()
                    assert actual_response.get("coords") == expected_coords, (
                        f"Unexpected coordinates! Expected: {expected_coords}, Got: {actual_response.get('coords')}"
                    )
                    assert actual_response.get("patches") == expected_patches, (
                        f"Unexpected patches! Expected: {expected_patches}, Got: {actual_response.get('patches')}"
                    )
                except (json.JSONDecodeError, KeyError) as e:
                    raise AssertionError(f"Error parsing server response: {e}")
            elif actual_status == 400 or actual_status == 500:
                if context.response.text.strip():
                    print(f"Error response: {context.response.text}") 
                print(f"Error response, status: {actual_status}")
            else:
                print(f"Unexpected status code: {actual_status}. Response: {context.response.text}")
        else:
            raise AssertionError(f"Expected status code {expected_status}, but got {actual_status}")


@then('the test is tagged as {test_tag}')
def verify_test_tag(context, test_tag):
    print(f"Test is tagged as {test_tag}.")

