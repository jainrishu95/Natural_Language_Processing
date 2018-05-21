import perceplearn3 as p3
import sys, json, time

def input(filename):
    lst = [json.loads(every) for every in open(filename, 'r').read().split('\n')]
    weight_true_fake = lst[0]
    bias_true_fake = lst[1]
    weight_pos_neg = lst[2]
    bias_pos_neg = lst[3]
    return weight_true_fake, bias_true_fake, weight_pos_neg, bias_pos_neg

def cleanline(line):
    replace_str = ['<', '>', '?', '.', '"', ')', '(', '|', '-', '#', '*', '+', ';', '!', '/', '\\', '=', ',', ':', '$',
                   '[', ']', '@', '&', '%', '{', '}', '^', '~']
    line = line.lower()
    for each in replace_str:
        if each in line:
            line = line.replace(each, ' ')
    return line

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

    # print("T_F_Acc : ", acc2)
    # print("P_N_Acc : ", acc1)
    #
    # #print((acc2+acc1)/2)
    #
    # print('Mean F1 Score: ' + str(f1_score * 100))
    return f1_score

def output(filename, ans):
    file = open(filename, 'w+')
    for every in ans:
        file.write(every)
    file.close()

def classify(weight_true_fake, bias_true_fake, weight_pos_neg, bias_pos_neg):
    file = open('dev-text.txt', 'r').readlines()
    #file = open(sys.argv[-1], 'r').readlines()
    lst = list()
    for eachline in file:
        true_fake = 0
        pos_neg = 0
        words = eachline.split()
        idd = words[0]
        words = words[1:]
        words = cleanline(' '.join(words)).split()
        ans = idd
        for everyword in words:
            if everyword in weight_true_fake:
                true_fake += weight_true_fake[everyword]
            if everyword in weight_pos_neg:
                pos_neg +=  weight_pos_neg[everyword]
        true_fake += bias_true_fake
        pos_neg += bias_pos_neg

        if true_fake < 0:
            ans += ' True '
        else:
            ans += ' Fake '

        if pos_neg < 0:
            ans += 'Pos'
        else:
            ans += 'Neg'
        ans += '\n'
        lst.append(ans)
    output('percepoutput.txt', lst)

if __name__ == '__main__':
    s = time.time()
    p3.input(30, 1.0)
    weight_true_fake, bias_true_fake, weight_pos_neg, bias_pos_neg = input('vanillamodel.txt')
    classify(weight_true_fake, bias_true_fake, weight_pos_neg, bias_pos_neg)
    print(calcF1('dev-key.txt', 'percepoutput.txt'))
    weight_true_fake, bias_true_fake, weight_pos_neg, bias_pos_neg = input('averagedmodel.txt')
    # weight_true_fake, bias_true_fake, weight_pos_neg, bias_pos_neg = input(sys.argv[-2])
    classify(weight_true_fake, bias_true_fake, weight_pos_neg, bias_pos_neg)
    print(calcF1('dev-key.txt', 'percepoutput.txt'))
    print(time.time()-s)