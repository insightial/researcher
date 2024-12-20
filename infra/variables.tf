variable "aws_access_key" {}

variable "aws_secret_key" {}

variable "region" {}

variable "db_name" {
  type        = string
  description = "The name of the database to create."
}

variable "db_username" {
  type        = string
  description = "Master username for the database."
}

variable "db_password" {
  type        = string
  description = "Master password for the database."
  sensitive   = true
}
