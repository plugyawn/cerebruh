# cerebruh
A Windows-based python application aimed at putting Wikipedia and the UrbanDictionary at the tip of your finger. One finger. Developed by Progyan Das.

# Platform Support

### Windows
Fully supported and tested. Updates will first come to Windows.

### Linux
Not tested, possibly broken. Will update after patching.

### MacOS
Absolutely not supported as of now. However, changing the hotkey for the copy function to correspond to MacOS should fix some issues.

# FAQs

### How do I run this?
Extract the .zip file to a directory of your choice and run ```cerebruh.py``` from the command-prompt.
Depending on how Python is configured on your system, this command might be ```py cerebruh.py``` once command-prompt is focused on the right directory.

### How do I install the libraries?
You'll need PIP. On Windows, if it hasn't been installed already with Python, ```python get-pip.py``` or ```py get-pip.py``` in the command-prompt could help.
Once PIP is installed, use ```pip install [libary]``` to install that library. You'll need to be connected to the internet.

### How do I use this program?
Once the program is running, highlight some text and press F2 to see how Urban Dictionary defines that word, or, press F9 to see how Wikipedia defines it. If you are on a laptop, some OEMs may require you to press the ```fn``` key along with F2 or F9. 


# Libraries and/or Modules required
  1. pyautogui
  2. time
  3. keyboard
  4. pyperclip
  5. requests
  6. bs4
  7. re
  8. tkinter
  9. lxml
  
  # List of known bugs

+ ### Wikipedia searches sometimes return blank message-boxes.
Some Wikipedia pages don't have text on the first index of the paragraph, and the program starts extracting for text from there, so it returns a blank message. Pressing YES to move on to the next paragraph works fine. 
 Can be potentially fixed by checking for ```None``` in the return statement for the ```getSummary()``` function.

+ ### tKinter Window goes out of focus after first search.
This seems to be an inherent problem with tKinter. Every time after the first search, the Message Box has to be opened back from the taskbar. As of now, I have not thought of a way to fix this.

+ ### End of file on Wikipedia.
It is possible to keep pressing YES and reach the end of a Wikipedia file, on which it will throw an error. 
 This can be easily fixed with a try:catch construct.
  
 # IIT Gandhinagar ES102 Course Project.
 ### Developed by Progyan Das.
 

  
