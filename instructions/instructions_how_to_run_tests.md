# Requirements:
- Docker v.18+
- Python v.3.6+
- Must run on Mac OS X or Linux (x86-64) 


# Download the repository at https://github.com/aweathertforecastk/sdet_assignment_resolution


# From the root of this repository, follow these steps:


# Create and activate a virtual environment:
 Ensure you have Python 3.6+ installed. You may optionally create and activate a virtual environment to isolate dependencies. 
 Use the following commands to create and activate a virtual environment:
- `python3 -m venv venv`
- `source venv/bin/activate`


# Install dependencies:
- `pip install -r requirements.txt`


# Building and running the service:
- `python3 service_management/build_and_run_service.py && sleep 30`


# Run tests and view results:
 Option 1: Run all tests and view results on the Allure web page:
- `python3 run_tests_and_view_results.py`

 Option 2: Run only positive test cases:
- `behave --tags=positive`

 Option 3: Run only negative test cases:
- `behave --tags=negative`


# Stop and remove the service:
- `python3 service_management/stop_and_delete_service.py `
