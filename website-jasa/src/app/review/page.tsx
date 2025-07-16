import Link from 'next/link'

export default function ReviewPage() {
  const stats = [
    { label: "Total Klien", value: "500+", icon: "👥" },
    { label: "Rating Rata-rata", value: "4.9/5", icon: "⭐" },
    { label: "Proyek Selesai", value: "98%", icon: "✅" },
    { label: "Klien Repeat Order", value: "85%", icon: "🔄" }
  ]

  const testimonials = [
    {
      id: 1,
      name: "Budi Santoso",
      company: "PT. Maju Jaya Abadi",
      position: "CEO",
      rating: 5,
      avatar: "👨‍💼",
      text: "WebJasa benar-benar mengubah bisnis kami! Website yang mereka buat tidak hanya cantik, tapi juga functional dan SEO-friendly. Traffic website naik 300% dalam 3 bulan pertama. Tim nya sangat profesional dan responsif. Highly recommended!",
      project: "Website Company Profile",
      industry: "Manufacturing"
    },
    {
      id: 2,
      name: "Sari Indah Permata",
      company: "Toko Sari Fashion",
      position: "Owner",
      rating: 5,
      avatar: "👩‍💼",
      text: "Toko online yang dibuat WebJasa sangat user-friendly dan modern. Penjualan online kami meningkat drastis 200% setelah website launching. Fitur inventory management sangat membantu operasional harian. Great job!",
      project: "E-Commerce Website",
      industry: "Fashion Retail"
    },
    {
      id: 3,
      name: "Ahmad Rahman",
      company: "Digital Marketing Agency",
      position: "Founder",
      rating: 5,
      avatar: "👨‍💻",
      text: "Sebagai agency, kami sangat picky soal kualitas website. WebJasa berhasil exceed expectations kami. Loading speed super fast, design modern, dan technically sound. Klien kami juga sangat puas dengan hasilnya.",
      project: "Agency Portfolio Website",
      industry: "Digital Marketing"
    },
    {
      id: 4,
      name: "Dr. Fitri Amelia",
      company: "Klinik Sehat Bersama",
      position: "Direktur",
      rating: 5,
      avatar: "👩‍⚕️",
      text: "Website klinik kami sekarang terlihat sangat profesional dan trustworthy. Fitur booking appointment online sangat membantu pasien dan staff. WebJasa juga memberikan training yang comprehensive untuk tim kami.",
      project: "Medical Website with Booking System",
      industry: "Healthcare"
    },
    {
      id: 5,
      name: "Rendra Wijaya",
      company: "PT. Solusi Teknologi",
      position: "CTO",
      rating: 5,
      avatar: "👨‍🔬",
      text: "Kami membutuhkan website dengan integrasi API yang kompleks. WebJasa berhasil deliver dengan sempurna. Technical expertise mereka sangat impressive, dan project management nya juga top notch. Pasti akan collaboration lagi.",
      project: "Enterprise Web Application",
      industry: "Technology"
    },
    {
      id: 6,
      name: "Lina Kusuma",
      company: "Bimbel Cerdas",
      position: "Principal",
      rating: 5,
      avatar: "👩‍🏫",
      text: "Website pembelajaran online yang dibuat WebJasa sangat memudahkan siswa dan guru. Fitur video streaming, quiz online, dan progress tracking bekerja dengan sempurna. Student engagement meningkat significantly!",
      project: "Educational Platform",
      industry: "Education"
    }
  ]

  const caseStudies = [
    {
      title: "E-Commerce Fashion: Peningkatan Conversion Rate 300%",
      client: "Toko Sari Fashion",
      challenge: "Website lama sulit digunakan dan conversion rate rendah",
      solution: "Redesign UX/UI, optimasi checkout process, implementasi recommendation engine",
      results: [
        "Conversion rate naik 300%",
        "Average order value naik 150%",
        "Loading time turun 60%",
        "Mobile traffic naik 250%"
      ],
      duration: "6 minggu",
      technology: "Next.js, Stripe, MongoDB"
    },
    {
      title: "Corporate Website: Lead Generation Meningkat 400%",
      client: "PT. Maju Jaya Abadi",
      challenge: "Website tidak generate leads dan ranking SEO rendah",
      solution: "SEO optimization, landing page optimization, lead magnet implementation",
      results: [
        "Lead generation naik 400%",
        "Organic traffic naik 500%",
        "Ranking Google page 1 untuk 15 keywords",
        "Bounce rate turun 45%"
      ],
      duration: "4 minggu",
      technology: "WordPress, Yoast SEO, Google Analytics"
    },
    {
      title: "Healthcare Platform: Efisiensi Operasional 250%",
      client: "Klinik Sehat Bersama",
      challenge: "Sistem booking manual dan administrasi tidak efisien",
      solution: "Online booking system, patient management system, telemedicine integration",
      results: [
        "Efisiensi operasional naik 250%",
        "Patient satisfaction score 95%",
        "Administrative cost turun 40%",
        "Online bookings 80% dari total"
      ],
      duration: "8 minggu",
      technology: "Laravel, MySQL, Payment Gateway"
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Review & Testimoni Klien
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Kepuasan klien adalah prioritas utama kami. Simak pengalaman dan hasil 
            yang telah dicapai oleh klien-klien yang telah mempercayakan proyeknya kepada WebJasa.
          </p>
        </div>
      </section>

      {/* Stats Section */}
      <section className="section-padding bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl mb-3">{stat.icon}</div>
                <div className="text-3xl font-bold text-blue-600 mb-2">{stat.value}</div>
                <p className="text-gray-600">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Grid */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Apa Kata Klien Kami
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Pengalaman nyata dari klien yang telah merasakan dampak positif 
              website berkualitas untuk bisnis mereka
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {testimonials.map((testimonial) => (
              <div key={testimonial.id} className="card-gradient rounded-xl p-6 hover-lift">
                {/* Rating */}
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <svg key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>

                {/* Testimonial Text */}
                <p className="text-gray-600 mb-6 italic leading-relaxed">
                  "{testimonial.text}"
                </p>

                {/* Project Info */}
                <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm text-blue-700">
                    <strong>Proyek:</strong> {testimonial.project}
                  </p>
                  <p className="text-sm text-blue-700">
                    <strong>Industri:</strong> {testimonial.industry}
                  </p>
                </div>

                {/* Client Info */}
                <div className="flex items-center">
                  <div className="text-3xl mr-4">{testimonial.avatar}</div>
                  <div>
                    <div className="font-semibold text-gray-900">{testimonial.name}</div>
                    <div className="text-sm text-gray-600">{testimonial.position}</div>
                    <div className="text-sm text-gray-500">{testimonial.company}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Case Studies */}
      <section className="section-padding bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Case Studies
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Studi kasus mendalam tentang bagaimana kami membantu klien 
              mencapai goals bisnis mereka melalui solusi website yang tepat
            </p>
          </div>

          <div className="space-y-12">
            {caseStudies.map((study, index) => (
              <div key={index} className="card-gradient rounded-xl overflow-hidden">
                <div className="p-8">
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div>
                      <h3 className="text-2xl font-bold text-gray-900 mb-4">
                        {study.title}
                      </h3>
                      <div className="space-y-4">
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">Challenge:</h4>
                          <p className="text-gray-600">{study.challenge}</p>
                        </div>
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">Solution:</h4>
                          <p className="text-gray-600">{study.solution}</p>
                        </div>
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-4">Results Achieved:</h4>
                      <ul className="space-y-2 mb-6">
                        {study.results.map((result, idx) => (
                          <li key={idx} className="flex items-center text-gray-600">
                            <svg className="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                            {result}
                          </li>
                        ))}
                      </ul>
                      
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="font-semibold text-gray-700">Duration:</span>
                          <p className="text-gray-600">{study.duration}</p>
                        </div>
                        <div>
                          <span className="font-semibold text-gray-700">Technology:</span>
                          <p className="text-gray-600">{study.technology}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Video Testimonials */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Video Testimonials
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Dengar langsung pengalaman klien kami dalam video testimonial
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                name: "Budi Santoso - PT. Maju Jaya",
                thumbnail: "🎥",
                duration: "2:30",
                description: "Cerita bagaimana website baru meningkatkan brand awareness"
              },
              {
                name: "Sari Indah - Toko Fashion",
                thumbnail: "🎬",
                duration: "1:45",
                description: "Dampak e-commerce terhadap penjualan offline dan online"
              },
              {
                name: "Dr. Fitri - Klinik Sehat",
                thumbnail: "📹",
                duration: "3:15",
                description: "Transformasi digital di industri healthcare"
              }
            ].map((video, index) => (
              <div key={index} className="card-gradient rounded-xl overflow-hidden hover-lift">
                <div className="aspect-video bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-6xl mb-4">{video.thumbnail}</div>
                    <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                      Play Video
                    </button>
                  </div>
                </div>
                <div className="p-6">
                  <h3 className="font-semibold text-gray-900 mb-2">{video.name}</h3>
                  <p className="text-gray-600 text-sm mb-2">{video.description}</p>
                  <span className="text-blue-600 text-sm">{video.duration}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Trust Signals */}
      <section className="section-padding bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Dipercaya oleh Berbagai Industri
            </h2>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
            {[
              { industry: "E-Commerce", icon: "🛒", count: "150+" },
              { industry: "Healthcare", icon: "🏥", count: "75+" },
              { industry: "Education", icon: "🎓", count: "100+" },
              { industry: "Manufacturing", icon: "🏭", count: "80+" },
              { industry: "Restaurant", icon: "🍽️", count: "60+" },
              { industry: "Technology", icon: "💻", count: "90+" }
            ].map((item, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl mb-3">{item.icon}</div>
                <div className="text-2xl font-bold text-blue-600 mb-1">{item.count}</div>
                <p className="text-gray-600 text-sm">{item.industry}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Siap Menjadi Klien Puas Berikutnya?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Bergabunglah dengan 500+ klien yang telah merasakan dampak positif 
            website berkualitas untuk pertumbuhan bisnis mereka.
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