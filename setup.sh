#!/bin/bash

echo "Setting up your Django project..."

# Step 0: Ensure python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install python3 and try again."
    exit 1
fi

# Step 1: Create a virtual environment
if [ ! -d "my_env-Netfix" ]; then
    echo "Creating virtual environment..."
    python3 -m venv my_env-Netfix
fi

# Step 2: Activate the virtual environment (handles Unix/macOS and Windows)
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    source my_env-Netfix/bin/activate
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    source my_env-Netfix/Scripts/activate
else
    echo "Error: Unsupported OS for virtual environment activation"
    exit 1
fi

# Step 3: Install the required dependencies
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found. Please ensure it exists."
    deactivate
    exit 1
fi

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

  # Check if openssl is available
  if command -v openssl &> /dev/null; then
    echo "DJANGO_SECRET_KEY='$(openssl rand -base64 32)'" >> .env
  else
    echo "Error: openssl not found. Please install openssl to generate a secret key."
    echo "DJANGO_SECRET_KEY='<manually-add-secret-key>'" >> .env
  fi

  echo "DEBUG=True" >> .env
  echo "ALLOWED_HOSTS=127.0.0.1,localhost" >> .env
#   echo "DATABASE_URL=sqlite:///db.sqlite3" >> .env
fi

# Step 6: Start the Django development server
echo "Starting the Django development server..."
python3 manage.py runserver

echo "Setup complete!"
