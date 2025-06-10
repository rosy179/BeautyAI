// Beauty App Main JavaScript Module
// Handles global functionality and interactions

// Utility functions defined first
function createToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${getToastIcon(type)} me-2"></i>
            <span>${message}</span>
        </div>
        <button type="button" class="toast-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    return toast;
}

function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-triangle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Define showToast globally before DOM loads
window.showToast = function(message, type = 'info') {
    const toast = createToast(message, type);
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // Auto-dismiss
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, 4000);
};

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize all modules
    initializeNavigation();
    initializeAnimations();
    initializeFormEnhancements();
    initializeImageHandling();
    initializeNotifications();
    initializeProductInteractions();
    initializeSearchFunctionality();
    initializeThemeToggle();
    
    // Initialize tooltips and popovers
    initializeBootstrapComponents();
}

// Navigation enhancements
function initializeNavigation() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Add active state to current page
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Navbar scroll effect
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
    
    // Mobile menu enhancements
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            this.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on a link
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 992) {
                    navbarCollapse.classList.remove('show');
                    navbarToggler.classList.remove('active');
                }
            });
        });
    }
}

// Animation effects
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    const animateElements = document.querySelectorAll('.card, .feature-icon, .step-card, .product-card');
    animateElements.forEach(el => {
        el.classList.add('animate-on-scroll');
        observer.observe(el);
    });
    
    // Add CSS for animations
    addAnimationStyles();
    
    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }
}

// Form enhancements
function initializeFormEnhancements() {
    // Enhanced form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            form.classList.add('was-validated');
        });
    });
    
    // Real-time validation for email fields
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateEmail(this);
        });
    });
    
    // Auto-format phone numbers
    const phoneInputs = document.querySelectorAll('input[type="tel"], input[name*="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            formatPhoneNumber(this);
        });
    });
    
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            autoResizeTextarea(this);
        });
        
        // Initial resize
        autoResizeTextarea(textarea);
    });
}

// Image handling and optimization
function initializeImageHandling() {
    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Image error handling
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', function() {
            this.src = '/static/images/placeholder.png';
            this.alt = 'Ảnh không tải được';
        });
    });
    
    // Image modal for product gallery
    const productImages = document.querySelectorAll('.product-image img');
    productImages.forEach(img => {
        img.addEventListener('click', function() {
            showImageModal(this.src, this.alt);
        });
    });
}

// Notification system
function initializeNotifications() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.classList.add('fade');
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 150);
            }
        }, 5000);
    });
    
    // Toast notifications are now handled by global showToast function
}

// Product interactions
function initializeProductInteractions() {
    // Product card hover effects
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
    
    // Quantity controls
    const quantityControls = document.querySelectorAll('.quantity-controls');
    quantityControls.forEach(control => {
        const minusBtn = control.querySelector('.btn:first-child');
        const plusBtn = control.querySelector('.btn:last-child');
        const input = control.querySelector('input');
        
        if (minusBtn && plusBtn && input) {
            minusBtn.addEventListener('click', function() {
                let value = parseInt(input.value) || 1;
                if (value > 1) {
                    input.value = value - 1;
                    input.dispatchEvent(new Event('change'));
                }
            });
            
            plusBtn.addEventListener('click', function() {
                let value = parseInt(input.value) || 1;
                const max = parseInt(input.getAttribute('max')) || 999;
                if (value < max) {
                    input.value = value + 1;
                    input.dispatchEvent(new Event('change'));
                }
            });
        }
    });
    
    // Wishlist functionality
    const wishlistBtns = document.querySelectorAll('.btn-wishlist');
    wishlistBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            this.classList.toggle('active');
            const icon = this.querySelector('i');
            if (icon) {
                icon.classList.toggle('fas');
                icon.classList.toggle('far');
            }
            
            const message = this.classList.contains('active') ? 
                'Đã thêm vào wishlist' : 'Đã xóa khỏi wishlist';
            showToast(message, 'success');
        });
    });
}

// Search functionality
function initializeSearchFunctionality() {
    const searchForms = document.querySelectorAll('form[role="search"], .search-form');
    searchForms.forEach(form => {
        const input = form.querySelector('input[type="search"], input[name="search"]');
        
        if (input) {
            // Live search suggestions
            let searchTimeout;
            input.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                const query = this.value.trim();
                
                if (query.length > 2) {
                    searchTimeout = setTimeout(() => {
                        // showSearchSuggestions(query, this);
                    }, 300);
                } else {
                    hideSearchSuggestions();
                }
            });
            
            // Clear search
            input.addEventListener('focus', function() {
                if (this.value) {
                    showClearButton(this);
                }
            });
        }
    });
}

// Theme toggle (if needed)
function initializeThemeToggle() {
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Update icon
            const icon = this.querySelector('i');
            if (icon) {
                icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        });
        
        // Load saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-bs-theme', savedTheme);
        }
    }
}

// Bootstrap components initialization
function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Initialize modals
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const autofocus = this.querySelector('[autofocus]');
            if (autofocus) {
                autofocus.focus();
            }
        });
    });
}

// Utility functions
function validateEmail(input) {
    const email = input.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        input.setCustomValidity('Vui lòng nhập email hợp lệ');
        input.classList.add('is-invalid');
    } else {
        input.setCustomValidity('');
        input.classList.remove('is-invalid');
        if (email) {
            input.classList.add('is-valid');
        }
    }
}

function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    
    if (value.startsWith('84')) {
        value = '+84 ' + value.substring(2);
    } else if (value.startsWith('0')) {
        value = '+84 ' + value.substring(1);
    } else if (value.length > 0) {
        value = '+84 ' + value;
    }
    
    input.value = value;
}

function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
}

function showImageModal(src, alt) {
    const modal = document.createElement('div');
    modal.className = 'modal fade image-modal';
    modal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${alt}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <img src="${src}" alt="${alt}" class="img-fluid">
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    modal.addEventListener('hidden.bs.modal', function() {
        modal.remove();
    });
}

function addAnimationStyles() {
    if (document.getElementById('main-animations')) return;
    
    const styles = document.createElement('style');
    styles.id = 'main-animations';
    styles.textContent = `
        .animate-on-scroll {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s ease;
        }
        
        .animate-on-scroll.animate-in {
            opacity: 1;
            transform: translateY(0);
        }
        
        .navbar-scrolled {
            background-color: rgba(0, 0, 0, 0.95) !important;
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .toast-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            display: flex;
            align-items: center;
            padding: 12px 16px;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        }
        
        .toast-notification.show {
            transform: translateX(0);
        }
        
        .toast-success {
            border-left: 4px solid #28a745;
        }
        
        .toast-error {
            border-left: 4px solid #dc3545;
        }
        
        .toast-warning {
            border-left: 4px solid #ffc107;
        }
        
        .toast-info {
            border-left: 4px solid #17a2b8;
        }
        
        .toast-content {
            flex-grow: 1;
            display: flex;
            align-items: center;
        }
        
        .toast-close {
            background: none;
            border: none;
            color: #6c757d;
            cursor: pointer;
            padding: 0;
            margin-left: 12px;
        }
        
        .toast-close:hover {
            color: #000;
        }
        
        @media (max-width: 768px) {
            .toast-notification {
                right: 10px;
                left: 10px;
                min-width: auto;
            }
        }
    `;
    
    document.head.appendChild(styles);
}

// Shopping cart functionality
function updateCartCount() {
    const cartBadge = document.querySelector('.badge');
    if (cartBadge) {
        // This would be updated via AJAX in a real implementation
        const count = parseInt(cartBadge.textContent) || 0;
        cartBadge.textContent = count;
        
        if (count > 0) {
            cartBadge.style.display = 'inline';
        } else {
            cartBadge.style.display = 'none';
        }
    }
}

// Page-specific initializations
function initializePageSpecific() {
    const pathname = window.location.pathname;
    
    if (pathname.includes('/products/')) {
        initializeProductDetail();
    } else if (pathname.includes('/cart')) {
        initializeCart();
    } else if (pathname.includes('/checkout')) {
        initializeCheckout();
    } else if (pathname === '/') {
        initializeHomePage();
    }
}

function initializeProductDetail() {
    // Product image gallery
    const productImages = document.querySelectorAll('.product-image img');
    productImages.forEach(img => {
        img.style.cursor = 'zoom-in';
    });
    
    // Review form enhancements
    const reviewForm = document.querySelector('#reviewForm');
    if (reviewForm) {
        const ratingInputs = reviewForm.querySelectorAll('input[type="radio"]');
        ratingInputs.forEach(input => {
            input.addEventListener('change', function() {
                updateStarDisplay(this.value);
            });
        });
    }
}

function initializeCart() {
    // Cart item updates would be handled here
    const removeButtons = document.querySelectorAll('.btn-remove-item');
    removeButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const item = this.closest('.cart-item');
            if (item && confirm('Bạn có chắc chắn muốn xóa sản phẩm này?')) {
                item.style.opacity = '0.5';
                // AJAX call would happen here
                showToast('Sản phẩm đã được xóa khỏi giỏ hàng', 'success');
            }
        });
    });
}

function initializeCheckout() {
    // Payment method selection
    const paymentInputs = document.querySelectorAll('input[name="payment_method"]');
    paymentInputs.forEach(input => {
        input.addEventListener('change', function() {
            updatePaymentInfo(this.value);
        });
    });
}

function initializeHomePage() {
    // Hero section animations
    const heroButtons = document.querySelectorAll('.hero-section .btn');
    heroButtons.forEach((btn, index) => {
        btn.style.animationDelay = `${index * 0.2}s`;
        btn.classList.add('animate-fade-in-up');
    });
}

function updateStarDisplay(rating) {
    const stars = document.querySelectorAll('.rating-display .fa-star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove('far');
            star.classList.add('fas');
        } else {
            star.classList.remove('fas');
            star.classList.add('far');
        }
    });
}

function updatePaymentInfo(method) {
    const paymentInfo = document.querySelector('.payment-info');
    if (paymentInfo) {
        let info = '';
        switch (method) {
            case 'cod':
                info = 'Thanh toán khi nhận hàng. Phí COD: 15,000đ';
                break;
            case 'bank_transfer':
                info = 'Chuyển khoản qua ngân hàng. Sẽ gửi thông tin tài khoản sau khi đặt hàng.';
                break;
            case 'momo':
                info = 'Thanh toán qua ví điện tử MoMo';
                break;
            case 'zalopay':
                info = 'Thanh toán qua ZaloPay';
                break;
        }
        paymentInfo.textContent = info;
    }
}

// Initialize page-specific functionality after DOM load
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initializePageSpecific, 100);
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    // Could send error reports to a logging service
});

// Service Worker registration (for PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // navigator.serviceWorker.register('/sw.js'); // Uncomment when SW is available
    });
}

// Export utilities for other modules
window.BeautyApp = {
    showToast,
    validateEmail,
    formatPhoneNumber,
    updateCartCount,
    showImageModal
};
