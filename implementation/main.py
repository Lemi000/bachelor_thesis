import json
from prompt import sample
from average import average
from cluster import cluster
from evaluate import evaluate
from evaluate import perse
from plot import first
from plot import gapPlot
from plot import gapAlpha

def main(num, model_name, format):
    with open ('dataset/table.json', mode='r', encoding='utf-8') as table:
        data = json.load(table)
        for entry in data:
            if model_name == entry['name']:
                code = entry['code']
                path = entry['path']
                #sample(num, code, path, format)
                #average(num, path, format)
                #cluster(num, path, format)
                #evaluate(num, path, format)
                #perse(num, path, format)
                #first(num, path, format)
                gapPlot(num, path, format)
                #gapAlpha(num,path,format)
                break

'''main(26, "META_LLAMA_32_3B", "")
main(50, "META_LLAMA_32_3B", "")
main(176, "META_LLAMA_32_3B", "")
main(264, "META_LLAMA_32_3B", "")
main(26, "META_LLAMA_31_8B", "")
main(50, "META_LLAMA_31_8B", "")
main(176, "META_LLAMA_31_8B", "")
main(264, "META_LLAMA_31_8B", "")
main(26, "META_LLAMA_31_70B", "")
main(50, "META_LLAMA_31_70B", "")
main(176, "META_LLAMA_31_70B", "")
main(264, "META_LLAMA_31_70B", "")
main(26, "META_LLAMA_31_405B", "")
main(50, "META_LLAMA_31_405B", "")
main(176, "META_LLAMA_31_405B", "")
main(264, "META_LLAMA_31_405B", "")

main(26, "META_LLAMA_32_3B", ".x")
main(50, "META_LLAMA_32_3B", ".x")
main(176, "META_LLAMA_32_3B", ".x")
main(264, "META_LLAMA_32_3B", ".x")
main(26, "META_LLAMA_31_8B", ".x")
main(50, "META_LLAMA_31_8B", ".x")
main(176, "META_LLAMA_31_8B", ".x")
main(264, "META_LLAMA_31_8B", ".x")
main(26, "META_LLAMA_31_70B", ".x")
main(50, "META_LLAMA_31_70B", ".x")
main(176, "META_LLAMA_31_70B", ".x")
main(264, "META_LLAMA_31_70B", ".x")
main(26, "META_LLAMA_31_405B", ".x")
main(50, "META_LLAMA_31_405B", ".x")
main(176, "META_LLAMA_31_405B", ".x")
main(264, "META_LLAMA_31_405B", ".x")'''

main(264, "META_LLAMA_32_3B", "")
main(264, "META_LLAMA_32_3B", ".x")
main(264, "META_LLAMA_31_8B", "")
main(264, "META_LLAMA_31_8B", ".x")
main(264, "META_LLAMA_31_70B", "")
main(264, "META_LLAMA_31_70B", ".x")
main(264, "META_LLAMA_31_405B", "")
main(264, "META_LLAMA_31_405B", ".x")