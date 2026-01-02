from .port import *
from cudax_lib import get_translation

_   = get_translation(__file__)  # I18N

def dialog_config(op_menu, op_txt, op_ini, op_proj, op_sess, op_list):

    id_menu = 0
    id_txt = 1
    id_ini = 2
    id_proj = 3
    id_sess = 4
    id_memo = 6
    id_ok = 7

    c1 = chr(1)

    label_add_item = _('Add "%(app)s" item to Explorer context &menu') % {'app': APP_NAME}
    label_assoc_txt = _('Associate %(app)s with "&txt" files') % {'app': APP_NAME}
    label_assoc_ini = _('Associate %(app)s with "&ini" files') % {'app': APP_NAME}
    label_assoc_proj = _('Associate %(app)s with "%(ext)s" files') % {'ext': EXT_PROJ, 'app': APP_NAME}
    label_assoc_sess = _('Associate %(app)s with "%(ext)s" files') % {'ext': EXT_SESS, 'app': APP_NAME}
    label_memo = _('&Also register extensions (no dots, one per line, lower case):')
    label_ok = _('&OK')
    label_cancel = _('Cancel')

    text = '\n'.join([]
        +[c1.join(['type=check', 'pos=6,6,500,0', 'cap='+label_add_item, 'val='+('1' if op_menu else '0') ])]
        +[c1.join(['type=check', 'pos=6,40,500,0', 'cap='+label_assoc_txt, 'val='+('1' if op_txt else '0')])]
        +[c1.join(['type=check', 'pos=6,64,500,0', 'cap='+label_assoc_ini, 'val='+('1' if op_ini else '0')])]
        +[c1.join(['type=check', 'pos=6,88,500,0', 'cap='+label_assoc_proj, 'val='+('1' if op_proj else '0')])]
        +[c1.join(['type=check', 'pos=6,112,500,0', 'cap='+label_assoc_sess, 'val='+('1' if op_sess else '0')])]
        +[c1.join(['type=label', 'pos=6,136,200,0', 'cap='+label_memo])]
        +[c1.join(['type=memo', 'pos=6,156,200,270', 'val='+'\t'.join(sorted(op_list))])]
        +[c1.join(['type=button', 'pos=200,280,300,0', 'cap='+label_ok, 'ex0=1'])]
        +[c1.join(['type=button', 'pos=306,280,402,0', 'cap='+label_cancel])]
    )

    res = dlg_custom('Explorer Integration', 408, 310, text)
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
    op_list = text[id_memo].split('\t')

    return (op_menu, op_txt, op_ini, op_proj, op_sess, op_list)
