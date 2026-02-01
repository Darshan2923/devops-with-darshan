
# SageMaker Processing Job – Hello World (Step-by-Step Guide)

This README explains **exactly** how to create and run a **SageMaker Processing Job** that:
- Runs a Python script (Hello World)
- Reads data from Amazon S3
- Writes output back to Amazon S3
- Uses **no notebooks** and **no custom containers**

This is the **correct foundation** for building validation pipelines (e.g., COBOL → Python accuracy checks).

---

## Why Processing Jobs (Notebooks vs Processing Jobs)

We use **SageMaker Processing Jobs** instead of notebooks because:
- They are **deterministic** (same input → same output)
- They are **stateless and reproducible**
- They are **auditable** (CloudWatch logs + S3 artifacts)
- They are **automation-ready** (CI/CD, Step Functions)

Notebooks are for experimentation only.  
Processing jobs are for **production-grade batch logic**.

---

## Prerequisites

- AWS account
- IAM role with:
  - `AmazonSageMakerFullAccess`
  - `AmazonS3FullAccess`
- An S3 bucket (example used below):
  ```
  s3://my-sagemaker-processing-demo/
  ```

---

## Step 1: Prepare S3 Folder Structure

Create the following structure in S3:

```
s3://my-sagemaker-processing-demo/
├── code/
│   └── hello_world.py
├── input/
│   └── input.txt
└── output/
```

### input.txt
```
Hello from S3
```

---

## Step 2: Create the Processing Script

Create a file called `hello_world.py` with the following content:

```python
import os

print("HELLO FROM SAGEMAKER PROCESSING JOB")

os.makedirs("/opt/ml/processing/output", exist_ok=True)

with open("/opt/ml/processing/output/output.txt", "w") as f:
    f.write("Job ran successfully\n")

print("OUTPUT FILE WRITTEN")
```

⚠️ IMPORTANT:
- Do **not** import `sagemaker`
- Do **not** call `get_execution_role()`
- Processing jobs already run under an IAM role

Upload this file to:

```
s3://my-sagemaker-processing-demo/code/hello_world.py
```

---

## Step 3: Create the Processing Job (Console)

1. Open **AWS Console**
2. Search for **Amazon SageMaker AI**
3. Do **NOT** open Studio
4. In the left sidebar:
   - Click **Processing**
   - Click **Processing jobs**
   - Click **Create processing job**

---

## Step 4: Job Settings

| Field | Value |
|------|------|
| Job name | `hello-world-processing` |
| IAM role | Your SageMaker execution role |

---

## Step 5: Container Configuration

Paste this **AWS-managed prebuilt container**:

```
683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3
```

This container:
- Is free to use
- Includes Python, Pandas, NumPy
- Requires no Docker knowledge

---

## Step 6: Instance Configuration

| Field | Value |
|------|------|
| Instance type | `ml.t3.medium` |
| Instance count | `1` |

`ml.t3.medium` is the cheapest option and Free-Tier eligible (if your account qualifies).

---

## Step 7: Configure Processing Inputs

### Input 1 – Code
| Field | Value |
|------|------|
| Input name | `code` |
| S3 URI | `s3://my-sagemaker-processing-demo/code/hello_world.py` |
| Local path | `/opt/ml/processing/code` |

### Input 2 – Data
| Field | Value |
|------|------|
| Input name | `input-data` |
| S3 URI | `s3://my-sagemaker-processing-demo/input/` |
| Local path | `/opt/ml/processing/input` |

---

## Step 8: Configure Processing Output

| Field | Value |
|------|------|
| Output name | `output-data` |
| Local path | `/opt/ml/processing/output` |
| S3 URI | `s3://my-sagemaker-processing-demo/output/` |

⚠️ SageMaker only uploads files from declared output paths.

---

## Step 9: Entrypoint and Arguments

### Entrypoint
```
python3
```

### Arguments
```
/opt/ml/processing/code/hello_world.py
```

This executes:
```
python3 /opt/ml/processing/code/hello_world.py
```

---

## Step 10: Run the Job

Click **Create processing job** and wait for status **Completed**.

---

## Step 11: Verify Logs

1. Open the job
2. Click **View logs in CloudWatch**
3. Open the latest log stream

Expected logs:
```
HELLO FROM SAGEMAKER PROCESSING JOB
OUTPUT FILE WRITTEN
```

---

## Step 12: Verify Output in S3

Check:

```
s3://my-sagemaker-processing-demo/output/output.txt
```

Expected content:
```
Job ran successfully
```

---

## What You Achieved

You successfully proved:
- SageMaker can run batch Python jobs
- S3 input/output works correctly
- Logs are captured in CloudWatch
- Jobs are reproducible and auditable

This is the **exact foundation** for:
- COBOL vs Python output comparison
- Accuracy computation (% match)
- Validation pipelines
- Bedrock + SageMaker workflows

---

## Next Steps

- Read two files (COBOL output & Python output)
- Compare values and compute accuracy %
- Write metrics.json to S3
- Fail job if accuracy < threshold
- Trigger jobs via SDK / Step Functions

---

## Key Rule to Remember

> **Notebooks orchestrate jobs.  
> Processing jobs execute logic.  
> Never mix the two.**
