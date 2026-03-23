provider "aws" {
  region = var.region
}

data "aws_caller_identity" "current" {}

# ---------------------------
# ECR
# ---------------------------
resource "aws_ecr_repository" "repo" {
  name = var.ecr_repo_name
}

# ---------------------------
# IAM Role Lambda
# ---------------------------
resource "aws_iam_role" "lambda_exec" {
  name = "lambda-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# ---------------------------
# DynamoDB
# ---------------------------
resource "aws_dynamodb_table" "sobreviventes" {
  name         = "sobreviventes"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "PassengerId"

  attribute {
    name = "PassengerId"
    type = "N"
  }
}

# Permissão DynamoDB
resource "aws_iam_role_policy" "lambda_dynamo" {
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:Scan",
        "dynamodb:DeleteItem"
      ]
      Resource = aws_dynamodb_table.sobreviventes.arn
    }]
  })
}

# ---------------------------
# Lambda (ECR)
# ---------------------------
locals {
  image_uri = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com/${var.ecr_repo_name}:latest"
}

resource "aws_lambda_function" "lambda" {
  function_name = var.lambda_name

  package_type = "Image"
  image_uri    = local.image_uri

  role = aws_iam_role.lambda_exec.arn

  timeout      = 30
  memory_size  = 512
}

# ---------------------------
# API Gateway (OpenAPI)
# ---------------------------
resource "aws_api_gateway_rest_api" "api" {
  name = "ml-api"

  body = templatefile("${path.module}/openapi.yaml", {
    region      = var.region
    lambda_arn  = aws_lambda_function.lambda.arn
  })
}

# Deploy
resource "aws_api_gateway_deployment" "deploy" {
  depends_on = [aws_api_gateway_rest_api.api]

  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_stage" "stage" {
  stage_name    = "dev"
  rest_api_id   = aws_api_gateway_rest_api.api.id
  deployment_id = aws_api_gateway_deployment.deploy.id
}

# ---------------------------
# Permissão Lambda ← API Gateway
# ---------------------------
resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "apigateway.amazonaws.com"
}