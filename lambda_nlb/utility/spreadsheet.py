import boto3, os, re, logging, datetime, xlsxwriter, csv, json
from collections import defaultdict
from botocore.exceptions import ClientError
import pandas as pd

region_name = AWS_REGION = 'us-west-2'
AWS_REGIONS = ['us-west-2']

def get_date ():
    now = datetime.datetime.now()
    return_string = str(now.strftime('%y%m%d'))

    return return_string

def open_csv_file( region_name, object_type):
    now = get_date()
    script_dir = os.path.dirname(__file__)
    relative_path = ('csv' + '/' + region_name + '')
    absolute_path = os.path.join(script_dir, relative_path)

    try:
        os.makedirs(absolute_path, exist_ok=True)
    except OSError as e:
        print(f'Error: {absolute_path}:{e.strerror}')

    file_name = str(absolute_path + '/' + now + '_' + object_type + '_' + region_name + '.csv')

    try:
        os.remove(file_name)
    except OSError as e:
        print(f'Error: {file_name}:{e.strerror}')
    return open(file_name, 'w+')

def get_az_region(region_name):
    client = boto3.client('ec2', region_name)
   
    try:        
        response = client.describe_availability_zones(
            Filters=[
                {
                    'Name': 'region-name',
                    'Values': [region_name]
                }
            ]
        )                
        return response

    except OSError as e:
        print(f'Could not ghet az for region.:{e.strerror}')
        raise

def get_listeners_elbv2_region(region_name, lb_arn):
    client = boto3.client('elbv2', region_name)
   
    try:        
        response = client.describe_listeners(
            LoadBalancerArn = lb_arn
        )                
        return response

    except OSError as e:
        print(f'Could not ghet az for region.:{e.strerror}')
        raise

def get_tg_elb2_region(region_name, tg_arn):
    client = boto3.client('elbv2', region_name)
   
    try:        
        response = client.describe_target_groups(
            TargetGroupArns = [tg_arn]
        )                
        return response

    except OSError as e:
        print(f'Could not get tg for region.:{e.strerror}')
        raise

def get_lb_elbv2_region(region_name):
    client = boto3.client('elbv2', region_name)
   
    try:        
        response = client.describe_load_balancers()                
        return response

    except OSError as e:
        print(f"Could not get lb's for region.:{e.strerror}")
        raise

def get_vpc_region(region_name):
    client = boto3.client('ec2', region_name)
   
    try:        
        response = client.describe_vpcs()                
        return response

    except OSError as e:
        print(f"Could not get vpc's for region.:{e.strerror}")
        raise


def elbv2_listener_spreadsheet_dict(region_name):
    # print('hello world!')
    dict_line_number = 0
    count = 0

    # listener_return = defaultdict(lambda: defaultdict(dict))
    listener_return = {}
    listener_return[count] = {}
    listener_return[count] = {'tg_arn': 'Target Group ARN'}
    count += 1

    vpc = defaultdict()
    vpc = get_vpc_region(region_name)
    # print('vpc: {0}' .format(str(vpc)))
    # print('len(vpc): {0}\n' .format(len(vpc)))

    lb = defaultdict()
    lb = get_lb_elbv2_region(region_name)
    # print('lb: {0}' .format(str(lb)))
    # print('len(lb): {0}\n' .format(len(lb)))

    for key in lb['LoadBalancers']:
        # print('key: {0}'.format(key))        
        lb_arn = key['LoadBalancerArn']
        lb_dns_name = key['DNSName']
        lb_chz_id = key['CanonicalHostedZoneId']
        lb_created_time = key['CreatedTime']
        lb_name = key['LoadBalancerName']
        lb_scheme = key['Scheme']
        lb_vpc_id = key['VpcId']
        lb_state = key['State']['Code']
        lb_type = key['Type']
        lb_az = key['AvailabilityZones']
        lb_ip_type = key['IpAddressType']

        print('\nlb_arn: {0}' .format(str(lb_arn)))
        # print('lb_dns_name: {0}' .format(str(lb_dns_name)))
        # print('lb_chz_id: {0}' .format(str(lb_chz_id)))
        # print('lb_created_time: {0}' .format(str(lb_created_time)))
        # print('lb_name: {0}' .format(str(lb_name)))
        # print('lb_scheme: {0}' .format(str(lb_scheme)))
        # print('lb_vpc_id: {0}' .format(str(lb_vpc_id)))
        # print('lb_state: {0}' .format(str(lb_state)))
        # print('lb_type: {0}' .format(str(lb_type)))
        # # print('lb_az: {0}' .format(str(lb_az)))
        # print('lb_ip_type: {0}' .format(str(lb_ip_type)))

        listeners = defaultdict()
        # listeners = get_listeners_elbv2_region(region_name, lb_arn)
        # for l_key, l_values in listeners['Listeners'][0].items():
        #     # print('l_key: {0}\nl_values: {1}'.format(l_key, l_values))
        #     print('{0} - {1}'.format(l_key, l_values))

        listeners = get_listeners_elbv2_region(region_name, lb_arn)
        
        for l_key in listeners['Listeners']:
            # print('l_key: {0}\nl_values: {1}'.format(l_key, l_values))
            # print('{0} - {1}'.format(l_key, l_values))
            # print('l_key: {0}'.format(l_key))

            listener_arn = l_key['ListenerArn']
            listener_lb_arn = l_key['LoadBalancerArn']
            listener_port = l_key['Port']
            listener_protocol = l_key['Protocol']
            listener_type = l_key['DefaultActions'][0]['Type']
            listener_default_actions = l_key['DefaultActions']

            # print('listener_arn: {0}'.format(listener_arn))
            print('listener_lb_arn: {0}'.format(listener_lb_arn))
            # print('listener_port: {0}'.format(listener_port))
            # print('listener_protocol: {0}'.format(listener_protocol))
            # print('listener_type: {0}'.format(listener_type))
            # print('listener_tg_arn: {0}'.format(listener_tg_arn))
            # print('listener_default_actions: {0}'.format(listener_default_actions))

            
            try:
                listener_tg_arn = l_key['DefaultActions'][0]['TargetGroupArn']
                tg = defaultdict()
                tg = get_tg_elb2_region(region_name, listener_tg_arn)
                # print('\ntg: {0}' .format(str(tg)))
                for t_key in tg['TargetGroups']:
                    # print('\nt_key: {0}'.format(t_key))
                    tg_arn = t_key['TargetGroupArn']
                    tg_name = t_key['TargetGroupName']
                    tg_protocol = t_key['Protocol']
                    tg_port = t_key['Port']
                    tg_vpc_id = t_key['VpcId']
                    tg_hc_protocol = t_key['HealthCheckProtocol']
                    tg_hc_port = t_key['HealthCheckPort']
                    tg_hc_enabled = str(t_key['HealthCheckEnabled'])
                    tg_hc_interval = t_key['HealthCheckIntervalSeconds']
                    tg_hc_timeout = t_key['HealthCheckTimeoutSeconds']
                    tg_ht_count = t_key['HealthyThresholdCount']
                    tg_ut_count = t_key['UnhealthyThresholdCount']
                    try:
                        tg_hc_path = t_key['HealthCheckPath']
                    except:
                        tg_hc_path = 'no hc path'
                        pass
                    tg_target_type = t_key['TargetType']
                    # if count > 1:
                    #     print('There may be something wrong')
                    
                    
                    # print('listener_tg_arn: {0}' .format(str(listener_tg_arn)))
                    print('tg_arn: {0}' .format(str(tg_arn)))
                    # print('tg_name: {0}' .format(str(tg_name)))
                    print('tg_protocol: {0}' .format(str(tg_protocol)))
                    print('tg_port: {0}' .format(str(tg_port)))
                    print('tg_vpc_id: {0}' .format(str(tg_vpc_id)))
                    # print('tg_hc_protocol: {0}' .format(str(tg_hc_protocol)))
                    # print('tg_hc_port: {0}' .format(str(tg_hc_port)))
                    # print('tg_hc_enabled: {0}' .format(str(tg_hc_enabled)))
                    # print('tg_hc_interval: {0}' .format(str(tg_hc_interval)))
                    # print('tg_hc_timeout: {0}' .format(str(tg_hc_timeout)))
                    # print('tg_ht_count: {0}' .format(str(tg_ht_count)))
                    # print('tg_ut_count: {0}' .format(str(tg_ut_count)))
                    # print('tg_hc_path: {0}' .format(str(tg_hc_path)))
                    # print('tg_target_type: {0}' .format(str(tg_target_type)))

                    

                    listener_line_key = str(str(count)+'-'+tg_arn+str(tg_protocol)+str(tg_port)+tg_vpc_id)
                    
                    print('listener_line_key: {0}' .format(str(listener_line_key)))
                    listener_return[count] = {'tg_arn': tg_arn}
                    count += 1
                    

                    # listener_return[



                    # not defined need more code :)-
                    # tg_ = t_key['LoadBalancerArns']
                    # tg_ = t_key['Matcher']
                    # break
            except: # OSError as e:
                # print(f'What went wrong... {e.strerror}')
                listener_tg_arn = str('No tg defined for: ' + listener_arn)
                tg_arn = str('No tg defined for: ' + listener_arn)
                tg_name = ''
                tg_protocol = ''
                tg_port = ''
                tg_vpc_id = ''
                tg_hc_protocol = ''
                tg_hc_port = ''
                tg_hc_enabled = ''
                tg_hc_interval = ''
                tg_hc_timeout = ''
                tg_ht_count = ''
                tg_ut_count = ''
                tg_hc_path = ''
                tg_target_type = ''
                                
                # print('listener_tg_arn: {0}' .format(str(listener_tg_arn)))
                # print('tg_arn: {0}' .format(str(tg_arn)))
                # print('tg_name: {0}' .format(str(tg_name)))
                # print('tg_protocol: {0}' .format(str(tg_protocol)))
                # print('tg_port: {0}' .format(str(tg_port)))
                # print('tg_vpc_id: {0}' .format(str(tg_vpc_id)))
                # print('tg_hc_protocol: {0}' .format(str(tg_hc_protocol)))
                # print('tg_hc_port: {0}' .format(str(tg_hc_port)))
                # print('tg_hc_enabled: {0}' .format(str(tg_hc_enabled)))
                # print('tg_hc_interval: {0}' .format(str(tg_hc_interval)))
                # print('tg_hc_timeout: {0}' .format(str(tg_hc_timeout)))
                # print('tg_ht_count: {0}' .format(str(tg_ht_count)))
                # print('tg_ut_count: {0}' .format(str(tg_ut_count)))
                # print('tg_hc_path: {0}' .format(str(tg_hc_path)))
                # print('tg_target_type: {0}' .format(str(tg_target_type)))

                # listener_line_key = str(str(count)+'-'+tg_arn+str(tg_protocol)+str(tg_port)+tg_vpc_id)
                # print('listener_line_key: {0}' .format(str(listener_line_key)))
                listener_return[count] = {}
                listener_return[count] = {'tg_arn': tg_arn}
                count += 1
                # pass

    return listener_return
            

def try200(region_name):
     # print('hello world!')
    dict_line_number = 0
    count = 0

    # listener_return = defaultdict(lambda: defaultdict(dict))
    listener_return = {}
    listener_return[count] = {}
    listener_return[count] = {'tg_arn': 'Target Group ARN'}
    count += 1

    vpc = defaultdict()
    vpc = get_vpc_region(region_name)
    # print('vpc: {0}' .format(str(vpc)))
    # print('len(vpc): {0}\n' .format(len(vpc)))

    lb = defaultdict()
    lb = get_lb_elbv2_region(region_name)
    # print('lb: {0}' .format(str(lb)))
    # print('len(lb): {0}\n' .format(len(lb)))

    
    lb_dict = defaultdict()
    listener_dict = defaultdict()
    tg_dict = defaultdict()
    for key in lb['LoadBalancers']:
        print(key)
        for l_key, l_value in key.items():
            print('l_key: {0}\nl_value: {1}'.format(l_key, l_value))
            if 'State' in key:
                print("key['State']['Code']: {0}" .format(str(key['State']['Code'])))
                continue
            else:
                y = 1



    # for key, value in lb['LoadBalancers'][0].items():
    #     print('key: {0}\nvalue: {1}'.format(key, value))
        
    #     if 'LoadBalancerArn' in str(key):
            # listener_count = 0
            # listeners = defaultdict()
            # listeners = get_listeners_elbv2_region(region_name, value)
            # for l_key, l_values in listeners['Listeners'][0].items():
            #     print('l_key: {0}\nl_values: {1}'.format(l_key, l_values))
            #     if 'DefaultActions' in str(l_key) and 'TargetGroupArn' in str(l_values) :
            #         tg_arn = l_values[0]['TargetGroupArn']
            #         tg = defaultdict()
            #         tg = get_tg_elb2_region(region_name, tg_arn)
            #         for t_key, t_values in tg['TargetGroups'][0].items():
            #             print('t_key: {0}\nt_values: {1}'.format(t_key, t_values))
            #             listener_return[count] = {t_key: t_values}
            #     else:
            #         lb_dict[listener_count] = {l_key: l_values}
            #         listener_count += 1
            # count += 1
            # print(str(lb_dict))

    # return listener_return                  




            


            
            # for t_key in tg['TargetGroups']:
            #     print('t_key: {0}'.format(t_key))
            #     break
            

        

        
# LoadBalancerArn
# DNSName
# CanonicalHostedZoneId
# CreatedTime
# LoadBalancerName
# Scheme
# VpcId
# State
# Type
# AvailabilityZones
# IpAddressType
        # break
    

    

    
    # print('listener_return: {0}' .format(str(listener_return)))
    
    


# Test lines
# object_type = 'test_file'
# test = open_csv_file( region_name, object_type)

# test = get_az_region(region_name)
# print ('test: {0}' .format(test))
# test_out = defaultdict()
# 





# foo = try200(region_name)
# print('foo:\n' + str(foo))






# print('test_out: {0}' .format(str(test_out)))

# workbook = xlsxwriter.Workbook('hello.xlsx')
# worksheet = workbook.add_worksheet()

# header_format = workbook.add_format({
#     'bold': True,
#     'text_wrap': True,
#     'valign': 'top',
#     'fg_color': '#D7E4BC',
#     'border': 1})
# # worksheet.write('A1', 'Hello worldwasdx')
# df = pd.DataFrame(data=test_out, index=[0])
# df = (df.T)
# print (df)
# df.to_excel('dict1.xlsx')
# workbook.close()

# for key, value in test_out.items():
#     print('key: {0}' .format(str(key)))
#     print('value: {0}' .format(str(value)))
# #     # for x in value.info():
# #     #     print('x: {0}' .format(str(x)))

# workbook.close()

# for key, value in test_out:
#     print('key: {0}\nvalue' .format(str(key), str(value)))
    # for test_key in key:
    #     print('key: {0}' .format(str(key)))


def elbv1_listener_vars_vpc_dict(region_name, vpc_id):
    return_dict = {vpc_id:{'load_balancers':{}}}
    client = boto3.client('elb', region_name)
    response = client.describe_load_balancers()

    for key in response['LoadBalancerDescriptions']:

        lb_vpc = key['VPCId']
        print('lb_vpc: {0}' .format(str(lb_vpc)))
        print('vpc_id: {0}' .format(str(vpc_id))) 
        lb_name = key['LoadBalancerName']
        lb_dns_name = key['DNSName']   
        listener_return = {}

        if 'ListenerDescriptions' in key:
            for listener in key['ListenerDescriptions']:            
                # print('listener: {0}' .format(str(listener)))
                listener_port = listener['Listener']['LoadBalancerPort'] #this will name the listener
                # print('listener_port: {0}' .format(str(listener_port)))
                listener_protocol = listener['Listener']['Protocol']
                
                listener_return[listener_port] = {
                             "port" : listener_port,
                             "protocol" : listener_protocol,
                             "internal_alb_name" : lb_name,
                             "internal_alb_dns_name" : lb_dns_name,
                             "internal_alb_region" : region_name
                         }

        else:
            # print('no listeners defined')
            listener_return = {}
        if vpc_id == lb_vpc:
                return_dict[vpc_id]['load_balancers'][lb_name] = listener_return

    # print('listener_return: {0}' .format(str(listener_return)))
    # print('return_dict: {0}' .format(str(return_dict)))
    
    return return_dict









listener_vars_vpc = elbv1_listener_vars_vpc_dict("us-west-2", 'vpc-0267647d6eb117c0d')
# print ('listener_vars_vpc:\n' + str(listener_vars_vpc))

# sjson = json.dumps(hello_world)
# f = open("dict.json","w")
# f.write(sjson)
# f.close()

# json_object = json.dumps(hello_world)
# json_formatted_str = json.dumps(json_object, indent=3, ensure_ascii=True)
# print(json_formatted_str)
# f = open("dict.json","w")
# f.write(json_formatted_str)
# f.close()

with open("developerPrettyPrint.json", "w") as write_file:
    json.dump(listener_vars_vpc, write_file, indent=2, separators=("", " = "), sort_keys=False)
print("Done writing pretty printed JSON data into a file")

