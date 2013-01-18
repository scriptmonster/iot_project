# -*- coding : utf-8 -*- 

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

    def __readFile(self):
        """Reads all of the file at once and returns the text"""
        self.__openFile()
        if self.file is None:
            return None
        txt = self.file.read()

        self.__closeFile()
        return txt

    def __removeNewLine(self, input):
        """Removes \\n char at the end of the each line"""
        if input is None:
            return None
        return re.sub('\n$','',input)


    def __readLine(self):
        """Reads a line at every call of the method, when EOF reached returns None"""
        if not self.__fileOpen:
            self.__openFile()
        if self.file is not None:
            txt = self.file.readline()
        else:
            txt = None
        return self.__removeNewLine(txt)

    def readFile(self):
        return self.__readFile()

    def readLine(self):
        return self.__readLine()
        