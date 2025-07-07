import json
from bert_score import BERTScorer

def average(num, path):
    scorer = BERTScorer(model_type='bert-base-uncased')
    with open(f'outputs/P{num}.{path}.sample.x.json', mode='r', encoding='utf-8') as input_file:
        input_data = json.load(input_file)
        output_data = []

        with open (f'outputs/P{num}.{path}.top2.x.json', mode='w', encoding='utf-8') as output_file:
            for entry in input_data:
                question = entry['question']
                answer = entry['answer']
                guess_sum_count = []    #list with guess, sum of the guess, count of the guess

                for guess_entry in entry['guesses']:    #iteration over 10 guesses
                    exist = False
                    for x in guess_sum_count:
                        if x['guess'] == guess_entry['guess']:  #check if the guess is already in the list
                            x['sum'] += guess_entry['probability']
                            x['count']+=1
                            exist = True
                            break
                    if not exist:
                        x = {'guess': guess_entry['guess'],
                            'sum': guess_entry['probability'],
                            'count': 1}
                        guess_sum_count.append(x)

                guesses = []
                for x in guess_sum_count:  #average out
                    if x['count'] == 1:
                        guesses.append({'guess': x['guess'],
                                        'probability': round(x['sum'],4)})
                    else:
                        prob = round(x['sum']/x['count'],4)
                        guesses.append({'guess': x['guess'],
                                        'probability': prob})
                
                guesses = sorted(guesses, key=lambda x: x['probability'], reverse=True)
                while len(guesses) > 1:
                    score = scorer.score([guesses[0]['guess']], [guesses[1]['guess']])[2].mean().item()
                    if score >= 0.8:
                        guesses.pop(1)
                    else:
                        guesses = guesses[:2]
                        break
                    
                data = {'question': question,
                        'answer': answer,
                        'guesses': guesses}
                output_data.append(data)

            json.dump(output_data, output_file, indent=4)
