
class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data


class AVLTree:

    def __init__(self):
        self._root = None

    # ── Internal book-keeping ─────────────────────────────────────────────

    def _h(self, node):
        return node._avl_height if node else 0

    def _bf(self, node):
        return self._h(node._avl_left) - self._h(node._avl_right) if node else 0

    def _update(self, node):
        node._avl_height = 1 + max(self._h(node._avl_left), self._h(node._avl_right))

    def _init(self, node):
        """Attach AVL metadata to a node the first time it's inserted."""
        if not hasattr(node, '_avl_height'):
            node._avl_height = 1
            node._avl_left = None
            node._avl_right = None

    # ── Rotations ─────────────────────────────────────────────────────────

    def _rotate_right(self, z):
        y = z._avl_left
        z._avl_left = y._avl_right
        y._avl_right = z
        self._update(z)
        self._update(y)
        return y

    def _rotate_left(self, z):
        y = z._avl_right
        z._avl_right = y._avl_left
        y._avl_left = z
        self._update(z)
        self._update(y)
        return y

    def _rebalance(self, node):
        self._update(node)
        bf = self._bf(node)
        if bf > 1:
            if self._bf(node._avl_left) < 0:
                node._avl_left = self._rotate_left(node._avl_left)
            return self._rotate_right(node)
        if bf < -1:
            if self._bf(node._avl_right) > 0:
                node._avl_right = self._rotate_right(node._avl_right)
            return self._rotate_left(node)
        return node

    # ── Recursive helpers ─────────────────────────────────────────────────

    def _insert(self, root, node):
        if root is None:
            return node
        if node.key < root.key:
            root._avl_left = self._insert(root._avl_left, node)
        elif node.key > root.key:
            root._avl_right = self._insert(root._avl_right, node)
        else:
            # Replace on duplicate key, preserve tree links
            node._avl_left = root._avl_left
            node._avl_right = root._avl_right
            node._avl_height = root._avl_height
            return node
        return self._rebalance(root)

    def _delete(self, root, key):
        if root is None:
            return None
        if key < root.key:
            root._avl_left = self._delete(root._avl_left, key)
        elif key > root.key:
            root._avl_right = self._delete(root._avl_right, key)
        else:
            if root._avl_left is None:
                return root._avl_right
            if root._avl_right is None:
                return root._avl_left
            successor = self._min_node(root._avl_right)
            root._avl_right = self._delete(root._avl_right, successor.key)
            successor._avl_left = root._avl_left
            successor._avl_right = root._avl_right
            successor._avl_height = root._avl_height
            root = successor
        return self._rebalance(root)

    def _search(self, root, key):
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self._search(root._avl_left, key)
        return self._search(root._avl_right, key)

    def _min_node(self, node):
        while node._avl_left:
            node = node._avl_left
        return node

    def _inorder(self, node, result):
        if node:
            self._inorder(node._avl_left, result)
            result.append(node)
            self._inorder(node._avl_right, result)

    # ── Public API ────────────────────────────────────────────────────────

    def insert(self, node):
        """Insert a node object (must have a .key attribute)."""
        self._init(node)
        self._root = self._insert(self._root, node)

    def delete(self, key):
        """Remove the node with the given key."""
        self._root = self._delete(self._root, key)

    def search(self, key):
        """Return the node with the given key, or None."""
        return self._search(self._root, key)

    def inorder(self):
        """Return all nodes in sorted key order."""
        result = []
        self._inorder(self._root, result)
        return result

    def min(self):
        if not self._root:
            raise ValueError("Tree is empty")
        return self._min_node(self._root)

    def max(self):
        if not self._root:
            raise ValueError("Tree is empty")
        node = self._root
        while node._avl_right:
            node = node._avl_right
        return node

    def __len__(self):
        return len(self.inorder())

    def __contains__(self, key):
        return self.search(key) is not None
    
def hash_str_to_int(input_str:str):
    accumulator  = 0
    norm_str = input_str.lower()
    for iteration,i in enumerate(norm_str):
        accumulator += ord(i) << (iteration * 8)
    print(accumulator )
    return accumulator 
