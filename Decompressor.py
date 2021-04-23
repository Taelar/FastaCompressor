import utils
import pickle
import gzip
import re
import argparse

parser = argparse.ArgumentParser(description="Compress a .fasta file.")
parser.add_argument("comp", type=str, nargs=1, help="path to compressed file")
parser.add_argument("--graph", type=str, nargs=1, default=[""], help="path to compressed graph")
parser.add_argument("--output", type=str, nargs=1, default=[""], help="path of output file")
args = parser.parse_args()


def decompress(path: str, graph_path: str, output_path: str):
    # Retrieve file name and erase potential extension
    target_path = re.search("[\w/]+", path).group(0)

    # Decompress Bloom Filter with pickle and gzip
    if graph_path == "":
        graph_path = target_path + ".graph.pgz"
    bloom_f = pickle.load(gzip.open(graph_path, "rb"))

    # Create/Open decompress file
    if output_path == "":
        output_path = target_path + ".fasta"
    target_file = open(output_path, "w")

    with open(target_path + ".comp", "r") as comp_file:
        i = 0

        for line in comp_file:
            decomp_line = ""

            # Clear final \n
            line = line.rstrip()

            # Retrieve first kmer using regex
            kmer = re.search("\w+", line).group(0)
            decomp_line += kmer

            # Calculate index of the first branching indication, i.e the first char after blank space
            line_index = len(kmer) + 1

            while len(decomp_line) < 100:
                kmer_found = 0
                candidate = ""

                neighbors = utils.getNeighbors(kmer)

                # Compute potential ambiguity
                for neigh in neighbors:
                    if bloom_f.exists(utils.canonical(neigh)):
                        kmer_found += 1
                        candidate = neigh

                # If ambiguity is found, use branching indications to take decision
                # Else candidate contains the only existing neighbor
                if kmer_found > 1:
                    added_char = line[line_index]
                    line_index += 1
                else:
                    added_char = candidate[-1]

                # Compute next kmer
                kmer = kmer[1:] + added_char
                decomp_line += added_char

            # Write decompressed line into file
            decomp_line = ">read " + str(i) + "\n" + decomp_line + "\n"
            target_file.write(decomp_line)
            i += 1


comp = args.comp[0]
graph = args.graph[0]
output = args.output[0]

decompress(comp, graph, output)
