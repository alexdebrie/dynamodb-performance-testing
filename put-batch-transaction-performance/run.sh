FUNCTIONS=("putItem" "batchWriteItem5" "batchWriteItem25" "transactWriteItem5" "transactWriteItem25" "transactWriteItem5Fail")

for function in "${FUNCTIONS[@]}"
do
    echo "Executing $function..."
    for i in `seq 400`; do sls invoke -f $function; done
    echo "Done executing $function."
done
