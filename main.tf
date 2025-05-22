provider "aws" {
  region     = "us-east-1"
}

resource "aws_instance" "devops_app" {
  ami                    = "ami-0c02fb55956c7d316"
  instance_type          = "t2.micro"
  key_name               = "chave-ssh"
  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io docker-compose git
              git clone https://github.com/seuusuario/CRUD-Carrinho-Lanchonete.git
              cd CRUD-Carrinho-Lanchonete
              docker-compose up -d
              EOF

  tags = {
    Name = "devops-carrinho"
  }
}
