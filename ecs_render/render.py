import os
import errno
import magic
import yaml
import jinja2
from jinja2 import Template


# support function allowing to read content of a file or directory specified by path variable
def load_path(path, ivalues=None):

    # test if file even exists
    if not os.path.exists(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
    
    # Load as a directory
    if os.path.isdir(path):
        vars = []
        for f in os.listdir(path):
            try:
                vars += load_path(os.path.join(path,f), ivalues)
            except Exception as e:
                # I particularly dont like this way, but it works.. 
                # TODO: should be modified, so an dedicated exception is raised
                if "Not a loadable yaml format" in str(e):
                    continue
                raise e
        return vars

    else:
        # print ("reading file")
        mime = magic.from_file(path, mime=True)
        if mime != "text/plain":
            raise Exception("Not a text/plain format")
        
        # Try to read yaml file
        with open(path, "r") as f:
            if not ivalues is None:
                # Interpolate the loaded file - this is most likely task_definition
                # That should be in Jinja2 format
                t = Template(f.read())
                r = t.render(**ivalues)
                data = yaml.load(r, Loader=yaml.FullLoader)
            else:
                # Simply load the yaml/json - this should be file with values
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

# This is just a helping function mimicing Ansible's interpolation within variables
# I do not exepct anybody will ever need more than 5 consecutive interpolations
# if so it means there is a very bad pattern how deployment is configured
def interpolate_values(values):
    td = yaml.dump(values, Dumper=yaml.Dumper)
    for i in range(0,5):
        template = Template(td)
        td = template.render(**values)
        if not "{{" in td:
            return yaml.load(td, Loader=yaml.FullLoader)
    raise Exception("Too many recusions")


# This function takes task_definition in the form of a dict and uses jinja2 for
# variable interplation using values which is another dict composed of all provided 
# variables
def render(task_definition, values):
    td = yaml.dump(task_definition, Dumper=yaml.Dumper)
    template = Template(td)
    td = template.render(interpolate_values(values))
    return yaml.load(td, Loader=yaml.FullLoader)
