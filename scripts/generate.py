import os
import sys
from generator.generation import generate_bulk


if __name__ == '__main__':
    for id in generate_bulk(1000):
        sys.stdout.write('%s\n' % id)
