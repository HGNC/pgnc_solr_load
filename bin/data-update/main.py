#!/usr/bin/env python

import psycopg2
import json
import argparse
import re
import time
import os
from http import HTTPStatus
import pysolr

from models.gene import Gene

class SolrUpdateError(Exception):
    """Exception raised for errors during Solr update operations."""
    pass

def get_xrefs_for_gene(connection: psycopg2.extensions.connection, gene_id: int) -> dict:
    xref_sql = """
        select x.display_id, er.name
        from gene_has_xref ghx
        join xref x on ghx.xref_id = x.id
        join external_resource er on x.ext_resource_id = er.id
        where ghx.gene_id = %s
    """
    xrefs: dict = {}
    cursor = connection.cursor()
    cursor.execute(xref_sql, (gene_id,))
    xref_res = cursor.fetchall()
    for xref in xref_res:
        if xref[1] not in xrefs:
            xrefs[xref[1]] = []
        xrefs[xref[1]].append(xref[0])
    cursor.close()
    return xrefs


def get_locus_types_for_gene(connection: psycopg2.extensions.connection, gene_id: int) -> list[str]:
    locus_types_sql = """
        select locus_type.name
        from gene_has_locus_type
        join locus_type on gene_has_locus_type.locus_type_id = locus_type.id
        where gene_has_locus_type.gene_id = %s
    """
    locus_types: list[str] = []
    cursor = connection.cursor()
    cursor.execute(locus_types_sql, (gene_id,))
    locus_type_res = cursor.fetchall()
    for locus_type in locus_type_res:
        locus_types.append(locus_type[0])
    cursor.close()
    return locus_types


def get_symbols_for_gene(connection: psycopg2.extensions.connection, gene_id: int) -> dict:
    symbols_sql = """
        select symbol.symbol, gene_has_symbol.type
        from gene_has_symbol
        join symbol
        on gene_has_symbol.symbol_id = symbol.id
        where gene_has_symbol.gene_id = %s
    """
    symbol_dict: dict = {
        'approved': None,
        'alias': [],
        'prev': []
    }
    cursor = connection.cursor()
    cursor.execute(symbols_sql, (gene_id,))
    symbols = cursor.fetchall()
    for symbol in symbols:
        if symbol[1] == 'approved':
            symbol_dict[symbol[1]] = symbol[0]
        else:
            symbol_dict[symbol[1]].append(symbol[0])
    cursor.close()
    return symbol_dict


def get_names_for_gene(connection: psycopg2.extensions.connection, gene_id: int) -> dict:
    names_sql = """
        select name.name, gene_has_name.type
        from gene_has_name
        join name on gene_has_name.name_id = name.id
        where gene_has_name.name_id = %s
    """
    name_dict = {
        'approved': None,
        'alias': [],
        'prev': []
    }
    cursor = connection.cursor()
    cursor.execute(names_sql, (gene_id,))
    names = cursor.fetchall()
    for name in names:
        if name[1] == 'approved':
            name_dict[name[1]] = name[0]
        else:
            name_dict[name[1]].append(name[0])
    cursor.close()
    return name_dict


def get_genes(connection: psycopg2.extensions.connection) -> list[Gene]:
    genes_sql = """
        select gene.id, gene.taxon_id, gene.status, location.name as chromosome
        from gene
        left outer join gene_has_location
            join location on gene_has_location.location_id = location.id
        on gene.id = gene_has_location.gene_id
        where gene.status in ('approved', 'withdrawn', 'merged', 'split')
    """
    genes: list[Gene] = []
    cursor = connection.cursor()
    cursor.execute(genes_sql)
    gene_recs = cursor.fetchall()
    for row in gene_recs:
        gene = Gene()
        gene.pgnc_id = row[0]
        gene.taxon_id = row[1]
        gene.status = row[2]
        gene.chromosome = row[3]
        genes.append(gene)
    cursor.close()
    return genes


def remove_empty_keys(d: dict) -> dict:
    for k in list(d.keys()):
        if not d[k]:
            del d[k]
        elif isinstance(d[k], list):
            if len(d[k]) == 0:
                del d[k]
        elif isinstance(d[k], dict):
            remove_empty_keys(d[k])
    return d


def create_solr_json() -> str:
    solr_json = None
    try:
        connection = psycopg2.connect(
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            database=os.environ['DB_NAME']
        )
        genes = get_genes(connection)
        solr_dicts: list[dict] = []
        for gene in genes:
            symbols = get_symbols_for_gene(connection, gene.pgnc_id)
            gene.alias_gene_symbol = symbols['alias']
            gene.prev_gene_symbol = symbols['prev']
            gene.gene_symbol = symbols['approved']
            names = get_names_for_gene(connection, gene.pgnc_id)
            gene.alias_gene_name = names['alias']
            gene.prev_gene_name = names['prev']
            gene.gene_name = names['approved']
            gene.locus_types = get_locus_types_for_gene(connection, gene.pgnc_id)
            xrefs = get_xrefs_for_gene(connection, gene.pgnc_id)
            gene.ensembl_gene_id = xrefs.get('Ensembl Gene', None)
            gene.ncbi_gene_id = xrefs.get('NCBI Gene', None)
            gene.pubmed_id = xrefs.get('PubMed', None)
            gene.uniprot_id = xrefs.get('UniProt', None)
            gene.phytozome_id = xrefs.get('Phytozome', None)
            if gene.phytozome_id is not None:
                gene.primary_id = xrefs['Phytozome'][0]
            else:
                gene.primary_id = gene.pgnc_id
            solr_dicts.append(remove_empty_keys(gene.to_dict()))
        if len(solr_dicts) < 1:
            raise SolrUpdateError("No gene data found to index in Solr")
        solr_json = json.dumps(solr_dicts, indent=4)
        return solr_json
    except (SolrUpdateError) as error:
        raise SolrUpdateError(f'Function: create_solr_json Error: {error}')
    finally:
        # closing database connection.
        if connection:
            connection.close()
            print("PostgreSQL connection is closed")


def __parse_solr_response(e: pysolr.SolrError) -> HTTPStatus:
    resp = str(e)
    code_mtch = re.search(r'HTTP (\d{3})', resp)
    if code_mtch.group(1):
        return HTTPStatus(int(code_mtch.group(1)))
    else:
        raise SolrUpdateError(f'Function: __parse_solr_response Error: {e}')


def upload_to_solr(solr_json: str, dry_run: bool) -> None:
    if dry_run:
        print(solr_json)
    else:
        retries = 3
        retry_codes = [
            HTTPStatus.TOO_MANY_REQUESTS,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        ]
        solr = pysolr.Solr('http://solr:8983/solr/pgnc', always_commit=True)
        for i in range(retries):
            try:
                solr.add(json.loads(solr_json))
                break
            except pysolr.SolrError as e:
                http_code = __parse_solr_response(e)
                if http_code in retry_codes:
                    print(f"HTTP {http_code} error. Retrying in 5 seconds...")
                    time.sleep(5)
                    retries -= 1
                    if retries == 0:
                        raise e
                    continue
                else:
                    raise e
        print("Successfully updated Solr index")

def __main__():
    try:
        parser = argparse.ArgumentParser(description='Update Solr index with gene data')
        parser.add_argument('--dry-run', help='Dry run mode', action='store_true')
        args = parser.parse_args()
        solr_json = create_solr_json()
        upload_to_solr(solr_json, args.dry_run)
    except SolrUpdateError as e:
        print(f"Error {type(e)} (__main__): {e}")


__main__()