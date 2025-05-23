import math


class Processor:
    def __init__(self, kinesis_pro_api, data_mapper, asset_count, count_per_group):
        self.kinesis_pro_api = kinesis_pro_api
        self.data_mapper = data_mapper
        self.asset_count = asset_count
        self.count_per_group = count_per_group
        self.groups = []

        for i in range(0, math.ceil(self.asset_count / self.count_per_group)):
            self.groups.append({
                "sequence": 0,
                "limit": self.count_per_group,
                "offset": i * self.count_per_group
            })

    async def poll(self):
        for group in self.groups:
            resp = await self.kinesis_pro_api.get_location_feed(group["sequence"], group["offset"], group["limit"])
            
            count = resp["count"]
            sequence = resp["sequence"]
            items = resp["items"]

            for item in items:
                await self.data_mapper.store(item)

            group["sequence"] = sequence
