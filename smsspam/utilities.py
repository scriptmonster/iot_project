# -*- coding : utf-8 -*- 

def abstractMethod():
    """ This should be called when an abstract method is called that should have been
    implemented by a subclass. It should not be called in situations where no implementation
    (i.e. a 'pass' behavior) is acceptable.
    Taken from pyBrain :) """
    raise NotImplementedError('Method not implemented!')
