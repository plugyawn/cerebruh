# I did not use the "from ... import *" structure because PyCharm doesn't show the available functions otherwise,
# and I wanted to know if I could improve the code further with functions that I didn't know about.
# I have heavily commented this code so that I can improve on it later when I forget basically everything about it


# IMPORT STATEMENTS
#
# Importing libraries essential for navigating around the screen, using the clipboard,
# manipulating keyboard presses, et cetera.
import pyautogui
import time
import keyboard
import pyperclip
# Importing libraries essential for webscraping. Here, I've used BS4, or BeautifulSoup4. I have had past experience
# webscraping wikipedia.org and old.reddit.com with this. I did not have the courage to attempt more complex libraries.
from requests import *
from bs4 import *
from re import *
# tkinter is a python library used for showing windows, message-boxes, et cetera. I used it to show the final window
# when the scraping is done.
from tkinter import messagebox
#####################################

# DEFINED FUNCTIONS

# Function for returning what is highlighted by the cursor
def copyHighlight():
    pyperclip.copy("") # in case nothing is highlighted, this line prevents duplicate entries
    # copying what is highlighted
    # stackoverflow suggests using the hotkey function, but for some reason that does not work
    pyautogui.hotkey('ctrl','c')
    time.sleep(0.01) # suggested by stackoverflow user [soundstripe]: ctrl + C is fast but sometimes programs runs faster
    pyautogui.click(pyautogui.position()) # dispels the highlighted text and indicates that the program has responded
    return pyperclip.paste() # returns what has been copied as a STRING

# Functions for scraping Wikipedia.com, using the library BeautifulSoup4, or BS4
# I chose Wikipedia.com for two reasons: one, it uses relatively simple code, and two, I have scraped it before.
def getLink(search):
    # the get function "gets" the HTML/XML/JavaScript code from the website. "html5lib" is a parser.
    # StackExchange recommended a parser named "lxml", but I couldn't get it to work. "html5lib" is an alternative.
    soup = BeautifulSoup(get("https://en.wikipedia.org/w/index.php?search="+search).content, "lxml")
    for link in soup.findAll("a") :  # a, from a href, seems to be the tag that identifies links in websites.
        # I figured this out from the documentation, but had to refer to stackexchange to fix a few bugs
        link_href = link.get('href') # extracts the actual link from within the <a></a> tag.
        link_rank = link.get('data-serp-pos') # I noticed that all search elements in search have this numbered tag
        # This how I identify search results from other links. If there is no rank, it is not a search result.
        if (link_rank)!=None: # findAll gets ALL links, but if the rank exists, it is a search result.
            if "wiki/" in link.get('href'): # there are some wiktionary links that pop in, but I needed the wikis only.
                return(link.get('href')) # returns the top search result of the input string.

# Summarizing the Wikipedia entry was hard for two reasons: there are disambiguation pages, and there are reference tags
# I had to read through https://en.wikipedia.org/wiki/Wikipedia:Advanced_source_searching to make this work.
# I used the Regular Expressions library, re, for separating the reference tags from the text.
def getSummary(link, index):
    print(link) # for reference; a link in the prompt helps to debug where the code went wrong and it is harmless.
    soup = BeautifulSoup(get(link).content,"lxml") # lxml is an efficient parser, I used html5lib before.
    # StackExchange suggested using 'lxml' instead of 'html5lib', because it apparently works better.
    # In my experience, they appeared about the same, although 'lxml' appeared a little faster. Not confirmed.
    return(sub('\[\d*?\]','',soup.find_all('p')[index].text)) # This statement used the RegularExpressions library
    # Going through the statement character by character - RegularExpressions takes a general expression as a wildcard,
    # and the sub function replaces it with something else, in this case, a blank character.
    # '\[' & '\]' are escaped square brackets. '*d' describes a digit, '?' indicates any number of the digit.

# Recursion based MessageBox
def PopUpWindow(response,index):
    if response == 1:
        index+=1
        response = messagebox.askyesno("Hello", getSummary("https://en.wikipedia.org" + getLink(search + " -disambiguation"), index))
        PopUpWindow(response, index)
    print("")

#####################################

#MAIN CODE
# The main code runs under a While(True) loop. I do not know if that is how all softwares work, but
# I know that is how videogames  run, in general. A predefined shortcut key can break the loop and exit the program.
#print("https://en.wikipedia.org/"+getLink("intitle:"+input("WHAT DO YOU WANT TO SEARCH FOR?    ")))
takingResponse = True
while(True):
    if takingResponse:
        print("Taking responses NOW.")
        takingResponse = False
    if keyboard.is_pressed('f3'):
        index = 1
        search = copyHighlight()
        summary=getSummary("https://en.wikipedia.org"+getLink(search+" -disambiguation"),index)
        print(summary)
        response = messagebox.askyesno("CEREBruh", summary)
        PopUpWindow(response, index)
        print("")
        takingResponse = True
        continue
    if keyboard.is_pressed('f2'):
        index = 1
        search = copyHighlight()
        summary=getSummary("https://en.wikipedia.org"+getLink(search+" -disambiguation"),index)
        print(summary)
        response = messagebox.askyesno("CEREBruh", summary)
        PopUpWindow(response, index)
        print("")
        takingResponse = True
        continue

    if keyboard.is_pressed('f6'):
        exit()
