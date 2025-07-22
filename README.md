# GovESB Python Package

## Sample to Receive Data from GovESB

```

import requests
from govesb.esb import (
    DataFormatEnum, ESBHelper
)

destination_scheme = "https"
destination_host = "jsonplaceholder.typicode.com"
destination_port = "443"
destination_path = "posts"
destination_username = "system-username"
destination_password = "password"

destination_url = f"{destination_scheme}://{destination_host}:{destination_port}/{destination_path}"

# govesb_public_key = ""
govesb_public_key = "+"
system_private_key = ""

sample_data = '''
{"data":{
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
},"signature":"MEUCIQDxN3MiBmeO1g2zD3M2Ncw3wQDe2R"}'''

responseData = ESBHelper.verify_and_extract_data(sample_data, DataFormatEnum.JSON, govesb_public_key)


if responseData.has_data and responseData is None:
    print("Signature Verification Failed")
    # body = ESBHelper2.create_response("{}", DataFormatEnum.JSON, system_private_key, False, "Signature Verification Failed")
else:
    print("sample payload", responseData.verified_data)
    response = requests.post(url=destination_url, data=responseData.verified_data, auth=(destination_username, destination_password))
    
```

## Sample to Send Data to GovESB
```

from govesb.esb import (
    DataFormatEnum, ESBHelper
)

destination_scheme = "https"
destination_host = "jsonplaceholder.typicode.com"
destination_port = "443"
destination_path = "posts"

client_id = "client_id"
client_secret = "client_secret"
api_code = "api_code"
signing_key = "signing_key"
esb_token_url = "esb_token_url"
esb_request_url = "esb_request_url"

destination_url = f"{destination_scheme}://{destination_host}:{destination_port}/{destination_path}"

sample_data = {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit suscipit recusandae consequuntur expedita et starchitecto"
}

encryptedDataResponse = ESBHelper.esb_request(
    client_id=client_id,
    client_secret=client_secret,
    api_code=api_code,
    esb_body=sample_data,
    format=DataFormatEnum.JSON,
    key=signing_key,
    esb_token_url=esb_token_url,
    esb_request_url=esb_request_url,
)

print('encryptedDataResponse', encryptedDataResponse)


```