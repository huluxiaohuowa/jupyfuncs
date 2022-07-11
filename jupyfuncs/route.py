# import json
import typing as t
# from tap import Tap


class MolNode(object):
    def __init__(
        self,
        id_type: str = "CAS",
        id_value: str = "111-222-333",
        smiles: str = "",
        routes: str = ""
    ) -> None:
        self.id_type = id_type
        self.id_value = id_value
        self.smiles = smiles
        self.routes = routes
        
        self.parse_dict()

        # self.info_dict = {
        #     "id_type": self.id_type,
        #     "id_value": self.id_value,
        #     "smiles": self.smiles,
        #     "routes": self.routes
        # }
    
    def parse_dict(self):
        routes = []
        for route in self.routes:
            parse_dict = getattr(route, 'parse_dict', None)
            if parse_dict is not None:
                route.parse_dict()
            # route_dict = route.get_dict()
            if isinstance(route, t.Dict):
                routes.append(route)
            else:
                routes.append(route.get_dict())
                
        self.routes = routes

    def get_dict(self):
        self.parse_dict()
        self.info_dict = {
            "id_type": self.id_type,
            "id_value": self.id_value,
            "smiles": self.smiles,
            "routes": self.routes
        }
        return self.info_dict


class RouteNode(object):
    def __init__(
        self,
        rxn_template: str = "",
        rxn_type: str = "",
        yld: float = 0.0,
        children: t.List[MolNode] = []
    ):
        self.rxn_template = rxn_template
        self.rxn_type = rxn_type
        self.yld = yld
        self.children = children

        self.parse_dict()
    
        # self.info_dict = {
        #     "rxn_template": self.rxn_template,
        #     "rxn_type": rxn_type,
        #     "yield": self.yld,
        #     "children": self.children
        # }
    
    def parse_dict(self):
        children = []
        for mol_node in self.children:
            parse_dict = getattr(mol_node, 'parse_dict', None)
            if parse_dict is not None:
                mol_node.parse_dict()
            if isinstance(mol_node, t.Dict):
                children.append(mol_node)
            else:
                children.append(mol_node.get_dict())
        self.children = children

    def get_dict(self):
        self.parse_dict()
        self.info_dict = {
            "rxn_template": self.rxn_template,
            "rxn_type": self.rxn_type,
            "yield": self.yld,
            "children": self.children
        }
        return self.info_dict
