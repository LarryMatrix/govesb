from govesb.govesb import GovEsbHelper
import requests

destination_scheme = "https"
destination_host = "jsonplaceholder.typicode.com"
destination_port = "443"
destination_path = "posts"
destination_username = "system-username"
destination_password = "password"

destination_url = f"{destination_scheme}://{destination_host}:{destination_port}/{destination_path}"


sample_data = {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}

GovEsbHelper.__init__()

encryptedData = GovEsbHelper.encrypt_ecies(str(sample_data))

print('encryptedData:', encryptedData)

# responseData = GovEsbHelper.verify_and_extract_data(sample_data, DataFormatEnum.JSON, govesb_public_key)



response = requests.post(url=destination_url, data=responseData.verified_data,
                         auth=(destination_username, destination_password))

