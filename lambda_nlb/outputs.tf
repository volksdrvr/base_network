# variable.tf outputs
# output "lambda_buckets_names_appended" {
#   description = "The values passed to define each s3 bucket"
#   value       = var.lambda_buckets
# }

# output "lambda_buckets_full_names" {
#   description = "The values passed to define each s3 bucket"
#   value       = [aws_s3_bucket.lambda_bucket.*.id]
# }

# module vars output
# output "for_keys_module_vars_env_load_balancers" {
#   description = "keys and values stored for the workspace"
#   value       = { for p in keys(module.vars.env.load_balancers) : p => module.vars.env.load_balancers[p] }
# }


# output "slected_vpc_subnet_ids" {
#   description = "data values given vpc filtered on name"
#   value       = [data.aws_subnet_ids.selected]
# }

# output "nlb_names" {
#   description = "these are the nlbs we created"
#   value       = { for p in sort(keys(module.vars.env.load_balancers)) : p => aws_lb.lb[p].name }
  
# }

# output "for_key_and_value" {
#   description = "The values passed to define each s3 bucket"
#   value       = [for key, value in module.vars.env.load_balancers : "key: ${key}"]
# }

# output "flatmerge" {
#   description = "The values passed to define each s3 bucket"
#   value       = local.flat

# }

# output "test_merge" {
#   description = "The values passed to define each s3 bucket"
#   value       = local.test_merge

# }

# output "test_for_nest" {
#   description = "The values passed to define each s3 bucket"
#   value       = local.test_for_nest

# }

# output "test_for" {
#   description = "The values passed to define each s3 bucket"
#   value       = local.test_for

# }

# output "datavaluetest_nlb_arn" {
#     value = data.aws_lb.nlb.arn
  
# }

