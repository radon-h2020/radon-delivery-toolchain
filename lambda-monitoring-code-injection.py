import boto3
import os
import sys
import time
import psutil
import threading
from prometheus_client import CollectorRegistry, Histogram, Gauge, Summary, push_to_gateway
from PIL import Image

s3_client = boto3.client('s3')

''' 
Lambda function for thumbnail generation
Gets image from "<bucket>", stores in "<bucket>-resized". Both buckets must exist for smooth execution.
Set thumbnail sizes in THUMBNAIL_SIZES_PX
'''
THUMBNAIL_SIZES_PX = [100, 160, 200]

def gather_metrics_data(registry):

  # Create our collectors
  ram_metric = Gauge("memory_usage_bytes", "Memory usage in bytes.",)
  cpu_metric = Gauge("cpu_usage_percent", "CPU usage percent.",)

  # register the metric collectors
  registry.register(ram_metric)
  registry.register(cpu_metric)
  print("[CODE INJECTED]: gather_metrics_data function is triggered")

  while True:
    # Start gathering metrics every second
    time.sleep(0.1)

    # Add ram metrics
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    ram_metric.set(ram.used)
    # Add cpu metrics
    for c, p in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
      cpu_metric.set(p)

    # send metrics to central monitoring dashboard
    push_to_gateway('radondashboard.ddns.net:9091',
                    job='image_resize', registry=registry)
    if stop_threads:
      print("[CODE INJECTED]: Treads are succesfully terminated")
      break


def resize_image(original_img_path, resized_img_path, new_size_px):
  print("[CODE INJECTED]: function resize_image is triggered")

  with Image.open(original_img_path) as image:
    ratio = max(image.size) / float(new_size_px)
    image.thumbnail(tuple(int(x / ratio) for x in image.size))
    image.save(resized_img_path)


def lambda_handler(event, context):
  # Create the registry
  registry = CollectorRegistry()
  thread = threading.Thread(target=gather_metrics_data, args=(registry, ))
  stop_threads = False
  thread.start()

  # actual lambda handler code
  for record in event['Records']:
    bucket = record['s3']['bucket']['name']
  key = record['s3']['object']['key']
  original_img = '/tmp/original-{}'.format(key)
  temp_img = '/tmp/temp-{}'.format(key)

  s3_client.download_file(bucket, key, original_img)

  for size_px in THUMBNAIL_SIZES_PX:
    resize_image(original_img, temp_img, size_px)
    new_name_key = key.replace(".jpg", "_"+str(size_px)+".jpg")
    s3_client.upload_file(
        temp_img, '{}-resized'.format(bucket), new_name_key)

  stop_threads = True
  thread.join()