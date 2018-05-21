import json, timeit, sys

def input():
    #sentencelst = open('zh_dev_raw.txt', 'r', encoding = 'UTF-8').read().splitlines()
    sentencelst = open(sys.argv[-1], 'r', encoding='UTF-8').read().splitlines()
    lst = [json.loads(x) for x in open('hmmmodel.txt', 'r', encoding = 'UTF-8').read().split('\t')]
    tagcount = lst[0]
    wordtag = lst[1]
    transitionprob = lst[2]
    starttagscount = lst[-1]
    return tagcount, wordtag, transitionprob, sentencelst, starttagscount

def viterbi(tagcount, wordtag, transitionprob, eachline, starttagscount):
    words_each_line = eachline.split(' ')
    wordline = list() #final list for tagged sentence

    #calculate probability from start to rest all tags
    line = dict()  # dict for start to all tags for 1st word
    prevtag = 'start'
    if words_each_line[0] in wordtag:
        nextagset = wordtag[words_each_line[0]]
    else:
        nextagset = tagcount
    for s in nextagset:
        # calculate transition probability
        transprob = transitionprob[prevtag][s]
        #calculate emission probability
        if words_each_line[0] in wordtag:
            if s in wordtag[words_each_line[0]]:
                emissionprob = wordtag[words_each_line[0]][s]
            else:
                emissionprob = 1
        else:
            emissionprob = 1

        prob = transprob * emissionprob
        data = dict()
        data['tag'] = s
        data['prob'] = prob
        data['backpointer'] = prevtag
        line[s] = data

    wordline.append(line)

    prevtagset = nextagset
    t1 = timeit.default_timer()
    #calulating probabilities for next words
    for eachword in words_each_line[1:]:
        line = dict()
        if eachword in wordtag:
            nextagset = wordtag[eachword]
        else:
            nextagset = tagcount
        for nextag in nextagset:
            maxvalue = {
                'tag': '',
                'prob': 0.0,
                'backpointer': ''
            }
            for prevtag in prevtagset:
                # calculate transition probability
                transprob = transitionprob[prevtag][nextag]

                # calculate emission probability
                if eachword in wordtag:
                    if nextag in wordtag[eachword]:
                        emissionprob = wordtag[eachword][nextag]
                    else:
                        emissionprob = 1
                else:
                    emissionprob = 1

                #final probability of state
                prob = transprob * emissionprob * wordline[-1][prevtag]['prob']

                if prob > maxvalue['prob']:
                    maxvalue['tag'] = nextag
                    maxvalue['prob'] = prob
                    maxvalue['backpointer'] = prevtag

            line[nextag] = maxvalue
        prevtagset = nextagset

        wordline.append(line)

    t2 = timeit.default_timer()
    #print(t2 - t1)

    #calculate probability from last tags till end
    endprob = {'backpointer': '',
               'prob': 0,
               'tag': 'end'}
    for tag in prevtagset:
        #calculate transition probability
        transprob = transitionprob[tag]['end']
        prob = transprob * wordline[-1][tag]['prob']
        if prob >= endprob['prob']:
            endprob['prob'] = prob
            endprob['backpointer'] = tag

    #backtraverse to tag words now
    lst = list()
    prevtag = endprob['backpointer']
    for i in wordline[::-1]:
        lst.append(i[prevtag]['tag'])
        prevtag = i[prevtag]['backpointer']
    lst = lst[::-1]

    ans = ''
    for i in range(len(words_each_line)):
        ans += words_each_line[i] + '/' + lst[i] + ' '
    ans += '\n'
    return ans

def decode(tagcount, wordtag, transitionprob, sentencelst, starttagscount):
    final = ''
    for eachline in sentencelst:
        final += viterbi(tagcount, wordtag, transitionprob, eachline, starttagscount)
    return final

def output(tagged):
    file = open('hmmoutput.txt', 'w+')
    file.write(tagged)
    file.close()

def accuracy(file_pred_path, file_orig_path):

    file_orig = open(file_orig_path, "r", encoding='UTF-8')
    file_orig_read = file_orig.read().splitlines()

    file_pred = open(file_pred_path, "r", encoding='UTF-8')
    file_pred_read = file_pred.read().splitlines()

    count_same = 0
    count_all = 0

    for i in range(len(file_orig_read)):

        word_tag_orig = file_orig_read[i].split(" ")
        word_tag_pred = file_pred_read[i].split(" ")

        for j in range(len(word_tag_orig)):

            if word_tag_orig[j] == word_tag_pred[j]:
                count_same += 1

            count_all += 1

    accuracy_value = (count_same/count_all)*100
    return accuracy_value

if __name__ == "__main__":
    start = timeit.default_timer()
    tagcount, wordtag, transitionprob, sentencelst, starttagscount = input()
    tagged = decode(tagcount, wordtag, transitionprob, sentencelst, starttagscount)
    output(tagged)
    #print(accuracy('hmmoutput.txt', 'zh_dev_tagged.txt'))
    end = timeit.default_timer()
    #print("time taken = " + str(end - start))

