provider "aws" {
  region = "us-east-1" # Update to your preferred region
}

resource "aws_key_pair" "deploy_key" {
  key_name   = "deploy-key"
  public_key = file("~/.ssh/id_rsa.pub") # Path to your SSH public key
}

resource "aws_security_group" "allow_http_ssh" {
  name        = "allow_http_ssh"
  description = "Allow HTTP and SSH traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow SSH from anywhere
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow HTTP traffic
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_instance" {
  ami           = "ami-0c02fb55956c7d316" # Update with an AMI ID valid for your region
  instance_type = "t2.micro"
  key_name      = aws_key_pair.deploy_key.key_name
  security_groups = [aws_security_group.allow_http_ssh.name]

  # Pass the Docker image and container setup via user_data
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y docker.io
              sudo systemctl start docker
              sudo docker run -d -p 80:80 $DOCKER_IMAGE
              EOF

  tags = {
    Name = "GitHub-Deployed-App"
  }
}

output "instance_ip" {
  value = aws_instance.app_instance.public_ip
}
