## DynamoDB Performance Testing

This repository contains example code for performance testing [Amazon DynamoDB](https://aws.amazon.com/dynamodb/). You can find a full summary of the results and explanation of the methodology in a blog post on [performance testing DynamoDB](https://www.alexdebrie.com/posts/dynamodb-transactions-performance/).

**Contents:**

- [Usage](#usage)
- [Results](#results)

## Usage

All performance tests are performed on AWS Lambda. The tests are deployed using the [Serverless Framework](https://github.com/serverless/serverless). You will need the Serverless Framework installed to deploy.

Once you have the Serverless Framework installed, you can replicate with the following steps:

1. Clone this repository and install dependencies

    Run the following command:

    ```bash
    git clone git@github.com:alexdebrie/dynamodb-performance-testing.git && cd dynamodb-performance-testing
    npm install
    ```

2. Deploy the service

    Run the following command to deploy the Serverless application:

    ```bash
    serverless deploy
    ```

3. Execute the tests

    Run the following command to invoke each configuration 400 times:

    ```bash
    bash run.sh
    ```

    If you would like to invoke a subset of the functions or run less than 400 times, edit the `run.sh` file.

## Results

The basic results are as follows:

| Operation                          | Min     | p50  | p90  | p95  | p99  | Max     |
|------------------------------------|---------|------|------|------|------|---------|
| PutItem                            | 5.47    | 7.55 | 11.3 | 13.2 | 16.2 | 29      |
| BatchWrite - 5 items               | 6.59    | 8.14 | 13.3 | 15.4 | 25.5 | 56.8    |
| BatchWrite - 25 items              | 7.96    | 10.2 | 16   | 18   | 27.6 | 76.4    |
| TransactWrite - 5 items            | 19.4    | 25.3 | 30.7 | 36.4 | 92.5 | 218     |
| TransactWrite - 25 items           | 23.5    | 32.1 | 40.5 | 47.2 | 97.5 | 258     |
| TransactWrite - 5 items w/ failure | 19.8    | 25.3 | 30.6 | 34.2 | 84.9 | 254     |

In graph format:

![DynamoDB Performance Test Results chart](https://user-images.githubusercontent.com/6509926/74391973-4afcc200-4dcb-11ea-9d87-b7a80e36f442.png)

Full results and methodology are written up in the [performance testing blog post](https://www.alexdebrie.com/posts/dynamodb-transactions-performance/).