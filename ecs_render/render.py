import os
import errno
import magic
import yaml
import jinja2
from jinja2 import Template


# support function allowing to read content of a file or directory specified by path variable
def load_path(path):

    # test if file even exists
    if not os.path.exists(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
    
    # Load as a directory
    if os.path.isdir(path):
        vars = []
        for f in os.listdir(path):
            vars += load_path(os.path.join(path,f))
        return vars

    else:
        # print ("reading file")
        mime = magic.from_file(path, mime=True)
        if mime != "text/plain":
            raise Exception("Not a text/plain format")
        
        # Try to read yaml file
        with open(path, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if data.__class__.__name__ != 'dict':
                raise Exception("Not a loadable yaml format - {}".format(path))
            return [data]


# This function will need to merge all loaded dicts
# At the moment, I will implemented very simple merge without deep nesting 
# merging support. 
def merge_dicts(list_of_dicts):
    _tmp = {}
    for d in list_of_dicts:
        print( _tmp, d)
        _tmp = {**_tmp, **d}
    return _tmp


# This function takes task_definition in the form of a dict and uses jinja2 for
# variable interplation using values which is another dict composed of all provided 
# variables
def render(task_definition, values):
    td = yaml.dump(task_definition, Dumper=yaml.Dumper)
    template = Template(td)
    r = template.render(**values)
    return yaml.load(r, Loader=yaml.FullLoader)
