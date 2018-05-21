import json, sys, time
# from nltk.stem.porter import *

def output(weight_true_fake, bias_true_fake, weight_pos_neg, bias_pos_neg, filename):
    file = open(filename, 'w+')
    file.write(json.dumps(weight_true_fake))
    file.write('\n')
    file.write(json.dumps(bias_true_fake))
    file.write('\n')
    file.write(json.dumps(weight_pos_neg))
    file.write('\n')
    file.write(json.dumps(bias_pos_neg))
    file.close()

def cleanline(line):
    replace_str = ['<', '>', '?', '.', '"', ')', '(', '|', '-', '#', '*', '+', ';', '!', '/', '\\', '=', ',', ':', '$',
                   '[', ']', '@', '&', '%', '{', '}', '^', '~']
    line = line.lower()
    for each in replace_str:
        if each in line:
            line = line.replace(each, ' ')
    return line

def input(maxiter, learning_rate):
    #file = open(sys.argv[-1], 'r').readlines()
    file = open('train-labeled.txt', 'r').readlines()
    file = [cleanline(line) for line in file]

    linematrix = list()                             # [true/fake pos/neg wordcount]
    uniquewords = set()
    true_fake = [-1, 1]
    pos_neg = [-1, 1]

    common_words = sorted([
        "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone",
        "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and",
        "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back",
        "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
        "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can",
        "cannot","cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due",
        "during","each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever",
        "every","everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first",
        "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get",
        "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein",
        "hereupon","hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed",
        "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd",
        "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
        "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine",
        "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once",
        "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own",
        "part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems",
        "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some",
        "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take",
        "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore",
        "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three",
        "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve",
        "twenty", "two","un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever",
        "when","whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever",
        "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
        "within","without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"])

    common_words = sorted([
        "a", "about", "above", "across", "after", "again", "all", "almost",
        "along", "also", "although", "always", "am", "amount", "an", "and",
        "another", "any", "anyone", "anything", "anyway", "are", "around", "as", "at", "back",
        "because", "been", "before", "being","between", "beyond", "both", "bottom", "but", "by", "call", "can", "co",
        "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "during",
        "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every",
        "everyone", "everywhere", "few", "fifteen", "fify", "fill", "find", "fire", "first",
        "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get",
        "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "hereafter", "hereby", "herein", "hereupon",
        "hers", "herself", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed",
        "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd",
        "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
        "move", "much", "must", "my", "name", "namely", "neither", "never", "nevertheless", "next", "nine",
        "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once",
        "one", "only", "onto", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own",
        "part", "per", "perhaps", "please", "put", "rather", "same", "see", "seem", "seemed", "seeming", "seems",
        "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some",
        "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "system", "take", "ten",
        "than","that", "the", "their", "them", "then", "thence", "there", "thereafter", "thereby", "therefore",
        "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three",
        "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve",
        "twenty", "two","un", "under", "until", "up", "upon", "us", "very", "was", "we", "well", "were", "what", "whatever", "when",
        "whence", "whenever", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever",
        "whether", "which", "while", "whither", "whoever", "whole", "whom", "whose", "why", "will", "with", "within",
        "without", "would", "yet", "you", "your", "yours", "yourselves", "afterwards", "against", "alone", "already",
        "among", "amongst", "amoungst", "anyhow", "be", "became", "become", "becomes", "becoming", "beforehand",
        "behind", "below", "beside", "besides", "bill", "cannot", "cant", "anywhere", "everything"])

    for everyline in file:
        everyline = everyline.split()[1:]
        type1 = everyline[0]
        type2 = everyline[1]
        everyline = everyline[2:]
        wordcount = dict()
        lst = list()
        for word in everyline:
            if word not in common_words:
                # stemmer = PorterStemmer()
                # word = stemmer.stem(word)
                uniquewords.add(word)
                if word in wordcount:
                    wordcount[word] += 1
                else:
                    wordcount[word] = 1
        if type1 == 'true':
            lst.append(true_fake[0])
        else:
            lst.append(true_fake[1])
        if type2 == 'pos':
            lst.append(pos_neg[0])
        else:
            lst.append(pos_neg[1])
        lst.append(wordcount)
        linematrix.append(lst)

    weight_true_fake = dict()
    weight_pos_neg = dict()
    cached_weight_true_fake = dict()
    cached_weight_pos_neg = dict()
    for everyword in uniquewords:
        weight_true_fake[everyword] = 0.0
        weight_pos_neg[everyword] = 0.0
        cached_weight_true_fake[everyword] = 0.0
        cached_weight_pos_neg[everyword] = 0.0

    bias_true_fake = 0.0
    bias_pos_neg = 0.0
    beta_true_fake = 0.0
    beta_pos_neg = 0.0
    counter = 1
    # maxiter = 20
    # learning_rate = 1.0

    for j in range(maxiter):
        for i in range(len(linematrix)):
            words = linematrix[i][2]
            vec_sum_true_fake = 0
            vec_sum_pos_neg = 0

            for everyword in words:
                vec_sum_true_fake += (linematrix[i][2][everyword] * weight_true_fake[everyword])
                vec_sum_pos_neg += (linematrix[i][2][everyword] * weight_pos_neg[everyword])

            vec_sum_true_fake += bias_true_fake
            vec_sum_pos_neg += bias_pos_neg
            #print(vec_sum_true_fake, vec_sum_pos_neg)

            # wrong predict true/fake
            if (vec_sum_true_fake * linematrix[i][0]) <= 0:
                for everyword in words:
                    weight_true_fake[everyword] += (linematrix[i][0] * linematrix[i][2][everyword] * learning_rate)
                    cached_weight_true_fake[everyword] += (linematrix[i][0] * linematrix[i][2][everyword] * counter * learning_rate)
                bias_true_fake += linematrix[i][0]
                beta_true_fake += (counter * linematrix[i][0])

            # wrong predict pos/neg
            if (vec_sum_pos_neg * linematrix[i][1]) <= 0:
                for everyword in words:
                    weight_pos_neg[everyword] += (linematrix[i][1] * linematrix[i][2][everyword] * learning_rate)
                    cached_weight_pos_neg[everyword] += (linematrix[i][1] * linematrix[i][2][everyword] * counter * learning_rate)
                bias_pos_neg += linematrix[i][1]
                beta_pos_neg += (linematrix[i][1] * counter)

            counter += 1
    #print(weight_true_fake)

    for everyword in weight_true_fake:
        cached_weight_true_fake[everyword] = weight_true_fake[everyword] - ((1 / counter) * cached_weight_true_fake[everyword])

    for everyword in weight_pos_neg:
        cached_weight_pos_neg[everyword] = weight_pos_neg[everyword] - ((1 / counter) * cached_weight_pos_neg[everyword])

    beta_true_fake = bias_true_fake - ((1 / counter) * beta_true_fake)
    beta_pos_neg = bias_pos_neg - ((1 / counter) * beta_pos_neg)

    output(weight_true_fake, bias_true_fake, weight_pos_neg, bias_pos_neg, 'vanillamodel.txt')
    output(cached_weight_true_fake, beta_true_fake, cached_weight_pos_neg, beta_pos_neg, 'averagedmodel.txt')

if __name__ == '__main__':
    s = time.time()
    input(20, 1.0)
    print(time.time()-s)