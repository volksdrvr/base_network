terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.48.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.2.0"
    }
  }

  required_version = "~> 1.0"
}

provider "aws" {
  region = "us-west-2"
}

locals {
  environment = terraform.workspace
}

#
# Fetch variables based on Environment\Workspace.
#
module "vars" {
#   count       = terraform.workspace != "default" ? 1 : 0
  source      = "./modules/vars"
  environment = local.environment
}

# data "aws_lb" "nlb" {
#   tags = {"internal_alb_dns_name" = "lb-foo-myezbrew-dev"}
# }

data "archive_file" "lambda_hello_world" {
  type = "zip"

  source_dir  = "${path.module}/populate_nlb_tg_with_alb_python3"
  output_path = "${path.module}/populate_nlb_tg_with_alb_python3.zip"
}

resource "aws_s3_bucket_object" "lambda_hello_world" {
  bucket = "lambda-re-pointer-utility"

  key    = "populate_nlb_tg_with_alb_python3.zip"
  source = data.archive_file.lambda_hello_world.output_path

  etag = filemd5(data.archive_file.lambda_hello_world.output_path)
}