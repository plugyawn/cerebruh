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

# Summarizing the UrbanDictionary entry was comparatively easier, but due to assignment pressure, I had to use my late days
# UrbanDictionary does not have <p> tags. Instead, it has <div> tags with a ['meaning'] attribute. The search URL is easy
# to generate, and the rest of the program follows much of the same pattern as the code above for scraping Wikipedia.
def summarizeUD(search): # Search is the returned variable from copyHighlight()
    respond = get("http://urbandictionary.com/define.php?term=" + search) # Broken into different lines for better reading
    soup = BeautifulSoup(respond.content, "lxml") # Gets the BeautifulSoup object, which contains the HTML code for the page
    string = "" # Initializing a string variable to later store the summary in it.
    returnNext = False # Some meanings don't have examples, and therefore two different meanings may pop up.
                       # this boolean prevents that from happening. Not very efficient, should improve.
    for tag in soup.find_all('div'): # In Wikipedia, I did this with the <p> tag. Here, I use the <div> tag.
        if tag.get('class') == ['meaning']: # The meaning tag identifies the definitions from useless links and other text.
            if not returnNext: # This prevents the function from returning multiple definitions.
                string += tag.text + "\n" # The '\n' is a line break, so the example is better formatted when added.
            else: # In statement above, tag.text returns the text from the <div> tag
                return(string) # If the example has already been added, this simply returns the string and does not add.
        if tag.get('class') == ['example']: # The example tag identifies an example of the word in the given meaning.
            string += "\nFor example, a sentence would be:\n" # Again, '\n' added for better formatting.
            string += tag.text # tag.text gives the text from within the <div> tag.
            return(string) # returns string if an example has been succesfully appended.

# Recursion based MessageBox
def PopUpWindow(response,index): # The response is the YES/NO at the end of the message-box. If Yes, this shows more information
    if response == 1: # 1 is YES, in this case
        index+=1 # The index is incremented so the next paragraph comes up
        # This is essentially identical to the original YES/NO prompt, except this ends in a recursive construct that
        # terminates when the user presses NO.
        response = messagebox.askyesno("Cerebruh [Wiki] "+search, getSummary("https://en.wikipedia.org" + getLink(search + " -disambiguation"), index))
        PopUpWindow(response, index) # Recursion call
    print("") # Was having some issues with this function, but a print function seemed to fix things. Will have to look into why.



#####################################

#MAIN CODE
# The main code runs under a While(True) loop. I do not know if that is how all softwares work, but
# I know that is how videogames  run, in general. A predefined shortcut key can break the loop and exit the program.
#print("https://en.wikipedia.org/"+getLink("intitle:"+input("WHAT DO YOU WANT TO SEARCH FOR?    ")))
takingResponse = True # This variable indicates whether the program is ready to take input, or not.
while(True): # An infinite Game-loop, inspired from PyGame. Keeps the program running.
    if takingResponse: # This chunk of code prints out a message whenever the program is ready to take an input.
        print("Taking responses NOW.")
        takingResponse = False # Keeps the program from spamming the same message over and over again.
    if keyboard.is_pressed('f9'): # Remappable. Change to any other key here, or use 'and' to make it a hotkey.
        entered = copyHighlight() # Assigns to the variable what has been highlighted on screen.
        print(entered) # Prints what has been entered. For convenience.
        string = summarizeUD(entered) # Summarizes the highlighted text
        print(string) # Summarizes, for convenience
        messagebox.showinfo("Cerebruh", string) # Shows MessageBox, with definition and example
        takingResponse = True # Indicates that program is ready for next input.
        continue # Loops back
    if keyboard.is_pressed('f2'): # Remappable, as before.
        index = 0 # The index identifies from which paragraph to start extracting. 0 is often unnecessary. 1 is the first line.
        search = copyHighlight() # Assigns to variable what is highlighted
        # The next line gets the summary. The '-disambiguation' makes it so that "Maybe you meant..." pages don't appear.
        # The - [minus] operator is for searching for those articles specifically that do not have that word in them.
        summary=getSummary("https://en.wikipedia.org"+getLink(search+" -disambiguation"),index) # Summarizes the text.
        print(summary) # For convenience. Prints the text in the console
        response = messagebox.askyesno("Cerebruh [Wiki] "+search, summary) # YES/NO to check if further info is wanted.
        PopUpWindow(response, index) # Recursive function, described above @ line85. Used to cycle through long pages.
        print("") # Blank print statement fixes a random bug. I don't exactly know why.
        takingResponse = True # Indicates readiness for next input
        continue # Loops back

    if keyboard.is_pressed('f6'): # Remappable
        exit() # Exits the program.
