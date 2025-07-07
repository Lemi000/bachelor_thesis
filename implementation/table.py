#create look up table for model name and path

import json

with open('dataset/table.json', mode='w', encoding='utf-8') as output_file:
    output_data = []

    #free models
    data = {'name': "META_LLAMA_32_1B_FREE",
            'code': "meta-llama/llama-3.2-1b-instruct:free",
            'path': "llama_32_1b_free"}
    output_data.append(data)

    data = {'name': "META_LLAMA_32_3B_FREE",    #logprobs
            'code': "meta-llama/llama-3.2-3b-instruct:free",
            'path': "llama_32_3b_free"}
    output_data.append(data)

    data = {'name': "META_LLAMA_31_8B_FREE",
            'code': "meta-llama/llama-3.1-8b-instruct:free",
            'path': "llama_31_8b_free"}
    output_data.append(data)

    data = {'name': "META_LLAMA_33_8B_FREE",
            'code': "meta-llama/llama-3.3-8b-instruct:free",
            'path': "llama_33_8b_free"}
    output_data.append(data)

    data = {'name': "META_LLAMA_32_11B_VISION_FREE",
            'code': "meta-llama/llama-3.2-11b-vision-instruct:free",
            'path': "llama_32_11b_vision_free"}
    output_data.append(data)

    data = {'name': "META_LLAMA_33_70B_FREE",
            'code': "meta-llama/llama-3.3-70b-instruct:free",
            'path': "llama_33_70b_free"}
    output_data.append(data)

    #non-free models
    data = {'name': "META_LLAMA_32_3B",
            'code': "meta-llama/llama-3.2-3b-instruct",
            'path': "llama_32_3b"}
    output_data.append(data)

    data = {'name': "META_LLAMA_31_8B",
            'code': "meta-llama/llama-3.1-8b-instruct",
            'path': "llama_31_8b"}
    output_data.append(data)

    data = {'name': "META_LLAMA_31_70B",
            'code': "meta-llama/llama-3.1-70b-instruct",
            'path': "llama_31_70b"}
    output_data.append(data)

    data = {'name': "META_LLAMA_31_405B",
            'code': "meta-llama/llama-3.1-405b-instruct",
            'path': "llama_31_405b"}
    output_data.append(data)

    json.dump(output_data, output_file, indent=4)