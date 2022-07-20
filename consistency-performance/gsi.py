from aws_embedded_metrics import metric_scope

from utils import test_gsi

@metric_scope
def handler(event, context, metrics):
    delay = (event["delay"] or 0) / 1000
    print(f"Running with delay of {delay}")
    metrics.set_namespace("DynamoDB Performance Testing")
    metrics.put_dimensions(
        {"Operation": f"Consistency -- GSI with {delay} second delay"}
    )
    attempts = 0
    matches = 0
    for _ in range(10):
        matched = test_gsi(delay)
        if matched:
            matches += 1
        attempts += 1

    metrics.put_metric("Matches", matches, "Count")
    metrics.put_metric("Attempts", attempts, "Count")
