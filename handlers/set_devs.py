from dataclasses import dataclass

from redis_utils import get_redis_client
from types import UserID


@dataclass
class SetDevsHandler:
    user_id: UserID
    workspace_id: str
    dev_ids: list[UserID]

    async def handle(self) -> None:
        async with get_redis_client() as redis:
            await redis.hset(self.key, 'dev_ids', ','.join(self.dev_ids))
            await redis.hset(self.key, 'index', 0)

    @property
    def key(self) -> str:
        return f'{self.workspace_id}:{self.user_id}'
