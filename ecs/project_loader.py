from .exceptions import InvalidProjectStructure, InvalidInputFiles
import os
import itertools


def verify_project_files(td, values):
    # Verify td path
    try:
        verify_input_file(td)
    except FileNotFoundError as e:
        raise InvalidProjectStructure

    # Validate there is at least one input file
    if len(values) == 0:
        raise InvalidProjectStructure

    # Verify value files
    for v in values:
        verify_input_file(v)



def verify_input_file(p):
    # path does not have even a value
    if not p:
        raise FileNotFoundError

    # p has a value but it is not a path
    if not os.path.exists(p):
        raise FileNotFoundError

    # Return value if complies
    return p


def _find_td_ser(project_path, tp="task-definition"):
    """
    Function identifying task-definition within a project directory. The
    exps variable define order/priority for selection of task-definition
    """
    e = [".yml", ".yaml", ".json", "/"]
    exps = ["{}{}".format(tp, x) for x in e]

    # Generate paths
    paths = [os.path.join(project_path, x) for x in exps]

    # Find the first matching file/dir
    for p in paths:
        if os.path.exists(p):
            return p
    
    # Raise exception if no such file is in the project directory
    raise FileNotFoundError


def _find_values(project_path):
    """
    This function identifies values used for tempalte interpolation within
    the values.yml of values/default.yml/yaml/json file.
    """

    # Define potential sources
    exts = ["yml", "yaml", "json"]
    file_names  = ["values", "values/default"]
    
    # Iterate
    for fn in file_names:
        p = itertools.product([fn], exts)
        paths = [os.path.join(project_path, "{}.{}".format(*x)) for x in p]

        for path in paths:
            if os.path.exists(path):
                return [path]

    # Raise exception if no such file is in the project directory
    raise FileNotFoundError


    

def load_project(project_path="ecs/", values=None):
    # Find task-definition.yml/json/yaml or task-definition/
    try:
        td = _find_td_ser(project_path)
    except FileNotFoundError as e:
        raise InvalidProjectStructure("Unable to find task-definition")

    # Find service.yml/json/yaml or service/
    try:
        service = _find_td_ser(project_path, tp="service")
    except FileNotFoundError as e:
        raise InvalidProjectStructure("Unable to find service definition")

    # if values == None then look for values.yml/yaml/json
    if values is None:
        try:
            values = _find_values(project_path)
        except FileNotFoundError as e:
            raise InvalidProjectStructure("Unable to find values for interpolation")
    else:
        # Deal with project files loading
        if values.__class__ != list:
            raise Exception('Invalid input variable values. Expecting list type!')
        
        # Lets validate input list
        ep = [os.path.exists(x) for x in values]
        if not all(ep):
            raise InvalidInputFiles

    # Return clean paths to task-definition and value files
    return (td, service, values)

