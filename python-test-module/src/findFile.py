import boto3
#
#
# event = "/uploads/2022-03-06T23_43_43.583Z-6802499/landmarks.json"
# print("event is ", event)
# session = boto3.Session(
#     aws_access_key_id="AKIAX2CW5VFBC5NTKEGC",
#     aws_secret_access_key="U6936MMnYesa6uau8tbRZSPr1ficwq/lsywUF7dE",
# )

s3 = boto3.client('s3', aws_access_key_id=... , aws_secret_access_key=...)
s3.download_file('your_bucket','k.png','/Users/username/Desktop/k.png')
#
# s3 = session.resource('s3')
# path = event
# thing = s3.Bucket('asl-dictionary-uploads').download_file('landmarks.json', path) #FIXME
#
# print(thing)
#

# import boto3
# event = "/uploads/2022-03-06T23_43_43.583Z-6802499/landmarks.json"
#
# s3_client = boto3.client('s3',
#     aws_access_key_id="<AKIAX2CW5VFBC5NTKEGC>",
#     aws_secret_access_key="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",
#     region_name='us-east-1'
# )
#
# s3_client.download_file('asl-dictionary-uploads', 'landmarks.json', event)
# print('success')