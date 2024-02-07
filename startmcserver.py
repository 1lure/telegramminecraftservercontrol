import subprocess


def start_minecraft_server():
    try:
        # Execute the command to start the Minecraft server within a detached screen session named 'minecraft'
        subprocess.run(['screen', '-dmS', 'minecraft', 'java', '-Xmx14G', '-Xms14G', '-jar', 'server.jar'])
        print("Minecraft server started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_minecraft_server()
