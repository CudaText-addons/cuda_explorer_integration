from .port import *

try:
    import winreg
    hkey = winreg.HKEY_CLASSES_ROOT
except:
    winreg = None
    hkey = None


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


def del_reg(keypath):
    winreg.DeleteKey(hkey, keypath)


RegKey0 = r'*\shell\%s'%APP_NAME
RegKey1 = RegKey0 + r'\command'
RegKeyList = '%s_List'%APP_NAME

RegKeyAppName = APP_NAME
RegKeyAppOpen = RegKeyAppName + r'\Shell\Open\Command'
RegKeyBak = '%s_bak'%APP_NAME

ShellValue = '"%s" "%%1"' % exe_path


def apply_shell_extension(en):
    if en:
        res = set_reg(RegKey1, '', ShellValue)
    else:
        del_reg(RegKey1)
        del_reg(RegKey0)
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
