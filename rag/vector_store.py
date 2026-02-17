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
    vec=np.array([query_vector]).astype("float32")
    distance,indices=index.search(vec,k)
    return [id_map[i] for i in indices[0] if i < len(id_map)]