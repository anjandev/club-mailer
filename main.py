import argparse
import os
from os import listdir
from os.path import isfile, join

EXIT_MSG = "Exiting. Remember to run daemon mode (with -d) to send your message."
WAITING_MSG_FOLDER = './waiting/'

def writeMsgToDisk(content):
    onlyfiles = [f for f in listdir(WAITING_MSG_FOLDER) if isfile(join(WAITING_MSG_FOLDER, f))]
    newFileName = str(len(onlyfiles))

    with open(os.path.join(WAITING_MSG_FOLDER, newFileName + '.txt'), 'a') as new_mail:
        for line in content:
            new_mail.write(line)

    print(EXIT_MSG)

def madlib(template):
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

    # NOTE: Check this
    while(writeOrNo != "Y" and writeOrNo != "n"):
        print("Please choose Y or n")
        writeOrNo = input("Write to message? [Y/n]")

    if writeOrNo == "Y":
        writeMsgToDisk(content)
    elif writeOrNo == "n":
        print(EXIT_MSG)

if __name__ == "__main__":
    print("Welcome to club mailer!")
    parser = argparse.ArgumentParser(description='Automate club communication')
    parser.add_argument('-t', '--template', required=True, help='template you wish to use (see folder ./templates/)')

    args = parser.parse_args()

    madlib(args.template)
