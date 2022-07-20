## DynamoDB Performance Testing -- Consistency lag

This directory contains code for testing consistency lag on DynamoDB tables. It aims to get a rough sense of how likely it is you'll get ["read-your-writes" behavior](https://jepsen.io/consistency/models/read-your-writes) (though not guarantees!) from both DynamoDB main tables and global secondary indexes.

In testing, a Lambda function attempts to write an item to a table and then read the item back. It allows you to add a configurable delay between the write and the read to test the probabilities of seeing the most recent update with various levels of delay.

Additional notes on [DynamoDB eventual consistency can be found here](https://alexdebrie.com/posts/dynamodb-eventual-consistency/#dealing-with-the-effects-of-eventual-consistency).

**Contents:**

- [Usage](#usage)
- [Results](#results)

## Usage

All performance tests are performed on AWS Lambda. The tests are deployed using the [Serverless Framework](https://github.com/serverless/serverless). You will need the Serverless Framework installed to deploy.

Once you have the Serverless Framework installed, you can replicate with the following steps:

1. Clone this repository and install dependencies

   Run the following command:

   ```bash
   git clone git@github.com:alexdebrie/dynamodb-performance-testing.git && cd dynamodb-performance-testing/consistency-performance
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

|            | 0 millisecond delay | 10 millisecond delay | 100 millisecond delay |
| ---------- | ------------------- | -------------------- | --------------------- |
| Main table | 99.50%              | 99.68%               | 100.00%               |
| GSI        | 96.54%              | 99.53%               | 99.72%                |

The rows down the left side show the target of the operation -- the main table or the GSI. The columns across the top show the amount of client-side delay between receiving the write and making the read request. Each value shows the percentage of times that the updated item was returned for the given target and delay combination.

Strong caveats in play here -- I only tested 5,000 instances of each configuration, and this is during standard operation. Results may vary widely.

In general, I would expect behavior on the main table to be fairly well-bounded even in worse times. Two of the three nodes have to accept the write for it to succeed, and reading from either of those will essentially give a strongly consistent write. Additionally, the third node shouldn't be far behind given it was sent the write operation at the same time as the other replica.

The story is more complicated with global secondary indexes, and I would expect a broader range of replication lag there. Seconds would not be uncommon, and even a delay of a minute or more is possible.

Use these numbers as a rule of thumb in good times, not a promise!
