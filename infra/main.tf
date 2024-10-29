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
