# musicapi-python
A demo API for a fictional music application written in Python

## How to execute this solution

### Set up an environment on Google Cloud using Terraform

Life is short, so let's use Terraform to first set up an env on Google Cloud.

Change the working directory to the terraform folder

```shell
cd terraform
```

Create a file named terraform.tfvars

```shell
touch terraform.tfvars
```

Add the following configuration variables to the file, with your own values.

```shell
billing_account = "YOUR_BILLING_ACCOUNT"
organization = "YOUR_ORGANIZATION_ID"
project_create = true/false
project_id = "YOUR_PROJECT_ID"
region = "YOUR_GCP_LOCATION"
```

Run the following command to initialize Terraform:
```shell
terraform init
```

Run the following command to apply the Terraform configuration.
```shell
terraform apply
```


## setup

ensure you are using python 3.11 or higher

active a virual environment

```shell
python -m venv venv
```

install the rewquirements for the project

```shell
pip install -r requirements.txt
```

## launch development server

```shell
fastapi dev main.py
```
