# config.py

# This file stores all application-level settings for CareSync.

# Application identity
APP_NAME = "CareSync"

<<<<<<< HEAD
APP_VERSION = "1.0.1"
=======
APP_VERSION = "1.1.0"
>>>>>>> origin/main

APP_DESCRIPTION = "Patient portal for hospital and clinic management"

# Database connection settings
DATABASE_HOST = "localhost"

DATABASE_PORT = 5432

DATABASE_NAME = "caresync_db"

DATABASE_USER = "caresync_user"

# User role definitions
ROLE_PATIENT = "patient"

ROLE_DOCTOR = "doctor"

ROLE_BILLING = "billing_staff"

# Pagination settings
DEFAULT_PAGE_SIZE = 20

MAX_PAGE_SIZE = 100