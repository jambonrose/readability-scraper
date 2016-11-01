import json
from itertools import chain

with open('links.json', 'r') as fp:
    data = json.loads(fp.read())

flat_chain_list = chain(*[chain(*page_dict.values()) for page_dict in data])

with open('links.txt', 'w') as fp:
    fp.write('\n'.join(flat_chain_list))
