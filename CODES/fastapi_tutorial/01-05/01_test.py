from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


from pydantic import BaseModel


class User(BaseModel):
    id: int  # 整型字段，必填
    name: str = "John Doe"  # 默认值
    signup_ts: datetime | None
    friends: List[int] = []


external_data = {"id": "123", "signup_ts": "2019-06-01 12:22", "friends": [1, 2, "3"]}

user = User(**external_data)
print(user.id)  #  123
print(user.signup_ts)  # 2019-06-01 12:22:00
print(
    user.model_dump()
)  # {'id': 123, 'name': 'John Doe', 'signup_ts': datetime.datetime(2019, 6, 1, 12, 22), 'friends': [1, 2, 3]}
