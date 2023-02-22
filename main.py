import os
import sys
import time
import json

import preprocessing
import assembly
import identification
import configuration_reader
import eggnog
import variant_calling
import tracer
import build_phylogenetic_tree

def main():

    start_time = time.time()
    start_process_time = time.process_time()

    argvs = sys.argv
    print('sys.argv =', argvs)

    # with open('./conf.json', 'r') as load_json:
    #     conf = json.load(load_json)

    if "-conf_file_path" in argvs:
        conf_file_path = argvs[argvs.index("-conf_file_path") + 1]
    else:
        print('Please input configuration file path.')
        exit()

    conf = configuration_reader.ConfigurationReader(conf_file_path).run()

    if '-o' in argvs:
        result_path = argvs[argvs.index('-o')+1]
    else:
        result_path = 'result'
    result_path += time.strftime('_%Y_%m_%d_%H_%M_%S', time.localtime())
    os.mkdir(result_path)

    if "-data_path" in argvs:
        data_path = argvs[argvs.index("-data_path") + 1]
    elif conf['identification']['enable'] != None:
        print("please input data path for identifying closest reference genome of resequencing module")
        exit()

    # 默认第二代测序
    sequencing_tech = '3gs' if '-3gs' in argvs else 'ngs'

    input_1 = argvs[argvs.index('-1')+1]
    input_2 = argvs[argvs.index('-2')+1] if '-2' in argvs else None

    if conf['preprocessing']['enable']:
        if sequencing_tech == 'ngs':
            preprocessing_obj = preprocessing.Preprocessing(result_path, conf, input_1, input_2)
            preprocessing_output_1, preprocessing_output_2 = preprocessing_obj.run()
        else:
            preprocessing_output_1, preprocessing_output_2 = input_1, input_2
    else:
        preprocessing_output_1, preprocessing_output_2 = input_1, input_2

    assembly_obj = assembly.Assembly(result_path, sequencing_tech, conf, preprocessing_output_1, preprocessing_output_2)
    contigs = assembly_obj.run() #返回的是contigs的地址

    identification_obj = identification.Identification(result_path, conf, data_path, contigs)
    # identification_obj.run()
    ref_genome_list = identification_obj.run()
    print(ref_genome_list)

    # use eggnog-mapper to annotate
    eggnog_obj = eggnog.Eggnog(result_path=result_path, contigs=contigs)
    eggnog_obj.run()

    # 变异检测
    variant_calling_obj = variant_calling.VariantCalling(result_path=result_path, reference_accession=ref_genome_list[0], input_1=contigs)
    variant_calling_obj.run()

    # 溯源推测
    tracer_obj = tracer.Tracer(result_path=result_path, blastn_result=result_path+"/identification/ref_viruses_rep_genomes_blast_out.xml")
    tracer_obj.run()

    # 构建系统发育树
    build_phylogenetic_tree_obj = build_phylogenetic_tree.TreeBuilder(result_path=result_path, ref_genome_list=ref_genome_list)
    build_phylogenetic_tree_obj.run()


    # 时间统计
    end_time = time.time()
    end_process_time = time.process_time()

    print('time.time = %s s' % (end_time - start_time))
    print('time.process_time = %s s' % (end_process_time - start_process_time))


if __name__ == '__main__':
    # sys.argv = ['main.py', '-f', 'SRR9523.fastq', '-o', 'result_SRR9523']
    main()


