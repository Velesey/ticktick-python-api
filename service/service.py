from datetime import datetime
from client import Client


class Service:
    client: Client

    def check_authorization_and_reconnect(self, method_name: str, response, content) -> bool:
        if response.status == 401:
            connected = self.client.reconnect()
            if not connected:
                print(f'Error in {method_name}')
                print(response)
                print(content)
                return False
            return True

        is_ok = response.status == 200
        if not is_ok:
            print(f'Error in {method_name}')
            print(response)
            print(content)
        return is_ok

    def _parse_datetime(self, dt: datetime):
        return dt.replace(microsecond=0).isoformat().replace('+00:00', '.000+0000')
