resource "aws_instance" "web" {
  ami           = "ami-0427090fd1714268b"
  subnet_id = aws_subnet.public_subnet.id
  instance_type = "t2.micro"
  associate_public_ip_address = true
  vpc_security_group_ids = ["aws_security_group.allow_tls.id"]

  tags = {
    Name = "Kademia web"
  }
}