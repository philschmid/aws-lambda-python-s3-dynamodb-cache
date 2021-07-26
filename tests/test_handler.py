import pytest
import os

os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_PROFILE"] = "hf-sm"
os.environ["S3_BUCKET_NAME"] = "test-dataset-cache-assetscd77a4d4eb9"
os.environ["DYNAMODB_TABLE_NAME"] = "test-dataset-cache-tablecd77a4d4eb9"
from handler import handler


event = {
    "version": "2.0",
    "routeKey": "GET /dataset",
    "rawPath": "/dataset",
    "rawQueryString": "datasetId=imdb",
    "cookies": [],
    "headers": {
        "Host": "localhost:3000",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        "sec-ch-ua-mobile": "?0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": 'intercom-id-hgve3glw=d67cc472-4325-4cf7-85b8-eec774c94dbc; _ga=GA1.1.252339221.1622202966; ajs_user_id=%2232077b58-baa4-5776-83ca-2fd1a403ebf9%22; ajs_anonymous_id=%228c4c6117-eeba-4129-a219-4f978e21bd67%22; _xsrf=2|3895eb8f|218efed5808de8c6630cae5ab2267277|1623080657; _hp2_id.1823968819=%7B%22userId%22%3A%228178964257955746%22%2C%22pageviewId%22%3A%224230864699568393%22%2C%22sessionId%22%3A%225579380179461068%22%2C%22identity%22%3A%2232077b58-baa4-5776-83ca-2fd1a403ebf9%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; username-localhost-8888="2|1:0|10:1627035613|23:username-localhost-8888|44:YTE4ZGM3OTA4ZjY1NDJmMzhkMTIyMWI5NWE3ZTRjN2Y=|37205d53469003bbd2f687f5727ed06a9fcc317d0d69327c71de09d14c5bd9f5"',
    },
    "queryStringParameters": {"datasetId": "imdb"},
    "requestContext": {
        "accountId": "offlineContext_accountId",
        "apiId": "offlineContext_apiId",
        "authorizer": {"jwt": {}},
        "domainName": "offlineContext_domainName",
        "domainPrefix": "offlineContext_domainPrefix",
        "http": {
            "method": "GET",
            "path": "/dataset",
            "protocol": "HTTP/1.1",
            "sourceIp": "127.0.0.1",
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        },
        "requestId": "offlineContext_resourceId",
        "routeKey": "GET /dataset",
        "stage": "$default",
        "time": "26/Jul/2021:12:53:33 +0200",
        "timeEpoch": 1627296813903,
        # comment body in if you are working with a body in the request
        # "body": '{ "dataset_id":"imdb"}',
    },
}


def test_handler():
    res = handler(event, "")
    assert isinstance(res, dict)
