import re

def rabinKarp(text, patterns, is_bigram = False, index = 0):
    prime = 101  # A prime number for hash calculation
    base = 256   # Number of possible characters (ASCII)

    # Find word boundaries in the text
    word_boundaries = [match.start() for match in re.finditer(r'\b\w+\b', text)]

    n = len(text)
    results = []

    for pattern in patterns:
        m = len(pattern)

        # Calculate the hash of the pattern and the first window in the text
        hash_pattern = 0
        hash_window = 0
        h = 1
        for i in range(m-1):
            h = (h * base) % prime

        if (m < n):
            for i in range(m):
                hash_pattern = (base * hash_pattern + ord(pattern[i])) % prime
                hash_window = (base * hash_window + ord(text[i])) % prime

        # Slide the pattern over the text
        for i in range(n-m+1):
            if hash_pattern == hash_window:
                if text[i:i+m] == pattern and i in word_boundaries:
                    if (is_bigram):
                        results = (pattern, text, index)
                    else:
                        end_index = i
                        while end_index < len(text) and text[end_index] != ' ':
                            end_index += 1
                        results.append((pattern, text[i + len(pattern):end_index], text[i:end_index], i))

            if i < n-m:
                hash_window = (base * (hash_window - ord(text[i]) * h) + ord(text[i+m])) % prime
                if hash_window < 0:
                    hash_window += prime

    return results