output "user_pool_id" {
  value       = module.cognito.user_pool_id
  description = "ID of the Cognito User Pool"
}

output "user_pool_client_id" {
  value       = module.cognito.user_pool_client_id
  description = "ID of the Cognito User Pool Client"
}
