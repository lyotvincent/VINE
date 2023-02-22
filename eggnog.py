import subprocess
import os

class Eggnog:
    
    def __init__(self, result_path, contigs):
        self.__result_path = result_path + '/eggnog_result'
        self.__contigs = contigs

    def run(self):

        print('start eggnog mapper')
        os.mkdir(self.__result_path)
        # subprocess.run('python2 ~/software/eggnog-mapper-1.0.3/emapper.py -i %s --output %s -m diamond' % (self.__contigs, self.__result_path), shell=True, check=True)
        subprocess.run('python2 ~/software/eggnog-mapper-1.0.3/emapper.py -i %s --output %s --output_dir %s -m diamond' % (self.__contigs, 'eggnog_result', self.__result_path), shell=True, check=True)


        print('end eggnog mapper')
