#   < A simple program to create mail quickly from templates and mail at proper time>
#   Copyright (C) <2018>  <Anjandev Momi anjan@momi.ca>

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


import argparse
import os
import datetime
import smtplib
from shutil import copyfile
from sys import exit

from os import listdir
from os.path import isfile, join

from subprocess import Popen, PIPE
from os import path


EXIT_MSG = "Exiting. Remember to run daemon mode (with -d) to send your message."
WAITING_MSG_FOLDER = './waiting/'

def writeMsgToDisk(content):
    # NOTE: This function has a bug with filenames. Find a better way to choose file names
    onlyfiles = [f for f in listdir(WAITING_MSG_FOLDER) if isfile(join(WAITING_MSG_FOLDER, f))]
    newFileName = str(len(onlyfiles))

    filePath =  os.path.join(WAITING_MSG_FOLDER, newFileName + '.txt')

    with open(filePath, 'a') as new_mail:
        for line in content:
            new_mail.write(line)

    return filePath

def madlib(template):
    # NOTE: add support for multiple events in one email
    print("Creating new message from " + template)
    print("Club mailer will print out a line that has a blank")
    print("Type what you want the blank to be filled with and press ENTER")
    print("If a line has multiple blanks, type what you would like in the first")
    print("blank, press enter, type what you would like in the next blank  press enter, etc.")

    PLACE_HOLDER = "{}"

    with open('./templates/' + template) as f:
        content = f.readlines()
        for contentIdx, line in enumerate(content):
            if PLACE_HOLDER in line:
                print(line)
                blanks = line.count(PLACE_HOLDER)
                replacementsForLine = []
                for i in range(0, blanks):
                    replacementsForLine.append(raw_input("Value for blank #" + str(i) + "\n"))
                # https://pyformat.info/
                # Using * because https://stackoverflow.com/questions/26758341/python-3-using-tuples-in-str-format
                line = line.format(*tuple(replacementsForLine))
                print(line)
                content[contentIdx] = line

    print("Your message is:")
    for line in content:
        print(line)

    writeOrNo = raw_input("Write to message? [Y/n]")

    while(writeOrNo != "Y" and writeOrNo != "n"):
        print("Please choose Y or n")
        writeOrNo = raw_input("Write to message? [Y/n] ")

    if writeOrNo == "Y":
        # NOTE: Have to add error handling
        date_entry = raw_input('Enter a date to send message in YYYY-MM-DD format\n')
        date_entry = date_entry + "\n"
        content = [date_entry] + content
        filePath = writeMsgToDisk(content)
        websiteSend(filePath, date_entry)
    elif writeOrNo == "n":
        print(EXIT_MSG)

def prompt(prompt):
    return raw_input(prompt).strip()

def sendmail(content):
    # NOTE: Put from and to into a conf file
    fromaddr = prompt("From: ")
    toaddrs  = prompt("To: ").split()
    msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (fromaddr, ", ".join(toaddrs)))

    for i in range(1, len(content)):
        msg = msg + content[i]

    server = smtplib.SMTP('mailgate.sfu.ca', 587)
    server.starttls()
    # NOTE: put password in a config file
    server.login(fromaddr, password)
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


def daemon():
    print("Running Daemon Mode")
    while True:
        onlyfiles = [f for f in listdir(WAITING_MSG_FOLDER) if isfile(join(WAITING_MSG_FOLDER, f))]
        newFileName = str(len(onlyfiles))

        for i in range(0, len(onlyfiles)):
            with open(os.path.join(WAITING_MSG_FOLDER, str(i) + '.txt'), 'r') as send_mail:
                content = send_mail.readlines()
                date = content[0]
                year, month, day = map(int, date.split('-'))
                date1 = datetime.datetime(year, month, day)
                print("Sending Message")
                if datetime.datetime.now() > date1:
                    sendmail(content)
                    #NOTE: add deleting email after sending


def websiteSend(postFilePath, postDate):
    WEBSITE_POSTS_PATH = './msess.github.io/_posts/'

    postTitle = raw_input("Enter post title")

    fileName = postDate + postTitle

    try:
        copyfile(postFilePath, os.path.join(WEBSITE_POSTS_PATH, fileName))
    except IOError as e:
        print("Unable to copy file. %s" % e)
        exit(1)
    except:
        print("Unexpected error:", sys.exc_info())
        exit(1)

    GIT_PATH = '/usr/bin/git'
    git_command = [GIT_PATH, 'status']
    repository  = path.dirname(WEBSITE_POSTS_PATH)

    git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
    (git_status, error) = git_query.communicate()

    if git_query.poll() == 0:
        git_command = [GIT_PATH, 'add', '--all']
        git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        #git_command = [GIT_PATH, 'commit', '-m', 'Added: fileName']
        #git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)
        #git_command = [GIT_PATH, 'push', 'origin', 'master']
        #git_query = Popen(git_command, cwd=repository, stdout=PIPE, stderr=PIPE)

if __name__ == "__main__":
    print("<club mailer>  Copyright (C) <2018>  <Anjandev Momi>")
    print("This program comes with ABSOLUTELY NO WARRANTY; for details see the `LICENSE` file.")
    print("This is free software, and you are welcome to redistribute it")
    print("under certain conditions; see the `LICENSE' file for details.")

    parser = argparse.ArgumentParser(description='Automate club communication')
    parser.add_argument('-t', '--template', help='template you wish to use (see folder ./templates/)')
    parser.add_argument('-d', '--daemon', action='store_true', help='run in daemon mode to send messages in ./waiting at proper time', default=False)

    args = parser.parse_args()

    if args.template is not None:
        madlib(args.template)
    elif args.daemon is True:
        daemon()
    else:
        print("Please choose Daemon mode (-d) or compose a new message (-t)")

