from cudatext import *

def dialog_config(op_menu, op_txt, op_ini, op_proj, op_sess):

    id_menu = 0
    id_txt = 1
    id_ini = 2
    id_proj = 3
    id_sess = 4
    id_ok = 5

    c1 = chr(1)
    text = '\n'.join([]
        +[c1.join(['type=check', 'pos=6,6,500,0', 'cap=Add "CudaText" item to Explorer context &menu', 'val='+('1' if op_menu else '0') ])]
        +[c1.join(['type=check', 'pos=6,40,500,0', 'cap=Associate CudaText with "&txt" files', 'val='+('1' if op_txt else '0')])]
        +[c1.join(['type=check', 'pos=6,64,500,0', 'cap=Associate CudaText with "&ini" files', 'val='+('1' if op_ini else '0')])]
        +[c1.join(['type=check', 'pos=6,88,500,0', 'cap=Associate CudaText with "cuda-&proj" files', 'val='+('1' if op_proj else '0')])]
        +[c1.join(['type=check', 'pos=6,112,500,0', 'cap=Associate CudaText with "cuda-&session" files', 'val='+('1' if op_sess else '0')])]
        +[c1.join(['type=button', 'pos=230,190,330,0', 'cap=&OK', 'props=1'])]
        +[c1.join(['type=button', 'pos=336,190,432,0', 'cap=Cancel'])]
    )

    res = dlg_custom('Explorer Integration', 438, 220, text)
    if res is None:
        return

    res, text = res
    text = text.splitlines()

    if res != id_ok:
        return

    op_menu = text[id_menu]=='1'
    op_txt = text[id_txt]=='1'
    op_ini = text[id_ini]=='1'
    op_proj = text[id_proj]=='1'
    op_sess = text[id_sess]=='1'

    return (op_menu, op_txt, op_ini, op_proj, op_sess)
    
