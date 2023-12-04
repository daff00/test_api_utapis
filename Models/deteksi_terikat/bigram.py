def generate_bigrams(text):
    words = text.split()
    bigrams = []

    for i in range(len(words)-1):
        bigrams.append((words[i] + " " + words[i+1], i))

    return bigrams

def split_words(input_string):
    return input_string.split()