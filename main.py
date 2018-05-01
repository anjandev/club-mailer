import argparse
import os
import datetime
import smtplib
from os import listdir
from os.path import isfile, join

EXIT_MSG = "Exiting. Remember to run daemon mode (with -d) to send your message."
WAITING_MSG_FOLDER = './waiting/'

def writeMsgToDisk(content):
    # NOTE: This function has a bug with filenames. Find a better way to choose file names
    onlyfiles = [f for f in listdir(WAITING_MSG_FOLDER) if isfile(join(WAITING_MSG_FOLDER, f))]
    newFileName = str(len(onlyfiles))

    with open(os.path.join(WAITING_MSG_FOLDER, newFileName + '.txt'), 'a') as new_mail:
        for line in content:
            new_mail.write(line)

    print(EXIT_MSG)

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
                    replacementsForLine.append(input("Value for blank #" + str(i) + "\n"))
                # https://pyformat.info/
                # Using * because https://stackoverflow.com/questions/26758341/python-3-using-tuples-in-str-format
                line = line.format(*tuple(replacementsForLine))
                print(line)
                content[contentIdx] = line

    print("Your message is:")
    for line in content:
        print(line)

    writeOrNo = input("Write to message? [Y/n]")

    while(writeOrNo != "Y" and writeOrNo != "n"):
        print("Please choose Y or n")
        writeOrNo = input("Write to message? [Y/n] ")

    if writeOrNo == "Y":
        # NOTE: Have to add error handling
        date_entry = input('Enter a date to send message in YYYY-MM-DD format\n')
        date_entry = date_entry + "\n"
        content = [date_entry] + content
        writeMsgToDisk(content)
    elif writeOrNo == "n":
        print(EXIT_MSG)

def prompt(prompt):
    return input(prompt).strip()

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


if __name__ == "__main__":
    print("Welcome to club mailer!")
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

