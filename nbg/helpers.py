from string import split

def listify(str):
    ret_list = split(str, ',')
    if ret_list[0] == "":
        ret_list = []
    else:
        ret_list = map(int, ret_list)

    return ret_list
