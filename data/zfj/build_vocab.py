"""Script to build words, chars and tags vocab"""

__author__ = "Guillaume Genthial"

from collections import Counter
from pathlib import Path

# TODO: modify this depending on your needs (1 will work just fine)
# You might also want to be more clever about your vocab and intersect
# the GloVe vocab with your dataset vocab, etc. You figure it out ;)
MINCOUNT = 1
SRC_FILE_PATH = 'src.d{}.replte{}.{}.python.a3s2.both.lte1000.recall30.txt'
TAG_FILE_PATH = 'bio.d{}.replte{}.{}.python.a3s2.both.lte1000.recall30.txt'
VOCAB_PATH = 'd{}.replte{}.vocab.words.txt'
VOCAB_CHARS_PATH = 'd{}.replte{}.vocab.chars.txt'
VOCAB_TAGS_PATH = 'd{}.replte{}.vocab.tags.txt'

DISTANCE = 5
REPEAT = 1

if __name__ == '__main__':
    # 1. Words
    # Get Counter of words on all the data, filter by min count, save
    def words(name):
        return SRC_FILE_PATH.format(DISTANCE, REPEAT, name)

    print('Build vocab words (may take a while)')
    counter_words = Counter()
    for n in ['train', 'valid', 'test']:
        with Path(words(n)).open() as f:
            for line in f:
                counter_words.update(line.strip().split())

    vocab_words = {w for w, c in counter_words.items() if c >= MINCOUNT}

    with Path(VOCAB_PATH.format(DISTANCE, REPEAT)).open('w') as f:
        for w in sorted(list(vocab_words)):
            f.write('{}\n'.format(w))
    print('- done. Kept {} out of {}'.format(
        len(vocab_words), len(counter_words)))

    # 2. Chars
    # Get all the characters from the vocab words
    print('Build vocab chars')
    vocab_chars = set()
    for w in vocab_words:
        vocab_chars.update(w)

    with Path(VOCAB_CHARS_PATH.format(DISTANCE, REPEAT)).open('w') as f:
        for c in sorted(list(vocab_chars)):
            f.write('{}\n'.format(c))
    print('- done. Found {} chars'.format(len(vocab_chars)))

    # 3. Tags
    # Get all tags from the training set

    def tags(name):
        return TAG_FILE_PATH.format(DISTANCE, REPEAT, name)

    print('Build vocab tags (may take a while)')
    vocab_tags = set()
    with Path(tags('train')).open() as f:
        for line in f:
            vocab_tags.update(line.strip().split())

    with Path(VOCAB_TAGS_PATH.format(DISTANCE, REPEAT)).open('w') as f:
        for t in sorted(list(vocab_tags)):
            f.write('{}\n'.format(t))
    print('- done. Found {} tags.'.format(len(vocab_tags)))
