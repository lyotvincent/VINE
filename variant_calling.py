import subprocess
import download_nucleotide
import os

class VariantCalling:

    def __init__(self, result_path, reference_accession, input_1, input_2=None):
        self.result_path = result_path + '/variant_calling'
        # self.conf = conf
        self.reference_accession = reference_accession
        self.input_1 = input_1
        self.input_2 = input_2

    def run(self):
        print('start variant calling...')
        os.mkdir(self.result_path)
        # subprocess.run('cp %s %s' % ('~/virus/train_data/'+self.reference_accession.split('.')[0]+'.fna', self.result_path+'/'+self.reference_accession+'.fasta'), shell=True, check=True)
        download_nucleotide.download_by_accession_version(self.result_path, self.reference_accession)
        subprocess.run('bowtie2-build %s %s' % (self.result_path+'/'+self.reference_accession+'.fasta', self.result_path+'/'+self.reference_accession+'_index'), shell=True, check=True)
        if self.input_2 == None:
            subprocess.run('bowtie2 -x %s -f -U %s -S %s' % (self.result_path+'/'+self.reference_accession+'_index', self.input_1, self.result_path+'/bowtie2_result.sam'), shell=True, check=True)
        else:
            subprocess.run('bowtie2 -x %s -1 %s -2 %s -S %s' % (self.result_path+'/'+self.reference_accession+'_index', self.input_1, self.input_2, self.result_path+'/bowtie2_result.sam'), shell=True, check=True)
        subprocess.run('samtools view -bS %s > %s' % (self.result_path+'/bowtie2_result.sam', self.result_path+'/bowtie2_result.bam'), shell=True, check=True)
        subprocess.run('freebayes -f %s %s > %s' % (self.result_path+'/'+self.reference_accession+'.fasta', self.result_path+'/bowtie2_result.bam', self.result_path+'/freebayes_result.vcf'), shell=True, check=True)

        print('end variant calling===')
# test command
# art_illumina -ss MSv3 -sam -i ../NC_045512.fasta -p -l 250 -f 50 -m 300 -s 10 -ir 0.005 -ir2 0.006 -dr 0.0055 -dr2 0.0065 -o simulated_NC_045512_
# bowtie2-build ../NC_045512.fasta NC_045512_index
# bowtie2 -x NC_045512_index -1 ../simulated_paired_end_NC_045512/simulated_NC_045512_1.fastq -2 ../simulated_paired_end_NC_045512/simulated_NC_045512_2.fastq -S test_NC_045512.sam
# samtools view -bS test_NC_045512.sam > test_NC_045512.bam
# freebayes 需要把NC_045512.fasta的序列都放在一行，要不然会出错
# freebayes -f ../NC_045512.fasta ./test_NC_045512.bam > test_freebayes.vcf
# samtools mpileup -q 1 -d 30000 -f ../NC_045512.fasta ./test_NC_045512.bam 1>merged_marked.mpileup 2>mpileup.log
# java -jar VarScan.jar mpileup2snp merged_marked.mpileup --output-vcf 1 > varscan.snp.vcf
