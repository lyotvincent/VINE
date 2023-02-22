from Bio.Blast.Applications import NcbiblastnCommandline
import subprocess
import xlrd
import os
import numpy as np
from keras.models import load_model
import time

import calculating_genome_similarity

class Identification:

    __family_labels_dict = {0: 'Ackermannviridae', 1: 'Adenoviridae', 2: 'Alloherpesviridae', 3: 'Alphaflexiviridae', 4: 'Alphasatellitidae', 5: 'Alphatetraviridae', 6: 'Alvernaviridae', 7: 'Amalgaviridae', 8: 'Amnoonviridae', 9: 'Ampullaviridae', 10: 'Anelloviridae',
        11: 'Arenaviridae', 12: 'Arteriviridae', 13: 'Ascoviridae', 14: 'Asfarviridae', 15: 'Aspiviridae', 16: 'Astroviridae', 17: 'Avsunviroidae', 18: 'Bacilladnaviridae', 19: 'Baculoviridae', 20: 'Barnaviridae',
        21: 'Benyviridae', 22: 'Betaflexiviridae', 23: 'Bicaudaviridae', 24: 'Bidnaviridae', 25: 'Birnaviridae', 26: 'Bornaviridae', 27: 'Botourmiaviridae', 28: 'Bromoviridae', 29: 'Caliciviridae', 30: 'Carmotetraviridae',
        31: 'Caulimoviridae', 32: 'Chrysoviridae', 33: 'Chuviridae', 34: 'Circoviridae', 35: 'Closteroviridae', 36: 'Coronaviridae', 37: 'Corticoviridae', 38: 'Cruliviridae', 39: 'Deltaflexiviridae', 40: 'Dicistroviridae',
        41: 'Endornaviridae', 42: 'Euroniviridae', 43: 'Filoviridae', 44: 'Fimoviridae', 45: 'Flaviviridae', 46: 'Fusariviridae', 47: 'Fuselloviridae', 48: 'Gammaflexiviridae', 49: 'Geminiviridae', 50: 'Genomoviridae',
        51: 'Globuloviridae', 52: 'Guttaviridae', 53: 'Hantaviridae', 54: 'Hepadnaviridae', 55: 'Hepeviridae', 56: 'Herelleviridae', 57: 'Herpesviridae', 58: 'Hypoviridae', 59: 'Hytrosaviridae', 60: 'Iflaviridae',
        61: 'Inoviridae', 62: 'Iridoviridae', 63: 'Kitaviridae', 64: 'Lavidaviridae', 65: 'Lipothrixviridae', 66: 'Lispiviridae', 67: 'Luteoviridae', 68: 'Malacoherpesviridae', 69: 'Marnaviridae', 70: 'Marseilleviridae',
        71: 'Matonaviridae', 72: 'Medioniviridae', 73: 'Megabirnaviridae', 74: 'Mesoniviridae', 75: 'Microviridae', 76: 'Mimiviridae', 77: 'Mymonaviridae', 78: 'Myoviridae', 79: 'Mypoviridae', 80: 'Nairoviridae',
        81: 'Nanoviridae', 82: 'Narnaviridae', 83: 'Nimaviridae', 84: 'Nodaviridae', 85: 'Nudiviridae', 86: 'Nyamiviridae', 87: 'Orthomyxoviridae', 88: 'Papillomaviridae', 89: 'Paramyxoviridae', 90: 'Partitiviridae',
        91: 'Parvoviridae', 92: 'Peribunyaviridae', 93: 'Permutotetraviridae', 94: 'Phasmaviridae', 95: 'Phenuiviridae', 96: 'Phycodnaviridae', 97: 'Picobirnaviridae', 98: 'Picornaviridae', 99: 'Pithoviridae', 100: 'Plasmaviridae',
        101: 'Pleolipoviridae', 102: 'Pneumoviridae', 103: 'Podoviridae', 104: 'Polycipiviridae', 105: 'Polydnaviridae', 106: 'Polyomaviridae', 107: 'Pospiviroidae', 108: 'Potyviridae', 109: 'Poxviridae', 110: 'Qinviridae',
        111: 'Quadriviridae', 112: 'Reoviridae', 113: 'Retroviridae', 114: 'Rhabdoviridae', 115: 'Roniviridae', 116: 'Rudiviridae', 117: 'Secoviridae', 118: 'Siphoviridae', 119: 'Smacoviridae', 120: 'Solemoviridae',
        121: 'Solinviviridae', 122: 'Sphaerolipoviridae', 123: 'Sunviridae', 124: 'Tectiviridae', 125: 'Tobaniviridae', 126: 'Togaviridae', 127: 'Tolecusatellitidae', 128: 'Tombusviridae', 129: 'Tospoviridae', 130: 'Totiviridae',
        131: 'Tristromaviridae', 132: 'Turriviridae', 133: 'Tymoviridae', 134: 'Virgaviridae', 135: 'Xinmoviridae', 136: 'Yueviridae'}


    def __init__(self, result_path, conf, data_path, contigs_path):
        self.result_path = result_path
        self.conf = conf
        self.data_path = data_path
        self.__contigs_path = contigs_path
    
    def run(self):
        print('begin identification')
        # temp_time = time.time()
        # map_vector = self._map_identification()
        # print('map time = %s' % (time.time() - temp_time))
        # temp_time = time.time()
        cnn_vector = self._cnn_identification()
        # print('cnn time = %s' % (time.time() - temp_time))
        # temp_time = time.time()
        blast_vector, ref_genome_list = self._blast_identification()
        # print('blast time = %s' % (time.time() - temp_time))
        # print(map_vector.tolist())
        print('cnn_vector = '+str(cnn_vector.tolist()))
        print('blast_vector = '+str(blast_vector.tolist()))

        combined_vector = (0.7*blast_vector+0.3*cnn_vector).tolist()
        print('combined_vector = '+str(combined_vector))
        predicted_family_label = self.__family_labels_dict[combined_vector.index(max(combined_vector))]
        print(predicted_family_label)
        
        # self._write_result_record(0.1, 'cnn_identification_result = '+predicted_family_label+'\n' )
        # combined_vector = (0.2*cnn_vector+0.8*map_vector).tolist()
        # predicted_family_label = self.__family_labels_dict[combined_vector.index(max(combined_vector))]
        # self._write_result_record(0.2, 'cnn_identification_result = '+predicted_family_label+'\n' )
        # combined_vector = (0.3*cnn_vector+0.7*map_vector).tolist()
        # predicted_family_label = self.__family_labels_dict[combined_vector.index(max(combined_vector))]
        # self._write_result_record(0.3, 'cnn_identification_result = '+predicted_family_label+'\n' )
        # combined_vector = (0.4*cnn_vector+0.6*map_vector).tolist()
        # predicted_family_label = self.__family_labels_dict[combined_vector.index(max(combined_vector))]
        # self._write_result_record(0.4, 'cnn_identification_result = '+predicted_family_label+'\n' )
        # combined_vector = (0.5*cnn_vector+0.5*map_vector).tolist()
        # predicted_family_label = self.__family_labels_dict[combined_vector.index(max(combined_vector))]
        # self._write_result_record(0.5, 'cnn_identification_result = '+predicted_family_label+'\n' )
        # combined_vector = (0.6*cnn_vector+0.4*map_vector).tolist()
        # predicted_family_label = self.__family_labels_dict[combined_vector.index(max(combined_vector))]
        # self._write_result_record(0.6, 'cnn_identification_result = '+predicted_family_label+'\n' )
        # combined_vector = (0.7*cnn_vector+0.3*map_vector).tolist()
        # predicted_family_label = self.__family_labels_dict[combined_vector.index(max(combined_vector))]
        # self._write_result_record(0.7, 'cnn_identification_result = '+predicted_family_label+'\n' )
        # combined_vector = (0.8*cnn_vector+0.2*map_vector).tolist()
        # predicted_family_label = self.__family_labels_dict[combined_vector.index(max(combined_vector))]
        # self._write_result_record(0.8, 'cnn_identification_result = '+predicted_family_label+'\n' )
        # combined_vector = (0.9*cnn_vector+0.1*map_vector).tolist()
        # predicted_family_label = self.__family_labels_dict[combined_vector.index(max(combined_vector))]
        # self._write_result_record(0.9, 'cnn_identification_result = '+predicted_family_label+'\n' )

        ref_genome_list = self._format_ref_list(ref_genome_list)

        print('end identification')
        return [i[0] for i in ref_genome_list]

    def _write_result_record(self, weight, content):
    
        temp_file = open('./result_record_'+str(weight)+'.txt', 'a+')
        temp_file.write(content)
        temp_file.close()

    def _map_identification(self):
        genome_similarity_calculator = calculating_genome_similarity.GenomeSimilarityCalculator(self.__contigs_path, self.data_path, similar_genome_number=self.conf['identification']['number_of_candidate_similar_genome'])
        similar_genome_list = genome_similarity_calculator.search_similar_genome_from_dataset()
        print(similar_genome_list)
        # [['NC_004718', 0.0283203125], ['NC_014470', 0.017578125], ['NC_009021', 0.001953125], ['NC_005038', 0.0009765625], ['NC_031024', 0.0009765625], ['NC_031006', 0.0009765625], ['NC_029024', 0.0009765625], ['NC_022103', 0.0009765625], ['NC_025217', 0.0009765625], ['NC_032629', 0.0009765625], ['NC_032584', 0.0009765625], ['NC_002526', 0.0009765625], ['NC_028805', 0.0009765625], ['NC_028814', 0.0009765625], ['NC_007988', 0.0009765625], ['NC_029006', 0.0009765625], ['NC_010105', 0.0009765625], ['NC_011811', 0.0009765625], ['NC_015292', 0.0009765625], ['NC_012741', 0.0009765625]]

        family_sheet = xlrd.open_workbook(os.path.dirname(os.path.realpath(__file__))+'/configurations/sequences.xlsx').sheet_by_name('Sheet1')

        for nrow in range(family_sheet.nrows):
            for genome_item in similar_genome_list:
                if family_sheet.cell_value(nrow, 0) in genome_item:
                    genome_item.append(family_sheet.cell_value(nrow, 3))
        # print(similar_genome_list)

        family_weight_dict = {}

        for genome_item in similar_genome_list:
            if len(genome_item) < 3:
                continue
            if not family_weight_dict.__contains__(genome_item[2]):
                family_weight_dict[genome_item[2]] = [genome_item[1], 1]
            else:
                family_weight_dict[genome_item[2]][0] += genome_item[1]
                family_weight_dict[genome_item[2]][1] += 1

        for key in family_weight_dict:
            family_weight_dict[key] = family_weight_dict[key][0] / family_weight_dict[key][1]

        total_weight = 0
        for key in family_weight_dict:
            total_weight += family_weight_dict[key]
        for key in family_weight_dict:
            family_weight_dict[key] = family_weight_dict[key]/total_weight

        map_identification_list = []

        for key in family_weight_dict:
            # map_identification_list.append([key, family_weight_dict[key][0] / family_weight_dict[key][1]])
            map_identification_list.append([key, family_weight_dict[key]])

        sorted(map_identification_list, key=lambda x:x[1])

        print(map_identification_list)

        # 把相似度结果放大到十分位
        multiple = 1
        # if map_identification_list[0][0] != '':
        #     temp_number = str(map_identification_list[0][1]).split('.')[1]
        #     for i in temp_number:
        #         if i != '0':
        #             break
        #         multiple *= 10

        map_identification_list = []

        for key in self.__family_labels_dict:
            if family_weight_dict.__contains__(self.__family_labels_dict[key]):
                map_identification_list.append( family_weight_dict[self.__family_labels_dict[key]] * multiple )
            else:
                map_identification_list.append(0)

        print(map_identification_list)

        map_identification_vector = np.array(map_identification_list)

        return map_identification_vector


    def _cnn_identification(self):
        
        # family_labels = {'Ackermannviridae': '0', 'Adenoviridae': '1', 'Alloherpesviridae': '2', 'Alphaflexiviridae': '3', 'Alphasatellitidae': '4', 'Alphatetraviridae': '5', 'Alvernaviridae': '6', 'Amalgaviridae': '7', 'Amnoonviridae': '8', 'Ampullaviridae': '9', 'Anelloviridae': '10',
        # 'Arenaviridae': '11', 'Arteriviridae': '12', 'Ascoviridae': '13', 'Asfarviridae': '14', 'Aspiviridae': '15', 'Astroviridae': '16', 'Avsunviroidae': '17', 'Bacilladnaviridae': '18', 'Baculoviridae': '19', 'Barnaviridae': '20',
        # 'Benyviridae': '21', 'Betaflexiviridae': '22', 'Bicaudaviridae': '23', 'Bidnaviridae': '24', 'Birnaviridae': '25', 'Bornaviridae': '26', 'Botourmiaviridae': '27', 'Bromoviridae': '28', 'Caliciviridae': '29', 'Carmotetraviridae': '30',
        # 'Caulimoviridae': '31', 'Chrysoviridae': '32', 'Chuviridae': '33', 'Circoviridae': '34', 'Closteroviridae': '35', 'Coronaviridae': '36', 'Corticoviridae': '37', 'Cruliviridae': '38', 'Deltaflexiviridae': '39', 'Dicistroviridae': '40',
        # 'Endornaviridae': '41', 'Euroniviridae': '42', 'Filoviridae': '43', 'Fimoviridae': '44', 'Flaviviridae': '45', 'Fusariviridae': '46', 'Fuselloviridae': '47', 'Gammaflexiviridae': '48', 'Geminiviridae': '49', 'Genomoviridae': '50',
        # 'Globuloviridae': '51', 'Guttaviridae': '52', 'Hantaviridae': '53', 'Hepadnaviridae': '54', 'Hepeviridae': '55', 'Herelleviridae': '56', 'Herpesviridae': '57', 'Hypoviridae': '58', 'Hytrosaviridae': '59', 'Iflaviridae': '60',
        # 'Inoviridae': '61', 'Iridoviridae': '62', 'Kitaviridae': '63', 'Lavidaviridae': '64', 'Lipothrixviridae': '65', 'Lispiviridae': '66', 'Luteoviridae': '67', 'Malacoherpesviridae': '68', 'Marnaviridae': '69', 'Marseilleviridae': '70',
        # 'Matonaviridae': '71', 'Medioniviridae': '72', 'Megabirnaviridae': '73', 'Mesoniviridae': '74', 'Microviridae': '75', 'Mimiviridae': '76', 'Mymonaviridae': '77', 'Myoviridae': '78', 'Mypoviridae': '79', 'Nairoviridae': '80',
        # 'Nanoviridae': '81', 'Narnaviridae': '82', 'Nimaviridae': '83', 'Nodaviridae': '84', 'Nudiviridae': '85', 'Nyamiviridae': '86', 'Orthomyxoviridae': '87', 'Papillomaviridae': '88', 'Paramyxoviridae': '89', 'Partitiviridae': '90',
        # 'Parvoviridae': '91', 'Peribunyaviridae': '92', 'Permutotetraviridae': '93', 'Phasmaviridae': '94', 'Phenuiviridae': '95', 'Phycodnaviridae': '96', 'Picobirnaviridae': '97', 'Picornaviridae': '98', 'Pithoviridae': '99', 'Plasmaviridae': '100',
        # 'Pleolipoviridae': '101', 'Pneumoviridae': '102', 'Podoviridae': '103', 'Polycipiviridae': '104', 'Polydnaviridae': '105', 'Polyomaviridae': '106', 'Pospiviroidae': '107', 'Potyviridae': '108', 'Poxviridae': '109', 'Qinviridae': '110',
        # 'Quadriviridae': '111', 'Reoviridae': '112', 'Retroviridae': '113', 'Rhabdoviridae': '114', 'Roniviridae': '115', 'Rudiviridae': '116', 'Secoviridae': '117', 'Siphoviridae': '118', 'Smacoviridae': '119', 'Solemoviridae': '120',
        # 'Solinviviridae': '121', 'Sphaerolipoviridae': '122', 'Sunviridae': '123', 'Tectiviridae': '124', 'Tobaniviridae': '125', 'Togaviridae': '126', 'Tolecusatellitidae': '127', 'Tombusviridae': '128', 'Tospoviridae': '129', 'Totiviridae': '130',
        # 'Tristromaviridae': '131', 'Turriviridae': '132', 'Tymoviridae': '133', 'Virgaviridae': '134', 'Xinmoviridae': '135', 'Yueviridae': '136'}

        contigs = []
        contigs_weights = []

        # 读取contigs firstly
        contigs_file = open(self.__contigs_path, 'r')
        contigs_lines = contigs_file.readlines()
        contigs_file.close()
        for contig in contigs_lines:
            if contig.startswith('>'):
                continue
            contig = contig.strip()
            for i in range(len(contig)//10000+1):
                temp_contig = contig[i*10000:i*10000+10000]
                contigs.append(temp_contig)
                contigs_weights.append(len(temp_contig)/10000)

            reversed_contig = contig[::-1]
            for i in range(len(reversed_contig)//10000+1):
                temp_contig = reversed_contig[i*10000:i*10000+10000]
                contigs.append(temp_contig[::-1])
                contigs_weights.append(len(temp_contig)/10000)


        test_data = self._vectorize_sequences(contigs, dimension=10000)

        print("Using loaded model to predict...")
        virus_classification_model = load_model(os.path.dirname(os.path.realpath(__file__))+'/virus_categorical_cnn_model_20200514.h5')
        predicted = virus_classification_model.predict(test_data)
        # print("Predicted softmax vector is: ")
        # [[0.0242 0.6763 0.2995]]
        # print(predicted)

        combined_predicted_softmax_vector = np.zeros(shape=(137))
        for i, prediction_result in enumerate(predicted):
            combined_predicted_softmax_vector = combined_predicted_softmax_vector + prediction_result*contigs_weights[i]
        
        vector_sum = sum(combined_predicted_softmax_vector)
        combined_predicted_softmax_vector = combined_predicted_softmax_vector/vector_sum
        return combined_predicted_softmax_vector
        # combined_predicted_softmax_vector = combined_predicted_softmax_vector.tolist()
        # predicted_family_label = self.__family_labels_dict[combined_predicted_softmax_vector.index(max(combined_predicted_softmax_vector))]
        # print(predicted_family_label)

        # return predicted_family_label

    def _vectorize_sequences(self, sequences, dimension):

        # token_index = {'A': 0, 'T': 1, 'C': 2, 'G': 3, 'U': 4, 'W': 5, 'S': 6, 'K': 7, 'M': 8, 'Y': 9, 'R': 10, 'B': 11, 'D': 12, 'H': 13, 'V': 14, 'N': 15}
        token_index = {'A': 0, 'T': 1, 'C': 2, 'G': 3, 'W': 4, 'S': 5, 'K': 6, 'M': 7, 'Y': 8, 'R': 9, 'B': 10, 'D': 11, 'H': 12, 'V': 13, 'N': 14}
        token_index_len = len(token_index)

        # print('Vectorizing data...')
        results = np.zeros(shape=(len(sequences), dimension, token_index_len))

        for i, sample in enumerate(sequences):
            for j, character in enumerate(sample):
                index = token_index.get(character)
                if index is None:
                    print('index is none: ', character)
                    exit()
                results[i, j, index] = 1.
        # print('Finish vectorizing data...')
        return results

    def _blast_identification(self):

        os.mkdir(self.result_path+"/identification/")

        # blastn_conf = self.conf['identification']['blastn']
        blastn_cline = NcbiblastnCommandline(query=self.__contigs_path, db="~/data/blastdb/ref_viruses_rep_genomes", outfmt=7, out=self.result_path+"/identification/ref_viruses_rep_genomes_blast_out.xml", num_threads=24, evalue=1e-5, num_alignments=10)
        # if not blastn_conf['num_threads'] == 0:
        #     blastn_cline.set_parameter('num_threads', blastn_conf['num_threads'])
        # if not blastn_conf['evalue'] == 0:
        #     blastn_cline.set_parameter('evalue', blastn_conf['evalue'])
        # if not blastn_conf['num_alignments'] == 0:
        #     blastn_cline.set_parameter('num_alignments', blastn_conf['num_alignments'])
        # if not blastn_conf['task'] == 0:
        #     blastn_cline.set_parameter('task', blastn_conf['task'])
        # if not blastn_conf['penalty'] == 0:
        #     blastn_cline.set_parameter('penalty', blastn_conf['penalty'])
        # if not blastn_conf['reward'] == 0:
        #     blastn_cline.set_parameter('reward', blastn_conf['reward'])
        # if not blastn_conf['dust'] == 0:
        #     blastn_cline.set_parameter('dust', blastn_conf['dust'])
        # if not blastn_conf['filtering_db'] == 0:
        #     blastn_cline.set_parameter('filtering_db', blastn_conf['filtering_db'])
        # if not blastn_conf['window_masker_taxid'] == 0:
        #     blastn_cline.set_parameter('window_masker_taxid', blastn_conf['window_masker_taxid'])
        # if not blastn_conf['no_greedy'] == 0:
        #     blastn_cline.set_parameter('no_greedy', blastn_conf['no_greedy'])
        # if not blastn_conf['min_raw_gapped_score'] == 0:
        #     blastn_cline.set_parameter('min_raw_gapped_score', blastn_conf['min_raw_gapped_score'])
        # if not blastn_conf['ungapped'] == 0:
        #     blastn_cline.set_parameter('ungapped', blastn_conf['ungapped'])
        # if not blastn_conf['off_diagonal_range'] == 0:
        #     blastn_cline.set_parameter('off_diagonal_range', blastn_conf['off_diagonal_range'])
        print(blastn_cline)
        stdout, stderr = blastn_cline()
        print(stdout)
        print(stderr)

        blast_result_file = open(self.result_path+"/identification/ref_viruses_rep_genomes_blast_out.xml", 'r')
        blast_lines = blast_result_file.readlines()
        blast_result_file.close()

        ref_list = []

        # contig_len = 0
        for blast_line in blast_lines:
            if blast_line.startswith('#'):
                continue
                # if blast_line.startswith('# Query:'):
                #     contig_len = blast_line.split()[-1][4:]
            else:
                items = blast_line.split()
                items[2] = float(items[2])
                items[3] = float(items[3])
                if items[2] >= 50:
                    # ref_list.append([items[1].split('.')[0], items[2], items[3]])
                    ref_list.append([items[1], items[2], items[3]])
        


        family_sheet = xlrd.open_workbook(os.path.dirname(os.path.realpath(__file__))+'/configurations/sequences.xlsx').sheet_by_name('Sheet1')

        for nrow in range(family_sheet.nrows):
            for ref_item in ref_list:
                if family_sheet.cell_value(nrow, 0) == ref_item[0].split('.')[0]:
                    ref_item.append(family_sheet.cell_value(nrow, 3))
        
        family_weight_dict = {}

        for genome_item in ref_list:
            if len(genome_item) < 4:
                continue
            if not family_weight_dict.__contains__(genome_item[3]):
                family_weight_dict[genome_item[3]] = genome_item[1] * genome_item[2]
            else:
                family_weight_dict[genome_item[3]] += genome_item[1] * genome_item[2]

        total_weight = 0
        for key in family_weight_dict:
            total_weight += family_weight_dict[key]
        for key in family_weight_dict:
            family_weight_dict[key] = family_weight_dict[key]/total_weight


        map_identification_list = []
        for key in family_weight_dict:
            # map_identification_list.append([key, family_weight_dict[key][0] / family_weight_dict[key][1]])
            map_identification_list.append([key, family_weight_dict[key]])

        sorted(map_identification_list, key=lambda x:x[1])
        print(map_identification_list)

        map_identification_list = []

        for key in self.__family_labels_dict:
            if family_weight_dict.__contains__(self.__family_labels_dict[key]):
                map_identification_list.append( family_weight_dict[self.__family_labels_dict[key]])
            else:
                map_identification_list.append(0)

        print(map_identification_list)

        map_identification_vector = np.array(map_identification_list)

        return map_identification_vector, ref_list

    def _format_ref_list(self, ref_genome_list):
        ref_dict = {}

        for ref in ref_genome_list:
            if not ref_dict.__contains__(ref[0]):
                ref_dict[ref[0]] = ref[1] * ref[2]
            else:
                ref_dict[ref[0]] += ref[1] * ref[2]
        
        ref_list = []
        for key in ref_dict:
            # map_identification_list.append([key, family_weight_dict[key][0] / family_weight_dict[key][1]])
            ref_list.append([key, ref_dict[key]])

        sorted(ref_list, key=lambda x:x[1])
        print(ref_list)
        return ref_list


    def _map_identification_old(self):

        os.mkdir(self.result_path+"/identification/")

        # blastn_conf = self.conf['identification']['blastn']
        blastn_cline = NcbiblastnCommandline(query=self.__contigs_path, db="~/data/blastdb/ref_viruses_rep_genomes", outfmt=7, out=self.result_path+"/identification/ncbi_bacteria_blast_out.xml", num_threads=24, evalue=1e-5, num_alignments=10)
        # if not blastn_conf['num_threads'] == 0:
        #     blastn_cline.set_parameter('num_threads', blastn_conf['num_threads'])
        # if not blastn_conf['evalue'] == 0:
        #     blastn_cline.set_parameter('evalue', blastn_conf['evalue'])
        # if not blastn_conf['num_alignments'] == 0:
        #     blastn_cline.set_parameter('num_alignments', blastn_conf['num_alignments'])
        # if not blastn_conf['task'] == 0:
        #     blastn_cline.set_parameter('task', blastn_conf['task'])
        # if not blastn_conf['penalty'] == 0:
        #     blastn_cline.set_parameter('penalty', blastn_conf['penalty'])
        # if not blastn_conf['reward'] == 0:
        #     blastn_cline.set_parameter('reward', blastn_conf['reward'])
        # if not blastn_conf['dust'] == 0:
        #     blastn_cline.set_parameter('dust', blastn_conf['dust'])
        # if not blastn_conf['filtering_db'] == 0:
        #     blastn_cline.set_parameter('filtering_db', blastn_conf['filtering_db'])
        # if not blastn_conf['window_masker_taxid'] == 0:
        #     blastn_cline.set_parameter('window_masker_taxid', blastn_conf['window_masker_taxid'])
        # if not blastn_conf['no_greedy'] == 0:
        #     blastn_cline.set_parameter('no_greedy', blastn_conf['no_greedy'])
        # if not blastn_conf['min_raw_gapped_score'] == 0:
        #     blastn_cline.set_parameter('min_raw_gapped_score', blastn_conf['min_raw_gapped_score'])
        # if not blastn_conf['ungapped'] == 0:
        #     blastn_cline.set_parameter('ungapped', blastn_conf['ungapped'])
        # if not blastn_conf['off_diagonal_range'] == 0:
        #     blastn_cline.set_parameter('off_diagonal_range', blastn_conf['off_diagonal_range'])
        print(blastn_cline)
        stdout, stderr = blastn_cline()
        print(stdout)
        print(stderr)

        blast_result_file = open(self.result_path+"/identification/ncbi_bacteria_blast_out.xml", 'r')
        blast_lines = blast_result_file.readlines()
        blast_result_file.close()

        ref_list = []

        contig_len = 0
        for blast_line in blast_lines:
            if blast_line.startswith('#'):
                if blast_line.startswith('# Query:'):
                    contig_len = blast_line.split()[-1][4:]
            else:
                items = blast_line.split()
                items[2] = float(items[2])
                items[3] = float(items[3])
                if items[2] >= 90:
                    ref_list.append([items[1].split('.')[0], items[2], items[3]])
        


        family_sheet = xlrd.open_workbook(os.path.dirname(os.path.realpath(__file__))+'/configurations/sequences.xlsx').sheet_by_name('Sheet1')

        for nrow in range(family_sheet.nrows):
            for ref_item in ref_list:
                if family_sheet.cell_value(nrow, 0) in ref_item:
                    ref_item.append(family_sheet.cell_value(nrow, 3))
        
        family_weight_dict = {}

        for genome_item in ref_list:
            if len(genome_item) < 4:
                continue
            if not family_weight_dict.__contains__(genome_item[3]):
                family_weight_dict[genome_item[3]] = genome_item[1] * genome_item[2]
            else:
                family_weight_dict[genome_item[3]] += genome_item[1] * genome_item[2]

        map_identification_list = []
        for key in family_weight_dict:
            # map_identification_list.append([key, family_weight_dict[key][0] / family_weight_dict[key][1]])
            map_identification_list.append([key, family_weight_dict[key]])

        sorted(map_identification_list, key=lambda x:x[1])
        print(map_identification_list)
        return map_identification_list[0][0]
