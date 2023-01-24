import requests
from argparse import ArgumentParser


def submit_tx(address, author, content):
    post_object = {
        'author': author,
        'content': content,
    }
    # Submit a transaction
    server_interfece = "/new_transaction"
    response = requests.post(f"{address}{server_interfece}",
                  json=post_object,
                  headers={'Content-type': 'application/json'})
    return response.json()


if __name__ == "__main__":
    ip = "http://127.0.0.1"
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    parser.add_argument('-a', '--author', default="hdk", help='who are you')
    parser.add_argument('-d', '--data', default="hhhhh",  help='send data')
    args = parser.parse_args()
    port = args.port
    author = args.author
    data = args.data
    url = f"{ip}:{port}"
    res = submit_tx(url, author, data)
    print(res)
