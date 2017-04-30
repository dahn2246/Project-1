import os

def clearText(fileName):
    open(fileName, 'w').close()

def write(fileName, text):
    with open(fileName, "a") as myfile:
        myfile.write(str(text) + "\n")

def read(fileName):
    text = ''
    with open(fileName,'r') as myfile:
        for line in myfile:
            text += myfile.readline()
    return text