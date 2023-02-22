from datasketch import MinHash
import glob
import pickle

class GenomeSimilarityCalculator:

    def __init__(self, contigs_path, data_path, similar_genome_number=1):
        self.__contigs_path = contigs_path
        self.__data_path = data_path
        self.__similar_genome_number = similar_genome_number
        self.__k_mer_length = 10
        super().__init__()

    def _get_sequence_from_fasta(self, fasta_file_name):
        temp_file = open(fasta_file_name, 'r')
        lines = temp_file.readlines()
        temp_file.close()

        sequence = ''
        accession = ''
        for line in lines:
            if line.startswith(">"):
                print(line.strip())
                if sequence != '':
                    print('there are many sequences in a fna file.')
                    break
                accession = line[1:].strip()
                continue
            else:
                sequence += line.strip()

        return accession, sequence

    # 用一条输入DNA序列构建MinHash
    def _construct_minhash(self, sequence):
        temp_minhash = MinHash(num_perm=2048)

        for i in range( len(sequence)-self.__k_mer_length+1 ):
            temp_minhash.update(sequence[i:i+self.__k_mer_length].encode('utf8'))
        
        return temp_minhash

    def _construct_contigs_minhash(self):
        
        contigs_minhash = MinHash(num_perm=2048)

        contigs_file = open(self.__contigs_path, 'r')
        contigs_lines = contigs_file.readlines()
        contigs_file.close()
        for contig in contigs_lines:
            if contig.startswith('>'):
                continue
            contigs_minhash.merge(self._construct_minhash(contig.strip()))

        return contigs_minhash
    
    def _insert_genome(self, similar_genome_list, closest_genome, jaccard_similar):

        for i in range(self.__similar_genome_number):

            if jaccard_similar > similar_genome_list[i][1]:
                # similar_genome_list.insert(i, [closest_genome.split('|')[3][:-2], jaccard_similar])
                similar_genome_list.insert(i, [closest_genome, jaccard_similar])
                break

        return similar_genome_list[:self.__similar_genome_number]

    def search_similar_genome_from_dataset(self):

        similar_genome_list = [['', 0] for i in range(self.__similar_genome_number)]

        max_jaccard = 0
        closest_genome = ''

        contigs_minhash = self._construct_contigs_minhash()

        # for refseq_file in glob.iglob(self.__data_path+'/*.fna'):
        for refseq_file in glob.iglob(self.__data_path+'/*.pkl'):
            # accession, refseq = self._get_sequence_from_fasta(refseq_file)
            # refseq_minhash = self._construct_minhash(refseq)

            accession = refseq_file.split('/')[-1][:-4]
            # print(refseq_file)
            # print(accession)

            refseq_minhash = MinHash(num_perm=2048)
            with open(refseq_file,'rb') as temp_file:
                refseq_minhash  = pickle.loads(temp_file.read())

            # 然后用contigs输入minhash，再比较

            # 只需要一个结果
            # if contigs_minhash.jaccard(refseq_minhash) > max_jaccard:
            #     closest_genome = accession

            similar_genome_list = self._insert_genome(similar_genome_list, accession, contigs_minhash.jaccard(refseq_minhash))
        
        # return closest_genome, max_jaccard
        return similar_genome_list

# data1 = ['minhash', 'is', 'a', 'probabilistic', 'data', 'structure', 'for', 'estimating', 'the', 'similarity', 'between', 'datasets']
# data2 = ['minhash', 'is', 'a', 'probability', 'data', 'structure', 'for', 'estimating', 'the', 'similarity', 'between', 'documents']
# data3 = ['minhash', 'is', 'a', 'probabilistic', 'data', 'structure', 'for']
# data4 = ['estimating', 'the', 'similarity', 'between', 'datasets']

# m1, m2 = MinHash(), MinHash()
# for d in data1:
#     m1.update(d.encode('utf8'))
# for d in data2:
#     m2.update(d.encode('utf8'))
# print("Estimated Jaccard for data1 and data2 is", m1.jaccard(m2))

# m3, m4 = MinHash(), MinHash()
# for d in data3:
#     m3.update(d.encode('utf8'))
# for d in data4:
#     m4.update(d.encode('utf8'))

# m3.merge(m4)
# print("Estimated Jaccard for data3 and data2 is", m3.jaccard(m2))


# s1 = set(data1)
# s2 = set(data2)
# actual_jaccard = float(len(s1.intersection(s2)))/float(len(s1.union(s2)))
# print("Actual Jaccard for data1 and data2 is", actual_jaccard)
