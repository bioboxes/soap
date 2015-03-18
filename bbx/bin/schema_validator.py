__author__ = 'pbelmann'

import argparse
import yaml
import Rx

def validate_schema(input_yaml_path, schema_file):
    data = yaml.load(open(input_yaml_path))
    rx = Rx.Factory({ "register_core_types": True })
    schema = rx.make_schema(yaml.load(open(schema_file)))
    if not schema.check(data):
        raise ValueError("YAML is not in a valid format. Please check the definition on bioboxes.")

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