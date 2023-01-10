
import boto3

# Create a client to access the resources from the Amazon Textract service 
textract_client = boto3.client('textract')

# Create an S3 bucket in AWS
s3_client = boto3.client('s3')

# Upload the PDF document to the S3 bucket
# s3_client.upload_file('ai_marketing_sales_pdfs/ai_adoption_in_monopoly_market.pdf', 'ai_marketing_sales_pdfs', 'ai_adoption_in_monopoly_market.pdf')

# Call Amazon Textract
response = textract_client.detect_document_text(Document={'S3Object': {'Bucket': 'ai-marketing-pdf', 'Name': 'ai_adoption_in_monopoly_market.pdf'}})

# Print extracted text 
text = response['Document']['Blocks']
print("Extracted Text:")
for item in text:
    if item['BlockType'] == 'LINE':
        print (item['Text'])