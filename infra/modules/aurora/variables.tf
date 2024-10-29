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

variable "db_subnet_group_name" {
  type        = string
  description = "The name of the subnet group to use for the database."
}

variable "vpc_security_group_ids" {
  type        = list(string)
  description = "The security group IDs to use for the database."
}
