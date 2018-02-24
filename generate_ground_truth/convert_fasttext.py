#!/usr/bin/env python3
import os
from sys import argv


# Script to aggregate and convert the TSV to a fasttext input file
line_template = "__label__%s %s"

output_path = "../data/fasttext/"
output_file_name = "dataset.full.txt"


def dump_chunk(output_file, chunk):
    _, text_and_label = chunk.split("\t")
    comps = text_and_label.split(" ")
    chunk_text = " ".join(comps[:-1])
    label = comps[-1].replace("\n", "")
    line = line_template % (label, chunk_text)
    print(line, file=output_file)


def main(args): 
    if len(args) != 1: 
        print("Usage: ./convert_fasttext.py [training_data_folder]")
        sys.exit(1)

    folder = args[0]

    print("Converting to fastText format")

    if not os.path.exists(output_path): 
        os.mkdir(output_path)

    output_file = open(os.path.join(output_path, output_file_name), "w")

    for _file in os.listdir(folder): 
        if _file.startswith("."): 
            continue 

        with open(os.path.join(folder, _file)) as text_file: 
            for chunk in text_file.readlines(): 
                dump_chunk(output_file, chunk)

    output_file.close()
    print("Finished converting; dumped to", output_path)


if __name__ == "__main__": 
    main(argv[1:])
