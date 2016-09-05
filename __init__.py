import os
from .port import *
from .dlg import *
from .reg_proc import *

class Command:
    def dialog(self):
        if os.name!='nt':
        	msg_error_func('This plugin is for Windows only')
        	return
    
        old_menu = is_shell_extension_enabled()
        old_txt = is_file_assoc_enabled('txt')
        old_ini = is_file_assoc_enabled('ini')
        old_proj = is_file_assoc_enabled(EXT_PROJ)
        old_sess = is_file_assoc_enabled(EXT_SESS)
        old_list = get_reg(RegKeyList, '').split(' ')
    
        res = dialog_config(old_menu, old_txt, old_ini, old_proj, old_sess, old_list)
        if res is None: return
        (op_menu, op_txt, op_ini, op_proj, op_sess, op_list) = res

        try:
            if old_menu!=op_menu: apply_shell_extension(op_menu)
            if old_txt!=op_txt: apply_file_assoc('txt', op_txt)
            if old_ini!=op_ini: apply_file_assoc('ini', op_ini)
            if old_proj!=op_proj: apply_file_assoc(EXT_PROJ, op_proj)
            if old_sess!=op_sess: apply_file_assoc(EXT_SESS, op_sess)

            #extension list
            op_list = [s.strip() for s in op_list if s.strip()]
            if old_list!=op_list:
                set_reg(RegKeyList, '', ' '.join(op_list))
                #handle deleted items
                for s in old_list:
                    if not s in op_list:
                        #print('unregister ext:', s)
                        apply_file_assoc(s, False)
                #handle added items
                for s in op_list:
                    if not s in old_list:
                        #print('register ext:', s)
                        apply_file_assoc(s, True)
                    
        except:
            msg_warn_func('Cannot write registry key.\nTry to run program as Administrator.')
