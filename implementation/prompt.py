import json
import math
import time
import requests
import os
from dotenv import load_dotenv
#from openai import OpenAI

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENROUTER_API_KEY")

#system_prompt = "Guess the most likely word replacements for '[mask]' in the given context. Provide the top 3 probable answers along with their confidence scores (as percentages). Format your response strictly as follows, with no additional text or explanations:\nword: score%\nword: score%\nword: score%"

system_prompt = "Cluster the words that have the same meaning with , separated. If there are multiple clusters, separate them with ;. No additional text or explanation."


#does not support provider parameter
'''client = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=API_KEY,)

def response(question, model_name):
    message = f"{question}\nReplace [MASK] with the correct word or phrase.\nRespond with the replacement only—no explanation."
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {'role': 'user',
             'content': message}
        ],
        temperature=0.8,
        logprobs=True,
        max_tokens=5,
        #seed=42
    )
    return completion'''

#get response from LM
def response(message, model_name, cluster=False):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}

    data = {'model': model_name,
            'messages': [{'role': "user",
                          'content': message}
                        ],
            'provider': {'require_parameters': True},
            'temperature': 0.8,
            'logprobs': True,
            'max_tokens': 5,
            }
    
    if cluster:
        data = {'model': model_name,
                'messages': [{'role': "user",
                              'content': message},
                              {'role': "system",
                               'conten': system_prompt}
                            ]
                }

    return requests.post(url, headers=headers, json=data).json()


#get logprobe
def probability(completion):
    logprob_total=0.
    for i, logprob in enumerate(completion['choices'][0]['logprobs']['content']):
        logprob_total+=logprob['logprob']

    return math.exp(logprob_total)


'''question = "Samir Soni is married to [mask]."
completion = response(question)
print(completion)
#print(probability(completion))
'''

#make json file with 10 predictions for each question
def sample(num, model_name, path, format):
    with open(f'dataset/test/P{num}.test.filter{format}.json', mode='r', encoding='utf-8') as input_file:
        with open(f'outputs/P{num}.{path}.sample{format}.json', mode='w', encoding='utf-8') as output_file:
            input_data = json.load(input_file)
            output_data = []
            i=1
            for entry in input_data:
                question = entry['question']
                answer = entry['answer']
                guesses = []

                print(i)
                print(question)
                print(answer)

                for _ in range(10):
                    message = f"{question}\nReplace [MASK] with the correct word or phrase.\nRespond with the replacement only—no explanation."
                    if format == ".x":
                        message = f"{question}\nRespond with the correct word or phrase. Answer only-no explanation."

                    completion = response(message, model_name)
                    #print(completion)
                    guess = completion['choices'][0]['message']['content']
                    prob = probability(completion)

                    print(guess)
                    print(prob)
                    x = {'guess': guess,
                        'probability': prob}
                    guesses.append(x)
                    time.sleep(1.0)

                data = {'question': question,
                        'answer': answer,
                        'guesses': guesses}
                output_data.append(data)

                '''if i==1:
                    break'''
                i+=1
            json.dump(output_data, output_file, indent=4)

#let an llm cluster
def cluster(num, path, format):
    model_name = "openai/gpt-5-chat"
    with open(f'outputs/P{num}.{path}.ave{format}.json', mode='r', encoding='utf-8') as input_file:
        input_data = json.load(input_file)
        for entry in input_data:
            guesses = entry['guesses']
            guess_list = [g['guess'] for g in guesses]
            message = ",".join(guess_list)
            print(message)
            #completion = response(message, model_name, cluster=True)
            #print(completion['choices'][0]['message']['content'])