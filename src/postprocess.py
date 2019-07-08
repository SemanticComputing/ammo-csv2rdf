#!/usr/bin/env python3
#  -*- coding: UTF-8 -*-
"""Postprocess coo1980.ttl"""
import argparse
import logging
import types

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import SKOS, RDF, Namespace
from rdflib.util import guess_format

log = logging.getLogger(__name__)

DCT = Namespace('http://purl.org/dc/terms/')
AMMO_HISCO = Namespace('http://ldf.fi/ammo/hisco/')
AMMO = Namespace('http://ldf.fi/ammo/')
AMMO_SCHEMA = Namespace('http://ldf.fi/schema/ammo/')


def add_coo1980_altlabels(g: Graph):
    for coo in g.subjects(RDF.type, SKOS.Concept):
        local_id = str(coo).split('/')[-1]

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


def remove_unused_resources(g: Graph, qualifier: types.FunctionType):
    log.info('Removing unused resources with qualifier %s' % qualifier)

    for resource in list(g.subjects(None, None)):
        if not list(g.subject_predicates(resource)) and qualifier(resource):
            log.debug('Removing resource %s' % resource)
            g.remove((resource, None, None))

    return g


def is_hisco_resource(resource: URIRef):
    return str(resource).startswith(str(AMMO_HISCO))


def add_hisco_labels(g: Graph):
    """
    Add English labels for AMMO resources from HISCO
    """
    for sub, obj in list(g.subject_objects(AMMO.hisco_code)):
        hisco_label = g.value(obj, SKOS.prefLabel)
        if hisco_label:
            g.add((sub, SKOS.prefLabel, hisco_label))
            g.add((sub, DCT.source, URIRef('http://ldf.fi/ammo/sources/hisco')))
        else:
            log.info('No prefLabel found for resource %s' % obj)

    return g


def main():
    argparser = argparse.ArgumentParser(description=__doc__, fromfile_prefix_chars='@')

    argparser.add_argument("task", help="Task to perform",
                           choices=['add_altlabels', 'remove_empty_literals', 'remove_unused_hisco', 'add_en_labels'],)
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
        log.info('Adding altLabels to COO1980')
        g = add_coo1980_altlabels(g)

    elif args.task == 'remove_empty_literals':
        log.info('Removing empty altLabels')
        g = remove_empty_literals(g, SKOS.altLabel)

    elif args.task == 'remove_unused_hisco':
        log.info('Removing unused HISCO resources')
        g = remove_unused_resources(g, is_hisco_resource)
        g = remove_unused_resources(g, is_hisco_resource)
        g = remove_unused_resources(g, is_hisco_resource)

    elif args.task == 'add_en_labels':
        log.info('Adding English labels from HISCO')
        g = add_hisco_labels(g)

    g.bind('dct', DCT)
    g.bind('skos', SKOS)
    g.bind('ammo', AMMO)
    g.bind('hisco', AMMO_HISCO)
    g.serialize(args.output, format=guess_format(args.output))


if __name__ == '__main__':
    main()
