import os, sys
import boto3
import argparse

def get_client(resource, profile=None):
    """
    Common resources: 'cognito-idp', 's3', 'sagemaker', 'sagemaker-runtime'
    """
    if profile is None:
        return boto3.client(resource)
    else:
        session = boto3.session.Session(profile_name = profile)
        return session.client(resource)


############################## AWS S3 ##############################
# Not needed not, give me time to port over from my past codes

############################## AWS Cognito ##############################
# def cognito_force_change_pw(user_pool_id, username, password, profile = None):
#     command = f"aws cognito-idp admin-set-user-password --user-pool-id {user_pool_id} --username {username} --password {password} --permanent"

#     if profile is not None:
#         command += f" --profile {profile}"

#     try:
#         os.system(command)
#     except Exception as e:
#         raise Exception("Something went wrong!") from e

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html
def cognito_list_users_in_group(UserPoolId, GroupName, Limit = None, NextToken = None, profile = None):
    client = get_client('cognito-idp', profile=profile)

    parameters = {
        'UserPoolId': UserPoolId,
        'GroupName': GroupName
    }
    if type(Limit) == int:
        parameters['Limit'] = Limit
    if NextToken is not None:
        parameters["NextToken"] = NextToken

    response = client.list_users_in_group(**parameters)
    return response

def cognito_list_users(UserPoolId, AttributesToGet = None, Limit = None, PaginationToken = None, Filter = None, profile = None):
    client = get_client('cognito-idp', profile=profile)

    parameters = {'UserPoolId':UserPoolId}

    if type(AttributesToGet) == list:
        parameters['AttributesToGet'] = AttributesToGet
    if type(Limit) == int:
        parameters['Limit'] = Limit
    if PaginationToken is not None:
        parameters['PaginationToken'] = PaginationToken
    if type(Filter) == str:
        parameters['Filter'] = Filter

    response = client.list_users(**parameters)
    return response

def cognito_list_groups(UserPoolId, Limit = None, NextToken = None, profile = None):
    client = get_client('cognito-idp', profile=profile)
    parameters = {'UserPoolId': UserPoolId}

    if type(Limit) == int:
        parameters['Limit'] = Limit
    if NextToken is not None:
        parameters["NextToken"] = NextToken

    response = client.list_groups(**parameters)
    return response

def cognito_get_user(AccessToken, profile):
    client = get_client('cognito-idp', profile=profile)
    response = client.get_user(
        AccessToken=AccessToken
    )
    return response

def cognito_add_custom_attributes(UserPoolId,CustomAttributes,profile = None):
    """
    :param CustomAttributes: [
            {
                'Name': 'string',
                'AttributeDataType': 'String'|'Number'|'DateTime'|'Boolean',
                'DeveloperOnlyAttribute': True|False,
                'Mutable': True|False,
                'Required': True|False,
                'NumberAttributeConstraints': {
                    'MinValue': 'string',
                    'MaxValue': 'string'
                },
                'StringAttributeConstraints': {
                    'MinLength': 'string',
                    'MaxLength': 'string'
                }
            },
        ]
    """
    client = get_client('cognito-idp', profile=profile)
    response = client.add_custom_attributes(
        UserPoolId=UserPoolId,
        CustomAttributes=CustomAttributes
    )
    return response

def cognito_admin_create_user(UserPoolId, Username, action = None, profile = None, **kwangs):
    """
    : action: 'create', 'remove'
    :**kwangs: UserAttributes, ValidationData, TemporaryPassword, ForceAliasCreation, MessageAction, DesiredDeliveryMediums, ClientMetadata
    
    - UserAttributes=[
        {
            'Name': 'string',
            'Value': 'string'
        },
    ],
    - ValidationData=[
        {
            'Name': 'string',
            'Value': 'string'
        },
    ],
    - TemporaryPassword='string',
    - ForceAliasCreation=True|False,
    - MessageAction='RESEND'|'SUPPRESS',
    - DesiredDeliveryMediums=[
        'SMS'|'EMAIL',
    ],
    - ClientMetadata={
        'string': 'string'
    }
    """
    client = get_client('cognito-idp', profile=profile)
    if action == 'create':
        parameters = {'UserPoolId':UserPoolId, 'Username':Username, **kwangs}
        response = client.admin_create_user(**parameters)

    elif action == 'delete':
        response = client.admin_delete_user(
            UserPoolId=UserPoolId,
            Username=Username
        )
    else:
        raise Exception("Supported action: 'create', 'delete'!")
    return response

def cognito_admin_delete_user_attributes(UserPoolId, Username, UserAttributeNames, profile = None):
    """:param UserAttributeNames: ['string']"""
    assert type(UserAttributeNames) == list, "UserAttributeNames must be a list"
    client = get_client('cognito-idp', profile=profile)
    response = client.admin_delete_user_attributes(
        UserPoolId=UserPoolId,
        Username=Username,
        UserAttributeNames=UserAttributeNames
    )
    return response

def cognito_admin_update_user_attributes(UserPoolId, Username, UserAttributes, ClientMetadata = None, profile=None):
    """
    - UserAttributes=[
            {
                'Name': 'string',
                'Value': 'string'
            },
    ]
    - ClientMetadata={
            'string': 'string'
    }
    """
    client = get_client('cognito-idp', profile=profile)
    assert type(UserAttributes) == list, "UserAttributes must be a list"
    parameters = {'UserPoolId':UserPoolId,'Username':Username,'UserAttributes':UserAttributes}

    if ClientMetadata is not None:
        parameters['ClientMetadata'] = ClientMetadata
    response = client.admin_update_user_attributes(**parameters)
    return response

def cognito_admin_get_user(UserPoolId, Username, profile=None):
    client = get_client('cognito-idp', profile=profile)
    response = client.admin_get_user(
        UserPoolId=UserPoolId,
        Username=Username
    )
    return response

def cognito_admin_add_remove_user_from_group(UserPoolId, Username, GroupName, action = None, profile=None):
    """Supported action: 'add', 'delete'"""
    client = get_client('cognito-idp', profile=profile)
    if action == 'delete':
        response = client.admin_remove_user_from_group(
            UserPoolId=UserPoolId,
            Username=Username,
            GroupName=GroupName
        )
    elif action == 'add':
        response = client.admin_add_user_to_group(
            UserPoolId=UserPoolId,
            Username=Username,
            GroupName=GroupName
        )
    else:
        raise Exception("Supported action: 'add', 'delete'")
    return response

def cognito_admin_set_user_password(UserPoolId, Username, Password, Permanent = True, profile=None):
    client = get_client('cognito-idp', profile=profile)

    response = client.admin_set_user_password(
        UserPoolId=UserPoolId,
        Username=Username,
        Password=Password,
        Permanent= Permanent
    )
    return response

def cognito_revoke_token(Token, ClientId, ClientSecret = None, profile=None):
    client = get_client('cognito-idp', profile=profile)
    parameters = {'Token':Token, 'ClientId':ClientId}
    if ClientSecret is not None:
        parameters['ClientSecret'] = ClientSecret

    response = client.revoke_token(**parameters)
    return response

def cognito_initiate_auth(AuthFlow, AuthParameters, ClientId, profile = None, **kwangs):
    """
    - AuthFlow = 'USER_SRP_AUTH', 'REFRESH_TOKEN_AUTH', 'REFRESH_TOKEN', 'CUSTOM_AUTH', 'ADMIN_NO_SRP_AUTH', 'USER_PASSWORD_AUTH', 'ADMIN_USER_PASSWORD_AUTH'
    - AuthParameters= {'string': 'string'}
    - ClientMetadata={'string': 'string'}
    - AnalyticsMetadata={'AnalyticsEndpointId': 'string'}
    - UserContextData={'IpAddress': 'string','EncodedData': 'string'}
    """
    AuthFlow = AuthFlow.upper()
    assert AuthFlow in ['USER_SRP_AUTH','REFRESH_TOKEN_AUTH','REFRESH_TOKEN','CUSTOM_AUTH','ADMIN_NO_SRP_AUTH','USER_PASSWORD_AUTH','ADMIN_USER_PASSWORD_AUTH'], "Invalid AuthFlow value"
    
    client = get_client('cognito-idp', profile=profile)
    parameters = {'AuthFlow':AuthFlow, 'AuthParameters':AuthParameters, 'ClientId':ClientId, **kwangs}
    response = client.initiate_auth(**parameters)
    return response

def cognito_list_devices(AccessToken, Limit = None, PaginationToken = None, profile = None):
    client = get_client('cognito-idp', profile=profile)

    parameters = {'AccessToken':AccessToken}
    if type(Limit) == int:
        parameters['Limit'] = Limit
    if PaginationToken is not None:
        parameters['PaginationToken'] = PaginationToken
    response = client.list_devices(**parameters)
    return response

############################## Main ##############################
if __name__ == "__main__":
    import json
    import dotenv
    from dotenv import load_dotenv
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--resource', default = 'cognito', type=str, help ="Supported resource: cognito")
    parser.add_argument('--action', default = None, type=str, help ="Supported action: get_token, refresh_token, revoke_token")

    parser.add_argument('--config', default = 'config.json', type=str, help ="Config file relative to aws.py")
    parser.add_argument('--env', default = None, type=str, help ="Environment file relative to aws.py")
    parser.add_argument('--s3profile', default = None, type=str, help ="S3 Session for local development")
    parser.add_argument('--verbose', action='store_true', help ="Print everything")

    args = parser.parse_args()

    # Load from environment
    try:
        if args.env is not None:
            dotenv_path = os.path.join(os.path.dirname(__file__), args.env)
            assert os.path.exists(dotenv_path), f"Environment file does not exists: {dotenv_path}"
            load_dotenv(dotenv_path)
        else:
            dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

        config_path = os.path.join(os.path.dirname(__file__), args.config)
        assert os.path.exists(config_path), f"Config file does not exist: {config_path}"
        with open(config_path, 'r') as f:
            cfg = json.load(f)
        profile = args.s3profile

    except Exception as e:
        raise Exception("Something wrong while getting credentials...") from e

    # Using the utilities in this file
    resource = args.resource
    action = args.action
    if action not in ["revoke_token"]:
        parameters = cfg[resource][action]

    if resource == "cognito":
        ClientId = os.environ.get("COGNITO_CLIENT_ID")
        ClientSecret = os.environ.get("COGNITO_CLIENT_SECRET")

        if action == "get_token":
            parameters = {"ClientId": ClientId, "profile":profile, **parameters}
            if args.verbose: print(json.dumps(parameters, indent=4))
            res = cognito_initiate_auth(**parameters)

            if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
                dotenv.set_key(dotenv_path, "COGNITO_ACCESS_TOKEN", res["AuthenticationResult"].get("AccessToken"))
                dotenv.set_key(dotenv_path, "COGNITO_REFRESH_TOKEN", res["AuthenticationResult"].get("RefreshToken"))
                dotenv.set_key(dotenv_path, "COGNITO_ID_TOKEN", res["AuthenticationResult"].get("IdToken"))

        elif action =="refresh_token":
            REFRESH_TOKEN = os.environ.get('COGNITO_REFRESH_TOKEN')
            parameters = {"AuthParameters": {"REFRESH_TOKEN": REFRESH_TOKEN}, "ClientId": ClientId, "profile":profile, **parameters}
            if args.verbose: print(json.dumps(parameters, indent=4))
            res = cognito_initiate_auth(**parameters)

            if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
                dotenv.set_key(dotenv_path, "COGNITO_ACCESS_TOKEN", res["AuthenticationResult"].get("AccessToken"))
                dotenv.set_key(dotenv_path, "COGNITO_ID_TOKEN", res["AuthenticationResult"].get("IdToken"))

        elif action =="revoke_token":
            REFRESH_TOKEN = os.environ.get('COGNITO_REFRESH_TOKEN')
            parameters = {"Token": REFRESH_TOKEN, "ClientId": ClientId, "ClientSecret": ClientSecret, "profile":profile}
            if args.verbose: print(json.dumps(parameters, indent=4))
            res = cognito_revoke_token(**parameters)

        else:
            raise Exception(f"Invalid action: {action}")

        if args.verbose: print(res)
    else:
        raise Exception(f"Invalid resource: {resource}")




    # # testing codes
    # profile = os.environ.get('profile')
    # userpoolid = os.environ.get('userpoolid')
    # groupname = os.environ.get('groupname')
    # CustomAttributes = [
    #     {
    #         'Name': 'attribute1',
    #         'AttributeDataType': 'String',
    #         'DeveloperOnlyAttribute': False,
    #         'Mutable': True,
    #         'Required': False,
    #         'StringAttributeConstraints': {'MinLength': '1','MaxLength': '10'}
    #     }
    # ]
    # AuthFlow = 'USER_PASSWORD_AUTH'
    # AuthParameters = {"USERNAME": 'user4', 'PASSWORD': 'P@ssw0rd'}
    
    # ClientId = os.environ.get('ClientId')
    # AccessToken = os.environ.get('AccessToken')

    # # AuthFlow = 'REFRESH_TOKEN_AUTH'
    # # REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')
    # # AuthParameters = {"REFRESH_TOKEN": REFRESH_TOKEN}

    # # res = cognito_list_users_in_group(userpoolid, groupname, profile = profile)
    # # res = cognito_list_users(userpoolid, profile = profile)
    # # res = cognito_list_groups(userpoolid, profile = profile)
    # # res = cognito_add_custom_attributes(userpoolid, CustomAttributes, profile = profile)
    # # res = cognito_admin_create_user(userpoolid, Username = 'user4', profile = profile, UserAttributes = [{'Name':'custom:test', 'Value': 'customtest'}])
    # # res = cognito_admin_delete_user(userpoolid, Username = 'user3' , profile = profile)
    # # res = cognito_admin_add_remove_user_from_group(userpoolid, 'user1', 'test-g1' , profile = profile, action = 'delete')
    # # res = cognito_admin_set_user_password(userpoolid, 'user4', 'P@ssw0rd' , profile = profile)
    # # res = cognito_admin_update_user_attributes(userpoolid, 'user1', profile = profile, UserAttributes = [{'Name':'custom:test', 'Value': 'test1'}])
    # # res = cognito_admin_get_user(userpoolid, Username = 'user1' , profile = profile)
    # # res = cognito_list_devices(AccessToken=AccessToken, profile=profile)

    # res = cognito_initiate_auth(AuthFlow, AuthParameters, ClientId, profile = profile)
    # # res = cognito_revoke_token(REFRESH_TOKEN, ClientId, ClientSecret = None, profile=profile)
    # print(res)
    # pass

    # # botocore.errorfactory.NotAuthorizedException: An error occurred (NotAuthorizedException) when calling the InitiateAuth operation: Incorrect username or password.