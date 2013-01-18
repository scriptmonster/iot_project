# -*- coding : utf-8 -*- 

from nltk.stem.porter import PorterStemmer
from itertools import groupby
from scipy import mean

import re

class CollectWordBaseFeatures():
    """Collect Word Based Features from given text input"""
    
    def __init__(self, **kwarg):
        self.isTotalNumOfWords = kwarg.get('totalNumOfWords',True)
        self.isAverageWordLength = kwarg.get('averageWordLength',True)
        self.isTotalNumOfDifferentWords = kwarg.get('totalNumOfDifferentWords',True)
        self.isTotalNumOfLongWords = kwarg.get('totalNumOfLongWords',True) # words hase more then 6 characters
        self.isTotalNumOfShortWords = kwarg.get('totalNumOfShortWords',True)
        self.isYulesI = kwarg.get('yulesI',True)
        #self.isDFS = kwarg.get('distinguishingFeatureSelector',True) # Thanks to paper http://dx.doi.org/10.1016/j.knosys.2012.06.005
        #self.isGiniIndex = kwarg.get('giniIndex',True)
        self.isTotalNumOfSmileys = kwarg.get('totalNumOfSmileys',True)
        self.addSmileysToWords = kwarg.get('addSmileysToWords',True)

        self.__defineGlobals()


    def __defineGlobals(self):
        self.lowercase = True
        self.alphaPattern = re.compile('[^a-zA-Z]+')
        self.specialCharsPattern = re.compile('[:,;+*!=<>~%&/\'\\^\\{\\(\\[\\]\\)\\}\\.-]+')
        self.smileyPattern = re.compile(':\)|:\(|:\-\)|:\-\(|:D|:P|:\-P', re.I)

    def __clearTheMess(self, input):

        # Lowercase all characters
        if self.lowercase:
            input = input.lower()

        #get smileys 
        smileys = re.findall(self.smileyPattern, input)

        input = input.replace('&lt;', ' ')
        input = input.replace('&gt;', ' ')
        input = input.replace('&amp;', ' ')
        input = re.sub(self.specialCharsPattern,' ', input)

        words = self.__words(input)

        return words, smileys

    def __uniqify(self, seq, idfun=None): 
        # order preserving
        if idfun is None:
            def idfun(x): return x;
        seen = {}
        result = []

        for item in seq:
            marker = idfun(item)
            # in old Python versions:
            # if seen.has_key(marker)
            # but in new ones:
            if marker in seen: continue
            seen[marker] = 1
            result.append(idfun(item))
        return result

    def __words(self, entry):
        return filter(lambda w: len(w) > 0,
            [w.strip("0123456789!:,.?<>(){}[];*\"'+") for w in entry.split()])

    def __stemWords(self, word):
        stemmer = PorterStemmer()
        return stemmer.stem(word).lower() 

    def __yule(self, words):
        # Thanks to https://github.com/dwillis
        # yule's I measure (the inverse of yule's K measure)
        # higher number is higher diversity - richer vocabulary
        d = {}
        for w in words:
            w = self.__stemWords(w)
            try:
                d[w] += 1
            except KeyError:
                d[w] = 1
     
        M1 = float(len(d))
        M2 = sum([len(list(g))*(freq**2) for freq,g in groupby(sorted(d.values()))])
     
        try:
            return (M1*M1)/(M2-M1)
        except ZeroDivisionError:
            return 0

    def __getFeatures(self, input):

        features = []

        words, smileys = self.__clearTheMess(input)

        uwords = self.__uniqify(words, self.__stemWords)
        usmileys = self.__uniqify(smileys)

        if self.isTotalNumOfWords:
            if self.addSmileysToWords:
                features.append(len(words + smileys))
            else:
                features.append(len(words))

        if self.isAverageWordLength:
            if self.addSmileysToWords:
                features.append(mean(map(len, words + smileys)))
            else:
                features.append(mean(map(len, words)))

        if self.isTotalNumOfDifferentWords:
            if self.addSmileysToWords:
                features.append(len(uwords + usmileys))
            else:
                features.append(len(uwords))

        if self.isTotalNumOfLongWords:
            if self.addSmileysToWords:
                features.append(len([word for word in words + smileys if len(word) > 6]))
            else:
                features.append(len([word for word in words if len(word) > 6]))

        if self.isTotalNumOfLongWords:
            if self.addSmileysToWords:
                features.append(len([word for word in words + smileys if len(word) <= 3]))
            else:
                features.append(len([word for word in words if len(word) <= 3]))

        if self.isYulesI:
            features.append(self.__yule(words))

        return features

    def getFeatures(self, input):
        return self.__getFeatures(input)