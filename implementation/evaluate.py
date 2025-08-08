import json
from bert_score import BERTScorer


#find prdictions exactly same as answer
def exactMatch(num, path):
    with open(f'outputs/P{num}.{path}.top2.json', mode='r', encoding='utf-8') as input_file:
        input_data = json.load(input_file)
        first = 0
        second = 0
        for entry in input_data:
            answer = entry['answer']
            guesses = entry['guesses']

            #check on guess1
            guess1 = guesses[0]['guess']
            if answer == guess1:
                print("guess1: ", guess1)
                first+=1
            
            #check on guess2
            if len(guesses) > 1:
                guess2 = entry['guesses'][1]['guess']
                if answer == guess2:
                    print("guess2: ", guess2)
                    second+=1

        print(f"Final result\nguess1: {first}\nguess2: {second}")


#find predcitons which have same words in answers or the other way around
def wordsInWords(num, path):
    with open(f'outputs/P{num}.{path}.top2.json', mode='r', encoding='utf-8') as input_file:
        input_data = json.load(input_file)
        first = 0
        second = 0
        for entry in input_data:
            answer = entry['answer']
            guesses = entry['guesses']

            #check on guess1
            guess1 = guesses[0]['guess']
            if answer in guess1 or guess1 in answer:
                print("guess1: ", guess1)
                print("answer: ", answer)
                first+=1
            
            #check on guess2
            if len(guesses) > 1:
                guess2 = entry['guesses'][1]['guess']
                if answer in guess2 or guess2 in answer:
                    print("guess2: ", guess2)
                    print("answer: ", answer)
                    second+=1

        print(f"Final result\nguess1: {first}\nguess2: {second}")


#make json file with BERTScore for each top 2 predictions
def bertscore(num, path, format):
    scorer = BERTScorer(model_type='bert-base-uncased')
    with open(f'outputs/P{num}.{path}{format}.top2.json', mode='r', encoding='utf-8') as input_file:
        with open(f'evaluation/P{num}.{path}{format}.json', mode='w', encoding='utf-8') as output_file:
            input_data = json.load(input_file)
            output_data = []
            for entry in input_data:
                question = entry['question']
                answer = entry['answer']
                guesses = entry['guesses']
                xs = []
                #guess1
                guess1 = guesses[0]['guess']
                prob1 = guesses[0]['probability']
                P, R, F1 = scorer.score([guess1], [answer])
                x = {'guess': guess1,
                     'probability': prob1,
                     'precision': round(P.mean().item(),4),
                     'recall': round(R.mean().item(),4),
                     'f1': round(F1.mean().item(),4)}
                xs.append(x)

                print(f"BERTScore Precision guess1: {P.mean():.4f}, Recall: {R.mean():.4f}, F1: {F1.mean():.4f}")

                #guess2
                if len(guesses) > 1:
                    guess2 = entry['guesses'][1]['guess']
                    prob2 = entry['guesses'][1]['probability']
                    P, R, F1 = scorer.score([guess2], [answer])
                    x = {'guess': guess2,
                         'probability': prob2,
                         'precision': round(P.mean().item(),4),
                         'recall': round(R.mean().item(),4),
                         'f1': round(F1.mean().item(),4)}
                    xs.append(x)

                    print(f"BERTScore Precision guess2: {P.mean():.4f}, Recall: {R.mean():.4f}, F1: {F1.mean():.4f}")
                
                data = {'question': question,
                        'answer': answer,
                        'guesses': xs}
                output_data.append(data)
            json.dump(output_data, output_file, indent=4)
