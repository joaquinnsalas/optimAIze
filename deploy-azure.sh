#!/bin/bash

# deploy-azure.sh - Deploy OptimAIze to Azure Web Apps

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration
RESOURCE_GROUP_NAME=${RESOURCE_GROUP_NAME:-"optimaize-rg"}
APP_SERVICE_PLAN=${APP_SERVICE_PLAN:-"optimaize-plan"}
WEB_APP_NAME=${WEB_APP_NAME:-"optimaize-app-$(date +%s)"}
LOCATION=${LOCATION:-"eastus"}
PYTHON_VERSION="3.11"

# Check if Azure CLI is installed
check_azure_cli() {
    if ! command -v az &> /dev/null; then
        log_error "Azure CLI is required but not installed"
        log_info "Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
        exit 1
    fi
    
    # Check if logged in
    if ! az account show > /dev/null 2>&1; then
        log_error "Not logged into Azure CLI"
        log_info "Run: az login"
        exit 1
    fi
    
    log_info "Azure CLI ready ✓"
}

create_azure_resources() {
    log_info "Creating Azure resources..."
    
    # Create resource group
    log_info "Creating resource group: $RESOURCE_GROUP_NAME"
    az group create --name "$RESOURCE_GROUP_NAME" --location "$LOCATION"
    
    # Create App Service Plan
    log_info "Creating App Service Plan: $APP_SERVICE_PLAN"
    az appservice plan create \
        --name "$APP_SERVICE_PLAN" \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --sku "B1" \
        --is-linux
    
    # Create Web App
    log_info "Creating Web App: $WEB_APP_NAME"
    az webapp create \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --plan "$APP_SERVICE_PLAN" \
        --name "$WEB_APP_NAME" \
        --runtime "PYTHON|$PYTHON_VERSION" \
        --deployment-local-git
    
    log_info "Azure resources created ✓"
}

configure_web_app() {
    log_info "Configuring Web App settings..."
    
    # Set Python version
    az webapp config set \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$WEB_APP_NAME" \
        --linux-fx-version "PYTHON|$PYTHON_VERSION"
    
    # Configure startup command
    az webapp config set \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$WEB_APP_NAME" \
        --startup-file "startup.sh start"
    
    # Set environment variables
    az webapp config appsettings set \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$WEB_APP_NAME" \
        --settings \
        ENVIRONMENT="azure" \
        PYTHONPATH="/home/site/wwwroot" \
        SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
        ENABLE_ORYX_BUILD="true" \
        WEBSITES_ENABLE_APP_SERVICE_STORAGE="false"
    
    log_info "Web App configured ✓"
}

setup_external_services() {
    log_info "Setting up external services for Azure..."
    
    # These would be actual Azure services in production
    log_warn "External services setup required:"
    log_info "1. Create Azure Container Instances for:"
    log_info "   - Qdrant (vector database)"
    log_info "   - Elasticsearch (keyword search)"
    log_info "   - Ollama (LLM service)"
    log_info "2. Or use Azure alternatives:"
    log_info "   - Azure AI Search (replaces Elasticsearch)"
    log_info "   - Azure OpenAI (replaces Ollama)"
    log_info "   - Azure Database for PostgreSQL (with vector extension)"
    
    echo ""
    log_info "For now, we'll use placeholder URLs"
    log_info "Update these in Azure Portal > Web App > Configuration:"
    
    # Set placeholder service URLs
    az webapp config appsettings set \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$WEB_APP_NAME" \
        --settings \
        QDRANT_URL="https://your-qdrant-instance.azurecontainer.io:6333" \
        ELASTICSEARCH_URL="https://your-elasticsearch-instance.azurecontainer.io:9200" \
        OLLAMA_URL="https://your-ollama-instance.azurecontainer.io:11434"
}

deploy_code() {
    log_info "Deploying code to Azure..."
    
    # Get Git URL
    GIT_URL=$(az webapp deployment source config-local-git \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$WEB_APP_NAME" \
        --query url -o tsv)
    
    # Add Azure remote if it doesn't exist
    if ! git remote get-url azure > /dev/null 2>&1; then
        log_info "Adding Azure Git remote..."
        git remote add azure "$GIT_URL"
    fi
    
    # Create deployment branch
    git checkout -b azure-deploy 2>/dev/null || git checkout azure-deploy
    
    # Create Azure-specific files
    create_azure_files
    
    # Commit changes
    git add .
    git commit -m "Azure deployment configuration" || true
    
    # Deploy
    log_info "Pushing to Azure (this may take a few minutes)..."
    git push azure azure-deploy:master
    
    log_info "Code deployed ✓"
}

create_azure_files() {
    log_info "Creating Azure-specific files..."
    
    # Create startup.sh if it doesn't exist (use the one we created earlier)
    if [ ! -f "startup.sh" ]; then
        log_error "startup.sh not found! Please create it first."
        exit 1
    fi
    
    # Make startup.sh executable
    chmod +x startup.sh
    
    # Create .deployment file for Azure
    cat > .deployment << 'EOF'
[config]
command = bash startup.sh setup
EOF
    
    # Create runtime.txt for Python version
    echo "python-$PYTHON_VERSION" > runtime.txt
    
    # Create requirements-azure.txt with additional Azure dependencies
    cat requirements.txt > requirements-azure.txt
    cat >> requirements-azure.txt << 'EOF'

# Azure-specific dependencies
azure-identity>=1.15.0
azure-storage-blob>=12.19.0
gunicorn>=21.2.0
EOF
    
    log_info "Azure files created ✓"
}

show_deployment_info() {
    WEB_APP_URL="https://$WEB_APP_NAME.azurewebsites.net"
    
    echo ""
    log_info "🎉 Deployment complete!"
    echo ""
    log_info "📱 Web App URL: $WEB_APP_URL"
    log_info "📚 API Documentation: $WEB_APP_URL/docs"
    log_info "🔍 Health Check: $WEB_APP_URL/health"
    echo ""
    log_info "📊 Monitor logs with:"
    echo "   az webapp log tail --resource-group $RESOURCE_GROUP_NAME --name $WEB_APP_NAME"
    echo ""
    log_warn "⚠️  Remember to configure external services:"
    log_info "1. Update service URLs in Azure Portal"
    log_info "2. Upload your documents to /home/site/wwwroot/data/input"
    log_info "3. Run indexing: POST $WEB_APP_URL/admin/index"
}

cleanup_deployment() {
    log_info "Cleaning up deployment artifacts..."
    git checkout main
    git branch -D azure-deploy 2>/dev/null || true
    rm -f .deployment runtime.txt requirements-azure.txt
}

show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy    - Full deployment to Azure"
    echo "  create    - Create Azure resources only"
    echo "  config    - Configure Web App only" 
    echo "  push      - Deploy code only"
    echo "  info      - Show deployment info"
    echo "  cleanup   - Remove Azure resources"
    echo "  help      - Show this help"
    echo ""
    echo "Environment Variables:"
    echo "  RESOURCE_GROUP_NAME - Azure resource group"
    echo "  WEB_APP_NAME        - Web app name"
    echo "  LOCATION            - Azure region"
}

cleanup_azure_resources() {
    log_warn "This will delete all Azure resources!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Deleting resource group: $RESOURCE_GROUP_NAME"
        az group delete --name "$RESOURCE_GROUP_NAME" --yes --no-wait
        log_info "Cleanup initiated (running in background)"
    else
        log_info "Cleanup cancelled"
    fi
}

# Main execution
main() {
    case "${1:-deploy}" in
        "deploy")
            check_azure_cli
            create_azure_resources
            configure_web_app
            setup_external_services
            deploy_code
            show_deployment_info
            ;;
        "create")
            check_azure_cli
            create_azure_resources
            ;;
        "config")
            configure_web_app
            setup_external_services
            ;;
        "push")
            deploy_code
            ;;
        "info")
            show_deployment_info
            ;;
        "cleanup")
            cleanup_azure_resources
            cleanup_deployment
            ;;
        "help"|"--help"|"-h")
            show_usage
            ;;
        *)
            log_error "Unknown command: $1"
            show_usage
            exit 1
            ;;
    esac
}

main "$@"