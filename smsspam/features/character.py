# -*- coding: utf-8 -*- 

import re

class CollectCharBasedFeatures():
    """Collect Character Based Features from given text input"""

    def __init__(self, **kwargs):
        self.isTotalNumOfChars = kwargs.get('totalNumOfChars',True)
        self.isTotalNumOfLetters = kwargs.get('totalNumOfLetters',True)
        self.isTotalNumOfDigits = kwargs.get('totalNumOfDigits',True)
        self.isTotalNumOfUpper = kwargs.get('totalNumOfUpper',True)
        self.isTotalNumOfWhiteSpace = kwargs.get('totalNumOfWhiteSpace',True)
        self.isTotalNumOfSpecialChars = kwargs.get('totalNumOfSpecialChars',True)
        self.isTotalNumOfCurrencyChars = kwargs.get('totalNumOfCurrencyChars',True)

        self.__defineGlobals()

    def __defineGlobals(self):
        self.alphaPattern = re.compile('[^a-zA-Z]+')
        self.digitPattern = re.compile('[^\d]+')
        self.upperPattern = re.compile('[^A-Z]+')
        self.whiteSpacePattern = re.compile('[^\s]+')
        self.specialCharsPattern = re.compile('[^:,;+*!=<>~%&/\'\\^\\{\\(\\[\\]\\)\\}\\.-]+')
        self.currencyCharsPattern = re.compile('[^£€$]+')


    def __getCountWithPattern(self, pattern, input):
        return len(re.sub(pattern, '', input))

    def __getTotalNumOfChars(self, input):
        return len(input)

    def __getTotalNumOfLetters(self, input):
        return self.__getCountWithPattern(self.alphaPattern, input)

    def __getTotalNumOfDigits(self, input):
        return self.__getCountWithPattern(self.digitPattern, input)

    def __getTotalNumOfUpper(self, input):
        return self.__getCountWithPattern(self.upperPattern, input)

    def __getTotalNumOfWhiteSpace(self, input):
        return self.__getCountWithPattern(self.whiteSpacePattern, input)

    def __getTotalNumOfSpecialChars(self, input):
        return self.__getCountWithPattern(self.specialCharsPattern, input)

    def __getTotalNumOfCurrencyChars(self, input):
        return self.__getCountWithPattern(self.currencyCharsPattern, input)

    
    def __getFeatures(self, input):
        features = []
        if self.isTotalNumOfChars:
            features.append(self.__getTotalNumOfChars(input))

        if self.isTotalNumOfLetters:
            features.append(self.__getTotalNumOfLetters(input))
            
        if self.isTotalNumOfDigits:
            features.append(self.__getTotalNumOfDigits(input))
            
        if self.isTotalNumOfUpper:
            features.append(self.__getTotalNumOfUpper(input))
            
        if self.isTotalNumOfWhiteSpace:
            features.append(self.__getTotalNumOfWhiteSpace(input))
            
        if self.isTotalNumOfSpecialChars:
            features.append(self.__getTotalNumOfSpecialChars(input))
            
        if self.isTotalNumOfCurrencyChars:
            features.append(self.__getTotalNumOfCurrencyChars(input))

        return features

    def getFeatures(self, input):
        return self.__getFeatures(input)
