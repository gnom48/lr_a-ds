from .prefix_tree_node import PrefixTreeNode


class PrefixTree:
    def __init__(self):
        self.root: PrefixTreeNode = PrefixTreeNode()

    def add(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = PrefixTreeNode()
            node = node.children[char]
        node.word_end_flag = True

    def starts_with(self, prefix: str) -> list[str]:
        node = self.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        prompts = []
        self._recursion(prefix, node, prompts)
        return prompts

    def _recursion(self, current_word: str, node: PrefixTreeNode, prompts: list[str]):
        if node.word_end_flag:
            prompts.append(current_word)
        for char, child_node in node.children.items():
            self._recursion(current_word + char, child_node, prompts)

    def contains(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return False
        return node.word_end_flag
