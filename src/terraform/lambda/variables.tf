variable "region" {
  default = "sa-east-1"
}

variable "lambda_name" {
  default = "ml-api"
}

variable "ecr_repo_name" {
  default = "ml-lambda"
}

variable "version_image" {
  default = "v0.0.5"
}