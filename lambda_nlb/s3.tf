

# resource "aws_s3_bucket" "lambda_bucket" {
#   count  = length(var.lambda_buckets)
#   bucket = "lambda-${var.project_name}-${var.lambda_buckets[count.index]}"

#   acl           = "private"
#   force_destroy = true

#   # versioning {
#   #   enabled = true
#   # }
#   # logging {
#   #   target_bucket = aws_s3_bucket.log_bucket.id
#   #   target_prefix = "log/"
#   # }
# }

# resource "aws_s3_bucket_public_access_block" "lambda_bucket" {
#   count  = length(var.lambda_buckets)
#   bucket = aws_s3_bucket.lambda_bucket[count.index].id

#   block_public_acls   = true
#   block_public_policy = true
# }
