from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../tete-426803-fcea6282bee1.json"
storage_client = storage.Client()
buckets = list(storage_client.list_buckets())

print(buckets)