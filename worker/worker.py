import time
import random
import os

def process_task():
    while True:
        print(f"Worker processing task - {os.environ.get('HOSTNAME', 'unknown')}")
        time.sleep(30)

if __name__ == '__main__':
    process_task()
