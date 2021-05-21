#Jupyter funcs

from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from IPython.display import SVG
import py3Dmol
from rdkit.Chem import AllChem
from ipywidgets import interact, interactive, fixed
from rdkit.Chem.rdRGroupDecomposition import RGroupDecomposition, RGroupDecompositionParameters, \
   RGroupMatching, RGroupScore, RGroupLabels, RGroupCoreAlignment, RGroupLabelling
import os
from rdkit.Chem.Draw import IPythonConsole
IPythonConsole.ipython_useSVG=True
import pandas as pd
from rdkit.Chem import PandasTools
from rdkit.Chem import Draw
from IPython.display import HTML
from rdkit import rdBase
from rdkit.Chem import Draw
from IPython.display import display
from copy import deepcopy


__all__ = [
    'draw_mol',
    'draw_confs',
    'show_decomp',
    'get_ids_folds',
    'show_pharmacophore',
    'mol_without_indices',
]

def show_atom_number(mol, label='atomNote'):
    new_mol = deepcopy(mol)
    for atom in new_mol.GetAtoms():
        atom.SetProp(label, str(atom.GetIdx()))
    return new_mol

def moltosvg(mol, molSize = (500,500), kekulize = True):
    mc = mol
    drawer = rdMolDraw2D.MolDraw2DSVG(molSize[0],molSize[1])
    drawer.DrawMolecule(mc)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    return svg.replace('svg:','')

def draw_mol(mol):
    return SVG(moltosvg(show_atom_number(mol)))

def drawit(m, p, confId=-1):
    mb = Chem.MolToMolBlock(m, confId=confId)
    p.removeAllModels()
    p.addModel(mb,'sdf')
    p.setStyle({'stick':{}})
    p.setBackgroundColor('0xeeeeee')
    p.zoomTo()
    return p.show()

def draw_confs(m):
    p = py3Dmol.view(width=500,height=500)
    return interact(drawit, m=fixed(m),p=fixed(p),confId=(0, m.GetNumConformers()-1))

def do_decomp(mols, cores, options):
#     options.removeHydrogensPostMatch = True
    options.rgroupLabelling = RGroupLabelling.AtomMap
    decomp = RGroupDecomposition(cores, options)
    for mol in mols:
        decomp.Add(mol)
#         print(Chem.MolToSmiles(mol))
    decomp.Process()
    return decomp

def show_decomp(mols, cores, options, item=False):
    decomp = do_decomp(mols, cores, options)
    if item:
        rows = decomp.GetRGroupsAsRows();
        items=['{}:{}'.format(group, Chem.MolToSmiles(row[group])) for row in rows for group in row]
        return ' '.join(items)
    else:
        cols = decomp.GetRGroupsAsColumns()
        cols['mol'] = mols
        cols['input core'] = cores[0]
        df = pd.DataFrame(cols);
        PandasTools.ChangeMoleculeRendering(df)
        return HTML(df.to_html())

def get_ids_folds(id_list, num_folds, need_shuffle=False):
    if need_shuffle:
        from random import shuffle
        shuffle(id_list)
    num_ids = len(id_list)
    assert num_ids >= num_folds
    
    num_each_fold = int(num_ids / num_folds)
    
    blocks = []
    
    for i in range(num_folds):
        start = num_each_fold * i
        end = start + num_each_fold
        if end > num_ids - 1:
            end = num_ids - 1
        
        blocks.append(id_list[start: end])
    
    id_blocks = []
    for i in range(num_folds):
        id_blocks.append(
            (list(itertools.chain.from_iterable([blocks[j] for j in range(num_folds) if j != i])),
             blocks[i])
        )
        
    return id_blocks


keep = ["Donor", "Acceptor","Aromatic", "Hydrophobe", "LumpedHydrophobe"]
def show_pharmacophore(
    sdf_path,
    keep=keep,
    fdf_dir='/data/aidd-server/trained_models/defined_BaseFeatures.fdef'
):
    template_mol = [m for m in Chem.SDMolSupplier(sdf_path)][0]
    fdef = AllChem.BuildFeatureFactory(
        fdf_dir
    )
    prob_feats = fdef.GetFeaturesForMol(template_mol)
    prob_feats = [f for f in prob_feats if f.GetFamily() in keep]
    prob_points = [list(x.GetPos()) for x in prob_feats]

    for i, feat in enumerate(prob_feats):
        atomids = feat.GetAtomIds()
        print(
            "pharamcophore index:{0}; feature:{1}; type:{2}; atom id:{3}".format(
                i, 
                feat.GetFamily(), 
                feat.GetType(),
                atomids
            )
        )
        display(
            Draw.MolToImage(
                template_mol,
                highlightAtoms=list(atomids),
                highlightColor=[0,1,0],
                useSVG=True
            )
        )


def mol_without_indices( 
    mol_input: Chem.Mol, 
    remove_indices=[], 
    keep_properties=[] 
): 
     
    atom_list, bond_list, idx_map = [], [], {}  # idx_map: {old: new} 
    for atom in mol_input.GetAtoms(): 
         
        props = {} 
        for property_name in keep_properties: 
            if property_name in atom.GetPropsAsDict(): 
                props[property_name] = atom.GetPropsAsDict()[property_name] 
        symbol = atom.GetSymbol() 
         
        if symbol.startswith('*'): 
            atom_symbol = '*' 
            props['molAtomMapNumber'] = atom.GetAtomMapNum() 
        elif symbol.startswith('R'): 
            atom_symbol = '*' 
            if len(symbol) > 1: 
                atom_map_num = int(symbol[1:]) 
            else: 
                atom_map_num = atom.GetAtomMapNum() 
            props['dummyLabel'] = 'R' + str(atom_map_num) 
            props['_MolFileRLabel'] = str(atom_map_num) 
            props['molAtomMapNumber'] = atom_map_num 
             
        else: 
            atom_symbol = symbol 
        atom_list.append( 
            ( 
                atom_symbol, 
                atom.GetFormalCharge(), 
                atom.GetNumExplicitHs(), 
                props 
            ) 
        ) 
    for bond in mol_input.GetBonds(): 
        bond_list.append( 
            ( 
                bond.GetBeginAtomIdx(), 
                bond.GetEndAtomIdx(), 
                bond.GetBondType() 
            ) 
        ) 
    mol = Chem.RWMol(Chem.Mol()) 
     
    new_idx = 0 
    for atom_index, atom_info in enumerate(atom_list): 
        if atom_index not in remove_indices: 
            atom = Chem.Atom(atom_info[0]) 
            atom.SetFormalCharge(atom_info[1]) 
            atom.SetNumExplicitHs(atom_info[2]) 
             
            for property_name in atom_info[3]: 
                if isinstance(atom_info[3][property_name], str): 
                    atom.SetProp(property_name, atom_info[3][property_name]) 
                elif isinstance(atom_info[3][property_name], int): 
                    atom.SetIntProp(property_name, atom_info[3][property_name]) 
            mol.AddAtom(atom) 
            idx_map[atom_index] = new_idx 
            new_idx += 1 
    for bond_info in bond_list: 
        if ( 
            bond_info[0] not in remove_indices 
            and bond_info[1] not in remove_indices 
        ): 
            mol.AddBond( 
                idx_map[bond_info[0]], 
                idx_map[bond_info[1]], 
                bond_info[2] 
            ) 
        else: 
            one_in = False 
            if ( 
                (bond_info[0] in remove_indices) 
                and (bond_info[1] not in remove_indices) 
            ): 
                keep_index = bond_info[1] 
                remove_index = bond_info[0] 
                one_in = True 
            elif ( 
                (bond_info[1] in remove_indices) 
                and (bond_info[0] not in remove_indices) 
            ): 
                keep_index = bond_info[0] 
                remove_index = bond_info[1] 
                one_in = True 
            if one_in:  
                if atom_list[keep_index][0] == 'N': 
                    old_num_explicit_Hs = mol.GetAtomWithIdx( 
                        idx_map[keep_index] 
                    ).GetNumExplicitHs() 

                    mol.GetAtomWithIdx(idx_map[keep_index]).SetNumExplicitHs( 
                        old_num_explicit_Hs + 1 
                    ) 
    mol = Chem.Mol(mol) 
    return mol
