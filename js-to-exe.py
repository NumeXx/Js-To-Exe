# Coded By NumeX
# JS-TO-EXE

# Import Modulee
import os, time

# Lte's Goooo
print('#---------------------------------------#')
print('[/] JS-TO-EXE By NumeX')
print('[/] Github : https://github.com/NumeXx')
print('#---------------------------------------#\n')
print('[1] Install Package')
print('[2] Convert JS-TO-EXE')
pilih = input('\n[?] Select Your Choice : ')
if pilih == '1':
    os.system("npm install -g pkg")
    print('Success Install Package..')
    input('Enter any key for continue...')
    os.system('cls || clear')
    os.system('python js-to-exe.py')
elif pilih == '2':
    fl = input("[/] Enter your file name (EX - test.js) : ")
    print('Converting...')
    time.sleep(1)
    os.system(f'pkg {fl}')
    os.system('cls || clear')
    print("Success Converting...")
    input('Enter any key for close...')
else:
    print("Error Keyword...")
exit()
