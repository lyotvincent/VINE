import xlrd
import identification
import os

class Tracer:
    
    def __init__(self, result_path, blastn_result):
        self.result_path = result_path + '/trace'
        # self.conf = conf
        self.blastn_result = blastn_result
    
    def run(self):
        print('start Tracer...')
        # TODO 在外面判断一下是否需要先blastn

        blastn_result_file = open(self.blastn_result, 'r')
        blastn_result_lines = blastn_result_file.readlines()
        blastn_result_file.close()
        
        sheet = xlrd.open_workbook(os.path.dirname(os.path.realpath(__file__))+'/configurations/trace.xlsx').sheet_by_index(0)

        os.mkdir(self.result_path)
        output = open(self.result_path + '/trace_result', 'w')
        for line in blastn_result_lines:
            if line.startswith('#'):
                output.write(line)
                continue
            else:
                line_items = line.strip().split()
                accession_version = line_items[1]
                for row_number in range(sheet.nrows):
                    row = sheet.row_values(row_number)
                    if row[0] == accession_version.split('.')[0]:
                        output.write('\t'.join(line_items+row[1:])+'\n')
        
        output.close()

        print('end Tracer...')


