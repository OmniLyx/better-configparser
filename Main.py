from typing import Literal
from configparser import ConfigParser as cn, SectionProxy as SP
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
        
        return section.lower() in self._conf.sections()
    
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
        if(self.hasOption(section)):
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
            
    def createSection(self, section:str) -> bool:
        if(self.hasSection(section.lower())):
            return True
        else:
            try:
                self._conf.add_section(section.lower())
                return True
            except Exception as e:
                self._errorList.append(e)
                return False
            
        return False


    def deleteSection(self, section:str):
        """
        Will remove a section
        """
        try:
            self._conf.remove_section(section.lower())
            return True
        except:
            return False

    def deleteOption(self, section:str, option:str):
        try:
            self._conf.remove_option(section.lower(), option.lower())
            return True
        except:
            return False


            
    def write(self, 
              section:str, 
              option:str, 
              value:str|int|float|bool,
              override:bool=True
              ):
        """
        ## Write

        ### Args:
            * Section: str = the section you are looking for
            * Option: str = the option you are looking for
            * Value: str|int|float|bool = The value you want to write to it
            * override: bool = defaults True this paramater will define if a function overrides the previous value or if it just returns without anything
        
        ### returns:
            * Bool = if it was successfully written
        """
        section, option, = section.lower(), option.lower()

        if(not self.hasSection(section)):
            self.createSection(section)
    
        if(self.hasOption(section, option)):
            if(not override):
                return False
        if(isinstance(value, bool)):
            value = "yes" if value else "no"
        self._conf[section][option] = value
        return self.confirm()
    
    def __getitem__(self, item:str):
        
        SectionProx = SectionProxy()

        if(not self.hasSection(item.lower())):
            self.createSection(item.lower())
            
        SectionProx._select(self._conf, item.lower(), self.confirm)

        
        return SectionProx
    


class SectionProxy:
    def __init__(self) -> None:
        pass

    def _select(self, config:cn, section:str, confirmFunction):
        self._config = config
        self._section = config[section.lower()]
        self._sectionStr = section.lower()
        self._confirm = confirmFunction

    def hasOption(self, option:str):
        return option.lower() in self._section.keys()

    def write(self,
              option:str,
              value:str|int|float|bool,
              override:bool=True,
              commit:bool=True
              ) -> bool:
        if(self.hasOption(option)):
            if(not override):
                return False
        if(isinstance(value, bool)):
            value = "yes" if value else "no"
        self._section[option.lower()] = value
        if(commit):
            return self._confirm()
        else:
            return True
    
    def deleteSection(self):
        """
        Will make this SectionProxy broken and will most likely not work
        """
        try:
            self._config.remove_section(self._sectionStr)
            return True
        except:
            return False

    def deleteOption(self, option:str):
        try:
            self._config.remove_option(self._sectionStr, option.lower())
            return True
        except:
            return False
    
    def get(self,
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
        

        section = self._sectionStr.lower()
        option = option.lower()

        if(not self.hasOption(option)):
            return fallback
        
        if(RType == "str"):
            try:
                return self._config.get(section, option)
            except Exception as e:
                return fallback
        if(RType == "bool"):
            try:
                return self._config.getboolean(section, option)
            except:
                return fallback
        if(RType == "float"):
            try:
                return self._config.getfloat(section, option)
            except:
                return fallback
        if(RType == "int"):
            try:
                return self._config.getint(section, option)
            except Exception as e:
                return fallback
            
    def __getitem__(self, item:str):
        OptionProx = OptionProxy()
        
        if(not self.hasOption(item.lower())):
            self._config[self._sectionStr][item.lower()] = ""
            self._confirm()
        
        OptionProx.FromSectionProxy(self._section, str(item), self._config, self._confirm)
        
        return OptionProx

    def __len__(self):
        return len(self._section.keys())
    
    def __str__(self) -> str:
        return self._sectionStr
    
    def __iter__(self):
        return iter([x for x in self._section.keys()])


class OptionProxy:

    def __init__(self) -> None:
        pass

    def FromSectionProxy(self, section:SP, name:str, config:cn, confirm):
        self._option:str = name.lower()
        self._section = section
        self._confirm = confirm
        self._config = config
    
    def exist(self) -> bool:
        return self._option in self._section 

    def get(self,
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
        

        option = self._option

        if(not self.exist()):
            return fallback
        
        if(RType == "str"):
            try:
                return self._section.get(option, fallback)
            except Exception as e:
                return fallback
        if(RType == "bool"):
            try:
                return self._section.getboolean(option, fallback)
            except:
                return fallback
        if(RType == "float"):
            try:
                return self._section.getfloat(option, fallback)
            except:
                return fallback
        if(RType == "int"):
            try:
                return self._section.getint(option, fallback)
            except Exception as e:
                return fallback
    
    def write(self,
              value:str|int|float|bool,
              override:bool=True
              ) -> bool:
        
        self._section[self._option]
    
    def delete(self) -> bool:
        self._config.remove_option(self._section.name, self._option)
        return self._confirm()

    
    def __set__(self, value:str|int|float|bool):
        return self.write(value)

    def __str__(self):
        return self.get()
    
    def __bool__(self):
        return self.get(RType="bool")
    

    def __int__(self):
        return self.get(RType="int")
    
    def __float__(self):
        return self.get(RType="float")