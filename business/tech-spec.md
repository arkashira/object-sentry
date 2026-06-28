# Tech Spec
## Stack
* Language: Python 3.10
* Framework: FastAPI 0.92.0
* Runtime: Uvicorn 0.18.3 with Gunicorn 20.1.0
* Computer Vision Library: OpenCV 4.6.0
* Machine Learning Library: PyTorch 1.12.1

## Hosting
* Primary Platform: AWS
* Free Tier: AWS Free Tier (12 months)
* Specific Services:
	+ AWS EC2 (t3.micro) for compute
	+ AWS S3 for storage
	+ AWS RDS (PostgreSQL) for database
	+ AWS Elastic Beanstalk for deployment

## Data Model
* **Images Table**
	+ id (primary key, UUID)
	+ image_data (byte array)
	+ uploaded_at (timestamp)
* **Objects Table**
	+ id (primary key, UUID)
	+ image_id (foreign key referencing Images Table)
	+ object_type (string)
	+ object_data (JSON)
	+ detected_at (timestamp)
* **Users Table**
	+ id (primary key, UUID)
	+ username (string)
	+ email (string)
	+ password (string, hashed)
	+ created_at (timestamp)

## API Surface
### Image Endpoints
* **POST /images**: Upload a new image
	+ Request Body: image_data (byte array)
	+ Response: 201 Created with image_id (UUID)
* **GET /images/{image_id}**: Retrieve an image by ID
	+ Response: 200 OK with image_data (byte array)
### Object Detection Endpoints
* **POST /objects**: Detect objects in an uploaded image
	+ Request Body: image_id (UUID)
	+ Response: 200 OK with object_data (JSON)
* **GET /objects/{object_id}**: Retrieve an object by ID
	+ Response: 200 OK with object_data (JSON)
### User Endpoints
* **POST /users**: Create a new user
	+ Request Body: username (string), email (string), password (string)
	+ Response: 201 Created with user_id (UUID)
* **GET /users/{user_id}**: Retrieve a user by ID
	+ Response: 200 OK with user_data (JSON)

## Security Model
* **Authentication**: JSON Web Tokens (JWT) with HS256 algorithm
* **Authorization**: Role-Based Access Control (RBAC) with three roles: admin, user, guest
* **Secrets Management**: AWS Secrets Manager
* **IAM**: AWS IAM with least privilege principle

## Observability
* **Logs**: AWS CloudWatch Logs
* **Metrics**: AWS CloudWatch Metrics
* **Traces**: AWS X-Ray

## Build/CI
* **Build Tool**: Docker 20.10.17
* **CI/CD Pipeline**: GitHub Actions with Python 3.10 environment
* **Test Framework**: Pytest 7.1.2
* **Code Coverage**: 80% minimum coverage required for merge
* **Deployment**: Automated deployment to AWS Elastic Beanstalk on merge to main branch