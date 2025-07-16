'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function FAQPage() {
  const [openItem, setOpenItem] = useState<number | null>(null)

  const toggleItem = (index: number) => {
    setOpenItem(openItem === index ? null : index)
  }

  const faqCategories = [
    {
      title: "Umum",
      questions: [
        {
          question: "Apa itu WebJasa?",
          answer: "WebJasa adalah perusahaan jasa pembuatan website profesional yang membantu bisnis Indonesia memiliki presence digital yang kuat. Kami menyediakan layanan lengkap mulai dari design, development, hingga maintenance website."
        },
        {
          question: "Sudah berapa lama WebJasa beroperasi?",
          answer: "WebJasa telah beroperasi sejak 2019 dan telah menyelesaikan lebih dari 500+ proyek website untuk berbagai jenis bisnis, dari startup hingga enterprise."
        },
        {
          question: "Di mana lokasi kantor WebJasa?",
          answer: "Kantor kami berlokasi di Jakarta Selatan, namun kami melayani klien dari seluruh Indonesia bahkan luar negeri. Sebagian besar komunikasi dan koordinasi dilakukan secara online."
        }
      ]
    },
    {
      title: "Layanan & Harga",
      questions: [
        {
          question: "Apa saja layanan yang ditawarkan WebJasa?",
          answer: "Kami menyediakan berbagai layanan: Website Bisnis, E-Commerce, Landing Page, Website Portal, Maintenance, SEO Optimization, dan Custom Development sesuai kebutuhan spesifik Anda."
        },
        {
          question: "Berapa kisaran harga untuk membuat website?",
          answer: "Harga bervariasi tergantung kompleksitas. Paket Starter mulai Rp 1.5jt, Professional Rp 2.5jt, dan Enterprise Rp 4.5jt. Kami juga menyediakan paket custom sesuai budget dan requirement."
        },
        {
          question: "Apakah ada biaya tersembunyi?",
          answer: "Tidak ada biaya tersembunyi. Semua biaya dijelaskan secara transparan di awal. Hosting tahun pertama sudah termasuk dalam paket, begitu juga dengan maintenance sesuai periode yang tertera."
        },
        {
          question: "Bagaimana sistem pembayaran?",
          answer: "Pembayaran dapat dilakukan dengan DP 50% di awal proyek dan pelunasan saat website ready to launch. Kami menerima transfer bank, e-wallet, dan payment gateway lainnya."
        }
      ]
    },
    {
      title: "Proses & Timeline",
      questions: [
        {
          question: "Berapa lama waktu pengerjaan website?",
          answer: "Timeline bervariasi: Landing Page (7-10 hari), Website Bisnis (14-21 hari), E-Commerce (30-45 hari). Timeline dapat disesuaikan dengan kompleksitas dan prioritas klien."
        },
        {
          question: "Bagaimana proses pengerjaan website?",
          answer: "Proses kami meliputi: 1) Konsultasi & analisis kebutuhan, 2) Design mockup & approval, 3) Development & coding, 4) Testing & review, 5) Launch & handover, 6) Training & support."
        },
        {
          question: "Apakah bisa request revisi?",
          answer: "Ya, kami memberikan unlimited revisi hingga Anda puas dengan hasilnya. Revisi major design dilakukan di tahap mockup, sedangkan minor adjustments bisa dilakukan sampai akhir proyek."
        },
        {
          question: "Bagaimana jika proyek terlambat?",
          answer: "Kami berkomitmen pada timeline yang telah disepakati. Jika terjadi keterlambatan karena faktor internal, kami akan memberikan kompensasi berupa extended support atau benefit lainnya."
        }
      ]
    },
    {
      title: "Teknis",
      questions: [
        {
          question: "Platform apa yang digunakan untuk membuat website?",
          answer: "Kami menggunakan berbagai platform tergantung kebutuhan: React/Next.js untuk performa optimal, WordPress untuk content management, Laravel untuk sistem kompleks, atau custom development sesuai requirement."
        },
        {
          question: "Apakah website responsive di mobile?",
          answer: "Ya, semua website yang kami buat 100% responsive dan mobile-friendly. Kami menggunakan pendekatan mobile-first design untuk memastikan UX yang optimal di semua device."
        },
        {
          question: "Apakah SEO sudah termasuk?",
          answer: "Basic SEO sudah termasuk dalam semua paket, meliputi: meta tags, sitemap, page speed optimization, dan structure markup. Untuk advanced SEO, tersedia sebagai layanan tambahan."
        },
        {
          question: "Bagaimana dengan keamanan website?",
          answer: "Kami implementasikan security best practices: SSL certificate, secure coding, regular updates, firewall protection, dan backup otomatis. Untuk e-commerce, kami juga implement PCI compliance."
        }
      ]
    },
    {
      title: "After Sales & Support",
      questions: [
        {
          question: "Apakah ada garansi?",
          answer: "Ya, kami memberikan garansi bug-fix dan technical support sesuai periode yang tertera di setiap paket. Juga ada garansi kepuasan - jika tidak sesuai ekspektasi, akan ada refund policy."
        },
        {
          question: "Bagaimana dengan maintenance website?",
          answer: "Basic maintenance sudah termasuk dalam periode support. Untuk long-term maintenance, tersedia paket bulanan mulai Rp 500rb yang meliputi: updates, backup, security monitoring, dan technical support."
        },
        {
          question: "Apakah saya mendapat source code?",
          answer: "Ya, setelah pembayaran lunas, Anda akan mendapat semua source code, database, dan asset website. Kami juga menyediakan dokumentasi untuk memudahkan future development."
        },
        {
          question: "Bagaimana jika website bermasalah?",
          answer: "Tim support kami siap membantu 24/7 untuk klien yang dalam masa maintenance. Untuk emergency issue, kami berkomitmen response time maksimal 2 jam dan resolution dalam 24 jam."
        }
      ]
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Frequently Asked Questions
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Temukan jawaban untuk pertanyaan yang sering ditanyakan tentang layanan, 
            proses, dan kebijakan WebJasa. Masih ada pertanyaan? Hubungi kami langsung.
          </p>
        </div>
      </section>

      {/* FAQ Content */}
      <section className="section-padding">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {faqCategories.map((category, categoryIndex) => (
            <div key={categoryIndex} className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 pb-3 border-b border-gray-200">
                {category.title}
              </h2>
              
              <div className="space-y-4">
                {category.questions.map((faq, faqIndex) => {
                  const itemIndex = categoryIndex * 100 + faqIndex
                  const isOpen = openItem === itemIndex
                  
                  return (
                    <div key={faqIndex} className="card-gradient rounded-lg">
                      <button
                        onClick={() => toggleItem(itemIndex)}
                        className="w-full text-left p-6 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-lg"
                      >
                        <div className="flex items-center justify-between">
                          <h3 className="text-lg font-semibold text-gray-900 pr-4">
                            {faq.question}
                          </h3>
                          <svg
                            className={`w-6 h-6 text-blue-600 transform transition-transform duration-200 ${
                              isOpen ? 'rotate-180' : ''
                            }`}
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                          </svg>
                        </div>
                      </button>
                      
                      {isOpen && (
                        <div className="px-6 pb-6">
                          <div className="pt-4 border-t border-gray-200">
                            <p className="text-gray-600 leading-relaxed">
                              {faq.answer}
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Contact Section */}
      <section className="section-padding bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            Masih Ada Pertanyaan?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Tim kami siap membantu menjawab pertanyaan spesifik tentang proyek Anda. 
            Jangan ragu untuk menghubungi kami untuk konsultasi gratis.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <a
              href="https://wa.me/6281234567890"
              target="_blank"
              rel="noopener noreferrer"
              className="card-gradient rounded-xl p-6 hover-lift text-center"
            >
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">WhatsApp</h3>
              <p className="text-gray-600 text-sm">Chat langsung untuk pertanyaan cepat</p>
            </a>

            <a
              href="mailto:info@webjasa.com"
              className="card-gradient rounded-xl p-6 hover-lift text-center"
            >
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Email</h3>
              <p className="text-gray-600 text-sm">Kirim pertanyaan detail via email</p>
            </a>

            <Link
              href="/kontak"
              className="card-gradient rounded-xl p-6 hover-lift text-center"
            >
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Konsultasi</h3>
              <p className="text-gray-600 text-sm">Form konsultasi lengkap</p>
            </Link>
          </div>

          <div className="text-center">
            <Link
              href="/kontak"
              className="btn-primary inline-block"
            >
              Konsultasi Gratis Sekarang
            </Link>
          </div>
        </div>
      </section>

      {/* Quick Tips */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Tips Sebelum Memulai Proyek
            </h2>
            <p className="text-gray-600">
              Persiapan yang baik akan membuat proyek website Anda berjalan lebih lancar
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: "Tentukan Tujuan Website",
                description: "Definisikan dengan jelas tujuan website: branding, lead generation, penjualan online, atau informasi.",
                icon: "🎯"
              },
              {
                title: "Siapkan Konten",
                description: "Kumpulkan teks, gambar, logo, dan materi lain yang akan ditampilkan di website.",
                icon: "📝"
              },
              {
                title: "Riset Kompetitor",
                description: "Pelajari website kompetitor untuk inspirasi fitur dan design yang ingin Anda implementasikan.",
                icon: "🔍"
              },
              {
                title: "Tentukan Budget",
                description: "Sesuaikan pilihan paket dan fitur dengan budget yang tersedia untuk hasil optimal.",
                icon: "💰"
              },
              {
                title: "Pikirkan Jangka Panjang",
                description: "Pertimbangkan kebutuhan future development, maintenance, dan skalabilitas website.",
                icon: "📈"
              },
              {
                title: "Komunikasi Aktif",
                description: "Berikan feedback yang clear dan tepat waktu untuk mempercepat proses development.",
                icon: "💬"
              }
            ].map((tip, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl mb-4">{tip.icon}</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">{tip.title}</h3>
                <p className="text-gray-600 text-sm">{tip.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}