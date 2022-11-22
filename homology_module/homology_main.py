# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 09:37:07 2022

@author: User
"""
import sys
from datetime import datetime
from homology_helperfunctions import sequence2string, LongestMatches, colour_matches, homology_output
from sequences import transcripts_adcy1, transcripts_adcy8

#from software_comparisons.main import recommended_sense_sequences, duplicate_sense_sequences

#####################################################
# 1. CHOOSE 2 SEQUENCES TO COMPARE, OR ENTER YOUR OWN
#####################################################

def select_sequences_new(transcripts_gene, first=True):
    
    # create a string containing all dictionary keys
    keys_string = ''
    for key, value in transcripts_gene.items():
        keys_string = keys_string + key + ","
    # remove last comma
    keys_string = keys_string[:-1]
    
    if first==True:
        key = input("Select your first sequence: " + keys_string + ": ")
    elif first==False:
        key = input("Select your second sequence: " + keys_string + ": ")
        
    return key 

key_seq1 = select_sequences_new(transcripts_adcy8,first=True)
key_seq2 = select_sequences_new(transcripts_adcy8,first=False)

sequence1 = transcripts_adcy8[key_seq1]
sequence2 = transcripts_adcy8[key_seq2]
        
##############################################################################
# 2. FIND MATCHES BETWEEN THE SEQUENCES YOU CHOSE IN STEP (1) & HIGHLIGHT THEM
##############################################################################

def compare_sequences(sequence1,sequence2,key1,key2):
    filename = input("Please enter a name under which the list of matches will be stored: ")
    
    # add a timestamp to the filename
    currenttime = datetime.now()
    date = str(currenttime.year) + str(currenttime.month) + str(currenttime.day)
    time = str(currenttime.hour) + str(currenttime.minute) + str(currenttime.second)
    filename = filename + '_' + date + '_' + time
    
    list_matches_seq1_seq2 = LongestMatches(sequence1,sequence2,filename)
    print("There is " + str(len(list_matches_seq1_seq2)) + "regions of homology >= 19nt between " + key1 + " and " + key2 + " .")
    
    coloured_seq1_seq2 = colour_matches(sequence1,list_matches_seq1_seq2)
    coloured_seq2_seq1 = colour_matches(sequence2,list_matches_seq1_seq2)
    
    return list_matches_seq1_seq2, coloured_seq1_seq2, coloured_seq2_seq1

list_matches_seq1_seq2,coloured_seq1_seq2,coloured_seq2_seq1 = compare_sequences(sequence1,sequence2,key_seq1,key_seq2)
print("HOMOLOGOUS REGIONS ON " + key_seq1 + " ARE HIGHLIGHTED IN GREEN")
print(coloured_seq1_seq2)
print("------------------------------------------------------------")
print("HOMOLOGOUS REGIONS ON " + key_seq2 + " ARE HIGHLIGHTED IN GREEN")
print(coloured_seq2_seq1)

##################################################################
# 3. SEE WHETHER LIST OF SENSE SEQUENCES FALL INTO HOMOLOGOUS REGIONS OF CHOICE

def U2T(sequence_Us):
    
    # create a copy of original string
    sequence_Ts = sequence_Us
    
    # Replace all instances of U with T
    sequence_Ts = sequence_Ts.replace('U','T')
        
    return sequence_Ts

def T2U(sequence_Ts):
    sequence_Us = sequence_Ts
    sequence_Us = sequence_Us.replace('T','U')
    return sequence_Us

def sense_homologous(sense_sequences,list_matches_seq1_seq2):
    
    sense_homol_list = []
    
    for homol in list_matches_seq1_seq2:
        for sense in sense_sequences:
            sense = U2T(sense[:-2])
            if sense in homol:
                print("targets matching region")
                sense = T2U(sense)
                print(sense)
                sense_homol_list.append(sense)
                
    return sense_homol_list

# human AC1 TV1
#triplicate_sense_sequences = ['CCUUGUUAUUAGAGGAGAATT','CCUCACAUUGCUAAAUUAATT','AGAAACACGAUGAGUACAUTT','UCCUUCAUUCUUUGUGAAATT','CUCCUAUGUGCAUGUCUAATT','CUGUUUGUUCAUACACUUATT','CCUGUCAUUGCGUCUAAUUTT','UAGUCACAAUGAAGAUGAATT','GGACGAAGUUUCAGAAUUGTT','GGAACUUAGUUUGAAUUUGTT','CCAGAUUCAAUAUGUUCUATT','ACAAGGACAUAGAGAAGAUTT','GGUAACUUCUCAUGAUAGATT','AGGACAUAGAGAAGAUCAATT','CUGAUUCUCUCAGAUAUAATT','GGAAAGAUUCGAAGUGUCATT','GCCUUGUCUACCUUCUAAUTT','GUCUGUUUCACUACCUUAATT','GGCACUUAUUGAGAAUUAATT']

# mouse AC1
#triplicate_sense_sequences = ['CUGUAAGUCUAACAAGAAUTT','UGGCAUCUUCUUAAAUCAATT','GGCAUCUUCUUAAAUCAAUTT','GUGAUAAACAACCUUCUUUTT','CACCUAGAUAACUAUCUUATT','CCGAUAUAAUAGCAUCAUUTT','CUGUGCUUAAUUCAAAUCATT','CUCCAGUUACAGCUCUUACTT','GUGCUUAAUUCAAAUCAAUTT','GGACUUGACAUGAUCGAUATT','GUGUCAUCUCACAUAUAGATT','AGGAUUCUCUCCAAAUUAUTT','UCCAGUUACAGCUCUUACATT','UGCCUUCAUCCCUGUUAAATT','GAGAAAGGAUUGAGAAAGUTT','CUGAAGAUGAGGACAUGAATT','CGAGAUGAGUAAUUGAAUATT','GAGUCAAGCUGGACAACAATT']
#matches_AC1mouse_humanTV1 = ['CGGAACATGGACCTCTACTACCAGTCCTACTCCCAGGTGGGCGTCATGTTTGCCTCCATCCCCAACTTCAATGACTTCTACAT','CTCCTTTTGGTCACCTTCGTGTCCTATGCCTTGCTGCCCGTGCGCAGCCT','GCCAAGCGCCCACGTCTCTGGAGGACGCTCGGTGCCAATGCC','CTGCTGGTGCAGCTCATGCACTGCCGGAAAATGTTCAAGGC','GCTCGCAGGCCCCAGTACGACATCTGGGGAAACACAGTCAA','CACACCATGCCCTGCTCTGCTGCCTGGTGGGCACCCTCCC','CCGCTGCATGGCGCTGAGATGGCGGGGGCGCCGCGCGGC','TGTACAATATTCATGTACAAATGTTAGAGCCATT','TGCAACTTTTCTACTGAGTGTTTGCACTATACT','TCCCAGTGCACAGCCCAGGAGCTGGTGAAACT','CGGGTCCAGTGTTTTCCAGGGTGCCTGACGAT','TACTCCACTAGAGGCTGTGCTTAATTCAAATC','CAGGTGACTGAGGAAGTCCACCGGCTGCTGA','AGTAATTGAATAATTTGTCCTATTTTTATTT','GAGCTGGAGGCGCTGTTCCGCGGCTACACG','TACTTTCTAGAAGGCAGGACTGATGGAAAC','TGTATTATATTGCCTTATTTATTTTTAATC','ACCTTCCAGTCTTTTTCAAGATTGTTAAAT','GACTTCCTGAAGCCCCCTGAGAGGATTTT','GAAGCCCGCCAGACAGAGCTGGAGATGGC','AACTTGTTTCTCACCTCCCACCAGCAACC','ATCAATACGGGTCTATTTTTATGTCAACT','TGCGGCTGGAGCAGGCGGCCACGCTGAA','GGCAGGGTCCTCTGTGGTGTCCTGGGC','GGCTAAGAAGTCCATCTCCTCCCACCT','GCCCACTGCTGTGTGGAGATGGGACT','CGCGTCAACAGGTACATCAGCCGCCT','GTTCTGGATGAAATCAACTACCAGTC','CCCTCATCCTGGCTGCCTTATTTGG','GGCGCGGGCGAGCCCGGGGGCGC','CACAAGATTTACATCCAGAGGCA','GACAATGTGAGCATCCTGTTTGC','CTGAAGTACAAACATGTCGAACG','TACCACCAGCTTCAGGACGAGTA','TTCATAGTGGTCTTAATCTACTC','GTGGCCAGTCGGATGGATAGCAC','TCTTCAGCCTCACCTTCGCGCT','AGCCAGAGGCAGGTCTTCTGGA','GAAGCACAAGTCTCAGGGGACC','AATGTGAATGTACATTTCTTAA','TCTTATTTAACAAAAATAAAGG','TTCACCAGCGCCGTTGTCCTC','TTCGCGCTGGGCGGCCCCGC','TTTATTGTGCCATCCCATCG','AGGATGAAGTTCAAGACTGT','TGTGTGGTGGGCTGCCTGCC','CGGGTGTCCTCCTTGCCAAA','CAGCACTTCCTCATGTCCAA','ATATGCAAGCCATTTGCACT','CCCAGCTGCAGCAGGTCGG','GGCTGGACTACCTCTGGGC','ACATCTCCATCATCAGCAA','CTGTCATAGAAGCAATAAC','GTAAGCCCAAAGCCCACTT']
# duplicate_sense_sequences = [duplicate_sense_sequences = ['GAGUUCCUUACUUAAAAAATT', 'CCAUUCUGUUCCACACAUATT', 'CUCCAGUUACAGCUCUUACTT', 'UCCAGUUACAGCUCUUACATT', 'UCCUUACUUAAAAAAAAAATT', 'CCAGUUACAGCUCUUACAUTT', 'AGUUACAGCUCUUACAUUCTT', 'CAAAUGUUAGAGCCAUUUATT', 'CAGAUCUGUUCAGUAGCUUTT', 'GAGUCAAGCUGGACAACAATT', 'GGAGAAUUCUGGAGAGUGUTT', 'GCCAUUUAGGUAGGAUUCUTT', 'CAGUAGCUUAUAAAACAAATT', 'GGAAGCAACUGGCUGGAAATT', 'GAAGCAACUGGCUGGAAAUTT', 'AGGUAGGAUUCUCUCCAAATT', 'AGAGUGUCAUCUCACAUAUTT', 'GAGUGUCAUCUCACAUAUATT', 'AGGAUUCUCUCCAAAUUAUTT', 'GUGUCAUCUCACAUAUAGATT', 'GGAUUCUCUCCAAAUUAUUTT', 'GUAGGAUUCUCUCCAAAUUTT', 'GGUGAAACUGCUCAAUGAATT', 'UCCAAAUUAUUUAUUUUAATT', 'CUGUGCUUAAUUCAAAUCATT', 'UGUGCUUAAUUCAAAUCAATT', 'GUGCUUAAUUCAAAUCAAUTT', 'UGGCAAGUUCGAUGAGUUATT', 'UGAAGAUACUCAGUUUCAATT', 'GAAGAUACUCAGUUUCAAUTT', 'AAGAUACUCAGUUUCAAUATT', 'AAGCCAGGUGAAAUCUGUATT', 'GAUACUCAGUUUCAAUACATT', 'CAGGUGAAAUCUGUAAGAATT', 'AGGUGAAAUCUGUAAGAACTT', 'GGUGAAAUCUGUAAGAACUTT', 'CUCAGUUUCAAUACAGGAATT', 'CCAGGUGAAAUCUGUAAGATT', 'CCAGAGCAAGUGAGUAUAUTT', 'GCAAGUGAGUAUAUGGUGATT', 'GUGAGUAUAUGGUGACUUUTT', 'CUUGAUCACUUGUACCAAATT', 'UGAUGCUAUCGUCUAUACATT', 'GAUGCUAUCGUCUAUACAATT', 'GCAUGCAUGUCUAAUAAGATT', 'UGUUGCCUUCAUCCCUGUUTT', 'UUGCCUUCAUCCCUGUUAATT', 'UGCCUUCAUCCCUGUUAAATT', 'AUGUCUAAUAAGACAUAAATT', 'GUCUAAUAAGACAUAAAAUTT', 'UCCCUGUUAAAAUUGAGUATT', 'CCCUGUUAAAAUUGAGUAUTT', 'CCUGGAGCUCUCAGUCUAATT', 'GCAGCCUUCCGAUCCUUAUTT', 'CGUAAUAGUGGCAGGGAAATT', 'AACUUCAAUGACUUCUACATT', 'GGAGAGAUGCUAACGUACUTT', 'CUUCAAUGACUUCUACAUATT', 'UAUGAGAACUCGAUGAUUATT', 'GAGAUGCUAACGUACUUUCTT', 'ACUUCAAUGACUUCUACAUTT', 'GAUGCUAACGUACUUUCUATT', 'GGAAAGAACACUGCUACAUTT', 'UGAGAACUCGAUGAUUAUATT', 'CUCGAUGAUUAUAUUCACATT', 'UCGAUGAUUAUAUUCACAATT', 'CACUGAAGAAAAAUAAAUATT', 'CCUAUCCUUGAAUCGUGAUTT', 'AUCCUUGAAUCGUGAUGUUTT', 'UCCUUGAAUCGUGAUGUUUTT', 'GGACUUGACAUGAUCGAUATT', 'GAACUGAGGCACCUAGAUATT', 'GAGGCACCUAGAUAACUAUTT', 'UGCACCUUAGUUUGAAUUUTT', 'GCACCUAGAUAACUAUCUUTT', 'CACCUAGAUAACUAUCUUATT', 'ACCUAGAUAACUAUCUUAUTT', 'GGGUAACCUCUCACAAUAGTT', 'CCUAGAUAACUAUCUUAUATT', 'UAGAUAACUAUCUUAUACATT', 'AGAUAACUAUCUUAUACAUTT', 'GAUAACUAUCUUAUACAUATT', 'GCACCUUAGUUUGAAUUUGTT', 'UAACUAUCUUAUACAUAAATT', 'AACUAUCUUAUACAUAAAUTT', 'UGUGCACCUUAGUUUGAAUTT', 'CUCACAAUAGAUUUGUAUATT', 'CUAUCUUAUACAUAAAUCATT', 'CUUCACACAGACACACUGATT', 'CUGACACCAUAGAAUAGAATT', 'UCACUUGGGACACUUGAUATT', 'AGACUACAUCCACUUCAGATT', 'GGACACUUGAUAUCCUAUATT', 'GACACUUGAUAUCCUAUAATT', 'CGAGAUCAUUGCCGACUUUTT', 'GCCAAGUGCUGGUCAUUUATT', 'GGUGUCUUGGACGCUGUAATT', 'GGACGCUGUAAGUCUAACATT', 'GACGCUGUAAGUCUAACAATT', 'CGCUGUAAGUCUAACAAGATT', 'GCUGUAAGUCUAACAAGAATT', 'CUGUAAGUCUAACAAGAAUTT', 'CUUUGACACCAGAGAGAAATT', 'GUAAGUCUAACAAGAAUCATT', 'GGUUCCUGAGGCGUGGUAUTT', 'UCUUUGGUGUGAACAUGUATT', 'UCUUCUUUGGUGUGAACAUTT', 'UGAGAGAAAGCAACCUUUATT', 'CAGAGAGAAAACGUGUUGATT', 'GCGUGGUAUUUUGUUGUAATT', 'AGAAUCAAGCCUUCGUUUATT', 'GUGGUAUUUUGUUGUAACATT', 'GAAUCAAGCCUUCGUUUAUTT', 'UGCUGAGAAUUAGCAUUUCTT', 'UCACAGCAGACACGAUGAATT', 'CAGUCUUUUUCAAGAUUGUTT', 'GUCUUUUUCAAGAUUGUUATT', 'UGCUUUUUAAUGGCUUCAATT', 'CACGAUGAAUGUGGUUGAATT', 'CUGCAUUCCUCCAAGGUUATT', 'CGAUGAAUGUGGUUGAAAUTT', 'UUGUUAAAUCGAGAUGAGUTT', 'CGAGAUGAGUAAUUGAAUATT', 'GAGAUGAGUAAUUGAAUAATT', 'CAAGGAAGGUCAAUCAUUATT', 'ACCAUUCCGAGCAAGAAAUTT', 'CCAUUCCGAGCAAGAAAUUTT', 'UGAAUAAUUUGUCCUAUUUTT', 'GCCUACUACUAAGUCUCUUTT', 'UCUUUACUCUGAAGUACAATT', 'UGGCUUGAUAAAAUUAAUATT', 'UUGUCCUAUUUUUAUUUAATT', 'GUACAAACAUGUCGAACGATT', 'CCUGUACCUACAUAGUCAATT', 'GUGAGCACAGGUCCAAUAATT', 'ACAUGUCGAACGAGAACAATT', 'GACCGAUAUAAUAGCAUCATT', 'GGCCUGAAGGAUUGAGAAATT', 'CCGAUAUAAUAGCAUCAUUTT', 'GGAUGGCAGCUUGGAUAUUTT', 'GAUAUAAUAGCAUCAUUCUTT', 'GCCUUAUAGUGCCCUUGAUTT', 'UUGAGAAAGGAUUGAGAAATT', 'GUAGCAGUUUCAAGUAUGATT', 'GAGAAAGGAUUGAGAAAGUTT', 'AUGUUAAUGUGAAUGUACATT', 'GGAUAUUAUGUGGGUCUUUTT', 'GGGGUAAAUUGAUCAAACATT', 'UCUUAAGAUUGCACUUAUATT', 'UAGUCUCAAAGGUUUUGAATT', 'AUGUGAAUGUACAUUUCUUTT', 'UGAUCAAACAUUCAUUCCUTT', 'GAUCAAACAUUCAUUCCUATT', 'UCAAACAUUCAUUCCUAGUTT', 'CUGUGGUUCAUUCCAUAAATT', 'GGAAGGUCCACAUCACAAATT', 'AACAUUCAUUCCUAGUACUTT', 'UUCCUAGUACUUCCAUUUATT', 'UCCUAGUACUUCCAUUUAGTT', 'CCUAGUACUUCCAUUUAGUTT', 'UACUUCCAUUUAGUUUUGCTT', 'GUCAUAGAAGCAAUAACCATT', 'AUAGAAGCAAUAACCAUAATT', 'UAGAAGCAAUAACCAUAACTT', 'AAGCAAUAACCAUAACCUATT', 'AGCAAUAACCAUAACCUAATT', 'GCAAUAACCAUAACCUAAUTT', 'GUGGCAUCUUCUUAAAUCATT', 'UGGCAUCUUCUUAAAUCAATT', 'GGCAUCUUCUUAAAUCAAUTT', 'GGCUUUGAAUGUUUCUAUATT', 'CCAUGGAGAUGAAGGAAGATT', 'CCACACGUGCAGCCAUAAUTT', 'CCUCAGAAGUGGACAGAAATT', 'CAUAACCUAAUACUGUAGATT', 'AGCUGAUGGCUCACUAAUUTT', 'CACAUUCUGUCACUAAACATT', 'GGCUCACUAAUUUGCACAATT', 'GCUCACUAAUUUGCACAAATT', 'GGGGUCUUAUUUAACAAAATT', 'GGGUCUUAUUUAACAAAAATT', 'GUCUUAUUUAACAAAAAUATT', 'UCAACUACCAGUCCUACAATT', 'GCUUGAACCAAUAGCUCAUTT', 'UUGCACAAAUGGAAUUGUUTT', 'ACCAAUAGCUCAUUUCUAUTT', 'AACAAAAAUAAAGGAGAAATT', 'GUCCUACAACGACUUUGUUTT', 'UUAUCCAAUCAACACAUCATT', 'GUGAUAAACAACCUUCUUUTT', 'GCCCAAGCAGAUUGCUAUUTT', 'CCAAUCAACACAUCAUUAUTT', 'GGUGAUAAACAACCUUCUUTT', 'UCCAAUCAACACAUCAUUATT', 'AUCAACACAUCAUUAUCUATT', 'GAGGAUUUUUCACAAGAUUTT', 'UCGAAUAGGGACAGAGCUATT', 'CAGAUUGCUAUUCCAGAAATT', 'GCUGAGACUGUGCAAAUGATT', 'CAACACAUCAUUAUCUAAUTT', 'GUUGCUGACCUGAAGAUGATT', 'CUGAAGAUGAGGACAUGAATT', 'UGCUAAUACUCAAUACACATT', 'GAAGAUGAGGACAUGAAAUTT', 'AAGAUGAGGACAUGAAAUATT', 'GUGAUAAAAAUGUAUUAUATT', 'AGCAGUAUCUUGAUUUAAATT', 'CAGUAUCUUGAUUUAAAGUTT', 'GGACAUGAAAUACAUUGAATT', 'GGCAGGAGGUUGAUGGUUATT', 'GCAGGAGGUUGAUGGUUAATT', 'GUGCAUGUGAGAUUGCUAUTT', 'GUAUUAUAUUGCCUUAUUUTT', 'GAGUAAGAGGGAAACAGUUTT', 'ACACCUCUUACUGCAUGAATT']
# list_matches_seq1_seq2 = ['CGGAACATGGACCTCTACTACCAGTCCTACTCCCAGGTGGGCGTCATGTTTGCCTCCATCCCCAACTTCAATGACTTCTACAT','CTCCTTTTGGTCACCTTCGTGTCCTATGCCTTGCTGCCCGTGCGCAGCCT','GCCAAGCGCCCACGTCTCTGGAGGACGCTCGGTGCCAATGCC','CTGCTGGTGCAGCTCATGCACTGCCGGAAAATGTTCAAGGC','GCTCGCAGGCCCCAGTACGACATCTGGGGAAACACAGTCAA','CACACCATGCCCTGCTCTGCTGCCTGGTGGGCACCCTCCC','CCGCTGCATGGCGCTGAGATGGCGGGGGCGCCGCGCGGC','TGTACAATATTCATGTACAAATGTTAGAGCCATT','TGCAACTTTTCTACTGAGTGTTTGCACTATACT','TCCCAGTGCACAGCCCAGGAGCTGGTGAAACT','CGGGTCCAGTGTTTTCCAGGGTGCCTGACGAT','TACTCCACTAGAGGCTGTGCTTAATTCAAATC','CAGGTGACTGAGGAAGTCCACCGGCTGCTGA','AGTAATTGAATAATTTGTCCTATTTTTATTT','GAGCTGGAGGCGCTGTTCCGCGGCTACACG','TACTTTCTAGAAGGCAGGACTGATGGAAAC','TGTATTATATTGCCTTATTTATTTTTAATC','ACCTTCCAGTCTTTTTCAAGATTGTTAAAT','GACTTCCTGAAGCCCCCTGAGAGGATTTT','GAAGCCCGCCAGACAGAGCTGGAGATGGC','AACTTGTTTCTCACCTCCCACCAGCAACC','ATCAATACGGGTCTATTTTTATGTCAACT','TGCGGCTGGAGCAGGCGGCCACGCTGAA','GGCAGGGTCCTCTGTGGTGTCCTGGGC','GGCTAAGAAGTCCATCTCCTCCCACCT','GCCCACTGCTGTGTGGAGATGGGACT','CGCGTCAACAGGTACATCAGCCGCCT','GTTCTGGATGAAATCAACTACCAGTC','CCCTCATCCTGGCTGCCTTATTTGG','GGCGCGGGCGAGCCCGGGGGCGC','CACAAGATTTACATCCAGAGGCA','GACAATGTGAGCATCCTGTTTGC','CTGAAGTACAAACATGTCGAACG','TACCACCAGCTTCAGGACGAGTA','TTCATAGTGGTCTTAATCTACTC','GTGGCCAGTCGGATGGATAGCAC','TCTTCAGCCTCACCTTCGCGCT','AGCCAGAGGCAGGTCTTCTGGA','GAAGCACAAGTCTCAGGGGACC','AATGTGAATGTACATTTCTTAA','TCTTATTTAACAAAAATAAAGG','TTCACCAGCGCCGTTGTCCTC','TTCGCGCTGGGCGGCCCCGC','TTTATTGTGCCATCCCATCG','AGGATGAAGTTCAAGACTGT','TGTGTGGTGGGCTGCCTGCC','CGGGTGTCCTCCTTGCCAAA','CAGCACTTCCTCATGTCCAA','ATATGCAAGCCATTTGCACT','CCCAGCTGCAGCAGGTCGG','GGCTGGACTACCTCTGGGC','ACATCTCCATCATCAGCAA','CTGTCATAGAAGCAATAAC','GTAAGCCCAAAGCCCACTT']


# rat AC1
#triplicate_sense_sequences = ['GGGTAAAGCTGGACAACAATT','GAGGATATTTCACAAGATTTT','GGACTTGACATGATCGATATT','GGAACATGGATCTCTATTATT','GGTGAAACTGCTCAATGAATT','CTGAAGTAGACCTGAACATTT']
#matches_AC1rat_humanTV1 = ['CTCCTTTTGGTCACCTTCGTGTCCTATGCCTTGCTGCCCGTGCGCAGCCT','CACAAGATTTACATCCAGAGGCACGACAATGTGAGCATCCTGTTTGC','GCTCGCAGGCCCCAGTACGACATCTGGGGAAACACAGTCAA','TACCAGTCCTACTCCCAGGTGGGCGTCATGTT','CCTGCTCTGCTGCCTGGTGGGCACCCTCCC','GCCAAGCGCCCACGTCTCTGGAGGACGCT','GTCTGCTACCTGCTGGTGCAGCTCATGCA','GAAGCCCGCCAGACAGAGCTGGAGATGGC','TGCGGCTGGAGCAGGCGGCCACGCTGAA','GGGTCCAGTGTTTTCCAGGGTGCCTGAC','GGCAGGGTCCTCTGTGGTGTCCTGGGC','CTGGCGCTGGCCGAGCTGCTGGGCGC','GACTTCCTGAAGCCCCCTGAGAGGAT','GCCCACTGCTGTGTGGAGATGGGACT','TACTTTCTAGAAGGCAGGACTGATGG','GTCAACAGGTACATCAGCCGCCT','GTGGTCTTAATCTACTCAGTAGC','GTGGCCAGTCGGATGGATAGCAC','CAGGTGACTGAGGAAGTCCACCG','TCTTCAGCCTCACCTTCGCGCT','TTCACCAGCGCCGTTGTCCTC','TTCGCGCTGGGCGGCCCCGC','GCCCAGGAGCTGGTGAAACT','GGCCTCACCCAGCCCAAGAC','CGCAAGTGGCAGTACGACGT','TTTATTGTGCCATCCCATCG','TGCCGGAAAATGTTCAAGGC','GACCTGAACTTCTTTACCCT','CTGCCTTGGGCCTGGAGCTC','CGGGTGTCCTCCTTGCCAAA','ATCCTCTTCAACCTCCTGCC','CAGCACTTCCTCATGTCCAA','GCCTCCATCCCCAACTTCAA','CCCAGCTGCAGCAGGTCGG','GGCTGGACTACCTCTGGGC']
# duplicate_sense_sequences = [['AGCUUCAAGAUGAGUACUUTT','UCUUCUUUGGUGUGAACAUTT','UCUUUGGUGUGAACAUGUATT','UGGACAAGGACUUCUACAATT','CGUAAUGACCUGUGAGGAUTT','UCUACAAGGACCUGGAGAATT','AGAGGGUAAAGCUGGACAATT','CCUGUGAGGAUGAUGACAATT','GGGUAAAGCUGGACAACAATT','GGUUUGAUUCUCUCGGAUATT','GUUUGAUUCUCUCGGAUAUTT','GGGAGAGAUGCUAACGUACTT','AACUUCAACGACUUCUACATT','CUUCAACGACUUCUACAUATT','ACUUCAACGACUUCUACAUTT','GAGAUGCUAACGUACUUUCTT','GAUGCUAACGUACUUUCUATT','GCUGGUGAAACUGCUCAAUTT','AGCUGGUGAAACUGCUCAATT','UGGUGAAACUGCUCAAUGATT','GGUGAAACUGCUCAAUGAATT','CCAUUGGGAGUACCUAUAUTT','UCAACUACCAGUCCUACAATT','ACAUAGAACUGGAUGGCAATT','UCAAUGAACUCUUUGGCAATT','CCUCGGAGAAGCUCAGAAATT','CCUGAGAGGAUAUUUCACATT','GAGAGGAUAUUUCACAAGATT','AGAGGAUAUUUCACAAGAUTT','GAGGAUAUUUCACAAGAUUTT','UCUUUACCCUCAAGUACAATT','GGAUAUUUCACAAGAUUUATT','GGACUUGACAUGAUCGAUATT','UGGCAAGUUCGAUGAGUUATT','GGGAAGAAUUCAGGUGACUTT','CCUCAAGUACAAGCAUGUUTT','CUCAAGUACAAGCAUGUUGTT','CAAGUACAAGCAUGUUGAATT','AGAUUUACAUCCAGAGGCATT','CAAGCAUGUUGAACGGGAATT','GCAUGUUGAACGGGAACAATT','CAUGUUGAACGGGAACAAATT','GCUCAUGCAUUGCCGGAAATT','GCGGCUGGAAGAUGAGAAUTT','GGCUGGAAGAUGAGAAUGATT','UGGAAGAUGAGAAUGAGAATT','GGAAGAUGAGAAUGAGAAATT','CCGGAACAUGGAUCUCUAUTT','GGAACAUGGAUCUCUAUUATT','UGAGAUCAUUGCUGACUUUTT','GCGAAGGAUGUUUCCUUAUTT','CUGAAGUAGACCUGAACAUTT']]

# sheep AC1 
#triplicate_sense_sequences = ['GGUAACUUCUCAUGAUAGATT','CUGGAUUCAGUUUGUUCUATT','AGCAACUACUAGAGAGUAATT','CAGUUUGUUCUACACUAAUTT','GGGAUGACAUGGAGAAAGUTT','GCACACAGUUCUUCACUUATT','CAGAUUCCACUCCCAUUUATT','CACAGUUCUUCACUUACAUTT','AGAAAGUGAAGCUGGAUAATT','GGGAAGGAACUGUCUAGAATT','GGAAGGAACUGUCUAGAAATT','CUGAUUCUGUCAGACAUAATT','GCAGCAACCUGGAUAUAAUTT','CCCAGAUUGUCAUGUAACATT','CAUCACACACAUAGGAAAUTT','AGCAGGAUUGGAUUCUAAATT','CUAUAGGAAUACAGGAAUATT','CAGCAAAGACUUACAACAUTT','CGAAUGACAACAACUCAAUTT','AGAAUUGGAUGGUGAAGAATT']

# rat AC 1 duplicates
# duplicate_sense_sequences = ['AGCUUCAAGAUGAGUACUUTT','UCUUCUUUGGUGUGAACAUTT','UCUUUGGUGUGAACAUGUATT','UGGACAAGGACUUCUACAATT','CGUAAUGACCUGUGAGGAUTT','UCUACAAGGACCUGGAGAATT','AGAGGGUAAAGCUGGACAATT','CCUGUGAGGAUGAUGACAATT','GGGUAAAGCUGGACAACAATT','GGUUUGAUUCUCUCGGAUATT','GUUUGAUUCUCUCGGAUAUTT','GGGAGAGAUGCUAACGUACTT','AACUUCAACGACUUCUACATT','CUUCAACGACUUCUACAUATT','ACUUCAACGACUUCUACAUTT','GAGAUGCUAACGUACUUUCTT','GAUGCUAACGUACUUUCUATT','GCUGGUGAAACUGCUCAAUTT','AGCUGGUGAAACUGCUCAATT','UGGUGAAACUGCUCAAUGATT','GGUGAAACUGCUCAAUGAATT','CCAUUGGGAGUACCUAUAUTT','UCAACUACCAGUCCUACAATT','ACAUAGAACUGGAUGGCAATT','UCAAUGAACUCUUUGGCAATT','CCUCGGAGAAGCUCAGAAATT','CCUGAGAGGAUAUUUCACATT','GAGAGGAUAUUUCACAAGATT','AGAGGAUAUUUCACAAGAUTT','GAGGAUAUUUCACAAGAUUTT','UCUUUACCCUCAAGUACAATT','GGAUAUUUCACAAGAUUUATT','GGACUUGACAUGAUCGAUATT','UGGCAAGUUCGAUGAGUUATT','GGGAAGAAUUCAGGUGACUTT','CCUCAAGUACAAGCAUGUUTT','CUCAAGUACAAGCAUGUUGTT','CAAGUACAAGCAUGUUGAATT','AGAUUUACAUCCAGAGGCATT','CAAGCAUGUUGAACGGGAATT','GCAUGUUGAACGGGAACAATT','CAUGUUGAACGGGAACAAATT','GCUCAUGCAUUGCCGGAAATT','GCGGCUGGAAGAUGAGAAUTT','GGCUGGAAGAUGAGAAUGATT','UGGAAGAUGAGAAUGAGAATT','GGAAGAUGAGAAUGAGAAATT','CCGGAACAUGGAUCUCUAUTT','GGAACAUGGAUCUCUAUUATT','UGAGAUCAUUGCUGACUUUTT','GCGAAGGAUGUUUCCUUAUTT','CUGAAGUAGACCUGAACAUTT']

# mouse AC8 triplicates
#triplicate_sense_sequences = ['GCCCUAACAAGAAAUUCAATT','CCCUAACAAGAAAUUCAAUTT','CAGCACACCUCCAAAUUAATT','GCAUCAUCAAGAGCCAUUATT','CAGGAAUCUUCAUCAGUUATT','GAGGAAAUUAACAAGAGAATT','GGAGAAAGACAGAGACAAUTT','ACAGCAAUGUGAAGAUAAATT','GCAUACAAGAGAUCAACAATT','GGUUUGUCGUCCUGGAAAUTT','CAGAACGAAGCACGAUGUUTT','GAGACAAUGAGGAGCUGUATT','GAACGAAGCACGAUGUUGATT']

# rat AC8 triplicates
#triplicate_sense_sequences = ['GCCCUAACAAGAAAUUCAATT','GAGCUGUAUUCUCAAUCCUTT','GCAUCAUCAAGAGCCAUUATT','AGGACAUAGAGAAGAUUAATT','GGAGAAAGACAGAGACAAUTT','GCGAGGAACUCUAUACCAUTT','ACAGCAAUGUGAAGAUAAATT','GGGAACACAAUGAGAACAUTT','CAGCGAACAAGAAGGGAAATT','GCAUACAAGAGAUCAACAATT','GUUGGAUUAACGAGACCUATT','GAACGAAGCAUGAUGUUGATT','GAGACAAUGAGGAGCUGUATT','GCUCAUUGCUGUGUUGAAATT','AGGACUGUCACCAGAGAAATT']

# sheep AC8 triplicates
triplicate_sense_sequences = ['GAGGAAAUUAACAAGAGAATT','GUGCAUUUAUCGUUCUUCUTT','CCAAAGAGGAGAUCAACGATT','CUGGAGAUGAUCAACGAUATT','UGGAGAUGAUCAACGAUAUTT','GAGCUGUAUUCUCAAUCCUTT']


#list_matches_seq1_seq2 = ['CGGAACATGGACCTCTACTACCAGTCCTACTCCCAGGTGGGCGTCATGTTTGCCTCCATCCCCAACTTCAATGACTTCTACAT','CTCCTTTTGGTCACCTTCGTGTCCTATGCCTTGCTGCCCGTGCGCAGCCT','GCCAAGCGCCCACGTCTCTGGAGGACGCTCGGTGCCAATGCC','CTGCTGGTGCAGCTCATGCACTGCCGGAAAATGTTCAAGGC','GCTCGCAGGCCCCAGTACGACATCTGGGGAAACACAGTCAA','CACACCATGCCCTGCTCTGCTGCCTGGTGGGCACCCTCCC','CCGCTGCATGGCGCTGAGATGGCGGGGGCGCCGCGCGGC','TGTACAATATTCATGTACAAATGTTAGAGCCATT','TGCAACTTTTCTACTGAGTGTTTGCACTATACT','TCCCAGTGCACAGCCCAGGAGCTGGTGAAACT','CGGGTCCAGTGTTTTCCAGGGTGCCTGACGAT','TACTCCACTAGAGGCTGTGCTTAATTCAAATC','CAGGTGACTGAGGAAGTCCACCGGCTGCTGA','AGTAATTGAATAATTTGTCCTATTTTTATTT','GAGCTGGAGGCGCTGTTCCGCGGCTACACG','TACTTTCTAGAAGGCAGGACTGATGGAAAC','TGTATTATATTGCCTTATTTATTTTTAATC','ACCTTCCAGTCTTTTTCAAGATTGTTAAAT','GACTTCCTGAAGCCCCCTGAGAGGATTTT','GAAGCCCGCCAGACAGAGCTGGAGATGGC','AACTTGTTTCTCACCTCCCACCAGCAACC','ATCAATACGGGTCTATTTTTATGTCAACT','TGCGGCTGGAGCAGGCGGCCACGCTGAA','GGCAGGGTCCTCTGTGGTGTCCTGGGC','GGCTAAGAAGTCCATCTCCTCCCACCT','GCCCACTGCTGTGTGGAGATGGGACT','CGCGTCAACAGGTACATCAGCCGCCT','GTTCTGGATGAAATCAACTACCAGTC','CCCTCATCCTGGCTGCCTTATTTGG','GGCGCGGGCGAGCCCGGGGGCGC','CACAAGATTTACATCCAGAGGCA','GACAATGTGAGCATCCTGTTTGC','CTGAAGTACAAACATGTCGAACG','TACCACCAGCTTCAGGACGAGTA','TTCATAGTGGTCTTAATCTACTC','GTGGCCAGTCGGATGGATAGCAC','TCTTCAGCCTCACCTTCGCGCT','AGCCAGAGGCAGGTCTTCTGGA','GAAGCACAAGTCTCAGGGGACC','AATGTGAATGTACATTTCTTAA','TCTTATTTAACAAAAATAAAGG','TTCACCAGCGCCGTTGTCCTC','TTCGCGCTGGGCGGCCCCGC','TTTATTGTGCCATCCCATCG','AGGATGAAGTTCAAGACTGT','TGTGTGGTGGGCTGCCTGCC','CGGGTGTCCTCCTTGCCAAA','CAGCACTTCCTCATGTCCAA','ATATGCAAGCCATTTGCACT','CCCAGCTGCAGCAGGTCGG','GGCTGGACTACCTCTGGGC','ACATCTCCATCATCAGCAA','CTGTCATAGAAGCAATAAC','GTAAGCCCAAAGCCCACTT']

sense_homol_list = sense_homologous(triplicate_sense_sequences,list_matches_seq1_seq2)


"""
sense_homol_duplicates = sense_homologous(duplicate_sense_sequences,list_matches_seq1_seq2)
sense_homol = sense_homologous(recommended_sense_sequences,list_matches_seq1_seq2)                
""" 

