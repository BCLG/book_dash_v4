import json
import os
import dropbox
import boto3
import io

def lambda_handler(event, context):
    
    # Dropbox set-up
    dbx_token = os.environ['dbx_token_var']
    file_name = os.environ['file_name_var']
    
    # S3 set-up
    aws_region = os.environ['aws_region_var']
    bucket_name = os.environ['bucket_name_var']
    prefix = os.environ['prefix_var']
    name = os.environ['name_var']
    success_flag = False
    
    #Dropbox side
    print('Initializing Dropbox API')
    dbx = dropbox.Dropbox(dbx_token)
    print('.Success')

    print("Scanning for all files")
    all_files = dbx.files_list_folder(path="")
    print('.Success')

    print("Finding correct file")
    for item in all_files.entries:
        print('-', str(item.name.lower()))
        if item.name.lower() == file_name.lower():
            success_flag = True
            
            print("..Downloading file")
            meta, res = dbx.files_download(item.path_lower)
            print('..Success')

            #S3 side
            print('..Initalizing S3 connection')
            s3 = boto3.client('s3', region_name = aws_region)
            print('..Success')

            print("..Send to S3") # https://stackoverflow.com/questions/46677138/copy-files-from-dropbox-to-aws-s3-using-python
            s3.upload_fileobj(io.BytesIO(res.content), bucket_name, prefix+name)
            print('..Success')
        
        
        else:
            print('.')
    
    if success_flag == True:
        print('Full Success - file uploaded to ')
    else:
        print('Failure - no data uploaded to S3')
    
    return {
        'statusCode': 200,
        'body': json.dumps('hello world')
    }
