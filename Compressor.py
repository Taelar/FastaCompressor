from BloomFilter import BloomFilter
from Reader import readFile
import utils
import pickle
import gzip
import re
import argparse

parser = argparse.ArgumentParser(description="Compress a .fasta file.")
parser.add_argument("fasta", type=str, nargs=1, help="path to fasta file")
parser.add_argument("--graph", type=str, nargs=1, default=[""], help="path to compressed graph")
parser.add_argument("--output", type=str, nargs=1, default=[""], help="path of output file")
parser.add_argument("--kmer_size", type=int, nargs=1, default=[20], help="Kmer size")
parser.add_argument("--bloom_size", type=int, nargs=1, default=[1000000], help="Bloom Filter size")
parser.add_argument("--bloom_hash", type=int, nargs=1, default=[7], help="Number of hashing functions used")
args = parser.parse_args()


def compress(b_filter: BloomFilter, kmer_size: int, path: str, output_path: str, graph_path: str):
    # Retrieve file name and erase potential extension
    target_path = re.search("[\w/]+", path).group(0)

    # Compress De Bruijn Graph
    if graph_path == "":
        graph_path = target_path + ".graph.pgz"
    pickle.dump(b_filter, gzip.open(graph_path, "wb"))

    # Create/Open compress file
    if output_path == "":
        output_path = target_path + ".comp"
    target_file = open(output_path, "w")

    with open(target_path + ".fasta", "r") as in_file:
        for line in in_file:
            # Clear final \n
            line = line.rstrip()

            if not line.startswith(">"):
                # comp_line is computed during the incoming loop then wrote into the file
                comp_line = line[0:kmer_size] + ' '

                limit = len(line) - kmer_size
                ind = 0

                while ind < limit:
                    ambiguity_found = False

                    # Current kmer bounds
                    begin = ind
                    end = begin + kmer_size
                    kmer = line[begin:end]

                    # k_char takes value of the first char after kmer
                    k_char = line[end]

                    neighbors = utils.getNeighbors(kmer)

                    for neigh in neighbors:
                        # If a possible neighbor exists in Bloom Filter and is different from actual neighbor,
                        # the situation is "ambiguous" and requires the right char to be written into compress file
                        if b_filter.exists(utils.canonical(neigh)) and (neigh[-1] != k_char):
                            ambiguity_found = True

                    if ambiguity_found:
                        comp_line += k_char

                    ind += 1

                # Write computed line into compress file
                comp_line += '\n'
                target_file.write(comp_line)

    target_file.close()


# Retrieve args
b_size = args.bloom_size[0]
b_hash = args.bloom_hash[0]
k_size = args.kmer_size[0]
fasta = args.fasta[0]
graph = args.graph[0]
output = args.output[0]

# Process
bloom_filter = readFile(fasta, b_size, b_hash, k_size)
compress(bloom_filter, k_size, fasta, output, graph)
