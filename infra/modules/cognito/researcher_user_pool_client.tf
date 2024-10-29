resource "aws_cognito_user_pool_client" "researcher_user_pool_client" {
  name         = "researcher-user-pool-client"
  user_pool_id = aws_cognito_user_pool.researcher_user_pool.id

  generate_secret = true
  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]
}
