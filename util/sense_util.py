#!/usr/bin/env python3

import argparse
import sys
import os
import json

from sense.client.workflow_combined_api import WorkflowCombinedApi
from sense.client.profile_api import ProfileApi

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    operations = parser.add_mutually_exclusive_group()
    operations.add_argument("-c", "--create", action="store_true",
                            help="create service instance (requires one of optional -f, optional -u)")
    operations.add_argument("-d", "--delete", action="store_true",
                            help="cancel and delete service instance (requires -u)")
    operations.add_argument("-D", "--delete-only", action="store_true",
                            help="delete service instance (requires -u)")
    operations.add_argument("-s", "--status", action="store_true",
                            help="get service instance status (requires -u)")
    operations.add_argument("-p", "--profile", action="store_true",
                            help="describe a service profile (requires -u)")
    parser.add_argument("-f", "--file", action="append",
                        help="service intent request file")
    parser.add_argument("-u", "--uuid", action="append",
                        help="service profile uuid or instance uuid")
    parser.add_argument("-n", "--name", action="append",
                        help="service instance alias name")

    args = parser.parse_args()

    if args.create:
        if args.uuid:
            # create by straight profile
            intent = {'profileID': args.uuid[0]}
            if args.name:
                intent['alias'] = args.name[0]
            workflowApi = WorkflowCombinedApi()
            workflowApi.instance_new()
            response = workflowApi.instance_create(json.dumps(intent))
            print(response)
        elif args.file:
            workflowApi = WorkflowCombinedApi()
            workflowApi.instance_new()
            if not os.path.isfile(args.file[0]):
                raise Exception('request file not found: %s' % args.file[0])
            intent_file = open(args.file[0])
            intent = json.load(intent_file)
            if args.name:
                intent['alias'] = args.name[0]
            intent_file.close()
            response = workflowApi.instance_create(json.dumps(intent))
            print(response)
            workflowApi.instance_operate('provision', sync='true')
            status = workflowApi.instance_get_status()
            print(f'provision status={status}')
    elif args.delete:
        if args.uuid:
            workflowApi = WorkflowCombinedApi()
            workflowApi.instance_operate('cancel', si_uuid=args.uuid[0], sync='true')
            status = workflowApi.instance_get_status(si_uuid=args.uuid[0])
            print(f'cancel status={status}')
            if 'CANCEL - READY' in status:
                workflowApi.instance_delete(si_uuid=args.uuid[0])
            else:
                print(f'cancel operation disrupted - instance not deleted - contact admin')
        else:
            raise ValueError("Missing the required parameter `uuid` ")
    elif args.delete_only:
        if args.uuid:
            workflowApi = WorkflowCombinedApi()
            workflowApi.instance_delete(si_uuid=args.uuid[0])
        else:
            raise ValueError("Missing the required parameter `uuid` ")
    elif args.profile:
        if args.uuid:
            profileApi = ProfileApi()
            profile = profileApi.profile_describe(args.uuid[0])
            print(json.dumps(json.loads(profile), indent=2))
        else:
            raise ValueError("Missing the required parameter `uuid` ")
    elif args.status:
        if args.uuid:
            workflowApi = WorkflowCombinedApi()
            status = workflowApi.instance_get_status(si_uuid=args.uuid[0])
            print(status)
        else:
            raise ValueError("Missing the required parameter `uuid` ")