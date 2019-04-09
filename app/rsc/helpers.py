import json
import os
import glob
import re

def open_json_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data

def update_metadata(data, new_features):
        result = data.copy()
        result.setdefault("metadata", new_features).update(new_features)
        return result

def get_jsons_file_path_from_dir(abs_dir_path):
        file_path = os.path.join(abs_dir_path,"**/*.json")
        return glob.glob(file_path,recursive = True)

def parse_name(file_path, pattern):
        file_name = file_path.split("/")[-1]
        return re.match(pattern,file_name).groupdict()

def normalize_samples(sample_data, pattern):
        features = sample_data.copy()
        samples = list()
        for k,_ in sample_data.items():
            match = re.match(pattern,k)
            if match is not None:
                sample_num = match.groupdict().get("sample_id")
                sample_name = match.groupdict().get("sample_name")
                sample_data = features.pop(sample_name)
                sample_data.setdefault("sample_id", sample_num)
                samples.append(sample_data)
        return [dig_into_subdict({**sample,**features},"sample_id","metadata") for sample in samples]

def dig_into_subdict(dict_,key,target):
    value = dict_.pop(key)
    dict_.get(target).setdefault(key,value)
    return dict_

def get_samples_from_json(file_path, sample_name_pattern, file_name_pattern):
        data = open_json_file(file_path)
        samples = normalize_samples(data, sample_name_pattern)
        metadata = parse_name(file_path, file_name_pattern)
        return [update_metadata(sample, metadata) for sample in samples]
            
def sort_data_between(datas,categories):
    datas_tuple_list = [(data.get("metadata").get(categories), data) for data in datas]
    datas_tuple_list = sorted(datas_tuple_list,key=lambda x: x[0])
    collection_curr = datas_tuple_list[0][0]
    result = list()
    collections_samples = dict()
    for collection , data in datas_tuple_list:
        if collection == collection_curr:
            result.append(data)
        else:
            collections_samples.setdefault(collection_curr,result)
            collection_curr = collection
            result = [data]
    else:
        collections_samples.setdefault(collection_curr,result)
    return collections_samples