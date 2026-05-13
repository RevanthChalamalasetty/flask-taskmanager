terraform {
  backend "s3" {
    bucket  = "devops-tf-state-486336528116"
    key     = "flask-taskmanager/terraform.tfstate"
    region  = "us-east-1"
    profile = "devops"
  }
}
