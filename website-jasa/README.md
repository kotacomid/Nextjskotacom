# WebJasa - Website Jasa Pembuatan Website

WebJasa adalah website jasa pembuatan website profesional dengan tema modern biru dan putih, dibuat menggunakan Next.js 14, TypeScript, dan Tailwind CSS. Website ini dirancang khusus untuk bisnis jasa pembuatan website di Indonesia.

## 🚀 Features

### Halaman Utama
- **Beranda** - Landing page dengan hero section, statistik, layanan, testimonial, dan CTA
- **Layanan** - Detail lengkap semua layanan yang ditawarkan dengan pricing
- **Harga** - Paket harga dengan perbandingan fitur dan add-ons
- **Review** - Testimoni klien, case studies, dan video testimonials
- **Blog** - Artikel dan insights seputar web development
- **Tentang Kami** - Company profile, visi misi, tim, dan achievements
- **FAQ** - Frequently asked questions dengan kategorisasi
- **Kontak** - Form kontak lengkap dengan informasi perusahaan

### Design & UX
- ✅ Modern blue and white theme (inspired by Cursor)
- ✅ Fully responsive design (mobile-first approach)
- ✅ Smooth animations and hover effects
- ✅ Professional typography (Inter font)
- ✅ Consistent component design system
- ✅ SEO optimized structure

### Technical Features
- ✅ Next.js 14 with App Router
- ✅ TypeScript for type safety
- ✅ Tailwind CSS for styling
- ✅ Component-based architecture
- ✅ Mobile responsive navigation
- ✅ Form handling with validation
- ✅ Optimized performance
- ✅ SEO meta tags

## 🛠️ Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Font**: Inter (Google Fonts)
- **Icons**: SVG icons (Heroicons style)
- **Deployment**: Vercel

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd website-jasa
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🏗️ Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Homepage
│   ├── blog/              # Blog page
│   ├── faq/               # FAQ page
│   ├── harga/             # Pricing page
│   ├── kontak/            # Contact page
│   ├── layanan/           # Services page
│   ├── review/            # Reviews page
│   └── tentang/           # About page
└── components/            # Reusable components
    ├── Navigation.tsx     # Main navigation
    └── Footer.tsx         # Footer component
```

## 🎨 Design System

### Colors
- **Primary Blue**: #2563eb
- **Primary Blue Dark**: #1d4ed8
- **Primary Blue Light**: #60a5fa
- **Accent Blue**: #3b82f6
- **Background**: #ffffff
- **Text Primary**: #0f172a
- **Text Secondary**: #475569

### Typography
- **Font Family**: Inter (system fallback)
- **Headings**: Font weights 600-800
- **Body text**: Font weight 400-500

### Components
- **Cards**: Gradient background with hover effects
- **Buttons**: Primary (blue) and secondary (outlined) variants
- **Forms**: Consistent input styling with focus states
- **Navigation**: Glass effect with responsive mobile menu

## 📱 Pages Overview

### 1. Beranda (Homepage)
- Hero section dengan CTA
- Statistik perusahaan
- Overview layanan
- Mengapa memilih kami
- Testimonial klien
- CTA section

### 2. Layanan (Services)
- Detail 6 layanan utama
- Fitur dan benefit setiap layanan
- Proses pengerjaan
- Teknologi yang digunakan
- CTA untuk konsultasi

### 3. Harga (Pricing)
- 3 paket utama (Starter, Professional, Enterprise)
- Paket custom
- Add-on services
- FAQ seputar harga
- Transparent pricing

### 4. Review (Testimonials)
- Statistik kepuasan klien
- Grid testimonial dengan rating
- Case studies dengan hasil terukur
- Video testimonials
- Trust signals per industri

### 5. Blog
- Featured articles
- Article grid dengan kategori
- Sidebar dengan popular posts
- Newsletter subscription
- CTA untuk layanan

### 6. Tentang Kami (About)
- Company story
- Visi & misi
- Core values
- Tim profesional
- Awards & recognition
- CTA kolaborasi

### 7. FAQ
- Kategorisasi pertanyaan
- Expandable answers
- Quick contact options
- Tips sebelum memulai proyek

### 8. Kontak (Contact)
- Form kontak lengkap
- Informasi perusahaan
- Jam operasional
- Quick contact links
- Mini FAQ

## 🚀 Deployment

### Vercel (Recommended)

1. Push code ke GitHub repository
2. Connect repository di Vercel dashboard
3. Deploy automatically

### Manual Deployment

1. Build the project:
```bash
npm run build
```

2. Start production server:
```bash
npm start
```

## 🔧 Customization

### Changing Colors
Update CSS custom properties in `src/app/globals.css`:

```css
:root {
  --primary-blue: #your-color;
  --primary-blue-dark: #your-color;
  /* ... other colors */
}
```

### Adding New Pages
1. Create new folder in `src/app/`
2. Add `page.tsx` file
3. Update navigation in `src/components/Navigation.tsx`

### Modifying Content
- Update text content directly in component files
- Modify testimonials, services, and other data in respective page files
- Update company information in footer and contact page

## 📝 Content Guidelines

### Bahasa Indonesia
- Gunakan bahasa formal tapi friendly
- Fokus pada benefit untuk bisnis
- Include social proof dan testimonial
- CTA yang jelas dan persuasive

### SEO Optimization
- Meta titles dan descriptions
- Proper heading hierarchy (H1, H2, H3)
- Alt text untuk images
- Internal linking structure
- Fast loading performance

## 🔍 Performance

- Lighthouse Score: 90+ (Performance, Accessibility, Best Practices, SEO)
- Core Web Vitals optimized
- Image optimization with Next.js
- CSS optimization with Tailwind
- Minimal JavaScript bundle

## 📞 Support

Jika ada pertanyaan atau butuh bantuan:
- Email: info@webjasa.com
- WhatsApp: +62 812-3456-7890
- Website: https://webjasa.com

## 📄 License

This project is proprietary and confidential. All rights reserved.

---

**Dibuat dengan ❤️ untuk bisnis Indonesia**
