# 🔗 WordPress Integration Guide

Panduan lengkap untuk mengintegrasikan portfolio website collection dengan WordPress untuk kemudahan pengelolaan konten.

## 🎯 Tujuan WordPress Integration

### ✅ Benefits
- **Content Management** - Edit konten tanpa coding
- **Dynamic Content** - Update otomatis tanpa redeploy
- **Multi-user** - Tim bisa edit bersama
- **SEO Advanced** - Plugin SEO WordPress
- **Blog Integration** - Sistem blog terintegrasi
- **E-commerce Ready** - WooCommerce support

## 🏗️ Architecture Overview

```
Frontend (Vercel) ← API → WordPress (Headless CMS) ← Admin Dashboard
```

### Components:
1. **WordPress Backend** - Content management + API
2. **Static Frontend** - HTML/CSS templates di Vercel
3. **API Connection** - WordPress REST API
4. **Content Sync** - Otomatis update konten

## 🚀 Implementation Methods

### Method 1: Headless WordPress (Recommended)
**WordPress sebagai CMS, Frontend tetap static**

### Method 2: WordPress Themes
**Convert HTML templates ke WordPress themes**

### Method 3: Hybrid Approach
**WordPress untuk blog/admin, static untuk landing pages**

---

## 📋 Method 1: Headless WordPress Setup

### A. WordPress Backend Setup

#### 1. Install WordPress
```bash
# Option 1: Local development
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz

# Option 2: Use hosting provider
# - Hostinger, Niagahoster, dll
# - Auto-install WordPress
```

#### 2. Enable REST API
```php
// functions.php
function enable_cors() {
    header("Access-Control-Allow-Origin: *");
    header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
    header("Access-Control-Allow-Headers: Content-Type");
}
add_action('init', 'enable_cors');

// Enable REST API for custom post types
add_action('init', function() {
    register_post_type('services', array(
        'public' => true,
        'show_in_rest' => true,
        'rest_base' => 'services',
        'supports' => array('title', 'editor', 'thumbnail', 'custom-fields')
    ));
    
    register_post_type('testimonials', array(
        'public' => true,
        'show_in_rest' => true,
        'rest_base' => 'testimonials',
        'supports' => array('title', 'editor', 'thumbnail', 'custom-fields')
    ));
    
    register_post_type('portfolio', array(
        'public' => true,
        'show_in_rest' => true,
        'rest_base' => 'portfolio',
        'supports' => array('title', 'editor', 'thumbnail', 'custom-fields')
    ));
});
```

#### 3. Install Required Plugins
```
- Advanced Custom Fields (ACF) - Custom fields
- WP REST API Controller - API management
- Yoast SEO - SEO optimization
- Contact Form 7 - Forms management
```

### B. Frontend Integration

#### 1. Create API Service
```javascript
// js/wordpress-api.js
class WordPressAPI {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }
    
    async getServices() {
        try {
            const response = await fetch(`${this.baseURL}/wp-json/wp/v2/services`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching services:', error);
            return [];
        }
    }
    
    async getTestimonials() {
        try {
            const response = await fetch(`${this.baseURL}/wp-json/wp/v2/testimonials`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching testimonials:', error);
            return [];
        }
    }
    
    async getPortfolio() {
        try {
            const response = await fetch(`${this.baseURL}/wp-json/wp/v2/portfolio`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching portfolio:', error);
            return [];
        }
    }
    
    async getPages(slug) {
        try {
            const response = await fetch(`${this.baseURL}/wp-json/wp/v2/pages?slug=${slug}`);
            const pages = await response.json();
            return pages[0] || null;
        } catch (error) {
            console.error('Error fetching page:', error);
            return null;
        }
    }
}

// Initialize API
const wpAPI = new WordPressAPI('https://your-wordpress-site.com');
```

#### 2. Dynamic Content Loading
```javascript
// js/content-loader.js
document.addEventListener('DOMContentLoaded', async function() {
    // Load services dynamically
    await loadServices();
    
    // Load testimonials
    await loadTestimonials();
    
    // Load portfolio items
    await loadPortfolio();
    
    // Load page content
    await loadPageContent();
});

async function loadServices() {
    const services = await wpAPI.getServices();
    const servicesContainer = document.getElementById('services-container');
    
    if (servicesContainer && services.length > 0) {
        servicesContainer.innerHTML = services.map(service => `
            <div class="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
                <div class="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mb-6">
                    <i class="fas fa-${service.acf.icon} text-2xl text-blue-600"></i>
                </div>
                <h3 class="text-xl font-semibold text-gray-800 mb-4">${service.title.rendered}</h3>
                <div class="text-gray-600 mb-6">${service.content.rendered}</div>
                <div class="text-blue-600 font-semibold">
                    ${service.acf.price ? `Mulai dari ${service.acf.price}` : 'Konsultasi Gratis'}
                </div>
            </div>
        `).join('');
    }
}

async function loadTestimonials() {
    const testimonials = await wpAPI.getTestimonials();
    const testimonialsContainer = document.getElementById('testimonials-container');
    
    if (testimonialsContainer && testimonials.length > 0) {
        testimonialsContainer.innerHTML = testimonials.map(testimonial => `
            <div class="bg-gray-50 rounded-xl p-8">
                <div class="flex text-yellow-400 mb-4 text-lg">
                    ${'★'.repeat(5)}
                </div>
                <p class="text-gray-600 mb-6 italic">"${testimonial.content.rendered}"</p>
                <div class="flex items-center">
                    <div class="bg-blue-200 w-12 h-12 rounded-full flex items-center justify-center mr-4">
                        <i class="fas fa-user text-blue-600"></i>
                    </div>
                    <div>
                        <p class="font-semibold text-gray-800">${testimonial.title.rendered}</p>
                        <p class="text-sm text-gray-600">${testimonial.acf.position || 'Client'}</p>
                    </div>
                </div>
            </div>
        `).join('');
    }
}

async function loadPortfolio() {
    const portfolio = await wpAPI.getPortfolio();
    const portfolioContainer = document.getElementById('portfolio-container');
    
    if (portfolioContainer && portfolio.length > 0) {
        portfolioContainer.innerHTML = portfolio.map(item => `
            <div class="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow">
                <div class="h-64 bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
                    ${item.featured_media ? 
                        `<img src="${item.acf.image}" alt="${item.title.rendered}" class="w-full h-full object-cover">` :
                        `<i class="fas fa-image text-6xl text-gray-400"></i>`
                    }
                </div>
                <div class="p-6">
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="text-lg font-semibold text-gray-800">${item.title.rendered}</h3>
                        <span class="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-semibold">
                            ${item.acf.category || 'Portfolio'}
                        </span>
                    </div>
                    <p class="text-gray-600 text-sm mb-4">${item.excerpt.rendered}</p>
                    <div class="flex items-center justify-between">
                        <span class="text-xs text-gray-500">${item.acf.location || 'Indonesia'} • ${new Date(item.date).getFullYear()}</span>
                        <button class="text-blue-600 hover:text-blue-700 font-semibold text-sm">
                            Lihat Detail <i class="fas fa-arrow-right ml-1"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }
}

async function loadPageContent() {
    const aboutPage = await wpAPI.getPages('tentang-kami');
    if (aboutPage) {
        const aboutSection = document.getElementById('about-content');
        if (aboutSection) {
            aboutSection.innerHTML = aboutPage.content.rendered;
        }
    }
}
```

#### 3. Form Integration
```javascript
// js/form-handler.js
class FormHandler {
    constructor(wpBaseURL) {
        this.wpBaseURL = wpBaseURL;
    }
    
    async submitContactForm(formData) {
        try {
            const response = await fetch(`${this.wpBaseURL}/wp-json/contact-form-7/v1/contact-forms/123/feedback`, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                this.showSuccess('Pesan berhasil dikirim! Kami akan menghubungi Anda segera.');
            } else {
                this.showError('Terjadi kesalahan. Silakan coba lagi.');
            }
        } catch (error) {
            this.showError('Koneksi bermasalah. Silakan coba lagi.');
        }
    }
    
    showSuccess(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'fixed top-4 right-4 bg-green-500 text-white p-4 rounded-lg shadow-lg z-50';
        alertDiv.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-check-circle mr-2"></i>
                <span>${message}</span>
            </div>
        `;
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
    
    showError(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'fixed top-4 right-4 bg-red-500 text-white p-4 rounded-lg shadow-lg z-50';
        alertDiv.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-exclamation-circle mr-2"></i>
                <span>${message}</span>
            </div>
        `;
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Initialize form handler
const formHandler = new FormHandler('https://your-wordpress-site.com');

// Handle form submissions
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        await formHandler.submitContactForm(formData);
    });
});
```

---

## 📋 Method 2: WordPress Theme Conversion

### A. Theme Structure
```
wp-content/themes/portfolio-collection/
├── index.php
├── style.css
├── functions.php
├── header.php
├── footer.php
├── single.php
├── page.php
├── templates/
│   ├── healthcare.php
│   ├── automotive.php
│   ├── business.php
│   └── digital.php
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── inc/
    ├── customizer.php
    └── post-types.php
```

### B. Convert HTML to PHP Templates

#### 1. Header Template
```php
<?php
// header.php
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php wp_title('|', true, 'right'); ?><?php bloginfo('name'); ?></title>
    <?php wp_head(); ?>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body <?php body_class(); ?>>
    <nav class="bg-white shadow-lg fixed w-full z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0 flex items-center">
                        <?php if (has_custom_logo()) : ?>
                            <?php the_custom_logo(); ?>
                        <?php else : ?>
                            <i class="fas fa-heartbeat text-2xl text-blue-600 mr-2"></i>
                            <span class="text-xl font-bold text-gray-800"><?php bloginfo('name'); ?></span>
                        <?php endif; ?>
                    </div>
                </div>
                <div class="hidden md:flex items-center space-x-8">
                    <?php
                    wp_nav_menu(array(
                        'theme_location' => 'primary',
                        'menu_class' => 'flex space-x-8',
                        'container' => false,
                        'fallback_cb' => false,
                    ));
                    ?>
                </div>
            </div>
        </div>
    </nav>
```

#### 2. Functions.php Setup
```php
<?php
// functions.php

// Theme setup
function portfolio_theme_setup() {
    // Add theme support
    add_theme_support('post-thumbnails');
    add_theme_support('custom-logo');
    add_theme_support('title-tag');
    add_theme_support('custom-header');
    
    // Register navigation menus
    register_nav_menus(array(
        'primary' => 'Primary Menu',
        'footer' => 'Footer Menu'
    ));
}
add_action('after_setup_theme', 'portfolio_theme_setup');

// Enqueue scripts and styles
function portfolio_scripts() {
    wp_enqueue_style('portfolio-style', get_stylesheet_uri());
    wp_enqueue_script('portfolio-script', get_template_directory_uri() . '/assets/js/main.js', array('jquery'), '1.0.0', true);
    
    // Localize script for AJAX
    wp_localize_script('portfolio-script', 'ajax_object', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('portfolio_nonce')
    ));
}
add_action('wp_enqueue_scripts', 'portfolio_scripts');

// Register custom post types
function register_portfolio_post_types() {
    // Services post type
    register_post_type('services', array(
        'labels' => array(
            'name' => 'Services',
            'singular_name' => 'Service'
        ),
        'public' => true,
        'has_archive' => true,
        'supports' => array('title', 'editor', 'thumbnail', 'custom-fields'),
        'menu_icon' => 'dashicons-admin-tools'
    ));
    
    // Portfolio post type
    register_post_type('portfolio', array(
        'labels' => array(
            'name' => 'Portfolio',
            'singular_name' => 'Portfolio Item'
        ),
        'public' => true,
        'has_archive' => true,
        'supports' => array('title', 'editor', 'thumbnail', 'custom-fields'),
        'menu_icon' => 'dashicons-portfolio'
    ));
    
    // Testimonials post type
    register_post_type('testimonials', array(
        'labels' => array(
            'name' => 'Testimonials',
            'singular_name' => 'Testimonial'
        ),
        'public' => true,
        'supports' => array('title', 'editor', 'thumbnail', 'custom-fields'),
        'menu_icon' => 'dashicons-format-quote'
    ));
}
add_action('init', 'register_portfolio_post_types');

// Add custom fields support
function add_portfolio_meta_boxes() {
    add_meta_box(
        'service_details',
        'Service Details',
        'service_details_callback',
        'services'
    );
    
    add_meta_box(
        'portfolio_details',
        'Portfolio Details',
        'portfolio_details_callback',
        'portfolio'
    );
}
add_action('add_meta_boxes', 'add_portfolio_meta_boxes');

function service_details_callback($post) {
    wp_nonce_field('save_service_details', 'service_details_nonce');
    
    $price = get_post_meta($post->ID, '_service_price', true);
    $icon = get_post_meta($post->ID, '_service_icon', true);
    $features = get_post_meta($post->ID, '_service_features', true);
    
    echo '<table class="form-table">';
    echo '<tr><th><label for="service_price">Price</label></th>';
    echo '<td><input type="text" id="service_price" name="service_price" value="' . esc_attr($price) . '" /></td></tr>';
    echo '<tr><th><label for="service_icon">Icon (FontAwesome)</label></th>';
    echo '<td><input type="text" id="service_icon" name="service_icon" value="' . esc_attr($icon) . '" /></td></tr>';
    echo '<tr><th><label for="service_features">Features (one per line)</label></th>';
    echo '<td><textarea id="service_features" name="service_features" rows="5" cols="50">' . esc_textarea($features) . '</textarea></td></tr>';
    echo '</table>';
}

// Save custom fields
function save_service_details($post_id) {
    if (!isset($_POST['service_details_nonce']) || !wp_verify_nonce($_POST['service_details_nonce'], 'save_service_details')) {
        return;
    }
    
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }
    
    if (!current_user_can('edit_post', $post_id)) {
        return;
    }
    
    if (isset($_POST['service_price'])) {
        update_post_meta($post_id, '_service_price', sanitize_text_field($_POST['service_price']));
    }
    
    if (isset($_POST['service_icon'])) {
        update_post_meta($post_id, '_service_icon', sanitize_text_field($_POST['service_icon']));
    }
    
    if (isset($_POST['service_features'])) {
        update_post_meta($post_id, '_service_features', sanitize_textarea_field($_POST['service_features']));
    }
}
add_action('save_post', 'save_service_details');

// AJAX handlers for dynamic content
function get_services_ajax() {
    check_ajax_referer('portfolio_nonce', 'nonce');
    
    $services = get_posts(array(
        'post_type' => 'services',
        'posts_per_page' => -1,
        'post_status' => 'publish'
    ));
    
    $services_data = array();
    foreach ($services as $service) {
        $services_data[] = array(
            'id' => $service->ID,
            'title' => $service->post_title,
            'content' => $service->post_content,
            'price' => get_post_meta($service->ID, '_service_price', true),
            'icon' => get_post_meta($service->ID, '_service_icon', true),
            'features' => get_post_meta($service->ID, '_service_features', true)
        );
    }
    
    wp_send_json_success($services_data);
}
add_action('wp_ajax_get_services', 'get_services_ajax');
add_action('wp_ajax_nopriv_get_services', 'get_services_ajax');
```

#### 3. Page Templates
```php
<?php
// page-healthcare.php (Healthcare template)
get_header();

// Get healthcare specific options
$hero_title = get_field('hero_title') ?: 'Pelayanan Kesehatan Terpercaya';
$hero_subtitle = get_field('hero_subtitle') ?: 'Memberikan layanan kesehatan terbaik dengan dokter berpengalaman';
$primary_color = get_field('primary_color') ?: '#0ea5e9';
?>

<style>
:root {
    --primary-color: <?php echo esc_attr($primary_color); ?>;
}
</style>

<!-- Hero Section -->
<section id="beranda" class="pt-16 bg-gradient-to-br from-blue-50 to-green-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
                <h1 class="text-4xl md:text-5xl font-bold text-gray-800 mb-6">
                    <?php echo esc_html($hero_title); ?>
                </h1>
                <p class="text-xl text-gray-600 mb-8 leading-relaxed">
                    <?php echo esc_html($hero_subtitle); ?>
                </p>
                <div class="flex flex-col sm:flex-row gap-4">
                    <a href="#layanan" class="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                        <i class="fas fa-calendar-check mr-2"></i>
                        Buat Janji
                    </a>
                    <a href="#kontak" class="border-2 border-blue-600 text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-600 hover:text-white transition-colors">
                        <i class="fas fa-phone mr-2"></i>
                        Hubungi Kami
                    </a>
                </div>
            </div>
            
            <div class="relative">
                <?php if (has_post_thumbnail()) : ?>
                    <?php the_post_thumbnail('large', array('class' => 'rounded-2xl shadow-xl')); ?>
                <?php else : ?>
                    <div class="bg-blue-100 rounded-2xl p-8 text-center">
                        <i class="fas fa-user-md text-6xl text-blue-600 mb-4"></i>
                        <p class="text-blue-800">Healthcare Professional</p>
                    </div>
                <?php endif; ?>
            </div>
        </div>
    </div>
</section>

<!-- Services Section -->
<section id="layanan" class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
            <h2 class="text-3xl font-bold text-gray-800 mb-4">Layanan Kami</h2>
            <p class="text-xl text-gray-600">Pelayanan kesehatan komprehensif untuk keluarga Anda</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="services-container">
            <?php
            $services = get_posts(array(
                'post_type' => 'services',
                'posts_per_page' => 6,
                'post_status' => 'publish'
            ));
            
            foreach ($services as $service) :
                $price = get_post_meta($service->ID, '_service_price', true);
                $icon = get_post_meta($service->ID, '_service_icon', true) ?: 'stethoscope';
            ?>
                <div class="bg-gray-50 rounded-xl p-8 hover:shadow-lg transition-shadow">
                    <div class="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mb-6">
                        <i class="fas fa-<?php echo esc_attr($icon); ?> text-2xl text-blue-600"></i>
                    </div>
                    <h3 class="text-xl font-semibold text-gray-800 mb-4"><?php echo esc_html($service->post_title); ?></h3>
                    <p class="text-gray-600 mb-6"><?php echo wp_trim_words($service->post_content, 20); ?></p>
                    <div class="flex justify-between items-center">
                        <?php if ($price) : ?>
                            <span class="text-blue-600 font-semibold"><?php echo esc_html($price); ?></span>
                        <?php endif; ?>
                        <a href="<?php echo get_permalink($service->ID); ?>" class="text-blue-600 hover:text-blue-700 font-semibold">
                            Selengkapnya <i class="fas fa-arrow-right ml-1"></i>
                        </a>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<!-- Testimonials Section -->
<section class="py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
            <h2 class="text-3xl font-bold text-gray-800 mb-4">Testimoni Pasien</h2>
            <p class="text-xl text-gray-600">Kepercayaan pasien adalah prioritas utama kami</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <?php
            $testimonials = get_posts(array(
                'post_type' => 'testimonials',
                'posts_per_page' => 3,
                'post_status' => 'publish'
            ));
            
            foreach ($testimonials as $testimonial) :
                $rating = get_post_meta($testimonial->ID, '_testimonial_rating', true) ?: 5;
                $position = get_post_meta($testimonial->ID, '_testimonial_position', true) ?: 'Pasien';
            ?>
                <div class="bg-white rounded-xl p-8">
                    <div class="flex text-yellow-400 mb-4 text-lg">
                        <?php for ($i = 0; $i < $rating; $i++) : ?>
                            <i class="fas fa-star"></i>
                        <?php endfor; ?>
                    </div>
                    <p class="text-gray-600 mb-6 italic">"<?php echo esc_html($testimonial->post_content); ?>"</p>
                    <div class="flex items-center">
                        <div class="bg-blue-200 w-12 h-12 rounded-full flex items-center justify-center mr-4">
                            <i class="fas fa-user text-blue-600"></i>
                        </div>
                        <div>
                            <p class="font-semibold text-gray-800"><?php echo esc_html($testimonial->post_title); ?></p>
                            <p class="text-sm text-gray-600"><?php echo esc_html($position); ?></p>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<?php get_footer(); ?>
```

---

## 🎛️ WordPress Admin Customization

### A. Custom Admin Dashboard
```php
// functions.php - Admin customization

// Custom admin dashboard
function portfolio_admin_dashboard() {
    wp_add_dashboard_widget(
        'portfolio_dashboard_widget',
        'Portfolio Website Stats',
        'portfolio_dashboard_widget_function'
    );
}
add_action('wp_dashboard_setup', 'portfolio_admin_dashboard');

function portfolio_dashboard_widget_function() {
    $services_count = wp_count_posts('services')->publish;
    $portfolio_count = wp_count_posts('portfolio')->publish;
    $testimonials_count = wp_count_posts('testimonials')->publish;
    
    echo '<div class="activity-block">';
    echo '<h3>Content Overview</h3>';
    echo '<ul>';
    echo '<li><strong>Services:</strong> ' . $services_count . ' published</li>';
    echo '<li><strong>Portfolio Items:</strong> ' . $portfolio_count . ' published</li>';
    echo '<li><strong>Testimonials:</strong> ' . $testimonials_count . ' published</li>';
    echo '</ul>';
    echo '</div>';
    
    echo '<div class="activity-block">';
    echo '<h3>Quick Actions</h3>';
    echo '<p><a href="' . admin_url('post-new.php?post_type=services') . '" class="button button-primary">Add New Service</a></p>';
    echo '<p><a href="' . admin_url('post-new.php?post_type=portfolio') . '" class="button button-primary">Add Portfolio Item</a></p>';
    echo '</div>';
}

// Custom admin menu
function portfolio_admin_menu() {
    add_menu_page(
        'Portfolio Settings',
        'Portfolio',
        'manage_options',
        'portfolio-settings',
        'portfolio_settings_page',
        'dashicons-portfolio',
        30
    );
    
    add_submenu_page(
        'portfolio-settings',
        'Industry Templates',
        'Templates',
        'manage_options',
        'portfolio-templates',
        'portfolio_templates_page'
    );
}
add_action('admin_menu', 'portfolio_admin_menu');

function portfolio_settings_page() {
    if (isset($_POST['submit'])) {
        update_option('portfolio_primary_color', sanitize_hex_color($_POST['primary_color']));
        update_option('portfolio_business_type', sanitize_text_field($_POST['business_type']));
        update_option('portfolio_company_name', sanitize_text_field($_POST['company_name']));
        echo '<div class="notice notice-success"><p>Settings saved!</p></div>';
    }
    
    $primary_color = get_option('portfolio_primary_color', '#2563eb');
    $business_type = get_option('portfolio_business_type', 'healthcare');
    $company_name = get_option('portfolio_company_name', '');
    
    ?>
    <div class="wrap">
        <h1>Portfolio Settings</h1>
        <form method="post" action="">
            <table class="form-table">
                <tr>
                    <th scope="row">Company Name</th>
                    <td><input type="text" name="company_name" value="<?php echo esc_attr($company_name); ?>" class="regular-text" /></td>
                </tr>
                <tr>
                    <th scope="row">Business Type</th>
                    <td>
                        <select name="business_type">
                            <option value="healthcare" <?php selected($business_type, 'healthcare'); ?>>Healthcare</option>
                            <option value="automotive" <?php selected($business_type, 'automotive'); ?>>Automotive</option>
                            <option value="business" <?php selected($business_type, 'business'); ?>>Business</option>
                            <option value="digital" <?php selected($business_type, 'digital'); ?>>Digital Services</option>
                            <option value="education" <?php selected($business_type, 'education'); ?>>Education</option>
                            <option value="professional" <?php selected($business_type, 'professional'); ?>>Professional</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Primary Color</th>
                    <td><input type="color" name="primary_color" value="<?php echo esc_attr($primary_color); ?>" /></td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}
```

### B. Industry Template Selector
```php
function portfolio_templates_page() {
    if (isset($_POST['apply_template'])) {
        $template = sanitize_text_field($_POST['template']);
        apply_industry_template($template);
        echo '<div class="notice notice-success"><p>Template applied successfully!</p></div>';
    }
    
    ?>
    <div class="wrap">
        <h1>Industry Templates</h1>
        <p>Choose a pre-designed template for your industry:</p>
        
        <form method="post" action="">
            <div class="template-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0;">
                
                <div class="template-card" style="border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
                    <h3>Healthcare Template</h3>
                    <p>Perfect for clinics, hospitals, and medical practices.</p>
                    <ul>
                        <li>Medical appointment booking</li>
                        <li>Doctor profiles</li>
                        <li>Service listings</li>
                        <li>Patient testimonials</li>
                    </ul>
                    <button type="submit" name="apply_template" value="healthcare" class="button button-primary">Apply Template</button>
                </div>
                
                <div class="template-card" style="border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
                    <h3>Automotive Template</h3>
                    <p>Ideal for car dealers, auto services, and transportation.</p>
                    <ul>
                        <li>Vehicle catalog</li>
                        <li>Financing calculator</li>
                        <li>Service booking</li>
                        <li>Inventory management</li>
                    </ul>
                    <button type="submit" name="apply_template" value="automotive" class="button button-primary">Apply Template</button>
                </div>
                
                <div class="template-card" style="border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
                    <h3>Business Template</h3>
                    <p>Great for restaurants, e-commerce, and retail businesses.</p>
                    <ul>
                        <li>Product/menu showcase</li>
                        <li>Online ordering</li>
                        <li>Customer reviews</li>
                        <li>Contact forms</li>
                    </ul>
                    <button type="submit" name="apply_template" value="business" class="button button-primary">Apply Template</button>
                </div>
                
                <div class="template-card" style="border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
                    <h3>Digital Services Template</h3>
                    <p>Perfect for digital agencies and tech companies.</p>
                    <ul>
                        <li>Service packages</li>
                        <li>Portfolio showcase</li>
                        <li>Case studies</li>
                        <li>Client testimonials</li>
                    </ul>
                    <button type="submit" name="apply_template" value="digital" class="button button-primary">Apply Template</button>
                </div>
                
            </div>
        </form>
    </div>
    <?php
}

function apply_industry_template($template) {
    // Delete existing content
    $post_types = array('services', 'portfolio', 'testimonials');
    foreach ($post_types as $post_type) {
        $posts = get_posts(array('post_type' => $post_type, 'posts_per_page' => -1));
        foreach ($posts as $post) {
            wp_delete_post($post->ID, true);
        }
    }
    
    // Apply template-specific content
    switch ($template) {
        case 'healthcare':
            create_healthcare_content();
            break;
        case 'automotive':
            create_automotive_content();
            break;
        case 'business':
            create_business_content();
            break;
        case 'digital':
            create_digital_content();
            break;
    }
}

function create_healthcare_content() {
    // Create healthcare services
    $services = array(
        array(
            'title' => 'Konsultasi Umum',
            'content' => 'Pemeriksaan kesehatan umum dengan dokter berpengalaman.',
            'price' => 'Rp 150.000',
            'icon' => 'stethoscope'
        ),
        array(
            'title' => 'Kardiologi',
            'content' => 'Pemeriksaan dan pengobatan penyakit jantung.',
            'price' => 'Rp 300.000',
            'icon' => 'heartbeat'
        ),
        array(
            'title' => 'Radiologi',
            'content' => 'Layanan rontgen dan imaging diagnostik.',
            'price' => 'Rp 200.000',
            'icon' => 'x-ray'
        )
    );
    
    foreach ($services as $service) {
        $post_id = wp_insert_post(array(
            'post_title' => $service['title'],
            'post_content' => $service['content'],
            'post_type' => 'services',
            'post_status' => 'publish'
        ));
        
        update_post_meta($post_id, '_service_price', $service['price']);
        update_post_meta($post_id, '_service_icon', $service['icon']);
    }
    
    // Create testimonials
    $testimonials = array(
        array(
            'title' => 'Sarah Putri',
            'content' => 'Pelayanan sangat profesional dan ramah. Dokternya berpengalaman dan fasilitas kliniknya modern.',
            'position' => 'Ibu Rumah Tangga'
        ),
        array(
            'title' => 'Ahmad Reza',
            'content' => 'Proses pemeriksaan cepat dan hasil diagnosanya akurat. Sangat puas dengan layanannya.',
            'position' => 'Karyawan Swasta'
        )
    );
    
    foreach ($testimonials as $testimonial) {
        $post_id = wp_insert_post(array(
            'post_title' => $testimonial['title'],
            'post_content' => $testimonial['content'],
            'post_type' => 'testimonials',
            'post_status' => 'publish'
        ));
        
        update_post_meta($post_id, '_testimonial_position', $testimonial['position']);
        update_post_meta($post_id, '_testimonial_rating', 5);
    }
}
```

---

## 🚀 Deployment Automation

### A. WordPress + Vercel Integration Script
```bash
#!/bin/bash
# deploy-wordpress.sh

echo "🚀 WordPress + Static Frontend Deployment"

# Function to deploy WordPress backend
deploy_wordpress() {
    echo "📦 Deploying WordPress backend..."
    
    read -p "Enter your hosting provider (hostinger/niagahoster/other): " hosting
    read -p "Enter your domain name: " domain
    
    echo "📝 Creating deployment package..."
    
    # Create WordPress deployment package
    mkdir -p wordpress-deploy
    cp -r wp-content/themes/portfolio-collection wordpress-deploy/
    
    # Create setup instructions
    cat > wordpress-deploy/SETUP.md << EOF
# WordPress Setup Instructions

1. Install WordPress on your hosting
2. Upload theme files to wp-content/themes/
3. Activate the Portfolio Collection theme
4. Install required plugins:
   - Advanced Custom Fields
   - Contact Form 7
   - Yoast SEO
5. Configure REST API endpoints
6. Update frontend API URLs

## API Endpoints:
- Services: ${domain}/wp-json/wp/v2/services
- Portfolio: ${domain}/wp-json/wp/v2/portfolio  
- Testimonials: ${domain}/wp-json/wp/v2/testimonials

EOF
    
    echo "✅ WordPress deployment package created in wordpress-deploy/"
}

# Function to deploy static frontend
deploy_frontend() {
    echo "🌐 Deploying static frontend to Vercel..."
    
    read -p "Enter WordPress API URL (e.g., https://api.yourdomain.com): " api_url
    
    # Update API configuration
    find portfolio-websites -name "*.html" -type f -exec sed -i "s|https://your-wordpress-site.com|$api_url|g" {} \;
    
    # Deploy to Vercel
    for website in portfolio-websites/*/; do
        if [ -d "$website" ]; then
            echo "Deploying $(basename "$website")..."
            cd "$website"
            
            # Add WordPress integration
            cat >> index.html << 'EOF'
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script>
// WordPress API integration
const WP_API_URL = 'API_URL_PLACEHOLDER';

async function loadWordPressContent() {
    try {
        const services = await axios.get(`${WP_API_URL}/wp-json/wp/v2/services`);
        const testimonials = await axios.get(`${WP_API_URL}/wp-json/wp/v2/testimonials`);
        
        // Update content dynamically
        updateServices(services.data);
        updateTestimonials(testimonials.data);
    } catch (error) {
        console.log('Using static content as fallback');
    }
}

// Load content when page loads
document.addEventListener('DOMContentLoaded', loadWordPressContent);
</script>
EOF
            
            # Replace placeholder with actual API URL
            sed -i "s|API_URL_PLACEHOLDER|$api_url|g" index.html
            
            # Deploy to Vercel
            vercel --prod --yes
            
            cd ../../..
        fi
    done
}

# Main menu
echo "Select deployment option:"
echo "1. Deploy WordPress backend only"
echo "2. Deploy static frontend only"  
echo "3. Deploy both (full integration)"
echo "4. Exit"

read -p "Choose option (1-4): " choice

case $choice in
    1)
        deploy_wordpress
        ;;
    2)
        deploy_frontend
        ;;
    3)
        deploy_wordpress
        deploy_frontend
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo "🎉 Deployment completed!"
```

### B. Content Sync Automation
```javascript
// scripts/content-sync.js
const axios = require('axios');
const fs = require('fs');
const path = require('path');

class ContentSync {
    constructor(wpApiUrl) {
        this.wpApiUrl = wpApiUrl;
    }
    
    async syncAllContent() {
        console.log('🔄 Starting content sync...');
        
        try {
            const services = await this.fetchServices();
            const testimonials = await this.fetchTestimonials();
            const portfolio = await this.fetchPortfolio();
            
            // Update each website
            const websites = [
                'portfolio-websites/healthcare/klinik-sehat',
                'portfolio-websites/automotive/dealer-mobil',
                'portfolio-websites/business/toko-online'
                // Add more websites as needed
            ];
            
            for (const website of websites) {
                await this.updateWebsite(website, {
                    services,
                    testimonials, 
                    portfolio
                });
            }
            
            console.log('✅ Content sync completed!');
        } catch (error) {
            console.error('❌ Sync failed:', error.message);
        }
    }
    
    async fetchServices() {
        const response = await axios.get(`${this.wpApiUrl}/wp-json/wp/v2/services`);
        return response.data;
    }
    
    async fetchTestimonials() {
        const response = await axios.get(`${this.wpApiUrl}/wp-json/wp/v2/testimonials`);
        return response.data;
    }
    
    async fetchPortfolio() {
        const response = await axios.get(`${this.wpApiUrl}/wp-json/wp/v2/portfolio`);
        return response.data;
    }
    
    async updateWebsite(websitePath, content) {
        console.log(`📝 Updating ${websitePath}...`);
        
        const indexPath = path.join(websitePath, 'index.html');
        let html = fs.readFileSync(indexPath, 'utf8');
        
        // Update services section
        const servicesHtml = this.generateServicesHtml(content.services);
        html = html.replace(
            /<!-- SERVICES_START -->.*<!-- SERVICES_END -->/s,
            `<!-- SERVICES_START -->\n${servicesHtml}\n<!-- SERVICES_END -->`
        );
        
        // Update testimonials section
        const testimonialsHtml = this.generateTestimonialsHtml(content.testimonials);
        html = html.replace(
            /<!-- TESTIMONIALS_START -->.*<!-- TESTIMONIALS_END -->/s,
            `<!-- TESTIMONIALS_START -->\n${testimonialsHtml}\n<!-- TESTIMONIALS_END -->`
        );
        
        fs.writeFileSync(indexPath, html);
        console.log(`✅ Updated ${websitePath}`);
    }
    
    generateServicesHtml(services) {
        return services.map(service => `
            <div class="bg-gray-50 rounded-xl p-8 hover:shadow-lg transition-shadow">
                <div class="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mb-6">
                    <i class="fas fa-${service.acf?.icon || 'star'} text-2xl text-blue-600"></i>
                </div>
                <h3 class="text-xl font-semibold text-gray-800 mb-4">${service.title.rendered}</h3>
                <p class="text-gray-600 mb-6">${service.excerpt.rendered}</p>
                <div class="flex justify-between items-center">
                    ${service.acf?.price ? `<span class="text-blue-600 font-semibold">${service.acf.price}</span>` : ''}
                    <a href="#" class="text-blue-600 hover:text-blue-700 font-semibold">
                        Selengkapnya <i class="fas fa-arrow-right ml-1"></i>
                    </a>
                </div>
            </div>
        `).join('');
    }
    
    generateTestimonialsHtml(testimonials) {
        return testimonials.map(testimonial => `
            <div class="bg-white rounded-xl p-8">
                <div class="flex text-yellow-400 mb-4 text-lg">
                    ${'★'.repeat(testimonial.acf?.rating || 5)}
                </div>
                <p class="text-gray-600 mb-6 italic">"${testimonial.content.rendered}"</p>
                <div class="flex items-center">
                    <div class="bg-blue-200 w-12 h-12 rounded-full flex items-center justify-center mr-4">
                        <i class="fas fa-user text-blue-600"></i>
                    </div>
                    <div>
                        <p class="font-semibold text-gray-800">${testimonial.title.rendered}</p>
                        <p class="text-sm text-gray-600">${testimonial.acf?.position || 'Client'}</p>
                    </div>
                </div>
            </div>
        `).join('');
    }
}

// Usage
const contentSync = new ContentSync('https://your-wordpress-site.com');
contentSync.syncAllContent();
```

---

## 📋 Quick Setup Commands

### WordPress Integration Setup:
```bash
# 1. Setup WordPress backend
./deploy-wordpress.sh

# 2. Install required plugins
wp plugin install advanced-custom-fields contact-form-7 wordpress-seo --activate

# 3. Sync content to static sites
node scripts/content-sync.js

# 4. Deploy to Vercel
./deploy.sh --deploy-all
```

### One-Line WordPress Theme Install:
```bash
# Download and install theme
wget https://github.com/your-repo/portfolio-wordpress-theme.zip
unzip portfolio-wordpress-theme.zip -d wp-content/themes/
```

---

## 🎉 **WordPress Integration Complete!**

Sekarang Anda memiliki **sistem hybrid yang powerful**:

✅ **WordPress Backend** - Easy content management  
✅ **Static Frontend** - Fast loading, Vercel hosted  
✅ **API Integration** - Dynamic content updates  
✅ **Multi-template Support** - Industry-specific themes  
✅ **Automated Deployment** - One-click setup  

**Total waktu setup: 15 menit untuk full WordPress integration! 🚀**