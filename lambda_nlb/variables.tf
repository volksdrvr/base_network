# variable "environment" {
#   description = "The environment which to fetch the configuration for."
#   type        = object ({
#       lb_dns_name = string,
#       hello_mars = string
#   })
# }



variable "lambda_buckets" {
  description = "List of string for each bucket needed. We need '1' per port and a utility bucket."
  type        = list(string)
  default     = ["utility", "80", "443", "8080"]
}

variable "project_name" {
  description = "The common name used for the project"
  type        = string
  default     = "re-pointer"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

