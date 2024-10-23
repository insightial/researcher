output "user_pool_id" {
  value       = aws_cognito_user_pool.researcher_user_pool.id
  description = "ID of the Cognito User Pool"
}

output "user_pool_arn" {
  value       = aws_cognito_user_pool.researcher_user_pool.arn
  description = "ARN of the Cognito User Pool"
}

output "user_pool_client_id" {
  value       = aws_cognito_user_pool_client.researcher_user_pool_client.id
  description = "ID of the Cognito User Pool Client"
}
