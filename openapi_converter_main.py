# Filename is openapi_converter_main.py
# This file contains the main function to convert an OpenAPI 3.0 spec to 3.1

import argparse
import openapi_converter as converter 
import yaml
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file', nargs='?', default=None)
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file '{args.input_file}' does not exist.")

    with open(args.input_file, 'r') as f:
        openapi_dict = yaml.safe_load