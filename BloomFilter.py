from BitArray import BitArray
import mmh3


class BloomFilter:

    def __init__(self, n: int, k: int):
        self.size = n
        self.array = BitArray(n)
        self.nb_hash = k

    def get_hash_values(self, w):
        hashes = []
        for i in range(self.nb_hash):
            hashes.append(mmh3.hash(w, i) % self.size)
        return hashes

    def add(self, w):
        hashes = self.get_hash_values(w)
        for h in hashes:
            self.array.set_i(h)

    def exists(self, w):
        hashes = self.get_hash_values(w)
        for h in hashes:
            if not self.array.exists(h):
                return False
        return True

    def __contains__(self, item):
        return self.exists(item)