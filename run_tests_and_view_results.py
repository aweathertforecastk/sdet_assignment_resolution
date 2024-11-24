import subprocess
import os
import shutil
import sys


def clear_allure_results():
    if os.path.exists("allure-results"):
        print("Clearing old allure-results...")
        shutil.rmtree("allure-results")
    os.makedirs("allure-results")


def generate_allure_results():
    try:
        clear_allure_results()

        subprocess.run([
            "behave",
            "-f", "allure_behave.formatter:AllureFormatter",
            "-o", "allure-results",
            "./features"
        ], capture_output=True, text=True)

        print("Allure results generated successfully.")

    except Exception as e:
        print(f"Error generating Allure results: {e}")
        sys.exit(1)


def serve_allure_report():
    try:
        print("Serving Allure report locally...")
        subprocess.run(["allure", "serve", "allure-results"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error serving Allure report: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Allure CLI is not installed or not in PATH. Please install Allure and try again.")
        sys.exit(1)


generate_allure_results()
serve_allure_report()

