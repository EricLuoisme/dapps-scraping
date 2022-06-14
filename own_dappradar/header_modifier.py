from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.parser import HttpParser
from typing import Optional


class BasicAuthorizationPlugin(HttpProxyBasePlugin):
    """Modifies request headers."""

    def before_upstream_connection(
            self, request: HttpParser) -> Optional[HttpParser]:
        return request

    def handle_client_request(
            self, request: HttpParser) -> Optional[HttpParser]:
        request.add_header('Referer'.encode('utf-8'), 'https://dappradar.com/rankings/2'.encode('utf-8'))
        return request

    def on_upstream_connection_close(self) -> None:
        pass

    def handle_upstream_chunk(self, chunk: memoryview) -> memoryview:
        return chunk
