from threading import Thread

class DownloadMessageTreeWorker(Thread):
    def __init__(self, api, session_id, queue, visited, nodes, vlock, nlock):
        Thread.__init__(self)
        self.queue = queue
        self.vlock = vlock
        self.nlock = nlock
        self.nodes = nodes
        self.visited = visited
        self.session_id = session_id
        self.api = api
    
    def run(self):
        while not self.queue.empty():
            next_id = self.queue.get()

            if self.__has_been_visited(next_id):
                continue
        
            next_r = self.__get_next(next_id)

            self.__add_children_to_queue(next_r)
            self.__add_node(next_r)
            
            self.queue.task_done()

    def __has_been_visited(self, next_id):
        with self.vlock:
            if next_id in self.visited:
                return True
            else:
                self.visited.add(next_id)
                return False

    def __get_next(self, next_id):
        return { k.lower() : v for k, v, in self.api.get_next(next_id, self.session_id).items() }

    def __add_node(self, next_r):
        with self.nlock:
            self.nodes[next_r['id']] = next_r

    def __add_children_to_queue(self, next_r):
        if not 'next' in next_r:
            return
        
        if type(next_r['next']) is list:
            for n in next_r['next']:
                self.queue.put(n)
        else:
            self.queue.put(next_r['next'])
