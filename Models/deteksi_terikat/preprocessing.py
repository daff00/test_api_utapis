import re
import string

def preprocessing(text):
    # menghapus karakter yang tidak diinginkan (encoded char)
    text = ''.join(t for t in text if ord(t) < 128)

    # menghapus angka
    text = re.sub(r"\d+", "", text)

    # menghapus \r \n
    text = text.replace('\r', ' ').replace('\n', ' ')

    # menghapus tanda baca tanpa -
    text = text.translate(str.maketrans("", "", string.punctuation.replace('-', '')))

    # menghapus spasi di awal dan akhir
    text = text.strip()

    return text
