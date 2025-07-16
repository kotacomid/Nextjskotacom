import Link from 'next/link'

export default function TentangPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Tentang WebJasa
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Dengan passion untuk teknologi dan dedikasi terhadap kepuasan klien, 
            kami berkomitmen menjadi partner terpercaya dalam transformasi digital bisnis Anda.
          </p>
        </div>
      </section>

      {/* Company Story */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                Perjalanan Kami
              </h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  WebJasa didirikan pada tahun 2019 dengan misi sederhana namun mulia: 
                  membantu bisnis Indonesia berkembang melalui teknologi website yang tepat guna. 
                  Bermula dari tim kecil yang terdiri dari 3 developer passionate, 
                  kini kami telah berkembang menjadi tim solid dengan lebih dari 15 profesional.
                </p>
                <p>
                  Selama perjalanan ini, kami telah dipercaya oleh lebih dari 500+ klien dari 
                  berbagai industri - mulai dari startup rintisan hingga perusahaan besar. 
                  Setiap proyek adalah kesempatan bagi kami untuk belajar, berinovasi, 
                  dan memberikan solusi terbaik.
                </p>
                <p>
                  Filosofi kami sederhana: "Your Success is Our Success". Kami tidak hanya 
                  membuat website, tetapi membangun partnership jangka panjang dengan klien 
                  untuk mencapai goals bisnis mereka.
                </p>
              </div>
            </div>
            <div className="card-gradient rounded-xl p-8">
              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">500+</div>
                  <p className="text-gray-600">Proyek Selesai</p>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">5+</div>
                  <p className="text-gray-600">Tahun Pengalaman</p>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">15+</div>
                  <p className="text-gray-600">Tim Profesional</p>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">98%</div>
                  <p className="text-gray-600">Kepuasan Klien</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Vision & Mission */}
      <section className="section-padding bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Visi & Misi Kami
            </h2>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="card-gradient rounded-xl p-8 text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Visi</h3>
              <p className="text-gray-600">
                Menjadi perusahaan pengembangan website terdepan di Indonesia yang 
                membantu transformasi digital bisnis menuju era modern dan kompetitif.
              </p>
            </div>

            <div className="card-gradient rounded-xl p-8 text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Misi</h3>
              <p className="text-gray-600">
                Menyediakan solusi website berkualitas tinggi dengan teknologi terkini, 
                service excellent, dan harga yang kompetitif untuk memberdayakan 
                bisnis Indonesia di era digital.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Nilai-Nilai Kami
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Prinsip-prinsip fundamental yang menjadi landasan dalam setiap pekerjaan kami
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: "Kualitas Terbaik",
                description: "Kami berkomitmen memberikan hasil kerja dengan standar kualitas internasional dan detail yang sempurna.",
                icon: "⭐",
                color: "bg-yellow-100 text-yellow-600"
              },
              {
                title: "Integritas",
                description: "Transparansi, kejujuran, dan konsistensi dalam setiap komunikasi dan pekerjaan dengan klien.",
                icon: "🤝",
                color: "bg-green-100 text-green-600"
              },
              {
                title: "Inovasi",
                description: "Selalu mengikuti perkembangan teknologi terkini dan mengimplementasikan solusi inovatif.",
                icon: "💡",
                color: "bg-blue-100 text-blue-600"
              },
              {
                title: "Customer First",
                description: "Kepuasan dan kesuksesan klien adalah prioritas utama dalam setiap keputusan bisnis kami.",
                icon: "❤️",
                color: "bg-red-100 text-red-600"
              },
              {
                title: "Teamwork",
                description: "Kekuatan tim yang solid dan kolaborasi yang efektif untuk mencapai hasil terbaik.",
                icon: "👥",
                color: "bg-purple-100 text-purple-600"
              },
              {
                title: "Continuous Learning",
                description: "Komitmen untuk terus belajar dan mengembangkan skill untuk memberikan service terbaik.",
                icon: "📚",
                color: "bg-indigo-100 text-indigo-600"
              }
            ].map((value, index) => (
              <div key={index} className="text-center">
                <div className={`w-16 h-16 ${value.color} rounded-full flex items-center justify-center mx-auto mb-4`}>
                  <span className="text-2xl">{value.icon}</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{value.title}</h3>
                <p className="text-gray-600">{value.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="section-padding bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Tim Profesional Kami
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Dibalik setiap website berkualitas, ada tim passionate yang berdedikasi tinggi
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                name: "Ahmad Rizki",
                position: "Founder & CEO",
                bio: "10+ tahun pengalaman di industri teknologi. Visioner yang memimpin tim dengan passion untuk inovasi.",
                avatar: "👨‍💼"
              },
              {
                name: "Sarah Putri",
                position: "Lead Designer",
                bio: "Expert UI/UX dengan eye for detail. Mengubah ide menjadi design yang beautiful dan user-friendly.",
                avatar: "👩‍🎨"
              },
              {
                name: "Budi Santoso",
                position: "Senior Developer",
                bio: "Full-stack developer dengan keahlian multiple framework. Perfectionist dalam coding dan problem solving.",
                avatar: "👨‍💻"
              },
              {
                name: "Dewi Lestari",
                position: "Project Manager",
                bio: "Mengkoordinasi proyek dengan timeline yang ketat. Memastikan setiap deliverable sesuai ekspektasi klien.",
                avatar: "👩‍💼"
              },
              {
                name: "Randi Permana",
                position: "Digital Marketing",
                bio: "SEO expert yang membantu website klien ranking di Google. Data-driven dan result-oriented.",
                avatar: "👨‍📊"
              },
              {
                name: "Indira Sari",
                position: "Customer Success",
                bio: "Always ready to help! Memastikan customer journey yang smooth dari awal hingga after-sales.",
                avatar: "👩‍💬"
              }
            ].map((member, index) => (
              <div key={index} className="card-gradient rounded-xl p-6 text-center hover-lift">
                <div className="text-6xl mb-4">{member.avatar}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{member.name}</h3>
                <p className="text-blue-600 font-medium mb-3">{member.position}</p>
                <p className="text-gray-600 text-sm">{member.bio}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Awards & Recognition */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Pencapaian & Pengakuan
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Prestasi yang kami raih berkat kepercayaan dan dukungan klien-klien kami
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: "Best Web Agency 2023",
                description: "Penghargaan dari Indonesia Web Developer Association",
                icon: "🏆"
              },
              {
                title: "Top Rated Service",
                description: "Rating 4.9/5 di platform freelance marketplace",
                icon: "⭐"
              },
              {
                title: "Client Choice Award",
                description: "Dipilih sebagai vendor terpercaya oleh 95% klien",
                icon: "🎖️"
              },
              {
                title: "Innovation Excellence",
                description: "Pengakuan atas implementasi teknologi terdepan",
                icon: "💎"
              }
            ].map((award, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl mb-4">{award.icon}</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{award.title}</h3>
                <p className="text-gray-600 text-sm">{award.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Mari Berkolaborasi dengan Kami
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Bergabunglah dengan 500+ klien yang telah mempercayakan proyeknya kepada kami. 
            Mari wujudkan visi digital bisnis Anda bersama tim profesional WebJasa.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/kontak"
              className="bg-white text-blue-600 font-semibold py-3 px-8 rounded-lg hover:bg-gray-100 transition-all duration-300"
            >
              Mulai Konsultasi
            </Link>
            <Link
              href="/layanan"
              className="border-2 border-white text-white font-semibold py-3 px-8 rounded-lg hover:bg-white hover:text-blue-600 transition-all duration-300"
            >
              Lihat Portfolio
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}