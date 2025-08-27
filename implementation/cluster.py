import numpy as np
import hdbscan
import json
from bert_score import BERTScorer
from itertools import combinations
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity

#cluster in set, clusters in list, edge in set, edges in list
def myCluster(C, E):
    while len(E) > 0:
        edge = E.pop(0)
        ele = list(edge)[0]
        ele2 = list(edge)[1]
        cluster = None
        cluster2 = None
        for entry in C:
            if ele in entry:
                cluster = entry
            if ele2 in entry:
                cluster2 = entry
        
        no_edge = False #no edge between two complete graphs
        for v in cluster:
            if no_edge:
                break
            for v2 in cluster2:
                if no_edge:
                    break
                to_check = {v,v2}
                exist = False   #edge between two verticies
                if to_check != edge:
                    for checked in E:
                        if to_check == checked:
                            E.remove(checked)
                            exist = True
                            break
                else:   #edge being checked is the popped edge
                    exist = True
                
                if exist:
                    continue
                else:
                    no_edge = True
        
        if not no_edge:
            new_cluster = cluster | cluster2
            C.remove(cluster)
            C.remove(cluster2)
            C.append(new_cluster)


def hdbCluster():
    words = ["Bank.", "bank", "bench", "cheese"]
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(words, normalize_embeddings=True)
    similarity_matrix = cosine_similarity(embeddings)
    distance_matrix = 1 - similarity_matrix
    distance_matrix = distance_matrix.astype(np.float64)
    clusterer = hdbscan.HDBSCAN(metric='precomputed', min_cluster_size=2, cluster_selection_epsilon=0.2)
    labels = clusterer.fit_predict(distance_matrix)
    print(labels)
    print(clusterer.probabilities_)


def dataToGraph(num, path, format):
    with open(f'outputs/P{num}.{path}.ave{format}.json', mode='r', encoding='utf-8') as input_file:
        input_data = json.load(input_file)
        for entry in input_data:
            #answer = entry['answer']
            guesses = entry['guesses']
            guess_list = [g['guess'] for g in guesses]
            result = [set(p) for p in combinations(guess_list, 2)]
            result = list(filter(lambda x: getScore(list(x)[0], list(x)[1]) >= 0.8, result))
            result = sorted(result, key=lambda x: getScore(list(x)[0], list(x)[1]), reverse=True)
            #continue...

def getScore(a, b):
    scorer = BERTScorer(model_type='bert-base-uncased')
    P, R, F1 = scorer.score([a], [b])
    return F1.mean().item()


def agglo(words):
    # Input words
    #words = ['Leonard Bernstein', 'Fannie Hurst', 'Nikolai G', 'F. Scott Fitzgerald', 'F. C. J', 'Leonard Bernstein, with']

    # Normalize words
    # maybe like punctation and so on

    # Load a good general-purpose embedding model
    #model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder="implementation/hf_models")
    model = SentenceTransformer("implementation/hf_models/models--sentence-transformers--all-MiniLM-L6-v2/snapshots/c9745ed1d9f207416be6d2e6f8de32d1f16199bf")

    # Get embeddings directly for words
    embeddings = model.encode(words, normalize_embeddings=True)

    # Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(embeddings)

    # Convert similarity to distance
    distance_matrix = 1 - similarity_matrix

    # Agglomerative clustering
    clustering = AgglomerativeClustering(
        metric='precomputed',
        linkage='average',
        distance_threshold=0.2,  # adjust for stricter/looser grouping 0.3>
        n_clusters=None
    )
    labels = clustering.fit_predict(distance_matrix)
    return labels

    # Group and print clusters
    clusters = {}
    for original_word, label in zip(words, labels):
        clusters.setdefault(label, []).append(original_word)
    for cid, wlist in clusters.items():
        print(f"Cluster {cid}: {wlist}")

def cluster(num, path, format):
    with open(f'outputs/P{num}.{path}.ave{format}.json', mode='r', encoding='utf-8') as input_file:
        data = json.load(input_file)
        for i, entry in enumerate(data):
            guesses = entry['guesses']
            guess_list = [g['guess'] for g in guesses]
            if len(guess_list) > 1:
                clusters = {}
                labels = agglo(guess_list)
                for original_word, label in zip(guesses, labels):
                    clusters.setdefault(label, []).append(original_word)
                clusters = list(clusters.values())
                if len(clusters) > 1:
                    clusters = sorted(clusters, key=lambda x: x[0]['probability'], reverse=True)[:2]
            else:
                clusters = [guesses]
            
            data[i]['guesses'] = clusters
        with open(f'outputs/P{num}.{path}.top2{format}.json', mode='w', encoding='utf-8') as output_file:
            json.dump(data, output_file, indent=4)
