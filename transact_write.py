import os
import timeit

from aws_embedded_metrics import metric_scope

from utils import get_client, make_transact_items, exception_wrapper

COUNT = int(os.environ['TRANSACT_ITEM_COUNT'])
FAIL = True if os.environ['FAIL'].lower() == 'true' else False


@metric_scope
def handler(event, context, metrics):
    client = get_client()
    metrics.set_namespace('DynamoDB Performance Testing')
    metrics.put_dimensions({"Operation": f"TransactWriteItems -- {COUNT} items, Failure {FAIL}"})
    for i in range(10):
        wrapped = exception_wrapper(client.transact_write_items, **make_transact_items(COUNT, FAIL))
        latency = timeit.timeit(wrapped, number=1)
        metrics.put_metric("Latency", latency * 1000, "Milliseconds")