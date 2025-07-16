import Link from 'next/link'

export default function LayananPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Layanan Pembuatan Website
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Solusi lengkap untuk semua kebutuhan website bisnis Anda. Dari konsep hingga maintenance, 
            kami siap membantu mewujudkan website impian Anda.
          </p>
        </div>
      </section>

      {/* Services Grid */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {[
              {
                title: "Website Bisnis",
                description: "Website profesional yang meningkatkan kredibilitas dan memperluas jangkauan bisnis Anda",
                icon: "🏢",
                price: "Mulai dari Rp 2,500,000",
                features: [
                  "Design modern dan professional",
                  "Responsive di semua device",
                  "SEO optimization",
                  "Contact form integration",
                  "Google Analytics setup",
                  "SSL Certificate",
                  "Basic hosting 1 tahun",
                  "Free maintenance 3 bulan"
                ],
                includes: [
                  "Homepage + 4-6 halaman",
                  "Company profile section",
                  "Product/service showcase",
                  "Contact information",
                  "About us page"
                ]
              },
              {
                title: "E-Commerce",
                description: "Toko online lengkap dengan sistem pembayaran dan manajemen produk yang mudah digunakan",
                icon: "🛒",
                price: "Mulai dari Rp 4,500,000",
                features: [
                  "Shopping cart functionality",
                  "Payment gateway integration",
                  "Product management system",
                  "Order tracking",
                  "Inventory management",
                  "Customer account system",
                  "Mobile responsive design",
                  "Admin dashboard"
                ],
                includes: [
                  "Product catalog",
                  "Shopping cart",
                  "Payment processing",
                  "Order management",
                  "Customer reviews"
                ]
              },
              {
                title: "Landing Page",
                description: "Halaman landing yang converting tinggi untuk campaign marketing dan lead generation",
                icon: "🎯",
                price: "Mulai dari Rp 1,500,000",
                features: [
                  "High converting design",
                  "A/B testing ready",
                  "Lead capture forms",
                  "Analytics integration",
                  "Fast loading speed",
                  "Mobile optimized",
                  "Call-to-action optimization",
                  "Social media integration"
                ],
                includes: [
                  "Single page design",
                  "Lead generation forms",
                  "Analytics setup",
                  "Performance optimization",
                  "Conversion tracking"
                ]
              },
              {
                title: "Website Portal",
                description: "Portal informasi dan layanan untuk organisasi, komunitas, atau instansi",
                icon: "🌐",
                price: "Mulai dari Rp 3,500,000",
                features: [
                  "User management system",
                  "Content management",
                  "Multi-language support",
                  "User registration/login",
                  "Document management",
                  "Search functionality",
                  "News/article system",
                  "User roles & permissions"
                ],
                includes: [
                  "User authentication",
                  "Content management",
                  "Document library",
                  "News system",
                  "Search function"
                ]
              },
              {
                title: "Website Maintenance",
                description: "Pemeliharaan berkala untuk menjaga performa, keamanan, dan update website Anda",
                icon: "🔧",
                price: "Mulai dari Rp 500,000/bulan",
                features: [
                  "Regular updates",
                  "Security monitoring",
                  "Performance optimization",
                  "Backup management",
                  "Content updates",
                  "Bug fixes",
                  "Technical support",
                  "Monthly reports"
                ],
                includes: [
                  "Weekly backups",
                  "Security scans",
                  "Performance monitoring",
                  "Content updates",
                  "Technical support"
                ]
              },
              {
                title: "SEO Optimization",
                description: "Optimasi website untuk meningkatkan ranking di mesin pencari dan traffic organik",
                icon: "📈",
                price: "Mulai dari Rp 1,000,000/bulan",
                features: [
                  "Keyword research",
                  "On-page SEO",
                  "Technical SEO",
                  "Content optimization",
                  "Link building",
                  "Performance tracking",
                  "Competitor analysis",
                  "Monthly SEO reports"
                ],
                includes: [
                  "SEO audit",
                  "Keyword strategy",
                  "Content optimization",
                  "Performance tracking",
                  "Monthly reports"
                ]
              }
            ].map((service, index) => (
              <div key={index} className="card-gradient rounded-xl p-8 hover-lift">
                <div className="flex items-center mb-6">
                  <div className="text-4xl mr-4">{service.icon}</div>
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">{service.title}</h3>
                    <p className="text-blue-600 font-semibold">{service.price}</p>
                  </div>
                </div>
                
                <p className="text-gray-600 mb-6">{service.description}</p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Fitur Utama:</h4>
                    <ul className="space-y-2">
                      {service.features.slice(0, 4).map((feature, idx) => (
                        <li key={idx} className="flex items-center text-sm text-gray-600">
                          <svg className="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Yang Termasuk:</h4>
                    <ul className="space-y-2">
                      {service.includes.map((include, idx) => (
                        <li key={idx} className="flex items-center text-sm text-gray-600">
                          <svg className="w-4 h-4 text-blue-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                          {include}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
                
                <Link
                  href="/kontak"
                  className="btn-primary w-full text-center block"
                >
                  Konsultasi Gratis
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section className="section-padding bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Proses Pengerjaan
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Metodologi yang terstruktur untuk memastikan hasil yang optimal dan tepat waktu
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                step: "01",
                title: "Konsultasi",
                description: "Diskusi kebutuhan dan goals website Anda"
              },
              {
                step: "02", 
                title: "Perencanaan",
                description: "Pembuatan wireframe dan sitemap"
              },
              {
                step: "03",
                title: "Development",
                description: "Coding dan implementasi fitur"
              },
              {
                step: "04",
                title: "Testing & Launch",
                description: "Quality assurance dan go-live"
              }
            ].map((process, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                  {process.step}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{process.title}</h3>
                <p className="text-gray-600">{process.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technologies Section */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Teknologi yang Kami Gunakan
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Teknologi modern dan terpercaya untuk performa website yang optimal
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
            {[
              { name: "React", icon: "⚛️" },
              { name: "Next.js", icon: "🚀" },
              { name: "WordPress", icon: "📝" },
              { name: "Laravel", icon: "🔧" },
              { name: "Node.js", icon: "💚" },
              { name: "Python", icon: "🐍" }
            ].map((tech, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl mb-3">{tech.icon}</div>
                <h3 className="font-semibold text-gray-900">{tech.name}</h3>
              </div>
            ))}
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
            Konsultasikan kebutuhan website Anda dengan tim ahli kami secara gratis
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/kontak"
              className="bg-white text-blue-600 font-semibold py-3 px-8 rounded-lg hover:bg-gray-100 transition-all duration-300"
            >
              Konsultasi Gratis
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