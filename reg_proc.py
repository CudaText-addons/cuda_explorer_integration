from .port import *

try:
    import winreg
    hkey = winreg.HKEY_CLASSES_ROOT
except:
    winreg = None
    hkey = None


def add_reg(name, descr, cmd):
    try:
        if descr == "":
            descr = name
        import winreg as winreg
        #associate with both any files & Folders (right click on folder is neat !)
        for item in ["*", "Directory"]:
            key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r'%s\shell\%s' % (item, name))
            key2 = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r'%s\shell\%s\command' % (item, name))
            winreg.SetValueEx(key, "", None, winreg.REG_SZ, "%s " % descr)
            #icon will take binary icon from cmd
            winreg.SetValueEx(key, "Icon", None, winreg.REG_SZ, cmd)
            #put Cuda at top of context-menu
            #winreg.SetValueEx(key, "Position", None, winreg.REG_SZ, "Top")
            winreg.SetValueEx(key, "", None, winreg.REG_SZ, "%s " % descr)
            
            if item == "*":
                winreg.SetValueEx(key2, "", None, winreg.REG_SZ, '"%s" "%%1"' % cmd)
            if item == "Directory":
                winreg.SetValueEx(key2, "", None, winreg.REG_SZ, '"%s" "%%V"' % cmd)
            winreg.CloseKey(key2)
            winreg.CloseKey(key)
            
        return True
    except WindowsError:
        return False

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
        return ''

RegKeyShell = r'*\shell'
RegKeyFiles = r'*\shell\%s'%APP_NAME
RegKeyFolders = r'Directory\shell\%s'%APP_NAME
RegKey1 = RegKeyFiles + r'\command'
RegKeyList = '%s_List'%APP_NAME
RegKeyAppName = APP_NAME
RegKeyAppOpen = RegKeyAppName + r'\shell\Open\command'
RegKeyBak = '%s_bak'%APP_NAME
ShellValue = '"%s" "%%1"' % exe_path

def apply_shell_extension(en):
    if en:
        res = add_reg(APP_NAME, 'Open with &CudaText', exe_path)
    else:
        winreg.DeleteKey(hkey, RegKeyFiles)
        winreg.DeleteKey(hkey, RegKeyFolders)
        res = True

    if res:
        return True
    else:
        raise PermissionError

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
        if v1 and v2 and v3:
            return True
        else:
            raise PermissionError
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
