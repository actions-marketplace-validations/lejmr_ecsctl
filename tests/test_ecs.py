from moto import mock_ecs
from ecs.ecs import install_or_update_task_definition, _compare_dicts, install_service
import os
from botocore.exceptions import ParamValidationError, UnsupportedS3AccesspointConfigurationError
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


def test_compare_dict9():
    import datetime
    current = {'placementConstraints': [], 
               'taskDefinitionArn': 'arn:aws:ecs:us-east-1:657399224926:task-definition/website_DEV:45', 
               'requiresAttributes': [{'name': 'com.amazonaws.ecs.capability.logging-driver.awslogs'}, {'name': 'com.amazonaws.ecs.capability.ecr-auth'}, {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.19'}, {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.21'}, {'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.18'}], 
               'registeredAt': datetime.datetime(2021, 7, 28, 15, 58, 19, 630000), 
               'status': 'ACTIVE', 'revision': 45, 'volumes': [], 
               'compatibilities': ['EXTERNAL', 'EC2'], 
               'registeredBy': 'arn:aws:iam::657399224926:user/mkozak', 
               'containerDefinitions': [
                   {
                       'mountPoints': [], 
                       'essential': True, 
                       'dockerLabels': {'traefik.http.middlewares.dev__website__test_redirect.redirectregex.regex': '^.*', 'traefik.http.routers.dev__website__test_redirect.middlewares': 'dev__website__test_redirect', 'traefik.enable': 'true', 'traefik.http.routers.dev__website__test_frontend.priority': '1', 'traefik.http.middlewares.dev__website__test_redirect.redirectregex.replacement': 'http://dev-website-test.nonprod-internal.finmason.com/', 'traefik.http.routers.dev__website__test_redirect.rule': '', 'traefik.http.routers.dev__website__test_frontend.rule': 'Host(`dev-website-test.nonprod-internal.finmason.com`)'}, 
                       'name': 'frontend', 
                       'image': '657399224926.dkr.ecr.us-east-1.amazonaws.com/website:0.0.18', 
                       'cpu': 0, 
                       'memoryReservation': 128, 
                       'logConfiguration': {'options': {'awslogs-group': '/DEV/generic_frontend/', 'awslogs-stream-prefix': 'website_test', 'awslogs-region': 'us-east-1'}, 
                       'logDriver': 'awslogs'}, 
                       'portMappings': [{'hostPort': 0, 'containerPort': 80, 'protocol': 'tcp'}], 
                       'environment': [{'value': '/mail', 'name': 'MAILER_URL'}, {'value': '', 'name': 'TRACKING_ID'}, {'value': 'ke', 'name': 'RECAPTCHA_SITEKEY'}, {'value': 'http://dev-website-cms-test.nonprod-internal.finmason.com', 'name': 'CMS_URL'}], 
                       'volumesFrom': []
                    }, 
                    {
                        'mountPoints': [], 
                        'environment': [{'value': 'https://api.sendgrid.com/v3/mail/send', 'name': 'API_SEND_URL'}, {'value': 'dsadsa', 'name': 'API_KEY'}, {'value': 'd-blank', 'name': 'CONTACT_TEMPLATE_ID'}, {'value': 'ktetervak@finmason.com', 'name': 'GENERAL_EMAIL'}, {'value': 'blank', 'name': 'RECAPTCHA_SECRET_KEY'}, {'value': 'ktetervak@finmason.com', 'name': 'REQUEST_EMAIL'}, {'value': 'dsadsa', 'name': 'REQUEST_TEMPLATE_ID'}, {'value': 'ktetervak@finmason.com', 'name': 'ERROR_EMAIL'}, {'value': 'ke', 'name': 'RECAPTCHA_SITEKEY'}], 
                        'image': '657399224926.dkr.ecr.us-east-1.amazonaws.com/website/mailer:0.0.18', 
                        'dockerLabels': {'traefik.http.routers.dev__website__test_mailer.rule': 'Host(`dev-website-test.nonprod-internal.finmason.com`) && PathPrefix(`/mail/`)', 'traefik.http.routers.dev__website__test_mailer.priority': '100', 'traefik.enable': 'true'}, 
                        'name': 'mailer', 
                        'memoryReservation': 256, 
                        'logConfiguration': {'options': {'awslogs-group': '/DEV/generic_frontend/', 'awslogs-stream-prefix': 'website_mailer_test', 'awslogs-region': 'us-east-1'}, 
                        'logDriver': 'awslogs'}, 
                        'volumesFrom': [], 
                        'command': ['node', 'server.js'], 
                        'essential': True, 'cpu': 0, 
                        'portMappings': [{'hostPort': 0, 'containerPort': 8080, 'protocol': 'tcp'}]
                    }, 
                    {
                        'mountPoints': [], 
                        'essential': True, 
                        'dockerLabels': {'traefik.http.routers.dev__website__test_wp_content.priority': '100', 'traefik.http.routers.dev__website__test_wp_content.rule': 'Host(`dev-website-test.nonprod-internal.finmason.com`) && PathPrefix(`/wp-content/`)', 'traefik.enable': 'true'}, 
                        'name': 'wp_content', 
                        'image': 'pottava/s3-proxy', 
                        'cpu': 0, 
                        'memoryReservation': 256, 
                        'logConfiguration': {'options': {'awslogs-group': '/DEV/generic_frontend/', 'awslogs-stream-prefix': 'website_mailer_test', 'awslogs-region': 'us-east-1'}, 
                        'logDriver': 'awslogs'}, 'portMappings': [{'hostPort': 0, 'containerPort': 80, 'protocol': 'tcp'}], 
                        'environment': [{'value': 'https://api.sendgrid.com/v3/mail/send', 'name': 'API_SEND_URL'}, {'value': 'dsadsa', 'name': 'API_KEY'}, {'value': 'd-blank', 'name': 'CONTACT_TEMPLATE_ID'}, {'value': 'ktetervak@finmason.com', 'name': 'GENERAL_EMAIL'}, {'value': 'blank', 'name': 'RECAPTCHA_SECRET_KEY'}, {'value': 'ktetervak@finmason.com', 'name': 'REQUEST_EMAIL'}, {'value': 'dsadsa', 'name': 'REQUEST_TEMPLATE_ID'}, {'value': 'ktetervak@finmason.com', 'name': 'ERROR_EMAIL'}, {'value': 'ke', 'name': 'RECAPTCHA_SITEKEY'}], 
                        'volumesFrom': []}
                    ], 
                'family': 'website_DEV'}
    update = {'family': 'website_DEV', 
              'containerDefinitions': [
                  {
                      'environment': [{'name': 'RECAPTCHA_SITEKEY', 'value': 'ke'}, {'name': 'MAILER_URL', 'value': '/mail'}, {'name': 'CMS_URL', 'value': 'http://dev-website-cms-test.nonprod-internal.finmason.com'}, {'name': 'TRACKING_ID', 'value': ''}], 'cpu': 0, 'portMappings': [{'protocol': 'tcp', 'hostPort': 0, 'containerPort': 80}], 'dockerLabels': {'traefik.http.routers.dev__website__test_redirect.rule': '', 'traefik.http.middlewares.dev__website__test_redirect.redirectregex.regex': '^.*', 'traefik.http.routers.dev__website__test_redirect.middlewares': 'dev__website__test_redirect', 'traefik.http.routers.dev__website__test_frontend.priority': '1', 'traefik.http.routers.dev__website__test_frontend.rule': 'Host(`dev-website-test.nonprod-internal.finmason.com`)', 'traefik.http.middlewares.dev__website__test_redirect.redirectregex.replacement': 'http://dev-website-test.nonprod-internal.finmason.com/', 'traefik.enable': 'true'}, 'name': 'frontend', 'memoryReservation': 128, 'image': '657399224926.dkr.ecr.us-east-1.amazonaws.com/website:0.0.18', 'logConfiguration': {'logDriver': 'awslogs', 'options': {'awslogs-stream-prefix': 'website_test', 'awslogs-group': '/DEV/generic_frontend/', 'awslogs-region': 'us-east-1'}}}, {'environment': [{'name': 'API_KEY', 'value': 'dsadsa'}, {'name': 'API_SEND_URL', 'value': 'https://api.sendgrid.com/v3/mail/send'}, {'name': 'REQUEST_EMAIL', 'value': 'ktetervak@finmason.com'}, {'name': 'GENERAL_EMAIL', 'value': 'ktetervak@finmason.com'}, {'name': 'ERROR_EMAIL', 'value': 'ktetervak@finmason.com'}, {'name': 'REQUEST_TEMPLATE_ID', 'value': 'dsadsa'}, {'name': 'CONTACT_TEMPLATE_ID', 'value': 'd-blank'}, {'name': 'RECAPTCHA_SITEKEY', 'value': 'ke'}, {'name': 'RECAPTCHA_SECRET_KEY', 'value': 'blank'}], 'command': ['node', 'server.js'], 'cpu': 0, 'portMappings': [{'protocol': 'tcp', 'hostPort': 0, 'containerPort': 8080}], 'dockerLabels': {'traefik.http.routers.dev__website__test_mailer.rule': 'Host(`dev-website-test.nonprod-internal.finmason.com`) && PathPrefix(`/mail/`)', 'traefik.http.routers.dev__website__test_mailer.priority': '100', 'traefik.enable': 'true'}, 'name': 'mailer', 'memoryReservation': 256, 'image': '657399224926.dkr.ecr.us-east-1.amazonaws.com/website/mailer:0.0.18', 'logConfiguration': {'logDriver': 'awslogs', 'options': {'awslogs-stream-prefix': 'website_mailer_test', 'awslogs-group': '/DEV/generic_frontend/', 'awslogs-region': 'us-east-1'}}}, {'environment': [{'name': 'API_KEY', 'value': 'dsadsa'}, {'name': 'API_SEND_URL', 'value': 'https://api.sendgrid.com/v3/mail/send'}, {'name': 'REQUEST_EMAIL', 'value': 'ktetervak@finmason.com'}, {'name': 'GENERAL_EMAIL', 'value': 'ktetervak@finmason.com'}, {'name': 'ERROR_EMAIL', 'value': 'ktetervak@finmason.com'}, {'name': 'REQUEST_TEMPLATE_ID', 'value': 'dsadsa'}, {'name': 'CONTACT_TEMPLATE_ID', 'value': 'd-blank'}, {'name': 'RECAPTCHA_SITEKEY', 'value': 'ke'}, {'name': 'RECAPTCHA_SECRET_KEY', 'value': 'blank'}], 'cpu': 0, 'portMappings': [{'protocol': 'tcp', 'hostPort': 0, 'containerPort': 80}], 'dockerLabels': {'traefik.http.routers.dev__website__test_wp_content.priority': '100', 'traefik.http.routers.dev__website__test_wp_content.rule': 'Host(`dev-website-test.nonprod-internal.finmason.com`) && PathPrefix(`/wp-content/`)', 'traefik.enable': 'true'}, 'name': 'wp_content', 'memoryReservation': 256, 'image': 'pottava/s3-proxy', 'logConfiguration': {'logDriver': 'awslogs', 'options': {'awslogs-stream-prefix': 'website_mailer_test', 'awslogs-group': '/DEV/generic_frontend/', 'awslogs-region': 'us-east-1'}}}]}
    assert _compare_dicts(current, update)

def test_compare_dict9a():
    current = {
        "a": [
            {"name": "a", "value": "a"},
            {"name": "b", "value": "b"},
            {"name": "c", "value": "c"}
        ]
    }
    update = {
        "a": [
            {"name": "b", "value": "b"},
            {"name": "a", "value": "a"},
            {"name": "c", "value": "c"}
        ]
    }
    assert _compare_dicts(current, update)

def test_compare_dict9a1():
    current = {
        "a": [
            {"name": "a", "value": "a"},
            {"name": "b", "value": "b"},
            {"name": "c", "value": "c"}
        ]
    }
    update = {
        "a": [
            {"name": "b", "value": "b"},
            {"name": "a", "value": "a1"},
            {"name": "c", "value": "c"}
        ]
    }
    assert not _compare_dicts(current, update)

#### Service management
@mock_ecs
def test_service_create():

    # Create a cluster and task-definition
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    client = boto3.client('ecs')
    clusterName = "testCluster"
    client.create_cluster(clusterName=clusterName)

    # Create a new task definition
    arn_t = install_or_update_task_definition({
        'family': 'test',
        'containerDefinitions': [
            {
                "name": "main_app"
            }
        ]
        })
    
    # 
    arn_s = install_service({
        "serviceName": "testService",
        "cluster": clusterName,
        "desiredCount": 1,
        "taskDefinition": ""
    }, arn_t)

    # Validate state
    assert arn_s in client.list_services(cluster=clusterName)['serviceArns']


@mock_ecs
def test_service_update():

    # Create a cluster and task-definition
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    client = boto3.client('ecs')
    clusterName = "testCluster"
    client.create_cluster(clusterName=clusterName)

    # Create a new task definition and service
    arn_t = install_or_update_task_definition({
        'family': 'test',
        'containerDefinitions': [
            {
                "name": "main_app"
            }
        ]
        })
    arn_s = install_service({
        "serviceName": "testService",
        "cluster": clusterName,
        "desiredCount": 1,
        "taskDefinition": ""
    }, arn_t)

    # Update td and service
    arn_t2 = install_or_update_task_definition({
        'family': 'test2',
        'containerDefinitions': [
            {
                "name": "main_app",
                "image": "nginx"
            }
        ]
        })
    arn_s = install_service({
        "serviceName": "testService",
        "cluster": clusterName,
        "desiredCount": 1,
    }, arn_t2)

    # Validate state
    assert arn_s in client.list_services(cluster=clusterName)['serviceArns']
    s = client.describe_services(cluster=clusterName, services=[arn_s])['services'][0]
    assert s['taskDefinition'] == arn_t2