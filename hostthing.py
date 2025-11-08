import socket
import subprocess

# Set up socket communication
HOST = "localhost"  # Localhost
PORT = 17        # Port to connect to
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Connected to terminal display. Type commands below:")

while True:
    # Get user input
    command = input("> ")
    if command.lower() == "exit":
        break

    # Execute the command using subprocess
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout.strip() or result.stderr.strip() or "Command executed."
    except Exception as e:
        output = f"Error: {str(e)}"

    # Send the output to the terminal display
    client_socket.sendall(output.encode("utf-8"))

client_socket.close()