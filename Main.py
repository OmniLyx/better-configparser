from typing import Literal
from configparser import ConfigParser as cn
import os, platform

class BetterParser:
    def __init__(self, file:str) -> None:
        """
        provided by OmniLyx
        # BetterParser

        I needed a better ConfigParser for work because well error catching is always nice to have

        I also thought that if I need it maybe more people need it

        This BetterConfigParser may hold some personal Data for internal functional changes

        if you want to know more about this please use the privacyCheck function
        
        """
        self._file:str = file
        self._conf:cn = cn()
        if(os.path.exists(file)):
            self._conf.read(file)
        else:
            with open(file, "w") as f:
                f.write("")
            
        self._errorList:list = []

        self._personalStorage = {
            "DeviceName": platform.node(),
            "Machine": platform.machine(),
            "bits": platform.architecture()[0], 
            "Operating": platform.system(),
            "PyVersion": platform.version()
            }
    
    def privacyCheck(self, DisplayType:Literal["raw", "keyList", "valueList", "dict"] = "dict") -> list|dict|str:
        """
        This is a function that returns every little bit of information we have on you

        if you dont trust this go to the source code
        
        """
        if(DisplayType == "dict"):
            return self._personalStorage
        if(DisplayType == "keyList"):
            return [x for x in self._personalStorage.keys()]
        if(DisplayType == "valueList"):
            return [x for x in self._personalStorage.values()]
        if(DisplayType == "raw"):
            v = ""
            for i in self._personalStorage:
                v = v + f"{i}: {self._personalStorage[i]}\n"
            
            return v    
        # If you see this well now you know that we don't hide anything (except for this message)

    def confirm(self) -> bool:
        
        try:
            with open(self._file, "w") as f:
                self._conf.write(f)
            return True
        except Exception as e:
            self._errorList.append(e)
            return False
        
    def hasSection(self, section:str) -> bool:
        """
        ## hasSection

        return a bool that will tell you if the section exists
        """
        
        return section.lower() in self._conf.sections
    
    def hasOption(self, section:str, option:str) -> bool:
        """
        ## HasOption

        ### Args:
            * section: str = The section you will search for
            * option: str = The option you want to search for

        ### Returns:
            * True if it does exist
            * False if it doesn't (what did you expect)
        """
        if(self.hasSection(section)):
            return option.lower() in self._conf.options(section)
        else:
            return False

    def get(self, 
            section:str, 
            option:str, 
            fallback:(
                str|
                int|
                bool|
                float|
                None
                )=None,

            RType:
            Literal["str", "int", "bool", "float"]="str") -> \
                \
                (
                str|
                int|
                bool|
                float|
                None
                ):
        """
        ##get

        this will get the value that is requested from the selected file
        
        """
        section = section.lower()
        option = option.lower()

        if(not self.hasSection(section)):
            return fallback
        if(not self.hasOption(section, option)):
            return fallback
        
        if(RType == "str"):
            try:
                return self._conf.get(section, option)
            except Exception as e:
                return fallback
        if(RType == "bool"):
            try:
                return self._conf.getboolean(section, option)
            except:
                self._errorList.append(e)
                return fallback
        if(RType == "float"):
            try:
                return self._conf.getfloat(section, option)
            except:
                self._errorList.append(e)
                return fallback
        if(RType == "int"):
            try:
                return self._conf.getint(section, option)
            except Exception as e:
                self._errorList.append(e)
                return fallback
            
    def write(self, 
              section:str, 
              option:str, 
              value:str|int|float|bool
              ):
        """
        ## Write

        ### Args:
            * Section: str = the section you are looking for
            * Option: str = the option you are looking for
            * Value: str|int|flaot|bool = The value you want to write to it
        
        ### returns:
            * Bool = if it was successfully written
        """
        if(self.hasOption(section, option)):
            if(isinstance(value, bool)):
                value = "yes" if value else "no"
            self._conf[section][option] = value
            return self.confirm()
        else: return False