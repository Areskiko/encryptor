class Enigma():

    def translation(self, mode, password):
        """Sets up a trantab with a custom alphabet."""
        normAlpha = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890"
        tempAlpha = normAlpha
        for i in range(len(password)):
            tempAlpha = tempAlpha.replace(password[i], "")
        spesAlpha = password + tempAlpha

        #Desciding how the alphabets are being set up
        if mode == "encrypt":
            trantab = str.maketrans(normAlpha, spesAlpha)
        elif mode == "decrypt":
            trantab = str.maketrans(spesAlpha, normAlpha)
        return trantab

    def encrypt(self, text, DeKey1, DeKey2, password):
        """Parses a target file, converts the information and writes it to a new file."""
        try:
            #Parsing file and gathering keywords to use for the encryption
            BigList = text.split(" ")
            CompletedList =  []
            DeKey1t = str(DeKey1)
            DeKey2t = str(DeKey2)

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
            sentence = ""
            for lis in CompletedList:
                for word in lis:
                    sentence += word+" "
            return sentence
        except Exception as e:
            return ["Failure", e]

    def decrypt(self, text, DeKey1, DeKey2, password):
        """Parses a target file, converts the information and writes it to a new file."""
        try:
            #Parsing file and gathering keywords to use for the encryption
            BigList = text.split(" ")
            CompletedList = []
            DeKey1t = str(DeKey1)
            DeKey2t = str(DeKey2)

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
            sentence = ""
            for lis in CompletedList:
                for word in lis:
                    sentence += word+" "
            return sentence
        except Exception as e:
            return ["Failure", e]

if __name__ == "__main__":
    mac = Enigma()
    #'enc', 'Jeg heter stefan', 'zipo', 'leto', 'kalu'
    to = "Jeg heter stefan"
    d1 = "zipo"
    d2 = "leto"
    pa = "kalu"
    enc = mac.encrypt(to, d1, d2, pa)
    dec = mac.decrypt(enc, d1, d2 ,pa)
    print(dec)
    to=""
    for i in range(12):
        to = to+str(i)
        enc = mac.encrypt(to, d1, d2, pa)
        dec = mac.decrypt(enc, d1, d2, pa)
        print(dec)
