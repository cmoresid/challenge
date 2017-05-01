"""Contains main driver logic."""

import time

from threading import Lock
from Queue import Queue
from api_request import ChallengeApi
from worker import DownloadMessageTreeWorker
from traversal import MessageTreeTraversal

# Number of threads to spin up to help build
# the tree
NUM_OF_THREADS = 10
# Number of seconds between spinning up new threads.
SLEEP_SECS = 5

def download_tree():
    """Download the secret message tree from the API using multiple threads."""
    queue = Queue()
    visited = set()
    nodes = {}
    vlock = Lock()
    nlock = Lock()
    api = ChallengeApi()

    session_id = api.get_session()
    root_id, children = api.get_start(session_id)
    nodes[root_id] = children

    if isinstance(children, list):
        for child_id in children:
            queue.put(child_id)
    else:
        queue.put(children)

    print '\tSpawning %s threads ...' % (NUM_OF_THREADS,)
    for _ in range(NUM_OF_THREADS):
        worker = DownloadMessageTreeWorker(api, session_id, queue, visited, \
                                           nodes, vlock, nlock)
        worker.daemon = True
        worker.start()
        time.sleep(SLEEP_SECS)

    queue.join()

    return nodes

if __name__ == "__main__":
    print 'Downloading tree ...'
    tree_nodes = download_tree()
    print 'Building secret message from tree ...'
    tree_traversal = MessageTreeTraversal('start', tree_nodes)
    print '\nSecret Message: %s\n' % (tree_traversal.get_message(),)
