import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-6">
                Wujudkan Website 
                <span className="block text-blue-200">Impian Bisnis Anda</span>
              </h1>
              <p className="text-xl text-blue-100 mb-8 leading-relaxed">
                Solusi terpercaya untuk kebutuhan website profesional. Kami menghadirkan website modern, 
                responsif, dan berkualitas tinggi yang akan mengembangkan bisnis Anda ke level berikutnya.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  href="/kontak"
                  className="bg-white text-blue-600 font-semibold py-3 px-8 rounded-lg hover:bg-gray-100 transition-all duration-300 text-center"
                >
                  Mulai Konsultasi Gratis
                </Link>
                <Link
                  href="/layanan"
                  className="border-2 border-white text-white font-semibold py-3 px-8 rounded-lg hover:bg-white hover:text-blue-600 transition-all duration-300 text-center"
                >
                  Lihat Layanan Kami
                </Link>
              </div>
            </div>
            <div className="relative">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                    <span className="text-blue-100">Website Responsif</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                    <span className="text-blue-100">SEO Optimized</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                    <span className="text-blue-100">Loading Cepat</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                    <span className="text-blue-100">Maintenance 24/7</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">500+</div>
              <p className="text-gray-600">Website Selesai</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">98%</div>
              <p className="text-gray-600">Kepuasan Klien</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">5</div>
              <p className="text-gray-600">Tahun Pengalaman</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">24/7</div>
              <p className="text-gray-600">Support</p>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Layanan Kami
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Kami menyediakan berbagai solusi website yang disesuaikan dengan kebutuhan bisnis Anda
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: "Website Bisnis",
                description: "Website profesional untuk meningkatkan kredibilitas dan jangkauan bisnis Anda",
                icon: "🏢",
                features: ["Design Modern", "Mobile Responsive", "SEO Ready"]
              },
              {
                title: "E-Commerce",
                description: "Toko online lengkap dengan sistem pembayaran dan manajemen produk",
                icon: "🛒",
                features: ["Payment Gateway", "Inventory Management", "Analytics"]
              },
              {
                title: "Landing Page",
                description: "Halaman landing yang converting untuk campaign marketing Anda",
                icon: "🎯",
                features: ["High Converting", "A/B Testing", "Analytics"]
              },
              {
                title: "Website Portal",
                description: "Portal informasi dan layanan untuk organisasi atau komunitas",
                icon: "🌐",
                features: ["User Management", "Content Management", "Multi-language"]
              },
              {
                title: "Maintenance",
                description: "Pemeliharaan dan update berkala untuk menjaga performa website",
                icon: "🔧",
                features: ["Regular Updates", "Security Monitoring", "Backup"]
              },
              {
                title: "SEO Optimization",
                description: "Optimasi website untuk meningkatkan ranking di mesin pencari",
                icon: "📈",
                features: ["Keyword Research", "On-page SEO", "Performance Optimization"]
              }
            ].map((service, index) => (
              <div key={index} className="card-gradient rounded-xl p-6 hover-lift">
                <div className="text-4xl mb-4">{service.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{service.title}</h3>
                <p className="text-gray-600 mb-4">{service.description}</p>
                <ul className="space-y-2">
                  {service.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center text-sm text-gray-500">
                      <svg className="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link
              href="/layanan"
              className="btn-primary inline-block"
            >
              Lihat Semua Layanan
            </Link>
          </div>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="section-padding bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Mengapa Memilih WebJasa?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Kami berkomitmen memberikan layanan terbaik dengan standar kualitas internasional
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: "Tim Profesional",
                description: "Developer berpengalaman dengan keahlian teknologi terkini",
                icon: "👥"
              },
              {
                title: "Harga Kompetitif",
                description: "Paket harga yang terjangkau tanpa mengurangi kualitas",
                icon: "💰"
              },
              {
                title: "Support 24/7",
                description: "Tim support yang siap membantu kapan saja dibutuhkan",
                icon: "🚀"
              },
              {
                title: "Garansi Kualitas",
                description: "Garansi kepuasan dan revisi hingga Anda puas",
                icon: "✅"
              },
              {
                title: "Delivery Tepat Waktu",
                description: "Komitmen menyelesaikan proyek sesuai timeline yang disepakati",
                icon: "⏰"
              },
              {
                title: "After Sales Service",
                description: "Layanan maintenance dan support berkelanjutan",
                icon: "🛠️"
              }
            ].map((reason, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">{reason.icon}</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{reason.title}</h3>
                <p className="text-gray-600">{reason.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Apa Kata Klien Kami
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Kepuasan klien adalah prioritas utama kami
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                name: "Budi Santoso",
                company: "PT. Maju Jaya",
                rating: 5,
                text: "Website yang dibuat WebJasa sangat profesional dan sesuai dengan kebutuhan bisnis kami. Tim nya sangat responsif dan hasil akhirnya melampaui ekspektasi."
              },
              {
                name: "Sari Indah",
                company: "Toko Sari Fashion",
                rating: 5,
                text: "Toko online kami jadi lebih modern dan penjualan meningkat 200% setelah menggunakan jasa WebJasa. Highly recommended!"
              },
              {
                name: "Ahmad Rahman", 
                company: "Digital Marketing Agency",
                rating: 5,
                text: "Pelayanan yang sangat baik, komunikasi lancar, dan website selesai tepat waktu. Tim WebJasa memang profesional!"
              }
            ].map((testimonial, index) => (
              <div key={index} className="card-gradient rounded-xl p-6">
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <svg key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>
                <p className="text-gray-600 mb-6 italic">"{testimonial.text}"</p>
                <div>
                  <div className="font-semibold text-gray-900">{testimonial.name}</div>
                  <div className="text-sm text-gray-500">{testimonial.company}</div>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link
              href="/review"
              className="btn-secondary inline-block"
            >
              Lihat Semua Review
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Siap Memulai Proyek Website Anda?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Konsultasikan kebutuhan website bisnis Anda dengan tim ahli kami secara gratis
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/kontak"
              className="bg-white text-blue-600 font-semibold py-3 px-8 rounded-lg hover:bg-gray-100 transition-all duration-300"
            >
              Konsultasi Gratis Sekarang
            </Link>
            <Link
              href="/harga"
              className="border-2 border-white text-white font-semibold py-3 px-8 rounded-lg hover:bg-white hover:text-blue-600 transition-all duration-300"
            >
              Lihat Paket Harga
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
