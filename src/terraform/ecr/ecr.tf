provider "aws" {
  region = var.region
}

# ---------------------------
# ECR
# ---------------------------
resource "aws_ecr_repository" "repo" {
  name = var.ecr_repo_name
}
