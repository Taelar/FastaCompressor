from BloomFilter import BloomFilter
import utils
import re


def readFile(path: str, filter_size: int, hash_k: int, kmer_size: int) -> BloomFilter:
    # Retrieve file name and erase potential extension and add ".fasta" (secure input)
    target_path = re.search("[\w/]+", path).group(0) + ".fasta"

    # Initialise Bloom Filter
    bloom_filter = BloomFilter(filter_size, hash_k)
    with open(target_path, "r") as in_file:
        for line in in_file:
            # Clear final \n
            line = line.rstrip()
            if not line.startswith(">"):
                ind = 0
                limit = len(line) - kmer_size

                # Add each kmer of current read to Bloom Filter
                while ind <= limit:
                    kmer = line[ind:ind + kmer_size]
                    bloom_filter.add(utils.canonical(kmer))
                    ind += 1

    return bloom_filter
