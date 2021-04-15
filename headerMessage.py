HEADER_SIZE=8
NAME_SIZE=8
SURNAME_SIZE=8
UNAME_SIZE = 8
PASSW_SIZE = 8
SIGNAL_SIZE=1
def format_message(message,msgType):
    if not message:
        return None
    header = f'{len(message):<{HEADER_SIZE}}'
    signal = f'{msgType:<{SIGNAL_SIZE}}'
    return f'{header}{signal}{message}'
def format_register_message(name, surname, uname, password,msgType):
    header = f'{len(name+surname+uname+password):<{HEADER_SIZE}}'
    signal = f'{msgType:<{SIGNAL_SIZE}}'
    len_name = f'{len(name):<{NAME_SIZE}}'
    len_surname = f'{len(surname):<{SURNAME_SIZE}}'
    len_Uname = f'{len(uname):<{UNAME_SIZE}}'
    len_pw = f'{len(password):<{PASSW_SIZE}}'
    return f'{header}{signal}{len_name}{len_surname}{len_Uname}{len_pw}{name}{surname}{uname}{password}'