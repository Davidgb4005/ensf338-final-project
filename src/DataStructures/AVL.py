import matplotlib.pyplot as plt
import BookingSystem.room_booking as rb
 
class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = []
        self.data.append(data)
 
 
class AVLTree:
    def __init__(self):
        self._root = None
 
    def _h(self, node):
        return node._avl_height if node else 0
 
    def _bf(self, node):
        return self._h(node._avl_left) - self._h(node._avl_right) if node else 0
 
    def _update(self, node):
        node._avl_height = 1 + max(self._h(node._avl_left), self._h(node._avl_right))
 
    def _init(self, node):
        if not hasattr(node, '_avl_height'):
            node._avl_height = 1
            node._avl_left = None
            node._avl_right = None
 
    def _rotate_right(self, z):
        y = z._avl_left
        z._avl_left = y._avl_right
        y._avl_right = z
        self._update(z)
        self._update(y)
        print("RHS Rotate")
        return y
 
    def _rotate_left(self, z):
        y = z._avl_right
        z._avl_right = y._avl_left
        y._avl_left = z
        self._update(z)
        self._update(y)
        print("LHS Rotate")
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
 
    def _insert(self, root, node):
        if root is None:
            return node

        if node.key < root.key:
            root._avl_left = self._insert(root._avl_left, node)
        elif node.key > root.key:
            root._avl_right = self._insert(root._avl_right, node)
        else:
            root.data.extend(node.data)
            return root

        return self._rebalance(root)
 
    def _delete(self, root, key, obj):
        if root is None:
            return None

        if key < root.key:
            root._avl_left = self._delete(root._avl_left, key, obj)

        elif key > root.key:
            root._avl_right = self._delete(root._avl_right, key, obj)

        else:
            # If obj is provided, remove only that specific entry
            if obj is not None:
                for i in root.data:
                    if obj is i.data:
                        root.data.remove(i)
                        break
                # Node still has other data — keep it in the tree
                if len(root.data) > 0:
                    return root

            # No data left (or obj is None = structural removal): remove this node
            if root._avl_left is None:
                return root._avl_right

            if root._avl_right is None:
                return root._avl_left

            # Two children: replace with in-order successor
            successor = self._min_node(root._avl_right)
            successor_key = successor.key

            # Remove successor structurally from the right subtree
            root._avl_right = self._delete(root._avl_right, successor_key, None)

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
 
    def insert(self, node):
        self._init(node)
        self._root = self._insert(self._root, node)
 
    def delete(self, key, object):
        self._root = self._delete(self._root, key, object)
 
    def search(self, key):
        node: Node = self._search(self._root, key)
        if node is None:
            return None
        for i in node.data:
            rb.print_daily_booking(i)
        return node
 
    def inorder(self):
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
 
 
    def _get_positions(self, node, depth=0, counter=None):
        if counter is None:
            counter = [0]
        if node is None:
            return {}
        pos = {}
        pos.update(self._get_positions(node._avl_left, depth + 1, counter))
        pos[node.key] = (counter[0], -depth)
        counter[0] += 1
        pos.update(self._get_positions(node._avl_right, depth + 1, counter))
        return pos
 
    def _get_edges(self, node, edges=None):
        if edges is None:
            edges = []
        if node is None:
            return edges
        if node._avl_left:
            edges.append((node.key, node._avl_left.key))
            self._get_edges(node._avl_left, edges)
        if node._avl_right:
            edges.append((node.key, node._avl_right.key))
            self._get_edges(node._avl_right, edges)
        return edges
 
    def _get_nodes(self, node, result=None):
        if result is None:
            result = []
        if node is None:
            return result
        result.append(node)
        self._get_nodes(node._avl_left, result)
        self._get_nodes(node._avl_right, result)
        return result
 
    def _draw_tree(self, ax, root, highlight_key=None, highlight_color="#2f9e44", title=""):
        ax.clear()
        ax.set_facecolor("#0f1117")
        ax.axis("off")
        ax.set_aspect("equal")
 
        if root is None:
            ax.text(0.5, 0.5, "empty tree", transform=ax.transAxes,
                    ha="center", va="center", color="#868e96", fontsize=11)
            ax.set_title(title, color="#adb5bd", fontsize=9, pad=6)
            return
 
        pos   = self._get_positions(root)
        edges = self._get_edges(root)
        nodes = self._get_nodes(root)
 
        xs  = [p[0] for p in pos.values()]
        ys  = [p[1] for p in pos.values()]
        pad = 1.4
        ax.set_xlim(min(xs) - pad, max(xs) + pad)
        ax.set_ylim(min(ys) - pad, max(ys) + pad * 0.5)
 
        NODE_R = 0.36
 
        for (pk, ck) in edges:
            px, py = pos[pk]
            cx, cy = pos[ck]
            dx, dy = cx - px, cy - py
            length = (dx**2 + dy**2) ** 0.5
            ux, uy = dx / length, dy / length
            x1, y1 = px + ux * NODE_R, py + uy * NODE_R
            x2, y2 = cx - ux * NODE_R, cy - uy * NODE_R
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="-|>", color="#495057",
                                        lw=1.2, mutation_scale=10))
 
        for node in nodes:
            x, y         = pos[node.key]
            is_highlight = (node.key == highlight_key)
            color        = highlight_color if is_highlight else "#3b5bdb"
 
            if is_highlight:
                ax.add_patch(plt.Circle((x, y), NODE_R + 0.1,
                                        color=color, alpha=0.25, zorder=2))
 
            ax.add_patch(plt.Circle((x, y), NODE_R, color=color, zorder=3,
                                    linewidth=1.5,
                                    edgecolor="white" if is_highlight else color))
 
            ax.text(x, y, str(hash_int_to_str(node.key)), ha="center", va="center",
                    fontsize=10, fontweight="bold", color="white", zorder=4)
 
            ax.text(x + NODE_R * 0.7, y + NODE_R * 0.7, f"h{node._avl_height}",
                    ha="center", va="center", fontsize=6, color="#868e96", zorder=4)
 
            lh = node._avl_left._avl_height  if node._avl_left  else 0
            rh = node._avl_right._avl_height if node._avl_right else 0
            bf = lh - rh
            bf_color = ("#2f9e44" if bf == 0 else "#f59f00" if abs(bf) == 1 else "#e03131")
            ax.text(x, y - NODE_R - 0.16, f"bf{bf:+d}",
                    ha="center", va="top", fontsize=6, color=bf_color, zorder=4)
 
        ax.set_title(title, color="#adb5bd", fontsize=9, pad=6)
 
    def insert_visu(self, node):
        fig, axes = plt.subplots(1, 3, figsize=(15, 6))
        fig.patch.set_facecolor("#0f1117")
        fig.suptitle(f"AVL Insert  ->  key = {node.key}",
                     color="#f1f3f5", fontsize=13, fontweight="bold", y=0.90)
 
        self._draw_tree(axes[0], self._root,
                        title=f"Before insert({node.key})")
 
        self._init(node)
        self._root = self._insert(self._root, node)
 
        self._draw_tree(axes[1], self._root,
                        highlight_key=node.key, highlight_color="#2f9e44",
                        title=f"Node {node.key} inserted  (green)")
 
        self._draw_tree(axes[2], self._root,
                        title=f"After rebalancing  (height={self._root._avl_height if self._root else 0})")
 
        fig.text(0.355, 0.5, "->", color="#74c0fc", fontsize=22,
                 ha="center", va="center", transform=fig.transFigure)
        fig.text(0.645, 0.5, "->", color="#74c0fc", fontsize=22,
                 ha="center", va="center", transform=fig.transFigure)
 
        plt.tight_layout()
        plt.show()
 
    def delete_visu(self, key, booking):
        fig, axes = plt.subplots(1, 3, figsize=(15, 6))
        fig.patch.set_facecolor("#0f1117")
        fig.suptitle(f"AVL Delete  ->  key = {key}",
                     color="#f1f3f5", fontsize=13, fontweight="bold", y=1.01)
 
        node_exists = self.search(key) is not None
 
        self._draw_tree(axes[0], self._root,
                        highlight_key=key if node_exists else None,
                        highlight_color="#e03131",
                        title=f"Before delete({key})  {'(red = target)' if node_exists else '(key not found)'}")
 
        if not node_exists:
            for ax in axes[1:]:
                self._draw_tree(ax, self._root, title=f"Key {key} not found - no change")
            plt.tight_layout()
            plt.show()
            return
 
        self._draw_tree(axes[1], self._root,
                        highlight_key=key, highlight_color="#e03131",
                        title=f"Removing node {key} ...")
 
        self._root = self._delete(self._root, key, booking)
 
        self._draw_tree(axes[2], self._root,
                        title=f"After rebalancing  (height={self._root._avl_height if self._root else 0})")
 
        fig.text(0.355, 0.5, "->", color="#74c0fc", fontsize=22,
                 ha="center", va="center", transform=fig.transFigure)
        fig.text(0.645, 0.5, "->", color="#74c0fc", fontsize=22,
                 ha="center", va="center", transform=fig.transFigure)
 
        plt.tight_layout()
        plt.show()
 
 
def hash_str_to_int(input_str: str):
    accumulator = 0
    norm_str = input_str.lower()
    for iteration, i in enumerate(norm_str):
        accumulator += ord(i) << (iteration * 8)
    return accumulator
 
 
def hash_int_to_str(hash_val: int):
    result = []
    i = 0
    while hash_val > 0:
        char_code = (hash_val >> (i * 8)) & 0xFF
        if char_code == 0:
            break
        result.append(chr(char_code))
        i += 1
    return "".join(result)
