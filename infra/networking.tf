resource "aws_vpc" "researcher_vpc" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name    = "researcher_vpc"
    Project = "researcher"
    Owner   = "DataEngg"
  }
}

resource "aws_subnet" "researcher_subnet1" {
  vpc_id                  = aws_vpc.researcher_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name    = "researcher_subnet1"
    Project = "researcher"
    Owner   = "DataEngg"
  }
}

resource "aws_subnet" "researcher_subnet2" {
  vpc_id                  = aws_vpc.researcher_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name    = "researcher_subnet2"
    Project = "researcher"
    Owner   = "DataEngg"
  }
}

resource "aws_db_subnet_group" "researcher_db_subnet_group" {
  name = "researcher-db-subnet-group"
  subnet_ids = [
    aws_subnet.researcher_subnet1.id,
    aws_subnet.researcher_subnet2.id
  ]

  tags = {
    Name    = "researcher_db_subnet_group"
    Project = "researcher"
    Owner   = "DataEngg"
  }
}

resource "aws_security_group" "researcher_db_security_group" {
  name        = "researcher_db_security_group"
  description = "Security group for Researcher"
  vpc_id      = aws_vpc.researcher_vpc.id

  # Inbound rules
  # Allow SSH (port 22) from everywhere by default
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow PostgreSQL (port 5432) from everywhere
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow Redshift (port 5439) from everywhere
  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTP (port 80) from everywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTPS (port 443) from everywhere
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound rules
  # Allow all outbound traffic by default
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "researcher_security_group"
    Project = "researcher"
    Owner   = "DataEngg"
  }
}

resource "aws_internet_gateway" "researcher_igw" {
  vpc_id = aws_vpc.researcher_vpc.id

  tags = {
    Name    = "researcher_igw"
    Project = "researcher"
    Owner   = "DataEngg"
  }
}

resource "aws_route_table" "researcher_route_table" {
  vpc_id = aws_vpc.researcher_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.researcher_igw.id
  }

  tags = {
    Name    = "researcher_route_table"
    Project = "researcher"
    Owner   = "DataEngg"
  }
}

resource "aws_route_table_association" "researcher_assoc_subnet1" {
  subnet_id      = aws_subnet.researcher_subnet1.id
  route_table_id = aws_route_table.researcher_route_table.id
}

resource "aws_route_table_association" "researcher_assoc_subnet2" {
  subnet_id      = aws_subnet.researcher_subnet2.id
  route_table_id = aws_route_table.researcher_route_table.id
}
