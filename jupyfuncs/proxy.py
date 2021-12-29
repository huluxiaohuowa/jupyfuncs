import requests


def get_proxy():
    return requests.get("http://172.20.0.9:5010/get/?type=https").json().get("proxy")


def get_proxies(https=False):
    http_proxy = requests.get("http://172.20.0.9:5010/get/").json().get("proxy")
    https_proxy = requests.get("http://172.20.0.9:5010/get/?type=https").json().get("proxy")
    if https:
        proxy_dict = {
            'http': f'http://{https_proxy}',
            'https': f'https://{https_proxy}'
        }
    else:
        proxy_dict = {
            'http': f'http://{http_proxy}',
            'https': f'https://{http_proxy}'
        }
    return proxy_dict