# 🖼️ Serverless Image Processing Application

This is a serverless application that automatically resizes and watermarks images uploaded to an S3 bucket using AWS Lambda.

---

## ✅ Features

- Upload image → Automatically processed via Lambda
- Resizes to thumbnail (200x200)
- Adds a watermark
- Stores final image in a separate S3 bucket

---

## 📌 Architecture Diagram

![Architecture]([Cloud Architecture.jpeg](https://lucid.app/lucidchart/85834a86-0a44-4642-a073-29fe20b3dfae/edit?invitationId=inv_9de66629-5c0d-400e-9f0d-fafbdc28464f))

---

## 🚀 How It Works

1. User uploads image to S3 (raw-images-bucket)
2. S3 triggers a Lambda function
3. Lambda resizes and watermarks the image
4. The image is saved to another S3 bucket (my-processed-images-123)

---

## 🧠 Technologies

- **Amazon S3** — Image storage
- **AWS Lambda** — Image processing
- **Pillow (PIL)** — Python image library
- **IAM Roles** — Secure access


---

## 📂 Repository Structure

```bash
lambda_function.py        # Core Lambda code
architecture-diagram.png  # Architecture overview
README.md                 # Documentation
