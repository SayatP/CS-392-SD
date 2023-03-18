# for ((n=0;n<1000;n++)); do
#     bash calls.bash &
#     bash calls.bash &
#     bash calls.bash &
#     wait
# done

# the processes should run in parallel, to increase the load you can also run this command from multiple terminals at once





# this will send all the requests crom calls.bash 10000 times with 50 parallel requests at a time
seq 1 10000 | xargs -n1 -P50 bash calls.bash
