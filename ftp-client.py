import socket

def send_request(request):
    sock = socket.socket()
    sock.connect(('localhost', 6666))
    sock.send(request.encode())
    response = sock.recv(1024).decode()
    sock.close()
    return response

while True:
    command = input('>')
    if command == 'exit':
        send_request(command)
        print("Exiting...")
        break
    response = send_request(command)
    print(response)
