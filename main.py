import argparse

def madlib(template):
    print("Creating new message from " + template + "\n")
    print("Club mailer will print out a line that has a blank\n")
    print("Type what you want the blank to be filled with and press ENTER\n")
    print("If a line has multiple blanks, type what you would like in the first\n")
    print("blank, press enter, type what you would like in the next blank  press enter, etc.\n")

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

        print(content)

if __name__ == "__main__":
    print("Welcome to club mailer!")
    parser = argparse.ArgumentParser(description='Automate club communication')
    parser.add_argument('-t', '--template', required=True, help='template you wish to use (see folder ./templates/)')

    args = parser.parse_args()

    madlib(args.template)
