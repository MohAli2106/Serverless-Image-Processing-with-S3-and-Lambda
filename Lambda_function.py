import boto3
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.parse

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get uploaded file details
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    print(f"Triggered by file: s3://{bucket}/{key}")
    
    # Download image from S3
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
    except s3.exceptions.NoSuchKey:
        print(f"Error: Object with key '{key}' not found in bucket '{bucket}'")
        raise

    image_data = response['Body'].read()
    
    # Open and resize image
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail((200, 200))
    
    # Convert RGBA or other formats to RGB before saving as JPEG
    if image.mode in ("RGBA", "LA"):
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1])
        image = background
    elif image.mode != "RGB":
        image = image.convert("RGB")

    # Add watermark
    draw = ImageDraw.Draw(image)
    watermark_text = "© YourBrand"
    
    # Load font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except:
        font = ImageFont.load_default()

    # Use textbbox instead of textsize
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    margin = 10
    x = image.width - text_width - margin
    y = image.height - text_height - margin

    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255))  # White text

    # Convert image to byte stream
    buffer = io.BytesIO()
    image.save(buffer, "JPEG")
    buffer.seek(0)

    # Upload to processed bucket
    processed_bucket = "my-processed-images-123"  # Replace with your real bucket name

    s3.put_object(
        Bucket=processed_bucket,
        Key=f"resized/{key}",
        Body=buffer,
        ContentType="image/jpeg"
    )
    
    return {
        'statusCode': 200,
        'body': f'Successfully processed and watermarked {key}'
    }
