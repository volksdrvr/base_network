# data "aws_subnet_ids" "selected" {
#   # change to appropriate value this needs to match the vpc for the nlb
#   vpc_id = terraform.workspace

#   tags = {
#     Name = "vpc-re-pointer-*-private-us-west-2*"
#   }
# }

data "aws_lb" "nlb" {
  tags = {"internal_alb_name" = "${var.internal_alb_name}"}
  depends_on = [aws_lb_target_group.lb_target_group]
}


resource "aws_lb_target_group" "lb_target_group" {
  
  name        = "${var.internal_alb_name}-${var.port}"
  port        = var.port
  protocol    = "TCP"
  vpc_id      = var.vpc_id
  target_type = "ip"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lb_listener" "lb_listener" {
  # for_each = aws_lb_target_group.lb_target_group
  load_balancer_arn = data.aws_lb.nlb.arn
  port              = var.port
  protocol          = "TCP"
  #certificate_arn   = 


  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.lb_target_group.arn
  }
  # depends_on = [aws_lb_target_group.lb_target_group]
}

resource "aws_cloudformation_stack" "nlb_lambda" {
  name = "${var.name}-${var.port}"
  parameters = {
    InternalALBDNSName = var.internal_alb_dns_name
    # InternalALBDNSName = module.vars.environment.lb_dns_name
    ALBListenerPort = var.port
    CWMetricFlagIPCount = "True"
    InvocationBeforeDeregistration = "3"
    MAXDNSLookupPerInvocation = "50"
    NLBTargetGroupARN = data.aws_lb.nlb.arn
    S3BucketName = "lambda-re-pointer-${var.port}"
    SameVPC = "True"
    Region = "us-west-2"
  }
  template_body = file("${path.module}/cf_templates/template_poplulate_NLB_TG_with_ALB_python3.json")
  capabilities = ["CAPABILITY_AUTO_EXPAND", "CAPABILITY_IAM"]
  depends_on = [aws_lb_listener.lb_listener]
}

# to fix this:
# 1. module to make the nlb tagged with the classic_lb_name
# 2.  
