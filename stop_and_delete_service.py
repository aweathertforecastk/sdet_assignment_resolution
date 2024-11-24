import subprocess


commands = [
    "sudo docker stop pltsci-sdet-assignment",
    "sudo docker rm pltsci-sdet-assignment"
]


def execute_commands():
    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")

execute_commands()

