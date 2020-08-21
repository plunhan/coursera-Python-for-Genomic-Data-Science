from collections import Counter

def count_records(fileName):
    i = 0
    with open(fileName, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line[0] == '>':
                i += 1
    return i

def find_longest_and_shortest_sequence(fileName):
    record_dict = {}
    flag = 0
    max_length = 0
    min_length = 10000000000
    f = open(fileName, 'r')
    sequence = ''
    identifier = ''
    while True:
        line = f.readline().split('\n')[0]
        if not line:
            record_dict[identifier] = len(sequence)
            if len(sequence) > max_length:
                max_length = len(sequence)
            if len(sequence) < min_length:
                min_length = len(sequence) 
            break
        if line[0] == '>':
            if flag == 1: 
                record_dict[identifier] = len(sequence)
                if len(sequence) > max_length:
                    max_length = len(sequence)
                if len(sequence) < min_length:
                    min_length = len(sequence) 
            identifier = line.split()[0][1:]
            sequence = ''
            flag = 1
        else: 
            sequence += line
    '''
    The structure of record_dict is as follows: 
    key - identifier.
    value - the length of corresponding sequence.
    '''
    f.close()
    return max_length, min_length

def find_longest_ORF_in_a_string(string, reading_frame_number):
    '''
    This function returns the starting position and length of the longest ORF in the sequence. 
    position, length = find_longest_ORF_in_a_string(string, reading_frame_number)
    '''
    pos_start = [] # record position of start codons
    pos_stop = [] # record position of stop codons
    stop_codons = set(['TAA', 'TAG', 'TGA'])
    for i in range(reading_frame_number-1, len(string), 3):
        if i+3 >= len(string):
            break
        if string[i:i+3] == 'ATG':
            pos_start.append(i)
        elif string[i:i+3] in stop_codons:
            pos_stop.append(i)
    pos_start.sort()
    pos_stop.sort()
    max_length = 0
    max_pos = 0
    for start in pos_start: 
        for stop in pos_stop: 
            if start+3 < stop: 
                length = stop - start + 3
                if length > max_length:
                    max_pos, max_length = start+1, length
                break
    return max_pos, max_length

def find_longest_ORF(fileName, reading_frame_number):
    record_dict = {}
    flag = 0
    f = open(fileName, 'r')
    while True:
        line = f.readline().split('\n')[0]
        if not line:
            record_dict[identifier] = sequence
            break
        if line[0] == '>':
            if flag == 1: 
                record_dict[identifier] = sequence
            identifier = line.split()[0][1:]
            sequence = ''
            flag = 1
        else: 
            sequence += line
    '''
    The structure of record_dict is as follows: 
    key - identifier.
    value - the length of corresponding sequence.
    '''
    f.close()
    max_key, max_pos, max_length = '', 0, 0
    for key, value in record_dict.items():
        max_pos_current, max_length_current = find_longest_ORF_in_a_string(value, reading_frame_number)
        if max_length_current > max_length: 
            max_key, max_pos, max_length = key, max_pos_current, max_length_current
    return max_key, max_pos, max_length

def find_longest_ORF_for_specific_identifier(fileName, identifier_target):
    flag = 0
    sequence = ''
    f = open(fileName, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        if line.startswith('>'): 
            if flag == 1: 
                break
            identifier = line[1:].split()[0]
            if identifier == identifier_target: 
                flag = 1
        elif flag == 1: 
            sequence = sequence + line.split('\n')[0]
    max_pos1, max_length1 = find_longest_ORF_in_a_string(sequence, 1)
    max_pos2, max_length2 = find_longest_ORF_in_a_string(sequence, 2)
    max_pos3, max_length3 = find_longest_ORF_in_a_string(sequence, 3)
    return max([max_length1, max_length2, max_length3])

def find_most_frequent_repeat(fileName, repeat_length):
    sequences = []
    f = open(fileName, 'r')
    lines = f.readlines()
    f.close()
    flag = 0
    for line in lines:
        if line.startswith('>'):
            if flag == 1:
                sequences.append(sequence)
            flag = 1
            sequence = ''
            continue
        else: 
            line = line.split('\n')[0]
            sequence += line
    sequences.append(sequence)
    repeat_list = []
    for sequence in sequences:
        for i in range(len(sequence)-repeat_length+1):
            repeat_list.append(sequence[i:i+repeat_length])
    repeat_counter = Counter(repeat_list)
    repeat_dict = dict(repeat_counter)
    max_occurrence = repeat_counter.most_common()[0][1]
    max_occurrence_sequence = [key for key in repeat_dict if repeat_dict[key] == max_occurrence]
    return max_occurrence, max_occurrence_sequence

def question_1(FastaFileName):
    print(count_records(FastaFileName))

def question_2_3(FastaFileName):
    max_length, min_length = find_longest_and_shortest_sequence(FastaFileName)
    print('The length of the longest sequence is: %d' % max_length)
    print('The length of the shortest sequence is: %d' % min_length)

def question_4(FastaFileName): 
    identifier, pos, length = find_longest_ORF(FastaFileName, 2)
    print('The length of the longest ORF appearing in reading frame 2 of any of the sequences is: %d' % length)

def question_5(FastaFileName):
    identifier, pos, length = find_longest_ORF(FastaFileName, 3)
    print('The starting position of the longest ORF appearing in reading frame 3 of any of the sequence is: %d' % pos)

def question_6(FastaFileName):
    identifier1, pos1, length1 = find_longest_ORF(FastaFileName, 1)
    identifier2, pos2, length2 = find_longest_ORF(FastaFileName, 2)
    identifier3, pos3, length3 = find_longest_ORF(FastaFileName, 3)
    print(max([length1, length2, length3]))

def question_7(FastaFileName, identifier_target):
    print(find_longest_ORF_for_specific_identifier(FastaFileName, identifier_target))

def question_8(FastaFileName, repeat_length):
    max_occurrence, max_occurrence_sequence = find_most_frequent_repeat(FastaFileName, repeat_length)
    print(max_occurrence)

def question_9(FastaFileName, repeat_length):
    max_occurrence, max_occurrence_sequence = find_most_frequent_repeat(FastaFileName, repeat_length)
    print(len(max_occurrence_sequence))

def question_10(FastaFileName, repeat_length):
    max_occurrence, max_occurrence_sequence = find_most_frequent_repeat(FastaFileName, repeat_length)
    print(max_occurrence_sequence)

def main():
    FastaFileName = 'dna2.fasta'
    identifier_target = 'gi|142022655|gb|EQ086233.1|16'
    question_1(FastaFileName)
    question_2_3(FastaFileName)
    question_4(FastaFileName)
    question_5(FastaFileName)
    question_6(FastaFileName)
    question_7(FastaFileName, identifier_target)
    question_8(FastaFileName, 6)
    question_9(FastaFileName, 12)
    question_10(FastaFileName, 7)

if __name__ == '__main__':
    main()