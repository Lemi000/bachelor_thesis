#filter the dataset into 50 questions and answers

from transformers import AutoTokenizer
from dotenv import load_dotenv
import json
import random
import os

load_dotenv()  # Load environment variables from .env file
access_token = os.getenv("HUGGINGFACE_ACCESS_TOKEN")

model_path = "meta-llama/Llama-3.1-8B-Instruct"



tokenizer = AutoTokenizer.from_pretrained(model_path, token=access_token)


'''text = "Philip II of Macedon"
tokens = tokenizer.tokenize(text)
print(tokens)
print(len(tokens))'''

num = 264
seed_value = 42

with open(f'dataset/test/P{num}.test.json', mode='r', encoding='utf-8') as input_file:
    input_data = json.load(input_file)
    output_data = input_data.copy()

    with open (f'dataset/test/P{num}.test.filter2.json', mode='w', encoding='utf-8') as output_file:
        i=0
        for entry in input_data:
            if len(entry['answers']) > 1:   #filter out question with muliple answers
                output_data.pop(i)
                continue
            answer = entry['answers'][0]
            tokens = tokenizer.tokenize(answer)

            if len(tokens) > 5:     #filter out question with more than 5 tokens answer
                output_data.pop(i)
                continue
            elif len(tokens) < 3:   #filter out question with less than 3 tokens answer
                output_data.pop(i)
                continue
            i+=1
        
        random.seed(seed_value)
        output_data = random.sample(output_data, 50)    #50 random elements (seed:42)

        result = []
        for entry in output_data:
            data = {'question': entry['question'],
                    'answer': entry['answers'][0]}
            result.append(data)
        json.dump(result, output_file, indent=4)
