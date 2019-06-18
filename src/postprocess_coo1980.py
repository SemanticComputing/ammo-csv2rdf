#!/usr/bin/env python3
#  -*- coding: UTF-8 -*-
"""Postprocess coo1980.ttl"""
import argparse
import logging

from rdflib import Graph, Literal
from rdflib.namespace import SKOS, RDF, Namespace
from rdflib.util import guess_format

log = logging.getLogger(__name__)


def add_alt_labels(g: Graph):
    for coo in g.subjects(RDF.type, SKOS.Concept):
        local_id = str(coo).split('#')[-1]

        if local_id == '6_7':
            local_id = '6/7'

        g.add((coo, SKOS.altLabel, Literal(local_id)))

        log.debug('Annotating altLabel %s to URI %s' % (local_id, coo))

    return g


def main():
    argparser = argparse.ArgumentParser(description=__doc__, fromfile_prefix_chars='@')

    argparser.add_argument("input", help="Input RDF file")
    argparser.add_argument("output", help="Output RDF file")
    argparser.add_argument("--loglevel", default='DEBUG', help="Logging level",
                           choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    argparser.add_argument("--logfile", default='tasks.log', help="Logfile")

    args = argparser.parse_args()

    log = logging.getLogger()  # Get root logger
    log_handler = logging.FileHandler(args.logfile)
    log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    log.addHandler(log_handler)
    log.setLevel(args.loglevel)

    g = Graph()
    g.parse(args.input, format=guess_format(args.input))

    g = add_alt_labels(g)

    g.serialize(args.output, format=guess_format(args.output))


if __name__ == '__main__':
    main()
