# -*- coding: utf-8 -*-
'''
Queries for experiments with ENDSEQ operator
'''

import os

from gen.directory import write_to_txt, get_env_file, get_query_dir, \
    get_out_file
from gen.experiment import SLI, RAN, ALGORITHM, CQL_ALG, ATT, \
    get_attribute_list
from gen.query.basic import get_register_stream, REG_Q_OUTPUT_STR, REG_Q_STR


# =============================================================================
# Query using ENDSEQ operator
# =============================================================================
ENDSEQ_QUERY = '''
SELECT SUBSEQUENCE END POSITION
FROM SEQUENCE IDENTIFIED BY a1
[RANGE {ran} SECOND, SLIDE {sli} SECOND] FROM s;
'''

# =============================================================================
# CQL Queries
# =============================================================================
# Query to get sequence from stream
CQL_Z = '''
SELECT SEQUENCE IDENTIFIED BY a1 [RANGE {ran} SECOND, SLIDE {sli} SECOND]
FROM s;
'''

# Query equivalent to ENDSEQ operator
CQL_EQUIV = '''
SELECT _pos - {ran} + 1 AS _pos, {att} FROM z WHERE _pos >= {ran}
'''


def gen_endseq_query(configuration, experiment_conf):
    '''
    Generate queries with ENDSEQ operator
    '''
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'endseq.cql'
    query = ENDSEQ_QUERY.format(ran=experiment_conf[RAN],
                                sli=experiment_conf[SLI])
    write_to_txt(filename, query)


def gen_cql_final_query(query_dir, experiment_conf):
    '''
    Generate final query equivalent to ENDSEQ operator
    '''
    filename = query_dir + os.sep + 'equiv.cql'
    if os.path.isfile(filename):
        return
    range_value = experiment_conf[RAN]
    att_list = get_attribute_list(experiment_conf[ATT])
    att_str = ', '.join(att_list)
    pos_query_list = []
    for position in range(1, range_value + 1):
        pos_query = CQL_EQUIV.format(att=att_str, ran=position)
        pos_query_list.append(pos_query)
    query = '\nUNION\n'.join(pos_query_list) + ';'
    out_file = open(filename, 'w')
    out_file.write(query)
    out_file.close()


def gen_cql_queries(configuration, experiment_conf):
    '''
    Generate all CQL queries equivalent to ENDSEQ operator
    '''
    query_dir = get_query_dir(configuration, experiment_conf)
    query = CQL_Z.format(ran=experiment_conf[RAN],
                         sli=experiment_conf[SLI])
    filename = query_dir + os.sep + 'z.cql'
    write_to_txt(filename, query)
    gen_cql_final_query(query_dir, experiment_conf)
#     filename = query_dir + os.sep + 'equiv.cql'
#     att_list = get_attribute_list(experiment_conf[ATT])
#     att_list = ', '.join(att_list)
#     query = CQL_EQUIV.format(att=att_list, ran=experiment_conf[RAN])
#     write_to_txt(filename, query)


def gen_all_queries(configuration, experiment_list):
    '''
    Generate all queries
    '''
    for exp_conf in experiment_list:
        if exp_conf[ALGORITHM] == CQL_ALG:
            gen_cql_queries(configuration, exp_conf)
        else:
            gen_endseq_query(configuration, exp_conf)


def gen_endseq_env(configuration, experiment_conf, output):
    '''
    Generate environment files for ENDSEQ operator
    '''
    text = get_register_stream(configuration, experiment_conf)
    # Get query filename
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'endseq.cql'
    # Register query
    if output:
        # Get output filename
        out_file = get_out_file(configuration, experiment_conf)
        text += REG_Q_OUTPUT_STR.format(qname='endseq', qfile=filename,
                                        ofile=out_file)
    else:
        text += REG_Q_STR.format(qname='endseq', qfile=filename)
    # Get environment filename
    filename = get_env_file(configuration, experiment_conf)
    write_to_txt(filename, text)


def gen_cql_env(configuration, experiment_conf, output):
    '''
    Generate environment files for StremPref
    '''
    text = get_register_stream(configuration, experiment_conf)
    query_dir = get_query_dir(configuration, experiment_conf)
    # Environment files for equivalent CQL queries
    filename = query_dir + os.sep + 'z.cql'
    text += REG_Q_STR.format(qname='z', qfile=filename)
    # Final equivalent query
    filename = query_dir + os.sep + 'equiv.cql'
    if output:
        # Get output filename
        out_file = get_out_file(configuration, experiment_conf)
        text += REG_Q_OUTPUT_STR.format(qname='equiv', qfile=filename,
                                        ofile=out_file)
    else:
        text += REG_Q_STR.format(qname='equiv', qfile=filename)
    filename = get_env_file(configuration, experiment_conf)
    write_to_txt(filename, text)


def gen_all_env(configuration, experiment_list, output=False):
    '''
    Generate all environment files
    '''
    for exp_conf in experiment_list:
        if exp_conf[ALGORITHM] == CQL_ALG:
            gen_cql_env(configuration, exp_conf, output)
        else:
            gen_endseq_env(configuration, exp_conf, output)
