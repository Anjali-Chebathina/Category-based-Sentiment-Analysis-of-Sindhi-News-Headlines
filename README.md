# install requirements
pip install -r requirements.txt

# Apply all migrations
python manage.py migrate

# Create Superuser
python manage.py createsuperuser
## Enter username, email, and password when prompted

## Load Sample Data
# Run the dataset creation script
python create_sample_dataset.py

#  Train Models
python train_models.py

# Run Development Server
python manage.py runserver

# Training Models (First Time Setup)
## Login as Admin
Go to http://127.0.0.1:8000/accounts/login/

Create an admin user or update existing user's role to 'admin' in Django admin

## Upload Dataset (if needed)
Go to Admin Dashboard → Manage Dataset

Upload the sample_headlines.csv file

Verify headlines are imported

## Train Models
Go to Admin Dashboard

Click "Train Sentiment Analysis Model"

Wait for training to complete

Click "Train Classification Model"

Verify model performance metrics

