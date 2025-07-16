#!/bin/bash

# 🚀 WordPress + Portfolio Integration Deployment Script
# Script otomatis untuk deploy WordPress backend dan static frontend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}[WORDPRESS]${NC} $1"
}

# Function to create WordPress theme structure
create_wordpress_theme() {
    local theme_name="portfolio-collection"
    local theme_dir="wordpress-deploy/wp-content/themes/$theme_name"
    
    print_header "Creating WordPress theme structure..."
    
    # Create theme directories
    mkdir -p "$theme_dir"/{templates,assets/{css,js,images},inc}
    
    # Create style.css with theme header
    cat > "$theme_dir/style.css" << 'EOF'
/*
Theme Name: Portfolio Collection
Description: Professional portfolio theme with industry-specific templates for Indonesian businesses. Supports healthcare, automotive, business, digital services, education, and professional sectors.
Version: 1.0.0
Author: Portfolio Collection Team
Text Domain: portfolio-collection
Requires at least: 5.0
Tested up to: 6.4
Requires PHP: 7.4
License: GPL v2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Tags: business, portfolio, professional, responsive, custom-post-types, tailwind
*/

/* Basic theme styles */
:root {
    --primary-blue: #2563eb;
    --primary-blue-dark: #1d4ed8;
    --primary-blue-light: #60a5fa;
    --success-green: #10b981;
    --warning-yellow: #f59e0b;
    --error-red: #ef4444;
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-800: #1f2937;
    --gray-900: #111827;
}

body {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    line-height: 1.6;
    color: var(--gray-800);
}

.wp-admin .portfolio-admin-header {
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
    color: white;
    padding: 20px;
    margin: 0 -20px 20px -20px;
    border-radius: 8px;
}

.template-selector {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.template-card {
    border: 2px solid #e5e7eb;
    padding: 24px;
    border-radius: 12px;
    transition: all 0.3s ease;
    background: white;
}

.template-card:hover {
    border-color: var(--primary-blue);
    box-shadow: 0 10px 25px rgba(37, 99, 235, 0.1);
    transform: translateY(-2px);
}

.template-card.active {
    border-color: var(--primary-blue);
    background: #eff6ff;
}

.template-preview {
    width: 100%;
    height: 120px;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    border-radius: 8px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2em;
    color: var(--primary-blue);
}
EOF

    # Create functions.php
    cat > "$theme_dir/functions.php" << 'EOF'
<?php
/**
 * Portfolio Collection Theme Functions
 * 
 * @package PortfolioCollection
 * @version 1.0.0
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Theme version
define('PORTFOLIO_THEME_VERSION', '1.0.0');

/**
 * Theme Setup
 */
function portfolio_theme_setup() {
    // Add theme support
    add_theme_support('post-thumbnails');
    add_theme_support('custom-logo', array(
        'height'      => 100,
        'width'       => 400,
        'flex-height' => true,
        'flex-width'  => true,
    ));
    add_theme_support('title-tag');
    add_theme_support('custom-header');
    add_theme_support('custom-background');
    add_theme_support('automatic-feed-links');
    
    // HTML5 support
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
    ));
    
    // Register navigation menus
    register_nav_menus(array(
        'primary' => __('Primary Menu', 'portfolio-collection'),
        'footer'  => __('Footer Menu', 'portfolio-collection'),
        'mobile'  => __('Mobile Menu', 'portfolio-collection'),
    ));
    
    // Add image sizes
    add_image_size('portfolio-thumbnail', 400, 300, true);
    add_image_size('portfolio-large', 800, 600, true);
    add_image_size('service-icon', 100, 100, true);
}
add_action('after_setup_theme', 'portfolio_theme_setup');

/**
 * Enqueue Scripts and Styles
 */
function portfolio_scripts() {
    // Styles
    wp_enqueue_style('portfolio-style', get_stylesheet_uri(), array(), PORTFOLIO_THEME_VERSION);
    wp_enqueue_style('tailwind-css', 'https://cdn.tailwindcss.com', array(), '3.3.0');
    wp_enqueue_style('font-awesome', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css', array(), '6.0.0');
    
    // Scripts
    wp_enqueue_script('portfolio-script', get_template_directory_uri() . '/assets/js/main.js', array('jquery'), PORTFOLIO_THEME_VERSION, true);
    
    // Localize script for AJAX
    wp_localize_script('portfolio-script', 'portfolio_ajax', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce'    => wp_create_nonce('portfolio_nonce'),
        'api_url'  => home_url('/wp-json/wp/v2/'),
    ));
    
    // Load comment reply script
    if (is_singular() && comments_open() && get_option('thread_comments')) {
        wp_enqueue_script('comment-reply');
    }
}
add_action('wp_enqueue_scripts', 'portfolio_scripts');

/**
 * Admin Scripts and Styles
 */
function portfolio_admin_scripts($hook) {
    wp_enqueue_style('portfolio-admin', get_template_directory_uri() . '/assets/css/admin.css', array(), PORTFOLIO_THEME_VERSION);
    wp_enqueue_script('portfolio-admin', get_template_directory_uri() . '/assets/js/admin.js', array('jquery'), PORTFOLIO_THEME_VERSION, true);
}
add_action('admin_enqueue_scripts', 'portfolio_admin_scripts');

/**
 * Register Custom Post Types
 */
function register_portfolio_post_types() {
    // Services Post Type
    register_post_type('services', array(
        'labels' => array(
            'name'                  => _x('Services', 'Post type general name', 'portfolio-collection'),
            'singular_name'         => _x('Service', 'Post type singular name', 'portfolio-collection'),
            'menu_name'             => _x('Services', 'Admin Menu text', 'portfolio-collection'),
            'add_new'               => __('Add New', 'portfolio-collection'),
            'add_new_item'          => __('Add New Service', 'portfolio-collection'),
            'new_item'              => __('New Service', 'portfolio-collection'),
            'edit_item'             => __('Edit Service', 'portfolio-collection'),
            'view_item'             => __('View Service', 'portfolio-collection'),
            'all_items'             => __('All Services', 'portfolio-collection'),
            'search_items'          => __('Search Services', 'portfolio-collection'),
            'not_found'             => __('No services found.', 'portfolio-collection'),
            'not_found_in_trash'    => __('No services found in Trash.', 'portfolio-collection'),
        ),
        'public'             => true,
        'publicly_queryable' => true,
        'show_ui'            => true,
        'show_in_menu'       => true,
        'show_in_rest'       => true,
        'rest_base'          => 'services',
        'query_var'          => true,
        'rewrite'            => array('slug' => 'services'),
        'capability_type'    => 'post',
        'has_archive'        => true,
        'hierarchical'       => false,
        'menu_position'      => 20,
        'menu_icon'          => 'dashicons-admin-tools',
        'supports'           => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
    ));
    
    // Portfolio Post Type
    register_post_type('portfolio', array(
        'labels' => array(
            'name'                  => _x('Portfolio', 'Post type general name', 'portfolio-collection'),
            'singular_name'         => _x('Portfolio Item', 'Post type singular name', 'portfolio-collection'),
            'menu_name'             => _x('Portfolio', 'Admin Menu text', 'portfolio-collection'),
            'add_new'               => __('Add New', 'portfolio-collection'),
            'add_new_item'          => __('Add New Portfolio Item', 'portfolio-collection'),
            'new_item'              => __('New Portfolio Item', 'portfolio-collection'),
            'edit_item'             => __('Edit Portfolio Item', 'portfolio-collection'),
            'view_item'             => __('View Portfolio Item', 'portfolio-collection'),
            'all_items'             => __('All Portfolio', 'portfolio-collection'),
            'search_items'          => __('Search Portfolio', 'portfolio-collection'),
            'not_found'             => __('No portfolio items found.', 'portfolio-collection'),
            'not_found_in_trash'    => __('No portfolio items found in Trash.', 'portfolio-collection'),
        ),
        'public'             => true,
        'publicly_queryable' => true,
        'show_ui'            => true,
        'show_in_menu'       => true,
        'show_in_rest'       => true,
        'rest_base'          => 'portfolio',
        'query_var'          => true,
        'rewrite'            => array('slug' => 'portfolio'),
        'capability_type'    => 'post',
        'has_archive'        => true,
        'hierarchical'       => false,
        'menu_position'      => 21,
        'menu_icon'          => 'dashicons-portfolio',
        'supports'           => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
    ));
    
    // Testimonials Post Type
    register_post_type('testimonials', array(
        'labels' => array(
            'name'                  => _x('Testimonials', 'Post type general name', 'portfolio-collection'),
            'singular_name'         => _x('Testimonial', 'Post type singular name', 'portfolio-collection'),
            'menu_name'             => _x('Testimonials', 'Admin Menu text', 'portfolio-collection'),
            'add_new'               => __('Add New', 'portfolio-collection'),
            'add_new_item'          => __('Add New Testimonial', 'portfolio-collection'),
            'new_item'              => __('New Testimonial', 'portfolio-collection'),
            'edit_item'             => __('Edit Testimonial', 'portfolio-collection'),
            'view_item'             => __('View Testimonial', 'portfolio-collection'),
            'all_items'             => __('All Testimonials', 'portfolio-collection'),
            'search_items'          => __('Search Testimonials', 'portfolio-collection'),
            'not_found'             => __('No testimonials found.', 'portfolio-collection'),
            'not_found_in_trash'    => __('No testimonials found in Trash.', 'portfolio-collection'),
        ),
        'public'             => true,
        'publicly_queryable' => true,
        'show_ui'            => true,
        'show_in_menu'       => true,
        'show_in_rest'       => true,
        'rest_base'          => 'testimonials',
        'query_var'          => true,
        'rewrite'            => array('slug' => 'testimonials'),
        'capability_type'    => 'post',
        'has_archive'        => false,
        'hierarchical'       => false,
        'menu_position'      => 22,
        'menu_icon'          => 'dashicons-format-quote',
        'supports'           => array('title', 'editor', 'thumbnail', 'custom-fields'),
    ));
}
add_action('init', 'register_portfolio_post_types');

/**
 * Enable CORS for REST API
 */
function portfolio_enable_cors() {
    remove_filter('rest_pre_serve_request', 'rest_send_cors_headers');
    add_filter('rest_pre_serve_request', function($value) {
        header('Access-Control-Allow-Origin: *');
        header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
        header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');
        header('Access-Control-Allow-Credentials: true');
        return $value;
    });
}
add_action('rest_api_init', 'portfolio_enable_cors');

/**
 * Add custom meta boxes
 */
function add_portfolio_meta_boxes() {
    // Service meta box
    add_meta_box(
        'service_details',
        __('Service Details', 'portfolio-collection'),
        'service_details_callback',
        'services',
        'normal',
        'high'
    );
    
    // Portfolio meta box
    add_meta_box(
        'portfolio_details',
        __('Portfolio Details', 'portfolio-collection'),
        'portfolio_details_callback',
        'portfolio',
        'normal',
        'high'
    );
    
    // Testimonial meta box
    add_meta_box(
        'testimonial_details',
        __('Testimonial Details', 'portfolio-collection'),
        'testimonial_details_callback',
        'testimonials',
        'normal',
        'high'
    );
}
add_action('add_meta_boxes', 'add_portfolio_meta_boxes');

/**
 * Service meta box callback
 */
function service_details_callback($post) {
    wp_nonce_field('save_service_details', 'service_details_nonce');
    
    $price = get_post_meta($post->ID, '_service_price', true);
    $icon = get_post_meta($post->ID, '_service_icon', true);
    $features = get_post_meta($post->ID, '_service_features', true);
    $category = get_post_meta($post->ID, '_service_category', true);
    
    ?>
    <table class="form-table">
        <tr>
            <th scope="row"><label for="service_price"><?php _e('Price', 'portfolio-collection'); ?></label></th>
            <td>
                <input type="text" id="service_price" name="service_price" value="<?php echo esc_attr($price); ?>" class="regular-text" placeholder="e.g., Rp 150.000" />
                <p class="description"><?php _e('Service price in Indonesian Rupiah', 'portfolio-collection'); ?></p>
            </td>
        </tr>
        <tr>
            <th scope="row"><label for="service_icon"><?php _e('Icon', 'portfolio-collection'); ?></label></th>
            <td>
                <input type="text" id="service_icon" name="service_icon" value="<?php echo esc_attr($icon); ?>" class="regular-text" placeholder="e.g., stethoscope" />
                <p class="description"><?php _e('FontAwesome icon name (without fa- prefix)', 'portfolio-collection'); ?></p>
            </td>
        </tr>
        <tr>
            <th scope="row"><label for="service_category"><?php _e('Category', 'portfolio-collection'); ?></label></th>
            <td>
                <select id="service_category" name="service_category">
                    <option value=""><?php _e('Select Category', 'portfolio-collection'); ?></option>
                    <option value="healthcare" <?php selected($category, 'healthcare'); ?>><?php _e('Healthcare', 'portfolio-collection'); ?></option>
                    <option value="automotive" <?php selected($category, 'automotive'); ?>><?php _e('Automotive', 'portfolio-collection'); ?></option>
                    <option value="business" <?php selected($category, 'business'); ?>><?php _e('Business', 'portfolio-collection'); ?></option>
                    <option value="digital" <?php selected($category, 'digital'); ?>><?php _e('Digital Services', 'portfolio-collection'); ?></option>
                    <option value="education" <?php selected($category, 'education'); ?>><?php _e('Education', 'portfolio-collection'); ?></option>
                    <option value="professional" <?php selected($category, 'professional'); ?>><?php _e('Professional', 'portfolio-collection'); ?></option>
                </select>
            </td>
        </tr>
        <tr>
            <th scope="row"><label for="service_features"><?php _e('Features', 'portfolio-collection'); ?></label></th>
            <td>
                <textarea id="service_features" name="service_features" rows="5" cols="50" class="large-text"><?php echo esc_textarea($features); ?></textarea>
                <p class="description"><?php _e('One feature per line', 'portfolio-collection'); ?></p>
            </td>
        </tr>
    </table>
    <?php
}

/**
 * Save service meta
 */
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
    
    $fields = array('service_price', 'service_icon', 'service_features', 'service_category');
    
    foreach ($fields as $field) {
        if (isset($_POST[$field])) {
            update_post_meta($post_id, '_' . $field, sanitize_text_field($_POST[$field]));
        }
    }
}
add_action('save_post', 'save_service_details');

/**
 * Custom admin dashboard
 */
function portfolio_admin_dashboard() {
    wp_add_dashboard_widget(
        'portfolio_dashboard_widget',
        __('Portfolio Website Stats', 'portfolio-collection'),
        'portfolio_dashboard_widget_function'
    );
}
add_action('wp_dashboard_setup', 'portfolio_admin_dashboard');

function portfolio_dashboard_widget_function() {
    $services_count = wp_count_posts('services')->publish;
    $portfolio_count = wp_count_posts('portfolio')->publish;
    $testimonials_count = wp_count_posts('testimonials')->publish;
    
    ?>
    <div class="portfolio-admin-header">
        <h3><i class="fas fa-chart-bar"></i> <?php _e('Content Overview', 'portfolio-collection'); ?></h3>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
        <div style="text-align: center; padding: 16px; background: #f8fafc; border-radius: 8px;">
            <div style="font-size: 2em; color: #2563eb; margin-bottom: 8px;">
                <i class="fas fa-cogs"></i>
            </div>
            <div style="font-size: 1.5em; font-weight: bold; color: #1f2937;"><?php echo $services_count; ?></div>
            <div style="color: #6b7280;"><?php _e('Services', 'portfolio-collection'); ?></div>
        </div>
        
        <div style="text-align: center; padding: 16px; background: #f8fafc; border-radius: 8px;">
            <div style="font-size: 2em; color: #059669; margin-bottom: 8px;">
                <i class="fas fa-briefcase"></i>
            </div>
            <div style="font-size: 1.5em; font-weight: bold; color: #1f2937;"><?php echo $portfolio_count; ?></div>
            <div style="color: #6b7280;"><?php _e('Portfolio Items', 'portfolio-collection'); ?></div>
        </div>
        
        <div style="text-align: center; padding: 16px; background: #f8fafc; border-radius: 8px;">
            <div style="font-size: 2em; color: #dc2626; margin-bottom: 8px;">
                <i class="fas fa-quote-right"></i>
            </div>
            <div style="font-size: 1.5em; font-weight: bold; color: #1f2937;"><?php echo $testimonials_count; ?></div>
            <div style="color: #6b7280;"><?php _e('Testimonials', 'portfolio-collection'); ?></div>
        </div>
    </div>
    
    <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
        <h4><?php _e('Quick Actions', 'portfolio-collection'); ?></h4>
        <p>
            <a href="<?php echo admin_url('post-new.php?post_type=services'); ?>" class="button button-primary">
                <i class="fas fa-plus"></i> <?php _e('Add New Service', 'portfolio-collection'); ?>
            </a>
            <a href="<?php echo admin_url('post-new.php?post_type=portfolio'); ?>" class="button button-secondary">
                <i class="fas fa-plus"></i> <?php _e('Add Portfolio Item', 'portfolio-collection'); ?>
            </a>
        </p>
    </div>
    <?php
}

/**
 * Include additional files
 */
require_once get_template_directory() . '/inc/customizer.php';
require_once get_template_directory() . '/inc/template-functions.php';

// Load theme textdomain
function portfolio_load_textdomain() {
    load_theme_textdomain('portfolio-collection', get_template_directory() . '/languages');
}
add_action('after_setup_theme', 'portfolio_load_textdomain');
EOF

    # Create index.php
    cat > "$theme_dir/index.php" << 'EOF'
<?php
/**
 * The main template file
 *
 * @package PortfolioCollection
 */

get_header(); ?>

<main id="primary" class="site-main">
    <div class="container mx-auto px-4 py-8">
        
        <?php if (have_posts()) : ?>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <?php while (have_posts()) : the_post(); ?>
                    <article id="post-<?php the_ID(); ?>" <?php post_class('bg-white rounded-lg shadow-lg overflow-hidden'); ?>>
                        
                        <?php if (has_post_thumbnail()) : ?>
                            <div class="aspect-w-16 aspect-h-9">
                                <?php the_post_thumbnail('portfolio-large', array('class' => 'w-full h-48 object-cover')); ?>
                            </div>
                        <?php endif; ?>
                        
                        <div class="p-6">
                            <h2 class="text-xl font-semibold text-gray-800 mb-2">
                                <a href="<?php the_permalink(); ?>" class="hover:text-blue-600 transition-colors">
                                    <?php the_title(); ?>
                                </a>
                            </h2>
                            
                            <div class="text-gray-600 mb-4">
                                <?php the_excerpt(); ?>
                            </div>
                            
                            <div class="flex justify-between items-center">
                                <span class="text-sm text-gray-500">
                                    <?php echo get_the_date(); ?>
                                </span>
                                <a href="<?php the_permalink(); ?>" class="text-blue-600 hover:text-blue-700 font-semibold">
                                    <?php _e('Read More', 'portfolio-collection'); ?> <i class="fas fa-arrow-right ml-1"></i>
                                </a>
                            </div>
                        </div>
                    </article>
                <?php endwhile; ?>
            </div>
            
            <?php the_posts_navigation(); ?>
            
        <?php else : ?>
            
            <div class="text-center py-12">
                <h1 class="text-2xl font-bold text-gray-800 mb-4">
                    <?php _e('Nothing here', 'portfolio-collection'); ?>
                </h1>
                <p class="text-gray-600">
                    <?php _e('It looks like nothing was found at this location. Maybe try a search?', 'portfolio-collection'); ?>
                </p>
                <?php get_search_form(); ?>
            </div>
            
        <?php endif; ?>
        
    </div>
</main>

<?php get_footer(); ?>
EOF

    # Create header.php
    cat > "$theme_dir/header.php" << 'EOF'
<?php
/**
 * The header for our theme
 *
 * @package PortfolioCollection
 */

?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div id="page" class="site min-h-screen flex flex-col">
    <a class="skip-link screen-reader-text" href="#primary"><?php _e('Skip to content', 'portfolio-collection'); ?></a>

    <header id="masthead" class="site-header bg-white shadow-lg fixed w-full z-50">
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <div class="site-branding flex items-center">
                        <?php if (has_custom_logo()) : ?>
                            <?php the_custom_logo(); ?>
                        <?php else : ?>
                            <?php
                            $business_type = get_option('portfolio_business_type', 'healthcare');
                            $icons = array(
                                'healthcare' => 'heartbeat',
                                'automotive' => 'car',
                                'business' => 'store',
                                'digital' => 'laptop',
                                'education' => 'graduation-cap',
                                'professional' => 'briefcase'
                            );
                            $icon = isset($icons[$business_type]) ? $icons[$business_type] : 'star';
                            ?>
                            <i class="fas fa-<?php echo esc_attr($icon); ?> text-2xl text-blue-600 mr-2"></i>
                            <span class="text-xl font-bold text-gray-800">
                                <?php bloginfo('name'); ?>
                            </span>
                        <?php endif; ?>
                    </div>
                </div>
                
                <div class="hidden md:flex items-center space-x-8">
                    <?php
                    wp_nav_menu(array(
                        'theme_location' => 'primary',
                        'menu_class'     => 'flex space-x-8',
                        'container'      => false,
                        'fallback_cb'    => false,
                        'walker'         => new Portfolio_Walker_Nav_Menu(),
                    ));
                    ?>
                </div>
                
                <div class="md:hidden flex items-center">
                    <button class="mobile-menu-button text-gray-700 hover:text-blue-600 focus:outline-none">
                        <i class="fas fa-bars text-xl"></i>
                    </button>
                </div>
            </div>
            
            <!-- Mobile menu -->
            <div class="mobile-menu hidden md:hidden">
                <div class="px-2 pt-2 pb-3 space-y-1 bg-white border-t">
                    <?php
                    wp_nav_menu(array(
                        'theme_location' => 'mobile',
                        'menu_class'     => 'space-y-1',
                        'container'      => false,
                        'fallback_cb'    => false,
                    ));
                    ?>
                </div>
            </div>
        </nav>
    </header>

    <div id="content" class="site-content flex-grow pt-16">
EOF

    # Create footer.php
    cat > "$theme_dir/footer.php" << 'EOF'
<?php
/**
 * The template for displaying the footer
 *
 * @package PortfolioCollection
 */

?>

    </div><!-- #content -->

    <footer id="colophon" class="site-footer bg-gray-800 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
                
                <div>
                    <div class="flex items-center mb-4">
                        <?php if (has_custom_logo()) : ?>
                            <?php the_custom_logo(); ?>
                        <?php else : ?>
                            <i class="fas fa-heartbeat text-2xl text-blue-400 mr-2"></i>
                            <span class="text-xl font-bold"><?php bloginfo('name'); ?></span>
                        <?php endif; ?>
                    </div>
                    <p class="text-gray-400 mb-4">
                        <?php bloginfo('description'); ?>
                    </p>
                    <div class="flex space-x-4">
                        <a href="#" class="text-gray-400 hover:text-blue-400 transition-colors">
                            <i class="fab fa-facebook-f"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-blue-400 transition-colors">
                            <i class="fab fa-instagram"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-blue-400 transition-colors">
                            <i class="fab fa-linkedin"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-blue-400 transition-colors">
                            <i class="fab fa-twitter"></i>
                        </a>
                    </div>
                </div>
                
                <div>
                    <h3 class="text-lg font-semibold mb-4"><?php _e('Services', 'portfolio-collection'); ?></h3>
                    <?php
                    $services = get_posts(array(
                        'post_type' => 'services',
                        'posts_per_page' => 5,
                        'post_status' => 'publish'
                    ));
                    
                    if ($services) :
                    ?>
                        <ul class="space-y-2">
                            <?php foreach ($services as $service) : ?>
                                <li>
                                    <a href="<?php echo get_permalink($service->ID); ?>" class="text-gray-400 hover:text-white transition-colors">
                                        <?php echo esc_html($service->post_title); ?>
                                    </a>
                                </li>
                            <?php endforeach; ?>
                        </ul>
                    <?php endif; ?>
                </div>
                
                <div>
                    <h3 class="text-lg font-semibold mb-4"><?php _e('Company', 'portfolio-collection'); ?></h3>
                    <?php
                    wp_nav_menu(array(
                        'theme_location' => 'footer',
                        'menu_class'     => 'space-y-2',
                        'container'      => false,
                        'fallback_cb'    => false,
                        'walker'         => new Portfolio_Walker_Footer_Menu(),
                    ));
                    ?>
                </div>
                
                <div>
                    <h3 class="text-lg font-semibold mb-4"><?php _e('Contact', 'portfolio-collection'); ?></h3>
                    <div class="space-y-2 text-gray-400">
                        <div class="flex items-center">
                            <i class="fas fa-map-marker-alt mr-2"></i>
                            <span><?php echo get_option('portfolio_address', 'Jakarta, Indonesia'); ?></span>
                        </div>
                        <div class="flex items-center">
                            <i class="fas fa-phone mr-2"></i>
                            <span><?php echo get_option('portfolio_phone', '+62 21 1234 5678'); ?></span>
                        </div>
                        <div class="flex items-center">
                            <i class="fas fa-envelope mr-2"></i>
                            <span><?php echo get_option('portfolio_email', 'info@yoursite.com'); ?></span>
                        </div>
                    </div>
                </div>
                
            </div>
            
            <div class="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
                <p>&copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. <?php _e('All rights reserved.', 'portfolio-collection'); ?></p>
            </div>
        </div>
    </footer>

</div><!-- #page -->

<?php wp_footer(); ?>

<script>
// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
});
</script>

</body>
</html>
EOF

    # Create inc/customizer.php
    mkdir -p "$theme_dir/inc"
    cat > "$theme_dir/inc/customizer.php" << 'EOF'
<?php
/**
 * Portfolio Collection Theme Customizer
 *
 * @package PortfolioCollection
 */

/**
 * Add postMessage support for site title and description for the Theme Customizer.
 */
function portfolio_customize_register($wp_customize) {
    $wp_customize->get_setting('blogname')->transport         = 'postMessage';
    $wp_customize->get_setting('blogdescription')->transport  = 'postMessage';
    $wp_customize->get_setting('header_textcolor')->transport = 'postMessage';

    // Add Portfolio Settings Panel
    $wp_customize->add_panel('portfolio_settings', array(
        'title'       => __('Portfolio Settings', 'portfolio-collection'),
        'description' => __('Customize your portfolio website settings', 'portfolio-collection'),
        'priority'    => 30,
    ));

    // Business Information Section
    $wp_customize->add_section('portfolio_business', array(
        'title'    => __('Business Information', 'portfolio-collection'),
        'panel'    => 'portfolio_settings',
        'priority' => 10,
    ));

    // Company Name
    $wp_customize->add_setting('portfolio_company_name', array(
        'default'           => '',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('portfolio_company_name', array(
        'label'    => __('Company Name', 'portfolio-collection'),
        'section'  => 'portfolio_business',
        'type'     => 'text',
    ));

    // Business Type
    $wp_customize->add_setting('portfolio_business_type', array(
        'default'           => 'healthcare',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('portfolio_business_type', array(
        'label'    => __('Business Type', 'portfolio-collection'),
        'section'  => 'portfolio_business',
        'type'     => 'select',
        'choices'  => array(
            'healthcare'   => __('Healthcare', 'portfolio-collection'),
            'automotive'   => __('Automotive', 'portfolio-collection'),
            'business'     => __('Business', 'portfolio-collection'),
            'digital'      => __('Digital Services', 'portfolio-collection'),
            'education'    => __('Education', 'portfolio-collection'),
            'professional' => __('Professional', 'portfolio-collection'),
        ),
    ));

    // Contact Information
    $wp_customize->add_setting('portfolio_phone', array(
        'default'           => '',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('portfolio_phone', array(
        'label'    => __('Phone Number', 'portfolio-collection'),
        'section'  => 'portfolio_business',
        'type'     => 'text',
    ));

    $wp_customize->add_setting('portfolio_email', array(
        'default'           => '',
        'sanitize_callback' => 'sanitize_email',
    ));

    $wp_customize->add_control('portfolio_email', array(
        'label'    => __('Email Address', 'portfolio-collection'),
        'section'  => 'portfolio_business',
        'type'     => 'email',
    ));

    $wp_customize->add_setting('portfolio_address', array(
        'default'           => '',
        'sanitize_callback' => 'sanitize_textarea_field',
    ));

    $wp_customize->add_control('portfolio_address', array(
        'label'    => __('Address', 'portfolio-collection'),
        'section'  => 'portfolio_business',
        'type'     => 'textarea',
    ));

    // Colors Section
    $wp_customize->add_section('portfolio_colors', array(
        'title'    => __('Colors', 'portfolio-collection'),
        'panel'    => 'portfolio_settings',
        'priority' => 20,
    ));

    // Primary Color
    $wp_customize->add_setting('portfolio_primary_color', array(
        'default'           => '#2563eb',
        'sanitize_callback' => 'sanitize_hex_color',
    ));

    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'portfolio_primary_color', array(
        'label'    => __('Primary Color', 'portfolio-collection'),
        'section'  => 'portfolio_colors',
        'settings' => 'portfolio_primary_color',
    )));

    // Secondary Color
    $wp_customize->add_setting('portfolio_secondary_color', array(
        'default'           => '#10b981',
        'sanitize_callback' => 'sanitize_hex_color',
    ));

    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'portfolio_secondary_color', array(
        'label'    => __('Secondary Color', 'portfolio-collection'),
        'section'  => 'portfolio_colors',
        'settings' => 'portfolio_secondary_color',
    )));
}
add_action('customize_register', 'portfolio_customize_register');

/**
 * Render the site title for the selective refresh partial.
 */
function portfolio_customize_partial_blogname() {
    bloginfo('name');
}

/**
 * Render the site tagline for the selective refresh partial.
 */
function portfolio_customize_partial_blogdescription() {
    bloginfo('description');
}

/**
 * Binds JS handlers to make Theme Customizer preview reload changes asynchronously.
 */
function portfolio_customize_preview_js() {
    wp_enqueue_script('portfolio-customizer', get_template_directory_uri() . '/assets/js/customizer.js', array('customize-preview'), PORTFOLIO_THEME_VERSION, true);
}
add_action('customize_preview_init', 'portfolio_customize_preview_js');
EOF

    # Create assets directory and main.js
    mkdir -p "$theme_dir/assets/js"
    cat > "$theme_dir/assets/js/main.js" << 'EOF'
/**
 * Portfolio Collection Theme Scripts
 */

(function($) {
    'use strict';

    // WordPress API integration
    const portfolioAPI = {
        init: function() {
            this.loadDynamicContent();
            this.setupMobileMenu();
            this.setupSmoothScroll();
            this.setupFormHandlers();
        },

        loadDynamicContent: function() {
            if (typeof portfolio_ajax !== 'undefined') {
                this.loadServices();
                this.loadTestimonials();
                this.loadPortfolio();
            }
        },

        loadServices: function() {
            const container = document.getElementById('services-container');
            if (!container) return;

            fetch(portfolio_ajax.api_url + 'services')
                .then(response => response.json())
                .then(services => {
                    if (services.length > 0) {
                        container.innerHTML = services.map(service => this.generateServiceHTML(service)).join('');
                    }
                })
                .catch(error => {
                    console.log('Using static content as fallback');
                });
        },

        loadTestimonials: function() {
            const container = document.getElementById('testimonials-container');
            if (!container) return;

            fetch(portfolio_ajax.api_url + 'testimonials')
                .then(response => response.json())
                .then(testimonials => {
                    if (testimonials.length > 0) {
                        container.innerHTML = testimonials.map(testimonial => this.generateTestimonialHTML(testimonial)).join('');
                    }
                })
                .catch(error => {
                    console.log('Using static content as fallback');
                });
        },

        loadPortfolio: function() {
            const container = document.getElementById('portfolio-container');
            if (!container) return;

            fetch(portfolio_ajax.api_url + 'portfolio')
                .then(response => response.json())
                .then(portfolio => {
                    if (portfolio.length > 0) {
                        container.innerHTML = portfolio.map(item => this.generatePortfolioHTML(item)).join('');
                    }
                })
                .catch(error => {
                    console.log('Using static content as fallback');
                });
        },

        generateServiceHTML: function(service) {
            const price = service.meta && service.meta._service_price ? service.meta._service_price[0] : '';
            const icon = service.meta && service.meta._service_icon ? service.meta._service_icon[0] : 'star';
            
            return `
                <div class="bg-gray-50 rounded-xl p-8 hover:shadow-lg transition-shadow">
                    <div class="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mb-6">
                        <i class="fas fa-${icon} text-2xl text-blue-600"></i>
                    </div>
                    <h3 class="text-xl font-semibold text-gray-800 mb-4">${service.title.rendered}</h3>
                    <div class="text-gray-600 mb-6">${service.excerpt.rendered}</div>
                    <div class="flex justify-between items-center">
                        ${price ? `<span class="text-blue-600 font-semibold">${price}</span>` : ''}
                        <a href="${service.link}" class="text-blue-600 hover:text-blue-700 font-semibold">
                            Selengkapnya <i class="fas fa-arrow-right ml-1"></i>
                        </a>
                    </div>
                </div>
            `;
        },

        generateTestimonialHTML: function(testimonial) {
            const rating = testimonial.meta && testimonial.meta._testimonial_rating ? parseInt(testimonial.meta._testimonial_rating[0]) : 5;
            const position = testimonial.meta && testimonial.meta._testimonial_position ? testimonial.meta._testimonial_position[0] : 'Client';
            
            return `
                <div class="bg-white rounded-xl p-8">
                    <div class="flex text-yellow-400 mb-4 text-lg">
                        ${'★'.repeat(rating)}
                    </div>
                    <p class="text-gray-600 mb-6 italic">"${testimonial.content.rendered}"</p>
                    <div class="flex items-center">
                        <div class="bg-blue-200 w-12 h-12 rounded-full flex items-center justify-center mr-4">
                            <i class="fas fa-user text-blue-600"></i>
                        </div>
                        <div>
                            <p class="font-semibold text-gray-800">${testimonial.title.rendered}</p>
                            <p class="text-sm text-gray-600">${position}</p>
                        </div>
                    </div>
                </div>
            `;
        },

        generatePortfolioHTML: function(item) {
            const category = item.meta && item.meta._portfolio_category ? item.meta._portfolio_category[0] : 'Portfolio';
            const location = item.meta && item.meta._portfolio_location ? item.meta._portfolio_location[0] : 'Indonesia';
            
            return `
                <div class="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow">
                    <div class="h-64 bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
                        ${item.featured_media ? 
                            `<img src="${item.featured_media}" alt="${item.title.rendered}" class="w-full h-full object-cover">` :
                            `<i class="fas fa-image text-6xl text-gray-400"></i>`
                        }
                    </div>
                    <div class="p-6">
                        <div class="flex justify-between items-start mb-2">
                            <h3 class="text-lg font-semibold text-gray-800">${item.title.rendered}</h3>
                            <span class="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-semibold">
                                ${category}
                            </span>
                        </div>
                        <p class="text-gray-600 text-sm mb-4">${item.excerpt.rendered}</p>
                        <div class="flex items-center justify-between">
                            <span class="text-xs text-gray-500">${location} • ${new Date(item.date).getFullYear()}</span>
                            <a href="${item.link}" class="text-blue-600 hover:text-blue-700 font-semibold text-sm">
                                Lihat Detail <i class="fas fa-arrow-right ml-1"></i>
                            </a>
                        </div>
                    </div>
                </div>
            `;
        },

        setupMobileMenu: function() {
            const mobileMenuButton = document.querySelector('.mobile-menu-button');
            const mobileMenu = document.querySelector('.mobile-menu');
            
            if (mobileMenuButton && mobileMenu) {
                mobileMenuButton.addEventListener('click', function() {
                    mobileMenu.classList.toggle('hidden');
                });
            }
        },

        setupSmoothScroll: function() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        },

        setupFormHandlers: function() {
            const forms = document.querySelectorAll('form.contact-form');
            forms.forEach(form => {
                form.addEventListener('submit', this.handleFormSubmit.bind(this));
            });
        },

        handleFormSubmit: function(e) {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            formData.append('action', 'portfolio_contact_form');
            formData.append('nonce', portfolio_ajax.nonce);

            fetch(portfolio_ajax.ajax_url, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.showAlert('success', 'Pesan berhasil dikirim! Kami akan menghubungi Anda segera.');
                    form.reset();
                } else {
                    this.showAlert('error', 'Terjadi kesalahan. Silakan coba lagi.');
                }
            })
            .catch(error => {
                this.showAlert('error', 'Koneksi bermasalah. Silakan coba lagi.');
            });
        },

        showAlert: function(type, message) {
            const alertDiv = document.createElement('div');
            const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
            const icon = type === 'success' ? 'check-circle' : 'exclamation-circle';
            
            alertDiv.className = `fixed top-4 right-4 ${bgColor} text-white p-4 rounded-lg shadow-lg z-50`;
            alertDiv.innerHTML = `
                <div class="flex items-center">
                    <i class="fas fa-${icon} mr-2"></i>
                    <span>${message}</span>
                </div>
            `;
            
            document.body.appendChild(alertDiv);
            
            setTimeout(() => {
                alertDiv.remove();
            }, 5000);
        }
    };

    // Initialize when DOM is ready
    $(document).ready(function() {
        portfolioAPI.init();
    });

})(jQuery);
EOF

    print_success "✅ WordPress theme structure created successfully!"
}

# Function to create WordPress deployment package
create_deployment_package() {
    print_header "Creating WordPress deployment package..."
    
    # Create WordPress theme
    create_wordpress_theme
    
    # Create plugin installer script
    cat > "wordpress-deploy/install-plugins.sh" << 'EOF'
#!/bin/bash

# WordPress Plugin Installation Script
echo "Installing required WordPress plugins..."

# Array of required plugins
plugins=(
    "advanced-custom-fields"
    "contact-form-7"
    "wordpress-seo"
    "wp-rest-api-controller"
    "custom-post-type-ui"
)

# Install and activate each plugin
for plugin in "${plugins[@]}"; do
    echo "Installing $plugin..."
    wp plugin install "$plugin" --activate --allow-root
done

echo "All plugins installed successfully!"
EOF
    
    chmod +x "wordpress-deploy/install-plugins.sh"
    
    # Create setup instructions
    cat > "wordpress-deploy/SETUP.md" << 'EOF'
# WordPress Portfolio Collection Setup Guide

## Quick Installation

### 1. Upload Theme
1. Upload the `portfolio-collection` folder to `wp-content/themes/`
2. Activate the theme in WordPress admin

### 2. Install Required Plugins
Run the installation script:
```bash
./install-plugins.sh
```

Or install manually:
- Advanced Custom Fields
- Contact Form 7
- Yoast SEO
- WP REST API Controller
- Custom Post Type UI

### 3. Configure Settings
1. Go to **Appearance > Customize > Portfolio Settings**
2. Set your business information:
   - Company Name
   - Business Type
   - Contact Information
   - Colors

### 4. Add Content
1. **Services**: Add your services with prices and icons
2. **Portfolio**: Showcase your work
3. **Testimonials**: Add client testimonials

### 5. Setup Menus
1. Go to **Appearance > Menus**
2. Create menus for:
   - Primary Menu
   - Footer Menu
   - Mobile Menu

### 6. Configure REST API
The theme automatically enables CORS and REST API endpoints:
- Services: `/wp-json/wp/v2/services`
- Portfolio: `/wp-json/wp/v2/portfolio`
- Testimonials: `/wp-json/wp/v2/testimonials`

## Frontend Integration

To integrate with static frontend websites, update the API URL in your JavaScript:

```javascript
const WP_API_URL = 'https://your-wordpress-site.com';
```

## Industry Templates

Use the built-in template selector in WordPress admin to apply industry-specific content:

1. **Healthcare**: Medical services, doctor profiles, patient testimonials
2. **Automotive**: Vehicle catalog, financing, service booking
3. **Business**: Products/services, customer reviews, contact forms
4. **Digital**: Service packages, portfolio, case studies
5. **Education**: Academic programs, faculty, student achievements
6. **Professional**: Professional services, expertise areas, client work

## Customization

### Colors
Customize colors in **Appearance > Customize > Portfolio Settings > Colors**

### Business Type
Select your industry in **Appearance > Customize > Portfolio Settings > Business Information**

### Templates
Apply industry templates in **Portfolio > Templates** in WordPress admin

## Support

For technical support and customization, refer to the main documentation or contact support.
EOF
    
    # Create SQL for demo content
    cat > "wordpress-deploy/demo-content.sql" << 'EOF'
-- Demo content for Portfolio Collection WordPress theme

-- Insert demo services
INSERT INTO wp_posts (post_title, post_content, post_excerpt, post_status, post_type, post_date) VALUES
('Konsultasi Umum', 'Pemeriksaan kesehatan umum dengan dokter berpengalaman untuk menjaga kesehatan Anda.', 'Pemeriksaan kesehatan umum dengan dokter berpengalaman', 'publish', 'services', NOW()),
('Kardiologi', 'Pemeriksaan dan pengobatan penyakit jantung dengan teknologi terdepan.', 'Pemeriksaan dan pengobatan penyakit jantung', 'publish', 'services', NOW()),
('Radiologi', 'Layanan rontgen dan imaging diagnostik dengan peralatan modern.', 'Layanan rontgen dan imaging diagnostik', 'publish', 'services', NOW());

-- Insert demo testimonials
INSERT INTO wp_posts (post_title, post_content, post_status, post_type, post_date) VALUES
('Sarah Putri', 'Pelayanan sangat profesional dan ramah. Dokternya berpengalaman dan fasilitas kliniknya modern.', 'publish', 'testimonials', NOW()),
('Ahmad Reza', 'Proses pemeriksaan cepat dan hasil diagnosanya akurat. Sangat puas dengan layanannya.', 'publish', 'testimonials', NOW()),
('Linda Sari', 'Tim medis yang kompeten dan fasilitas yang lengkap. Recommended untuk keluarga.', 'publish', 'testimonials', NOW());

-- Insert demo portfolio
INSERT INTO wp_posts (post_title, post_content, post_excerpt, post_status, post_type, post_date) VALUES
('Modern Healthcare Center', 'Desain klinik modern dengan fasilitas lengkap dan suasana yang nyaman untuk pasien.', 'Desain klinik modern dengan fasilitas lengkap', 'publish', 'portfolio', NOW()),
('Digital Health Platform', 'Platform kesehatan digital untuk konsultasi online dan manajemen rekam medis.', 'Platform kesehatan digital untuk konsultasi online', 'publish', 'portfolio', NOW());
EOF
    
    print_success "✅ WordPress deployment package created!"
}

# Function to deploy WordPress backend
deploy_wordpress() {
    print_header "🚀 Deploying WordPress backend..."
    
    read -p "Enter your hosting provider (hostinger/niagahoster/cpanel/other): " hosting
    read -p "Enter your domain name (e.g., api.yourdomain.com): " domain
    
    echo
    print_status "📝 Creating deployment package..."
    
    # Create WordPress deployment package
    create_deployment_package
    
    # Create hosting-specific instructions
    case $hosting in
        hostinger)
            create_hostinger_instructions "$domain"
            ;;
        niagahoster)
            create_niagahoster_instructions "$domain"
            ;;
        cpanel)
            create_cpanel_instructions "$domain"
            ;;
        *)
            create_generic_instructions "$domain"
            ;;
    esac
    
    print_success "✅ WordPress deployment package ready!"
    print_status "📁 Package location: ./wordpress-deploy/"
    print_status "🌐 Configure your domain: $domain"
    
    echo
    print_warning "Next steps:"
    echo "1. Upload wordpress-deploy contents to your hosting"
    echo "2. Install WordPress"
    echo "3. Upload and activate the Portfolio Collection theme"
    echo "4. Run the plugin installation script"
    echo "5. Configure theme settings"
    echo "6. Update frontend websites with API URL: https://$domain"
}

# Function to create hosting-specific instructions
create_hostinger_instructions() {
    local domain=$1
    cat > "wordpress-deploy/HOSTINGER_SETUP.md" << EOF
# Hostinger WordPress Setup

## 1. Install WordPress
1. Login to Hostinger control panel
2. Go to **Auto Installer > WordPress**
3. Select domain: $domain
4. Install WordPress

## 2. Upload Theme
1. Go to **File Manager**
2. Navigate to **public_html/wp-content/themes/**
3. Upload **portfolio-collection.zip**
4. Extract the theme

## 3. Activate Theme
1. Login to WordPress admin
2. Go to **Appearance > Themes**
3. Activate **Portfolio Collection**

## 4. Install Plugins
Use Hostinger's WordPress manager or install manually:
- Advanced Custom Fields
- Contact Form 7
- Yoast SEO

## 5. Configure SSL
1. Go to **SSL/TLS > SSL Certificates**
2. Enable SSL for $domain
3. Force HTTPS redirect

Your WordPress API will be available at:
**https://$domain/wp-json/wp/v2/**
EOF
}

create_niagahoster_instructions() {
    local domain=$1
    cat > "wordpress-deploy/NIAGAHOSTER_SETUP.md" << EOF
# Niagahoster WordPress Setup

## 1. Auto Install WordPress
1. Login to cPanel
2. Go to **Softaculous Apps Installer**
3. Select **WordPress**
4. Install on domain: $domain

## 2. Upload Theme via cPanel
1. Go to **File Manager**
2. Navigate to **public_html/wp-content/themes/**
3. Upload theme files
4. Extract if needed

## 3. Plugin Installation
1. Use WordPress admin dashboard
2. Go to **Plugins > Add New**
3. Install required plugins

## 4. Enable SSL
1. Go to **SSL/TLS**
2. Enable **Let's Encrypt SSL**
3. Force HTTPS in WordPress settings

Your API endpoint: **https://$domain/wp-json/wp/v2/**
EOF
}

create_cpanel_instructions() {
    local domain=$1
    cat > "wordpress-deploy/CPANEL_SETUP.md" << EOF
# cPanel WordPress Setup

## 1. WordPress Installation
1. Login to cPanel
2. Go to **WordPress Manager** or **Softaculous**
3. Install WordPress on $domain

## 2. File Upload
1. Use **File Manager** in cPanel
2. Upload theme to **wp-content/themes/**
3. Set proper permissions (755 for folders, 644 for files)

## 3. Database Setup
1. Import demo-content.sql if needed
2. Use **phpMyAdmin** in cPanel

## 4. DNS & SSL
1. Point domain to your hosting
2. Enable SSL certificate
3. Update WordPress URLs

API URL: **https://$domain/wp-json/wp/v2/**
EOF
}

create_generic_instructions() {
    local domain=$1
    cat > "wordpress-deploy/GENERIC_SETUP.md" << EOF
# Generic WordPress Setup

## 1. Server Requirements
- PHP 7.4+
- MySQL 5.7+
- Apache/Nginx
- SSL Certificate

## 2. WordPress Installation
1. Download WordPress from wordpress.org
2. Upload to your server
3. Create database
4. Run WordPress installation

## 3. Theme Setup
1. Upload portfolio-collection theme
2. Activate in WordPress admin
3. Install required plugins

## 4. Configuration
1. Enable pretty permalinks
2. Configure SSL
3. Set up CORS for API access

## 5. API Endpoints
Base URL: https://$domain/wp-json/wp/v2/
- Services: /services
- Portfolio: /portfolio
- Testimonials: /testimonials

## 6. Security
1. Use strong passwords
2. Install security plugin
3. Regular backups
4. Update WordPress regularly
EOF
}

# Function to deploy static frontend with WordPress integration
deploy_frontend() {
    print_header "🌐 Deploying static frontend to Vercel..."
    
    read -p "Enter WordPress API URL (e.g., https://api.yourdomain.com): " api_url
    
    print_status "📝 Updating API configuration in websites..."
    
    # Update API configuration in all websites
    find portfolio-websites -name "*.html" -type f -exec sed -i "s|https://your-wordpress-site.com|$api_url|g" {} \;
    
    # Add WordPress integration script to each website
    for website in portfolio-websites/*/; do
        if [ -d "$website" ]; then
            website_name=$(basename "$website")
            print_status "📦 Updating $website_name..."
            
            cd "$website"
            
            # Add WordPress integration script if not exists
            if ! grep -q "wordpress-api.js" index.html; then
                # Add WordPress API integration
                sed -i '/<\/body>/i\
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>\
<script>\
// WordPress API integration\
const WP_API_URL = '"'"''"$api_url"''"'"';\
\
async function loadWordPressContent() {\
    try {\
        const services = await axios.get(`${WP_API_URL}/wp-json/wp/v2/services`);\
        const testimonials = await axios.get(`${WP_API_URL}/wp-json/wp/v2/testimonials`);\
        \
        // Update content dynamically\
        updateServices(services.data);\
        updateTestimonials(testimonials.data);\
    } catch (error) {\
        console.log('"'"'Using static content as fallback'"'"');\
    }\
}\
\
function updateServices(services) {\
    const container = document.getElementById('"'"'services-container'"'"');\
    if (container && services.length > 0) {\
        // Update services section with WordPress data\
        container.innerHTML = services.map(service => {\
            const price = service.meta && service.meta._service_price ? service.meta._service_price[0] : '"'"''"'"';\
            const icon = service.meta && service.meta._service_icon ? service.meta._service_icon[0] : '"'"'star'"'"';\
            return `<div class="service-item"><h3>${service.title.rendered}</h3><p>${service.excerpt.rendered}</p></div>`;\
        }).join('"'"''"'"');\
    }\
}\
\
function updateTestimonials(testimonials) {\
    const container = document.getElementById('"'"'testimonials-container'"'"');\
    if (container && testimonials.length > 0) {\
        container.innerHTML = testimonials.map(testimonial => {\
            return `<div class="testimonial-item"><p>"${testimonial.content.rendered}"</p><cite>${testimonial.title.rendered}</cite></div>`;\
        }).join('"'"''"'"');\
    }\
}\
\
// Load content when page loads\
document.addEventListener('"'"'DOMContentLoaded'"'"', loadWordPressContent);\
</script>' index.html
            fi
            
            # Deploy to Vercel if vercel CLI is available
            if command -v vercel &> /dev/null; then
                print_status "🚀 Deploying $website_name to Vercel..."
                vercel --prod --yes
            else
                print_warning "⚠️  Vercel CLI not found. Skipping auto-deployment."
                print_status "📋 To deploy manually:"
                echo "   1. Install Vercel CLI: npm install -g vercel"
                echo "   2. Login: vercel login"
                echo "   3. Deploy: vercel --prod"
            fi
            
            cd - > /dev/null
        fi
    done
    
    print_success "✅ Frontend websites updated with WordPress integration!"
}

# Function to create content sync script
create_content_sync() {
    print_header "📄 Creating content sync automation..."
    
    mkdir -p scripts
    
    cat > "scripts/content-sync.js" << 'EOF'
#!/usr/bin/env node

/**
 * WordPress to Static Site Content Sync
 * Automatically sync content from WordPress to static websites
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

class ContentSync {
    constructor(wpApiUrl) {
        this.wpApiUrl = wpApiUrl.replace(/\/$/, ''); // Remove trailing slash
        this.apiBase = `${this.wpApiUrl}/wp-json/wp/v2`;
    }
    
    async syncAllContent() {
        console.log('🔄 Starting content sync from WordPress...');
        console.log(`📡 API URL: ${this.apiBase}`);
        
        try {
            // Fetch content from WordPress
            const [services, testimonials, portfolio] = await Promise.all([
                this.fetchServices(),
                this.fetchTestimonials(),
                this.fetchPortfolio()
            ]);
            
            console.log(`📊 Found: ${services.length} services, ${testimonials.length} testimonials, ${portfolio.length} portfolio items`);
            
            // Update each website
            const websites = [
                'portfolio-websites/healthcare/klinik-sehat',
                'portfolio-websites/automotive/dealer-mobil',
                'portfolio-websites/automotive/sepeda-listrik',
                'portfolio-websites/business/toko-online',
                'portfolio-websites/business/restoran-cafe',
                'portfolio-websites/digital/digital-marketing',
                'portfolio-websites/government/sekolah-digital',
                'portfolio-websites/professional/arsitek-interior'
            ];
            
            for (const website of websites) {
                if (fs.existsSync(website)) {
                    await this.updateWebsite(website, {
                        services,
                        testimonials, 
                        portfolio
                    });
                } else {
                    console.log(`⚠️  Website not found: ${website}`);
                }
            }
            
            console.log('✅ Content sync completed successfully!');
        } catch (error) {
            console.error('❌ Sync failed:', error.message);
            process.exit(1);
        }
    }
    
    async fetchServices() {
        try {
            const response = await axios.get(`${this.apiBase}/services`);
            return response.data;
        } catch (error) {
            console.error('Error fetching services:', error.message);
            return [];
        }
    }
    
    async fetchTestimonials() {
        try {
            const response = await axios.get(`${this.apiBase}/testimonials`);
            return response.data;
        } catch (error) {
            console.error('Error fetching testimonials:', error.message);
            return [];
        }
    }
    
    async fetchPortfolio() {
        try {
            const response = await axios.get(`${this.apiBase}/portfolio`);
            return response.data;
        } catch (error) {
            console.error('Error fetching portfolio:', error.message);
            return [];
        }
    }
    
    async updateWebsite(websitePath, content) {
        console.log(`📝 Updating ${websitePath}...`);
        
        const indexPath = path.join(websitePath, 'index.html');
        
        if (!fs.existsSync(indexPath)) {
            console.log(`⚠️  Index file not found: ${indexPath}`);
            return;
        }
        
        let html = fs.readFileSync(indexPath, 'utf8');
        
        // Update services section
        if (content.services.length > 0) {
            const servicesHtml = this.generateServicesHtml(content.services);
            html = this.replaceSection(html, 'SERVICES', servicesHtml);
        }
        
        // Update testimonials section
        if (content.testimonials.length > 0) {
            const testimonialsHtml = this.generateTestimonialsHtml(content.testimonials);
            html = this.replaceSection(html, 'TESTIMONIALS', testimonialsHtml);
        }
        
        // Update portfolio section
        if (content.portfolio.length > 0) {
            const portfolioHtml = this.generatePortfolioHtml(content.portfolio);
            html = this.replaceSection(html, 'PORTFOLIO', portfolioHtml);
        }
        
        // Write updated HTML
        fs.writeFileSync(indexPath, html);
        console.log(`✅ Updated ${websitePath}`);
    }
    
    replaceSection(html, sectionName, newContent) {
        const startComment = `<!-- ${sectionName}_START -->`;
        const endComment = `<!-- ${sectionName}_END -->`;
        
        const regex = new RegExp(`${startComment}[\\s\\S]*?${endComment}`, 'g');
        
        if (regex.test(html)) {
            return html.replace(regex, `${startComment}\n${newContent}\n${endComment}`);
        } else {
            console.log(`⚠️  Section markers not found for ${sectionName}`);
            return html;
        }
    }
    
    generateServicesHtml(services) {
        return services.map(service => {
            const price = service.meta?._service_price?.[0] || '';
            const icon = service.meta?._service_icon?.[0] || 'star';
            
            return `
                <div class="bg-gray-50 rounded-xl p-8 hover:shadow-lg transition-shadow">
                    <div class="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mb-6">
                        <i class="fas fa-${icon} text-2xl text-blue-600"></i>
                    </div>
                    <h3 class="text-xl font-semibold text-gray-800 mb-4">${service.title.rendered}</h3>
                    <div class="text-gray-600 mb-6">${service.excerpt.rendered}</div>
                    <div class="flex justify-between items-center">
                        ${price ? `<span class="text-blue-600 font-semibold">${price}</span>` : ''}
                        <a href="${service.link}" class="text-blue-600 hover:text-blue-700 font-semibold">
                            Selengkapnya <i class="fas fa-arrow-right ml-1"></i>
                        </a>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    generateTestimonialsHtml(testimonials) {
        return testimonials.map(testimonial => {
            const rating = testimonial.meta?._testimonial_rating?.[0] || 5;
            const position = testimonial.meta?._testimonial_position?.[0] || 'Client';
            
            return `
                <div class="bg-white rounded-xl p-8">
                    <div class="flex text-yellow-400 mb-4 text-lg">
                        ${'★'.repeat(parseInt(rating))}
                    </div>
                    <p class="text-gray-600 mb-6 italic">"${testimonial.content.rendered}"</p>
                    <div class="flex items-center">
                        <div class="bg-blue-200 w-12 h-12 rounded-full flex items-center justify-center mr-4">
                            <i class="fas fa-user text-blue-600"></i>
                        </div>
                        <div>
                            <p class="font-semibold text-gray-800">${testimonial.title.rendered}</p>
                            <p class="text-sm text-gray-600">${position}</p>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    generatePortfolioHtml(portfolio) {
        return portfolio.map(item => {
            const category = item.meta?._portfolio_category?.[0] || 'Portfolio';
            const location = item.meta?._portfolio_location?.[0] || 'Indonesia';
            
            return `
                <div class="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow">
                    <div class="h-64 bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
                        ${item.featured_media ? 
                            `<img src="${item.featured_media}" alt="${item.title.rendered}" class="w-full h-full object-cover">` :
                            `<i class="fas fa-image text-6xl text-gray-400"></i>`
                        }
                    </div>
                    <div class="p-6">
                        <div class="flex justify-between items-start mb-2">
                            <h3 class="text-lg font-semibold text-gray-800">${item.title.rendered}</h3>
                            <span class="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-semibold">
                                ${category}
                            </span>
                        </div>
                        <p class="text-gray-600 text-sm mb-4">${item.excerpt.rendered}</p>
                        <div class="flex items-center justify-between">
                            <span class="text-xs text-gray-500">${location} • ${new Date(item.date).getFullYear()}</span>
                            <a href="${item.link}" class="text-blue-600 hover:text-blue-700 font-semibold text-sm">
                                Lihat Detail <i class="fas fa-arrow-right ml-1"></i>
                            </a>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }
}

// CLI usage
if (require.main === module) {
    const args = process.argv.slice(2);
    const apiUrl = args[0];
    
    if (!apiUrl) {
        console.error('Usage: node content-sync.js <wordpress-api-url>');
        console.error('Example: node content-sync.js https://api.yourdomain.com');
        process.exit(1);
    }
    
    const contentSync = new ContentSync(apiUrl);
    contentSync.syncAllContent();
}

module.exports = ContentSync;
EOF
    
    chmod +x "scripts/content-sync.js"
    
    # Create package.json for content sync script
    cat > "scripts/package.json" << 'EOF'
{
  "name": "portfolio-content-sync",
  "version": "1.0.0",
  "description": "WordPress to static site content synchronization",
  "main": "content-sync.js",
  "bin": {
    "content-sync": "./content-sync.js"
  },
  "dependencies": {
    "axios": "^1.6.0"
  },
  "scripts": {
    "sync": "node content-sync.js"
  }
}
EOF
    
    print_success "✅ Content sync script created!"
    print_status "📄 Location: ./scripts/content-sync.js"
    print_status "🔧 Install dependencies: cd scripts && npm install"
}

# Main menu function
show_main_menu() {
    clear
    echo
    echo "🚀 WordPress + Portfolio Integration Deployment"
    echo "=============================================="
    echo
    echo "1. Deploy WordPress backend only"
    echo "2. Deploy static frontend only"
    echo "3. Deploy both (full integration)"
    echo "4. Create content sync automation"
    echo "5. Exit"
    echo
    read -p "Choose option (1-5): " choice
    
    case $choice in
        1)
            deploy_wordpress
            ;;
        2)
            deploy_frontend
            ;;
        3)
            deploy_wordpress
            echo
            deploy_frontend
            echo
            create_content_sync
            ;;
        4)
            create_content_sync
            ;;
        5)
            print_success "👋 Goodbye! Happy building!"
            exit 0
            ;;
        *)
            print_error "❌ Invalid option"
            show_main_menu
            ;;
    esac
}

# Main execution
main() {
    # Check if we're in the right directory
    if [[ ! -d "portfolio-websites" ]]; then
        print_error "❌ Script must be run from the project root directory!"
        print_error "   Make sure you're in the directory containing 'portfolio-websites' folder"
        exit 1
    fi
    
    print_status "🔍 Environment check passed"
    show_main_menu
}

# Run main function
main