import json
from promptOpenrouter import sample
from average import average
from evaluate import bertscore


def main(num, model_name):
    with open ('dataset/table.json', mode='r', encoding='utf-8') as table:
        data = json.load(table)
        for entry in data:
            if model_name == entry['name']:
                code = entry['code']
                path = entry['path']
                #sample(num, code, path)
                #average(num, path)
                bertscore(num, path)
                break

'''main(26, "META_LLAMA_32_3B")
main(50, "META_LLAMA_32_3B")
main(176, "META_LLAMA_32_3B")
main(264, "META_LLAMA_32_3B")
main(26, "META_LLAMA_31_8B")
main(50, "META_LLAMA_31_8B")
main(176, "META_LLAMA_31_8B")
main(264, "META_LLAMA_31_8B")
main(26, "META_LLAMA_31_70B")
main(50, "META_LLAMA_31_70B")
main(176, "META_LLAMA_31_70B")
main(264, "META_LLAMA_31_70B")
main(26, "META_LLAMA_31_405B")
main(50, "META_LLAMA_31_405B")
main(176, "META_LLAMA_31_405B")
main(264, "META_LLAMA_31_405B")'''
