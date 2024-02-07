import subprocess

def stop_minecraft_server():
    try:
        subprocess.run(['screen', '-S', 'minecraft', '-p', '0', '-X', 'stuff', 'stop\n'])
        print("Minecraft server stop command sent successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    stop_minecraft_server()