resource "aws_cognito_user_pool" "researcher_user_pool" {
  name = "researcher-user-pool"

  alias_attributes = ["email", "preferred_username"]

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
    email_subject        = "Account Confirmation"
    email_message        = "Your confirmation code is {####}"
  }

  schema {
    attribute_data_type = "String"
    name                = "email"
    required            = true
    mutable             = true
  }

  tags = {
    Name        = "researcher-user-pool"
    Project     = "researcher"
    Owner       = "cloud"
    Environment = "production"
  }
}
