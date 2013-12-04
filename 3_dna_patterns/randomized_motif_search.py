import random
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
import itertools
import numpy
from greedy_motif_search import make_profile, print_motifs, profile_most_prob, score_motifs, prob_profile, consensus
#from scipy.stats import rv_discrete

def randomized_motif_search(dna, k, t):
    best_motifs = []
    for seq in dna:
        pos = random.randrange(len(seq) - k + 1)
        best_motifs.append(seq[pos:pos + k])

    while True:
        profile = make_profile(best_motifs, k)
        motifs = [profile_most_prob(profile, seq, k) for seq in dna]
        if score_motifs(motifs) < score_motifs(best_motifs):
            best_motifs = motifs
        else:
            return best_motifs

def random_descrete(probs):
    #s = sum(probs)
    #probs = [float(p) / s for p in probs]
    #pos = rv_discrete(values=(numpy.arange(len(probs)), probs)).rvs()
    s = sum(probs)
    probs = [float(p) / s for p in probs]
    intervals = [0]
    for p in probs[:-1]:
        intervals.append(intervals[-1] + p)
    intervals.append(1)
    intervals = intervals[1:]
    x = random.random()
    for i, interval in enumerate(intervals):
        if x <= interval:
            return i

def profile_rand_kmer(profile, seq, k):
    probs = []
    for i in range(len(seq) - k + 1):
        probs.append(prob_profile(seq[i:i + k], profile))
    pos = random_descrete(probs)
    return seq[pos:pos + k]

def gibbs_sampler(dna, k, t, N, M=20):
    def run():
        best_motifs = []
        for seq in dna:
            pos = random.randrange(len(seq) - k + 1)
            best_motifs.append(seq[pos:pos + k])
        best_score = score_motifs(best_motifs)
        motifs = best_motifs[:]
        for _ in range(N):
            i = random.randrange(t)
            profile = make_profile(motifs[:i] + motifs[i + 1:], k)
            motifs[i] = profile_rand_kmer(profile, dna[i], k)
            score = score_motifs(motifs)
            if score < best_score:
                best_motifs, best_score = motifs[:], score

        print_motifs(best_motifs)
        return best_score, best_motifs

    score, motifs = min((run() for i in range(M)))
    return motifs

def main():
    input = '''8 5 100
    CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA
    GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG
    TAGTACCGAGACCGAAAGAAGTATACAGGCGT
    TAGATCAAGTTTCAGGTGCACGTCGGTGAACC
    AATCCACCAGCTCCACGTGCAATGTTGGCCTA'''

    input = '''15 20
CTCTTAACCTACGAGCAGCGGTGAAGCGGACGACATGGCCGAGACAGCACCCACGTGCTGGTGCTAATTACTAAAAAAGCTTGCAGCTGCGATCGCTCCCGGTGTTCCCCGGCGACGTGGAACAATCTTGGCCCTTGTTTACACTAGTCAGCAGGGTTCTGGGATACATCTACTCTTAACCTACGAG
CAGCGGTGAAGCGGACTCTCACAAAGCCCAGGACATGGCCGAGACAGCACCCACGTGCTGGTGCTAATTACTAAAAAAGCTTGCAGCTGCGATCGCTCCCGGTGTTCCCCGGCGACGTGGAACAATCTTGGCCCTTGTTTACACTAGTCAGCAGGGTTCTGGGATACATCTACTCTTAACCTACGAG
GTCTGGCCAAGCCCAGCTTCAATTCCGAGTAAGATTGTGTGCTAGCACTGCAGAATGCCGTAGAGACTCACCGGTATTGGGCAATGTAGCTGGCGGGCTTATATGGTGAAACCATAAACGAACATCTTCGGCACTTTGGCGGTTGAACTCTCAGACGGGGCAACAGTATACTTCCAGTACCTACATT
ACCTGATATGCCAAGTATTCTGCAAATGTGGCTAACTGCCACCTCCAAGGAAAAGCCTCATGGTAAGAAGTACTGTCTTAGCAGAAGACCCTGCAACTGCGCGTGACGTCGTGATTGTCGCATCACCTAAAGGTGCACCGCTGTGGCTCTGCAATGACCCAGGCATCGAAACGTTGAACTGGTGAGC
TACGGACAGCGACCTTCTGCAAAAGTAAAGCAGAGCCGGAACGACGAACACACTTCCTAGTCCATTTTAAGGAGCCATCGATAACAATTCCGGAGATCGTTCCCTGTTAGTTACCGGGAACGGGGGTATGGTCTGTAGGGACCCATCGCGTTCAACGTCAGTCCTTTATTCACGGTCAGTTGATGAT
ACAGCTGTGTGCTTCGTAAGCGTCTCCCCAACTACCACATGTCTGCTACTATCTCTTTTGTAGGCTGGCCTCAACCCTCCTTTCTAACCCTTCACCGTGAAATTAGCGCCAATTATGGTATAACGTCAGGCTTGTACCTGAGCGCAAAAGCCCAGTGTGTTACCTTCGGCCAGAATGCACATCCCCA
TAGTTTTTGTTCCAAGGACCGGGAAAGGGTAGGCTGTACCTAAATCGGAACTAGGCTTTACGGTCACGCAACAATCCTCGCCGATTGCTTTAGATTCTTGGTTGACATGAGCCGCAAATCCCCCTGTATTGCAAAAGCCCACCAGGCCAAGTTACATTCACTGTTCCGGATCTGAATCGACTCACGC
CCGCTTACGAAAGGGAGGCTTCCGATAGACTCATCAATCGCATTAGCCCCACGTCTGCAAAAGCGTCGTGCGCGCTCAAGCATAGAAGCGATAGCCAGGTGATGCTCTTAACTGAAGGACGTCAAGAAGCTAACTATGTAGACTAAGGTACGTGGCATCTGAAATCACGCCTCATTCCAATGTACAC
CAGAACCCTGTACGGACGGACGAAAACTTGAGCTCCCGACCCAACAGTAGAACTGACCTGCATTAATGACTCCCTTAGAGATCGATTTGACAAAAAACACAGCATTTAATTCGATAAAAGCCCAGGGCGGGTGGGAGCTGAATCATGAATGTTCATTTTTACCGCGCCTATTCATCCTATCTAAATA
GTTTTTGAATTTGCACCCCTATCACGTATGAGTCCTGCTCAGTAGAGGGCTGCGTAAGATGCTAGCGTTGCAAAATACTGGGATTGCATACGTCGTCCTCTCCCACCGGCTATGCCTAGCACCTTCAGCATCTATGAGTTTAGCCTTTATAACACCATCTGTTGAAGCCCAGCGAGCGGCATGCTCT
TTAAGCTCCGTGGTGATCTGCTGTTCGGGGGATTGTGTCCCGCTTGCTTTATGGTGCGATAGCGAGCGTGAGTAGCTCTGCTGTAGCCCAGCTCTTCCTTGTTGGGTACCGCAAGAGCTAGGACCATTCGGGGATCCGGCGGAGGTTCGTTAAGTCTATTCACCTGTTTCAGAGGAGATAGCTGTTG
TGCATTAACGTATAGGTTTTAATGGGTCCTGCAAAAGCCCCCTTCAGAGCAGCGGCTGACTAACCGCGCATCAGTTGTCTACTGACAAACGCGTACATCGATGGGTCAAACTCTATAGGCTTTGGCTTGCTTGACTACCCTTGAGAATTTTCAAGTAGGTGATGAGAGGCCATTTTCCAACGGCTGT
ACCTGGCAGAATCCTCCTCGGATGAAGCCCAGCTTCATATGATACCTAAAAAGGAGGCATCAGGCCACACTGGGGCGAAGACTCCGAATGGGGCGCGTCGTCTACCTGGTCCTGCAAACCCGTTTTCCTGGCCGATTCTGCAAAAGCCACAGAAGTTGGCAATCCGGATTACCGTGTTCCATTTCAA
ATCCCGCAAAGATCTCTGCACTCGCCCAGAATGGTTTTCAGGCATAAGCCAGCATATTTTCATGCGTTGGCGTTGCTTTTAAGCGTAGTCCAAATTAAGGAGATCCAGCAGTTGTCCAGTCGACCGGTAAGGTCAGGAAAGCATCGTTTATGCAGGTTATCTCTGAGTGAATCGCTTCTTAGGCGCT
GGTACGGTCTGCAAACAACCAGGTGTTGATGCTTCCATATTTCATCGGAACTCCTCGGCGTTAAGACCCCACACACTACAGACGAAGTGAGGGCCATTCGGTTTCCGTCCTAGGGGGTGCTAGACAGCTCTTAACTGCGATACGTGCTTATTGGATTAGACATCCGCTGTCGTGTAGTACACGCTAG
TCTAGTACTAATGGGAGCACCGTCTATAAGGGAGGGGGTGCCTGCGTGAGCCCCCAGTGAGGTTTGCGGGTGGACCAGTTGCGACCAGTTCACCTCTGCTTTTGGGAGGTTACGTCCTTGCTTTACAACTCCGCTTCTCTGAAAGCCCAGCTTGGCTCACGTAAACCGCGCTTACCGTTAGATATAT
GTAGATCAGAACGACGGTAATCTACAATGCCCGTCAACTAGCATTGTGTCCTGCACCTAAAATCCCACTATGCGCTGTAAATAGAACCATTCTGCAAAATTGCAGAGGGGCCAAACCTCATTCCCACAACTTAACCCCTTCCCTGATGGGACTTATAATCAGCGGAGTTGTAATTGCCCTCATACAT
GGTATAAGTTCAACTATACAACCTGACATTTTGTGTAAAGTGACGGATCGCTTTGGGCTACCGAGCGACGGCGATTTTGGGCTTCTCTGCAGGTGCCCAGATTGTTACACTGCAGGAAACCGAGGTGAGGCAGAGCGCGAGTAGTATTCGTGATCACGTATCCTTTGGCAACGGTATGTTTGCCTCC
ATGCGTAGATAAAGCTAGAACCTAGAGATGCTAATAGAAATCTCTAACGGGCGCACCAGAAGCCCTTTCATATAAGTTTAGAGTTGCGCGCACTAAAGTAGTGCAAAGGCCCGCCTCGGTTACCATAGGGCTCTGCCGTAGCCCAGGATCCATCGTCGATCCCAGCAACGGCGGTGACCCGACTTTT
GTTTGCTCTCTCTGTTGTATCCCAGACTACGGTGGGGCTCAATTTTACAAGTTTAGCAGGCTCCAAGTCGCCGGTTATGATCATCCGCAAAATTTTCGGAAAGACAGTCATCCACACGGGGGTATCAGGGGATGCCAGCCAAGTAAGGTTAACCTCTCCTCTGGACAAAAGCCCAGGGGGCGGGTTA'''

    input1 = '''15 20 10000
TAATCTGGGAAATAAGGACTTTACTCATATTGGACGAATATAAGCGGTGGCTAGCGGCGTTTGCTTGATCTATGATTTACGCCCCAGTTTGGTGACAGTTGGTCACGTGAGCAATGAACGATTCGTCATCAGGTTGCCGATCCCTGCACTACTTCTACGTTGTAGTCGTTCGGATACCTCCATGAGATAGGTAAGAACCGAGTGCCGAGGGCCTGCCGTATAGCGTACCCTAATGACGCCGGTCCCACTGGTCTATGGACCTGATAGGCGCGCGAAGCTTCCGGCAAAGGGGATGCTACGAACATTATTTAGGGTCCTAGCCCGGCAGCTTCTCATTCTGCGGTTTCAGGGCTGTTGCGTGCTCGCAGGAGCTGATGGACCAGTGTCTAAGATTCGCCTAATCTGGGAAATAA
GGACTTTACTCATATTGGACGAATATAAGCGGTGGCTAGCGGCGTTTGCTTGATCTATGATTTACGCCCCAGTTTGGTGACAGTTGGTCACGTGAGCTAACGAGGATCGCGAAATGAACGATTCGTCATCAGGTTGCCGATCCCTGCACTACTTCTACGTTGTAGTCGTTCGGATACCTCCATGAGATAGGTAAGAACCGAGTGCCGAGGGCCTGCCGTATAGCGTACCCTAATGACGCCGGTCCCACTGGTCTATGGACCTGATAGGCGCGCGAAGCTTCCGGCAAAGGGGATGCTACGAACATTATTTAGGGTCCTAGCCCGGCAGCTTCTCATTCTGCGGTTTCAGGGCTGTTGCGTGCTCGCAGGAGCTGATGGACCAGTGTCTAAGATTCGCCTAATCTGGGAAATAA
ATGCTGCATGGCCGAAAGGAATGACTCGAACCCACATGGCAAAAAATCGGAGCCCCGGAGACGGACTCTGGGCGGAGCATTCTCCTTTTCTCTCGGATCGCGACATTTCCCGTTCGATTTCTTGTTGATTTCCTTCCCGCATATGTATGCCGCCCAAGGTCGGGATAGAGTAAAGTCGTCACACCGATTAAAAATCGTTCAGACGACGCCTAACAAATCACTTGTTATTAGTGAATATGGTCCAACAGGAGTAGGATAGAACGATGGGTTAACCAAACCACGGGCCCGCGATTGGCCGCCATTTCGACAGTATCTGCTGACGAACACTCATGTCCAAAGTAGCTCCGATATTGGCGATTCCGAAGCGACGGCGGCGCAAGCGTCGGCGGAAGTTCAAGAGGGAATAAACAACT
AATAGAATAGTATCCCTCTAGATAGATGGCAATAGTTGTATCGTAAACTGCGATTTCCGGTGCACCGGATAAGATATGGTCGTGTGACTCTTTCATTCGGAGAGTGTTTTAGTGCAGATAAAACTACGACGTACACACATTCCATACTGCGGCTTTTGTTGGGCTTGACTACTCTGATGCGATGTGTGGACCATGCAGAGGATCTTTGTCCTATTGCTCCGATGCAACTGTTACAGGAATAAGCAGTCCAAGCTAAAACCGATCTAGCATGGCTGTTAAAAGAGATCGCGAACCCAGCCTACGTTCTCTCGAACAATCACTGTTAGGACACTTGCTTTGTGGACGACAATGTCGCCTCTCAGAATTACACTTCAATTCGGGCAAACGGAGTCAGTTGTGCGATGAACCAGGTT
AAAGGTTCGAGGGAGGTAGATGATCCTACAAGAGGAACCGGCTCCATAAAAGGATGGGTAGACTGCGTGAGTATCATTTATAAACTAGATCGCGAATCCACGATGCTGGTGGGCCGCCGAGCTAATCCGGTACATAAGATTTCTCCGGCTTTTTCCACGGGCTGAGGACAATGGTGTGACAGCTGTCAAGCCAAGGCTGGATCCCTAGTTTATGGCGCAACCGTGAAGGGTCAGTTTCACTTACGTCCCTTTTTGCATATCAACGATTCTTAATGTTCCCCCCGTCACAGAAGCCCGTACGAAGCCTAGCATCGACATTGTAGATGTGATGACGGGGCAACCTTCCAACGCGTCGAGATCTACAGAACTACAGCTACCAGTAATTGTCGCGAATCTAAAAAGTGCGTTGGCCG
CCGACTTGACGCTAGGTAATTGGTCCTCGTCGCGCGGCTTTGTCGGTCAACCTGCGATACGCCAAGAGGGGCGACGCCTGTGAACGATGTGGCTGACAATGGAGAGCTTGTCGAGGGCTGACGACTGAAGGGGCAATTACAGGCGAGGTGACACCTGCCGGCTATATCACGTTACGTACTAATTATTTTGCGTATGGACATACGGCATGACTCTGGTTTCATTAGTTACATCATACATTGCTATACGGCCTATGATGACCAGCTCATGAAGGATCAATGTGGTCTGCTTCGAATAGACCGAGAAATAGTAGCACCTCCTTTATGCAATCGGATCGCGTTTGTAATCTTTCTACGCTTAAGCCCATCCTACTCTCCAGGGTTTATGAATCGGGGGCAAGACTTTTTTTTCTATA
ATGGTTGACACTCTACTCACGCCCCGGCAATTTGCAGTTTACAGCAGTGTAATGCACGCAACCCCGGAGCCTGGATCGTTCAGGCGCCCTCGAGACTAATTTTGATTACTTGGACTTGGCGTACCAGCTCTCATGCATAATAACGGTCGGTGGCTGCGTCGACTGGATGCAGCGGGGAATCAAGGCGAAGAGGGCTTGACACGCAGTAGTATCTGTACAACATGTGCGACTACCATTAGTTCGGATCGGATCGCGAGGTACGGCTTAGACTACCTACATCGATTAGACGAACCCACCTCTCCTCGCTCGGATCGCAAAGGAAGAGGGCCCTGGAGCTCATTTCTGTCGTGAGCAAATAGAAAGGCCGGGTTCTAAAACGATAGCTAAGCTGCCCTCGAATAAAAAATGCCCTG
ACCCGTCTATGCTCTAAGGCCGAAGCCACGCAATTGTTGAGATCCCCGCACGGGGGTTGCATCCGTTAAAAATCGTAAATCGCGCAAACGACAACGCCATCCACAAGTCTGTTCTGGGGAAAAGTGTGGCAGCTCGTCTCGACAACTTTTCAATAGAGAATAAATCGACAGTGATCATCGTCCTACCCCCACGGCTCTTGTTCCTTAAATCCTCTCGCGACGATAGGGAGACTCATACACCTACTGGTCGCCCTACCGGCCTTACTAGCTACAATCCCATGAGCGATTGAACTTGGCATGTGGAACCCACTTATCCCCAGTTGCAGTTGAGTGTACACGCAGTTTCGTAGCGACTCGTAGAAATGCGCTCAAAGGCAGGACTGGACCTCTCTAGGATGCGTTAGTTCATTTTG
TAGAAATCGGATCGCATCGATTCCTGTATAATCTTATCGCCGGGTCATGTTTTACTTTCTCGGAGCGTTCCGGTATTTGTGGTATATGGCTTCTGTAGTAAGCAGACCAAGGCCAGCAAGCAACATCGCGACACCCTCGACTGCCGTCCGCCTCAGTATGATCTTTTCGAAAGGTTTAAGGGCCGATTTGAACATATGAAGATGGCACGCTTACTTGCTAGGTTTCATTTTCTGGATAGGATTCTGTATAACTCGGTACGCGCTAAGCATCCAGCTATAGCGCCCCCGGATTACTCGCGTGGCCTCTGCCACAAATGTTTTACTGGCCATCCATGGGACGGCGGTGAACCCCGTGACCTATACCCGTCCCTCCCGTCAACTCACAGCTGGGTGCGCGAGTTAACCCCGATTCG
AATTCAAGGCGGATCCGCTTTAGCCCAGCTTACGAGGATCAGAATATGGGCGACCGTGAATTATAACTTGGTCTCTTCGGAGCGTCTGATCGTAAAATGTAGCGCGCAAGTCGTGGGACTCACTCCTTTAAGCCTCAACAGTCCTTAATAACCCACCAGCTAGTTGGTAATTTTATGGTATCGGTGGGCAGGGCATTCGGTAGCAAGAGCAAGCGTCAATGGTGCCAAGTCTTAATTAACGGAGACGCATCGGCCTCGTCCCGCAAGATATAACACGAAGTATGGGCTTCTATCAGCCGTGCAGAAGTGATCCCTAGGACCCAGCCCGAGATACAATGACATCAGATGTAATAGTACGCTGCGGTGAGCGATCTGGGACATAAATTTCATCGCGATTCCCATAAATTTCCCAT
ACTGTCAGTCTGGAGGAAGGGGCCCTGATCAGCAATGATCTTCAGGGCGTCGAGCGGCCCTGGCTCAACGTGCGCATAGTTTGGTGCCCCCATTTTCTCCGCTACGATGACTGGAAGTCGAACTTACGCTGTCTCATCGCACATCAGGGCGGGAGTTGGAAGTAGGTAAACAACAAACTGCGAGGGAGATTGCGGGATATGAGAGGGAGTATGTTTGCGCAACCCGTCGGCCCTGGTACGTGCCCTGCCCCGTGGTCGACCTGGGCGGCTCGTGACGGGGCACCTCAGTCTTTGTTTGCTGGATATTCTAAGACAAGCAGTTCAATGCGCCCTCCCAGAACCAACTTAAATCGGATTTGGATCCTCATAAGAGAGAGGTGACACAGCCATGGGGAGCTTGCAAGAAGATGACG
GCGTAGGAAATAGCCGTTGCTGCTAGTCAAAAACTATAGACGGTTGACATCATCAAAGTCAAGAGGCAAGCGACGATGCTGCCCCCAAGCCAAGAGGATAAATGACATCGCGATCGCAGCGCGGAAGGACTCACGGACCATACTAATGCAGACGTTGACTACAGGAAGTCTTACACTTACCAATCTGAGGCACACTGGGAGTTGAGAGAGCTGTCTCAGGCTCGAAGTCGATGTGCCTTTCTTCCGACTGAAATCCGCGAGTCACATAAACGGCGGCCTCTTCGAATGGTACTCTGTAGGATGTCCGCTACGCCGCTTGTGATACCCTGTTCCGGCGTACTGCGGGTATTAACATCATCACTTTCGTATGTGGCCCTTTCCTTAGTTCGAGTAACTGTCGAAAAGATGATAAC
AACACACAGCGAATGCACGTCTTAGCAAGGTATAACCCAAATTCTAGTTTCATTAGTATCGATATTACACATACTATAGGACTCTCGCAAGGTTGGCTAAGTCCTAATCAATGTATTTATAGTGACGACGTGTCTTATACAGCGCACTACCGACATTACTCAACGGAGTGACTCACCCCCGCGGTTCAAGTGTCTGAGAGACGATTCTCCAGCTCGTAGCCGTGTCTGCACGTATGCCGGATCGCGATCCGCAGGACACCACAGCAAGCGAGTACTACGCGAGTGCCTCCACCTACCCTGCTTTGGGCCGGAGGCACAAAGTCGGATCTCTTCCCAGGCTCGGCCTGCGGCGGTTGGGTCCCCCGATGTATCATGCGAGCGAGAGAGTCAAGTCGGTCAGGGACGTGGCGTTC
GACAAAAGTGGTGCCGGCTTATCGATGTCTTGGCGTTTTGTGGGACCTGTTGGATGGAGGAAACCACCTCTACCAACCCATAGCTTCCGAAGTTGGAACTTGGCACCCTAACCGTAAAGGCACCCTTCCTCTGATTGAACGAAGAAGTGCATCAACTCCGATGTTACGGCCACAAAAGCGATACGAACCCTGAGTCAGGCTGACGATTCGCATCCATAACCTTCATCGACCGGCAGTAGCAATCAGCTATGGACACACTAGTCCATTTGGACGGGCCTATATTCTAGTCAGACAAGAGAGGTATGTCGACGGCGATCGTAATAGGGATCGCGACGTACCCTCCGCACCACACGGAACTCTACGGATAGTTTCGAGAAGAGTCCGCCTCAGAATCGGAATTCCGTTGAAAACGT
AGGCTAGGACACGCACCGGGGTAAACTCGGTTAGTCGGTGATAGCCCTCGTTCGGACGACCTATTTCGGTGACAGAGGACACTTCAGTCCATGTGCAGTGGTTGGACCTTAATAAGGCACAGATGCTATACGACGTCAGTCTAAATCGGATCGTTTATTACAGCTACAGCCCCCGGCGCCCGTCTGTCTCACTCGGGACCACCTCAAGGTCGAACCAATAGTTGTGGACATTGAAGTCTGCTGAACACCACATACGCTATATACTGCCACTGGCGCCAAATGTCGACACACCGTACGGGCGAGGAATGTTGACTCTTACTAAGAGGGAGATGTAGAAGCTGTATAACCACACCGGTTGAATTTTCGTCCCCATTGTGACACCGAACCTCACGAGGAAGATACAGTTTTCTTTG
GAAGACAATTGGAAGCGTCGCCCGACTACCCCTCGTCTGAGACTATCGCATCGTGCATGGTCATGGCATCATTAGGACGTACAAGGAAGGTGCCTCCGTAGGAGGTGGACCCTTCTAAAGCGTGCGCAACATACCGCTCGGCTTATCTGAATTCTTTAGACAATATGGCTGTTATAGGTACTTATCTTCACCTGCATTTCGTACGACCGGGCTGGTTTGACTTAAGACCTGGTACAGGTTAGTCGTTGGAGACGGTCAATCGCTTAACAACTAAATCGGTGGGCGACGCCCCCTTGAATGCGGAGATTGAGTAGCCCGCTCAAGCCCTATATCCTAGTTTTTGCGCATGTAGCTTATAAGTCTTTTACCTCAGGCGTGGGGGACTTATCTGGGACTTTTATATATGGACAACC
TAGACGATGATTTATACAAACGGACGAGAGGGGGCTGGGAGCGGTGCGAGGCTGCGCTCCCAGTCTGAAGATGGGGAATGTTATCTTCCATTCTGGTGTGGTCGACGCCGTGCTCGTCGTGAACCAAGCCCTATCCCCGCAATTTAGAGCGTATCGCCCTATCAGGCTGTTTGGGCTCTTGGATCCCTTGGAATATAATTATCGGGCCGGCAGGTTAGGCCATATACCTAGTCCGTAATGTGTTGGAGGGCGTCGCCGAATTGGAGGTCTAATCATTTGAGATACGAGACCGGTTGGTTTAGATTTAAGACAAGTCTTGGATGCCTCGGGGATGTATAGGCGTTCCTGTATAAATCGCTGCGCGACACTTTCCTCAGTGTCAGTGTCCAGATAGTAGGGTGCCTCTACCCGCA
TTTCCTAAATCGCTCTGACTACGGCATCTCGAGTCTACCATGCTGTGTGGATTTTAAGAAGTATCCTAAGAATGACTATCTAGACGAACCTACCGCAAAAAGGGCCTGGTAATTCCACCTGATTAATCGAGGTCGAATCGAGTTACGACTGGGCGTTGTTAAATCGGAGGCCGAATAACTCGCTACATAAGTCAAAGGTGCTCTAAAGCTATACAAGTCACTGCGCGGGGGGATCACACTACTAACATGTAGTCCCAAAGTTACAAACCGAACCCGCCACTTTGCTTCTGCTACAAGGCCACATTGACTAATCATGACACTCAAGTGGTTCAACGCACCCGACTGCAATCATCTTGTCGCGATATTTCGTCCCGTTGTAGTTATCCAGCTATGTAGCCAAATTCAGGCCGTTG
TATGTTACTGAGGCAATGATCGCCTAGTTGCGGAGTATCCTTTAGAGTGGGGACTCGGAGGGAATGATTGCTGTTTGGACTTACAGCAGGTCCTCAACCACCTGAATCCCAGGGTCTCCGAGAACTCAGCCTTCGGGGACGAAACCGAAAATTACGCTAATTCTGTACTTTGCCATCGGGTTGAGGACACCTTTCCTACATCTGGCGTGCGCGCTTGAACTGGGAGCATTGTTTATCCCTCGAGGCTAAATCGGATCAGTAGCCCGTGATCATTGGGATACGCGGTATGCATCGCACTCAACGGCACTGATCGAATAGTTATGTTCTTCGCTGAGCAAGTATGCACGAGCATTGACTGAGCCGAGACGATTTGAGCTTATGTAACCCCTCTATCAGCTCGCGACATGCGTCTT
GTATCAGCGAAAAGGAAAGGTACTGAGTCCTTTCGAGGTGTCAGGACGTCGCCTCCCCCGTCACATGCCTGATTAGGTCTTGCGGCTCTAAATCACTTCGCGATAGCGGCAACAACTGTTCCCCGGTCGGGCAAGTAACGCCCGCACTGGCCAGATCTTACAATCATATTTTTTACCAGCCTAATCGCGATGTCATTCGCATATTACGTATTATGCACACCACAGCTATGTGTTTCATGCCCAGAGAGCGATCTTCTTAGGCCGGCAGATTGCATAGCTATACGAAACTGGTTTAGCGTCCTTGGCATGCACGCCATAGACAATCAACACCTCTGGACAAATCATCACAGGCCCTTCAACAAACCAATGGGCGAAGGGTTCGTGCGTATGCGCCTTGACGGCAATGAGACGAG'''

    input1 = '''10 10 1000
    GCGCCCCGCCCGGACAGCCATGCGCTAACCCTGGCTTCGATGGCGCCGGCTCAGTTAGGGCCGGAAGTCCCCAATGTGGCAGACCTTTCGCCCCTGGCGGACGAATGACCCCAGTGGCCGGGACTTCAGGCCCTATCGGAGGGCTCCGGCGCGGTGGTCGGATTTGTCTGTGGAGGTTACACCCCAATCGCAAGGATGCATTATGACCAGCGAGCTGAGCCTGGTCGCCACTGGAAAGGGGAGCAACATC
CCGATCGGCATCACTATCGGTCCTGCGGCCGCCCATAGCGCTATATCCGGCTGGTGAAATCAATTGACAACCTTCGACTTTGAGGTGGCCTACGGCGAGGACAAGCCAGGCAAGCCAGCTGCCTCAACGCGCGCCAGTACGGGTCCATCGACCCGCGGCCCACGGGTCAAACGACCCTAGTGTTCGCTACGACGTGGTCGTACCTTCGGCAGCAGATCAGCAATAGCACCCCGACTCGAGGAGGATCCCG
ACCGTCGATGTGCCCGGTCGCGCCGCGTCCACCTCGGTCATCGACCCCACGATGAGGACGCCATCGGCCGCGACCAAGCCCCGTGAAACTCTGACGGCGTGCTGGCCGGGCTGCGGCACCTGATCACCTTAGGGCACTTGGGCCACCACAACGGGCCGCCGGTCTCGACAGTGGCCACCACCACACAGGTGACTTCCGGCGGGACGTAAGTCCCTAACGCGTCGTTCCGCACGCGGTTAGCTTTGCTGCC
GGGTCAGGTATATTTATCGCACACTTGGGCACATGACACACAAGCGCCAGAATCCCGGACCGAACCGAGCACCGTGGGTGGGCAGCCTCCATACAGCGATGACCTGATCGATCATCGGCCAGGGCGCCGGGCTTCCAACCGTGGCCGTCTCAGTACCCAGCCTCATTGACCCTTCGACGCATCCACTGCGCGTAAGTCGGCTCAACCCTTTCAAACCGCTGGATTACCGACCGCAGAAAGGGGGCAGGAC
GTAGGTCAAACCGGGTGTACATACCCGCTCAATCGCCCAGCACTTCGGGCAGATCACCGGGTTTCCCCGGTATCACCAATACTGCCACCAAACACAGCAGGCGGGAAGGGGCGAAAGTCCCTTATCCGACAATAAAACTTCGCTTGTTCGACGCCCGGTTCACCCGATATGCACGGCGCCCAGCCATTCGTGACCGACGTCCCCAGCCCCAAGGCCGAACGACCCTAGGAGCCACGAGCAATTCACAGCG
CCGCTGGCGACGCTGTTCGCCGGCAGCGTGCGTGACGACTTCGAGCTGCCCGACTACACCTGGTGACCACCGCCGACGGGCACCTCTCCGCCAGGTAGGCACGGTTTGTCGCCGGCAATGTGACCTTTGGGCGCGGTCTTGAGGACCTTCGGCCCCACCCACGAGGCCGCCGCCGGCCGATCGTATGACGTGCAATGTACGCCATAGGGTGCGTGTTACGGCGATTACCTGAAGGCGGCGGTGGTCCGGA
GGCCAACTGCACCGCGCTCTTGATGACATCGGTGGTCACCATGGTGTCCGGCATGATCAACCTCCGCTGTTCGATATCACCCCGATCTTTCTGAACGGCGGTTGGCAGACAACAGGGTCAATGGTCCCCAAGTGGATCACCGACGGGCGCGGACAAATGGCCCGCGCTTCGGGGACTTCTGTCCCTAGCCCTGGCCACGATGGGCTGGTCGGATCAAAGGCATCCGTTTCCATCGATTAGGAGGCATCAA
GTACATGTCCAGAGCGAGCCTCAGCTTCTGCGCAGCGACGGAAACTGCCACACTCAAAGCCTACTGGGCGCACGTGTGGCAACGAGTCGATCCACACGAAATGCCGCCGTTGGGCCGCGGACTAGCCGAATTTTCCGGGTGGTGACACAGCCCACATTTGGCATGGGACTTTCGGCCCTGTCCGCGTCCGTGTCGGCCAGACAAGCTTTGGGCATTGGCCACAATCGGGCCACAATCGAAAGCCGAGCAG
GGCAGCTGTCGGCAACTGTAAGCCATTTCTGGGACTTTGCTGTGAAAAGCTGGGCGATGGTTGTGGACCTGGACGAGCCACCCGTGCGATAGGTGAGATTCATTCTCGCCCTGACGGGTTGCGTCTGTCATCGGTCGATAAGGACTAACGGCCCTCAGGTGGGGACCAACGCCCCTGGGAGATAGCGGTCCCCGCCAGTAACGTACCGCTGAACCGACGGGATGTATCCGCCCCAGCGAAGGAGACGGCG
TCAGCACCATGACCGCCTGGCCACCAATCGCCCGTAACAAGCGGGACGTCCGCGACGACGCGTGCGCTAGCGCCGTGGCGGTGACAACGACCAGATATGGTCCGAGCACGCGGGCGAACCTCGTGTTCTGGCCTCGGCCAGTTGTGTAGAGCTCATCGCTGTCATCGAGCGATATCCGACCACTGATCCAAGTCGGGGGCTCTGGGGACCGAAGTCCCCGGGCTCGGAGCTATCGGACCTCACGATCACC'''

    k, t, N = map(int, input.split('\n')[0].split())
    dna = [Seq(line.strip(), IUPAC.unambiguous_dna) for line in input.upper().split('\n')[1:]]

    #best_motifs = randomized_motif_search(dna, k, t)
    best_motifs = gibbs_sampler(dna, k, t, N, 20)

    print
    print 'Mine:',
    print_motifs(best_motifs)

    print
    print 'Theirs:',
    print_motifs([l.strip() for l in '''TCTCGGGG
    CCAAGGTG
    TACAGGCG
    TTCAGGTG
    TCCACGTG'''.split()])

def main1():
    input_dna = '''ttACCTtaac
gATGTctgtc
ccgGCGTtag
cactaACGAg
cgtcagAGGT'''
    dna = [Seq(line.strip(), IUPAC.unambiguous_dna) for line in input_dna.upper().split('\n')]
    input_motifs = '''ttac
gtct
ggcg
taac
gtca'''
    motifs = [Seq(line.strip(), IUPAC.unambiguous_dna) for line in input_motifs.upper().split('\n')]
    print_motifs(motifs)

    profile = make_profile(motifs, 4)
    print
    print profile

    print
    new_motifs = []
    for seq in dna:
        new_motifs.append(profile_most_prob(profile, seq, 4))
    print_motifs(new_motifs)

    profile = make_profile(new_motifs, 4)
    print
    print profile

    print
    new_motifs = []
    for seq in dna:
        new_motifs.append(profile_most_prob(profile, seq, 4))
    print_motifs(new_motifs)

if __name__ == '__main__':
    main()