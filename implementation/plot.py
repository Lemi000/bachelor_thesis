import pandas as pd
import matplotlib.pyplot as plt
import json

'''num = 26
format = ".x" # "" for CS format, ".x" for QA format'''

# makes csv file with precision, recall and f1 for both 2 guesses
'''
path = "llama_31_8b"
with open(f'evaluation/P{num}.{path}.json', mode='r', encoding='utf-8') as input_file:
    input_data = json.load(input_file)
    precision_1 = []
    recall_1 = []
    f1_1 = []
    precision_2 = []
    recall_2 = []
    f1_2 = []

    for entry in input_data:
        guesses = entry['guesses']
        if len(guesses) == 2:
            guess1 = guesses[0]
            guess2 = guesses[1]

            precision_1.append(guess1['precision'])
            recall_1.append(guess1['recall'])
            f1_1.append(guess1['f1'])
            precision_2.append(guess2['precision'])
            recall_2.append(guess2['recall'])
            f1_2.append(guess2['f1'])
        else:
            guess1 = guesses[0]
            precision_1.append(guess1['precision'])
            recall_1.append(guess1['recall'])
            f1_1.append(guess1['f1'])
            precision_2.append(None)
            recall_2.append(None)
            f1_2.append(None)
    
    data = {'precision_1': precision_1,
            'recall_1': recall_1,
            'f1_1': f1_1,
            'precision_2': precision_2,
            'recall_2': recall_2,
            'f1_2': f1_2}
    df = pd.DataFrame(data)
    df.to_csv(f"plot/P{num}.{path}.csv", encoding='utf8', index=False, header=True)
    df = pd.read_csv('plot/P26.llama_31_8b.csv')
    df.plot()
    plt.show()'''


# scatter plot on the number of score >= 0.8 of guess1 depending on the gap of probabilities between guess1 and guess2
def gapPlot(num, path, format):
    x_axis = ["≤0.1","≤0.2","≤0.3","≤0.4","≤0.5","≤0.6","≤0.7","≤0.8","≤0.9","≤1"]
    count = [0,0,0,0,0,0,0,0,0,0] #count the number of guesses depending on the prob gap
    count_right = [0,0,0,0,0,0,0,0,0,0]   #count the number of guesses with score >= 0.8 depending on the prob gap
    with open(f'score/P{num}.{path}{format}.json', mode='r', encoding='utf-8') as file:
        data = json.load(file)
        for entry in data:
            prob1 = entry[0]['prob']
            prob2 = entry[1]['prob'] if len(entry) == 2 else 0
            gap = prob1 - prob2
            score = entry[0]['score']
            if gap <= 0.1:
                count[0]+=1
                if score >= 0.8:
                    count_right[0]+=1
            elif gap <= 0.2:
                count[1]+=1
                if score >= 0.8:
                    count_right[1]+=1
            elif gap <= 0.3:
                count[2]+=1
                if score >= 0.8:
                    count_right[2]+=1
            elif gap <= 0.4:
                count[3]+=1
                if score >= 0.8:
                    count_right[3]+=1
            elif gap <= 0.5:
                count[4]+=1
                if score >= 0.8:
                    count_right[4]+=1
            elif gap <= 0.6:
                count[5]+=1
                if score >= 0.8:
                    count_right[5]+=1
            elif gap <= 0.7:
                count[6]+=1
                if score >= 0.8:
                    count_right[6]+=1
            elif gap <= 0.8:
                count[7]+=1
                if score >= 0.8:
                    count_right[7]+=1
            elif gap <= 0.9:
                count[8]+=1
                if score >= 0.8:
                    count_right[8]+=1
            else:
                count[9]+=1
                if score >= 0.8:
                    count_right[9]+=1
    y_axis = []
    for x, y in zip(count, count_right):
        y_axis.append(y/x if x != 0 else None)
    print(y_axis)

    '''plt.figure()
    plt.scatter(x_axis, y_axis, color='blue')
    plt.xlabel("Gap between Top and Second Prediction")
    plt.ylabel("Proportion of Predictions (score ≥ 0.8)")
    plt.savefig(f'plot/gap/P{num}.{path}{format}.png', dpi=300)'''

def gapAlpha(num, path, format):
    x = []
    y = []
    with open(f'score/P{num}.{path}{format}.json', mode='r', encoding='utf-8') as file:
        data = json.load(file)
        for entry in data:
            if len(entry) == 2:
                x.append(entry[0]['prob'] - entry[1]['prob'])
            else:
                x.append(entry[0]['prob'])
            y.append(entry[0]['score'])
    
    plt.figure()
    plt.scatter(x, y)
    plt.xlabel("Gap between Top and Second Prediction")
    plt.ylabel("score")
    plt.savefig(f'plot/gap@/P{num}.{path}{format}.png', dpi=300)

# how many of first guess are right
def first(num, path, format):
    count = 0
    with open(f'score/P{num}.{path}{format}.json', mode='r', encoding='utf-8') as file:
        data = json.load(file)
        for entry in data:
            if entry[0]['score'] >= 0.8:
                count+=1
    print(f'{num}',f'{path}',f'{format}', count/50)

def secondBetter(num, path, format):
    return

#top2Plot()
#ratePlot()
#gapPlot()
#check()
