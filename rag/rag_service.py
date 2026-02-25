from .embedding import generate_embedding
from .vector_store import add_vector,search_vector
from spaceowner.models import AdvertisementSpace
import re
from .vector_store import reset_index

INDEX_READY = False
INDEXING = False

def ensure_index():
    global INDEX_READY, INDEXING

    if INDEX_READY or INDEXING:
        return

    INDEXING = True
    index_all_spaces()
    INDEX_READY = True
    INDEXING = False


def index_all_spaces():

    reset_index()

    spaces=AdvertisementSpace.objects.all()

    for space in spaces:
        text=f"{space.title} {space.description} {space.location}"

        embedding=generate_embedding(text)

        add_vector(embedding,space.id)

def extract_location_filter(query):
    query_lower=query.lower()

    all_locations=AdvertisementSpace.objects.values_list('location',flat=True)

    location_filter=None

    for location in all_locations:
        words=[w.strip() for w in location.lower().split(',')]

        for word in words:
            if word in query_lower:
                location_filter=word
                break

        if location_filter:
            break
        
    return location_filter


def extract_price_filter(query):

    query=query.lower()

    gt_match=re.search(r"(more than|above|greater than)\s*(\d+)",query)
    if gt_match:
        return {"type":"gt","value":int(gt_match.group(2))}


    lt_match=re.search(r"(less than|below|under)\s*(\d+)",query)
    if lt_match:
        return {"type":"lt","value":int(lt_match.group(2))}
    
    range_match=re.search(r"(between|from)\s*(\d+)\s*(and|to)\s*(\d+)",query)
    if range_match:
        return{
            "type":"range",
            "min":int(range_match.group(2)),
            "max":int(range_match.group(4))
        }
    
    return None

def rag_search(query):

    ensure_index()
    
    location_filter=extract_location_filter(query)
    price_filter=extract_price_filter(query)

    query_set=AdvertisementSpace.objects.all()

    if location_filter:
        query_set=query_set.filter(location__icontains=location_filter)

    if price_filter:
        if price_filter["type"]=="gt":
            query_set=query_set.filter(price__gt=price_filter["value"])
        
        elif price_filter["type"]=="lt":
            query_set=query_set.filter(price__lt=price_filter["value"])
        
        elif price_filter["type"]=="range":
            query_set=query_set.filter(
                price__gte=price_filter["min"],
                price__lte=price_filter["max"]
            )

    if not query_set.exists():
        return []

    query_embedding=generate_embedding(query)
    space_ids=search_vector(query_embedding)

    filtered_ids=list(query_set.values_list("id",flat=True))

    ordered_id=[i for i in space_ids if i in filtered_ids]

    if not ordered_id:
        ordered_id=filtered_ids

    ordered_space=sorted(
        AdvertisementSpace.objects.filter(id__in=ordered_id).prefetch_related('images'),
        key=lambda x:ordered_id.index(x.id)
    )
    return ordered_space