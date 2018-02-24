#!/usr/bin/env python3

import sys
import os
from fastText import train_supervised

def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

def main(args): 
    if len(args) != 2: 
        print("Usage: train.py [training set] [validation set]")
        sys.exit(1)

    train = args[0]
    valid = args[1]

    print("Starting training...")

    # train_supervised uses the same arguments and defaults as the fastText cli
    model = train_supervised(
        input=train, epoch=25, lr=1.0, wordNgrams=2, verbose=2, minCount=1
    )

    print("Finished training...")
    print_results(*model.test(valid))

    model.save_model("skip2be.bin")


if __name__ == "__main__":
    main(sys.argv[1:])