variable "region" {
  default = "us-east-1"
}

variable "public_key_path" {
  default = "~/.ssh/id_rsa.pub"
}

variable "docker_image" {
  description = "The Docker image to use for the EC2 instance"
  type        = string
}
