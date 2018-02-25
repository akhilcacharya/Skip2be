#!/usr/bin/env python3
import os
from sys import argv


# Script to aggregate and convert the TSV to a fasttext input file
line_template = "%s\t%s\t%s"

output_path = "../data/svm/"
output_file_name = "dataset.full.txt"


def dump_chunk(output_file, chunk, max_time):
    if len(chunk.split("\t")) == 2:
        time, text_and_label = chunk.split("\t")
        comps = text_and_label.split(" ")
        chunk_text = " ".join(comps[:-1])
        label = comps[-1].rstrip()
        line = line_template % (label, chunk_text, float(time)/max_time)
        print(line, file=output_file)

def get_max_time(f):
    m = 0
    for l in f.readlines():
        if len(l.split("\t")) == 2:
            time, _ = l.rstrip().split("\t")
            if int(time) > m:
                m = int(time)
    return m



def convert(folder): 
    print("Converting to svm format")

    if not os.path.exists(output_path): 
        os.mkdir(output_path)

    output_file = open(os.path.join(output_path, output_file_name), "w")

    for _file in os.listdir(folder): 
        if _file.startswith("."): 
            continue 

        with open(os.path.join(folder, _file)) as text_file: 
            max_time = get_max_time(text_file)
        

        with open(os.path.join(folder, _file)) as text_file: 
            for chunk in text_file.readlines(): 
                dump_chunk(output_file, chunk, max_time)

    output_file.close()
    print("Finished converting; dumped to", output_path)

def split(): 
    print("Splitting data by 70-15-15")
    with open(os.path.join(output_path, output_file_name)) as dataset_file: 
        lines = list(dataset_file.readlines()) 

        size = len(lines)

        train_size = int(size * 0.7)
        valid_size = train_size + int(size * 0.15)
        test_size = valid_size + int(size * 0.15)

        with open(os.path.join(output_path, "dataset.train"), "w") as output_file: 
            output_file.writelines(lines[0:train_size])

        with open(os.path.join(output_path, "dataset.valid"), "w") as output_file: 
            output_file.writelines(lines[train_size:valid_size])
        
        with open(os.path.join(output_path, "dataset.test"), "w") as output_file: 
            output_file.writelines(lines[valid_size:test_size])

    print("Finished splitting data")

def main(args): 
    if len(args) != 1: 
        print("Usage: ./convert_svm.py [training_data_folder]")
        sys.exit(1)

    folder = args[0]

    convert(folder)
    split()



if __name__ == "__main__": 
    main(argv[1:])
