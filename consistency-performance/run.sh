FUNCTIONS=("mainTable" "gsi")

CONFIGS=("config/zero.json" "config/ten.json" "config/hundred.json")

for function in "${FUNCTIONS[@]}"
do
    for config in "${CONFIGS[@]}"
    do
        echo "Executing $function with $config..."
        for i in `seq 500`; do sls invoke -f $function --path $config; done
        echo "Done executing $function with $config."
    done
done
