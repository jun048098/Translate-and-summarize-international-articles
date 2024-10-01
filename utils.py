import json

def save_txt(file_path: str, data: list, seperator: str ='\n*****\n'):
     with open(file_path, "w", encoding='utf8') as file:
        for line in data:
            file.write(line + seperator)
            

def load_txt(file_path: str, seperator: str ='\n*****\n'):
    with open(file_path, "r", encoding='utf8') as file:
        data = file.readlines()
        data = ''.join(data).split(seperator)
    return [i for i in data if i]


def save_json(file_path: str, data: list):
     with open(file_path, "w", encoding='utf8') as file:
        json.dump(data, file)