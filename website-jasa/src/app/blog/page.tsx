import Link from 'next/link'

export default function BlogPage() {
  const featuredPosts = [
    {
      id: 1,
      title: "10 Trend Desain Website 2024 yang Wajib Anda Ketahui",
      excerpt: "Pelajari tren desain website terbaru yang akan mendominasi tahun 2024, dari minimalism hingga dark mode dan micro-interactions.",
      category: "Design",
      date: "15 Januari 2024",
      readTime: "5 min read",
      image: "🎨",
      featured: true
    },
    {
      id: 2,
      title: "Panduan Lengkap SEO untuk Website Bisnis Lokal",
      excerpt: "Strategi SEO khusus untuk bisnis lokal agar website Anda mudah ditemukan customer di area sekitar.",
      category: "SEO",
      date: "12 Januari 2024", 
      readTime: "8 min read",
      image: "🔍",
      featured: true
    }
  ]

  const blogPosts = [
    {
      id: 3,
      title: "Mengapa Website Loading Speed Sangat Penting untuk Bisnis",
      excerpt: "Dampak loading speed terhadap user experience, SEO ranking, dan conversion rate. Plus tips optimasi performa website.",
      category: "Performance",
      date: "10 Januari 2024",
      readTime: "6 min read",
      image: "⚡"
    },
    {
      id: 4,
      title: "E-Commerce vs Marketplace: Mana yang Lebih Baik untuk Bisnis Anda?",
      excerpt: "Perbandingan lengkap antara membangun toko online sendiri vs berjualan di marketplace. Analisis keuntungan dan kekurangan.",
      category: "E-Commerce",
      date: "8 Januari 2024",
      readTime: "7 min read",
      image: "🛒"
    },
    {
      id: 5,
      title: "Cara Memilih Domain dan Hosting yang Tepat untuk Website",
      excerpt: "Tips memilih nama domain yang baik untuk SEO dan brand, plus panduan memilih hosting yang reliable dan fast.",
      category: "Technical",
      date: "5 Januari 2024",
      readTime: "4 min read",
      image: "🌐"
    },
    {
      id: 6,
      title: "Social Media Integration: Menghubungkan Website dengan Media Sosial",
      excerpt: "Strategi integrasi media sosial yang efektif untuk meningkatkan engagement dan traffic website bisnis Anda.",
      category: "Marketing",
      date: "3 Januari 2024",
      readTime: "5 min read",
      image: "📱"
    },
    {
      id: 7,
      title: "Website Security: Melindungi Bisnis Online dari Cyber Attack",
      excerpt: "Langkah-langkah penting untuk mengamankan website dari malware, hacking, dan ancaman keamanan cyber lainnya.",
      category: "Security",
      date: "1 Januari 2024",
      readTime: "6 min read", 
      image: "🔒"
    },
    {
      id: 8,
      title: "Content Management System (CMS): WordPress vs Custom Development",
      excerpt: "Perbandingan antara menggunakan CMS siap pakai seperti WordPress dengan custom development untuk website bisnis.",
      category: "Development",
      date: "28 Desember 2023",
      readTime: "8 min read",
      image: "⚙️"
    }
  ]

  const categories = [
    { name: "Semua", count: blogPosts.length + featuredPosts.length },
    { name: "Design", count: 3 },
    { name: "SEO", count: 2 },
    { name: "E-Commerce", count: 2 },
    { name: "Marketing", count: 2 },
    { name: "Technical", count: 3 }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Blog WebJasa
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Insights, tips, dan panduan terbaru seputar web development, digital marketing, 
            dan strategi bisnis online untuk membantu mengembangkan bisnis Anda.
          </p>
        </div>
      </section>

      {/* Featured Posts */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-8">Artikel Unggulan</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {featuredPosts.map((post) => (
                <article key={post.id} className="card-gradient rounded-xl overflow-hidden hover-lift">
                  <div className="p-8">
                    <div className="flex items-center justify-between mb-4">
                      <span className="inline-block bg-blue-100 text-blue-600 text-sm font-medium px-3 py-1 rounded-full">
                        {post.category}
                      </span>
                      <div className="text-4xl">{post.image}</div>
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 mb-3 leading-tight">
                      <Link href={`/blog/${post.id}`} className="hover:text-blue-600 transition-colors">
                        {post.title}
                      </Link>
                    </h3>
                    <p className="text-gray-600 mb-4 leading-relaxed">
                      {post.excerpt}
                    </p>
                    <div className="flex items-center justify-between text-sm text-gray-500">
                      <span>{post.date}</span>
                      <span>{post.readTime}</span>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Blog Grid */}
      <section className="section-padding bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row gap-12">
            {/* Main Content */}
            <div className="lg:w-2/3">
              <h2 className="text-3xl font-bold text-gray-900 mb-8">Artikel Terbaru</h2>
              <div className="space-y-8">
                {blogPosts.map((post) => (
                  <article key={post.id} className="card-gradient rounded-xl p-6 hover-lift">
                    <div className="flex flex-col md:flex-row gap-6">
                      <div className="md:w-1/4 flex items-center justify-center">
                        <div className="w-16 h-16 bg-blue-100 rounded-xl flex items-center justify-center text-3xl">
                          {post.image}
                        </div>
                      </div>
                      <div className="md:w-3/4">
                        <div className="flex items-center gap-4 mb-3">
                          <span className="inline-block bg-blue-100 text-blue-600 text-sm font-medium px-3 py-1 rounded-full">
                            {post.category}
                          </span>
                          <span className="text-sm text-gray-500">{post.date}</span>
                          <span className="text-sm text-gray-500">{post.readTime}</span>
                        </div>
                        <h3 className="text-xl font-bold text-gray-900 mb-3 leading-tight">
                          <Link href={`/blog/${post.id}`} className="hover:text-blue-600 transition-colors">
                            {post.title}
                          </Link>
                        </h3>
                        <p className="text-gray-600 mb-4 leading-relaxed">
                          {post.excerpt}
                        </p>
                        <Link
                          href={`/blog/${post.id}`}
                          className="text-blue-600 font-medium hover:text-blue-700 transition-colors"
                        >
                          Baca Selengkapnya →
                        </Link>
                      </div>
                    </div>
                  </article>
                ))}
              </div>

              {/* Pagination */}
              <div className="mt-12 flex justify-center">
                <div className="flex items-center space-x-2">
                  <button className="px-4 py-2 border border-gray-300 rounded-lg text-gray-500 hover:bg-gray-50">
                    Previous
                  </button>
                  <button className="px-4 py-2 bg-blue-600 text-white rounded-lg">1</button>
                  <button className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">2</button>
                  <button className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">3</button>
                  <button className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
                    Next
                  </button>
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="lg:w-1/3 space-y-8">
              {/* Categories */}
              <div className="card-gradient rounded-xl p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Kategori</h3>
                <div className="space-y-2">
                  {categories.map((category, index) => (
                    <Link
                      key={index}
                      href={`/blog/category/${category.name.toLowerCase()}`}
                      className="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-blue-50 transition-colors"
                    >
                      <span className="text-gray-700">{category.name}</span>
                      <span className="text-sm text-gray-500">({category.count})</span>
                    </Link>
                  ))}
                </div>
              </div>

              {/* Newsletter */}
              <div className="card-gradient rounded-xl p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Newsletter</h3>
                <p className="text-gray-600 mb-4">
                  Dapatkan tips dan insights terbaru langsung di email Anda.
                </p>
                <form className="space-y-3">
                  <input
                    type="email"
                    placeholder="Email Anda"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button
                    type="submit"
                    className="w-full btn-primary"
                  >
                    Subscribe
                  </button>
                </form>
              </div>

              {/* Popular Posts */}
              <div className="card-gradient rounded-xl p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Artikel Populer</h3>
                <div className="space-y-4">
                  {blogPosts.slice(0, 3).map((post) => (
                    <Link
                      key={post.id}
                      href={`/blog/${post.id}`}
                      className="block group"
                    >
                      <div className="flex gap-3">
                        <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center text-lg flex-shrink-0">
                          {post.image}
                        </div>
                        <div>
                          <h4 className="text-sm font-medium text-gray-900 group-hover:text-blue-600 transition-colors leading-snug">
                            {post.title}
                          </h4>
                          <p className="text-xs text-gray-500 mt-1">{post.date}</p>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>

              {/* Contact CTA */}
              <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-6 text-white">
                <h3 className="text-xl font-bold mb-4">Butuh Website?</h3>
                <p className="text-blue-100 mb-4">
                  Konsultasikan kebutuhan website bisnis Anda dengan tim ahli kami.
                </p>
                <Link
                  href="/kontak"
                  className="block w-full bg-white text-blue-600 font-semibold py-3 px-6 rounded-lg text-center hover:bg-gray-100 transition-colors"
                >
                  Konsultasi Gratis
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="hero-gradient text-white section-padding">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Siap Mengimplementasikan Tips dari Blog?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Mari wujudkan website profesional untuk bisnis Anda dengan menerapkan 
            best practices dan strategi yang telah kami bagikan.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/kontak"
              className="bg-white text-blue-600 font-semibold py-3 px-8 rounded-lg hover:bg-gray-100 transition-all duration-300"
            >
              Mulai Proyek Website
            </Link>
            <Link
              href="/layanan"
              className="border-2 border-white text-white font-semibold py-3 px-8 rounded-lg hover:bg-white hover:text-blue-600 transition-all duration-300"
            >
              Lihat Layanan Kami
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}