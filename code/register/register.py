import os
from os.path import relpath
import azureml
import argparse
from pathlib2 import Path
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import ContainerImage, Image
from azureml.core.webservice import Webservice, AciWebservice
from azureml.core.authentication import ServicePrincipalAuthentication 

def info(msg, char = "#", width = 75):
    print("")
    print(char * width)
    print(char + "   %0*s" % ((-1*width)+5, msg) + char)
    print(char * width)

def run(model_path, model_name, tenant_id, service_principal_id,
        service_principal_password, subscription_id, resource_group, workspace):
    auth_args = {
        'tenant_id': tenant_id,
        'service_principal_id': service_principal_id,
        'service_principal_password': service_principal_password
    }

    ws_args = {
        'auth': ServicePrincipalAuthentication(**auth_args),
        'subscription_id': subscription_id,
        'resource_group': resource_group
    }

    ws = Workspace.get(workspace, **ws_args)

    print(ws.get_details())

    print('\nSaving model {} to {}'.format(model_path, model_name))

    # Model Path needs to be relative
    model_path = relpath(model_path, '.')

    model = Model.register(ws, model_name=model_name, model_path=model_path)
    print('Done!')

if __name__ == "__main__":
    # argparse stuff for model path and model name
    parser = argparse.ArgumentParser(description='sanity check on model')
    parser.add_argument('-b', '--base_path', help='directory to base folder', default='..')
    parser.add_argument('-m', '--model', help='path to model file', default='/model/latest.h5')
    parser.add_argument('-n', '--model_name', help='AML Model name', default='tacosandburritos')
    parser.add_argument('-t', '--tenant_id', help='tenant_id')
    parser.add_argument('-s', '--service_principal_id', help='service_principal_id')
    parser.add_argument('-p', '--service_principal_password', help='service_principal_password')
    parser.add_argument('-u', '--subscription_id', help='subscription_id')
    parser.add_argument('-r', '--resource_group', help='resource_group')
    parser.add_argument('-w', '--workspace', help='workspace')
    args = parser.parse_args()
    
    print('Azure ML SDK Version: {}'.format(azureml.core.VERSION))
    args.model = 'model/' + args.model
    model_path = str(Path(args.base_path).resolve(strict=False).joinpath(args.model).resolve(strict=False))
    rgs = {
        'model_path': model_path,
        'model_name': args.model_name,
        'tenant_id': args.tenant_id,
        'service_principal_id': args.service_principal_id,
        'service_principal_password': args.service_principal_password,
        'subscription_id': args.subscription_id,
        'resource_group': args.resource_group,
        'workspace': args.workspace
    }

    # printing out args for posterity
    for i in rgs:
        if i == 'service_principal_password':
            print('{} => **********'.format(i))
        else:
            print('{} => {}'.format(i, rgs[i]))

    run(**rgs)

    # python register.py --model_path v --model_name c --tenant_id c
    # --service_principal_id v --service_principal_password v
    # --subscription_id v --resource_group x --workspace c
