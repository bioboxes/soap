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
VALUE_KEY = "value"
ID_KEY = "id"
LIB_KEY = "lib"
BBX_INPUT_DIR = "/bbx/input"


class Assembler:
    def __init__(self, **entries):
        self.__dict__[LIB_KEY] = dict()
        # restructure the data
        fastq_exists = False
        fragment_size_exists = False
        fragment_size_length = 0
        fastq_length = 0
        for argument in entries[ARGUMENTS_KEY]:
            if argument.has_key(FASTQ_KEY):
                fastq_exists = True
                for fastq in argument[FASTQ_KEY]:
                    gzipped = gzip.open(BBX_INPUT_DIR + fastq[VALUE_KEY], 'rb')
                    gzipped_content = gzipped.read()
                    fastq_path = '/tmp/' + fastq[ID_KEY]
                    with open(fastq_path, 'w+') as extracted:
                        extracted.write(gzipped_content)
                    gzipped.close()
                    self.__dict__[LIB_KEY][fastq[ID_KEY]] = dict(value=fastq_path, type=fastq[TYPE_KEY])
            if argument.has_key(FRAGMENT_SIZE_KEY):
                fragment_size_exists = True
                for fragment_size in argument[FRAGMENT_SIZE_KEY]:
                    self.__dict__[LIB_KEY][fragment_size[ID_KEY]][FRAGMENT_SIZE_KEY] = fragment_size[VALUE_KEY]

        #soap needs fragment_sizes
        if (not fastq_exists):
            sys.exit("fastq has to be provided")

        if (not fragment_size_exists):
            sys.exit("soap needs fragment size")

        if (fastq_length != fragment_size_length):
            sys.exit("soap needs fragment size parameter for every fastq library")


def write_config(assembler):
    path_to_conf = '/tmp/soap.config'
    conf = open(path_to_conf, 'w+')
    for lib_id in assembler.lib.keys():
        conf.write("[LIB]\n")
        conf.write("avg_ins=" + str(assembler.lib[lib_id][FRAGMENT_SIZE_KEY]) + "\n")

        type = ""
        if (assembler.lib[lib_id][TYPE_KEY] == "paired"):
            type = "p="
        elif (assembler.lib[lib_id][TYPE_KEY] == "single"):
            type = "q="
        conf.write(type + str(assembler.lib[lib_id][VALUE_KEY]) + "\n")
    conf.close()
    return path_to_conf


if __name__ == "__main__":
    # Parse arguments
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
    if (exit == 0):
        out_dir = output_path + "/bbx"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        yaml_output = out_dir + "/biobox.yaml"
        output_data = {'version': '0.9.0', 'arguments': [{
                                                             'fasta': [{"value": "/soap/soap.contig", "type": "contig",
                                                                        "id": "1"},
                                                                       {"value": "/soap/soap.scaf", "type": "scaffold",
                                                                        "id" : "2"}]
                                                         }]}

        stream = open(yaml_output, 'w')
        yaml.dump(output_data, default_flow_style=False, stream=stream)