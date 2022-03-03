import boto3
import pandas
import passwords
import json

client = boto3.client(
    's3',
    aws_access_key_id = str(passwords.AWSAccessKeyId),
    aws_secret_access_key = str(passwords.AWSSecretKey),
    region_name = 'us-east-1'
)

# Creating the high level object oriented interface
resource = boto3.resource(
    's3',
    aws_access_key_id = str(passwords.AWSAccessKeyId),
    aws_secret_access_key = str(passwords.AWSSecretKey),
    region_name = 'us-east-1'
)


# print(passwords.AWSSecretKey)
# # Creating the low level functional client
# client = boto3.client(
#     's3', passwords.AWSAccessKeyId,passwords.AWSSecretKey,'us-east-1'
# )
#
# # Creating the high level object oriented interface
# resource = boto3.resource(
#     's3',
#     aws_access_key_id = passwords.AWSAccessKeyId,
#     aws_secret_access_key = passwords.AWSSecretKey,
#     region_name = 'us-east-1'
# )
#
# # Fetch the list of existing buckets
clientResponse = client.list_buckets()

# Print the bucket names one by one
print('Printing bucket names...')
for bucket in clientResponse['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')


# Print the data frame
my_bucket = resource.Bucket("asl-dictionary-uploads")
summaries = my_bucket.objects.all()
jsonFilesKeys = []
jsonFiles = []
for file in summaries:
    if file.key.endswith("json"):
        print(f"file is {file}")
        jsonFilesKeys.append(file.key)
        obj = client.get_object(
            Bucket = 'asl-dictionary-uploads',
            Key = file.key
        )
        json = pandas.read_csv(obj['Body'])
        jsonFiles.append(json.columns)
print(jsonFiles)