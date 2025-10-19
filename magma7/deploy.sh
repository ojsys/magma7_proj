#!/bin/bash

###############################################################################
# Magma7Fitness Deployment Script for cPanel
# This script helps automate common deployment tasks
###############################################################################

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "virtualenv" ] && [ ! -d "venv" ]; then
    print_error "Virtual environment not found!"
    print_info "Please create a virtual environment first"
    exit 1
fi

# Activate virtual environment
if [ -d "virtualenv" ]; then
    source virtualenv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

print_success "Virtual environment activated"

# Function to show menu
show_menu() {
    echo ""
    echo "╔════════════════════════════════════════════╗"
    echo "║   Magma7Fitness Deployment Menu           ║"
    echo "╚════════════════════════════════════════════╝"
    echo ""
    echo "1) Install Dependencies"
    echo "2) Run Migrations"
    echo "3) Collect Static Files"
    echo "4) Create Superuser"
    echo "5) Run All (1-3)"
    echo "6) Restart Application"
    echo "7) Check Status"
    echo "8) View Error Logs"
    echo "9) Backup Database"
    echo "0) Exit"
    echo ""
}

# Function to install dependencies
install_dependencies() {
    print_info "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_success "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        return 1
    fi
}

# Function to run migrations
run_migrations() {
    print_info "Running database migrations..."
    python manage.py makemigrations
    python manage.py migrate
    if [ $? -eq 0 ]; then
        print_success "Migrations completed successfully"
    else
        print_error "Migration failed"
        return 1
    fi
}

# Function to collect static files
collect_static() {
    print_info "Collecting static files..."
    python manage.py collectstatic --noinput
    if [ $? -eq 0 ]; then
        print_success "Static files collected successfully"
    else
        print_error "Failed to collect static files"
        return 1
    fi
}

# Function to create superuser
create_superuser() {
    print_info "Creating superuser..."
    python manage.py createsuperuser
}

# Function to restart application
restart_app() {
    print_info "Restarting application..."

    # Create tmp directory if it doesn't exist
    mkdir -p tmp

    # Touch restart.txt to trigger Passenger restart
    touch tmp/restart.txt

    # Also try the standard restart command
    if command -v passenger-config &> /dev/null; then
        passenger-config restart-app "$SCRIPT_DIR"
    fi

    print_success "Application restart triggered"
    print_info "Note: It may take a few seconds for changes to take effect"
}

# Function to check application status
check_status() {
    print_info "Checking application status..."
    echo ""

    # Check if .env exists
    if [ -f ".env" ]; then
        print_success ".env file exists"
    else
        print_error ".env file not found"
    fi

    # Check if static files directory exists
    if [ -d "staticfiles" ]; then
        print_success "staticfiles directory exists"
        echo "   Files: $(find staticfiles -type f | wc -l)"
    else
        print_error "staticfiles directory not found"
    fi

    # Check if media directory exists
    if [ -d "media" ]; then
        print_success "media directory exists"
    else
        print_error "media directory not found - creating it..."
        mkdir -p media
        chmod 755 media
    fi

    # Check if logs directory exists
    if [ -d "logs" ]; then
        print_success "logs directory exists"
    else
        print_error "logs directory not found - creating it..."
        mkdir -p logs
        chmod 755 logs
    fi

    # Check database connectivity
    print_info "Testing database connection..."
    python manage.py check --database default
    if [ $? -eq 0 ]; then
        print_success "Database connection OK"
    else
        print_error "Database connection failed"
    fi

    echo ""
}

# Function to view error logs
view_logs() {
    print_info "Viewing error logs (last 50 lines)..."
    echo ""

    if [ -f "logs/django_errors.log" ]; then
        tail -n 50 logs/django_errors.log
    else
        print_error "No error log file found"
    fi

    echo ""
    print_info "Press Enter to continue..."
    read
}

# Function to backup database
backup_database() {
    print_info "Creating database backup..."

    # Create backups directory if it doesn't exist
    mkdir -p backups

    # Get database credentials from .env
    if [ -f ".env" ]; then
        source .env

        BACKUP_FILE="backups/backup_$(date +%Y%m%d_%H%M%S).sql"

        if [ ! -z "$DB_NAME" ]; then
            print_info "Backing up database: $DB_NAME"
            mysqldump -u "$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" "$DB_NAME" > "$BACKUP_FILE"

            if [ $? -eq 0 ]; then
                print_success "Database backed up to: $BACKUP_FILE"

                # Compress the backup
                gzip "$BACKUP_FILE"
                print_success "Backup compressed: ${BACKUP_FILE}.gz"
            else
                print_error "Database backup failed"
            fi
        else
            print_error "Database credentials not found in .env"
        fi
    else
        print_error ".env file not found"
    fi
}

# Main loop
while true; do
    show_menu
    read -p "Choose an option: " choice

    case $choice in
        1)
            install_dependencies
            ;;
        2)
            run_migrations
            ;;
        3)
            collect_static
            ;;
        4)
            create_superuser
            ;;
        5)
            print_info "Running full deployment..."
            install_dependencies && run_migrations && collect_static
            if [ $? -eq 0 ]; then
                print_success "Full deployment completed!"
                print_info "Don't forget to restart the application (option 6)"
            fi
            ;;
        6)
            restart_app
            ;;
        7)
            check_status
            ;;
        8)
            view_logs
            ;;
        9)
            backup_database
            ;;
        0)
            print_info "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid option"
            ;;
    esac

    echo ""
    read -p "Press Enter to continue..."
done
