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

# govesb_public_key = "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEon0az66Kz+6ZIz4G7La8uPeSbOT/E/suRjNMgFQ4isjJwFXaS20vHcndEFxXz8M68sbxkbLrGuNS/wFcEzubWQ=="
govesb_public_key = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE7rWxM3ScEpFBeNyhuMi5GG+Jp1U9v8mED5xWxxKJ6qP6ODvIUPd2SpzAO7PbyMZ7cig0iTOwVYQZThCuHLVtn2A=="
system_private_key = "MD4CAQAwEAYHKoZIzj0CAQYFK4EEAAoEJzAlAgEBBCA+WSlrAHLF9SVtOzHu1QucdBCOkxcaYnP0Pwyntw4vYA=="

sample_data = '''
{"data":{
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
},"signature":"MEUCIQDxN3MiBmeO1g2zD3M2Ncw3wQGynTCcWCBv+Lsq4HVc6wIgXZTx6RrplPVAXqpWMP7V7HDKZ5NvjDkBiIu5UDe2Rvw="}'''

responseData = ESBHelper.verify_and_extract_data(sample_data, DataFormatEnum.JSON, govesb_public_key)


if responseData.has_data and responseData is None:
    print("Signature Verification Failed")
    # body = ESBHelper2.create_response("{}", DataFormatEnum.JSON, system_private_key, False, "Signature Verification Failed")
else:
    print("sample payload", responseData.verified_data)
    response = requests.post(url=destination_url, data=responseData.verified_data, auth=(destination_username, destination_password))
```

## Sample to Send Data to GovESB

[//]: # (* fsdf)

[//]: # ()
[//]: # (- fsdf)

[//]: # (- dfsf)

[//]: # (- dsf)

[//]: # ()
[//]: # (`fsdffsdf)

[//]: # (fdsf)

[//]: # (fsdf)

[//]: # (fsdf`)

[//]: # ()
```fsaddssads```

[//]: # (```asdadsa```)

[//]: # (```dasda```)

[//]: # (```dasdfs```)

[//]: # ()
[//]: # (| s)

[//]: # ()
[//]: # ( fsdfsf)

[//]: # ()
[//]: # (& dsa)