terraform {
  backend "s3" {
    bucket = "researcher-tf-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
