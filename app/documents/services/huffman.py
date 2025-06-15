from __future__ import annotations

import heapq


class HuffmanNode:
    def __init__(
        self,
        frequency: int,
        data: str | None,
        left: HuffmanNode | None = None,
        right: HuffmanNode | None = None
    ) -> None:
        self.frequency = frequency
        self.data = data
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"<HuffmanNode: freq={self.frequency}, data={repr(self.data)}>"

    def __lt__(self, other: HuffmanNode) -> bool:
        return self.frequency < other.frequency


def generate_huffman_tree(mappings: dict[str, int]) -> HuffmanNode:
    # time complexity - O(nlogn) where n = len(mappings)
    # space complexity - O(n) where n = len(mappings)

    heap = [HuffmanNode(freq, char) for char, freq in mappings.items()]
    heapq.heapify(heap)  # build a min-heap

    while len(heap) > 1:
        first = heapq.heappop(heap)  # first smallest node
        second = heapq.heappop(heap)  # second smallest node
        merged_node = HuffmanNode(
            first.frequency + second.frequency, None, first, second
        )  # merges two nodes into a new internal one
        heapq.heappush(heap, merged_node)

    return heap[0]


def create_codes(
    node: HuffmanNode | None, bit_stream: str, codebook: dict[str, str]
) -> None:
    if node is None:
        return None

    # if node is a leaf, store the bit stream as its code
    if node.left is None and node.right is None:
        codebook[node.data] = bit_stream
        return None

    # traverse left and right subtrees
    create_codes(node.left, bit_stream + "0", codebook)
    create_codes(node.right, bit_stream + "1", codebook)


def encode(text: str) -> tuple[str, HuffmanNode | None]:
    if not text:
        return "", None

    frequency_map = generate_frequency_map(text)
    root = generate_huffman_tree(frequency_map)
    code_book = generate_codebook(root)
    encoded_text = ''.join(code_book[char] for char in text)

    return encoded_text, root


def generate_frequency_map(text: str) -> dict[str, int]:
    frequency_map = {}

    for char in text:
        frequency_map[char] = frequency_map.get(char, 0) + 1

    return frequency_map


def generate_codebook(root: HuffmanNode) -> dict[str, str]:
    codebook = {}
    create_codes(root, "", codebook)

    return codebook


def decode(encoded_text: str, root: HuffmanNode | None) -> str:
    if root is None:
        return ""

    decoded_text = ""
    current_node = root

    for bit in encoded_text:
        current_node = current_node.left if bit == "0" else current_node.right

        # if leaf node is reached, append character to result
        if current_node.left is None and current_node.right is None:
            decoded_text += current_node.data
            current_node = root  # restart for next character

    return decoded_text
