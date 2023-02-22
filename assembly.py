import subprocess
import os

class Assembly:

    def __init__(self, result_path, sequencing_tech, conf, input_1, input_2=None):
        self.result_path = result_path + '/assembly'
        self.sequencing_tech = sequencing_tech
        self.conf = conf
        self.input_1 = input_1
        self.input_2 = input_2
    
    def run(self):
        os.mkdir(os.path.abspath('.') + '/' + self.result_path)
        if self.sequencing_tech == 'ngs':
            if self.input_2 == None:
                self.__megahit_single_end()
                return self.result_path+'/megahit_out/final.contigs.fa'
            else:
                self.__megahit_paired_end()
                return self.result_path+'/megahit_out/final.contigs.fa'
        else:
            self.__canu()
            return self.result_path+'/canu_out/canu_assembly_result.contigs.fasta'


    def __megahit_single_end(self):
        print('start megahit single end')
        megahit_conf = self.conf['identification']['assembly']['megahit']
        command_line = 'megahit '
        if megahit_conf['--min-count'] != None:
            command_line += '--min-count '+str(megahit_conf['--min-count'])+' '
        if megahit_conf['--k-list'] != None:
            command_line += '--k-list '+str(megahit_conf['--k-list'])+' '
        if megahit_conf['--no-mercy'] != None:
            command_line += '--no-mercy '
        if megahit_conf['--bubble-level'] != None:
            command_line += '--bubble-level '+str(megahit_conf['--bubble-level'])+' '
        if megahit_conf['--merge-level'] != None:
            command_line += '--merge-level '+str(megahit_conf['--merge-level'])+' '
        if megahit_conf['--prune-level'] != None:
            command_line += '--prune-level '+str(megahit_conf['--prune-level'])+' '
        if megahit_conf['--prune-depth'] != None:
            command_line += '--prune-depth '+str(megahit_conf['--prune-depth'])+' '
        if megahit_conf['--low-local-ratio'] != None:
            command_line += '--low-local-ratio '+str(megahit_conf['--low-local-ratio'])+' '
        if megahit_conf['--max-tip-len'] != None:
            command_line += '--max-tip-len '+str(megahit_conf['--max-tip-len'])+' '
        if megahit_conf['--no-local'] != None:
            command_line += '--no-local '
        if megahit_conf['--kmin-1pass'] != None:
            command_line += '--kmin-1pass '
        if megahit_conf['-m'] != None:
            command_line += '-m '+str(megahit_conf['-m'])+' '
        if megahit_conf['--mem-flag'] != None:
            command_line += '--mem-flag '+str(megahit_conf['--mem-flag'])+' '
        if megahit_conf['-t'] != None:
            command_line += '-t '+str(megahit_conf['-t'])+' '
        if megahit_conf['--no-hw-accel'] != None:
            command_line += '--no-hw-accel '
        if megahit_conf['--min-contig-len'] != None:
            command_line += '--min-contig-len '+str(megahit_conf['--min-contig-len'])+' '
        command_line += '-r '+self.input_1+' -o '+self.result_path+'/megahit_out'
        subprocess.run(command_line, shell=True, check=True)
        print('end megahit single end')

    def __megahit_paired_end(self):
        print('start megahit paired end')
        megahit_conf = self.conf['identification']['assembly']['megahit']
        command_line = 'megahit '
        if megahit_conf['--min-count'] != None:
            command_line += '--min-count '+str(megahit_conf['--min-count'])+' '
        if megahit_conf['--k-list'] != None:
            command_line += '--k-list '+str(megahit_conf['--k-list'])+' '
        if megahit_conf['--no-mercy'] != None:
            command_line += '--no-mercy '
        if megahit_conf['--bubble-level'] != None:
            command_line += '--bubble-level '+str(megahit_conf['--bubble-level'])+' '
        if megahit_conf['--merge-level'] != None:
            command_line += '--merge-level '+str(megahit_conf['--merge-level'])+' '
        if megahit_conf['--prune-level'] != None:
            command_line += '--prune-level '+str(megahit_conf['--prune-level'])+' '
        if megahit_conf['--prune-depth'] != None:
            command_line += '--prune-depth '+str(megahit_conf['--prune-depth'])+' '
        if megahit_conf['--low-local-ratio'] != None:
            command_line += '--low-local-ratio '+str(megahit_conf['--low-local-ratio'])+' '
        if megahit_conf['--max-tip-len'] != None:
            command_line += '--max-tip-len '+str(megahit_conf['--max-tip-len'])+' '
        if megahit_conf['--no-local'] != None:
            command_line += '--no-local '
        if megahit_conf['--kmin-1pass'] != None:
            command_line += '--kmin-1pass '
        if megahit_conf['-m'] != None:
            command_line += '-m '+str(megahit_conf['-m'])+' '
        if megahit_conf['--mem-flag'] != None:
            command_line += '--mem-flag '+str(megahit_conf['--mem-flag'])+' '
        if megahit_conf['-t'] != None:
            command_line += '-t '+str(megahit_conf['-t'])+' '
        if megahit_conf['--no-hw-accel'] != None:
            command_line += '--no-hw-accel '
        if megahit_conf['--min-contig-len'] != None:
            command_line += '--min-contig-len '+str(megahit_conf['--min-contig-len'])+' '
        command_line += '-1 '+self.input_1+' -2 '+self.input_2+' -o '+self.result_path+'/megahit_out'
        subprocess.run(command_line, shell=True, check=True)
        print('end megahit paired end')

    def __canu(self):
        print('start canu single end')
        canu_conf = self.conf['assembly']['canu']
        command_line = 'canu -p canu_assembly_result -d '+self.result_path+'/canu_output/ '
        if canu_conf['genomeSize='] != None:
            command_line += 'genomeSize='+canu_conf['-p']+' '
        else:
            command_line += 'genomeSize=4.8m '
        if canu_conf['-pacbio-raw'] != None:
            command_line += '-pacbio-raw '
        elif canu_conf['-pacbio-corrected'] != None:
            command_line += '-pacbio-corrected '
        elif canu_conf['-nanopore-raw'] != None:
            command_line += '-nanopore-raw '
        elif canu_conf['-nanopore-corrected'] != None:
            command_line += '-nanopore-corrected '
        else:
            command_line += '-pacbio-raw '
        command_line += self.input_1
        subprocess.run(command_line, shell=True, check=True)
        print('end canu single end')
