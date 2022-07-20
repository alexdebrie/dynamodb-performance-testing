import timeit

from aws_embedded_metrics import metric_scope

from utils import get_client, make_put_item, wrapper


@metric_scope
def handler(event, context, metrics):
    client = get_client()
    metrics.set_namespace('DynamoDB Performance Testing')
    metrics.put_dimensions({"Operation": "PutItem"})
    for i in range(10):
        wrapped = wrapper(client.put_item, **make_put_item())
        latency = timeit.timeit(wrapped, number=1)
        metrics.put_metric("Latency", latency * 1000, "Milliseconds")