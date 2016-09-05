import os
import cudatext as app

APP_NAME = 'CudaText'
EXT_PROJ = 'cuda-proj'
EXT_SESS = 'cuda-session'

def msg_warn_func(s):
    app.msg_box(s, app.MB_OK+app.MB_ICONWARNING)

def msg_error_func(s):
    app.msg_box(s, app.MB_OK+app.MB_ICONERROR)

exe_path = os.path.join(app.app_path(app.APP_DIR_EXE), 'cudatext.exe')
dlg_custom = app.dlg_custom
