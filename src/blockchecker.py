import requests 
import operator

def get_faulty_nodes():

    faulty_nodes = {}

    # Get list of pools
    r = requests.get(url='https://raw.githubusercontent.com/turtlecoin/turtlecoin-pools-json/master/turtlecoin-pools.json')

    pools = []

    pool_stats = {}

    for pool in r.json():
        pool_name = pool
        pool_api = r.json()[pool]['url']
        api_command = pool_api + "stats"

        try:
             re = requests.get(url=api_command)
             pool_stats[pool] = re.json()['network']

        except:
             print("Cannot connect to " + pool)
             continue

    block_heights = {}
    pool_stats['z-pool.com'] = {'timestamp': 1521833885, 'height': 289595, 'reward': 2954626, 'hash': '41d0910d028f2eee9fb8354970477092ced618b087250ce8f7c36ab26cdcae1d', 'difficulty': 345465105}
    for pool in pool_stats:
        height = pool_stats[pool]['height']
        if height not in block_heights:
            block_heights[height] = 1
        else:
            block_heights[height] += 1
    correct_height = sorted(block_heights.items(), key=operator.itemgetter(1))[-1][0]

    for pool in pool_stats:
        if ( correct_height - pool_stats[pool]['height'] ) > 5:
            faulty_nodes[pool] = pool_stats[pool]['height']

    return faulty_nodes
