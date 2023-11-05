import socket

from views import index, blog

from icecream import ic

ic.configureOutput(includeContext=True)

URLS = {
    r"/": index,
    r"/blog": blog,
}


def parse_request(request: str) -> tuple:
    parsed = request.split(' ')
    method = parsed[0]
    assert len(parsed) > 1, f"{request=} {parsed=}"
    url = parsed[1]
    return method, url


def generate_headers(method: str, url: str) -> tuple:
    if not method == "GET":
        return 'HTTP/1.1 405 Method not allowed\n\n', 405

    if url not in URLS:
        return 'HTTP/1.1 404 Page not found\n\n', 404

    return 'HTTP/1.1 200 OK\n\n', 200


def generate_content(code: str, url: str) -> str:
    if code == 404:
        return '<h1>404 Not found</h1>'
    elif code == 405:
        return '<h1>Method not allowed</h1>'
    return URLS[url]()


def generate_response(request: str) -> str:
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)
    ic(method, url, headers, code, body)
    return (headers + body).encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 5000))
    server_socket.listen()

    while True:

        client_socket, addr = server_socket.accept()
        # When retrieving a socket option, or setting it, you specify the option name as well as the level.
        # When level = SOL_SOCKET, the item will be searched for in the socket itself.
        # Т.е. речь идет о этом нашем сокете
        # Допустить переиспользование адреса SO_REUSEADDR, value = 1, or True
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        request = client_socket.recv(1024)

        # print(request.decode('utf-8'))
        print(f"{request=}")
        print()
        print(f"{addr=}")

        response = generate_response(request.decode('utf-8'))

        # Ответ клиенту
        client_socket.sendall(response)
        client_socket.close()


if __name__ == "__main__":
    run()
