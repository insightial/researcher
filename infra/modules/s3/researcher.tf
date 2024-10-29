resource "aws_s3_bucket" "llm_researcher" {
  bucket = "llm-researcher"

  tags = {
    Name        = "llm-researcher"
    Project     = "llm_researcher"
    Owner       = "DataEngg"
    Environment = "Production"
  }
}

resource "aws_s3_bucket_ownership_controls" "llm_researcher_ownership_controls" {
  bucket = aws_s3_bucket.llm_researcher.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "llm_researcher_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.llm_researcher_ownership_controls]

  bucket = aws_s3_bucket.llm_researcher.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "llm_researcher_versioning" {
  bucket = aws_s3_bucket.llm_researcher.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "llm_researcher_server_side_encryption_configuration" {
  bucket = aws_s3_bucket.llm_researcher.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "llm_researcher_lifecycle_configuration" {
  bucket = aws_s3_bucket.llm_researcher.id

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "GLACIER"
    }
  }
}
