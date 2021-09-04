import node


class Scrape:
    
    singletonTags = [
        "area",
        "base",
        "br",
        "col",
        "command",
        "embed",
        "hr",
        "img",
        "input",
        "keygen",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
        "menuitem",
        "!DOCTYPE",
        "!doctype"
    ]

    def __init__(self, html:str):
        self.__html = html
        self.__count = 0
        self.tree = self.__createTree()


    
    # Get the type of an opentag
    def __getType(self, pos:int, closetag:bool = False):
        
        returnDict = {
            "type": "",
            "singleton": False,
            "pos": None,
            "newtag": False
        }
        
        while self.__html[pos] != " " and self.__html[pos] != ">":
            
            if self.__html[pos] == "<":
                returnDict["type"] = "<" + returnDict["type"]
                returnDict["newtag"] = True
                returnDict["pos"] = pos
                return returnDict
            
            if self.__html[pos] != '\n':
                returnDict["type"] += self.__html[pos]
            
            pos += 1
        
        if returnDict["type"] in self.singletonTags: 
            returnDict["singleton"] = True
        
        if closetag:
            while self.__html[pos] != ">":
                pos += 1
         
        returnDict["pos"] = pos
        
        return returnDict
    
    
    
    # Format attributes and values into a dictonary
    def __formatAttr(self, splittedText:list):  
        
        i = 0
        attributes = {}
        
        while i < len(splittedText):
            
            if len(splittedText) - 1 > i:
                
                if splittedText[i + 1] == "=":
                    attributes[splittedText[i]] = splittedText[i + 2]
                    i += 3
                
                else:
                    attributes[splittedText[i]] = None
                    i += 1
            
            # Else : Last attribute has no value
            else:
                attributes[splittedText[i]] = None
                i += 1 

        
        return attributes
    
    
    
    # Split a string into attributes and their values
    def __splitAttr(self, attr:str):
        
        splittedText = []
        currentAttr = ""
        insideQuote = False
        i = 0
        
        while i < len(attr):
            
            if attr[i] == " " and not insideQuote:
                
                if currentAttr != "":
                    splittedText.append(currentAttr)
                    
                currentAttr = ""
                i += 1

            elif attr[i] == "=" and not insideQuote:
                
                if currentAttr != "":
                    splittedText.append(currentAttr)
                    
                splittedText.append(attr[i])
                currentAttr = ""
                i += 1
            
            else:
                if attr[i] != '"' and attr[i] != '\n':
                    currentAttr += attr[i]
                i += 1

            if i < len(attr):
                if attr[i] == '"':
                    insideQuote = not insideQuote
            
            
        if currentAttr != "":
            splittedText.append(currentAttr)

        return self.__formatAttr(splittedText)
    
    
    
    # Get type and attribute of a tag
    def __getTag(self, pos:int):
        
        type_dict = self.__getType(pos)
        
        returnDict = {
            "type": type_dict["type"],
            "singleton": type_dict["singleton"],
            "attributes": None,
            "newtag": {
                "open": False,
                "text": ""
            },
            "newpos": pos
        }
        
        if type_dict["newtag"]:
            returnDict["newpos"] = type_dict["pos"]
            returnDict["newtag"]["open"] = True
            returnDict["newtag"]["text"] = type_dict["type"]
            return returnDict
        
        attrString = ""
        insideQuote = False
        i = type_dict["pos"]

        while i < len(self.__html):
            
            if self.__html[i] == ">" and not insideQuote:
                
                if self.__html[i - 1] == "/":
                    returnDict["singleton"] = True
                    attrString = attrString[0: len(attrString) - 1]
                    
                returnDict["attributes"] = self.__splitAttr(attrString)

                break

            else:
                if self.__html[i] == '"':
                    insideQuote = not insideQuote
                
                attrString += self.__html[i]
            
            
            i += 1

        
        returnDict["newpos"] = i
        return returnDict
   


    # Create an html tree
    def __createTree(self):
        
        stack = []
        closed_tags = []
        i = 0
        
        while i < len(self.__html):
 
            if self.__html[i] == "<" and self.__html[i + 1] != "/":
                
                cur_tag = self.__getTag(i + 1)
                cur_node = None
                
                if not cur_tag["newtag"]["open"]:
                
                    if len(stack) > 0:
                        cur_node = node.Node(cur_tag["type"], cur_tag["attributes"], "", stack[-1], self.__count)
                    else:
                        cur_node = node.Node(cur_tag["type"], cur_tag["attributes"], "", None, self.__count)
                    
                    if cur_tag["singleton"]:
                        closed_tags.append(cur_node)
                    else:
                        stack.append(cur_node)
                        
                    self.__count += 1
                    i = cur_tag["newpos"] + 1
                
                else:
                    if len(stack) > 0:
                        stack[-1].text += cur_tag["newtag"]["text"] 
                        i = cur_tag["newpos"]
            
            elif self.__html[i] == "<" and self.__html[i + 1] == "/":
                
                close_type = self.__getType(i + 2, True)
                i = close_type["pos"] + 1
                
                if len(stack) > 0:
                    if close_type["type"] == stack[-1].type:
                        closed_tags.append(stack.pop())
            
            else:
                if len(stack) > 0:
                    stack[-1].text += self.__html[i]
                i += 1
        
        return closed_tags
    
    
    
    
    def findChildren(self, element):
        
        returnArr = []
        
        for i in self.tree:
            if i.parent == element.parent:
                returnArr.append(i)

        return returnArr
    
    
    
    def findChildren(self, tag):
            
            returnArr = []
            
            for i in self.tree:
                if i.parent == tag:
                    returnArr.append(i)

            return returnArr
    
    
    
    def getElementsByAttribute(self, attr:str, value:str):
        
        returnArr = []
        
        for i in self.tree:
            if i.equateAttribute(attr, value):
                returnArr.append(i)
        
        return returnArr
        
    
    
    def getElementByID(self, value:str):
        
        for i in self.tree:
            if i.equateAttribute("id", value):
                return i

        return None
    
    
    
    def getElementsByType(self, name:str):
        
        returnArr = []
        
        for i in self.tree:
            if i.type == name:
                returnArr.append(i)
                
        return returnArr
        