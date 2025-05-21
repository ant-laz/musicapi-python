# musicapi-python
A demo API for a fictional music application written in Python

## demo overview

![Diagram of the demo architecture.](/images/api_demo_architectcure.png)

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
developer_email = "YOUR_EMAIL_ADDRESS"
```

Run the following command to initialize Terraform:
```shell
terraform init
```

Run the following command to apply the Terraform configuration.
```shell
terraform apply
```

### Set up environment variables

navigate up to the root of the repository
```shell
cd ..
```

execute the bash script, created by terraform, to make some env vars
```shell
source scripts/00_set_variables.sh
```

### Insert dummy data into the Terraformed Spanner Instance + Database

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

```sql
        INSERT INTO 
        Albums (AlumbId, Name, ReleaseDate) 
        VALUES 
        (1, "Thriller", "1982-11-29"),
        (2, "The Dark Side of the Moon", "1973-03-01"),
        (3, "21", "2011-01-24"),
        (4, "Abbey Road", "1969-09-26"),
        (5, "Nevermind", "1991-09-24"),
        (6, "Rumours", "1977-02-04"),
        (7, "Lemonade", "2016-04-23"),
        (8, "Back in Black", "1980-07-25"),
        (9, "The Miseducation of Lauryn Hill", "1998-08-25"),
        (10, "Purple Rain", "1984-06-25");
```

```sql
        INSERT INTO 
        Labels (LabelId, Name, FoundedInDate)
        VALUES
        (1, "Universal Music Group", "1934-01-01"),
        (2, "Sony Music Entertainment", "1929-01-01"),
        (3, "Warner Music Group", "1958-01-01"),
        (4, "EMI", "1931-01-01"),
        (5, "BMG", "2008-01-01"),
        (6, "Beggars Group", "1977-01-01"),
        (7, "Concord", "1995-01-01"),
        (8, "Believe Digital", "2005-01-01"),
        (9, "HYBE Corporation", "2005-01-01"),
        (10, "Def Jam Recordings", "1984-01-01");
```

### Use Cloud Build to create a Docker Image, push to artifact registry & deploy on cloud run

Ensure you are at the root directory of the project, the same level as the Dockefile.

Submit the Dockerfile to Cloud Build to:
 - create a Docker Image
 - push the Docker Image to Artifact Registry
 - deploy the Docker Image from Artifact Registry to Cloud Run

```shell
gcloud builds submit \
--config cloudbuild.yaml \
--region ${LOCATION}  \
--default-buckets-behavior REGIONAL_USER_OWNED_BUCKET \
--substitutions=_CODE_REPO_NAME="${_CODE_REPO_NAME}",_IMAGE_NAME="${_IMAGE_NAME}",_IMAGE_TAG="${_IMAGE_TAG},_SERVICE_ACCOUNT_EMAIL=${SERVICE_ACCOUNT_EMAIL},_SPANNER_INSTANCE_ID=${SPANNER_INSTANCE_ID},_SPANNER_DATABASE_ID=${SPANNER_DATABASE_ID}"
```

