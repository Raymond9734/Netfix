#!/bin/bash

echo "Setting up your Django project..."

# Step 1: Create a virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Step 3: Install the required dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Apply migrations
echo "Applying migrations..."
python3 manage.py migrate

# Step 5: Create a .env file (if required)
if [ ! -f ".env" ]; then
  echo "Creating .env file..."
  touch .env
  echo "DJANGO_SECRET_KEY=$(openssl rand -base64 32)" >> .env
  echo "DEBUG=True" >> .env
  echo "ALLOWED_HOSTS=127.0.0.1,localhost" >> .env
#   echo "DATABASE_URL=sqlite:///db.sqlite3" >> .env
fi

# Step 6: Start the Django development server
echo "Starting the Django development server..."
python3 manage.py runserver

echo "Setup complete!"
