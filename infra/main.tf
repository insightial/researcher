terraform {
  backend "s3" {
    bucket = "researcher-tf-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

module "cognito" {
  source = "./modules/cognito"
}

module "s3" {
  source = "./modules/s3"
}

module "aurora" {
  source = "./modules/aurora"

  vpc_security_group_ids = [aws_security_group.researcher_db_security_group.id]
  db_subnet_group_name   = aws_db_subnet_group.researcher_db_subnet_group.name
  db_name                = var.db_name
  db_username            = var.db_username
  db_password            = var.db_password
}
