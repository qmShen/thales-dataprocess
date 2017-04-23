# v, vn, vt, f, g
import json
class ObjParser:
    def __init__(self):
        pass

    def read_obj(self, file_path):
        self.path = file_path
        self.obj_lines = []
        with open(file_path, 'r') as obj_file:
            lines = obj_file.readlines()
            lines = [line.strip() for line in lines]
            self.obj_lines = lines
            self.backup_lines = lines

            self.init_all_vertex()
            # print(self.vertex)

    def restore_lines(self):
        self.obj_lines = self.backup_lines


    def remove_unnecessary_lines(self, un_arr):
        lines = []
        for line in self.obj_lines:
            save = True
            for start_sign in un_arr:
                if line.startswith(start_sign):
                    save = False
                    break
            if save == True:
                lines.append(line)
        self.obj_lines = lines


    def extract_lines_start_with(self, start_sign):
        lines = []
        for line in self.obj_lines:
            if line.startswith(start_sign):
                lines.append(line)
        return lines

    def init_all_vertex(self):
        """
        Init vertex array
        :return: 
        """
        self.vertex = []
        for line in self.backup_lines:
            if self.type_of_line(line) == 'v':
                context = self.context_of_line(line)
                self.vertex.append([float(e) for e in context])

    def resort_lines(self):
        v_lines = self.extract_lines_start_with('v')
        f_lines = self.extract_lines_start_with('f')
        lines = v_lines + f_lines
        self.obj_lines = lines

    def type_of_line(self, line):
        if line.strip() == '':
            return None
        segs = line.split(' ');
        segs = [seg.strip() for seg in segs]
        if segs[0] == 'g':
            return 'g'
        elif segs[0] == 'v':
            return 'v'
        elif segs[0] == 'vt':
            return 'vt'
        elif segs[0] == 'f':
            return 'f'
        elif segs[0] == 'vn':
            return 'vn'

    def context_of_line(self, line):
        line_type = self.type_of_line(line)
        segs = line.split(' ');
        segs = [seg.strip() for seg in segs]

        if line_type == 'v' or line_type == 'vn' or line_type == 'vt' or line_type == 'f' or line_type == 'g':
            return segs[1:]
        else:
            return None

    def _get_vertex_from_face_context(self, face_context):
        if (not self.vertex) or (len(self.vertex) == 0):
            return None
        vertex_for_one_face = []
        for vertex in face_context:
            _v = self.vertex[int(vertex.split('/')[0]) - 1];
            vertex_for_one_face.append([_v[2], _v[0], _v[1]])

        # vertex_for_one_face = [self.vertex[int(vertex.split('/')[0]) - 1] for vertex in face_context]

        return vertex_for_one_face



    def extract_map_through_layers(self):
        all_meshes = []
        meshs = []
        for i in range(len(self.obj_lines)):
            line = self.obj_lines[i]

            if self.type_of_line(line) == 'g':

                if len(meshs) != 0:
                    all_meshes.append(meshs)
                meshs = []

            if self.type_of_line(line) == 'f':
                vertices = self._get_vertex_from_face_context(self.context_of_line(line))
                meshs.append(vertices)

            if i == len(self.obj_lines) - 1:
                all_meshes.append(meshs)

        mesh_map = {}

        for i in range(len(all_meshes)):
            mesh_map[i] = all_meshes[i]
        print(mesh_map)
        return mesh_map

    def output_to_file(self, path):
        with open(path, 'w') as output_file:
            for line in self.obj_lines:
                output_file.write(line+'\n')

    def generate_map(self, output_path):

        json_data = self.extract_map_through_layers()
        with open(output_path, 'w') as output_file:
            json.dump(json_data, output_file)