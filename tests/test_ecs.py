from moto import mock_ecs
from ecs.ecs import install_or_update_task_definition, _compare_dicts
import os
from botocore.exceptions import ParamValidationError
import pytest
import boto3


@mock_ecs
def test_create_empty_td():
    """ This is in invalid request, as td is empty """
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    with pytest.raises(ParamValidationError):
        install_or_update_task_definition({'family': 'td'})

@mock_ecs
def test_create_a_new_td():
    """ This is in invalid request, as td is empty """
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    # Create a new task definition
    install_or_update_task_definition({
        'family': 'test',
        'containerDefinitions': [
            {
                "name": "main_app"
            }
        ]
        })
    
    # Validate the task definition has been created
    client = boto3.client('ecs')
    a = client.list_task_definition_families()
    assert 'test' in a.get('families', [])


@mock_ecs
def test_update_td():
    """ This is in invalid request, as td is empty """
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    # Create a new task definition
    arn1 = install_or_update_task_definition({
        'family': 'test',
        'containerDefinitions': [
            {
                "name": "main_app"
            }
        ]
        })
    # arn1 = tdi['taskDefinition']['taskDefinitionArn']

    # Send an update
    arn2 = install_or_update_task_definition({
        'family': 'test',
        'containerDefinitions': [
            {
                "name": "main_app",
                "image": "nginx"
            }
        ]
        })
    # arn2 = tdi['taskDefinition']['taskDefinitionArn']

    # Tests
    client = boto3.client('ecs')
    a = client.list_task_definition_families()
    assert 'test' in a.get('families', [])
    assert arn1 != arn2
    assert int(arn1.split(':')[-1]) == 1
    assert int(arn2.split(':')[-1]) == 2

@mock_ecs
def test_update_td_with_same_configuration():
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    # Create a new task definition
    arn1 = install_or_update_task_definition({
        'family': 'test',
        'containerDefinitions': [
            {
                "name": "main_app"
            }
        ]
        })
    
    # Send an update
    arn2 = install_or_update_task_definition({
        'family': 'test',
        'containerDefinitions': [
            {
                "name": "main_app"
            }
        ]
        })
    
    # Tests
    client = boto3.client('ecs')
    a = client.list_task_definition_families()
    assert 'test' in a.get('families', [])
    assert arn1 == arn2
    assert int(arn1.split(':')[-1]) == 1
    assert int(arn2.split(':')[-1]) == 1


@mock_ecs
def test_update_td_with_same_configuration_force_update():
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    # Create a new task definition
    arn1 = install_or_update_task_definition({
        'family': 'test',
        'containerDefinitions': [
            {
                "name": "main_app"
            }
        ]
        })
    
    # Send an update
    arn2 = install_or_update_task_definition({
        'family': 'test',
        'containerDefinitions': [
            {
                "name": "main_app"
            }
        ]
        }, force_update=True)
    
    # Tests
    client = boto3.client('ecs')
    a = client.list_task_definition_families()
    assert 'test' in a.get('families', [])
    assert arn1 != arn2
    assert int(arn1.split(':')[-1]) == 1
    assert int(arn2.split(':')[-1]) == 2


# helping function
def test_compare_dict1():
    assert _compare_dicts({}, {})

def test_compare_dict2():
    assert not _compare_dicts({}, {'a': 'test'})

def test_compare_dict3():
    assert _compare_dicts({'a': 'test'}, {'a': 'test'})

def test_compare_dict4():
    assert not _compare_dicts({'a': 'test'}, {'a': 'ntest'})

def test_compare_dict4():
    assert not _compare_dicts({'a': 'test'}, {'a': {'b':'test2'}})

def test_compare_dict5():
    assert not _compare_dicts({}, {'a': {'b':'test2'}})

def test_compare_dict6():
    assert _compare_dicts(
        {'taskDefinitionArn': 'arn:aws:ecs:us-east-1:123456789012:task-definition/test:1', 'containerDefinitions': [
                {'name': 'main_app', 'cpu': 0, 'portMappings': [], 'essential': True, 'environment': [], 'mountPoints': [], 'volumesFrom': []}
            ], 
            'family': 'test', 'networkMode': 'bridge', 'revision': 1, 'volumes': [], 'status': 'ACTIVE', 'placementConstraints': [], 'compatibilities': ['EC2']}, 
        {'family': 'test', 'containerDefinitions': [{'name': 'main_app'}]})

def test_compare_dict7():
    assert not _compare_dicts(
        {'taskDefinitionArn': 'arn:aws:ecs:us-east-1:123456789012:task-definition/test:1', 'containerDefinitions': [
                {'name': 'main_app', 'cpu': 0, 'portMappings': [], 'essential': True, 'environment': [], 'mountPoints': [], 'volumesFrom': []}
            ], 
            'family': 'test', 'networkMode': 'bridge', 'revision': 1, 'volumes': [], 'status': 'ACTIVE', 'placementConstraints': [], 'compatibilities': ['EC2']}, 
        {'family': 'test', 'containerDefinitions': [{'name': 'main_app_new'}]})

def test_compare_dict8():
    assert not _compare_dicts(
        {'taskDefinitionArn': 'arn:aws:ecs:us-east-1:123456789012:task-definition/test:1', 'containerDefinitions': [
                {'name': 'main_app', 'cpu': 0, 'portMappings': [], 'essential': True, 'environment': [], 'mountPoints': [], 'volumesFrom': []}
            ], 
            'family': 'test', 'networkMode': 'bridge', 'revision': 1, 'volumes': [], 'status': 'ACTIVE', 'placementConstraints': [], 'compatibilities': ['EC2']}, 
        {'family': 'test', 'containerDefinitions': [{'name': 'main_app', 'essential': False}]})