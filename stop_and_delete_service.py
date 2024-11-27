import subprocess
from features.config import CONTAINER_NAME




# Commands to stop and remove the container
commands = [
    f"sudo docker stop {CONTAINER_NAME}",
    f"sudo docker rm {CONTAINER_NAME}"]

def stop_and_delete_service():
    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")

stop_and_delete_service()