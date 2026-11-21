import json
from typing import Any, Optional
from redis import Redis

class RedisClient:
    def __init__(
        self,
        engine: Redis,
        expire_seconds: Optional[int] = None
    ):
        self._engine = engine
        self._expire = expire_seconds


    def set(
        self,
        key: str,
        data: Any,
        expire: Optional[int] = None,
    ) -> None:
        if not isinstance(data, (int, str)):
            data = json.dumps(data)

        self._engine.set(key, data, expire)
    
    def get(
        self,
        key: str
    ) -> Any:
        res = self._engine.get(key)

        if res is None:
            return None

        return json.loads(res)
    

    def exists(
        self,
        key: str
    ) -> bool:
        return self._engine.exists(key)


    def delete(
        self,
        key: str
    ) -> None:
        self._engine.delete(key)