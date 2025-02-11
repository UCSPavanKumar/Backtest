import boto3
import json
import io
import os
import pandas as pd


class cls_s3(object):

    def __init__(self):
        access_key = os.environ.get('aws_key')
        secret_key = os.environ.get('aws_secret')
        self.s3 = boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_key)

    def getObject(self,symbol,bucket,key):
        actual_key = f'{key}/{symbol}.csv'#'{0}/{1}.csv'.format(key,symbol)
        read_file = self.s3.get_object(Bucket=bucket,Key=actual_key)
        body = read_file['Body'].read().decode('utf-8')
        df = pd.read_csv(io.StringIO(body))
        return df

    
    def saveObject(self,df,bucket,key):
        symbol = list(df['symbol'].unique())
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer,index=False)
        response = self.s3.put_object(Bucket = bucket,Key='{0}/{1}.csv'.format(key,symbol[0]),Body=csv_buffer.getvalue())
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 put object response for symbol {symbol}")
        else:
            print(f'Unsuccesful S3 put object response for symbol {symbol}, status {status}')


