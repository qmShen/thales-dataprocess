from objParseLib.objParser import ObjParser

if __name__ == '__main__':
    obj_parser = ObjParser()
    obj_parser.read_obj('objData/Mongkok.obj')
    # obj_parser.extract_map_through_layers()
    obj_parser.generate_map('output/Mongkok.json')