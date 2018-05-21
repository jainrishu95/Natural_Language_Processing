import sys, math, json

def input():
    lst = [json.loads(every) for every in open('nbmodel.txt', 'r').read().split('\n\n')]
    truedict = lst[0]
    fakedict = lst[1]
    positivedict = lst[2]
    negativedict = lst[3]
    return truedict, fakedict, positivedict, negativedict

def cleanline(line):
    replace_str = '~!?,.:;@#$%&*<>(){}[]=1234567890"+^|\\-\'/'
    replace_str = ['<', '>', '?', '.', '"', ')', '(', '|', '-', '#', '*', '+', ';', '!', '/', '\\', '=', ',', ':', '$',
                   '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '[', ']', '@', '&', '%', '{', '}', '^', '~']
    for each in replace_str:
        if each in line:
            line = line.replace(each, ' ')
    return line

def output(ans):
    file = open('nboutput.txt', 'w+')
    for every in ans:
        file.write(every)
    file.close()

def classify(truedict, fakedict, positivedict, negativedict):
    file = open('dev-text.txt', 'r').readlines()
    #file = open(sys.argv[-1], 'r').readlines()
    ans = list()
    for everyline in file:
        if '\n' in everyline:
            everyline = everyline.replace('\n', '')
        everyline = everyline.split()
        final = ''
        final += everyline[0]
        final += ' '
        everyline = cleanline(' '.join(everyline[1:])).split()
        fakeprob = math.log(fakedict['prior'])
        trueprob = math.log(truedict['prior'])
        positiveprob = math.log(positivedict['prior'])
        negativeprob = math.log(negativedict['prior'])

        for everyword in everyline:
            everyword = everyword.lower()
            if everyword in fakedict['words']:
                fakeprob += math.log((1.0 * fakedict['words'][everyword]) / (1.0 * fakedict['len']))

            if everyword in truedict['words']:
                trueprob += math.log((1.0 * truedict['words'][everyword]) / (1.0 * truedict['len']))

            if everyword in positivedict['words']:
                positiveprob += math.log((1.0 * positivedict['words'][everyword]) / (1.0 * positivedict['len']))

            if everyword in negativedict['words']:
                negativeprob += math.log((1.0 * negativedict['words'][everyword]) / (1.0 * negativedict['len']))

        if fakeprob > trueprob:
            final += 'Fake '
        else:
            final += 'True '
        if negativeprob > positiveprob:
            final += 'Neg'
        else:
            final += 'Pos'
        final += '\n'
        ans.append(final)
    output(ans)

def calcF1(true_key_path, pred_key_path):

    acc_count = 0

    file_orig = open(true_key_path, "r", encoding='UTF-8')
    true_keys = file_orig.read().splitlines()

    file_pred = open(pred_key_path, "r", encoding='UTF-8')
    pred_keys = file_pred.read().splitlines()

    t_f_class_counts = [0,0,0,0]
    p_n_class_counts = [0,0,0,0]

    for i in range(0, len(true_keys)):

        true_key_entry = true_keys[i]
        pred_key_entry = pred_keys[i]

        if true_key_entry == pred_key_entry:
            acc_count = acc_count + 1

        true_key_entry_parts = true_key_entry.split(" ")
        pred_key_entry_parts = pred_key_entry.split(" ")

        if true_key_entry_parts[0] == pred_key_entry_parts[0]:

            true_label_t_f = true_key_entry_parts[1]
            pred_label_t_f = pred_key_entry_parts[1]

            true_label_p_n = true_key_entry_parts[2]
            pred_label_p_n = pred_key_entry_parts[2]

            if true_label_t_f == "True" and pred_label_t_f == "True":
                t_f_class_counts[0] = t_f_class_counts[0] + 1
            elif true_label_t_f == "Fake" and pred_label_t_f == "True":
                t_f_class_counts[1] = t_f_class_counts[1] + 1
            elif true_label_t_f == "True" and pred_label_t_f == "Fake":
                t_f_class_counts[2] = t_f_class_counts[2] + 1
            elif true_label_t_f == "Fake" and pred_label_t_f == "Fake":
                t_f_class_counts[3] = t_f_class_counts[3] + 1

            if true_label_p_n == "Pos" and pred_label_p_n == "Pos":
                p_n_class_counts[0] = p_n_class_counts[0] + 1
            elif true_label_p_n == "Neg" and pred_label_p_n == "Pos":
                p_n_class_counts[1] = p_n_class_counts[1] + 1
            elif true_label_p_n == "Pos" and pred_label_p_n == "Neg":
                p_n_class_counts[2] = p_n_class_counts[2] + 1
            elif true_label_p_n == "Neg" and pred_label_p_n == "Neg":
                p_n_class_counts[3] = p_n_class_counts[3] + 1

    prec_true = (t_f_class_counts[0]*1.0) / (t_f_class_counts[0]+t_f_class_counts[1])*1.0
    rec_true = (t_f_class_counts[0] * 1.0) / (t_f_class_counts[0] + t_f_class_counts[2]) * 1.0
    prec_fake = (t_f_class_counts[3] * 1.0) / (t_f_class_counts[3] + t_f_class_counts[2]) * 1.0
    rec_fake = (t_f_class_counts[3] * 1.0) / (t_f_class_counts[3] + t_f_class_counts[1]) * 1.0

    f_true = (2.0*prec_true*rec_true)/(prec_true+rec_true)*1.0
    f_fake = (2.0 * prec_fake * rec_fake) / (prec_fake + rec_fake) * 1.0

    prec_pos = (p_n_class_counts[0] * 1.0) / (p_n_class_counts[0] + p_n_class_counts[1]) * 1.0
    rec_pos = (p_n_class_counts[0] * 1.0) / (p_n_class_counts[0] + p_n_class_counts[2]) * 1.0
    prec_neg = (p_n_class_counts[3] * 1.0) / (p_n_class_counts[3] + p_n_class_counts[2]) * 1.0
    rec_neg = (p_n_class_counts[3] * 1.0) / (p_n_class_counts[3] + p_n_class_counts[1]) * 1.0

    f_pos = (2.0 * prec_pos * rec_pos) / (prec_pos + rec_pos) * 1.0
    f_neg = (2.0 * prec_neg * rec_neg) / (prec_neg + rec_neg) * 1.0

    f1_score = 1.0*(f_true + f_fake +f_pos +f_neg)/ 4.0

    #print(acc_count/len(true_keys))
    acc1 = (p_n_class_counts[0]+p_n_class_counts[3])/(p_n_class_counts[0]+p_n_class_counts[1]+p_n_class_counts[2]+p_n_class_counts[3])
    acc2 = (t_f_class_counts[0]+t_f_class_counts[3])/(t_f_class_counts[0]+t_f_class_counts[1]+t_f_class_counts[2]+t_f_class_counts[3])

    print("T_F_Acc : ", acc2)
    print("P_N_Acc : ", acc1)

    #print((acc2+acc1)/2)

    print('Mean F1 Score: ' + str(f1_score * 100))

if __name__ == '__main__':
    truedict, fakedict, positivedict, negativedict = input()
    classify(truedict, fakedict, positivedict, negativedict)
    calcF1('dev-key.txt', 'nboutput.txt')