#!/usr/bin/env python

# -*- coding : utf-8 -*- 

from load import LoadDataFile
from character import CollectCharBasedFeatures
from word import CollectWordBaseFeatures

import re

def parseLine(line, pattern):
    matchResult = pattern.match(line)
    if matchResult is None:
        return None
    else:
        return matchResult.group(1), matchResult.group(2)

def main():
    ldf = LoadDataFile('../../input/SMSSpamCollection')
    ccbf = CollectCharBasedFeatures()
    cwbf = CollectWordBaseFeatures()

    linePattern = re.compile('^(?P<class>spam|ham)\\t(?P<message>.*)$')

    txt = ldf.readLine()
    while txt:
        klass, message = parseLine(txt, linePattern)
        #print klass, '$', message, '$', ccbf.getFeatures(message), cwbf.getFeatures(message)
        print message, ', '.join(map(str,ccbf.getFeatures(message) + cwbf.getFeatures(message))) + ' - > ' + klass
        txt = ldf.readLine()


if __name__ == '__main__':
    main()