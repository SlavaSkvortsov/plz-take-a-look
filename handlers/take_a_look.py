from dataclasses import dataclass

from redis_utils import get_redis_client
from types import UserID


@dataclass
class TakeALookHandler:
    user_id: UserID
    workspace_id: str

    async def handle(self) -> UserID:
        async with get_redis_client() as redis:
            dev_ids_str = (await redis.hget(self.key, 'dev_ids')).decode()
            dev_ids = dev_ids_str.split(',')
            index = int(await redis.hget(self.key, 'index') or 0)
            try:
                result = UserID(dev_ids[index])
            except IndexError:
                result = UserID(dev_ids[0])
                new_index = 1
            else:
                new_index = index + 1

            await redis.hset(self.key, 'index', new_index)

        return result

    @property
    def key(self) -> str:
        return f'{self.workspace_id}:{self.user_id}'
