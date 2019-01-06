word = "abcde"
initial_part = [[letter] for letter in word]
words = [''.join(element) for element in initial_part] #transformare lista de partitii in lista de cuvinte formate din partitii
# max_acc = acc(words)
# best_part = initial_part

def partition(current_partition, pos):
    print(current_partition, "  Length = ", len(current_partition))
    words = [''.join(element) for element in current_partition]

    ##########################################################################################################
    # prelucrare current_partition
    # calcularea accuratete, comparat cu acuratetea maxima gasita, actualizata acuratetea maxima daca este cazul
    # ceva gen
    # if acc(words) > max_acc:
    #     best_part = current_partition
    #######################NU SCRIE COD SUB ASTA, APELUL RECURSIV ESTE MAI JOS#################################

    if (len(current_partition) > 1):
        for i in range(pos, len(current_partition)):
            if i + 2 < len(current_partition):
                new_partition = current_partition[0: i] + [current_partition[i] + current_partition[i + 1]] \
                                + current_partition[i + 2: len(current_partition)]
                partition(new_partition, i)
            elif i + 1 < len(current_partition):
                new_partition = current_partition[0: i] + [current_partition[i] + current_partition[i + 1]]
                partition(new_partition, i)


partition(initial_part, 0)