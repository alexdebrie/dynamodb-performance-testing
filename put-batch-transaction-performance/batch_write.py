import os
import timeit

from aws_embedded_metrics import metric_scope

from utils import get_client, make_batch_items, wrapper

COUNT = int(os.environ['BATCH_ITEM_COUNT'])


@metric_scope
def handler(event, context, metrics):
    client = get_client()
    metrics.set_namespace('DynamoDB Performance Testing')
    metrics.put_dimensions({"Operation": f"BatchWriteItem -- {COUNT} items"})
    for i in range(10):
        wrapped = wrapper(client.batch_write_item, **make_batch_items(COUNT))
        latency = timeit.timeit(wrapped, number=1)
        metrics.put_metric("Latency", latency * 1000, "Milliseconds")