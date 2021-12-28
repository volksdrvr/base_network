# foo 
locals {
  vpc-0267647d6eb117c0d = {
    "load_balancers" = {
      "lb-foo-myezbrew-dev" = {
        "8080" = {
          "port" = 8080
          "protocol" = "HTTP"
          "internal_alb_name" = "lb-foo-myezbrew-dev"
          "internal_alb_dns_name" = "internal-lb-foo-myezbrew-dev-1406793425.us-west-2.elb.amazonaws.com"
          "internal_alb_region" = "us-west-2"
        }
        "80" = {
          "port" = 80
          "protocol" = "HTTP"
          "internal_alb_name" = "lb-foo-myezbrew-dev"
          "internal_alb_dns_name" = "internal-lb-foo-myezbrew-dev-1406793425.us-west-2.elb.amazonaws.com"
          "internal_alb_region" = "us-west-2"
        }
      }
    }
  }
}


# lb_1 requirements
#       lb_1 = {
#         "lb_l_listeners_1" = {
# 
#           # used to create target group
#           port = "wasdx"
#           protocol = "wasdx"
#           target_type  = "wasdx"
#           vpc_id = "wasdx"
# 
#           # used to create listener
#           port = "wasdx"
#           protocol = "wasdx"
#           ssl_policy = "wasdx"
#           certificate_arn = "wasdx"
#           default_action_type = "wasdx"
#           default_action_target_group_arn = "wasdx"

#           # used for lambda
#           "internal_alb_dNS_name" = "wasdx"
#           "alb_listener_port" = "wasdx"
#           "region" = "us-west-2"
#           } 
#       }
