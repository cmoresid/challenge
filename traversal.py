"""Encapsulates secret message tree traversal approaches."""

class MessageTreeTraversal(object):
    """Traverses the secret message tree, grabbing all of its juicy secrets."""
    def __init__(self, root_id, nodes):
        self.nodes = nodes
        self.root_id = root_id

    def get_message(self):
        """
        Performs a breadth first traversal over tree in order to retrieve
        the secret message.
        """
        result = []
        queue = self.nodes['start']
        visited = set()

        while not queue:
            current_id = queue.pop(0)

            if current_id in visited:
                continue
            else:
                visited.add(current_id)

            current_node = self.nodes[current_id]

            if 'secret' in current_node and current_node['secret'] != u'':
                result.append(current_node['secret'])

            if 'next' in current_node:
                if isinstance(current_node['next'], list):
                    queue.extend(current_node['next'])
                else:
                    queue.append(current_node['next'])

        return "".join(result)
