locals {
  default = {
    # test_objects_1 = {
    #   "object_key_acceptance_1_1" = "object_value_acceptance_1_1"
    #   "object_key_acceptance_1_2" = "object_value_acceptance_1_2"
    # }
    load_balancers = {
      # lb_1
      lb-bar-some-test = {
        "lb-l-listeners-1" = {
          # used by the user
          "use_case" = "wasdx1"
          # used to create target group
          port        = "80"
          protocol    = "TCP"
          target_type = "ip"
          protocol                        = "wasd1x"
          ssl_policy                      = "wasd1x"
          certificate_arn                 = "wasdx1"
          default_action_type             = "wasdx1"
          default_action_target_group_arn = "internal-lb-bar-wasdx1-dev-1404439995.us-west-2.elb.amazonaws.com"

          # used for lambda
          "internal_alb_dNS_name" = "wasdx1"
          # "alb_listener_port" = "wasdx1"
          "region" = "us-west-2"
        }
      }
    }
  }
}


