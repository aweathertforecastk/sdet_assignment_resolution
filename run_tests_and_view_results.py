import subprocess
import os
import shutil
import sys


class AllureReportManager:
    """
    A class for automating the process of generating and serving Allure reports
    from Behave test results.
    
    """
    def __init__(self, results_dir="allure-results", features_dir="./features"):
        self.results_dir = results_dir
        self.features_dir = features_dir

  
    def clear_allure_results(self):
        if os.path.exists(self.results_dir):
            shutil.rmtree(self.results_dir)
        os.makedirs(self.results_dir)

  
    def generate_allure_results(self):
        try:
            self.clear_allure_results()
            print("Running tests and generating Allure report...")

            subprocess.run([
                "behave",
                "-f", "allure_behave.formatter:AllureFormatter",
                "-o", self.results_dir,
                self.features_dir
            ], capture_output=True, text=True)

            print("Allure report generated successfully.")

        except Exception as e:
            print(f"Error generating Allure results: {e}")
            sys.exit(1)

  
    def serve_allure_report(self):
        try:
            subprocess.run(["allure", "serve", self.results_dir], check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error serving Allure report: {e}")
            sys.exit(1)

        except FileNotFoundError:
            print("Allure is not installed or not in the system's PATH. Please install Allure and try again.")
            sys.exit(1)

  
    def generate_and_serve_report(self):
        self.generate_allure_results()
        self.serve_allure_report()


allure_manager = AllureReportManager()
allure_manager.generate_and_serve_report()
