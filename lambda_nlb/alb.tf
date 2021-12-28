data "aws_subnet_ids" "selected" {
  # change to appropriate value this needs to match the vpc for the nlb
  vpc_id = terraform.workspace

  tags = {
    Name = "vpc-re-pointer-foo-private-us-west-2*"
  }
}

locals {

  test_merge = merge([
    for k1, v1 in module.vars.env.load_balancers :
    {
      for v2 in v1 :
      "${k1}-${v2.port}" => v2
    }
  ]...)
  test_for_nest = [for k1, v1 in module.vars.env.load_balancers :
    {
      for v2 in v1 :
      "${k1}-${v2.port}" => v2
  }]
  test_for = [for k1, v1 in module.vars.env.load_balancers : "${v1}"]
}


resource "aws_lb" "lb" {
  for_each = module.vars.env.load_balancers
  name                       = "${var.project_name}-${each.key}"
  internal                   = true
  load_balancer_type         = "network"
  subnets                    = data.aws_subnet_ids.selected.ids
  enable_deletion_protection = false

  # Add if testing bool
  enable_cross_zone_load_balancing = true
  tags = {
    internal_alb_name = each.key
  }
}

module "aws_lb_target_group" {
  source      = "./modules/nlb_lambda"
  for_each = local.test_merge
  #for_each = toset(local.test_for)
  name        = "${var.project_name}"
  port        = each.value.port
  # protocol    = "TCP"
  vpc_id      = terraform.workspace
  internal_alb_name = each.value.internal_alb_name
  internal_alb_dns_name = each.value.internal_alb_dns_name
}
 
