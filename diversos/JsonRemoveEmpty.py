import json

test = json.loads('{"update": {"IMM": {"update": {"SSH": {"update": {}}, "LoginID": {"update": {"1": "USERFG"}}}}}}')

def RemoveEmptyValues(info):
    """
    recursive function to delete empty values
    """
    if isinstance(info, dict):
        for key, value in info.items():

            if isinstance(value, dict) or isinstance(value, list):
                value = RemoveEmptyValues(value)

            if value in ["", None, [], {}]:
                del info[key]

    elif isinstance(info, list):
        for index in reversed(range(len(info))):
            value = info[index]

            if isinstance(value, dict) or isinstance(value, list):
                value = RemoveEmptyValues(value)

            if value in ["", None, [], {}]:
                info.pop(index)

    return info

print(RemoveEmptyValues(test))
