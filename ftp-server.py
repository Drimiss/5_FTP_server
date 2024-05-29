import socket
import os
import shutil

current_dir = os.path.join(os.getcwd(), 'docs')

def pwd(commands):
    return current_dir

def ls(commands):
    try:
        return '; '.join(os.listdir(current_dir))
    except Exception as e:
        return str(e)

def mkdir(commands):
    if len(commands) < 2:
        return 'No directory name provided'
    try:
        os.mkdir(os.path.join(current_dir, commands[1]))
        return f"Directory {commands[1]} created"
    except Exception as e:
        return str(e)

def rmdir(commands):
    if len(commands) < 2:
        return 'No directory name provided'
    try:
        os.rmdir(os.path.join(current_dir, commands[1]))
        return f"Directory {commands[1]} removed"
    except Exception as e:
        return str(e)

def rmfile(commands):
    if len(commands) < 2:
        return 'No file name provided'
    try:
        os.remove(os.path.join(current_dir, commands[1]))
        return f"File {commands[1]} removed"
    except Exception as e:
        return str(e)

def rename(commands):
    if len(commands) < 3:
        return 'Usage: rename <old_name> <new_name>'
    try:
        os.rename(os.path.join(current_dir, commands[1]), os.path.join(current_dir, commands[2]))
        return f"Renamed {commands[1]} to {commands[2]}"
    except Exception as e:
        return str(e)

def touch(commands):
    if len(commands) < 2:
        return 'Usage: touch <filename>'
    try:
        with open(os.path.join(current_dir, commands[1]), 'w') as f:
            pass  # Просто создаем файл
        return f"File {commands[1]} created"
    except Exception as e:
        return str(e)

def cat(commands):
    if len(commands) < 2:
        return 'No file name provided'
    try:
        with open(os.path.join(current_dir, commands[1]), 'r') as f:
            return f.read()
    except Exception as e:
        return str(e)

def cd(commands):
    global current_dir
    if len(commands) < 2:
        return 'No directory specified'
    if commands[1] == '..':
        current_dir = os.path.dirname(current_dir)
    else:
        new_dir = os.path.join(current_dir, commands[1])
        if os.path.isdir(new_dir):
            current_dir = new_dir
        else:
            return f"Directory {commands[1]} does not exist"
    return f"Changed directory to {current_dir}"

def process(req):
    commands = req.split()
    command = commands[0]
    
    cmd_map = {
        'pwd': pwd,
        'ls': ls,
        'mkdir': mkdir,
        'rmdir': rmdir,
        'rmfile': rmfile,
        'rename': rename,
        'touch': touch,
        'cat': cat,
        'cd': cd,
        'exit': lambda commands: 'exit'
    }

    func = cmd_map.get(command, lambda commands: 'bad request')
    return func(commands)


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    print(f"Connected by {addr}")

    request = conn.recv(1024).decode()
    print(request)

    response = process(request)
    if response == 'exit':
        conn.send(response.encode())
        conn.close()
        break

    conn.send(response.encode())

sock.close()
