"""
author: sun jialiang
environment: python3.6
how to run: 
"""

import os
import sys
import time
import subprocess
import json
from ftplib import FTP
import socket

def download_patric1():
    menu = []
    ftp = FTP("140.221.78.45")
    ftp.encoding = 'utf-8'
    ftp.login("anonymous", "3066268521@qq.com")
    ftp.cwd("genomes/100053.7/")
    print(ftp.getwelcome())
    fs = ftp.retrlines('LIST', lambda line: menu.append(line))
    print(fs)
    for i in range(len(menu)):
        menu[i] = (menu[i].split())[-1]
    print(menu)
    
    for i in menu:
        if str(i).endswith('.fna'):
            print(1)
            ftp.retrbinary('RETR %s' % i, open('./patric/'+i, 'wb').write)
    print("quit")
    ftp.quit()

def get_AMR_genome_sets_path():
    root_menu = ['Acinetobacter', 'Escherichia', 'Klebsiella', 'Mycobacterium', 'Neisseria', 'Peptoclostridium', 'Pseudomonas', 'Salmonella', 'Staphylococcus', 'Streptococcus']
    first_floor_menu = ['Acinetobacter/amikacin', 'Acinetobacter/carbapenem', 'Acinetobacter/imipenem', 'Escherichia/amoxicillin', 'Escherichia/ampicillin', 'Escherichia/cefotaxime', 'Escherichia/ceftazidime', 'Escherichia/cefuroxime', 'Escherichia/ciprofloxacin', 'Escherichia/gentamicin', 'Escherichia/piperacillin', 'Escherichia/trimethoprim', 'Klebsiella/amikacin', 'Klebsiella/amoxicillin', 'Klebsiella/aztreonam', 'Klebsiella/cefazolin', 'Klebsiella/cefepime', 'Klebsiella/cefoxitin', 'Klebsiella/ceftazidime', 'Klebsiella/ceftriaxone', 'Klebsiella/ciprofloxacin', 'Klebsiella/gentamicin', 'Klebsiella/imipenem', 'Klebsiella/levofloxacin', 'Klebsiella/meropenem', 'Klebsiella/piperacillin', 'Klebsiella/tetracycline', 'Klebsiella/tobramycin', 'Klebsiella/trimethoprim', 'Mycobacterium/amikacin', 'Mycobacterium/capreomycin', 'Mycobacterium/ethambutol', 'Mycobacterium/ethionamide', 'Mycobacterium/isoniazid', 'Mycobacterium/kanamycin', 'Mycobacterium/ofloxacin', 'Mycobacterium/pyrazinamide', 'Mycobacterium/rifampin', 'Mycobacterium/streptomycin', 'Neisseria/azithromycin', 'Peptoclostridium/azithromycin', 'Peptoclostridium/clarithromycin', 'Peptoclostridium/moxifloxacin', 'Pseudomonas/amikacin', 'Pseudomonas/levofloxacin', 'Pseudomonas/meropenem', 'Salmonella/chloramphenicol', 'Staphylococcus/ciprofloxacin', 'Staphylococcus/clindamycin', 'Staphylococcus/erythromycin', 'Staphylococcus/fusidic', 'Staphylococcus/gentamicin', 'Staphylococcus/methicillin', 'Staphylococcus/oxacillin', 'Staphylococcus/penicillin', 'Staphylococcus/tetracycline', 'Staphylococcus/trimethoprim', 'Streptococcus/chloramphenicol', 'Streptococcus/tetracycline', 'Streptococcus/trimethoprim']
    file_menu = {}
    ftp = FTP("140.221.78.45")
    ftp.encoding = 'utf-8'
    ftp.login("anonymous", "3066268521@qq.com")
    output = open('AMR_menu.txt', 'w')
    
    for i in first_floor_menu:
        try:
            ftp.cwd("/AMR_genome_sets/"+i+"/Resistant/")
            temp_menu = []
            ftp.retrlines('LIST', lambda line: temp_menu.append(line))
            for j in range(len(temp_menu)):
                temp_menu[j] = (temp_menu[j].split())[-1]
                if temp_menu[j].endswith('.fna'):
                    file_menu[temp_menu[j]] = "/AMR_genome_sets/"+i+"/Resistant/"
                    output.write(temp_menu[j]+"\n")
        except:
            print('except')

        try:
            ftp.cwd("/AMR_genome_sets/"+i+"/Susceptible/")
            temp_menu = []
            ftp.retrlines('LIST', lambda line: temp_menu.append(line))
            for j in range(len(temp_menu)):
                temp_menu[j] = (temp_menu[j].split())[-1]
                if temp_menu[j].endswith('.fna'):
                    file_menu[temp_menu[j]] = "/AMR_genome_sets/"+i+"/Susceptible/"
                    output.write(temp_menu[j]+"\n")
        except:
            print('except')

    # print(file_menu)

    print("quit")
    ftp.quit()

def download_patric2():
    menu1 = []
    menu2 = []
    ftp = FTP("140.221.78.45")
    ftp.encoding = 'utf-8'
    ftp.login("anonymous", "3066268521@qq.com")
    ftp.cwd("genomes")
    print(ftp.getwelcome())
    
    fs = ftp.retrlines('LIST', lambda line: menu1.append(line))
    print(fs)
    for i in range(len(menu1)):
        menu1[i] = (menu1[i].split())[-1]
    print(menu1)

    for m in menu1:
        ftp.cwd(m)
        ftp.retrlines('LIST', lambda line: menu2.append(line))
        for i in range(len(menu2)):
            if str(i).endswith('.fna'):
                ftp.retrbinary('RETR %s' % i, open('./', 'wb').write)

    print("quit")
    ftp.quit()

def download_patric3():
    ftp = FTP("140.221.78.45")
    ftp.encoding = 'utf-8'
    ftp.login("anonymous", "3066268521@qq.com")
    ftp.cwd("genomes/100053.7/")
    print(ftp.getwelcome())
    
    ftp.retrbinary('RETR %s' % '100053.7.fna', open('./patric/'+'100053.7.fna', 'wb').write)
    ftp.cwd("../100053.4/")
    print(ftp.getwelcome())
    ftp.retrbinary('RETR %s' % '100053.4.fna', open('./patric/'+'100053.4.fna', 'wb').write)
    print("quit")
    ftp.quit()

def find_first_not_exist():
    menu = open('./patric/menu.html', 'r')
    lines = menu.readlines()
    previous_file = ''
    for item in lines:
        if not os.path.exists('./patric/'+item[:-2]+'.fna'):
            return previous_file, item[:-2]+'.fna'
        else:
            previous_file = item[:-2]+'.fna'

def download_patric4():
    menu = open('./patric/menu.html', 'r')
    lines = menu.readlines()
    ftp = FTP("140.221.78.45")
    ftp.encoding = 'utf-8'
    ftp.login("anonymous", "3066268521@qq.com")
    print(ftp.getwelcome())
    print(lines[0][:-2])
    ftp.cwd("genomes/"+str(lines[0][:-2]))
    
    previous_file = ''
    now_file = ''
    should_download_file = ''
    while not os.path.exists('./patric/999898.3.fna'):
        # flag = 0
        i = 0
        previous_file, now_file = find_first_not_exist()
        if previous_file == '':
            should_download_file = now_file
        else:
            should_download_file = previous_file
        print("pre_file="+previous_file+' nowfile='+now_file+'\nshoulddownload='+should_download_file)
        line = lines[i]
        print('line='+line)
        while line:
            # print("judge "+line[:-2]+"==should_download_file "+should_download_file[:-4])
            if line[:-2] == should_download_file[:-4]:
                break
            i += 1
            line = lines[i]
        while line:
            print('downloading '+line[:-2])
            ftp.cwd("../"+line[:-2])
            try:
                ftp.retrbinary('RETR %s' % line[:-2]+'.fna', open('./patric/'+line[:-2]+'.fna', 'wb').write)
            except Exception as e:
                print(e)
            i += 1
            line = lines[i]

    menu.close()
    print("quit")
    ftp.quit()

def download_patric5():
    with open('./patric/download_record.json', 'r') as load_f:
        load_dict = json.load(load_f)
    socket.setdefaulttimeout(60)
    ftp = FTP("140.221.78.45")
    ftp.encoding = 'utf-8'
    ftp.login("anonymous", "3066268521@qq.com")
    print(ftp.getwelcome())
    print('100.9')
    ftp.cwd("genomes/100.9")
    
    while not os.path.exists('./patric/999898.3.fna'):
        for key in load_dict:
            # file not download = 0, already download = 1, file not exists in ftp = 2
            if load_dict[key] == 0 :
                print(time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime())+' downloading '+key+'.fna')
                ftp.cwd("../"+key)
                try:
                    ftp.retrbinary('RETR %s' % key+'.fna', open('./patric/'+key+'.fna', 'wb').write)
                    load_dict[key] = 1
                except Exception as e:
                    if 'No such file or directory' in str(e):
                        load_dict[key] = 2
                    # elif 'timed out' in str(e):
                    #     # ftp.quit()
                    #     ftp = FTP("140.221.78.45")
                    #     ftp.encoding = 'utf-8'
                    #     ftp.login("anonymous", "3066268521@qq.com")
                    #     print(ftp.getwelcome())
                    #     print('reconnect 100.9')
                    #     ftp.cwd("genomes/100.9")
                    print(str(e))
                finally:
                    with open('./patric/download_record.json', 'w') as f:
                        json.dump(load_dict, f)

    print("quit")
    ftp.quit()

def download_patric_AMR():
    with open('./patric_AMR/download_AMR_record.json', 'r') as load_f:
        load_dict = json.load(load_f)
    socket.setdefaulttimeout(30)
    ftp = FTP("140.221.78.45")
    ftp.encoding = 'utf-8'
    ftp.login("anonymous", "3066268521@qq.com")
    print(ftp.getwelcome())
    print('100.9')
    ftp.cwd("genomes/100.9")
    
    while 0 in load_dict.values():
        for key in load_dict:
            # file not download = 0, already download = 1, file not exists in ftp = 2
            if load_dict[key] == 0 :
                file_name = key.split('/')[-1]
                path = key[:-len(file_name)]
                # print(path)
                print(time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime())+' downloading '+key)
                ftp.cwd(path)
                try:
                    ftp.retrbinary('RETR %s' % key, open('./patric_AMR/'+file_name, 'wb').write)
                    load_dict[key] = 1
                except Exception as e:
                    if 'No such file or directory' in str(e):
                        load_dict[key] = 2
                    # elif 'timed out' in str(e):
                    #     # ftp.quit()
                    #     ftp = FTP("140.221.78.45")
                    #     ftp.encoding = 'utf-8'
                    #     ftp.login("anonymous", "3066268521@qq.com")
                    #     print(ftp.getwelcome())
                    #     print('reconnect 100.9')
                    #     ftp.cwd("genomes/100.9")
                    print(str(e))
                finally:
                    with open('./patric_AMR/download_AMR_record.json', 'w') as f:
                        json.dump(load_dict, f)

    print("quit")
    ftp.quit()

def read_patric_dir():
    index_of_genomes = open('Index_of_genomes.html', 'r')
    lines = index_of_genomes.readlines()
    new_file = open('tbody.html', 'w')
    for i in lines:
        if '<tbody id="tbody">' in i or '</tbody>' in i:
            new_file.write(i)

def split_tbody():
    tbody = open('tbody.html', 'r')
    lines = tbody.readlines()
    new_file = open('pretty_tbody.html', 'w')
    new_file.write(lines[0])
    new_lines = lines[1].split('</td>')
    for line in new_lines:
        if 'detailsColumn' not in line:
            new_file.write(line+'</td>\n')

def create_menu():
    tbody = open('pretty_tbody.html', 'r')
    lines = tbody.readlines()
    new_file = open('menu.html', 'w')
    for line in lines:
        line_list = line.split('"')
        for i in line_list:
            if 'value' not in i and '>' not in i and '<' not in i and '=' not in i and 'tbody' not in i and 'dir' not in i and 'f' not in i:
                new_file.write(i+'\n')

#
def downloadblastdb():

    i = 0
    while(os.path.exists('nt.70.tar.gz.md5') == False):
        i += 1
        print(i)
        try:
            subprocess.run('update_blastdb nt', shell=True, check=True)
        except:
            print('except')
    try:
        subprocess.run('update_blastdb nt', shell=True, check=True)
    except:
        print('except')

    print('starttime='+ time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime()))
    print('endtime='+time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime()))
    print("End")

if __name__ == "__main__":
    download_patric_AMR()
    # create_menu()
