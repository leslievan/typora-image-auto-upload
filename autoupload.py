#!/bin/bash

import oss2
import configparser
import argparse
import time
from os.path import join
from pathlib import Path
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Upload file')
    parser.add_argument('--from_local', '-f', nargs='+',
                        help='path of file to upload')
    args = parser.parse_args()

    config_path = Path('./config.ini').resolve()

    config = configparser.ConfigParser()
    config.read(config_path)

    oss_type = config.get('config', 'type')
    endpoint = config.get('config', 'endpoint')
    bucket = config.get('config', 'bucket')
    secret_id = config.get('config', 'secret_id')
    secret_key = config.get('config', 'secret_key')
    path = config.get('config', 'path')

    ym = time.strftime("%Y/%m", time.localtime())

    if oss_type == 'aliyun':
        auth = oss2.Auth(secret_id, secret_key)
        client = oss2.Bucket(auth, endpoint, bucket)

        domain = 'https://' + bucket + '.' + endpoint

        for path in args.from_local:
            file = path.rsplit("/")[-1]
            obj = join(ym, file)
            client.put_object_from_file(obj, path)
            print(join(domain, obj))

    if oss_type == 'tencent':
        auth = CosConfig(
            Endpoint=endpoint, SecretId=secret_id, SecretKey=secret_key)
        client = CosS3Client(auth)

        domain = 'https://' + bucket + '.' + endpoint

        for path in args.from_local:
            file = path.rsplit("/")[-1]
            obj = join(ym, file)
            client.put_object_from_local_file(
                Bucket=bucket,
                LocalFilePath=path,
                Key=obj,
            )
            print(join(domain, obj))

