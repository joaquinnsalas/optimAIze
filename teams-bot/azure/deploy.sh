#!/bin/bash

# OptimAIze Teams Bot - Azure Deployment Script
# This script deploys the Teams bot to Azure App Service and Azure Bot Service

set -e  # Exit on any error

# Configuration
RESOURCE_GROUP="optimaize-teams-bot-rg"
LOCATION="East US"
BOT_NAME="optimaize-teams-bot"
APP_SERVICE_PLAN="optimaize-bot-plan"
APP_SERVICE_NAME="optimaize-teams-bot-app"
BOT_DISPLAY_NAME="OptimAIze Assistant"
BOT_DESCRIPTION="AI-powered document assistant for Altura Engineering"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Azure CLI is installed
    if ! command -v az &> /dev/null; then
        log_error "Azure CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check if logged in to Azure
    if ! az account show &> /dev/null; then
        log_error "Not logged in to Azure. Please run 'az login' first."
        exit 1
    fi
    
    # Check if required environment variables are set
    if [[ -z "$OPTIMAIZE_BACKEND_URL" ]]; then
        log_error "OPTIMAIZE_BACKEND_URL environment variable is required"
        exit 1
    fi
    
    if [[ -z "$ALTURA_TENANT_ID" ]]; then
        log_error "ALTURA_TENANT_ID environment variable is required"
        exit 1
    fi
    
    log_info "Prerequisites check passed ✓"
}

# Create resource group
create_resource_group() {
    log_info "Creating resource group: $RESOURCE_GROUP"
    
    az group create \
        --name $RESOURCE_GROUP \
        --location "$LOCATION" \
        --output table
    
    log_info "Resource group created ✓"
}

# Create user-assigned managed identity
create_managed_identity() {
    log_info "Creating user-assigned managed identity..."
    
    IDENTITY_NAME="${BOT_NAME}-identity"
    
    az identity create \
        --resource-group $RESOURCE_GROUP \
        --name $IDENTITY_NAME \
        --output table
    
    # Get the identity details
    IDENTITY_CLIENT_ID=$(az identity show \
        --resource-group $RESOURCE_GROUP \
        --name $IDENTITY_NAME \
        --query clientId \
        --output tsv)
    
    IDENTITY_PRINCIPAL_ID=$(az identity show \
        --resource-group $RESOURCE_GROUP \
        --name $IDENTITY_NAME \
        --query principalId \
        --output tsv)
    
    TENANT_ID=$(az account show --query tenantId --output tsv)
    
    log_info "Managed identity created ✓"
    log_info "Client ID: $IDENTITY_CLIENT_ID"
    log_info "Principal ID: $IDENTITY_PRINCIPAL_ID"
    log_info "Tenant ID: $TENANT_ID"
    
    # Export for later use
    export MICROSOFT_APP_ID=$IDENTITY_CLIENT_ID
    export MICROSOFT_APP_TENANT_ID=$TENANT_ID
    export MICROSOFT_APP_TYPE="UserAssignedMSI"
    export MICROSOFT_APP_PASSWORD=""  # Not needed for managed identity
}

# Create App Service Plan
create_app_service_plan() {
    log_info "Creating App Service Plan: $APP_SERVICE_PLAN"
    
    az appservice plan create \
        --name $APP_SERVICE_PLAN \
        --resource-group $RESOURCE_GROUP \
        --location "$LOCATION" \
        --sku F1 \
        --is-linux \
        --output table
    
    log_info "App Service Plan created ✓"
}

# Create App Service (Web App)
create_app_service() {
    log_info "Creating App Service: $APP_SERVICE_NAME"
    
    az webapp create \
        --name $APP_SERVICE_NAME \
        --resource-group $RESOURCE_GROUP \
        --plan $APP_SERVICE_PLAN \
        --runtime "PYTHON|3.11" \
        --output table
    
    # Configure app settings
    log_info "Configuring app settings..."
    
    az webapp config appsettings set \
        --name $APP_SERVICE_NAME \
        --resource-group $RESOURCE_GROUP \
        --settings \
            MICROSOFT_APP_ID=$MICROSOFT_APP_ID \
            MICROSOFT_APP_PASSWORD=$MICROSOFT_APP_PASSWORD \
            MICROSOFT_APP_TENANT_ID=$MICROSOFT_APP_TENANT_ID \
            MICROSOFT_APP_TYPE=$MICROSOFT_APP_TYPE \
            OPTIMAIZE_BACKEND_URL=$OPTIMAIZE_BACKEND_URL \
            ALTURA_TENANT_ID=$ALTURA_TENANT_ID \
            ALTURA_DOMAIN="alturaengineering.com" \
            LOG_LEVEL="INFO" \
            ENABLE_ANALYTICS_LOGGING="true" \
        --output table
    
    # Get the app service URL
    APP_SERVICE_URL=$(az webapp show \
        --name $APP_SERVICE_NAME \
        --resource-group $RESOURCE_GROUP \
        --query defaultHostName \
        --output tsv)
    
    log_info "App Service created ✓"
    log_info "App Service URL: https://$APP_SERVICE_URL"
    
    export BOT_ENDPOINT="https://$APP_SERVICE_URL/api/messages"
}

# Create Azure Bot Service
create_bot_service() {
    log_info "Creating Azure Bot Service: $BOT_NAME"
    
    az bot create \
        --resource-group $RESOURCE_GROUP \
        --name $BOT_NAME \
        --app-type UserAssignedMSI \
        --app-id $MICROSOFT_APP_ID \
        --tenant-id $MICROSOFT_APP_TENANT_ID \
        --endpoint $BOT_ENDPOINT \
        --display-name "$BOT_DISPLAY_NAME" \
        --description "$BOT_DESCRIPTION" \
        --output table
    
    log_info "Azure Bot Service created ✓"
}

# Enable Teams channel
enable_teams_channel() {
    log_info "Enabling Teams channel for bot..."
    
    az bot msteams create \
        --name $BOT_NAME \
        --resource-group $RESOURCE_GROUP \
        --output table
    
    log_info "Teams channel enabled ✓"
}

# Assign managed identity to App Service
assign_managed_identity() {
    log_info "Assigning managed identity to App Service..."
    
    az webapp identity assign \
        --name $APP_SERVICE_NAME \
        --resource-group $RESOURCE_GROUP \
        --identities "/subscriptions/$(az account show --query id --output tsv)/resourcegroups/$RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/${BOT_NAME}-identity" \
        --output table
    
    log_info "Managed identity assigned ✓"
}

# Deploy code to App Service
deploy_code() {
    log_info "Deploying code to App Service..."
    
    # Create deployment package
    cd ..  # Go back to project root
    
    # Create a zip file with the application code
    log_info "Creating deployment package..."
    
    # Create temporary directory for deployment files
    mkdir -p deploy-temp
    
    # Copy necessary files
    cp -r *.py deploy-temp/
    cp requirements.txt deploy-temp/
    cp .env deploy-temp/ 2>/dev/null || log_warn ".env file not found - using environment variables"
    
    # Create startup command file for Azure
    cat > deploy-temp/startup.sh << 'EOF'
#!/bin/bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
EOF
    chmod +x deploy-temp/startup.sh
    
    # Create zip file
    cd deploy-temp
    zip -r ../optimaize-teams-bot.zip .
    cd ..
    
    # Deploy to Azure
    az webapp deploy \
        --resource-group $RESOURCE_GROUP \
        --name $APP_SERVICE_NAME \
        --src-path optimaize-teams-bot.zip \
        --type zip \
        --output table
    
    # Configure startup command
    az webapp config set \
        --name $APP_SERVICE_NAME \
        --resource-group $RESOURCE_GROUP \
        --startup-file "startup.sh" \
        --output table
    
    # Clean up
    rm -rf deploy-temp optimaize-teams-bot.zip
    
    log_info "Code deployment completed ✓"
}

# Generate Teams app manifest
generate_teams_manifest() {
    log_info "Generating Teams app manifest..."
    
    # Update manifest with actual bot ID and domain
    sed -i.bak "s/{{BOT_ID}}/$MICROSOFT_APP_ID/g" teams-app/manifest.json
    sed -i.bak "s/{{BOT_DOMAIN}}/$APP_SERVICE_URL/g" teams-app/manifest.json
    
    # Create app package
    cd teams-app
    zip -r ../optimaize-teams-app.zip manifest.json color.png outline.png
    cd ..
    
    log_info "Teams app manifest generated ✓"
    log_info "App package: optimaize-teams-app.zip"
    log_info "Upload this package to Teams Admin Center or sideload it for testing"
}

# Main deployment function
main() {
    log_info "Starting OptimAIze Teams Bot deployment..."
    
    # Load environment variables if .env exists
    if [[ -f "../.env" ]]; then
        log_info "Loading environment variables from .env file..."
        export $(cat ../.env | grep -v '^#' | xargs)
    fi
    
    check_prerequisites
    
    log_info "Creating Azure resources..."
    create_resource_group
    create_managed_identity
    create_app_service_plan
    create_app_service
    create_bot_service
    enable_teams_channel
    assign_managed_identity
    
    log_info "Deploying application..."
    deploy_code
    
    log_info "Generating Teams app package..."
    generate_teams_manifest
    
    log_info ""
    log_info "🎉 Deployment completed successfully!"
    log_info ""
    log_info "📋 Deployment Summary:"
    log_info "   Resource Group: $RESOURCE_GROUP"
    log_info "   Bot Name: $BOT_NAME"
    log_info "   App Service: https://$APP_SERVICE_URL"
    log_info "   Bot ID: $MICROSOFT_APP_ID"
    log_info "   Bot Endpoint: $BOT_ENDPOINT"
    log_info ""
    log_info "🚀 Next Steps:"
    log_info "   1. Upload optimaize-teams-app.zip to Teams Admin Center"
    log_info "   2. Or sideload the app for testing in Teams"
    log_info "   3. Test the bot by messaging it in Teams"
    log_info "   4. Check logs: az webapp log tail --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP"
    log_info ""
    log_info "🔧 Useful Commands:"
    log_info "   - View logs: az webapp log tail --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP"
    log_info "   - Restart app: az webapp restart --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP"
    log_info "   - Update config: az webapp config appsettings set --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP --settings KEY=VALUE"
}

# Cleanup function (optional)
cleanup() {
    log_warn "Cleaning up deployment resources..."
    
    read -p "Are you sure you want to delete the resource group $RESOURCE_GROUP? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        az group delete --name $RESOURCE_GROUP --yes --no-wait
        log_info "Resource group deletion initiated"
    else
        log_info "Cleanup cancelled"
    fi
}

# Handle command line arguments
case "${1:-deploy}" in
    deploy)
        main
        ;;
    cleanup)
        cleanup
        ;;
    *)
        echo "Usage: $0 [deploy|cleanup]"
        echo "  deploy  - Deploy the Teams bot to Azure (default)"
        echo "  cleanup - Delete all Azure resources"
        exit 1
        ;;
esac