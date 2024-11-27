import subprocess
from config import CONTAINER_NAME, IMAGE_NAME, SERVICE_PATH


commands = [
    f"sudo chmod +x {SERVICE_PATH}/run.sh",
    f"sudo docker build -t {IMAGE_NAME} {SERVICE_PATH}",
    f"sudo docker run -d -p 8080:8080 --name {CONTAINER_NAME} {IMAGE_NAME}"
]


def build_and_run_service():
    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")


build_and_run_service()
