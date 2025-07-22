from govesb.esb import (
    DataFormatEnum, ESBHelper
)
import requests

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
