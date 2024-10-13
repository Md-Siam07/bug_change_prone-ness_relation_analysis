import os

function_call_path = "/home/mdsiam/Desktop/extension/Callgraph/cg2"

for file in os.listdir(function_call_path):
    if file.endswith(".txt"):
        # rename the file with lower
        os.rename(f"{function_call_path}/{file}", f"{function_call_path}/{file.lower()}")