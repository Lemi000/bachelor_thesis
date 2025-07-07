import pandas as pd
import matplotlib.pyplot as plt
import json

num = 26

#makes csv file with precision, recall and f1 for both 2 guesses
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


with open(f'evaluation/P{num}.llama_32_3b.x.json', mode='r', encoding='utf-8') as l3b_file, open(f'evaluation/P{num}.llama_31_8b.x.json', mode='r', encoding='utf-8') as l8b_file, open(f'evaluation/P{num}.llama_31_70b.x.json', mode='r', encoding='utf-8') as l70b_file, open(f'evaluation/P{num}.llama_31_405b.x.json', mode='r', encoding='utf-8') as l405b_file:
    l3b = json.load(l3b_file)
    l8b = json.load(l8b_file)
    l70b = json.load(l70b_file)
    l405b = json.load(l405b_file)

list3 = []  #list with 3b guess1 f1 values
list3_2 = []    #list with 3b guess2 f1 values (when no entry -> None)
list8 = []
list8_2 = []
list70 = []
list70_2 = []
list405 = []
list405_2 = []

model_list = [list3, list3_2, list8, list8_2, list70, list70_2, list405, list405_2]
model_name_list = ["3B 1", "3B 2", "8B 1", "8B 2", "70B 1", "70B 2", "405B 1", "405B 2"]

for a,b,c,d in zip(l3b, l8b, l70b, l405b):
    ag = a['guesses']
    bg = b['guesses']
    cg = c['guesses']
    dg = d['guesses']
    list3.append(ag[0]['f1'])
    list8.append(bg[0]['f1'])
    list70.append(cg[0]['f1'])
    list405.append(dg[0]['f1'])
    if len(ag) == 2:
        list3_2.append(ag[1]['f1'])
    else:
        list3_2.append(None)
    if len(bg) == 2:
        list8_2.append(bg[1]['f1'])
    else:
        list8_2.append(None)
    if len(cg) == 2:
        list70_2.append(cg[1]['f1'])
    else:
        list70_2.append(None)
    if len(dg) == 2:
        list405_2.append(dg[1]['f1'])
    else:
        list405_2.append(None)
    

#scatter plots of guess1 and guess2
def top2Plot():
    plt.scatter(range(1,51), list3, s=20, label="Top Prediction")
    plt.scatter(range(1,51), list3_2, s=20, label="Second Prediction")
    plt.title(f"P{num} Llama 3.2 3B:\nBERTScore F1 Evaluation of Top 2 Probable Predictions in QA Format")
    plt.xlabel("Question Index")
    plt.ylabel("F1 Score")
    plt.legend()
    #plt.show()
    plt.savefig(f'plot/top2/P{num}.llama_32_3b.x.png', dpi=300)


#bar plots of guess1 and guess2 with f1 bertscore >=0.8
def freqPlot():
    count = []
    for x in model_list:
        x = list(filter(lambda y: y is not None and y >= 0.8, x))
        count.append(len(x))

    plt.bar(model_name_list, count, color = ['red', 'red', 'orange', 'orange', 'green', 'green', 'blue', 'blue'])
    plt.title(f"P{num}; Frequency of Predictions with BERTScore F1 ≥ 0.8 in QA Format")
    plt.xlabel("Model Name")
    plt.ylabel("Frequency")
    plt.savefig(f'plot/freq/P{num}.x.png', dpi=300)


#bar plot on the number of f1 >=0.8 of guess1 depending on the gap of probabilities between guess1 and guess2
def gapPlot():
    x_axis = ["≤0.1","≤0.2","≤0.3","≤0.4","≤0.5","≤0.6","≤0.7","≤0.8","≤0.9","≤1"]
    count = [0,0,0,0,0,0,0,0,0,0] #count the number of guesses depending on the prob gap
    countf1 = [0,0,0,0,0,0,0,0,0,0]   #count the number of guesses wiht f1 >= 0.8 depending on the prob gap
    for entry, f1 in zip(l405b, list405):
        guesses = entry['guesses']
        prob1 = guesses[0]['probability']
        prob2 = guesses[1]['probability'] if len(guesses) == 2 else 0
        gap = prob1 - prob2

        if gap <= 0.1:
            count[0]+=1
            if f1 >= 0.8:
                countf1[0]+=1
        elif gap <= 0.2:
            count[1]+=1
            if f1 >= 0.8:
                countf1[1]+=1
        elif gap <= 0.3:
            count[2]+=1
            if f1 >= 0.8:
                countf1[2]+=1
        elif gap <= 0.4:
            count[3]+=1
            if f1 >= 0.8:
                countf1[3]+=1
        elif gap <= 0.5:
            count[4]+=1
            if f1 >= 0.8:
                countf1[4]+=1
        elif gap <= 0.6:
            count[5]+=1
            if f1 >= 0.8:
                countf1[5]+=1
        elif gap <= 0.7:
            count[6]+=1
            if f1 >= 0.8:
                countf1[6]+=1
        elif gap <= 0.8:
            count[7]+=1
            if f1 >= 0.8:
                countf1[7]+=1
        elif gap <= 0.9:
            count[8]+=1
            if f1 >= 0.8:
                countf1[8]+=1
        else:
            count[9]+=1
            if f1 >= 0.8:
                countf1[9]+=1
    y_axis = []
    for x, y in zip(count, countf1):
        y_axis.append(y/x if y != 0 else None)
    plt.scatter(x_axis, y_axis, color='blue')
    plt.title(f"P{num} Llama 3.1 405B: Proportion of Predictions with F1 ≥ 0.8 vs.\nTop-Second Probability Gap")
    plt.xlabel("Gap between Top and Second Prediction")
    plt.ylabel("Proportion of Predictions (F1 ≥ 0.8)")
    plt.savefig(f'plot/gap/P{num}.llama_31_405b.png', dpi=300)

top2Plot()
#freqPlot()
#gapPlot()