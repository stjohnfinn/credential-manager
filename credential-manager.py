#!/usr/bin/python

import os, sys, time, subprocess
from termcolor import cprint, colored

HOMEPATH = os.path.expanduser('~')
CRED_PATH = HOMEPATH + '/.user-credentials-cm'

def showHelp():
    cprint("Help: ", 'green')

def createCredentials(cmd):
    filepath = HOMEPATH + '/.user-credentials-cm/' + cmd[0]
    usernameCount = 0
    passwordCount = 0
    keyCount = 0
    emailCount = 0
    try:
        file = open(filepath, 'w')
    except FileNotFoundError:
        os.system('mkdir -p ~/.user-credentials-cm/')
        file = open(filepath, 'w')
    cprint('Created: ' + filepath, 'green')

    for c in cmd[1:]:
        if c == '-u':
            usernameCount += 1
        elif c == '-k':
            keyCount += 1
        elif c == '-p':
            passwordCount += 1
        elif c == '-e':
            emailCount += 1

    file.write(cmd[0] + '\n')

    if usernameCount > 0:
        for i in range(usernameCount):
            print(colored(f'Enter username {i + 1}: ', 'white'), end='')
            username = input()
            file.write('u ' + username + '\n')
    if passwordCount > 0:
        for i in range(passwordCount):
            print(colored(f'Enter password {i + 1}: ', 'white'), end='')
            password = input()
            file.write('p ' + password + '\n')
    if emailCount > 0:
        for i in range(emailCount):
            print(colored(f'Enter email {i + 1}: ', 'white'), end='')
            email = input()
            file.write('e ' + email + '\n')
    if keyCount > 0:
        for i in range(keyCount):
            print(colored(f'Enter key {i + 1}: ', 'white'), end='')
            key = input()
            file.write('k ' + key + '\n')

    file.close()

    cprint('Credential successfully created!', 'green')

def readCredentials(name):
    file = None
    try:
        file = open(f'{CRED_PATH}/{name}')
        cprint(f"{name} credentials:", 'yellow')
        data = file.read().split('\n')
        for index, line in enumerate(data):
            if line == '' or index == 0:
                continue
            if (line[0] == 'u'):
                out = line[2:]
                print(f'\n  Username: {out}')
            elif (line[0] == 'p'):
                out = line[2:]
                print(f'\n  Password: {out}')
            elif (line[0] == 'k'):
                out = line[2:]
                print(f'\n  Key: {out}')
            elif (line[0] == 'e'):
                out = line[2:]
                print(f'\n  Email: {out}')
        file.close()
        print(' ')
        return
    except FileNotFoundError:
        cprint("No credentials found.", 'red')
    except IsADirectoryError:
        cprint("Illegal whitespace exists in your command.", 'red')

def removeCredentials(name):
    try:
        result = os.remove(f'{CRED_PATH}/{name}')
        cprint(f'Removed {name} credentials.', 'green')
    except FileNotFoundError:
        cprint(f'No credentials found.', 'red')

def displayAllCredentials():
    dirContents = os.listdir(f'{CRED_PATH}')
    if len(dirContents) == 0:
        cprint('No credentials found.', 'yellow')
        return
    print('Listing credentials: ')
    [print('\n  ' + cred) for cred in dirContents]
    print(' ')

cprint('Welcome to Credential Manager!', 'magenta')

while True:
    print(colored(' > ', 'white'), end='')
    cmd = input()

    cmd = cmd.strip().split(' ')

    if cmd[0][0] == '$':
        cmd[0] = cmd[0].replace('$', '')
        syscmd = ' '.join(cmd)
        os.system(syscmd)
        continue

    quitCommands = [
        'exit',
        'q',
        'quit',
        'x',
        'kill'
    ]
    if cmd[0] in quitCommands:
        cprint('Goodbye!', 'magenta')
        sys.exit()

    helpCommands = [
        'help',
        'h',
        'assist',
        '-h',
        '--help'
    ]
    if cmd[0] in helpCommands:
        showHelp()
        continue

    clearCommands = [
        'clear',
        'cls',
        'clearscreen'
    ]
    if cmd[0] in clearCommands:
        os.system('clear')
        cprint('Welcome to Credential Manager!', 'magenta')
        continue

    createCommands = [
        'create',
        'c',
        'add',
        'make',
        'new'
    ]
    if cmd[0] in createCommands:
        try:
            createCredentials(cmd[1:])
        except IndexError:
            cprint('You must enter the name of a credential set.', 'red')
        continue

    readCommands = [
        'read',
        'r',
    ]
    if cmd[0] in readCommands:
        try:
            readCredentials(cmd[1])
        except IndexError:
            cprint('You must enter the name of a credential set.', 'red')
        continue

    removeCommands = [
        'remove',
        'rm',
    ]
    if cmd[0] in removeCommands:
        try:
            removeCredentials(cmd[1])
        except IndexError:
            cprint('You must enter the name of a credential set.', 'red')
        continue

    listCommands = [
        'list',
        'showall',
        'displayall',
        'display',
        'da',
        'sa'
    ]
    if cmd[0] in listCommands:
        displayAllCredentials()
        continue

    cprint(' ! invalid command ! ', 'red')
