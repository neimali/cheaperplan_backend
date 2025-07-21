import asyncio
from app.utils.reminder import push_same_message 

if __name__ == "__main__":
    asyncio.run(push_same_message())
