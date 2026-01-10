terraform{
    required_providers{
        aws={
            source="hashicorp/aws"
            version = "~>3.0"
        }
    }
}

provider "aws" {
region = "us-east-1"
}

resource "aws_instance" "example" {
  ami = "ami-07ff62358b87c7116" # Amazon Linux 
  instance_type = "t3.micro"
}