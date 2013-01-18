# -*- coding : utf-8 -*- 

from random import randint

import codecs, re


class LoadDataFile():
    """
    Loads Features for classification
    """

    def __init__(self, path, **kwargs):
        """Class constructor"""
        self.filePath = path
        #self.fileType = kwargs.get('type', 'file')
        self.fileEncoding = kwargs.get('encoding', 'utf-8')
        self.file = None
        self.__fileOpen = False

        self.__defineRegexPatterns()

    def __openFile(self):
        """Opens file with specified encoding(default utf-8) and set fileOpen flag True"""
        try:
            self.file = codecs.open(self.filePath, 'r', self.fileEncoding)
        except ValueError, e:
            print("Specified encoding cannot be found!\nException message:", e.message)
        except IOError, e:
            print("Specified file does not exists! \n Exception message:", e.message)
        finally:
            self.__fileOpen = True

    def __closeFile(self):
        """Closes file and set fileOpen flag False"""
        self.file.close()
        self.__fileOpen = False

    def __defineRegexPatterns(self):
        self.regex = {}
        self.regex['newLineChar'] = re.compile('\n$')
        self.regex['decimal'] = re.compile("(^| )&lt;DECIMAL&gt;( |$)")
        self.regex['digit'] = re.compile("(^| )&lt;#&gt;( |$)")
        self.regex['time'] = re.compile("(^| )&lt;TIME&gt;( |$)")
        self.regex['url'] = re.compile("(^| )&lt;URL&gt;( |$)")
        self.regex['email'] = re.compile("(^| )&lt;EMAIL&gt;( |$)")


    def __refillParams(self, input):
        """There exists some removed values in dataset, such as decimal numbers, digits, time, url, email and etc.
        This metod randomly replaces these values to increase feature quality"""
        input = re.sub(self.regex['decimal'], str(randint(2,5)), input)
        input = re.sub(self.regex['digit'], '3', input)
        input = re.sub(self.regex['time'], '%d:%d' %(randint(0,23),randint(0,59)), input)
        input = re.sub(self.regex['url'], 'http://www.com', input)
        input = re.sub(self.regex['email'], 'mail@domain.com', input)

        return input

    def __readFile(self):
        """Reads all of the file at once and returns the text"""
        self.__openFile()
        if self.file is None:
            return None
        txt = self.file.read()

        self.__closeFile()
        return txt

    def __removeNewLineChar(self, input):
        """Removes \\n char at the end of the each line"""
        if input is None:
            return None
        return self.__refillParams(re.sub(self.regex['newLineChar'],'',input))


    def __readLine(self):
        """Reads a line at every call of the method, when EOF reached returns None"""
        if not self.__fileOpen:
            self.__openFile()
        if self.file is not None:
            txt = self.file.readline()
        else:
            txt = None
        return self.__removeNewLineChar(txt)

    def readFile(self):
        return self.__readFile()

    def readLine(self):
        return self.__readLine()
        