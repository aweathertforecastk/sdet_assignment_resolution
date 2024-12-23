import subprocess
from config import CONTAINER_NAME


commands = [
    f"docker stop {CONTAINER_NAME}",
    f"docker rm {CONTAINER_NAME}"]


def stop_and_delete_service():
    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")


stop_and_delete_service()
