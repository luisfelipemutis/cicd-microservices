import time
import os
import sys

print("🚀 Worker service started successfully!")
print(f"📝 Running in pod: {os.environ.get('HOSTNAME', 'unknown')}")
sys.stdout.flush()

counter = 0
while True:
    counter += 1
    message = f"🔄 Worker processing task #{counter} - Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    print(message)
    sys.stdout.flush()
    time.sleep(30)
