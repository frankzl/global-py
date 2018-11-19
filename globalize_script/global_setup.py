#!/usr/bin/python3
import os
import stat
from subprocess import Popen, PIPE

def mkdir(DIR):
    if not os.path.exists(DIR):
        os.makedirs(DIR)

def rmdir(DIR):
    if os.path.exists(DIR):
        os.rmdir(DIR)

def chmod_x( filename ):
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


def make_executable(filename, python_version="python3"):

    path = is_available(python_version)

    if path is None:
        return False
    
    chmod_x(filename)

    SHEBANG = "#!"+path

    with open(filename, 'r') as original:
        data = original.read()

    if data[:2] != "#!":
        with open(filename, 'w') as modified:
            modified.write( SHEBANG + "\n" + data)
    else:
        print("file already executable: " + data.split('\n')[0])

    return True


def execute(command):
    commands = command.split(" ")
    p = Popen(commands, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    
    output, err = p.communicate( b"input data that is passed to subprocess stdin")
    return (output.decode("utf-8"))


def is_available(python_version):
    output = execute( "which " + python_version )
    path = output.split("\n")[0]
    if "/" in path:
        return path
    return None

if __name__ == '__main__':
    HOME = os.getenv("HOME")
    MY_GLOBAL = os.path.join( HOME, "pyglobal-bin" )
    make_executable("global_setup.py", "python3")
    mkdir(MY_GLOBAL)
    rmdir(MY_GLOBAL)
