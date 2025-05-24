import aiohttp

class KinesisProApi:
    def __init__(self, url, api_key, client_id):
        self.url = url
        self.api_key = api_key
        self.client_id = client_id

    async def get_location_feed(self, sequence: int, offset: int, limit: int) -> dict:
        # path = f"data/feeds/telemetry/{client_id}?sequence={sequence}&offset={offset}&limit={limit}"
        path = f"data/feeds/location/{self.client_id}?sequence={sequence}&offset={offset}&limit={limit}"
        print(offset, sequence)
        headers = {
            'x-api-key': self.api_key
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/{path}", headers=headers) as response:
                return await response.json()