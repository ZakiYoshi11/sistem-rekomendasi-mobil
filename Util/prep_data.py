from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re


# ===========================Slang Word===========================
def load_slang(slangpath):
    slang_dict = {}
    with open(slangpath, 'r', encoding='Utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('\t')
                slang = parts[0]
                formal = parts[1] if len(parts) > 1 else ""
                slang_dict[slang] = formal
    return slang_dict

slang_file = "./Kuliah-tugas-besar-bigdata/Cache/slang.txt"
slang_training = "./Cache/slang.txt"
slng_dict = load_slang(slang_file)

def process_slang(text, slang_dict = slng_dict):
    words = text.split()
    processed_words = []

    for word in words:
         # Mengganti jika slang ditemukan, jika tidak, biarkan seperti itu
        processed_word = slang_dict.get(word.lower(), word)
        processed_words.append(processed_word)

    processed_text = ' '.join(processed_words)
    return processed_text


# ===========================Preprocessing Text===========================
def prep(text):
   # Lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Stemming
    stem_factory = StemmerFactory()
    stemmer = stem_factory.create_stemmer()
    text = stemmer.stem(text)

    # Remove stopwords
    stopword_factory = StopWordRemoverFactory()
    stopword_remover = stopword_factory.create_stop_word_remover()
    text = stopword_remover.remove(text)

    # Tokenize
    tokens =  text.split()
    return tokens