import os

print("Hello World from SageMaker Processing!")

input_path = "/opt/ml/processing/input/input.txt"
output_path = "/opt/ml/processing/output/output.txt"

# Read input from S3-mounted path
with open(input_path, "r") as f:
    content = f.read()

print("Read from S3:", content)

# Write output
with open(output_path, "w") as f:
    f.write("Processed content:\n")
    f.write(content)
