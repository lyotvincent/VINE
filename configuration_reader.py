import xlrd
import yaml
import sys
import os

class ConfigurationReader:

    def __init__(self, conf_file_path):
        self.conf_file_path = conf_file_path
        with open(os.path.dirname(os.path.realpath(__file__))+'/conf_origin.yaml', encoding='UTF-8') as yaml_file:
            self.conf = yaml.safe_load(yaml_file)
        super().__init__()
    
    def run(self):
        self.read_preprocessing_configuration()
        self.read_identification_configuration()

        return self.conf
    
    def read_preprocessing_configuration(self):
        preprocessing_sheet = xlrd.open_workbook(self.conf_file_path).sheet_by_name('preprocessing')

        if preprocessing_sheet.cell_value(1, 1) != True:
            self.conf["preprocessing"]["enable"] = False
        
        if preprocessing_sheet.cell_value(3, 1) != "":
            self.conf["preprocessing"]["fastp"]["--phred64"] = preprocessing_sheet.cell_value(3, 1)
        if preprocessing_sheet.cell_value(4, 1) != "":
            self.conf["preprocessing"]["fastp"]["-V"] = preprocessing_sheet.cell_value(4, 1)
        if preprocessing_sheet.cell_value(5, 1) != "":
            self.conf["preprocessing"]["fastp"]["-A"] = preprocessing_sheet.cell_value(5, 1)
        if preprocessing_sheet.cell_value(6, 1) != "":
            self.conf["preprocessing"]["fastp"]["--adapter_sequence"] = preprocessing_sheet.cell_value(6, 1)
        if preprocessing_sheet.cell_value(7, 1) != "":
            self.conf["preprocessing"]["fastp"]["--adapter_sequence_r2"] = preprocessing_sheet.cell_value(7, 1)
        if preprocessing_sheet.cell_value(8, 1) != "":
            self.conf["preprocessing"]["fastp"]["--adapter_fasta"] = preprocessing_sheet.cell_value(8, 1)
        if preprocessing_sheet.cell_value(9, 1) != "":
            self.conf["preprocessing"]["fastp"]["--detect_adapter_for_pe"] = preprocessing_sheet.cell_value(9, 1)
        if preprocessing_sheet.cell_value(10, 1) != "":
            self.conf["preprocessing"]["fastp"]["-f"] = preprocessing_sheet.cell_value(10, 1)
        if preprocessing_sheet.cell_value(11, 1) != "":
            self.conf["preprocessing"]["fastp"]["-t"] = preprocessing_sheet.cell_value(11, 1)
        if preprocessing_sheet.cell_value(12, 1) != "":
            self.conf["preprocessing"]["fastp"]["-b"] = preprocessing_sheet.cell_value(12, 1)
        if preprocessing_sheet.cell_value(13, 1) != "":
            self.conf["preprocessing"]["fastp"]["-F"] = preprocessing_sheet.cell_value(13, 1)
        if preprocessing_sheet.cell_value(14, 1) != "":
            self.conf["preprocessing"]["fastp"]["-T"] = preprocessing_sheet.cell_value(14, 1)
        if preprocessing_sheet.cell_value(15, 1) != "":
            self.conf["preprocessing"]["fastp"]["-B"] = preprocessing_sheet.cell_value(15, 1)
        if preprocessing_sheet.cell_value(16, 1) != "":
            self.conf["preprocessing"]["fastp"]["--trim_poly_g"] = preprocessing_sheet.cell_value(16, 1)
        if preprocessing_sheet.cell_value(17, 1) != "":
            self.conf["preprocessing"]["fastp"]["--poly_g_min_len"] = preprocessing_sheet.cell_value(17, 1)
        if preprocessing_sheet.cell_value(18, 1) != "":
            self.conf["preprocessing"]["fastp"]["-G"] = preprocessing_sheet.cell_value(18, 1)
        if preprocessing_sheet.cell_value(19, 1) != "":
            self.conf["preprocessing"]["fastp"]["--trim_poly_x"] = preprocessing_sheet.cell_value(19, 1)
        if preprocessing_sheet.cell_value(20, 1) != "":
            self.conf["preprocessing"]["fastp"]["--poly_x_min_len"] = preprocessing_sheet.cell_value(20, 1)
        if preprocessing_sheet.cell_value(21, 1) != "":
            self.conf["preprocessing"]["fastp"]["--cut_by_quality5"] = preprocessing_sheet.cell_value(21, 1)
        if preprocessing_sheet.cell_value(22, 1) != "":
            self.conf["preprocessing"]["fastp"]["--cut_by_quality3"] = preprocessing_sheet.cell_value(22, 1)
        if preprocessing_sheet.cell_value(23, 1) != "":
            self.conf["preprocessing"]["fastp"]["-r"] = preprocessing_sheet.cell_value(23, 1)
        if preprocessing_sheet.cell_value(24, 1) != "":
            self.conf["preprocessing"]["fastp"]["-W"] = preprocessing_sheet.cell_value(24, 1)
        if preprocessing_sheet.cell_value(25, 1) != "":
            self.conf["preprocessing"]["fastp"]["--cut_mean_quality"] = preprocessing_sheet.cell_value(25, 1)
        if preprocessing_sheet.cell_value(26, 1) != "":
            self.conf["preprocessing"]["fastp"]["--cut_front_window_size"] = preprocessing_sheet.cell_value(26, 1)
        if preprocessing_sheet.cell_value(27, 1) != "":
            self.conf["preprocessing"]["fastp"]["--cut_front_mean_quality"] = preprocessing_sheet.cell_value(27, 1)
        if preprocessing_sheet.cell_value(28, 1) != "":
            self.conf["preprocessing"]["fastp"]["--cut_tail_window_size"] = preprocessing_sheet.cell_value(28, 1)
        if preprocessing_sheet.cell_value(29, 1) != "":
            self.conf["preprocessing"]["fastp"]["--cut_tail_mean_quality"] = preprocessing_sheet.cell_value(29, 1)
        if preprocessing_sheet.cell_value(30, 1) != "":
            self.conf["preprocessing"]["fastp"]["--cut_right_window_size"] = preprocessing_sheet.cell_value(30, 1)
        if preprocessing_sheet.cell_value(31, 1) != "":
            self.conf["preprocessing"]["fastp"]["--cut_right_mean_quality"] = preprocessing_sheet.cell_value(31, 1)
        if preprocessing_sheet.cell_value(32, 1) != "":
            self.conf["preprocessing"]["fastp"]["-Q"] = preprocessing_sheet.cell_value(32, 1)
        if preprocessing_sheet.cell_value(33, 1) != "":
            self.conf["preprocessing"]["fastp"]["-q"] = preprocessing_sheet.cell_value(33, 1)
        if preprocessing_sheet.cell_value(34, 1) != "":
            self.conf["preprocessing"]["fastp"]["-u"] = preprocessing_sheet.cell_value(34, 1)
        if preprocessing_sheet.cell_value(35, 1) != "":
            self.conf["preprocessing"]["fastp"]["-n"] = preprocessing_sheet.cell_value(35, 1)
        if preprocessing_sheet.cell_value(36, 1) != "":
            self.conf["preprocessing"]["fastp"]["-e"] = preprocessing_sheet.cell_value(36, 1)
        if preprocessing_sheet.cell_value(37, 1) != "":
            self.conf["preprocessing"]["fastp"]["-L"] = preprocessing_sheet.cell_value(37, 1)
        if preprocessing_sheet.cell_value(38, 1) != "":
            self.conf["preprocessing"]["fastp"]["--length_required"] = preprocessing_sheet.cell_value(38, 1)
        if preprocessing_sheet.cell_value(39, 1) != "":
            self.conf["preprocessing"]["fastp"]["--length_limit"] = preprocessing_sheet.cell_value(39, 1)
        if preprocessing_sheet.cell_value(40, 1) != "":
            self.conf["preprocessing"]["fastp"]["--low_complexity_filter"] = preprocessing_sheet.cell_value(40, 1)
        if preprocessing_sheet.cell_value(41, 1) != "":
            self.conf["preprocessing"]["fastp"]["--complexity_threshold"] = preprocessing_sheet.cell_value(41, 1)
        if preprocessing_sheet.cell_value(42, 1) != "":
            self.conf["preprocessing"]["fastp"]["--filter_by_index1"] = preprocessing_sheet.cell_value(42, 1)
        if preprocessing_sheet.cell_value(43, 1) != "":
            self.conf["preprocessing"]["fastp"]["--filter_by_index2"] = preprocessing_sheet.cell_value(43, 1)
        if preprocessing_sheet.cell_value(44, 1) != "":
            self.conf["preprocessing"]["fastp"]["--filter_by_index_threshold"] = preprocessing_sheet.cell_value(44, 1)
        if preprocessing_sheet.cell_value(45, 1) != "":
            self.conf["preprocessing"]["fastp"]["--correction"] = preprocessing_sheet.cell_value(45, 1)
        if preprocessing_sheet.cell_value(46, 1) != "":
            self.conf["preprocessing"]["fastp"]["--overlap_len_require"] = preprocessing_sheet.cell_value(46, 1)
        if preprocessing_sheet.cell_value(47, 1) != "":
            self.conf["preprocessing"]["fastp"]["--overlap_diff_limit"] = preprocessing_sheet.cell_value(47, 1)
        if preprocessing_sheet.cell_value(48, 1) != "":
            self.conf["preprocessing"]["fastp"]["--overlap_diff_percent_limit"] = preprocessing_sheet.cell_value(48, 1)
        if preprocessing_sheet.cell_value(49, 1) != "":
            self.conf["preprocessing"]["fastp"]["--umi"] = preprocessing_sheet.cell_value(49, 1)
        if preprocessing_sheet.cell_value(50, 1) != "":
            self.conf["preprocessing"]["fastp"]["--umi_loc"] = preprocessing_sheet.cell_value(50, 1)
        if preprocessing_sheet.cell_value(51, 1) != "":
            self.conf["preprocessing"]["fastp"]["--umi_len"] = preprocessing_sheet.cell_value(51, 1)
        if preprocessing_sheet.cell_value(52, 1) != "":
            self.conf["preprocessing"]["fastp"]["--umi_prefix"] = preprocessing_sheet.cell_value(52, 1)
        if preprocessing_sheet.cell_value(53, 1) != "":
            self.conf["preprocessing"]["fastp"]["--umi_skip"] = preprocessing_sheet.cell_value(53, 1)
        if preprocessing_sheet.cell_value(54, 1) != "":
            self.conf["preprocessing"]["fastp"]["-p"] = preprocessing_sheet.cell_value(54, 1)
        if preprocessing_sheet.cell_value(55, 1) != "":
            self.conf["preprocessing"]["fastp"]["-P"] = preprocessing_sheet.cell_value(55, 1)
        if preprocessing_sheet.cell_value(56, 1) != "":
            self.conf["preprocessing"]["fastp"]["-w"] = preprocessing_sheet.cell_value(56, 1)
    
    def read_identification_configuration(self):
        identification_sheet = xlrd.open_workbook(self.conf_file_path).sheet_by_name('identification')
        
        if identification_sheet.cell_value(1, 1) != True:
            self.conf["identification"]["enable"] = False

        if identification_sheet.cell_value(4, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--min-count"] = identification_sheet.cell_value(6, 1)
        if identification_sheet.cell_value(5, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--k-list"] = identification_sheet.cell_value(7, 1)
        if identification_sheet.cell_value(6, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--no-mercy"] = identification_sheet.cell_value(8, 1)
        if identification_sheet.cell_value(7, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--bubble-level"] = identification_sheet.cell_value(9, 1)
        if identification_sheet.cell_value(8, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--merge-level"] = identification_sheet.cell_value(10, 1)
        if identification_sheet.cell_value(9, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--prune-level"] = identification_sheet.cell_value(11, 1)
        if identification_sheet.cell_value(10, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--prune-depth"] = identification_sheet.cell_value(12, 1)
        if identification_sheet.cell_value(11, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--low-local-ratio"] = identification_sheet.cell_value(13, 1)
        if identification_sheet.cell_value(12, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--max-tip-len"] = identification_sheet.cell_value(14, 1)
        if identification_sheet.cell_value(13, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--no-local"] = identification_sheet.cell_value(15, 1)
        if identification_sheet.cell_value(14, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--kmin-1pass"] = identification_sheet.cell_value(16, 1)
        if identification_sheet.cell_value(15, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["-m"] = identification_sheet.cell_value(17, 1)
        if identification_sheet.cell_value(16, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--mem-flag"] = identification_sheet.cell_value(18, 1)
        if identification_sheet.cell_value(17, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["-t"] = identification_sheet.cell_value(19, 1)
        if identification_sheet.cell_value(18, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--no-hw-accel"] = identification_sheet.cell_value(20, 1)
        if identification_sheet.cell_value(19, 1) != "":
            self.conf["identification"]["assembly"]["megahit"]["--min-contig-len"] = identification_sheet.cell_value(21, 1)

        if identification_sheet.cell_value(4, 3) != "":
            self.conf["identification"]["assembly"]["canu"]["genomeSize="] = identification_sheet.cell_value(6, 3)
        if identification_sheet.cell_value(5, 3) != "":
            self.conf["identification"]["assembly"]["canu"]["-pacbio-raw"] = identification_sheet.cell_value(7, 3)
        if identification_sheet.cell_value(6, 3) != "":
            self.conf["identification"]["assembly"]["canu"]["-pacbio-corrected"] = identification_sheet.cell_value(8, 3)
        if identification_sheet.cell_value(7, 3) != "":
            self.conf["identification"]["assembly"]["canu"]["-nanopore-raw"] = identification_sheet.cell_value(9, 3)
        if identification_sheet.cell_value(8, 3) != "":
            self.conf["identification"]["assembly"]["canu"]["-nanopore-corrected"] = identification_sheet.cell_value(10, 3)

if __name__ == "__main__":
    cr = ConfigurationReader(sys.argv[1])
    cr.run()
