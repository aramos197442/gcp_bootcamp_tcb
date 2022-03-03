from google.cloud import storage

import sys

# Autentica service account com base em arquivos de credenciais 

key = sys.argv[1]

storage_client = storage.Client.from_service_account_json(key)

# Lista Cloud Storage Buckets
buckets = list(storage_client.list_buckets())
print(buckets)
