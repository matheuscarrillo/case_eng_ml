provider "aws" {
  region = var.region
}

data "aws_lambda_function" "lambda" {
  function_name = "ml-api"
}

# ---------------------------
# API Gateway (OpenAPI)
# ---------------------------
resource "aws_api_gateway_rest_api" "api" {
  name = "ml-api"

  body = templatefile("${path.module}/openapi.yaml", {
    region      = var.region
    lambda_arn  = data.aws_lambda_function.lambda.arn
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
  function_name = data.aws_lambda_function.lambda.function_name
  principal     = "apigateway.amazonaws.com"
}