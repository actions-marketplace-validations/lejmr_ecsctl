import boto3


# Compare td and des['taskDefinition']
def _compare_dicts(incumbent, updateting):

    # This variable defines how to match members of a list while default id is name
    matching_pattern = {
        'portMappings': 'containerPort',
        'environmentFiles': 'type',
        'mountPoints': 'sourceVolume',
        'volumesFrom': 'sourceContainer',
        'devices': 'hostPath',
        'tmpfs': 'containerPath',
        'dependsOn': 'containerName',
        'extraHosts': 'hostname',
        'systemControls': 'namespace',
        'resourceRequirements': 'value',
        'placementConstraints': 'type',
        'inferenceAccelerators': 'deviceName',
        'tags': 'key'
    }


    # Get all keys
    current_keys = incumbent.keys()

    # Compare updating items with current values
    for k,v in updateting.items():

        # Simple test on key level
        if not k in current_keys:
            return False
        
        # k is even in the current, so lets compare values
        if v.__class__ == dict:

            # Only compare if both are dicts
            if incumbent[k].__class__ != dict:
                return False

            # Compare two nested dicts
            r = _compare_dicts(incumbent[k], v)
            if not r: return False
            continue
        
        # Compare two list
        if v.__class__ == list:
            # Only compare if both are lists
            if incumbent[k].__class__ != list:
                return False
            
            # Different lenght of lists will cause td update
            if len(v) != len(incumbent[k]):
                return False

            # Compare plain lists
            if v[0].__class__ != dict and v != incumbent[k]:
                return False
            
            # Match dicts - this is brutal implementation, and should be improved over time because
            # there are some parts of task definition this implementation might not work perfect.
            matching_id = matching_pattern.get(k, "name")
            fn = list(filter(lambda x: matching_id in x.keys(), v))
            if len(fn) != 1:
                return False
            fc = list(filter(lambda x: matching_id in x.keys() and x[matching_id] == fn[0][matching_id], incumbent[k]))
            if len(fc) != 1:
                return False
            if not _compare_dicts(dict(fc[0]), dict(fn[0])):
                return False

            # Stop evaluation
            continue
        
        # Compare values of simple types
        if v != incumbent[k]:
            return False
    
    # All the items are the same
    return True

    
def install_or_update_task_definition(td, force_update=False):
    # Setup connection to ECS interface
    client = boto3.client('ecs')

    # Verify the TD already exits
    a = client.list_task_definition_families()
    update = td['family'] in a.get('families', [])

    # Verify td is different compared to the current task definition revision
    if not force_update and update:
        des = client.describe_task_definition(taskDefinition=td['family'])
        if _compare_dicts(des['taskDefinition'], td):
            return des['taskDefinition']['taskDefinitionArn']
        
    # Register a new task definition
    return client.register_task_definition(**td)['taskDefinition']['taskDefinitionArn']

    
def install_service(sd, td_arn):
    """ 
    Function for installation of service which deals with the rendered service 
    definition and 
    """
    pass