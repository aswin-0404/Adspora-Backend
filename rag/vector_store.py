import faiss
import numpy as np

dimension=384
index=faiss.IndexFlatL2(dimension)

id_map=[]

def add_vector(vector,obj_id):
    vec =np.array([vector]).astype("float32")
    index.add(vec)
    id_map.append(obj_id)

def search_vector(query_vector,k=3):
    if len(id_map) == 0:
        return []
    
    vec = np.array([query_vector]).astype("float32")
    distance, indices = index.search(vec, min(k, len(id_map)))
    return [id_map[i] for i in indices[0] if i < len(id_map)]

def reset_index():
    global index, id_map
    index.reset()
    id_map.clear()


