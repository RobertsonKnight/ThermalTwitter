from datetime import datetime, timezone, timedelta
import time

a = datetime.now(timezone.utc).replace(microsecond=0)
b = a - timedelta(seconds=30)
print(a.isoformat())
print(b.isoformat())