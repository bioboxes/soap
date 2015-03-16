__author__ = 'pbelmann'

import argparse
import yaml
import gzip
import os
import sys

TYPE_KEY = "type"
ARGUMENTS_KEY = "arguments"
FRAGMENT_SIZE_KEY = "fragment_size"
FASTQ_KEY = "fastq"
PATH_KEY = "path"
VALUE_KEY = "value"
ID_KEY = "id"
LIB_KEY = "lib"

class Assembler:
    def __init__(self, **entries):

        #soap needs fragment_sizes
        if(not entries[ARGUMENTS_KEY].has_key(FRAGMENT_SIZE_KEY)):
            sys.exit("soap needs fragment size")

        if(len(entries[ARGUMENTS_KEY][FRAGMENT_SIZE_KEY]) != len(entries[ARGUMENTS_KEY][FASTQ_KEY])):
            sys.exit("soap needs fragment size parameter for every fastq library")

        self.__dict__[LIB_KEY] = dict()
        #restructure the data
        for fastq in entries[ARGUMENTS_KEY][FASTQ_KEY]:
            gzipped = gzip.open(fastq[PATH_KEY], 'rb')
            gzipped_content = gzipped.read()
            fastq_path = '/tmp/' + fastq[ID_KEY]
            with open(fastq_path, 'w+') as extracted:
                extracted.write(gzipped_content)
            gzipped.close()
            self.__dict__[LIB_KEY][fastq[ID_KEY]] = dict(path=fastq_path, type=fastq[TYPE_KEY])


        for fragment_size in entries[ARGUMENTS_KEY][FRAGMENT_SIZE_KEY]:
            self.__dict__[LIB_KEY][fragment_size[ID_KEY]][FRAGMENT_SIZE_KEY] = fragment_size[VALUE_KEY]

def write_config(assembler):
    path_to_conf = '/tmp/soap.config'
    conf = open(path_to_conf, 'w+')
    for lib_id in  assembler.lib.keys():
       conf.write("[LIB]\n")
       conf.write("avg_ins="+str(assembler.lib[lib_id][FRAGMENT_SIZE_KEY])+"\n")

       type = ""
       if(assembler.lib[lib_id][TYPE_KEY] == "paired"):
            type = "p="
       elif(assembler.lib[lib_id][TYPE_KEY] == "single"):
            type = "q="
       conf.write(type + str(assembler.lib[lib_id][PATH_KEY])+"\n")
    conf.close()
    return path_to_conf

if __name__ == "__main__":
    #Parse arguments
    parser = argparse.ArgumentParser(description='Parses input yaml')
    parser.add_argument('-i', '--input_yaml', dest='i', nargs=1,
                        help='YAML input file')
    parser.add_argument('-o', '--output_path', dest='o', nargs=1,
                    help='Output path')
    args = parser.parse_args()

    #get input files
    input_yaml_path = ""
    output_path = ""
    if hasattr(args, 'i'):
        input_yaml_path = args.i[0]
    if hasattr(args, 'o'):
        output_path = args.o[0]

    #serialize yaml with python object
    f = open(input_yaml_path)
    assembler = Assembler(**yaml.safe_load(f))
    f.close()

    path = write_config(assembler)

    with open(path, 'r') as fin:
        print(fin.read())

    #run ray
    soap_out = output_path + "/soap"

    if not os.path.exists(soap_out):
        os.makedirs(soap_out)
    os.chdir(soap_out)

    bin = "soapdenovo2-63mer "
    conf = " all -K 31 -p 80 -s " + path
    output = " -o " + "soap"
    command = bin + conf + output
    exit = os.system(command)
    if(exit==0):
        out_dir = output_path + "/bbx"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        yaml_output = out_dir + "/out.yaml"
        output_data = {'version': '0.9.0', 'arguments': [{ "value": "soap/soap.contig" , "type" : "fasta"}]}
        stream = open(yaml_output, 'w')
        yaml.dump(output_data,default_flow_style=False,stream=stream)