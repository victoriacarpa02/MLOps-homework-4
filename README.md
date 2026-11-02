# MLOps Homework 4

I used a trained model to predict taxi trip duration.
I ran predictions locally and in Docker, then saved the results as Parquet files.

## Results

| Question | Result | Answer |
| --- | --- | --- |
| Q1 | March prediction standard deviation: 6.247489 | 6.24 |
| Q2 | Output size: 68,558,004 bytes, 65.38 MiB | 66M |
| Q3 | Convert the notebook to a Python script | Command below |
| Q4 | First scikit-learn hash | Hash below |
| Q5 | April mean predicted duration: 14.292283 minutes | 14.29 |
| Q6 | May mean predicted duration in Docker: 0.191744 minutes | 0.19 |

Q3 command:

```powershell
.\.venv\Scripts\python.exe -m nbconvert --to script .\starter.ipynb
```

Q4 hash for scikit-learn 1.5.0:

```text
sha256:057b991ac64b3e75c9c04b5f9395eaf19a6179244c089afdebaad98264bff37c
```

The Docker task uses the model included in the provided base image.
This is a different model from the local model.

## Setup

I used Windows, PowerShell, uv and Docker Desktop with Linux containers.

Local Python version: 3.10.20.
Container Python version: 3.10.13.
Pipenv version: 2024.4.1.

Run all commands from the project folder.

```powershell
uv python install 3.10.20

$env:PIPENV_VENV_IN_PROJECT = "1"
$env:PIPENV_IGNORE_VIRTUALENVS = "1"
$env:PIPENV_PYTHON = uv python find 3.10.20

uvx --python 3.10.20 pipenv@2024.4.1 sync --dev
```

## Run the notebook

```powershell
.\.venv\Scripts\python.exe -m jupyterlab
```

Open `starter.ipynb` and run the cells for March 2023.

## Run locally

The script takes a year and a month.

```powershell
.\.venv\Scripts\python.exe .\starter.py 2023 4
```

It downloads the monthly data and saves predictions in `output`.

## Run in Docker

Start Docker Desktop, then build the image:

```powershell
docker build -t taxi-duration:hw4 .
```

Run predictions for May 2023:

```powershell
New-Item -ItemType Directory -Path .\output -Force
$outputPath = (Resolve-Path .\output).Path

docker run --rm --mount "type=bind,source=$outputPath,target=/app/output" taxi-duration:hw4 2023 5
```

The output file stays in the local `output` folder after the container exits.

## Notes

Each output file contains `ride_id` and `predicted_duration`.
Files are saved with pyarrow, without compression or the dataframe index.

Generated data and the virtual environment are excluded from Git.

[Homework instructions](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2025/04-deployment/homework.md)