import timeit, sys, json, math
wordtag = dict()
tagcount = dict()
transitionprob = dict()

def input():
	global tagcount, wordtag, transitionprob
	#file = open('zh_train_tagged.txt', 'r', encoding = 'UTF-8').read().splitlines()
	file = open(sys.argv[-1], 'r', encoding='UTF-8').read().splitlines()
	filelen = len(file)

	for line in file:
		words = line.split(' ')
		prevtag = 'start'

		#for each words given tag in a line
		for every in words:
			pos = every.rfind('/')
			word = every[:pos]
			tag = every[pos+1:]

			# finding tags in file
			if tag in tagcount:
				tagcount[tag] += 1
			else:
				tagcount[tag] = 1

			# finding words with respective tags in file
			if word in wordtag:
				if tag in wordtag[word]:
					wordtag[word][tag] += 1
				else:
					wordtag[word][tag] = 1
			else:
				wordtag[word] = dict()
				wordtag[word][tag] = 1

			#transition probability
			nexttag = tag
			if prevtag in transitionprob:
				if nexttag in transitionprob[prevtag]:
					transitionprob[prevtag][nexttag] += 1
				else:
					transitionprob[prevtag][nexttag] = 1
			else:
				transitionprob[prevtag] = dict()
				transitionprob[prevtag][nexttag] = 1

			#update prevtag
			prevtag = nexttag

		nexttag = 'end'
		if prevtag in transitionprob:
			if nexttag in transitionprob[prevtag]:
				transitionprob[prevtag][nexttag] += 1
			else:
				transitionprob[prevtag][nexttag] = 1
		else:
			transitionprob[prevtag] = dict()
			transitionprob[prevtag][nexttag] = 1

	return tagcount, wordtag, transitionprob, filelen

def smoothing(tagcount, transitionprob):
	tagcount['end'] = 1
	l = len(tagcount)
	for prevtag in transitionprob:
		for eachtag in tagcount:
			if prevtag == 'start' and eachtag == 'end':
				continue
			else:
				if eachtag in transitionprob[prevtag]:
					transitionprob[prevtag][eachtag] += 2.05
				else:
					transitionprob[prevtag][eachtag] = 2.05
				#tagcount[eachtag] += 2.05
		if prevtag != 'start':
			tagcount[prevtag] += 4 * l
	del tagcount['end']
	'''tagcount2 = copy.deepcopy(tagcount)
	for eachtag in tagcount:
		if eachtag not in transitionprob:
			transitionprob[eachtag] = dict()
			for nexttag in tagcount2:
				transitionprob[eachtag][nexttag] = 1
			if eachtag in tagcount:
				tagcount[eachtag] += l
			else:
				tagcount[eachtag] = l
	for word in wordtag:
		print(word, len(wordtag[word]), wordtag[word])
	'''
	return tagcount, transitionprob

def calculation(tagcount, wordtag, transitionprob, starttags):
	n = len(tagcount) * 2
	for prevtag in transitionprob:
		for nexttag in transitionprob[prevtag]:
			if prevtag != 'start':
				transitionprob[prevtag][nexttag] = math.log(transitionprob[prevtag][nexttag]) - math.log(tagcount[prevtag]) + n
			else:
				transitionprob[prevtag][nexttag] = math.log(transitionprob[prevtag][nexttag]) - math.log(starttags) + n

	for eachword in wordtag:
		for eachtag in wordtag[eachword]:
			wordtag[eachword][eachtag] = math.log(wordtag[eachword][eachtag]) - math.log(tagcount[eachtag]) + n

	return wordtag, transitionprob

def output(tagcount, wordtag, transitionprob, starttags):
    file = open('hmmmodel.txt', 'w+')
    file.write(json.dumps(tagcount))
    file.write('\t')
    file.write(json.dumps(wordtag))
    file.write('\t')
    file.write(json.dumps(transitionprob))
    file.write('\t')
    file.write(str(starttags))
    file.close()

if __name__ == "__main__":
	start = timeit.default_timer()
	tagcount, wordtag, transitionprob, starttags = input()
	tagcount, transitionprob = smoothing(tagcount, transitionprob)
	wordtag, transitionprob = calculation(tagcount, wordtag, transitionprob, starttags)
	output(tagcount, wordtag, transitionprob, starttags + len(tagcount))
	end = timeit.default_timer()
	#print(end-start)
