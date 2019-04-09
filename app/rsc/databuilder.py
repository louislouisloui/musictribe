# Native
import os
import re
# Local
from rsc.helpers import get_samples_from_json, get_jsons_file_path_from_dir

class DataBuilder():
    """ A Builder pattern to extract json-formatted data
    """

    def __init__(self, data_rel_path = "data",
                sample_name_pattern = re.compile("^(?P<sample_name>sample_(?P<sample_id>\d+))"),
                file_name_pattern = re.compile("^ml_(?P<dataset>\w+)_data_(?P<instrument>\w+)_(?P<file_id>\d+).json")):
        self.sample_name_pattern = sample_name_pattern
        self.file_name_pattern = file_name_pattern
    
    def load(self,relative_path):
        abs_path = os.path.join(os.getcwd(),relative_path)
        if os.path.isfile(abs_path) or os.path.isdir(abs_path):
            load_method = self._get_loader(os.path.isfile(abs_path))
        else:
            raise Exception("Not a dir nor a file path")
        return load_method(abs_path)
    
    def _get_loader(self,isfile):
        return self._file_loader if isfile else self._dir_loader
    
    def _file_loader(self,file_path):
        return get_samples_from_json(file_path, self.sample_name_pattern, 
            self.file_name_pattern)
    
    def _dir_loader(self,dir_path):
        # Todo: thread to mitigate IO
        # In this case, should not be relevant
        file_paths = get_jsons_file_path_from_dir(dir_path)
        result = list()
        for file in file_paths:
            result += self._file_loader(file)
        return result