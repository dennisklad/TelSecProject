import os, subprocess
from shutil import copy

import pathdir


os.chdir(pathdir.BASEDIR_PATH)

#Create new directory and paste the file for every YAML specification
def create_dir():
    for filename in os.listdir(pathdir.YAML_PATH):
        dir = filename.rstrip('.yaml')
        subprocess.run(["mkdir", dir], shell=True, stdout=f, text=True)    
        copy(pathdir.YAML_PATH + filename, pathdir.BASEDIR_PATH + dir)


#------------
#STEP 1. COMPILE

#Change into every created directory and compile with RESTler
def compile_dir():
    for dirname in os.listdir(pathdir.BASEDIR_PATH):
        
        if os.path.isdir(dirname):
            #Error Catching (e.g. PathNotFound)
            try:
                os.chdir(pathdir.BASEDIR_PATH + dirname)
                dir = os.getcwd()
                compile_restler(dir)
            finally:
                os.chdir(pathdir.BASEDIR_PATH)
        

#Run compile command from RESTler to create the grammar
def compile_restler(dir):
    for yamlfile in os.listdir(dir):
        if yamlfile.endswith(".yaml"):
            print("Compiling dir: "+ dir)
            subprocess.run([pathdir.RESTLER_PATH, "compile", "--api_spec", pathdir.YAML_PATH + yamlfile], shell=True, stdout=f, text=True)    
        else:
            print("ERROR: Compiling in " + dir)   


#------------
#STEP 2. TEST

#Specification coverage with the default RESTler grammar
def test_dir():
    for dirname in os.listdir(pathdir.BASEDIR_PATH):
        
        if os.path.isdir(dirname):
            #Error Catching (e.g. PathNotFound)
            try:
                os.chdir(pathdir.BASEDIR_PATH + dirname + "/Compile")
                dir = os.getcwd()
                #Check if compilation worked as planned and created grammar.py
                if os.path.isfile("grammar.py") and os.path.isfile("dict.json") and  os.path.isfile("engine_settings.json"):
                    test_restler(dir)
                else:
                    print ("ERROR: Testing in " + dir)
            finally:
                os.chdir(pathdir.BASEDIR_PATH)

#Run the RESTler command that created the dir TEST with the file main.txt
def test_restler(dir):
    #Get out of the Compile directory
    dirout = dir.rstrip("Compile")
    print(dirout)
    os.chdir(dirout)
    print("Testing dir: " + dirout)
    subprocess.run([pathdir.RESTLER_PATH, "test", 
        "--grammar_file", dir + "/grammar.py", 
        "--dictionary_file", dir + "/dict.json",
        "--settings", dir + "/engine_settings.json",
        "--no_ssl"], shell=True, stdout=f, text=True)    



#------------
#STEP 3. FUZZ-LEAN

#
def fuzz_lean_dir():
    for dirname in os.listdir(pathdir.BASEDIR_PATH):
        
        if os.path.isdir(dirname):
            #Error Catching (e.g. PathNotFound)
            try:
                os.chdir(BASEDIR_PATH + dirname + "/Compile")
                dir = os.getcwd()
                #Check if compilation worked as planned and created grammar.py
                if os.path.isfile("grammar.py") and os.path.isfile("dict.json") and  os.path.isfile("engine_settings.json"):
                    fuzz_lean_restler(dir)
                else:
                    print ("ERROR: Fuzz-lean in " + dir)
            finally:
                os.chdir(pathdir.BASEDIR_PATH)


#Run the RESTler command that created the dir TEST with the file main.txt
def fuzz_lean_restler(dir):
    #Get out of the Compile directory
    dirout = dir.rstrip("Compile")
    print(dirout)
    os.chdir(dirout)
    print("Fuzz-leaning dir: " + dirout)
    subprocess.run([pathdir.RESTLER_PATH, "fuzz-lean", 
        "--grammar_file", dir + "/grammar.py", 
        "--dictionary_file", dir + "/dict.json",
        "--settings", dir + "/engine_settings.json",
        "--no_ssl"], shell=True, stdout=f, text=True)    



#------------
#STEP 4. FUZZ

#
def fuzz_dir():
    for dirname in os.listdir(pathdir.BASEDIR_PATH):
        
        if os.path.isdir(dirname):
            #Error Catching (e.g. PathNotFound)
            try:
                os.chdir(pathdir.BASEDIR_PATH + dirname + "/Compile")
                dir = os.getcwd()
                #Check if compilation worked as planned and created grammar.py
                if os.path.isfile("grammar.py") and os.path.isfile("dict.json") and  os.path.isfile("engine_settings.json"):
                    fuzz_lean_restler(dir)
                else:
                    print ("ERROR: Fuzzing in " + dir)
            finally:
                os.chdir(pathdir.BASEDIR_PATH)


#Run the RESTler command that created the dir TEST with the file main.txt
def fuzz_restler(dir):
    #Get out of the Compile directory
    dirout = dir.rstrip("Compile")
    print(dirout)
    os.chdir(dirout)
    print("Fuzzing dir: " + dirout)
    subprocess.run([pathdir.RESTLER_PATH, "fuzz", 
        "--grammar_file", dir + "/grammar.py", 
        "--dictionary_file", dir + "/dict.json",
        "--settings", dir + "/engine_settings.json",
        "--no_ssl",
        "--time_budget", "1"], shell=True, stdout=f, text=True)    




#------------
#MAIN

with open('log.txt', 'w') as f:

    #subprocess.run(["dir"], shell=True, stdout=f, text=True)    

    #create_dir()

    #compile_dir()
    
    #test_dir()

    fuzz_lean_dir()

    fuzz_dir()

    print("Completed.")

f.close()
