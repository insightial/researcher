resource "aws_rds_cluster" "user_db_cluster" {
  cluster_identifier      = "user-db-cluster"
  engine                  = "aurora-postgresql"
  engine_mode             = "serverless"
  master_username         = var.db_username
  master_password         = var.db_password
  database_name           = var.db_name
  backup_retention_period = 7
  preferred_backup_window = "07:00-09:00"

  scaling_configuration {
    auto_pause               = true
    max_capacity             = 2
    min_capacity             = 2
    seconds_until_auto_pause = 300 # Auto pause after 5 minutes of inactivity
  }

  db_subnet_group_name   = var.db_subnet_group_name
  vpc_security_group_ids = var.vpc_security_group_ids

  skip_final_snapshot = true


  tags = {
    Name        = "user-db-cluster"
    Project     = "researcher"
    Owner       = "DataEngg"
    Environment = "Production"
  }
}
