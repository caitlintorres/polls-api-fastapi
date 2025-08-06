from typing import List, Dict
from schemas import Poll, Option

# In-memory "database"
polls: Dict[int, Poll] = {}
poll_counter = 1
option_counter = 1
