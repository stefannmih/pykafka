from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time

# Generate UUID
def generate_uuid():
    return uuid.uuid4()


# Kafka producer
client = KafkaClient(hosts="kafka-svc.kafka.svc.cluster.local:9092")
topic = client.topics['geodatafinal']
producer = topic.get_sync_producer()


# Creating data
data = {}
data['busline'] = '00003'


def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        producer.produce(message.encode('ascii'))

        time.sleep(1)
        #if bus reaches last coordinates, start from beginning
        if i == len(coordinates) - 1:
            i = 0
        else:
            i += 1

# Read coordinates from geojson
input_file = open('./data/coordinates3.json')
json_array = json.load(input_file)

# From the json create a list of coordinates
coordinates = json_array['features'][0]['geometry']['coordinates'][0]
print(coordinates)
generate_checkpoint(coordinates)

