



# resource "aws_cloudformation_stack" "network" {
#   name = "myezbrew-stack"
#   parameters = {
#     InternalALBDNSName = "internal-elb-example-1353749286.us-west-2.elb.amazonaws.com"
#     # InternalALBDNSName = module.vars.environment.lb_dns_name
#     ALBListenerPort = "443"
#     CWMetricFlagIPCount = "True"
#     InvocationBeforeDeregistration = "3"
#     MAXDNSLookupPerInvocation = "50"
#     NLBTargetGroupARN = aws_lb_target_group.lb_target_group.arn
#     S3BucketName = aws_s3_bucket.lambda_bucket.id
#     SameVPC = "True"
#     Region = "us-west-2"
#   }
#   template_body = file("./cf_templates/template_poplulate_NLB_TG_with_ALB_python3.json")
#   capabilities = ["CAPABILITY_AUTO_EXPAND", "CAPABILITY_IAM"]
#   depends_on = [aws_lb.lb, aws_lb_target_group.lb_target_group, aws_s3_bucket_object.lambda_python]
# }