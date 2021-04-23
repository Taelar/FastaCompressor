class BitArray:
    def __init__(self, n: int):
        self.size_octet = 1 + (n // 8)
        self.array = bytearray(self.size_octet)

    def get_offset(self, i: int) -> int:
        return i // 8

    def get_position(self, i: int) -> int:
        return i % 8

    def set_i(self, i: int):
        offset = self.get_offset(i)
        pos = self.get_position(i)
        mask = 1 << pos
        byte = self.array[offset]
        self.array[offset] = byte | mask

    def exists(self, i: int) -> bool:
        offset = self.get_offset(i)
        pos = self.get_position(i)
        mask = 1 << pos
        byte = self.array[offset]
        return (byte & mask) > 0


