import subprocess

commands = [
    "sudo chmod +x service/run.sh",
    "sudo docker build -t pltsci-sdet-assignment service",
    "sudo docker run -d -p 8080:8080 --name pltsci-sdet-assignment pltsci-sdet-assignment"
]

def execute_commands():
    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}")

execute_commands()
