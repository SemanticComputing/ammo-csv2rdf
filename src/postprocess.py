#!/usr/bin/env python3
#  -*- coding: UTF-8 -*-
"""Postprocess coo1980.ttl"""
import argparse
import logging

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import SKOS, RDF, Namespace
from rdflib.util import guess_format

log = logging.getLogger(__name__)


def add_coo1980_altlabels(g: Graph):
    for coo in g.subjects(RDF.type, SKOS.Concept):
        local_id = str(coo).split('#')[-1]

        if local_id == '6_7':
            local_id = '6/7'

        g.add((coo, SKOS.altLabel, Literal(local_id)))

        log.debug('Annotating altLabel %s to URI %s' % (local_id, coo))

    return g


def remove_empty_literals(g: Graph, prop: URIRef):
    for resource, value in list(g.subject_objects(prop)):
        if str(value) == '':
            g.remove((resource, prop, value))
            log.debug('Removing empty literal for %s  %s' % (resource, prop))

    return g


def main():
    argparser = argparse.ArgumentParser(description=__doc__, fromfile_prefix_chars='@')

    argparser.add_argument("task", help="Task to perform", choices=['add_altlabels', 'remove_empty_literals'],)
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

    if args.task == 'add_altlabels':
        print('Adding altLabels to COO1980')
        g = add_coo1980_altlabels(g)

    elif args.task == 'remove_empty_literals':
        print('Removing empty altLabels')
        g = remove_empty_literals(g, SKOS.altLabel)

    g.bind('skos', SKOS)
    g.serialize(args.output, format=guess_format(args.output))


if __name__ == '__main__':
    main()
