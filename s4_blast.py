#!/usr/bin/python3
#=================================================  module import==================================================
import os
import subprocess
import shutil
import sys
import time

#=================================================function define==================================================
# to use linux commands in python
def linux_commands( str ):
    result = subprocess.run(str, shell = True,capture_output = True,text = True)
    return result.stdout ,result.stderr
# check/make/clear output_directory
def check_output_directory( outfolder ):
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    else :
        shutil.rmtree(outfolder)
        os.makedirs(outfolder)
# write data to file
def writefile(data, filename):
    with open(filename, 'w') as file:
        file.write(data)
# handle the usr's input (used in menu choices 2)
def process_input(input_text):
    lines = input_text.strip().split()
    return '\n'.join(lines)
# handle duplicate_ids (used in menu choices 1)
def remove_duplicate_ids(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    processing = False
    ncbi_ids = set()
    processed_lines = []

    for line in lines:
        if line.startswith('@'):#start to collect data
            processing = True
            processed_lines.append(line)
            continue

        if processing:
            ncbi_ids.add(line.strip())
        else:
            processed_lines.append(line)

    # add all id in to the file again
    for id in ncbi_ids:
        processed_lines.append(id + '\n')

    with open(filepath, 'w') as file:
        file.writelines(processed_lines)
# make a blast list (menu choices 1)
def make_blast_list():
    # Make the blast list
    while True:
        # make the filename
        outfolder = "s4_out"
        filename = f'{outfolder}/seqBLAST_pre.txt'

        # write the first two line
        header = 'BLASTseqs'.center(100)
        separator = 'Quene line'.center(100,"@")
        content = f"{header}\n{separator}\n"

        # Handle autoscreen.txt 
        print("AutoScreen".center(100,"="))
        print("Results".center(100))
        print()   
        with open('s3_out/autoscreen.txt', 'r') as file:
            print(file.read()) 
        flag_autoscreen = input("Do you use the ID in 'autoscreen.txt'in BLAST?(y/n): ").lower()
        if flag_autoscreen == "y":
            if os.path.exists('s3_out/autoscreen.txt'):
                with open('s3_out/autoscreen.txt', 'r') as file:
                    content += process_input(file.read()) + '\n'
            else:
                print("CAN'T FOUND autoscreen FILE!")

        # Handle the usrs input
        if input("Do you want to input some ID to BLAST BY YOURSELF (y/n): ").lower() == 'y':
            while True:
                print("\n\n")
                print("-".center(100,"-"))
                print("PLEASE PASTE(press Ctrl+D when finished):\n")
                user_input = sys.stdin.read()
                print()
                print("YOUR INPUT".center(100,"-"))
                print()
                print(process_input(user_input))
                print("-".center(100,"-"))
                print()
                if input("Do you want to input again?(y/n): ").lower() != 'y':
                    content += process_input(user_input) + '\n'
                    break
        writefile(content, filename)
        print("Current BLAST quene line".center(100,"-"))
        print("\n\n")
        with open(filename,"r") as file:
            print(file.read())
        print()
        print("-".center(100,"-"))
        print("\n\n")
        if input("Do you want to SAVE data?(y/n): ").lower() == 'y':
            print(f"Data have been saved".center(100,"="))
            break

#=====================================================main body==================================================

# make sure there is a folder
outfolder = "s4_out"
if not os.path.exists(outfolder):
        os.makedirs(outfolder)

# run blast menu








