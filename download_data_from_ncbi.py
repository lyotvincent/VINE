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

def get_bacterias_path():
    bacteria_menu = []
    ftp = FTP("130.14.250.12")
    ftp.encoding = 'utf-8'
    ftp.login("anonymous", "3066268521@qq.com")
    ftp.getwelcome()
    output = open('./ncbi_bacteria_menu/bacteria_menu.txt', 'w')
    
    ftp.cwd("/genomes/genbank/bacteria/")
    ftp.retrlines('LIST', lambda line: bacteria_menu.append(line))
    for j in bacteria_menu:
        # print(j)
         output.write((j.split())[-1]+'\n')

    output.close()
    print("quit")
    ftp.quit()

def get_all_assembly_path():
    bacterias = []
    bacterias_txt = open('./ncbi_bacteria_menu/bacteria_menu.txt', 'r')
    for line in bacterias_txt.readlines():
        bacterias.append(line[:-1])
    bacterias_txt.close()
    ftp = FTP("130.14.250.12")
    ftp.encoding = 'utf-8'
    ftp.login("anonymous", "3066268521@qq.com")
    ftp.getwelcome()
    
    # assembly = []
    # ftp.cwd("/genomes/genbank/bacteria/Acetobacter_tropicalis/all_assembly_versions/")
    # ftp.retrlines('LIST', lambda line: assembly.append(line))
    # for i in assembly:
    #     print(i)

    for bacteria in bacterias:
        assembly = []
        if os.path.exists('./ncbi_bacteria_menu/'+bacteria+'.txt'):
            continue
        try:
            print("open  "+bacteria)
            output = open('./ncbi_bacteria_menu/'+bacteria+'.txt', 'w')
            ftp.cwd("/genomes/genbank/bacteria/"+bacteria+"/all_assembly_versions/")
            ftp.retrlines('LIST', lambda line: assembly.append(line))
            print("write "+bacteria)
            for j in assembly:
                output.write((j.split())[-3]+'\n')
        except Exception as e:
            print(e)
            break
        finally:
            output.close()

    print("quit")
    ftp.quit()

def turn_ftpdirpaths_to_json():
    ftpdirpaths = open('ftpdirpaths', "r")
    lines = ftpdirpaths.readlines()
    ftpdirpaths.close()

    json_menu = {}

    for l in lines:
        if os.path.exists('./bacteria/'+l.split('/')[-1][:-1]+'_genomic.fna.gz'):
            json_menu[l[:-1]] = 1
        else:
            json_menu[l[:-1]] = 0
    with open('./bacteria_json_menu.json', 'w') as f:
        json.dump(json_menu, f)
        print('turn over')

def download_bacteria_latest_fna():
    with open('./bacteria_json_menu.json', 'r') as load_f:
        load_dict = json.load(load_f)
    socket.setdefaulttimeout(30)
    ftp = FTP("130.14.250.12")
    ftp.encoding = 'utf-8'
    ftp.login("anonymous", "3066268521@qq.com")
    ftp.getwelcome()

    # while len([name for name in os.listdir('./bacteria')]) < 14130:
    for key in load_dict:
        # file not download = 0, already download = 1, file not exists in ftp = 2
        if load_dict[key] == 0 or load_dict[key] == 2:
            file_name = key.split('/')[-1]+'_genomic.fna.gz'
            path = key[26:]
            # print(path)
            print(time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime())+' downloading '+path+'//'+file_name)
            try:
                ftp.cwd(path)
                ftp.retrbinary('RETR %s' % file_name, open('./bacteria/'+file_name, 'wb').write)
                load_dict[key] = 1
            except Exception as e:
                print(str(e))
                if 'No such file or directory' in str(e):
                    load_dict[key] = 2
                if 'Broken pipe' in str(e):
                    ftp.quit()
                    break
            finally:
                with open('./bacteria_json_menu.json', 'w') as f:
                    json.dump(load_dict, f)

    print("quit")
    ftp.quit()

if __name__ == "__main__":
    download_bacteria_latest_fna()
    # turn_ftpdirpaths_to_json()
