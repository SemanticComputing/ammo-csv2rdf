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
BIOC = Namespace('http://ldf.fi/schema/bioc/')


def add_coo1980_altlabels(g: Graph):
    for coo in g.subjects(RDF.type, SKOS.Concept):
        local_id = str(coo).split('/')[-1]

        if local_id == '6_7':
            local_id = '6/7'

        g.add((coo, SKOS.altLabel, Literal(local_id)))

        log.debug('Annotating altLabel %s to URI %s' % (local_id, coo))

    return g


def add_coo1980_members(g: Graph):
    for coo in g.subjects(RDF.type, SKOS.Concept):
        g.add((AMMO.coo1980, SKOS.member, coo))

        log.debug('Annotating COO1980 collection memberships to URI %s' % (coo))

    return g


def remove_empty_literals(g: Graph, prop: URIRef):
    for resource, value in list(g.subject_objects(prop)):
        if str(value) == '':
            g.remove((resource, prop, value))
            log.debug('Removing empty literal for %s  %s' % (resource, prop))

    return g


def remove_unused_resources(g: Graph):
    log.info('Removing unused HISCO resources')

    for resource in list(g.objects(AMMO.hisco, SKOS.member)):
        if not list(g.subjects(AMMO.hisco_code, resource)) and not list(g.subjects(SKOS.broader, resource)):
            log.debug('Removing resource %s' % resource)
            g.remove((resource, None, None))
            g.remove((None, SKOS.member, resource))

    return g


def _is_hisco_resource(resource: URIRef):
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


def get_localnames(g: Graph, prop: URIRef):
    for sub, obj in list(g.subject_objects(prop)):
        if str(obj).startswith('file://'):
            label = str(obj).split('/')[-1]
            g.remove((sub, prop, obj))
            g.add((sub, prop, Literal(label, lang="en")))

    return g


def process_kdb_labels(g: Graph):
    """
    Add English labels for AMMO resources transformed from KDB1
    """
    TEMP = Namespace('http://ldf.fi/temp/')

    for sub, obj in list(g.subject_objects(TEMP.kdb_link_preflabel)):
        kdb_label = g.value(obj, TEMP.label)
        if kdb_label:
            g.add((sub, SKOS.prefLabel, kdb_label))
            # g.add((sub, DCT.source, URIRef('http://ldf.fi/ammo/sources/kdb')))
            # g.remove((obj, SKOS.prefLabel, kdb_label))
            log.debug('Adding prefLabel "{lbl}" for resource {uri}'.format(lbl=kdb_label, uri=sub))
        else:
            log.info('No KDB1 prefLabel found for resource %s' % obj)

        g.remove((sub, TEMP.kdb_link_preflabel, obj))

    for sub, obj in list(g.subject_objects(URIRef('http://ldf.fi/temp/kdb_link_altlabel'))):
        kdb_label = g.value(obj, TEMP.label)
        if kdb_label:
            g.add((sub, SKOS.altLabel, kdb_label))
            log.debug('Adding altLabel "{lbl}" for resource {uri}'.format(lbl=kdb_label, uri=sub))
        else:
            log.info('No KDB1 altLabel found for resource %s' % obj)

        g.remove((sub, TEMP.kdb_link_altlabel, obj))

    for sub, pre, obj in list(g.triples((None, TEMP.label, None))):
        g.remove((sub, pre, obj))

    return g


def main():
    argparser = argparse.ArgumentParser(description=__doc__, fromfile_prefix_chars='@')

    argparser.add_argument("task", help="Task to perform",
                           choices=['add_altlabels', 'add_coo1980_members', 'remove_empty_literals',
                                    'remove_unused_hisco', 'add_en_labels', 'get_localnames', 'process_kdb_labels'],)
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

    if args.task == 'add_coo1980_members':
        log.info('Adding altLabels to COO1980')
        g = add_coo1980_members(g)

    elif args.task == 'remove_empty_literals':
        log.info('Removing empty altLabels')
        g = remove_empty_literals(g, SKOS.altLabel)
        g = remove_empty_literals(g, SKOS.prefLabel)

    elif args.task == 'remove_unused_hisco':
        log.info('Removing unused HISCO resources')
        g = remove_unused_resources(g)
        g = remove_unused_resources(g)
        g = remove_unused_resources(g)

    elif args.task == 'add_en_labels':
        log.info('Adding English labels from HISCO')
        g = add_hisco_labels(g)

    elif args.task == 'get_localnames':
        log.info('Map skos:prefLabel URI values to literals')
        g = get_localnames(g, SKOS.prefLabel)

    elif args.task == 'process_kdb_labels':
        log.info('Adding English labels from KDB1')
        g = process_kdb_labels(g)

    g.bind('ammo', AMMO)
    g.bind('ammo-s', AMMO_SCHEMA)
    g.bind('bio-crm', BIOC)
    g.bind('dct', DCT)
    g.bind('hisco', AMMO_HISCO)
    g.bind('skos', SKOS)
    g.serialize(args.output, format=guess_format(args.output))


if __name__ == '__main__':
    main()
