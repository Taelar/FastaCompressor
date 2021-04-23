# Global constants definition
A = "A"
C = "C"
G = "G"
T = "T"


# Returns the reverse complement of the given string
def reverseComplement(data: str) -> str:
    result = ""
    for char in data[::-1]:
        result += charComplement(char)
    return result


# Returns the complement of the given char, if a string is given, the function only considers the first char
def charComplement(char: str) -> str:
    if char[0] == A:
        return T
    elif char[0] == T:
        return A
    elif char[0] == C:
        return G
    elif char[0] == G:
        return C
    return "?"


# Returns a list of possibles neighbors for a given string
def getNeighbors(data: str) -> list:
    truncated_data = data[1:]
    return [truncated_data + A, truncated_data + C, truncated_data + G, truncated_data + T]


# Returns the canonical form of the given string
def canonical(data: str) -> str:
    reverse_comp = reverseComplement(data)
    for i in range(len(data)):
        if data[i] < reverse_comp[i]:
            return data
        elif data[i] > reverse_comp[i]:
            return reverse_comp
    return data
