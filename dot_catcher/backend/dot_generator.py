from kafka import KafkaProducer
import json, random, time
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

GRID_SIZE = 5
EVENT_TYPES = ["dot_appeared", "dot_moved", "dot_disappeared"]

try:
    while True:
        event = {
            "event_type": random.choice(EVENT_TYPES),
            "position": [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)],
            "timestamp": datetime.now().isoformat()
        }
        producer.send("dots", value=event)
        print("Event sent:", event)
        time.sleep(random.uniform(0.5, 2.0))
except KeyboardInterrupt:
    print("Stopping dot generator...")
    producer.flush()
    producer.close()
