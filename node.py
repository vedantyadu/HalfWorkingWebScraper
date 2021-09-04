
class Node:
    
    def __init__(self, tagtype:str, attributes:list, text:str, parent, identifier:int):
        self.type = tagtype
        self.attributes:dict = attributes
        self.text = text
        self.parent:self.__class__ = parent
        self.__identity = identifier
    
    
    
    def getIdentifier(self):
        return self.__identity
    
    
    
    def getAttribute(self, name:str):
        return self.attributes[name]
    
    
    
    def equateAttribute(self, name:str, value:str):

        if name in self.attributes:
            if self.attributes[name] == value:
                return True
        
        return False
        


    def equateIdentity(self, other):
        return self.getIdentifier() == other.getIdentifier()
