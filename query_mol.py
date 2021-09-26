import re

import cirpy
import pubchempy as pcp
# from rdkit import Chem
import molvs as mv


def query_from_cir(query_name: str):
    smiles = None
    # cas_list = []
    # name_list = []
    
    cas_list = cirpy.resolve(query_name, 'cas')
    if cas_list is None or not cas_list:
        cas_list = []
    if isinstance(cas_list, str):
        cas_list = [cas_list]

    name_list = cirpy.resolve(query_name, 'names')
    if name_list is None or not name_list:
        name_list = []
    if isinstance(name_list, str):
        name_list = [name_list]

    smiles = cirpy.resolve(query_name, 'smiles')

    return smiles, cas_list, name_list


def query_from_pubchem(query_name: str):
    results = pcp.get_compounds(query_name, 'name')
    smiles = None
    name_list = set()
    cas_list = set()

    if any(results):
        smiles = mv.standardize_smiles(results[0].canonical_smiles)
        for compound in results:
            name_list.update(set(compound.synonyms))
            for syn in compound.synonyms:
                match = re.match('(\d{2,7}-\d\d-\d)', syn)
                if match:
                    cas_list.add(match.group(1))
        
        cas_list = list(cas_list)
        name_list = list(name_list)

    return smiles, cas_list, name_list