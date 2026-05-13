variable "aws_region" {
  default = "us-east-1"
}

variable "project" {
  default = "flask-taskmanager"
}

variable "cluster_name" {
  default = "devops-eks"
}

variable "jenkins_instance_type" {
  default = "t3.micro"
}

variable "eks_node_instance_type" {
  default = "t3.micro"
}

variable "eks_desired_nodes" {
  default = 2
}

variable "eks_min_nodes" {
  default = 1
}

variable "eks_max_nodes" {
  default = 3
}
