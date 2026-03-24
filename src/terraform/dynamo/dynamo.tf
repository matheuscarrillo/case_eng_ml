provider "aws" {
  region = var.region
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
data "aws_iam_role" "lambda_exec" {
  name = "lambda-exec-role"
}

resource "aws_iam_role_policy" "lambda_dynamo" {
  role = data.aws_iam_role.lambda_exec.name

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


