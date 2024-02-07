import subprocess

def reload_minecraft_server():
    try:
        subprocess.run(['screen', '-S', 'minecraft', '-p', '0', '-X', 'stuff', 'reload\n'])
        print("Minecraft server reload command sent successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    reload_minecraft_server()