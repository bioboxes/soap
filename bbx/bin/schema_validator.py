__author__ = 'pbelmann'

import argparse
import yaml
import json
import sys
import os
from jsonschema import Draft4Validator
from jsonschema.exceptions import best_match

def validate_schema(input_yaml_path, schema_file):
    json_data_in = yaml.load(open(input_yaml_path))
    json_in = json.dumps(json_data_in)
    json_data_schema = json.load(open(schema_file))
    error = best_match(Draft4Validator(json_data_schema).iter_errors(json_data_in))
    if(error):
        sys.exit(error.message)

if __name__ == "__main__":
    #Parse arguments
    parser = argparse.ArgumentParser(description='Parses input yaml')
    parser.add_argument('-i', '--input_yaml', dest='i', nargs=1,
                        help='YAML input file')
    parser.add_argument('-s', '--schema_yaml', dest='s', nargs=1,
                        help='YAML schema file')
    args = parser.parse_args()

    #get input files
    input_yaml_path = ""
    schema_file = ""
    if hasattr(args, 'i'):
        input_yaml_path = args.i[0]
    if hasattr(args, 's'):
        schema_file = args.s[0]

    validate_schema(input_yaml_path,schema_file)