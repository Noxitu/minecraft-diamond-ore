import os
import shutil
import subprocess
import time
import signal


# JAVA_PATH = R'C:\Program Files (x86)\Minecraft Launcher\runtime\jre-x64\bin\java'
JAVA_PATH = R'C:\Program Files (x86)\Minecraft Launcher\runtime\java-runtime-alpha\windows-x64\java-runtime-alpha\bin\java'
# SERVER_JAR = R'..\jars\minecraft_server.1.16.5.jar'
SERVER_JAR = R'..\jars\minecraft_server.1.17.jar'


def generate_world(*, seed):
    if os.path.exists('world_gen'):
        shutil.rmtree('world_gen')

    os.makedirs('world_gen')
    
    with open('world_gen/eula.txt', 'w') as fd:
        print('eula=true', file=fd)

    with open('world_gen/server.properties', 'w') as fd:
        print(f'level-seed={seed}', file=fd)

    process = subprocess.Popen(
        [JAVA_PATH, '-jar', SERVER_JAR, '-nogui'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        cwd='world_gen',
    )

    for line in process.stdout:
        line = line.decode().strip()
        print(' server log --', line)

        if line.endswith(')! For help, type "help"'):
            break
    
    process.stdin.write(b'stop\r\n')
    process.stdin.flush()

    try:
        process.wait(30)
        print('Server stopped.')

    except subprocess.TimeoutExpired:
        process.terminate()
        print('Server terminated.')


if __name__ == '__main__':
    generate_world(seed=1)
