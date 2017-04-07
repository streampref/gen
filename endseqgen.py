#!/usr/bin/python -u
# -*- coding: utf-8 -*-
'''
Dataset generator for experiments with ENDSEQ operator
'''

from gen.directory import ENDSEQ_DIR_DICT, create_directories
from gen.experiment import ATT, VAR, DEF, NSQ, RAN, SLI, \
    PARAMETER, DIRECTORY, NAIVE_SUBSEQ, INC_SUBSEQ, \
    gen_experiment_list, ALGORITHM_LIST, CQL_ALG
from gen.run import run_experiments, summarize_all, confidence_interval_all
from gen.data import gen_all_streams
from gen.query.endseq import gen_all_queries, gen_all_env


# Parameters configuration
ENDSEQ_PAR = {
    # Attributes
    ATT: {
        VAR: [8, 10, 12, 14, 16],
        DEF: 10
        },
    # Sequences
    NSQ: {
        VAR: [4, 8, 16, 24, 32],
        DEF: 16
        },
    # Range
    RAN: {
        VAR: [10, 20, 40, 60, 80, 100],
        DEF: 40
        },
    # Slide
    SLI: {
        VAR: [1, 10, 20, 30, 40],
        DEF: 10
        },
    }

ENDSEQ_CONF = {
    # Algorithms
    ALGORITHM_LIST: [CQL_ALG, NAIVE_SUBSEQ, INC_SUBSEQ],
    # Directories
    DIRECTORY: ENDSEQ_DIR_DICT,
    # Parameters
    PARAMETER: ENDSEQ_PAR
    }

# Number of executions for experiments
RUN_COUNT = 2


def get_arguments(print_help=False):
    '''
    Get arguments
    '''
    import argparse
    parser = argparse.ArgumentParser('EndseqGen')
    parser.add_argument('-g', '--gen', action="store_true",
                        default=False,
                        help='Generate files')
    parser.add_argument('-o', '--output', action="store_true",
                        default=False,
                        help='Generate query output')
    parser.add_argument('-r', '--run', action="store_true",
                        default=False,
                        help='Run experiments')
    parser.add_argument('-s', '--summarize', action="store_true",
                        default=False,
                        help='Summarize results')
    args = parser.parse_args()
    if print_help:
        parser.print_help()
    return args


def main():
    '''
    Main routine
    '''
    args = get_arguments()
    exp_list = gen_experiment_list(ENDSEQ_CONF)
    if args.gen:
        create_directories(ENDSEQ_CONF, exp_list)
        print 'Generating stream data'
        gen_all_streams(ENDSEQ_CONF, exp_list)
        print 'Generating queries'
        gen_all_queries(ENDSEQ_CONF, exp_list)
        print 'Generating environments'
        gen_all_env(ENDSEQ_CONF, exp_list, output=args.output)
    elif args.run:
        print 'Running experiments'
        run_experiments(ENDSEQ_CONF, exp_list, RUN_COUNT)
    elif args.summarize:
        print 'Summarizing results'
        summarize_all(ENDSEQ_CONF, RUN_COUNT)
        print 'Calculating confidence intervals'
        confidence_interval_all(ENDSEQ_CONF)
    else:
        get_arguments(True)


if __name__ == '__main__':
    main()