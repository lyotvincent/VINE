from datasketch import MinHash
import glob
import pickle
import sys
import time

class PicklingData:

    def __init__(self, data_path):
        self.__data_path = data_path
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

    def pickle_data(self):
        for refseq_file in glob.iglob(self.__data_path+'/*.fna'):
            print(refseq_file)
            accession, refseq = self._get_sequence_from_fasta(refseq_file)
            refseq_minhash = self._construct_minhash(refseq)

            print(refseq_file[:-4]+".pkl")
            output_file = open(refseq_file[:-4]+".pkl", 'wb')
            dumped_str = pickle.dumps(refseq_minhash)
            # print(dumped_str)
            output_file.write(dumped_str)
            output_file.close()

if __name__ == "__main__":
    a = time.time()
    argvs = sys.argv
    print(argvs)
    obj = PicklingData(argvs[1])
    obj.pickle_data()
    print(time.time() - a)
