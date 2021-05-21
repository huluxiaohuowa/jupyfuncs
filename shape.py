# shape

import os
import subprocess
from copy import deepcopy

from rdkit import Chem
from rdkit.Chem import AllChem
from pyshapeit import AlignMol
import multiprocess as mp

from rdkit import RDLogger

from .pbar import tqdm
from .norm import Normalizer

lg = RDLogger.logger()
lg.setLevel(4)


__all__ = [
    'get_mols_from_smi',
    'get_aligned_mol',
    'get_aligned_sdf'
]


def get_mols_from_smi(probe_smifile):
    mols = []
    with open(probe_smifile) as f:
        for line in f.readlines():
            smi = line.strip()
            mol = None
            try:
                mol = Chem.MolFromSmiles(smi)
            except Exception as e:
                print(e)
            if mol:
                mols.append(mol)
    return mols


def get_aligned_mol(
    ref_mol, probe_mol, num_confs, num_cpu
):

    mol1 = ref_mol
    mol1.SetProp('_Name', 'ref')

    AllChem.EmbedMultipleConfs(
        probe_mol,
        numConfs=num_confs,
        numThreads=num_cpu
    )

    score = 0
    # conf_id = -1
    
    aligned_mol = deepcopy(probe_mol)

    for i in range(probe_mol.GetNumConformers()):

        mol2 = Chem.MolFromMolBlock(
            Chem.MolToMolBlock(probe_mol, confId=i)
        )
        mol2.SetProp('_Name', 'probe')

        sim_score = AlignMol(mol1, mol2)
        if sim_score > score:
            score = sim_score
            aligned_mol = deepcopy(mol2)
#     pbar.update(1)

    return aligned_mol


def get_aligned_mol_mp(
    config
):
    return get_aligned_mol(*config)


def gen_configs(ref_mol, mols, num_confs, num_cpu):
    configs = []
    for probe_mol in mols:
        configs.append((ref_mol, probe_mol, num_confs, num_cpu))
    return configs


def get_aligned_sdf(
    ref_sdf: str,
    probe_smifile: str,
    num_confs=150,
    num_cpu=5,
    num_workers=10,
    output_sdf=None,
    print_info=True,
    norm_mol=True
):
    ref_sdf = os.path.abspath(ref_sdf)
    ref_mol = Chem.SDMolSupplier(ref_sdf)[0]
    if not output_sdf:
        output_sdf = os.path.abspath(probe_smifile) + '.sdf'
    else:
        output_sdf = os.path.abspath(output_sdf)
    
    out_aligned = output_sdf + 'ali.sdf'
    score_file = output_sdf + 'score.csv'
    
    mols = get_mols_from_smi(probe_smifile)

    configs = gen_configs(
        ref_mol, mols, num_confs=num_confs, num_cpu=num_cpu
    )
    
    pool = mp.Pool(num_workers)
    aligned_mols = list(
        tqdm(
            pool.imap(get_aligned_mol_mp, configs),
            total=len(mols),
            desc='All mols'
        )
    )
    if norm_mol:
        normer = Normalizer()
    sdwriter = Chem.SDWriter(output_sdf) 
    for mol in aligned_mols:
        if norm_mol:
            mol = normer(mol)
        sdwriter.write(mol)
        sdwriter.flush()
    sdwriter.close()
    
    command = f'shape-it -r {ref_sdf} -d {output_sdf} -o {out_aligned} -s {score_file}' 
    # os.system(command)
    out_info = subprocess.getoutput(command)
    if print_info:
        print(out_info)
    
    if norm_mol:
        fix_path = out_aligned + 'fix.sdf'
        mols = Chem.SDMolSupplier(out_aligned)
        sdwriter = Chem.SDWriter(fix_path)
        for mol in mols:
            mol = normer(mol)
            sdwriter.write(mol)
            sdwriter.flush()
        sdwriter.close()
        return fix_path
    else:
        return out_aligned
    
    # shape-it -r ref_sdf  -d output_sdf -o out_aligned -s score_file