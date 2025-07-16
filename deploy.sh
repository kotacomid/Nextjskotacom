#!/bin/bash

# 🚀 Portfolio Website Deployment Script
# Script otomatis untuk deploy website ke Vercel

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if git is installed
check_git() {
    if ! command -v git &> /dev/null; then
        print_error "Git tidak terinstall. Silakan install Git terlebih dahulu."
        exit 1
    fi
}

# Check if vercel CLI is installed
check_vercel_cli() {
    if ! command -v vercel &> /dev/null; then
        print_warning "Vercel CLI tidak terinstall."
        read -p "Install Vercel CLI sekarang? (y/n): " install_vercel
        if [[ $install_vercel == "y" || $install_vercel == "Y" ]]; then
            npm install -g vercel
        else
            print_error "Vercel CLI diperlukan untuk deployment otomatis."
            exit 1
        fi
    fi
}

# List available websites
list_websites() {
    echo
    print_status "🌐 Daftar Website yang Tersedia:"
    echo
    
    websites=(
        "portfolio-websites/healthcare/klinik-sehat|Klinik Sehat Prima - Website Klinik Modern"
        "portfolio-websites/automotive/dealer-mobil|AutoPrime Dealer - Website Dealer Mobil"
        "portfolio-websites/automotive/sepeda-listrik|EcoBike Indonesia - Toko Sepeda Listrik"
        "portfolio-websites/business/toko-online|ShopMart - E-commerce Modern"
        "portfolio-websites/business/restoran-cafe|Cafe Nusantara - Website Restoran"
        "portfolio-websites/digital/digital-marketing|DigitalBoost Agency - Digital Marketing"
        "portfolio-websites/government/sekolah-digital|SMAN 1 Digital - Website Sekolah Modern"
        "portfolio-websites/professional/arsitek-interior|Visionary Design Studio - Arsitektur & Interior"
        "website-jasa|WebJasa - Website Jasa Pembuatan Website (Next.js)"
    )
    
    for i in "${!websites[@]}"; do
        IFS='|' read -ra ADDR <<< "${websites[$i]}"
        path="${ADDR[0]}"
        description="${ADDR[1]}"
        echo "$((i+1)). $description"
        echo "   📁 Path: $path"
        echo
    done
}

# Deploy single website
deploy_website() {
    local website_path=$1
    local website_name=$2
    
    if [[ ! -d "$website_path" ]]; then
        print_error "Direktori $website_path tidak ditemukan!"
        exit 1
    fi
    
    print_status "🚀 Memulai deployment untuk: $website_name"
    print_status "📁 Path: $website_path"
    
    # Navigate to website directory
    cd "$website_path"
    
    # Check if index.html exists (for static sites)
    if [[ -f "index.html" ]]; then
        print_status "📄 Terdeteksi sebagai static HTML website"
        
        # Create vercel.json for static deployment
        if [[ ! -f "vercel.json" ]]; then
            cat > vercel.json << EOF
{
  "builds": [
    {
      "src": "*.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/",
      "dest": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=86400"
        }
      ]
    }
  ]
}
EOF
            print_success "✅ vercel.json dibuat untuk optimasi deployment"
        fi
    elif [[ -f "package.json" ]]; then
        print_status "📦 Terdeteksi sebagai Node.js project"
    fi
    
    # Initialize git if not already initialized
    if [[ ! -d ".git" ]]; then
        print_status "🔧 Inisialisasi Git repository..."
        git init
        git add .
        git commit -m "Initial commit: $website_name"
        print_success "✅ Git repository berhasil diinisialisasi"
    else
        print_status "📝 Git repository sudah ada, menambahkan perubahan..."
        git add .
        if git diff --staged --quiet; then
            print_warning "⚠️  Tidak ada perubahan untuk di-commit"
        else
            git commit -m "Update: $(date '+%Y-%m-%d %H:%M:%S')"
            print_success "✅ Perubahan berhasil di-commit"
        fi
    fi
    
    # Deploy with Vercel CLI
    print_status "🚀 Memulai deployment ke Vercel..."
    
    # Create .vercelignore if needed
    if [[ ! -f ".vercelignore" ]]; then
        cat > .vercelignore << EOF
.git
.DS_Store
*.log
node_modules
.env.local
.env.development.local
.env.test.local
.env.production.local
EOF
    fi
    
    # Deploy
    vercel --prod
    
    if [[ $? -eq 0 ]]; then
        print_success "🎉 Website berhasil di-deploy!"
        print_success "🌐 Website Anda sekarang live di internet!"
    else
        print_error "❌ Deployment gagal. Silakan cek error di atas."
        exit 1
    fi
    
    # Return to original directory
    cd - > /dev/null
}

# Interactive website selection
select_website() {
    websites=(
        "portfolio-websites/healthcare/klinik-sehat|Klinik Sehat Prima"
        "portfolio-websites/automotive/dealer-mobil|AutoPrime Dealer"
        "portfolio-websites/automotive/sepeda-listrik|EcoBike Indonesia"
        "portfolio-websites/business/toko-online|ShopMart"
        "portfolio-websites/business/restoran-cafe|Cafe Nusantara"
        "portfolio-websites/digital/digital-marketing|DigitalBoost Agency"
        "portfolio-websites/government/sekolah-digital|SMAN 1 Digital"
        "portfolio-websites/professional/arsitek-interior|Visionary Design Studio"
        "website-jasa|WebJasa (Next.js)"
    )
    
    echo
    print_status "Pilih website yang ingin di-deploy:"
    
    for i in "${!websites[@]}"; do
        IFS='|' read -ra ADDR <<< "${websites[$i]}"
        description="${ADDR[1]}"
        echo "$((i+1)). $description"
    done
    
    echo
    read -p "Masukkan nomor pilihan (1-${#websites[@]}): " choice
    
    if [[ $choice -ge 1 && $choice -le ${#websites[@]} ]]; then
        selected_index=$((choice-1))
        IFS='|' read -ra ADDR <<< "${websites[$selected_index]}"
        selected_path="${ADDR[0]}"
        selected_name="${ADDR[1]}"
        
        deploy_website "$selected_path" "$selected_name"
    else
        print_error "Pilihan tidak valid!"
        exit 1
    fi
}

# Deploy all websites
deploy_all() {
    websites=(
        "portfolio-websites/healthcare/klinik-sehat|Klinik Sehat Prima"
        "portfolio-websites/automotive/dealer-mobil|AutoPrime Dealer"
        "portfolio-websites/automotive/sepeda-listrik|EcoBike Indonesia"
        "portfolio-websites/business/toko-online|ShopMart"
        "portfolio-websites/business/restoran-cafe|Cafe Nusantara"
        "portfolio-websites/digital/digital-marketing|DigitalBoost Agency"
        "portfolio-websites/government/sekolah-digital|SMAN 1 Digital"
        "portfolio-websites/professional/arsitek-interior|Visionary Design Studio"
        "website-jasa|WebJasa (Next.js)"
    )
    
    print_status "🚀 Memulai deployment semua website..."
    
    for website in "${websites[@]}"; do
        IFS='|' read -ra ADDR <<< "$website"
        path="${ADDR[0]}"
        name="${ADDR[1]}"
        
        if [[ -d "$path" ]]; then
            echo
            print_status "================================================"
            deploy_website "$path" "$name"
            print_status "================================================"
            echo
            sleep 2  # Wait a bit between deployments
        else
            print_warning "⚠️  Direktori $path tidak ditemukan, skip..."
        fi
    done
    
    print_success "🎉 Semua website berhasil di-deploy!"
}

# Main menu
show_menu() {
    echo
    echo "🚀 Portfolio Website Deployment Tool"
    echo "====================================="
    echo
    echo "1. Deploy satu website"
    echo "2. Deploy semua website"
    echo "3. Lihat daftar website"
    echo "4. Install Vercel CLI"
    echo "5. Login ke Vercel"
    echo "6. Keluar"
    echo
    read -p "Pilih opsi (1-6): " option
    
    case $option in
        1)
            select_website
            ;;
        2)
            deploy_all
            ;;
        3)
            list_websites
            show_menu
            ;;
        4)
            npm install -g vercel
            print_success "✅ Vercel CLI berhasil diinstall"
            show_menu
            ;;
        5)
            vercel login
            print_success "✅ Login ke Vercel berhasil"
            show_menu
            ;;
        6)
            print_success "👋 Terima kasih! Selamat menggunakan website Anda!"
            exit 0
            ;;
        *)
            print_error "Pilihan tidak valid!"
            show_menu
            ;;
    esac
}

# Main execution
main() {
    clear
    
    print_status "🔍 Memeriksa dependencies..."
    check_git
    
    # Check if we're in the right directory
    if [[ ! -d "portfolio-websites" && ! -d "website-jasa" ]]; then
        print_error "❌ Script harus dijalankan dari root directory project!"
        print_error "   Pastikan Anda berada di direktori yang berisi folder 'portfolio-websites'"
        exit 1
    fi
    
    print_success "✅ Environment check passed"
    
    # Show main menu
    show_menu
}

# Check for command line arguments
if [[ $# -eq 0 ]]; then
    main
else
    case $1 in
        --list)
            list_websites
            ;;
        --deploy)
            if [[ -n $2 ]]; then
                deploy_website "$2" "$(basename $2)"
            else
                print_error "Usage: $0 --deploy <website-path>"
                exit 1
            fi
            ;;
        --deploy-all)
            deploy_all
            ;;
        --help)
            echo "Portfolio Website Deployment Tool"
            echo
            echo "Usage:"
            echo "  $0                    # Interactive mode"
            echo "  $0 --list            # List available websites"
            echo "  $0 --deploy <path>   # Deploy specific website"
            echo "  $0 --deploy-all      # Deploy all websites"
            echo "  $0 --help           # Show this help"
            ;;
        *)
            print_error "Unknown option: $1"
            print_error "Use $0 --help for usage information"
            exit 1
            ;;
    esac
fi