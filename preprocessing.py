import subprocess
import os

class Preprocessing:

    def __init__(self, result_path, conf, input_1, input_2=None):
        self.result_path = result_path + '/preprocessing'
        self.conf = conf
        self.input_1 = input_1
        self.input_2 = input_2
    
    def run(self):
        os.mkdir(os.path.abspath('.') + '/' + self.result_path)
        if self.input_2 == None:
            self.__fastp_single_end()
            return self.result_path+'/fastp_output.fastq', None
        else:
            self.__fastp_paired_end()
            return self.result_path+'/fastp_output_1.fastq', self.result_path+'/fastp_output_2.fastq'


    def __fastp_single_end(self):
        print('start fastp single end')
        fastp_conf = self.conf['preprocessing']['fastp']
        com = "fastp -i %s -o %s -j %s -h %s " % (self.input_1, self.result_path+'/fastp_output.fastq', self.result_path+'/fastp.json', self.result_path+'/fastp.html')
        if fastp_conf['--phred64'] != None:
            com += '--phred64 '
        if fastp_conf['-V'] != None:
            com += '-V '
        if fastp_conf['-A'] != None:
            com += '-A '
        if fastp_conf['--adapter_sequence'] != None:
            com += '--adapter_sequence '+fastp_conf['--adapter_sequence']+' '
        # if fastp_conf['--adapter_sequence_r2'] != None:
        #     com += '--adapter_sequence_r2 '+fastp_conf['--adapter_sequence_r2']+' '
        if fastp_conf['--adapter_fasta'] != None:
            com += '--adapter_fasta '+fastp_conf['--adapter_fasta']+' '
        # if fastp_conf['--detect_adapter_for_pe'] != None:
        #     com += '--detect_adapter_for_pe '
        if fastp_conf['-f'] != None:
            com += '-f '+str(fastp_conf['-f'])+' '
        if fastp_conf['-t'] != None:
            com += '-t '+str(fastp_conf['-t'])+' '
        if fastp_conf['-b'] != None:
            com += '-b '+str(fastp_conf['-b'])+' '
        # if fastp_conf['-F'] != None:
        #     com += '-F '+str(fastp_conf['-F'])+' '
        # if fastp_conf['-T'] != None:
        #     com += '-T '+str(fastp_conf['-T'])+' '
        # if fastp_conf['-B'] != None:
        #     com += '-B '+str(fastp_conf['-B'])+' '
        if fastp_conf['--trim_poly_g'] != None:
            com += '--trim_poly_g '
        if fastp_conf['--poly_g_min_len'] != None:
            com += '--poly_g_min_len '+str(fastp_conf['--poly_g_min_len'])+' '
        if fastp_conf['-G'] != None:
            com += '-G '
        if fastp_conf['--trim_poly_x'] != None:
            com += '--trim_poly_x '
        if fastp_conf['--poly_x_min_len'] != None:
            com += '--poly_x_min_len '+str(fastp_conf['--poly_x_min_len'])+' '
        if fastp_conf['--cut_by_quality5'] != None:
            com += '--cut_by_quality5 '
        if fastp_conf['--cut_by_quality3'] != None:
            com += '--cut_by_quality3 '
        if fastp_conf['-r'] != None:
            com += '-r '
        if fastp_conf['-W'] != None:
            com += "-W "+str(fastp_conf['-W'])+' '
        if fastp_conf['--cut_mean_quality'] != None:
            com += "--cut_mean_quality "+str(fastp_conf['--cut_mean_quality'])+' '
        if fastp_conf['--cut_front_window_size'] != None:
            com += "--cut_front_window_size "+str(fastp_conf['--cut_front_window_size'])+' '
        if fastp_conf['--cut_front_mean_quality'] != None:
            com += "--cut_front_mean_quality "+str(fastp_conf['--cut_front_mean_quality'])+' '
        if fastp_conf['--cut_tail_window_size'] != None:
            com += "--cut_tail_window_size "+str(fastp_conf['--cut_tail_window_size'])+' '
        if fastp_conf['--cut_tail_mean_quality'] != None:
            com += "--cut_tail_mean_quality "+str(fastp_conf['--cut_tail_mean_quality'])+' '
        if fastp_conf['--cut_right_window_size'] != None:
            com += "--cut_right_window_size "+str(fastp_conf['--cut_right_window_size'])+' '
        if fastp_conf['--cut_right_mean_quality'] != None:
            com += "--cut_right_mean_quality "+str(fastp_conf['--cut_right_mean_quality'])+' '
        if fastp_conf['-Q'] != None:
            com += '-Q '
        if fastp_conf['-q'] != None:
            com += "-q "+str(fastp_conf['-q'])+' '
        if fastp_conf['-u'] != None:
            com += "-u "+str(fastp_conf['-u'])+' '
        if fastp_conf['-n'] != None:
            com += "-n "+str(fastp_conf['-n'])+' '
        if fastp_conf['-e'] != None:
            com += "-e "+str(fastp_conf['-e'])+' '
        if fastp_conf['-L'] != None:
            com += "-L "
        if fastp_conf['--length_required'] != None:
            com += "--length_required "+str(fastp_conf['--length_required'])+' '
        if fastp_conf['--length_limit'] != None:
            com += "--length_limit "+str(fastp_conf['--length_limit'])+' '
        if fastp_conf['--low_complexity_filter'] != None:
            com += "--low_complexity_filter "
        if fastp_conf['--complexity_threshold'] != None:
            com += "--complexity_threshold "+str(fastp_conf['--complexity_threshold'])+' '
        if fastp_conf['--filter_by_index1'] != None:
            com += "--filter_by_index1 "+str(fastp_conf['--filter_by_index1'])+' '
        if fastp_conf['--filter_by_index2'] != None:
            com += "--filter_by_index2 "+str(fastp_conf['--filter_by_index2'])+' '
        if fastp_conf['--filter_by_index_threshold'] != None:
            com += "--filter_by_index_threshold "+str(fastp_conf['--filter_by_index_threshold'])+' '
        # if fastp_conf['--correction'] != None:
        #     com += "--correction "
        # if fastp_conf['--overlap_len_require'] != None:
        #     com += "--overlap_len_require "+str(fastp_conf['--overlap_len_require'])+' '
        # if fastp_conf['--overlap_diff_limit'] != None:
        #     com += "--overlap_diff_limit "+str(fastp_conf['--overlap_diff_limit'])+' '
        # if fastp_conf['--overlap_diff_percent_limit'] != None:
        #     com += "--overlap_diff_percent_limit "+str(fastp_conf['--overlap_diff_percent_limit'])+' '
        if fastp_conf['--umi'] != None:
            com += '--umi '
        if fastp_conf['--umi_loc'] != None:
            com += '--umi_loc '+fastp_conf['--umi_loc']+' '
        if fastp_conf['--umi_len'] != None:
            com += '--umi_len '+str(fastp_conf['--umi_len'])+' '
        if fastp_conf['--umi_prefix'] != None:
            com += '--umi_prefix '+fastp_conf['--umi_prefix']+' '
        if fastp_conf['--umi_skip'] != None:
            com += '--umi_skip '+str(fastp_conf['--umi_skip'])+' '
        if fastp_conf['-p'] != None:
            com += '-p '
        if fastp_conf['-P'] != None:
            com += '-P '+str(fastp_conf['-P'])+' '
        if fastp_conf['-w'] != None:
            com += '-w '+str(fastp_conf['-w'])
        subprocess.run(com, shell=True, check=True)
        print('end fastp single end')


    def __fastp_paired_end(self):
        print('start fastp paired end')
        fastp_conf = self.conf['preprocessing']['fastp']
        com = "fastp -i %s -I %s -o %s -O %s -j %s -h %s " % (self.input_1, self.input_2, self.result_path+'/fastp_output_1.fastq', self.result_path+'/fastp_output_2.fastq', self.result_path+'/fastp.json', self.result_path+'/fastp.html')
        if fastp_conf['--phred64'] != None:
            com += '--phred64 '
        if fastp_conf['-V'] != None:
            com += '-V '
        if fastp_conf['-A'] != None:
            com += '-A '
        if fastp_conf['--adapter_sequence'] != None:
            com += '--adapter_sequence '+fastp_conf['--adapter_sequence']+' '
        if fastp_conf['--adapter_sequence_r2'] != None:
            com += '--adapter_sequence_r2 '+fastp_conf['--adapter_sequence_r2']+' '
        if fastp_conf['--adapter_fasta'] != None:
            com += '--adapter_fasta '+fastp_conf['--adapter_fasta']+' '
        if fastp_conf['--detect_adapter_for_pe'] != None:
            com += '--detect_adapter_for_pe '
        if fastp_conf['-f'] != None:
            com += '-f '+str(fastp_conf['-f'])+' '
        if fastp_conf['-t'] != None:
            com += '-t '+str(fastp_conf['-t'])+' '
        if fastp_conf['-b'] != None:
            com += '-b '+str(fastp_conf['-b'])+' '
        if fastp_conf['-F'] != None:
            com += '-F '+str(fastp_conf['-F'])+' '
        if fastp_conf['-T'] != None:
            com += '-T '+str(fastp_conf['-T'])+' '
        if fastp_conf['-B'] != None:
            com += '-B '+str(fastp_conf['-B'])+' '
        if fastp_conf['--trim_poly_g'] != None:
            com += '--trim_poly_g '
        if fastp_conf['--poly_g_min_len'] != None:
            com += '--poly_g_min_len '+str(fastp_conf['--poly_g_min_len'])+' '
        if fastp_conf['-G'] != None:
            com += '-G '
        if fastp_conf['--trim_poly_x'] != None:
            com += '--trim_poly_x '
        if fastp_conf['--poly_x_min_len'] != None:
            com += '--poly_x_min_len '+str(fastp_conf['--poly_x_min_len'])+' '
        if fastp_conf['--cut_by_quality5'] != None:
            com += '--cut_by_quality5 '
        if fastp_conf['--cut_by_quality3'] != None:
            com += '--cut_by_quality3 '
        if fastp_conf['-r'] != None:
            com += '-r '
        if fastp_conf['-W'] != None:
            com += "-W "+str(fastp_conf['-W'])+' '
        if fastp_conf['--cut_mean_quality'] != None:
            com += "--cut_mean_quality "+str(fastp_conf['--cut_mean_quality'])+' '
        if fastp_conf['--cut_front_window_size'] != None:
            com += "--cut_front_window_size "+str(fastp_conf['--cut_front_window_size'])+' '
        if fastp_conf['--cut_front_mean_quality'] != None:
            com += "--cut_front_mean_quality "+str(fastp_conf['--cut_front_mean_quality'])+' '
        if fastp_conf['--cut_tail_window_size'] != None:
            com += "--cut_tail_window_size "+str(fastp_conf['--cut_tail_window_size'])+' '
        if fastp_conf['--cut_tail_mean_quality'] != None:
            com += "--cut_tail_mean_quality "+str(fastp_conf['--cut_tail_mean_quality'])+' '
        if fastp_conf['--cut_right_window_size'] != None:
            com += "--cut_right_window_size "+str(fastp_conf['--cut_right_window_size'])+' '
        if fastp_conf['--cut_right_mean_quality'] != None:
            com += "--cut_right_mean_quality "+str(fastp_conf['--cut_right_mean_quality'])+' '
        if fastp_conf['-Q'] != None:
            com += '-Q '
        if fastp_conf['-q'] != None:
            com += "-q "+str(fastp_conf['-q'])+' '
        if fastp_conf['-u'] != None:
            com += "-u "+str(fastp_conf['-u'])+' '
        if fastp_conf['-n'] != None:
            com += "-n "+str(fastp_conf['-n'])+' '
        if fastp_conf['-e'] != None:
            com += "-e "+str(fastp_conf['-e'])+' '
        if fastp_conf['-L'] != None:
            com += "-L "
        if fastp_conf['--length_required'] != None:
            com += "--length_required "+str(fastp_conf['--length_required'])+' '
        if fastp_conf['--length_limit'] != None:
            com += "--length_limit "+str(fastp_conf['--length_limit'])+' '
        if fastp_conf['--low_complexity_filter'] != None:
            com += "--low_complexity_filter "
        if fastp_conf['--complexity_threshold'] != None:
            com += "--complexity_threshold "+str(fastp_conf['--complexity_threshold'])+' '
        if fastp_conf['--filter_by_index1'] != None:
            com += "--filter_by_index1 "+str(fastp_conf['--filter_by_index1'])+' '
        if fastp_conf['--filter_by_index2'] != None:
            com += "--filter_by_index2 "+str(fastp_conf['--filter_by_index2'])+' '
        if fastp_conf['--filter_by_index_threshold'] != None:
            com += "--filter_by_index_threshold "+str(fastp_conf['--filter_by_index_threshold'])+' '
        if fastp_conf['--correction'] != None:
            com += "--correction "
        if fastp_conf['--overlap_len_require'] != None:
            com += "--overlap_len_require "+str(fastp_conf['--overlap_len_require'])+' '
        if fastp_conf['--overlap_diff_limit'] != None:
            com += "--overlap_diff_limit "+str(fastp_conf['--overlap_diff_limit'])+' '
        if fastp_conf['--overlap_diff_percent_limit'] != None:
            com += "--overlap_diff_percent_limit "+str(fastp_conf['--overlap_diff_percent_limit'])+' '
        if fastp_conf['--umi'] != None:
            com += '--umi '
        if fastp_conf['--umi_loc'] != None:
            com += '--umi_loc '+fastp_conf['--umi_loc']+' '
        if fastp_conf['--umi_len'] != None:
            com += '--umi_len '+str(fastp_conf['--umi_len'])+' '
        if fastp_conf['--umi_prefix'] != None:
            com += '--umi_prefix '+fastp_conf['--umi_prefix']+' '
        if fastp_conf['--umi_skip'] != None:
            com += '--umi_skip '+str(fastp_conf['--umi_skip'])+' '
        if fastp_conf['-p'] != None:
            com += '-p '
        if fastp_conf['-P'] != None:
            com += '-P '+str(fastp_conf['-P'])+' '
        if fastp_conf['-w'] != None:
            com += '-w '+str(fastp_conf['-w'])
        subprocess.run(com, shell=True, check=True)
        print('end fastp paired end')

