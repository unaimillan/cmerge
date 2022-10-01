import os
import argparse
import re
import sys


def parse_includes(filename: str) -> dict[int, str]:
    """
    Parse the ``#include`` from the main file and return dict with line number
    and corresponding filename.
    :param filename: file to parse
    :return: dict with line number and corresponding filename to include
    """
    if not os.path.exists(filename):
        print('File "{}" does not exist.'.format(filename), file=sys.stderr)
        sys.exit(1)

    result = {}
    with open(filename, 'r') as f:
        for linen, line in enumerate(f, start=1):
            match = re.match(r'#include +[<"]([\w./]+)[>"]', line)
            if match is not None:
                result[linen] = match.group(1)
    return result


def find_files_to_include(include_filenames: list[str], dirs: list[str]) -> \
        dict[str, str]:
    """
    Search in the given folders for files to include and return dict
    with filename and corresponding content
    :param include_filenames:
    :param dirs:
    :return:
    """
    result = {}
    for filename in include_filenames:
        for cur_dir in dirs:
            full_path = os.path.join(cur_dir, filename)
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    result[filename] = f.read()
    return result


def write_merged_output(output_filename: str, main_file: str,
                        includes: dict[int, str],
                        files_to_include: dict[str, str]) -> None:
    """
    Merge everything to the output file
    :param output_filename:
    :param main_file:
    :param includes:
    :param files_to_include:
    """
    with open(output_filename, 'w') as f:
        with open(main_file, 'r') as main_f:
            for linen, line in enumerate(main_f, start=1):
                if linen in includes and includes[linen] in files_to_include:
                    f.write(files_to_include[includes[linen]])
                else:
                    f.write(line)


def main():
    parser = argparse.ArgumentParser(
        description='Merge several C files into one')
    parser.add_argument('-o', '--output', help='write the output to file',
                        default='solution.c')
    parser.add_argument('-d', '--dirs', help='directories to search for files',
                        nargs='+', default=['.'])
    parser.add_argument('file', help='main solution file', default='main.c')
    args = parser.parse_args()
    includes = parse_includes(args.file)
    files_to_include = find_files_to_include(list(includes.values()), args.dirs)
    write_merged_output(args.output, args.file, includes, files_to_include)


if __name__ == '__main__':
    main()
