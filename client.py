import requests


# response = requests.post(
#     'http://192.168.1.119:5000/ads/',
#     json={'heading': 'test2', 'description':'test2', 'owner':'test1'}
# )

response = requests.get(
    'http://192.168.1.119:5000/ads/9',
)

print(response.text)