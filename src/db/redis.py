# import aioredis
import redis.asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600

token_blacklist = redis.StrictRedis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0
)


# note that we wont be storing tokens but instead we store the JTI.
async def add_jti_to_blacklist(jti: str, expiry: int) -> None:
    await token_blacklist.setex(name=jti, value="blacklisted", time=expiry)



# check if the token exist in blacklist
async def token_in_blacklist(jti:str) -> bool:
    jti = await token_blacklist.get(name=jti)

    return jti is not None

async def remove_jti_from_blacklist(jti: str) -> None:
    await token_blacklist.delete(jti)

    return None
