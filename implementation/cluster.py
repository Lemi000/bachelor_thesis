#cluster in set, clusters in list, edge in set, edges in list

def cluster(C, E):
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

def make_graph():
    