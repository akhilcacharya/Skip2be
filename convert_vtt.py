#!/usr/bin/env python2
import sys
from os.path import abspath, exists
from datetime import datetime
import re

from pyvtt import WebVTTFile, WebVTTItem

def dump_chunk_timings(output_file, chunk_timings): 
    print >>output_file, "%d\t%s" % (chunk_timings[0], chunk_timings[1])

def dump_token_timings(output_file, token_timings): 
    print >>output_file, "%d\t%s" % (token_timings[0], token_timings[1])

def str_to_ms(time_str): 
    # Amazing hack! 
    epoch = datetime(1900, 1, 1)
    tm = datetime.strptime(time_str, '%H:%M:%S.%f')
    ms = (tm - epoch).total_seconds() * 1000 
    return ms

def fetch_chunk_time(line): 
    ms = str_to_ms(unicode(line.start))
    text = line.text_without_tags
    return (ms, text)

def fetch_word_time(line, before_delimiter='<', after_delimiter='>'):
    text = unicode(line)
    def _line_tag_cleaner(line):
        if (line.startswith(before_delimiter) and
            line.count(before_delimiter) == 1 and
                (line.count(after_delimiter) == 0 or
                    line.endswith(after_delimiter))):
            line = line[1:]
        if (line.endswith(after_delimiter) and
                line.count(after_delimiter) == 1 and
                line.count(before_delimiter) == 0):
            line = line[:-1]
        return line

    # Pre process line by line to avoid some ugly corner cases
    text = '\n'.join([_line_tag_cleaner(i) for i in text.split('\n')])
    regex_str = re.compile(r"{0}[^>]*?{1}".format(
        before_delimiter, after_delimiter))

    line_timings = regex_str.findall(text)

    # Filter out anything without a colon inside 
    # HACK
    line_timings = [timing.replace("<", "").replace(">", "") for timing in line_timings if ":" in timing]

    line_timings = [unicode(line.start)] + line_timings
    
    # Converto to MS
    line_timings = [str_to_ms(timing) for timing in line_timings]

    # Zip with the original words
    filtered_text = line.text_without_tags

    tokens = filtered_text.split(" ")

    token_timings = zip(line_timings, tokens)

    return token_timings


def parse(vtt_file): 

    name = vtt_file.split(".vtt")[0]
    
    vtt_lines = WebVTTFile.open(vtt_file)

    token_output = open("%s_token_output.tsv" % name, "w")
    chunk_output = open("%s_chunk_output.tsv" % name, "w")

    for line in vtt_lines:

        token_timings = fetch_word_time(line)

        chunk_timings = fetch_chunk_time(line)

        dump_chunk_timings(chunk_output, chunk_timings)

        for timing in token_timings: 
            dump_token_timings(token_output, timing)

    token_output.close() 
    chunk_output.close()


def main(args): 
    if len(args) != 1: 
        print "Usage: python convert_vtt.py file.vtt"
        sys.exit(1)
    vtt_file = args[0]
    parse(vtt_file)


if __name__ == "__main__": 
    main(sys.argv[1:])