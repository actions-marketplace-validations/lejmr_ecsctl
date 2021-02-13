import os
import errno
import magic
import yaml


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