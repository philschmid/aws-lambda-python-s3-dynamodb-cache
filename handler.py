import json
import os
import boto3

s3 = boto3.resource("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE_NAME"])


def check_cache_hit(dataset_id):
    """Checks if dataset_id is in dynamodb table to verify cache hit"""
    try:
        response = table.get_item(Key={"datasetId": dataset_id})
        if "Item" in response:
            return True
        else:
            return False
    except Exception as e:
        return False


def get_cache_file_from_s3(dataset_id):
    """Loads cached json from s3"""
    s3_object = s3.Object(os.environ["S3_BUCKET_NAME"], f"{dataset_id}_sample.json")
    file_content = s3_object.get()["Body"].read().decode("utf-8")
    json_content = json.loads(file_content)
    return json_content


def upload_cache_file_to_s3(dataset_id, cache_file_as_dict):
    """uploads cached json to s3"""
    print(os.environ["S3_BUCKET_NAME"])
    s3_object = s3.Object(os.environ["S3_BUCKET_NAME"], f"{dataset_id}_sample.json")
    s3_object.put(Body=(bytes(json.dumps(cache_file_as_dict).encode("UTF-8"))))
    update_cache_table(dataset_id)


def update_cache_table(dataset_id):
    """Updates the dynamodb table to include new cache"""
    response = table.put_item(Item={"datasetId": dataset_id})
    return response


# pseudo code 
def create_cache_file_from_dataset_id(dataset_id):
    """creates dictonary of the file which needs to be cached on s3"""
    # cache dir needs to be tmp, since you can only write files in /tmp in AWS Lambda
    cache_file = {"id": dataset_id}
    return cache_file


def handler(event, context):
    if event["queryStringParameters"] is not None:
        if "datasetId" in event["queryStringParameters"]:
            # extracts dataset_id from query parameter
            dataset_id = event["queryStringParameters"]["datasetId"]
            print("cache_hit", check_cache_hit(dataset_id))
            if check_cache_hit(dataset_id) is True:
                # get file from s3
                cache_file = get_cache_file_from_s3(dataset_id)
            else:
                # creates cache file and updates cache table
                cache_file = create_cache_file_from_dataset_id(dataset_id)
                # uploads cache file to s3
                upload_cache_file_to_s3(dataset_id, cache_file)

            response = {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                },
                "body": json.dumps(cache_file),
            }
        else:
            response = {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                },
                "body": json.dumps({"error": "datasetId as key not provided"}),
            }
    else:
        response = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"error": "No QueryParameter provided"}),
        }

    return response
