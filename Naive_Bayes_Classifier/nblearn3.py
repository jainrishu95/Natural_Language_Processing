import json, sys

def output(truedict, fakedict, positivedict, negativedict):
    file = open('nbmodel.txt', 'w+')
    ans = ''
    ans += json.dumps(truedict)
    ans += '\n\n'
    ans += json.dumps(fakedict)
    ans += '\n\n'
    ans += json.dumps(positivedict)
    ans += '\n\n'
    ans += json.dumps(negativedict)
    file.write(ans)
    file.close()

def cleanline(line):
    replace_str = '~!?,.:;@#$%&*<>(){}[]=1234567890"+^|\\-\'/'
    replace_str = ['<', '>', '?', '.', '"', ')', '(', '|', '-', '#', '*', '+', ';', '!', '/', '\\', '=', ',', ':', '$',
                   '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '[', ']', '@', '&', '%', '{', '}', '^', '~']
    line = line.lower()
    for each in replace_str:
        if each in line:
            line = line.replace(each, ' ')
    return line

def smoothing(fakewords, truewords, positivewords, negativewords, uniquewords):
    for everyword in uniquewords:
        if everyword in fakewords:
            fakewords[everyword] += 1
        else:
            fakewords[everyword] = 1

        if everyword in truewords:
            truewords[everyword] += 1
        else:
            truewords[everyword] = 1

        if everyword in positivewords:
            positivewords[everyword] += 1
        else:
            positivewords[everyword] = 1

        if everyword in negativewords:
            negativewords[everyword] += 1
        else:
            negativewords[everyword] = 1
    return fakewords, truewords, positivewords, negativewords

def add_to_dict(uniquewords, everyword, dict_):
    uniquewords.add(everyword)
    if everyword in dict_:
        dict_[everyword] += 1
    else:
        dict_[everyword] = 1
    return uniquewords, dict_

def input():
    file = open('train-labeled.txt', 'r').read().splitlines()
    #file = open(sys.argv[-1], 'r').readlines()
    total_lines = len(file)
    true_line = 0
    fake_line = 0
    neg_line = 0
    pos_line = 0
    total_fake_words = 0
    total_true_words = 0
    total_positive_words = 0
    total_negative_words = 0
    fakewords = dict()
    truewords = dict()
    positivewords = dict()
    negativewords = dict()
    uniquewords = set()

    common_words = ['i', 'was', 'very', 'with', 'this', 'have', 'in', 'other', 'and', 'them', 'much', 'but', 'the',
                     'can', 'only', 'be', 'as', 'there', 'no', 'during', 'asked', 'me', 'to', 'had', 'room','took',
                     'up', 'good', 'a', 'way', 'because', 'they', 'are', 'it', 'than', 'another', 'never', 'or',
                     'for', 'next', 'on', 'my', 'at', 'did', 'not', 'go', 'when', 'we', 'by', 'then', 'use', 'of',
                     'one', 'call', 'were', 'out', 'am', "wasn't", 'an', 'area', 'into', 'about', 'us', 'back', 'more',
                     'our', 'large', 'old', 'need', 'last', 'first', 'all', 'said', 'rooms', 'that', 'high', 'which',
                     'really', 'she', 'if', 'would', 'quite', 'will', 'ever', 'place', 'again', 'every', 'think', 'is',
                     'best', 'like', 'better', 'right', 'two', 'should', 'from', 'here', 'few', 'their', 'also',
                     'some', 'find', 'make', 'while', 'your', 'nothing', 'any', 'got', 'you', 'most', 'so', 'get',
                     'been', 'even', 'over', 'its', 'many', 'after', 'new', 'great', 'know', 'how', 'say', 'away',
                     'do', 'well', 'front', 'take', 'long', "didn't", 'work', 'going', 'made', 'what', 'though',
                     'before', "don't", 'being', 'too', 'he', 'off', 'down', 'found', "it's", 'went', 'could', 'just',
                     'around', 'top', 'has', 'however', 'came', 'where', 'seemed', 'want', 'who', 'small',
                     'everything', 'upon', 'felt', "i've", 'still']

    common_words = ['i', 'was', 'very', 'with', 'this', 'have', 'in', 'other', 'and', 'them', 'much', 'but', 'the',
                    'can', 'only', 'be', 'as', 'there', 'no', 'during', 'asked', 'me', 'to', 'had', 'room', 'took',
                    'up', 'good', 'a', 'way', 'because', 'they', 'are', 'it', 'than', 'another', 'never', 'or', 'for',
                    'next', 'on', 'my', 'at', 'did', 'not', 'go', 'when', 'we', 'by', 'then', 'use', 'of', 'one',
                    'call', 'were', 'out', 'am', "wasn't", 'an', 'area', 'into', 'about', 'us', 'back', 'more', 'our',
                    'large', 'old', 'need', 'last', 'first', 'all', 'said', 'rooms', 'that', 'high', 'which', 'really',
                    'she', 'if', 'would', 'quite', 'will', 'ever', 'place', 'again', 'every', 'think', 'is', 'best',
                    'like', 'better', 'right', 'two', 'should', 'from', 'here', 'few', 'their', 'also', 'some', 'find',
                    'make', 'while', 'your', 'nothing', 'any', 'got', 'you', 'most', 'so', 'get', 'been', 'even',
                    'over', 'its', 'many', 'after', 'new', 'great', 'know', 'how', 'say', 'away', 'do', 'well',
                    'front', 'take', 'long', "didn't", 'work', 'going', 'made', 'what', 'though', 'before',
                    "don't", 'being', 'since', 'too', 'he', 'see', 'off', 'down', 'found', "it's", 'went',
                    'could', 'just', 'around', 'top', 'has', 'however', 'came', 'gave', 'where', 'seemed',
                    'want', 'who', 'small', 'everything', 'upon', 'felt', "i've", 'still']

    common_words = ['down', 'and', 'with', 'you', 'hers', 'your', "he'd", 'had', "we're", 'i', 'again', 'so', 'my',
                    'yourself', 'there', 'between', 'was', 'we', 'only', 'this', "i'll", 'for', 'it', 'itself', "i'm",
                    'by', 'they', 'him', "that's", 'high', 'very', 'would', "when's", 'his', "i'd", 'further', 'nor',
                    "where's", "who's", 'own', 'about', 'doing', "we've", 'were', 'over', 'to', "she'll", 'having',
                    'what', "it's", 'why', 'has', 'if', 'where', 'more', 'up', 'yours', "they're", 'her', 'during',
                    'all', 'from', 'ought', "we'd", "i've", "you'll", 'been', 'are', 'being', 'also', 'most', 'few',
                    'its', 'while', 'into', "you're", 'other', "he's", 'have', 'the', "we'll", 'as', 'ours', 'he',
                    'should', "what's", 'below', 'before', 'our', 'then', 'against', 'on', "why's", 'their', "let's",
                    "there's", 'yourselves', 'but', 'she', 'these', 'at', 'who', 'when', 'did', 'theirs', 'same',
                    'each', 'be', 'until', 'how', 'or', 'them', 'once', "she'd", 'those', 'in', 'too', 'could',
                    "they'll", 'out', 'any', 'himself', 'after', 'of', 'such', 'through', "they'd", 'some', 'whom',
                    'do', 'a', "you've", 'myself', 'above', 'does', 'under', "they've", 'which', 'herself',
                    'themselves', 'me', "you'd", "he'll", "how's", 'am', 'is', 'now', 'ourselves', "here's", 'an',
                    'that', "she's", 'than', 'both', 'here', 'because']

    common_words = ['each', 'again', 'yours', 'so', 'under', 'do', 'down', 'had', 'my', 'now', 'we', 'both', 'whom', 'the', 'doing', 'theirs', 'of', 'than', 'few', 'would', 'old', "what's", 'ourselves', 'and', "i'd", 'yourself', 'but', 'as', "who's", 'there', 'when', 'he', 'was', 'our', "we're", 'asked', "why's", "you've", 'only', 'have', 'any', 'two', 'though', 'such', 'all', "they'll", 'below', 'most', 'quite', 'away', 'between', 'out', 'being', "he'd", "we'll", 'every', "you'll", 'to', "where's", 'through', 'about', "they've", 'which', 'why', 'his', "i'll", 'high', 'with', 'a', 'could', 'were', 'where', 'be', 'up', 'been', 'further', 'said', 'him', 'ours', "they're", 'also', 'who', 'next', 'at', 'having', 'she', 'myself', "let's", 'himself', 'should', "we'd", 'nor', 'until', 'has', 'am', 'in', "he'll", 'if', 'are', 'above', 'own', 'more', 'her', 'those', 'from', 'while', 'before', 'ought', 'once', "when's", 'by', "they'd", "i'm", "we've", 'other', 'or', 'themselves', 'then', 'for', 'what', 'i', 'herself', 'that', 'an', 'because', "she's", "it's", "you're", 'does', 'here', 'me', 'this', 'same', "she'd", 'during', 'too', 'it', "that's", "he's", 'their', "there's", 'rooms', 'on', 'over', 'many', 'some', 'these', 'its', 'your', 'how', 'yourselves', 'did', "you'd", 'you', 'into', "she'll", 'is', "i've", "how's", 'hers', 'them', 'very', "here's", 'against', 'make', 'itself', 'after', 'they']

    #print(len(common_words))
    for everyline in file:
        if '\n' in everyline:
            everyline = everyline.replace('\n', '')
        words = everyline[8:].split()
        type1 = words[0].lower()
        type2 = words[1].lower()
        words = words[2:]
        words = cleanline(' '.join(words)).split()

        if type1 == 'fake':
            fake_line += 1
            for everyword in words:
                if everyword not in common_words:
                    everyword = everyword.strip()
                    total_fake_words += 1
                    uniquewords, fakewords = add_to_dict(uniquewords, everyword, fakewords)

        else:
            true_line += 1
            for everyword in words:
                if everyword not in common_words:
                    everyword = everyword.strip()
                    total_true_words += 1
                    uniquewords, truewords = add_to_dict(uniquewords, everyword, truewords)

        if type2 == 'pos':
            pos_line += 1
            for everyword in words:
                if everyword not in common_words:
                    everyword = everyword.strip()
                    total_positive_words += 1
                    uniquewords, positivewords = add_to_dict(uniquewords, everyword, positivewords)

        else:
            neg_line += 1
            for everyword in words:
                if everyword not in common_words:
                    everyword = everyword.strip()
                    total_negative_words += 1
                    uniquewords, negativewords = add_to_dict(uniquewords, everyword, negativewords)

    fakewords, truewords, positivewords, negativewords = smoothing(fakewords, truewords, positivewords, negativewords, uniquewords)

    total_fake_words += len(uniquewords)
    total_true_words += len(uniquewords)
    total_positive_words += len(uniquewords)
    total_negative_words += len(uniquewords)

    fakedict = {
        'words': fakewords,
        'len': total_fake_words,
        'prior': (1.0 * fake_line) / (1.0 * total_lines)
    }

    truedict = {
        'words': truewords,
        'len': total_true_words,
        'prior': (1.0 * true_line) / (1.0 * total_lines)
    }

    positivedict = {
        'words': positivewords,
        'len': total_positive_words,
        'prior': (1.0 * pos_line) / (1.0 * total_lines)
    }

    negativedict = {
        'words': negativewords,
        'len': total_negative_words,
        'prior': (1.0 * neg_line) / (1.0 * total_lines)
    }

    output(truedict, fakedict, positivedict, negativedict)

if __name__ == '__main__':
    input()