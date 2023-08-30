from datetime import datetime, timedelta, timezone
# import boto3
# import os
from lib.ddb import Ddb
from lib.db import db

class MessageGroups:

  def run(cognito_user_id):
    # endpoint_url = os.getenv("AWS_ENDPOINT_URL")

    # # endpoint_url = 'http://dynamodb-local:8000'
    # if endpoint_url:
    #   attrs = { 'endpoint_url': endpoint_url }
    # else:
    #   attrs = {}
    # attrs = {'endpoint_url': 'http://localhost:8000'}
    # print(f"Endpoint_URL================={attrs}")
    # ddb = boto3.client('dynamodb',**attrs)

    model = {
      'errors': None,
      'data': None
    }

    sql = db.template('users','uuid_from_cognito_user_id')
    my_user_uuid = db.query_value(sql,{
      'cognito_user_id': cognito_user_id
    })


    print(f"Messages_groups.py ===== UUID: == {my_user_uuid}")

    data = Ddb.list_message_groups(my_user_uuid)
    print(f"Messages_groups.py ===== list_message_groups: == {data}")
    model['data'] = data
    return model