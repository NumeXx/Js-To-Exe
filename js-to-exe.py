from genericpath import isfile
import os
import sys
import wget
import pathlib
import time

def logo():
    print("""
[ ! ] Node JS To Exe
[ ! ] Tools By NumeX
[ ! ] Coded in Python3
    \n""")

def convert(file):
    pathnode = "C:/Program Files/nodejs/node.exe"
    if (os.path.isfile(pathnode)):
        print("[!] Installing Module...")
        time.sleep(1)
        os.system("cls || clear")
        os.system("npm i pkg -g")
        time.sleep(1)
        os.system("cls || clear")
        print("[!] Convert To Exe....")
        os.system(f"pkg {file}")
        time.sleep(1)
        os.system("cls || clear")
        logo()
        sys.exit("Closeee")
    
    else:
        print("[!] Please Install NodeJs. Downloading... [!]")
        time.sleep(1)
        down = wget.download("https://nodejs.org/dist/v14.17.6/node-v14.17.6-x64.msi")
        print(down)
        os.system("cls || clear")
        os.system("node-v14.17.6-x64.msi")
        time.sleep(1)
        os.system("cls || clear")
        os.system("npm i pkg -g")
        time.sleep(1)
        os.system("cls || clear")
        print("[!] Convert To Exe....")
        os.system(f"pkg {file}")
        time.sleep(1)
        os.system("cls || clear")
        logo()
        sys.exit("Closeee")


if __name__ == "__main__":
    logo()
    files = input("Enter Script Name [EX - text.js] : ")
    convert(files)
