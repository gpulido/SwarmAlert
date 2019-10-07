def service_list_to_str(services_list):
    return '\n'.join([s.name for s in services_list])

def sanitize_str_arg(str_arg):
    if str_arg.startswith('"') and str_arg.endswith('"'):
        str_arg = str_arg[1:-1]
    return str_arg


def get_list_from_params(params_list):
    new_list = sanitize_str_arg(params_list).split(',')
    if new_list == ['']:
        new_list = []
    return new_list
