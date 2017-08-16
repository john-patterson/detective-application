import argparse
import os
import json
from suplariapp.core import merge_testimonies

# Setting up argument parser
parser = argparse.ArgumentParser(description='Run the Suplari Detective algorithm.')
parser.add_argument('input_files',
                    help='Valid JSON testimony file.',
                    nargs='+')
parser.add_argument('-o', '--output',
                    help='Existing directory to write output to. Defaults to input directory.',
                    default=None)
parser.add_argument('-p', '--pretty',
                    help='Turns on indention in output file.',
                    action='store_true')
args = parser.parse_args()

def get_output_dir(input_file):
    if args.output:
        return args.output
    return os.path.dirname(os.path.realpath(input_file))

# Call the underlying implementation
def run(input_path, output_path, pretty_print=False):
    with open(input_path) as json_data:
        testimonies = json.load(json_data)
        merged_testimonies = merge_testimonies(testimonies)
        with open(output_path, 'w') as output_file:
            kwargs = {'indent': 4} if pretty_print else {}
            json.dump(merged_testimonies, output_file, **kwargs)


# Inject everything into run
def main():
    for input_file in args.input_files:
        file_path = os.path.realpath(input_file)
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = get_output_dir(input_file)
        output_path = os.path.join(output_dir,
                                   '{}_out.json'.format(file_name))
        run(file_path, output_path, pretty_print=args.pretty)

if __name__ == '__main__':
    main()
