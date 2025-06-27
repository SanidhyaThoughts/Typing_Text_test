import curses
from curses import wrapper
import time
import random

def startScreen(stdscr):
    stdscr.clear()

    #Print text at (y=5, x=10)  default(0,0)
    stdscr.addstr("SANIDHYA,Welcome to the speed Typing Test...!")
    stdscr.addstr("\nPress any key to begin.")
    stdscr.refresh()
    stdscr.getkey()


def displayText(stdscr,targetedText,currentText,wpm=0):
    stdscr.addstr(targetedText)
    stdscr.addstr(2,0,f"WPM:{wpm}")

    for i,char in enumerate(currentText):
        correct_char=targetedText[i]
        color=curses.color_pair(1)

        if char != correct_char:
            color=curses.color_pair(2)
        stdscr.addstr(0,i,char,color)


def loadtext():
    with open("tutorial.txt","r") as f:
        lines=f.readlines()   #lines is a list
        return random.choice(lines).strip()


def wpmTest(stdscr):
    targetedText=loadtext()
    currentText=[]
    wpm=0
    startTime=time.time()
    stdscr.nodelay(True)

    while True:
        timeElapsed=max(time.time() - startTime,1)
        wpm= round((len(currentText) / ( timeElapsed / 60 )) / 5)
        stdscr.clear()

        displayText(stdscr,targetedText,currentText,wpm)
        stdscr.refresh()

        if "".join(currentText)==targetedText:
            stdscr.nodelay(False)
            break

        try:
            key=stdscr.getkey()
        except:
            continue

        if ord(key)==27:
            break

        if key in("KEY_BACKSPACE","\b","\x7f"):
            currentText.pop()
        elif len(currentText) < len(targetedText):
            currentText.append(key)

# stdscr is main window object
def main(stdscr):
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)

    while True:
        startScreen(stdscr)
        wpmTest(stdscr)

        stdscr.addstr(4,0,"Test completed. Press ESC to exit or any other key to retry.")
        key=stdscr.getkey()
        
        if ord(key)==27:
            break


wrapper(main)
