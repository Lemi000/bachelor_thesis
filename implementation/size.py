#calcaulate the number of the questions

import json

num = 26

with open(f'dataset/test/P{num}.test.trans.json', mode='r', encoding='utf-8') as input_file:
    input_data = json.load(input_file)
    print(len(input_data))
