class MessageTreeTraversal(object):
    """Traverses the secret message tree, grabbing all of its juicy secrets."""
    def __init__(self, root_id, nodes):
        self.nodes = nodes
        self.root_id = root_id

    def get_message(self):
        result = []
        q = self.nodes['start']
        v = set()

        while len(q) != 0:
            current_id = q.pop(0)

            if current_id in v:
                continue
            else:
                v.add(current_id)

            current_node = self.nodes[current_id]

            if 'secret' in current_node and current_node['secret'] != u'':
                result.append(current_node['secret'])

            if 'next' in current_node:
                if type(current_node['next']) is list:
                    q.extend(current_node['next'])
                else:
                    q.append(current_node['next'])
        
        return "".join(result)
