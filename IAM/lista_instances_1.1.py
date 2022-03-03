#!/usr/bin/env python

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Baseado no original https://github.com/googleapis/python-compute/blob/HEAD/samples/snippets/quickstart.py
que apresenta uma forma de incluir, listar e deletar intâncias de vm usando uma conta de serviço no Google Cloud mas
foi simplificado para apenas mostrar todas as instâncias de vm de um projeto.

Contribuições de Jorge Roque Matias com o trecho:
    from google.oauth2 import service_account
    # JRM loads Auth key-file
    credentials = service_account.Credentials.from_service_account_file(key)

    aqui encontrado nsa linhas 93 e 96

e de Rogério Lopes com o trecho:
    compute_v1.InstancesClient(credentials=credentials)

    na linha 61.
"""

import re
import sys

import typing

import google.cloud.compute_v1 as compute_v1



# [START compute_instances_list_all]
def list_all_instances(
    project_id: str,
    credentials: str
) -> typing.Dict[str, typing.Iterable[compute_v1.Instance]]:
    """
    Return a dictionary of all instances present in a project, grouped by their zone.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
    Returns:
        A dictionary with zone names as keys (in form of "zones/{zone_name}") and
        iterable collections of Instance objects as values.
    """
    instance_client = compute_v1.InstancesClient(credentials=credentials)
    # Use the `max_results` parameter to limit the number of results that the API returns per response page.
    request = compute_v1.AggregatedListInstancesRequest(
        project=project_id, max_results=5
    )
    agg_list = instance_client.aggregated_list(request=request)
    all_instances = {}
    print("Instances found:")
    # Despite using the `max_results` parameter, you don't need to handle the pagination
    # yourself. The returned `AggregatedListPager` object handles pagination
    # automatically, returning separated pages as you iterate over the results.
    for zone, response in agg_list:
        if response.instances:
            all_instances[zone] = response.instances
            print(f" {zone}:")
            for instance in response.instances:
                print(f" - {instance.name} ({instance.machine_type})")
    return all_instances


# [END compute_instances_list_all]




def main(project_id: str, credentials: str) -> None:

    all_instances = list_all_instances(project_id, credentials)
    print(f"Instancias encontradas no projeto: {project_id}:")
    for i_zone, instances in all_instances.items():
        print(f"{i_zone}:", ", ".join(i.name for i in instances))


if __name__ == "__main__":
    import uuid
    import google.auth
    import google.auth.exceptions
    from google.oauth2 import service_account

    key = "c:\\gcp\\mission1-340818-4043c9ca12c6.json"
    credentials = service_account.Credentials.from_service_account_file(key)

    try:
        default_project_id = google.auth.load_credentials_from_file(key)[1]
        print(default_project_id)
    except google.auth.exceptions.DefaultCredentialsError:
        print(
            "Please use `gcloud auth application-default login` "
            "or set GOOGLE_APPLICATION_CREDENTIALS to use this script."
        )
    else:
        main(default_project_id, credentials)