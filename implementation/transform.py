#from QA format to non-QA format

import json

def transform(num, question):
    words = question.split()
    first = words.index('is')+1
    last = len(words)

    if num == 176:
        last = len(words) - 1 - words[::-1].index('produced')
        subject = ' '.join(words[first:last])
        return f"{subject} is produced by [mask]."
    
    if num == 264:
        last = len(words) - 1 - words[::-1].index('represented')
        subject = ' '.join(words[first:last])
        return f"{subject}'s musci label is represented by [mask]."

    if num == 50:
        first = words.index('of')+1
        words[last-1] = words[last-1].replace('?', '')  #remove "?" at the end of the sentence
        subject = ' '.join(words[first:last])
        return f"The author of {subject} is [mask]."

    if num == 26:
        last = len(words) - 1 - words[::-1].index('married')
        subject = ' '.join(words[first:last])
        return f"{subject} is married to [mask]."
    
num = 264

with open(f'dataset/test/P{num}.test.json', mode='r', encoding='utf-8') as input_file:
    input_data = json.load(input_file)
    output_data = input_data.copy()
    
    with open (f'dataset/test/P{num}.test.trans.json', mode='w', encoding='utf-8') as output_file:
        i = 0
        for entry in input_data:
            question = entry['question']
            output_data[i]['question'] = transform(num,question)
            i+=1
        json.dump(output_data, output_file, indent=4)
