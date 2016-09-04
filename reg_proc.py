import os
import winreg
from cudatext import *

hkey = winreg.HKEY_CLASSES_ROOT

def set_reg(keypath, keyname, keyvalue):
    try:
        winreg.CreateKey(hkey, keypath)
        registry_key = winreg.OpenKey(hkey, keypath, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, keyname, 0, winreg.REG_SZ, keyvalue)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False
        

def get_reg(keypath, keyname):
    try:
        registry_key = winreg.OpenKey(hkey, keypath, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, keyname)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None
        
                
def del_reg(keypath):
    winreg.DeleteKey(hkey, keypath) 
    
    
RegKey0 = r'*\shell\CudaText'
RegKey1 = RegKey0 + r'\command'

RegKeyAppName = 'CudaText'
RegKeyAppOpen = RegKeyAppName + r'\Shell\Open\Command'
RegKeyBak = 'CudaText_bak'

ExePath = os.path.join(app_path(APP_DIR_EXE), 'cudatext.exe')
ShellValue = '"%s" "%%1"' % ExePath


def apply_shell_extension(en):
    if en:
        return set_reg(RegKey1, '', ShellValue)
    else:
        v1 = del_reg(RegKey1)
        v2 = del_reg(RegKey0)
        return v1 and v2
 

def is_shell_extension_enabled():
    val = get_reg(RegKey1, '')
    return bool(val) and (val.upper() == ShellValue.upper())


def apply_file_assoc(ext, en):
    if en:
        #backup
        bak = get_reg('.'+ext, '')
        if bak:
            set_reg('.'+ext, RegKeyBak, bak)

        #set "HKEY_CLASSES_ROOT\.txt\@" to "SynWrite"
        #also set "HKEY_CLASSES_ROOT\SynWrite\@" to "Text Document"
        NewDoc = get_reg('txtfile', '')
        v1 = set_reg('.'+ext, '', RegKeyAppName)
        v2 = set_reg(RegKeyAppName, '', NewDoc)
        v3 = set_reg(RegKeyAppOpen, '', ShellValue)
        return v1 and v2 and v3
    else:
        #to restore, set "HKEY_CLASSES_ROOT\.txt\@" to "txtfile"
        val = get_reg('.'+ext, '')
        if not val: return
        bak = get_reg('.'+ext, RegKeyBak)
        if bak:
            set_reg('.'+ext, '', bak)
        else:
            del_reg('.'+ext)
        return True


def is_file_assoc_enabled(ext):
  	v1 = get_reg('.'+ext, '') == RegKeyAppName
  	val = get_reg(RegKeyAppOpen, '')
  	v2 = bool(val) and (val.upper() == ShellValue.upper())
  	return v1 and v2
