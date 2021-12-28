# data "aws_subnet_ids" "selected" {
#   # change to appropriate value this needs to match the vpc for the nlb
#   vpc_id = terraform.workspace

#   tags = {
#     Name = "vpc-re-pointer-*-private-us-west-2*"
#   }
# }
# data "aws_lb" "nlb" {
#   tags = {"internal_alb_name" = "${var.internal_alb_name}"}
#   depends_on = [var.internal_alb_name]
# }

# locals {
#   alb_arn = local.aws_lb.nlb.arn
# }


# resource "aws_lb_target_group" "lb_target_group" {
#   name        = "${var.name}-${var.port}}"
#   port        = var.port
#   protocol    = "TCP"
#   vpc_id      = var.vpc_id
#   target_type = "ip"
#   lifecycle {
#     create_before_destroy = true
#   }
# }

# resource "aws_lb_listener" "lb_listener" {
#     for_each = local.flat
#   load_balancer_arn = aws_lb.lb.arn
#   port              = "443"
#   protocol          = "TCP"
#   #certificate_arn   = 


#   default_action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.lb_target_group.arn
#   }
# }


# to fix this:
# 1. module to make the nlb tagged with the classic_lb_name
# 2.  
