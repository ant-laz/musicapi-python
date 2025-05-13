# musicapi-python
A demo API for a fictional music application written in Python

## How to execute this solution on Google Cloud

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

In spanner studio execute the following SQL to populate our database table with some records
```sql
        INSERT INTO 
        Singers (SingerId, FirstName, LastName, BirthDate) 
        VALUES 
        (1, "Freddie", "Mercury", "1946-09-05"),
        (2, "Aretha", "Franklin", "1942-03-25"),
        (3, "Michael", "Jackson", "1958-08-29"),
        (4, "Whitney", "Houston", "1963-08-09"),
        (5, "Elvis", "Presley", "1935-01-08"),
        (6, "Madonna", "Ciccone", "1958-08-16"),
        (7, "Stevie", "Wonder", "1950-05-13"),
        (8, "Frank", "Sinatra", "1915-12-12"),
        (9, "Beyoncé", "Knowles-Carter", "1981-09-04"),
        (10, "Adele", "Adkins", "1988-05-05"),
        (11, "Ed", "Sheeran", "1991-02-17"),
        (12, "Taylor", "Swift", "1989-12-13"),
        (13, "Harry", "Styles", "1994-02-01"),
        (14, "Dua", "Lipa", "1995-08-22"),
        (15, "Sam", "Smith", "1992-05-19");
```

### Use Cloud Build to create a Docker Image

Ensure you are at the root directory of the project, the same level as the Dockefile.

Submit the Dockerfile to Cloud Build to create a Docker Image on Artifact Registry

```shell
gcloud builds submit \
--config cloudbuild.yaml \
--region europe-west2
```

### Use Cloud Build to execute a Docker Container

Submit the Docker image, on Artifact Registry, to Cloud Run which executes a Docker Container of it.

```shell
gcloud run deploy musicapipython \
--image europe-west2-docker.pkg.dev/zaro-joonix-net-prj-app-dev/musicapipython/api-image:tag1 \
--region europe-west2 \
--allow-unauthenticated
```

Image 'europe-west2-docker.pkg.dev/zaro-joonix-net-prj-app-dev/musicapipython/api-image:tag1' not found.

## How to execute this app locally

https://cloud.google.com/run/docs/testing/local

```shell
gcloud auth configure-docker europe-west2-docker.pkg.dev
```

```shell
PORT=8080 && docker run -p 9090:${PORT} -e PORT=${PORT} europe-west2-docker.pkg.dev/zaro-joonix-net-prj-app-dev/musicapipython/api-image:tag1
```