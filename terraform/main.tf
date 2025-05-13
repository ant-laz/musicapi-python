#  Copyright 2025 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

// Terraform local variables
// https://developer.hashicorp.com/terraform/language/values/locals
// to avoid repeating the same values or expr multiple times in this config
//
locals {
  repo_codename = "musicapipython"
}

// Google Cloud Project
// https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/project
// IF var.project_create = TRUE THEN project_reuse = null THEN new project made
// IF var.project_create = FALSE THEN project_reuse = {} THEN existing proj used
module "google_cloud_project" {
  source          = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/project?ref=v38.0.0"
  billing_account = var.billing_account
  project_reuse   = var.project_create ? null : {}
  name            = var.project_id
  parent          = var.organization
  services = [
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "compute.googleapis.com",
    "spanner.googleapis.com",
  ]
}

// Google Cloud Artifact Registry
// https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/artifact-registry
module "docker_artifact_registry" {
  source     = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/artifact-registry?ref=v38.0.0"
  project_id = var.project_id
  location   = var.region
  name       = local.repo_codename
  format     = { docker = { standard = {} } }
}

// Google Cloud Service Account
// https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/iam-service-account
module "api_sa" {
  source     = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/iam-service-account?ref=v38.0.0"
  project_id = module.google_cloud_project.project_id
  name       = "${local.repo_codename}-sa"
  # non-authoritative roles granted *to* the service accounts on other resources
  iam_project_roles = {
    (module.google_cloud_project.project_id) = [
      "roles/storage.objectUser",
      "roles/artifactregistry.writer",
    ]
  }
}

// Google Cloud Spanner Instance & Database
// https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/spanner-instance
module "spanner_instace" {
  source     = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/spanner-instance?ref=v38.0.0"
  project_id = var.project_id
  instance = {
    name         = "${local.repo_codename}-instance"
    display_name = "TF instance in ${var.region}"
    config = {
      name = "regional-${var.region}"
    }
    num_nodes = 1
  }
  databases = {
    musicapipython-database = {
      database_dialect = "GOOGLE_STANDARD_SQL"
      // using "heredoc" strings to express DDL cleanly across multiple lines
      // https://developer.hashicorp.com/terraform/language/expressions/strings#heredoc-strings
      ddl = [
        <<MYDDLSQL
        CREATE TABLE Singers (
          SingerId   INT64 NOT NULL,
          FirstName  STRING(1024),
          LastName   STRING(1024),
          BirthDate  DATE
        ) PRIMARY KEY(SingerId)
        MYDDLSQL
      ]
    }
  }
}
