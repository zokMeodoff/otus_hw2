import collections
import ast
import os
from abc import ABCMeta
from statistics_collector.functions import flat_list, is_special_function, split_snake_case_name_to_words, get_verbs, get_nouns


class AbstractParser(metaclass=ABCMeta):
    def __init__(self):
        self._path = None

    def set_path(self, path):
        self._path = path

    def get_path(self):
        return self._path


class PythonParser(AbstractParser):
    def __init__(self):
        super(PythonParser, self).__init__()

    def _get_filenames(self, extension='py'):
        filenames = []
        for dirname, dirs, files in os.walk(self._path, topdown=True):
            for file in files:
                if file.endswith('.{extension}'.format(extension=extension)):
                    filenames.append(os.path.join(dirname, file))
        return filenames

    def _get_trees(self):
        trees = []
        for filename in self._get_filenames():
            with open(filename, 'r', encoding='utf-8') as attempt_handler:
                main_file_content = attempt_handler.read()
                try:
                    tree = ast.parse(main_file_content)
                    trees.append(tree)
                except SyntaxError as e:
                    pass
        return trees

    def _get_functions_names(self, tree):
        functions = [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return [f for f in functions if not is_special_function(f)]

    def _get_variables_names(self, tree):
        functions_bodies = [node.body for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return flat_list(
            [[a.targets[0].id for a in fb if isinstance(a, ast.Assign) and isinstance(a.targets[0], ast.Name)] for fb in
             functions_bodies])

    def _get_words_from_part_of_code(self, part_of_code):
        trees = self._get_trees()
        names = []
        if part_of_code == 'func':
            names = flat_list([self._get_functions_names(t) for t in trees])
        elif part_of_code == 'var':
            names = flat_list([self._get_variables_names(t) for t in trees])
        words = flat_list([split_snake_case_name_to_words(name) for name in names])
        return words

    def get_words_count(self, part_of_code, part_of_speech, top_size):
        words = self._get_words_from_part_of_code(part_of_code)
        sorted_words = {
            'verb': get_verbs(words),
            'noun': get_nouns(words),
        }
        result = sorted_words[part_of_speech]
        return collections.Counter(result).most_common(top_size)

