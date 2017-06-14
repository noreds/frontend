from pymongo import MongoClient
import os
import json

client = MongoClient('mongodb://localhost:27017/')
imported_db = client['news']
imported_collection = imported_db['imported']

imported_news = 'imported'

all_tags_with_items = {}


def query_all_items():
    all_items = []
    all_items_cursor = imported_collection.find({'item.text_en': {'$exists': True}})

    for item in all_items_cursor:
        all_items.append(item)

    return all_items


def cluster_items(all_items):
    items = {}

    for d in all_items:
        item_tags = {}
        for entity in d['item']['metadata']['entities']:
            if entity['type'] != 'XMN-TAG':
                entity_uri = entity['uri']
                #print(entity['label'])
                #print(entity['score'])

                # tags appear more than once on an item - we count the first one here
                if not item_tags.get(entity_uri, False):
                    item_tags[entity_uri] = entity

                    if not all_tags_with_items.get(entity_uri, False):
                        all_tags_with_items[entity_uri] = {
                            'label': entity['label'],
                            'items': [d['item']['fullText']]}
                    else:
                        all_tags_with_items[entity_uri]['items'].append(d['item']['fullText'])

                # append to item overview
                if not items.get(d['_id'], False):
                    items[d['_id']] = {'tags': item_tags,
                                       'item': d}

    ## clustering by tags

    from numpy import array
    from scipy.cluster.vq import vq, kmeans2, whiten

    all_bin_tags = []

    for item in list(items.values()):
        # print(item)
        binary_tags = [1 if x in item['tags'] else 0 for x in all_tags_with_items.keys()]
        # print(binary_tags)
        print('items bin tags: %s' % len(binary_tags))
        all_bin_tags.append(binary_tags)

    print('len of all items: %s ' % len(all_bin_tags))

    features = array(all_bin_tags)
    whitened = whiten(features)

    # book = array((whitened[0],whitened[2]))  # should be the k guess (fixed to 20 because was 2)

    centroids, labels = kmeans2(whitened, 200)
    print(labels)
    clustered = {}

    for num in range(len(labels)):
        label = labels[num]
        if not clustered.get(label, False):
            clustered[label] = [list(items.values())[num]]
        else:
            clustered[label].append(list(items.values())[num])
    return clustered

items = query_all_items()
clustered_items = cluster_items(items)
