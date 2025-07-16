import Link from 'next/link'

export default function HargaPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Paket Harga Website
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Pilih paket yang sesuai dengan kebutuhan dan budget Anda. 
            Semua paket termasuk konsultasi gratis dan garansi kepuasan.
          </p>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                name: "Starter",
                price: "1,500,000",
                period: "sekali bayar",
                description: "Cocok untuk landing page atau website personal",
                popular: false,
                features: [
                  "1 Halaman Landing Page",
                  "Design Modern & Responsive",
                  "Contact Form",
                  "Google Analytics",
                  "SEO Basic",
                  "SSL Certificate",
                  "Hosting 1 Tahun",
                  "Support 1 Bulan"
                ],
                cta: "Mulai Sekarang",
                highlight: false
              },
              {
                name: "Professional",
                price: "2,500,000",
                period: "sekali bayar",
                description: "Ideal untuk website bisnis dan company profile",
                popular: true,
                features: [
                  "5-7 Halaman Website",
                  "Design Custom Premium",
                  "Contact Form & WhatsApp Integration",
                  "Google Analytics & Search Console",
                  "SEO Optimization",
                  "SSL Certificate",
                  "Hosting 1 Tahun",
                  "Support 3 Bulan",
                  "Admin Panel",
                  "Gallery/Portfolio Section"
                ],
                cta: "Paling Populer",
                highlight: true
              },
              {
                name: "Enterprise",
                price: "4,500,000",
                period: "sekali bayar",
                description: "Solusi lengkap untuk e-commerce dan sistem kompleks",
                popular: false,
                features: [
                  "Website E-Commerce Lengkap",
                  "Unlimited Halaman",
                  "Payment Gateway Integration",
                  "Product Management System",
                  "Order & Inventory Management",
                  "Customer Account System",
                  "Advanced SEO",
                  "Hosting 1 Tahun",
                  "Support 6 Bulan",
                  "Training & Documentation"
                ],
                cta: "Konsultasi Gratis",
                highlight: false
              }
            ].map((plan, index) => (
              <div key={index} className={`relative rounded-2xl p-8 ${plan.highlight ? 'bg-gradient-to-br from-blue-600 to-blue-700 text-white transform scale-105' : 'card-gradient'} hover-lift`}>
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-yellow-400 text-gray-900 px-4 py-1 rounded-full text-sm font-semibold">
                      PALING POPULER
                    </span>
                  </div>
                )}
                
                <div className="text-center mb-8">
                  <h3 className={`text-2xl font-bold mb-2 ${plan.highlight ? 'text-white' : 'text-gray-900'}`}>
                    {plan.name}
                  </h3>
                  <div className="mb-4">
                    <span className={`text-4xl font-bold ${plan.highlight ? 'text-white' : 'text-blue-600'}`}>
                      Rp {plan.price}
                    </span>
                    <span className={`block text-sm ${plan.highlight ? 'text-blue-100' : 'text-gray-500'}`}>
                      {plan.period}
                    </span>
                  </div>
                  <p className={`${plan.highlight ? 'text-blue-100' : 'text-gray-600'}`}>
                    {plan.description}
                  </p>
                </div>

                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center">
                      <svg className={`w-5 h-5 mr-3 ${plan.highlight ? 'text-green-300' : 'text-green-500'}`} fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      <span className={`${plan.highlight ? 'text-white' : 'text-gray-600'}`}>
                        {feature}
                      </span>
                    </li>
                  ))}
                </ul>

                <Link
                  href="/kontak"
                  className={`block w-full text-center py-3 px-6 rounded-lg font-semibold transition-all duration-300 ${
                    plan.highlight 
                      ? 'bg-white text-blue-600 hover:bg-gray-100' 
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  {plan.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Custom Package */}
      <section className="section-padding bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
            Butuh Paket Custom?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Setiap bisnis memiliki kebutuhan yang unik. Tim kami siap membuat solusi khusus 
            yang disesuaikan dengan requirement dan budget Anda.
          </p>
          <div className="card-gradient rounded-xl p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">Paket Custom</h3>
            <p className="text-gray-600 mb-6">
              Konsultasikan kebutuhan spesifik Anda dan dapatkan proposal yang disesuaikan 
              dengan goals bisnis dan anggaran yang tersedia.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Yang Bisa Kami Buat:</h4>
                <ul className="space-y-2 text-left">
                  {[
                    "Website dengan fitur khusus",
                    "Integrasi sistem existing",
                    "Multi-platform application",
                    "Custom admin dashboard",
                    "API development",
                    "Database design"
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-center text-gray-600">
                      <svg className="w-4 h-4 text-blue-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Proses Custom:</h4>
                <ul className="space-y-2 text-left">
                  {[
                    "Analisis kebutuhan detail",
                    "Proposal & timeline",
                    "Development iteratif",
                    "Testing menyeluruh",
                    "Training & handover",
                    "Long-term support"
                  ].map((item, idx) => (
                    <li key={idx} className="flex items-center text-gray-600">
                      <svg className="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <Link
              href="/kontak"
              className="btn-primary inline-block"
            >
              Diskusi Kebutuhan Custom
            </Link>
          </div>
        </div>
      </section>

      {/* Add-ons */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Layanan Tambahan
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Tingkatkan performa website Anda dengan layanan tambahan yang kami sediakan
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                name: "SEO Optimization",
                price: "1,000,000",
                period: "/bulan",
                description: "Tingkatkan ranking website di mesin pencari",
                features: [
                  "Keyword research",
                  "On-page SEO",
                  "Content optimization",
                  "Monthly report"
                ]
              },
              {
                name: "Maintenance",
                price: "500,000",
                period: "/bulan",
                description: "Pemeliharaan berkala untuk performa optimal",
                features: [
                  "Regular updates",
                  "Security monitoring",
                  "Backup management",
                  "Technical support"
                ]
              },
              {
                name: "Content Writing",
                price: "200,000",
                period: "/artikel",
                description: "Artikel berkualitas untuk website dan blog",
                features: [
                  "SEO optimized content",
                  "Original & engaging",
                  "Research mendalam",
                  "CTA optimization"
                ]
              }
            ].map((addon, index) => (
              <div key={index} className="card-gradient rounded-xl p-6 hover-lift">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{addon.name}</h3>
                <div className="mb-4">
                  <span className="text-2xl font-bold text-blue-600">Rp {addon.price}</span>
                  <span className="text-gray-500">{addon.period}</span>
                </div>
                <p className="text-gray-600 mb-4">{addon.description}</p>
                <ul className="space-y-2 mb-6">
                  {addon.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center text-sm text-gray-600">
                      <svg className="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>
                <Link
                  href="/kontak"
                  className="btn-secondary w-full text-center block"
                >
                  Tambahkan ke Paket
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="section-padding bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Pertanyaan Seputar Harga
            </h2>
          </div>

          <div className="space-y-6">
            {[
              {
                question: "Apakah ada biaya tersembunyi?",
                answer: "Tidak ada biaya tersembunyi. Semua biaya sudah transparan dan tertulis jelas di setiap paket. Hosting untuk tahun pertama sudah termasuk dalam harga."
              },
              {
                question: "Bagaimana sistem pembayaran?",
                answer: "Pembayaran dapat dilakukan dengan DP 50% di awal dan pelunasan saat website siap launch. Kami menerima transfer bank, e-wallet, dan payment gateway."
              },
              {
                question: "Berapa lama proses pengerjaan?",
                answer: "Paket Starter: 7-10 hari, Professional: 14-21 hari, Enterprise: 30-45 hari. Timeline dapat disesuaikan dengan kebutuhan dan tingkat kompleksitas."
              },
              {
                question: "Apakah ada garansi?",
                answer: "Ya, kami memberikan garansi kepuasan dan revisi hingga Anda puas. Juga termasuk garansi bug-fix selama periode support yang tertera di setiap paket."
              }
            ].map((faq, index) => (
              <div key={index} className="card-gradient rounded-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">{faq.question}</h3>
                <p className="text-gray-600">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Mulai Proyek Website Anda Hari Ini
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Konsultasi gratis untuk menentukan paket yang paling sesuai dengan kebutuhan bisnis Anda
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/kontak"
              className="bg-white text-blue-600 font-semibold py-3 px-8 rounded-lg hover:bg-gray-100 transition-all duration-300"
            >
              Konsultasi Gratis
            </Link>
            <Link
              href="/layanan"
              className="border-2 border-white text-white font-semibold py-3 px-8 rounded-lg hover:bg-white hover:text-blue-600 transition-all duration-300"
            >
              Lihat Detail Layanan
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}