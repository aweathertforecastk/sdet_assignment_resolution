import subprocess
import os
import shutil
import sys


def clear_allure_results():
    """Clear the allure-results folder to ensure fresh results."""
    if os.path.exists("allure-results"):
        print("Clearing old allure-results...")
        shutil.rmtree("allure-results")  # Remove the old allure-results folder
    os.makedirs("allure-results")  # Recreate the allure-results folder


def generate_allure_results():
    """Run behave tests and generate Allure results."""
    try:
        # Ensure allure-results folder exists (it will be recreated by clear_allure_results)
        clear_allure_results()  # Clear previous results

        print("Running Behave tests with Allure formatter...")
        result = subprocess.run([
            "behave",
            "-f", "allure_behave.formatter:AllureFormatter",
            "-o", "allure-results",
            "./features"
        ], capture_output=True, text=True)

        # Print output for debugging
        print("Behave Output:")
        print(result.stdout)

        if result.stderr:
            print("Behave Errors:")
            print(result.stderr)

        # Print the return code to check for failure
        print(f"Behave return code: {result.returncode}")

        # Allow report generation even if tests fail (return code != 0)
        if result.returncode != 0:
            print(f"Warning: Behave tests failed with return code {result.returncode}.")

        print("Allure results generated successfully.")

    except Exception as e:
        print(f"Error generating Allure results: {e}")
        sys.exit(1)


def serve_allure_report():
    """Serve the Allure report locally."""
    try:
        print("Serving Allure report locally...")
        subprocess.run(["allure", "serve", "allure-results"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error serving Allure report: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Allure CLI is not installed or not in PATH. Please install Allure and try again.")
        sys.exit(1)


# Directly call the functions
generate_allure_results()  # Generate the Allure results even if tests fail
serve_allure_report()
