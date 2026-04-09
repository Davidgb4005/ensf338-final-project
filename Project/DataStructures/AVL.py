import sys
import os
from typing import TypeVar, Generic, Optional
T = TypeVar("T")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Node(Generic[T]):
    def __init__(self, key: int, data: T) -> None:
        self.key = key
        self.data = data
        # moved the avl height, left, and right stuff here for simplicity
        self.avl_height: int = 1
        self.avl_left: Optional[Node[T]] = None
        self.avl_right: Optional[Node[T]] = None

class AVLTree(Generic[T]):
    def __init__(self) -> None:
        self._root: Optional[Node[T]] = None

    # ── Internal book-keeping ─────────────────────────────────────────────

    def _height(self, node: Optional[Node[T]]) -> int: 
        if node is not None:
                return node.avl_height
        else:
            return 0

    def _balanceFactor(self, node: Optional[Node[T]]) -> int:
        if node is not None:
            return (self._height(node.avl_left) - self._height(node.avl_right)) 
        else:
            return 0

    def _update(self, node: Node[T]) -> None:
        node.avl_height = 1 + max(self._height(node.avl_left), self._height(node.avl_right))

    # ── Rotations ─────────────────────────────────────────────────────────

    def _rotate_right(self, subRoot: Node[T]) -> Node[T]:
        pivot = subRoot.avl_left
        if pivot is not None:
            subRoot.avl_left = pivot.avl_right
            pivot.avl_right = subRoot
            self._update(subRoot)
            self._update(pivot)
            return pivot
        else:
            return subRoot

    def _rotate_left(self, subRoot: Node[T]) -> Node[T]:
        pivot = subRoot.avl_right
        if pivot is not None:
            subRoot.avl_right = pivot.avl_left
            pivot.avl_left = subRoot
            self._update(subRoot)
            self._update(pivot)
            return pivot
        else:
            return subRoot
        

    def _rebalance(self, node: Node[T]) -> Node[T]:
        self._update(node)
        bf = self._balanceFactor(node)
        if bf > 1 and node.avl_left is not None: #check if not none. technically no way it can be None but pylance is reporting an issue
            if self._balanceFactor(node.avl_left) < 0:
                node.avl_left = self._rotate_left(node.avl_left)
            return self._rotate_right(node)
        if bf < -1 and node.avl_right is not None:
            if self._balanceFactor(node.avl_right) > 0:
                node.avl_right = self._rotate_right(node.avl_right)
            return self._rotate_left(node)
        return node

    # ── Recursive helpers ─────────────────────────────────────────────────

    def _insert(self, root: Optional[Node[T]], node: Node[T]) -> Node[T]:
        if root is None:
            return node
        if node.key < root.key:
            root.avl_left = self._insert(root.avl_left, node)
        elif node.key > root.key:
            root.avl_right = self._insert(root.avl_right, node)
        else:
            # Replace on duplicate key, preserve tree links
            node.avl_left = root.avl_left
            node.avl_right = root.avl_right
            node.avl_height = root.avl_height
            return node
        return self._rebalance(root)

    def _delete(self, root: Optional[Node[T]], key: int) -> None | Node[T]:
        if root is None:
            return None
        if key < root.key:
            root.avl_left = self._delete(root.avl_left, key)
        elif key > root.key:
            root.avl_right = self._delete(root.avl_right, key)
        else:
            if root.avl_left is None:
                return root.avl_right
            if root.avl_right is None:
                return root.avl_left
            successor = self._min_node(root.avl_right)
            root.avl_right = self._delete(root.avl_right, successor.key)
            successor.avl_left = root.avl_left
            successor.avl_right = root.avl_right
            successor.avl_height = root.avl_height
            root = successor
        return self._rebalance(root)

    def _search(self, root: Optional[Node[T]], key: int) -> None | Node[T]:
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self._search(root.avl_left, key)
        return self._search(root.avl_right, key)

    def _min_node(self, node: Node[T]) -> Node[T]:
        while node.avl_left:
            node = node.avl_left
        return node

    def _inorder(self, node: Optional[Node[T]], result: list[Node[T]]) -> None:
        if node:
            self._inorder(node.avl_left, result)
            result.append(node)
            self._inorder(node.avl_right, result)

    # ── Public API ────────────────────────────────────────────────────────

    def insert(self, node: Node[T]) -> None:
        """Insert a node object (must have a .key attribute)."""
        self._root = self._insert(self._root, node)

    def delete(self, key: int) -> None:
        """Remove the node with the given key."""
        self._root = self._delete(self._root, key)

    def search(self, key: int) -> None | Node[T]:
        """Return the node with the given key, or None."""
        return self._search(self._root, key)

    def inorder(self) -> list[Node[T]]:
        """Return all nodes in sorted key order."""
        result: list[Node[T]] = []
        self._inorder(self._root, result)
        return result

    def min(self) -> Node[T]:
        if not self._root:
            raise ValueError("Tree is empty")
        return self._min_node(self._root)

    def max(self) -> Node[T]:
        if not self._root:
            raise ValueError("Tree is empty")
        node = self._root
        while node.avl_right:
            node = node.avl_right
        return node

    def __len__(self) -> int:
        return len(self.inorder())

    def __contains__(self, key: int) -> bool:
        return self.search(key) is not None
    
def hash_str_to_int(input_str:str) -> int:
    accumulator  = 0
    norm_str = input_str.lower()
    for iteration,i in enumerate(norm_str):
        accumulator += ord(i) << (iteration * 8)
    print(accumulator)
    return accumulator 
