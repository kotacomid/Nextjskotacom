# 🚀 Panduan Deploy ke Vercel

Panduan lengkap untuk deploy portfolio website collection ke Vercel dengan mudah dan cepat.

## 📋 Prerequisites

1. **GitHub Account** - Untuk menyimpan kode
2. **Vercel Account** - Daftar gratis di [vercel.com](https://vercel.com)
3. **Git** - Terinstall di komputer Anda

## 🔧 Metode 1: Deploy Satu Website (Recommended)

### A. Persiapan Repository

1. **Pilih Website yang akan di-deploy:**
```bash
# Contoh: Deploy website klinik-sehat
cd portfolio-websites/healthcare/klinik-sehat/
```

2. **Inisialisasi Git Repository:**
```bash
git init
git add .
git commit -m "Initial commit: Klinik Sehat Prima website"
```

3. **Push ke GitHub:**
```bash
# Buat repository baru di GitHub dengan nama: klinik-sehat-website
git remote add origin https://github.com/username/klinik-sehat-website.git
git branch -M main
git push -u origin main
```

### B. Deploy di Vercel

1. **Login ke Vercel Dashboard:**
   - Kunjungi [vercel.com](https://vercel.com)
   - Login dengan GitHub account

2. **Import Project:**
   - Klik tombol **"Add New..."** > **"Project"**
   - Pilih **"Import Git Repository"**
   - Pilih repository yang baru dibuat
   - Klik **"Import"**

3. **Configure Project:**
   ```
   Project Name: klinik-sehat-prima
   Framework Preset: Other
   Root Directory: ./
   Build Command: (leave empty)
   Output Directory: ./
   Install Command: (leave empty)
   ```

4. **Deploy:**
   - Klik **"Deploy"**
   - Tunggu proses deployment selesai (1-2 menit)
   - Website akan tersedia di: `klinik-sehat-prima.vercel.app`

## 🔧 Metode 2: Deploy Website Next.js

### A. Deploy Website Jasa (Next.js Project)

1. **Masuk ke direktori project:**
```bash
cd website-jasa/
```

2. **Push ke GitHub:**
```bash
git init
git add .
git commit -m "Initial commit: WebJasa - Website Jasa Pembuatan Website"
git remote add origin https://github.com/username/webjasa-website.git
git branch -M main
git push -u origin main
```

3. **Deploy di Vercel:**
   - Import repository di Vercel Dashboard
   - Vercel akan otomatis detect Next.js project
   - Configuration akan ter-set otomatis:
   ```
   Framework Preset: Next.js
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

4. **Environment Variables (jika diperlukan):**
   - Tidak ada environment variables yang diperlukan untuk project ini

## 🌐 Metode 3: Deploy Multiple Websites (Advanced)

### A. Structure untuk Multiple Deployment

1. **Buat repository terpisah untuk setiap website:**
```bash
# Script untuk membuat multiple repositories
#!/bin/bash

websites=(
  "portfolio-websites/healthcare/klinik-sehat"
  "portfolio-websites/automotive/dealer-mobil"
  "portfolio-websites/automotive/sepeda-listrik"
  "portfolio-websites/business/toko-online"
  "portfolio-websites/business/restoran-cafe"
  "portfolio-websites/digital/digital-marketing"
  "portfolio-websites/government/sekolah-digital"
  "portfolio-websites/professional/arsitek-interior"
)

for website in "${websites[@]}"; do
  website_name=$(basename "$website")
  echo "Processing $website_name..."
  
  cd "$website"
  git init
  git add .
  git commit -m "Initial commit: $website_name website"
  
  # Push ke GitHub (ganti 'username' dengan GitHub username Anda)
  git remote add origin "https://github.com/username/$website_name-website.git"
  git branch -M main
  git push -u origin main
  
  cd ../../../..
done
```

### B. Bulk Import di Vercel

1. **Import semua repositories:**
   - Login ke Vercel Dashboard
   - Import masing-masing repository
   - Set custom domain jika diperlukan

## 🔗 Custom Domain Setup

### A. Tambah Custom Domain

1. **Di Vercel Dashboard:**
   - Pilih project yang sudah di-deploy
   - Masuk ke tab **"Settings"**
   - Pilih **"Domains"**
   - Tambahkan domain Anda

2. **DNS Configuration:**
```
Type: CNAME
Name: www
Value: your-project.vercel.app

Type: A
Name: @
Value: 76.76.19.19
```

### B. SSL Certificate
- Vercel otomatis provide SSL certificate
- HTTPS akan aktif dalam 24 jam

## ⚡ Performance Optimization

### A. Vercel.json Configuration

Untuk website HTML statis, buat file `vercel.json`:

```json
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
```

### B. Image Optimization

1. **Compress images sebelum deploy:**
```bash
# Install imagemin untuk optimasi gambar
npm install -g imagemin-cli imagemin-mozjpeg imagemin-pngquant

# Optimasi semua gambar
imagemin images/*.{jpg,png} --out-dir=images/optimized --plugin=mozjpeg --plugin=pngquant
```

## 📊 Monitoring & Analytics

### A. Vercel Analytics

1. **Enable Analytics:**
   - Masuk ke project settings
   - Enable "Analytics"
   - Gratis untuk personal projects

### B. Google Analytics Integration

Tambahkan ke `<head>` section:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
</script>
```

## 🛠️ Troubleshooting

### A. Common Issues

1. **Build Failed:**
   - Check file paths dan case sensitivity
   - Pastikan tidak ada broken links
   - Validate HTML markup

2. **404 Errors:**
   - Pastikan `index.html` ada di root directory
   - Check routing configuration

3. **Slow Loading:**
   - Optimize images
   - Minify CSS/JS
   - Use CDN untuk external resources

### B. Debug Commands

```bash
# Check HTML validation
npx html-validate index.html

# Test local build
npx serve .

# Check lighthouse score
npx lighthouse http://localhost:3000
```

## 📱 Mobile Testing

### A. Responsive Testing Tools

1. **Browser DevTools:**
   - F12 > Toggle device toolbar
   - Test berbagai ukuran layar

2. **Online Tools:**
   - [Responsive Design Checker](http://responsivedesignchecker.com/)
   - [Am I Responsive](http://ami.responsivedesign.is/)

## 🔐 Security Best Practices

### A. Content Security Policy

Tambahkan meta tag ke `<head>`:

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdnjs.cloudflare.com;
               script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com;
               font-src 'self' https://cdnjs.cloudflare.com;">
```

## 📈 SEO Optimization

### A. Meta Tags Checklist

Pastikan setiap halaman memiliki:

```html
<title>Judul Halaman - Brand Name</title>
<meta name="description" content="Deskripsi halaman maksimal 160 karakter">
<meta name="keywords" content="kata kunci, relevan, dengan, konten">
<meta name="author" content="Nama Perusahaan">

<!-- Open Graph -->
<meta property="og:title" content="Judul untuk Social Media">
<meta property="og:description" content="Deskripsi untuk Social Media">
<meta property="og:image" content="/images/og-image.jpg">
<meta property="og:url" content="https://domain.com">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Judul untuk Twitter">
<meta name="twitter:description" content="Deskripsi untuk Twitter">
<meta name="twitter:image" content="/images/twitter-image.jpg">
```

## 🎯 Final Checklist

### ✅ Pre-Deployment Checklist

- [ ] Semua links berfungsi dengan baik
- [ ] Images ter-optimize dan loading cepat
- [ ] Responsive design di semua devices
- [ ] Meta tags lengkap untuk SEO
- [ ] Contact forms berfungsi
- [ ] No console errors
- [ ] Performance score > 90
- [ ] Accessibility score > 90

### ✅ Post-Deployment Checklist

- [ ] Website accessible via domain
- [ ] SSL certificate aktif (HTTPS)
- [ ] Analytics tracking berfungsi
- [ ] Forms submit properly
- [ ] Mobile performance optimal
- [ ] Search engines dapat index
- [ ] Social media preview benar

## 📞 Support & Resources

### A. Official Documentation
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [HTML/CSS Best Practices](https://developer.mozilla.org/en-US/docs/Learn/HTML)

### B. Community Support
- [Vercel Discord](https://discord.gg/vercel)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/vercel)

---

## 🚀 Quick Start Commands

### Deploy Single Website:
```bash
# 1. Navigate to website directory
cd portfolio-websites/healthcare/klinik-sehat/

# 2. Initialize git
git init && git add . && git commit -m "Initial commit"

# 3. Push to GitHub
git remote add origin https://github.com/username/repo-name.git
git push -u origin main

# 4. Import to Vercel via dashboard
```

### Deploy Next.js Project:
```bash
# 1. Navigate to Next.js project
cd website-jasa/

# 2. Push to GitHub
git init && git add . && git commit -m "Initial commit"
git remote add origin https://github.com/username/webjasa.git
git push -u origin main

# 3. Import to Vercel (auto-detected as Next.js)
```

**Selamat! Website Anda sekarang live di internet! 🎉**