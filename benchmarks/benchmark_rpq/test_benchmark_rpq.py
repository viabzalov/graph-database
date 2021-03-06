import csv
import os
import time

import pytest
from conftest import params
from pygraphblas import *

from src.RegularPathQuering import rpq


@pytest.mark.parametrize('impl,graph,regex', params)
def test_benchmark_rpq(impl, graph, regex):
    impl_name = impl['name']

    g = impl['impl'].from_txt(graph['graph'])
    g_name = graph['name']

    r = impl['impl'].from_regex(regex['regex'])
    r_name = regex['name']

    result_file = f'{g_name}.csv'
    result_file_path = f'./benchmarks/benchmark_rpq/results/{result_file}'

    headers = [
        'Implementation'
        , 'Graph'
        , 'Regex'
        , 'Time (in microseconds)'
        , 'Control sum'
    ]

    if not os.path.exists(result_file_path):
        with open(result_file_path, mode='w+', newline='\n') as f:
            csv_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, escapechar=' ')
            csv_writer.writerow(headers)

    with open(result_file_path, mode='a+', newline='\n', buffering=1) as f:
        csv_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, escapechar=' ')

        start_time = time.time_ns()
        res = rpq(g, r)
        end_time = time.time_ns()

        result_time = (end_time - start_time) // (10 ** 3)

        results = [impl_name, g_name, r_name, result_time, res.select(lib.GxB_NONZERO).nvals]

        csv_writer.writerow(results)
