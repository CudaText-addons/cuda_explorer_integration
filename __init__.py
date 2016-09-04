from cudatext import *
from .dlg import *

class Command:
    def dialog(self):
    
        (op_menu, op_txt, op_ini, op_proj, op_sess) = (False, False, False, False, False)
    
        res = dialog_config(op_menu, op_txt, op_ini, op_proj, op_sess)
        if res is None: return
        (op_menu, op_txt, op_ini, op_proj, op_sess) = res
        
        print((op_menu, op_txt, op_ini, op_proj, op_sess))
