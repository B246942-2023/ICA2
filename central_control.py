#!/usr/bin/python3
#===================================================module import==================================================
import os
import subprocess
import shutil
#=================================================function define==================================================
# check/make/clear output_directory
def check_output_directory( outfolder ):
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    else :
        shutil.rmtree(outfolder)
        os.makedirs(outfolder)

# only make ,don't clear
def make_dir(outfolder):
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)



#=====================================================main body==================================================
#1 make all the dir
make_dir("s1_out")
make_dir("s2_out")
make_dir("s3_out")
make_dir("s4_out")
    #track the search and fetch
if os.path.exists("s1_out"):
    for file in os.listdir("s1_out"):
        if file.endswith('.fasta'):
            flag_search_fecth_done = True
           
while True:
    #status check : many steps can only work when the search and fecth fasta have done
    print("track")

    # menu content
    print("MENU".center(100,"="))
    print("Central Control".center(100))
    print()
    print()
    print()
    print(f'''    1.Search and Fetch 
    2.Analysis the Conservation
    3.Scan the Motifs
    4.BlAST
    5.Collate results
    6.Export data
    7.Reset
    8.Auto Mode
    9.Quit''')
    print()
    print()
    print()
    print()
    print("=".center(100,"="))

    # handle input 
    central_choices = input("Input your choices : ")
    if central_choices == "1":
        subprocess.run(["python3","s1_gainseq.py"]) # "python3" here is as same as the shebang line in the script 
    if central_choices == "2":
        if flag_search_fecth_done:
            subprocess.run(["python3","s2_conservation.py"]) 
        else :
            print("IMPORTANT:No data, Do '1.Search and Fetch' ".center(100))
    if central_choices == "3":
        if flag_search_fecth_done:
            subprocess.run(["python3","s3_motifs.py"])
        else :
            print("IMPORTANT:No data, Do '1.Search and Fetch' ".center(100))
    if central_choices == "4":
        if flag_search_fecth_done:
            subprocess.run(["python3","s4_blast.py"])
        else :
            print("IMPORTANT:No data, Do '1.Search and Fetch' ".center(100))
    if central_choices == "5":#collate_data
        if flag_search_fecth_done:
            print("collate_data()")

        else :
            print("IMPORTANT:No data, Do '1.Search and Fetch' ".center(100))
    if central_choices == "6":#export_data
        if flag_search_fecth_done:
            print("export_data()")
        else :
            print("IMPORTANT:No data, Do '1.Search and Fetch' ".center(100))
    if central_choices == "7":#reset
        print("reset()")

    if central_choices == "8":
        print("auto")

    if central_choices == "9":
        break
    if central_choices not in "1%2^3(4!5@6+7#8*9":# if just 123456789 when input 12, it will not be handled
        print("Wrong Input")
    input("Press Enter to back the MENU".center(100,"-"))


