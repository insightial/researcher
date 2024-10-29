output "llm_researcher_bucket" {
  value = aws_s3_bucket.llm_researcher.bucket
}

output "llm_researcher_bucket_arn" {
  value = aws_s3_bucket.llm_researcher.arn
}

output "llm_researcher_bucket_id" {
  value = aws_s3_bucket.llm_researcher.id
}
