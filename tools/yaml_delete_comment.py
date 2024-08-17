import argparse
import yaml
import os


# Create the parser
parser = argparse.ArgumentParser(description='Process a delete comment from input YAML file and return new file.')

## https://docs.python.org/ko/3/library/argparse.html
# Add the arguments
parser.add_argument('-i', '--inputfilepath', metavar='input-filepath', type=str, help='the path of the YAML file to process', required=True)
parser.add_argument('-o', '--outputfilepath', metavar='output-filepath', type=str, help='the path of the output YAML file', required=True)
parser.add_argument('-r', '--rootpath', metavar='root-path', type=str, help='the root path to prepend to file paths', default='')

# Parse the arguments
args = parser.parse_args()

# Check if a root path is provided
if args.rootpath:
    # Prepend the root path to the file paths
    root_path = os.path.realpath(args.rootpath)
    input_file_path = os.path.join(root_path, args.inputfilepath)
    output_file_path = os.path.join(root_path, args.outputfilepath)

    print('rootpath:', root_path)
else:
    # Convert the file paths to their canonical forms
    input_file_path = os.path.realpath(args.inputfilepath)
    output_file_path = os.path.realpath(args.outputfilepath)

# Print the file paths
print('Input file path:', input_file_path)
print('Output file path:', output_file_path)

# Read the YAML file
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

# Write the data to a new file, excluding comments
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write("## this file was auto generated file by ./util/yaml_delete_comment.py, DO NOT EDIT!\n")
    yaml.dump(data, file)
