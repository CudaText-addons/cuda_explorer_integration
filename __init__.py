import os
from cudatext import *
from .dlg import *
from .reg_proc import *

class Command:
    def dialog(self):
        if os.name!='nt':
        	msg_box('This plugin is for Windows only', MB_OK+MB_ICONERROR)
        	return
    
        old_menu = is_shell_extension_enabled()
        old_txt = is_file_assoc_enabled('txt')
        old_ini = is_file_assoc_enabled('ini')
        old_proj = is_file_assoc_enabled('cuda-proj')
        old_sess = is_file_assoc_enabled('cuda-session')
    
        res = dialog_config(old_menu, old_txt, old_ini, old_proj, old_sess)
        if res is None: return
        (op_menu, op_txt, op_ini, op_proj, op_sess) = res

        try:
            if old_menu!=op_menu: apply_shell_extension(op_menu)
            if old_txt!=op_txt: apply_file_assoc('txt', op_txt)
            if old_ini!=op_ini: apply_file_assoc('ini', op_ini)
            if old_proj!=op_proj: apply_file_assoc('cuda-proj', op_proj)
            if old_sess!=op_sess: apply_file_assoc('cuda-session', op_sess)
        except:
            msg_box('Cannot write registry key.\nTry to run program as Administrator.', MB_OK+MB_ICONWARNING)
