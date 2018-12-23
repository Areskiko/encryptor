#!/usr/bin/env python

__author__ = "Stefan Mack"
__copyright__ = "None"
__credits__ = ["Stefan Mack, Torbjørn Wiik, Alexander Bjerga"]
__license__ = "None"
__version__ = "0"
__maintainer__ = "Stefan Mack"
__email__ = "stefan_mack@hotmail.com"
__status__ = "Development"

#Requires Kivy

#Import standard libraries
import os

#Import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

class EnigmaScreen(Screen):
    def __init__(self, bColor, **kwargs):
        """Initializes the screen and gets the standard path to the user."""
        super(EnigmaScreen, self).__init__(**kwargs)
        self.boxL = BoxLayout(orientation = 'vertical', size_hint=(1, 1))
        self.grid1 = GridLayout(cols=2, rows=5, size_hint = (1, 0.6))
        self.bind(on_enter=self.re_size)
        self.bind(on_leave=self.re_size)

        #Getting the path to user/documents
        try:
            x = os.getlogin()
            y = 'C:\\Users\\' + str(x) + '\\'
        except:
            y = ''

        self.grid1.add_widget(Label(text = "File placement"))
        self.place = TextInput(text=str(y))
        self.grid1.add_widget(self.place)
        

        self.grid1.add_widget(Label(text = "File name"))
        self.fName = TextInput()
        self.grid1.add_widget(self.fName)

        self.grid1.add_widget(Label(text = "Password"))
        self.password = TextInput()
        self.grid1.add_widget(self.password)

        self.grid1.add_widget(Label(text = "DeKey One"))
        self.DeKey1 = TextInput()
        self.grid1.add_widget(self.DeKey1)

        self.grid1.add_widget(Label(text = "DeKey Two"))
        self.DeKey2 = TextInput()
        self.grid1.add_widget(self.DeKey2)

        self.grid2 = GridLayout(cols = 2, rows = 1, size_hint = (1, 0.3))
        self.enc = Button(text = "Encrypt", background_color = bColor)
        self.enc.bind(on_press=self.encrypt)
        self.grid2.add_widget(self.enc)
        
        self.dec = Button(text="Decrypt", background_color = bColor)
        self.dec.bind(on_press=self.decrypt)
        self.grid2.add_widget(self.dec)

        self.boxL.add_widget(self.grid1)
        self.boxL.add_widget(self.grid2)
        self.backbtn = Button(text='Back', size_hint=(1,0.2), background_color = bColor)
        self.backbtn.bind(on_press=self.back)
        self.boxL.add_widget(self.backbtn)
        self.add_widget(self.boxL)
        
    def re_size(self, instance, *args):
        """Empty function to be re-purposed once imported."""
        pass

    def back(self, instance, *args):
        """Empty function to be re-purposed once imported."""
        pass

    def parseFile(self):
        """Parses given file and puts the words in lists."""
        #Setting up the path to the file
        Directory = self.place.text
        Directory.replace("\\", "\\\\")
        file = str(self.fName.text) + ".txt"
        file.replace("\\", "\\\\")
        fFile = Directory + "\\" + file

        wordsInLine = []
        LinesInFile = []

        #Parses and catalogs the words
        with open(fFile, mode="r") as f:
            word = ""
            for line in f:
                for char in line:
                    if char == "\n" or char == " " or char == "," or char == "." or char == "!" or char == "?":
                        wordsInLine.append(word)
                        word = ""
                        wordsInLine.append(char)
                    else:
                        word = word + char
                LinesInFile.append(wordsInLine)
                wordsInLine = []

        #Return the list of lists of words
        return LinesInFile

    def translation(self, mode):
        """Sets up a trantab with a custom alphabet."""
        normAlpha = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890"
        tempAlpha = normAlpha
        for i in range(len(self.password.text)):
            tempAlpha = tempAlpha.replace(self.password.text[i], "")
        spesAlpha = self.password.text + tempAlpha

        #Desciding how the alphabets are being set up
        if mode == "encrypt":
            trantab = str.maketrans(normAlpha, spesAlpha)
        elif mode == "decrypt":
            trantab = str.maketrans(spesAlpha, normAlpha)
        return trantab

    def writeToFile(self, blist, mode):
        """Takes words from lists inside of lists and writes them to a specified file."""
        #Setting up target file
        Directory = self.place.text
        Directory.replace("\\", "\\\\")
        file = self.fName.text + ".txt"
        if mode == "encrypt":
            fFile = Directory + "\\enc_" + file
        elif mode == "decrypt":
            fFile = Directory + "\\dec_" + file

        #Writing the words to the target file
        with open(fFile, mode= "w") as f:
            for slist in blist:
                for word in slist:
                    f.write(word)
            f.close

    def encrypt(self, instance):
        """Parses a target file, converts the information and writes it to a new file."""
        try:
            #Parsing file and gathering keywords to use for the encryption
            BigList = self.parseFile()
            CompletedList =  []
            DeKey1t = str(self.DeKey1.text)
            DeKey2t = str(self.DeKey2.text)

            #Getting the number that marks the half of each keyword
            h1 = int(len(DeKey1t)/2)
            h2 = int(len(DeKey2t)/2)
            
            TempList = []
            #Encryption process
            for word in BigList:
                #Encrypting
                if word == "\n" or word == " " or word == "," or word == "." or word == "!" or word == "?":
                    pass
                elif len(word) == 1:
                    word = DeKey1t[0:2] + word + DeKey2t[0:2]
                elif len(word) == 2:
                    word = word[0] + DeKey2t[0:3] + DeKey1t[0:3] + word[1]
                elif len(word) == 3:
                    word = DeKey2t[:h2] + word[2] + DeKey1t[:h1] + word[0] + DeKey2t[h2:] + word[1] + DeKey1t[h1:]
                elif len(word) == 4:
                    word = DeKey1t[h1:] + word[0:2] + DeKey2t[h2:] + word[2:3] + DeKey1t[:h1] + DeKey2t[:h2] + word[3]
                elif len(word) == 5:
                    word = word[3] + DeKey1t[:h1] + word[0:3] + DeKey2t[h2:] + word[4]
                elif len(word) == 6:
                    word = word[3] + DeKey1t[h1:] + word[0:3] + DeKey2t[:h2] + word[4:]
                elif len(word) == 7:
                    word = DeKey2t[h2:] + word[4:5] + DeKey1t[h1:] + word[5:] + word[3] + DeKey1t[:h1] + word[0:3] + DeKey2t[:h2]
                elif 11 > len(word) > 7:
                    word = DeKey1t[:h1] + word[:2] + DeKey1t[:h1] + word[2:4] + DeKey2t[h2:] + word[4:6] + DeKey1t[:h1] + word[6:7] + DeKey2t[:h2] + word[7:9] + DeKey1t[h1:] + word[9:]
                elif len(word) > 11:
                    word = DeKey1t[:h1] + word[:2] + DeKey1t[:h1] + word[2:4] + DeKey2t[h2:] + word[4:6] + DeKey1t[:h1] + word[6:7] + DeKey2t[:h2] + word[7:9] + DeKey1t[h1:] + word[9:12] +  DeKey2t[h2:] + word[12:]
                #Translation
                trantab = self.translation("encrypt", password)
                word = word.translate(trantab)
                TempList.append(word)
            CompletedList.append(TempList)
            #Writing to file
            self.writeToFile(CompletedList, "encrypt")
        except:
            #Exception warning
            popup = Popup(title='Uh Oh',
            content=Label(text='One or more inputs are invalid!'),
            size_hint=(None, None), size=(390, 400))
            popup.open()

    def decrypt(self, instance):
        """Parses a target file, converts the information and writes it to a new file."""
        try:
            #Parsing file and gathering keywords to use for the encryption
            BigList = self.parseFile()
            CompletedList = []
            DeKey1t = str(self.DeKey1.text)
            DeKey2t = str(self.DeKey2.text)

            #Getting the number that marks the half of each keyword
            h1 = int(len(DeKey1t)/2)
            h2 = int(len(DeKey2t)/2)

            #Encryption process
            TempList = []
            for word in BigList:
                trantab = self.translation("decrypt", password)
                word = word.translate(trantab)
                #Decrypting
                if word == "\n" or word == " " or word == "," or word == "." or word == "!" or word == "?":
                    pass
                elif len(word) == 1 + len(DeKey1t[0:2]) + len(DeKey2t[0:2]):
                    word = word.replace(DeKey1t[0:2], "")
                    word = word.replace(DeKey2t[0:2], "")
                elif len(word) == 2 + len(DeKey1t[0:2]) + len(DeKey2t[0:2]):
                    word = word.replace(DeKey1t[0:2], "")
                    word = word.replace(DeKey2t[0:2], "")
                    word = word
                elif len(word) == 2 + len(DeKey1t[0:3]) + len(DeKey2t[0:3]):
                    word = word.replace(DeKey2t[0:3], "")
                    word = word.replace(DeKey1t[0:3], "")
                    word = word[0] + word[1]
                elif len(word) == 3 + len(DeKey1t) + len(DeKey2t):
                    word = word.replace(DeKey1t[:h1], "")
                    word = word.replace(DeKey2t[:h2], "")
                    word = word.replace(DeKey1t[h1:], "")
                    word = word.replace(DeKey2t[h2:], "")
                    word = word[1] + word[2] + word[0]
                elif len(word) == 4 + len(DeKey1t) + len(DeKey2t):
                    word = word.replace(DeKey1t[:h1], "")
                    word = word.replace(DeKey1t[h1:], "")
                    word = word.replace(DeKey2t[:h2], "")
                    word = word.replace(DeKey2t[h2:], "")
                elif len(word) == 5 + len(DeKey1t[:h1]) + len(DeKey2t[h2:]):
                    word = word.replace(DeKey1t[:h1], "")
                    word = word.replace(DeKey2t[h2:], "")
                    word = word[1:4] + word[0] + word[4]
                elif len(word) == 6 + len(DeKey1t[h1:]) + len(DeKey2t[:h2]):
                    word = word.replace(DeKey1t[h1:], "")
                    word = word.replace(DeKey2t[:h2], "")
                    word = word[1:4] + word[0] + word[4:]
                elif len(word) == 7 + len(DeKey1t) + len(DeKey2t):
                    word = word.replace(DeKey1t[:h1], "")
                    word = word.replace(DeKey1t[h1:], "")
                    word = word.replace(DeKey2t[:h2], "")
                    word = word.replace(DeKey2t[h2:], "")
                    word = word[4:] + word[3] + word[0:3]
                elif 11 + len(DeKey1t[:h1]) + len(DeKey1t[:h1]) + len(DeKey1t[:h1]) + len(DeKey2t) + len(DeKey1t[h1:]) > len(word) > 7 + len(DeKey1t[:h1]) + len(DeKey1t[:h1]) + len(DeKey1t[:h1]) + len(DeKey2t) + len(DeKey1t[h1:]):
                    word = word.replace(DeKey1t[:h1], "")
                    word = word.replace(DeKey1t[h1:], "")
                    word = word.replace(DeKey2t[h2:], "")
                    word = word.replace(DeKey2t[:h2], "")
                elif len(word) > 10 + len(DeKey1t[:h1]) + len(DeKey1t[:h1]) + len(DeKey1t[:h1]) + len(DeKey2t) + len(DeKey1t[h1:]) + len(DeKey2t[h2:]):
                    word = word.replace(DeKey1t[:h1], "")
                    word = word.replace(DeKey1t[h1:], "")
                    word = word.replace(DeKey2t[h2:], "")
                    word = word.replace(DeKey2t[:h2], "")

                #Translation
                TempList.append(word)
            CompletedList.append(TempList)
            #Writing to file
            self.writeToFile(CompletedList, "decrypt")
        except:
            #Exception warning
            popup = Popup(title='Uh Oh',
            content=Label(text='One or more inputs are invalid!'),
            size_hint=(None, None), size=(390, 400))
            popup.open()
            
if __name__ == '__main__':
    bColor = [1,1,1,1]
    sm = ScreenManager()
    sm.add_widget(EnigmaScreen(bColor, name='eng'))
    sm.current = "eng"

    class EnigmaApp(App):
        def build(self):
            return sm

    EnigmaApp().run()
