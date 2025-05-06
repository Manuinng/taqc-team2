import json

def camel_to_snake(camel_case_str):
    snake_case_str = []
    for char in camel_case_str:
        if char.isupper() and snake_case_str:
            snake_case_str.append('_')
            snake_case_str.append(char.lower())
        else:
            snake_case_str.append(char)
    return ''.join(snake_case_str)

def load_json(file_name):
    file_path = f"./tests/test_data/{file_name}"
    with open(file_path, 'r') as json_file:
        return json.load(json_file)
