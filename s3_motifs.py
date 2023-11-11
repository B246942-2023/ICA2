#!/usr/bin/python3
#===================================================module import==================================================
import os
import subprocess
import shutil
#=================================================function define==================================================
#run linux command in python
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
#=====================================================main body==================================================
print("START STEP3".center(100, '-'))
print(f'''STEP3:Scan the motifs''')
print("Scaning".center(100))
print()

#1 check and make directory
outfolder = "s3_out"
check_output_directory( outfolder )

#2 sperate the big fasta into small fasta files(each one contains only one seqences info)
#get the orignal fasta file path
folder_path = "s1_out"
filename_base = os.listdir(folder_path)[0].replace(".fasta","") # get the base filename for subsequent rename
file_path = f"{folder_path}/{filename_base}.fasta"

#read the file
with open(file_path, "r") as file:
    fasta_data = file.read()
#cat the whole orig_fasta file into many fasta files (each one only have one seqences info)
fasta_list = fasta_data.split(">")[1:] #the first element is " ",so remove 
for eachseq_str in fasta_list:
    lines_list = eachseq_str.strip().split('\n')  # split eachseq by "\n"
    seq_id = lines_list[0].split()[0] # just get the id
    seq_info = lines_list[0]  # the seq_id line is the first element in the list
    seq_data = '\n'.join(lines_list[1:])  # get the seq 
    with open(f"{outfolder}/{seq_id}.fasta", "w") as f:
            f.write(f">{seq_id}\n{seq_data}")

#3 send all the small fasta files into patmatmotifs
input_folder_path = "s3_out"
file_list = os.listdir(input_folder_path)
for file_path in file_list:
    patmatmotifs_inputpath = input_folder_path+"/"+file_path
    patmatmotifs_outputpath = input_folder_path+"/"+file_path.replace(".fasta","_motifs.txt")
    command_patmatmotifs = f"patmatmotifs -sequence {patmatmotifs_inputpath} -outfile {patmatmotifs_outputpath} -full "
    patmatdb_out,patmat_error = linux_commands(command_patmatmotifs)


#4 Analysis the motifs_data
motifs_counts = {}  # [motifname]: count
motifs_id = {}      # [motifname] : [id1,id2,id3....]
id_motifs={}        # [id] : [motif1,motif2,...]
id_Hitcount = {}    # [id]: motifs_counts
no_motifs_id = []   # [id of those have no motifs]
file_total = 0      # count the total file

for filename in os.listdir(input_folder_path):
    if filename.endswith('.txt'):  # all the txt files
        id = filename.replace("_motifs.txt","")# eg : id_motifs.txt
        file_total += 1
        motif_exist_flag = False
        with open(os.path.join(input_folder_path, filename), 'r') as file:
            for line in file:
                if 'HitCount' in line :
                    id_Hitcount[id] = line.split()[-1]
                if 'Motif' in line:  # find the Motif line
                    motif_exist_flag = True # flag on exist turn into True
                    motif = line.split()[-1]
                    #print(id)
                    #print(motif)
                    if motif in motifs_counts:
                        motifs_counts[motif] += 1
                        motifs_id[motif].append(id)
                    else :
                        motifs_counts[motif] = 1
                        motifs_id[motif] = [id]
        if motif_exist_flag == False:
            no_motifs_id.append(id)


