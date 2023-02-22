import subprocess
import os
from ete3 import Tree, TreeStyle
import download_nucleotide

class TreeBuilder:

    def __init__(self, result_path, ref_genome_list):
        self.__result_path = result_path + '/phylogenetic_tree'
        # self.conf = conf
        self.__ref_genome_list = ref_genome_list

    def run(self):
        print('start TreeBuilder')
        # TODO 需要先选择几个序列 cat > 加入temp_megacc_sequences.fasta
        # '~/virus/virus_data/'+self.reference_accession+'.fna'

        os.mkdir(self.__result_path)
        cat_command = 'cat '
        for ref_genome in self.__ref_genome_list:
            download_nucleotide.download_by_accession_version(self.__result_path, ref_genome)
            cat_command += self.__result_path+'/'+ref_genome+'.fasta '
        cat_command += '> '+self.__result_path+'/temp_megacc_sequences.fasta'
        subprocess.run(cat_command, shell=True, check=True)
        subprocess.run('megacc -a %s -d %s -o %s -f Fasta' % (os.path.dirname(os.path.realpath(__file__))+'/configurations/muscle_align_nucleotide.mao', self.__result_path+'/temp_megacc_sequences.fasta', self.__result_path+'/temp_megacc_result'), shell=True, check=True)
        subprocess.run('megacc -a %s -d %s -o %s' % (os.path.dirname(os.path.realpath(__file__))+'/configurations/infer_ML_nucleotide.mao', self.__result_path+'/temp_megacc_result.fasta', self.__result_path+'/temp_megacc_result'), shell=True, check=True)
        
        subprocess.run('figtree -graphic SVG %s %s' % (self.__result_path+'/temp_megacc_result.nwk', self.__result_path+"/tree.svg"), shell=True, check=True)
        
        # t = Tree(self.__result_path+'/temp_megacc_result.nwk')
        # t.render(self.__result_path+"/tree_ete.svg")

        print('end TreeBuilder')
# test command
# megacc -a muscle_align_nucleotide.mao -d testsequences.fasta -o ./testmegaccresult -f Fasta
# megacc -a infer_ML_nucleotide.mao -d testmegaccresult.fasta -o ./testmegaccresult
# figtree -graphic PNG testmegaccresult.nwk test.png
