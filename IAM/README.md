# Módulos I e II - Visão geral e IAM

Módulo I: princípios básicos do Google Cloud Platform com objetivo na certificação Google Cloud Engineer Associate.
Módulo II: IAM (Identity and Access Management) permite a administradores o controle de acesso em nível empresarial dos recursos em Nuvem GCP.

## Scripts disponíveis

No diretório você encontra os seguintes scripts Python usando a SDK do GCP:

### `lista_storage.py`

Com a variável de memória GOOGLE_APPLICATION_CREDENTIALS setada para o arquivo JSON com as chaves de acesso do projeto alvo, apresenta os Buckets contidos no projeto. 

### `lista_instances_1.1.py`

Script baseado no original [quickstart.py](https://github.com/googleapis/python-compute/blob/HEAD/samples/snippets/quickstart.py) que permite a listagem das instâncias de VM de todas as zonas GCP de um projeto.

### `quickstart.py`

Script Python que cria, lista e deleta instâncias de VM de uma determinada zona e projeto.