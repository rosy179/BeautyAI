// Skin Analysis JavaScript Module

document.addEventListener('DOMContentLoaded', function() {
    initializeSkinAnalysis();
});

function initializeSkinAnalysis() {
    const form = document.getElementById('skinAnalysisForm');
    const fileInput = document.querySelector('input[type="file"]');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    if (form) {
        setupFileUpload(fileInput);
        setupFormSubmission(form, analyzeBtn);
        setupCameraCapture();
    }
    
    // Initialize result animations if on results page
    if (document.querySelector('.analysis-result')) {
        animateResults();
    }
}

function setupFileUpload(fileInput) {
    if (!fileInput) return;
    
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            if (validateImageFile(file)) {
                previewImage(file);
            }
        }
    });
    
    // Drag and drop functionality
    const fileInputContainer = fileInput.closest('.mb-4');
    if (fileInputContainer) {
        setupDragAndDrop(fileInputContainer, fileInput);
    }
}

function previewImage(file) {
    const preview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    
    if (preview && previewImg) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

function removePreview() {
    const preview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const fileInput = document.querySelector('input[type="file"]');
    
    if (preview) preview.style.display = 'none';
    if (previewImg) previewImg.src = '';
    if (fileInput) fileInput.value = '';
}

function validateImageFile(file) {
    const maxSize = 5 * 1024 * 1024; // 5MB
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    
    if (!allowedTypes.includes(file.type)) {
        showError('Vui lòng chọn file ảnh định dạng JPG, JPEG hoặc PNG.');
        return false;
    }
    
    if (file.size > maxSize) {
        showError('Kích thước file không được vượt quá 5MB.');
        return false;
    }
    
    return true;
}

function previewImage(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        // Remove existing preview
        const existingPreview = document.querySelector('.image-preview');
        if (existingPreview) {
            existingPreview.remove();
        }
        
        // Create new preview
        const preview = document.createElement('div');
        preview.className = 'image-preview mt-3';
        preview.innerHTML = `
            <div class="card">
                <div class="card-body p-2">
                    <div class="d-flex align-items-center">
                        <img src="${e.target.result}" alt="Preview" class="preview-image me-3" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px;">
                        <div class="flex-grow-1">
                            <h6 class="mb-1">${file.name}</h6>
                            <small class="text-muted">${formatFileSize(file.size)}</small>
                        </div>
                        <button type="button" class="btn btn-sm btn-outline-danger" onclick="removePreview()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        const fileInput = document.querySelector('input[type="file"]');
        fileInput.closest('.mb-4').appendChild(preview);
    };
    reader.readAsDataURL(file);
}

function removePreview() {
    const preview = document.querySelector('.image-preview');
    const fileInput = document.querySelector('input[type="file"]');
    
    if (preview) preview.remove();
    if (fileInput) fileInput.value = '';
}

function setupDragAndDrop(container, fileInput) {
    const dropZone = document.createElement('div');
    dropZone.className = 'drop-zone border-2 border-dashed rounded p-4 text-center mt-2';
    dropZone.innerHTML = `
        <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-2"></i>
        <p class="mb-0">Kéo thả ảnh vào đây hoặc <strong>click để chọn file</strong></p>
    `;
    
    container.appendChild(dropZone);
    
    // Click to open file dialog
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Drag and drop events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-primary', 'bg-light');
    });
    
    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-primary', 'bg-light');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-primary', 'bg-light');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });
}

function setupFormSubmission(form, analyzeBtn) {
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            return;
        }
        
        // Show loading state
        if (analyzeBtn) {
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                Đang phân tích...
            `;
        }
        
        // Simulate progress (since we can't track real upload progress easily)
        showAnalysisProgress();
    });
}

function validateForm() {
    const fileInput = document.querySelector('input[type="file"]');
    
    if (!fileInput || !fileInput.files.length) {
        showError('Vui lòng chọn ảnh để phân tích.');
        return false;
    }
    
    return validateImageFile(fileInput.files[0]);
}

function showAnalysisProgress() {
    // Create progress modal
    const progressModal = document.createElement('div');
    progressModal.className = 'modal fade';
    progressModal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-body text-center p-4">
                    <div class="mb-3">
                        <i class="fas fa-brain fa-3x text-primary mb-3"></i>
                        <h5>Đang phân tích làn da của bạn</h5>
                        <p class="text-muted">AI đang xử lý ảnh và đưa ra đánh giá...</p>
                    </div>
                    
                    <div class="progress mb-3">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" 
                             role="progressbar" style="width: 0%" id="analysisProgress"></div>
                    </div>
                    
                    <div class="analysis-steps">
                        <div class="step active" id="step1">
                            <i class="fas fa-upload me-2"></i>Tải ảnh lên
                        </div>
                        <div class="step" id="step2">
                            <i class="fas fa-eye me-2"></i>Phát hiện khuôn mặt
                        </div>
                        <div class="step" id="step3">
                            <i class="fas fa-search me-2"></i>Phân tích làn da
                        </div>
                        <div class="step" id="step4">
                            <i class="fas fa-lightbulb me-2"></i>Tạo lời khuyên
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(progressModal);
    
    // Show modal (using Bootstrap 5 syntax)
    const modal = new bootstrap.Modal(progressModal);
    modal.show();
    
    // Simulate progress
    let progress = 0;
    const progressBar = document.getElementById('analysisProgress');
    const steps = ['step1', 'step2', 'step3', 'step4'];
    let currentStep = 0;
    
    const interval = setInterval(() => {
        progress += Math.random() * 15 + 5;
        if (progress > 100) progress = 100;
        
        progressBar.style.width = progress + '%';
        
        // Update steps
        if (progress > (currentStep + 1) * 25 && currentStep < steps.length - 1) {
            document.getElementById(steps[currentStep]).classList.remove('active');
            document.getElementById(steps[currentStep]).classList.add('completed');
            currentStep++;
            document.getElementById(steps[currentStep]).classList.add('active');
        }
        
        if (progress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                modal.hide();
                progressModal.remove();
            }, 1000);
        }
    }, 200);
}

function animateResults() {
    // Animate result cards
    const resultCards = document.querySelectorAll('.result-card, .routine-card');
    resultCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 200);
    });
    
    // Animate recommended products
    const productCards = document.querySelectorAll('.card');
    productCards.forEach((card, index) => {
        if (card.closest('.recommended-products')) {
            card.style.opacity = '0';
            card.style.transform = 'scale(0.9)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'scale(1)';
            }, 1000 + (index * 100));
        }
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showError(message) {
    // Remove existing error alerts
    const existingAlert = document.querySelector('.alert-danger.analysis-error');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    // Create new error alert
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show analysis-error';
    alert.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of form
    const form = document.getElementById('skinAnalysisForm');
    if (form) {
        form.insertBefore(alert, form.firstChild);
    }
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alert && alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

function showSuccess(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show';
    alert.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const form = document.getElementById('skinAnalysisForm');
    if (form) {
        form.insertBefore(alert, form.firstChild);
    }
    
    setTimeout(() => {
        if (alert && alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

// Additional utility functions for skin analysis
function getSkinTypeAdvice(skinType) {
    const advice = {
        'oily': {
            tips: [
                'Sử dụng sữa rửa mặt chứa salicylic acid',
                'Tránh sản phẩm có dầu (oil-free)',
                'Sử dụng toner không chứa cồn',
                'Thoa kem chống nắng dạng gel'
            ],
            products: ['gel cleanser', 'BHA toner', 'oil-free moisturizer']
        },
        'dry': {
            tips: [
                'Sử dụng sữa rửa mặt dịu nhẹ',
                'Thoa serum hyaluronic acid',
                'Dùng kem dưỡng ẩm dày',
                'Tránh sản phẩm chứa cồn'
            ],
            products: ['cream cleanser', 'hyaluronic serum', 'rich moisturizer']
        },
        'combination': {
            tips: [
                'Sử dụng sản phẩm khác nhau cho từng vùng da',
                'Toner cân bằng độ pH',
                'Kem dưỡng ẩm nhẹ',
                'Chú ý đặc biệt vùng T'
            ],
            products: ['gentle cleanser', 'balancing toner', 'lightweight moisturizer']
        },
        'sensitive': {
            tips: [
                'Chọn sản phẩm không mùi, không màu',
                'Test patch trước khi sử dụng',
                'Tránh scrub thô',
                'Sử dụng kem chống nắng mineral'
            ],
            products: ['gentle cleanser', 'sensitive skin moisturizer', 'mineral sunscreen']
        }
    };
    
    return advice[skinType] || advice['normal'];
}

// Camera capture functionality
function setupCameraCapture() {
    const cameraBtn = document.getElementById('cameraBtn');
    const cameraModal = document.getElementById('cameraModal');
    const video = document.getElementById('cameraVideo');
    const canvas = document.getElementById('cameraCanvas');
    const captureBtn = document.getElementById('captureBtn');
    const useCapturedBtn = document.getElementById('useCapturedBtn');
    const retakeBtn = document.getElementById('retakeBtn');
    const fileInput = document.querySelector('input[type="file"]');
    
    let stream = null;
    let capturedImageBlob = null;
    
    if (cameraBtn) {
        cameraBtn.addEventListener('click', async function() {
            try {
                await openCamera();
            } catch (error) {
                showError('Không thể truy cập camera. Vui lòng kiểm tra quyền truy cập camera.');
                console.error('Camera access error:', error);
            }
        });
    }
    
    if (captureBtn) {
        captureBtn.addEventListener('click', function() {
            capturePhoto();
        });
    }
    
    if (useCapturedBtn) {
        useCapturedBtn.addEventListener('click', function() {
            useCapturedPhoto();
        });
    }
    
    if (retakeBtn) {
        retakeBtn.addEventListener('click', function() {
            retakePhoto();
        });
    }
    
    // Close camera when modal is hidden
    if (cameraModal) {
        cameraModal.addEventListener('hidden.bs.modal', function() {
            stopCamera();
        });
    }
    
    async function openCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user'
                }
            });
            
            if (video) {
                video.srcObject = stream;
                video.play();
                
                // Show modal
                const modal = new bootstrap.Modal(cameraModal);
                modal.show();
                
                // Reset UI
                resetCameraUI();
            }
        } catch (error) {
            throw error;
        }
    }
    
    function capturePhoto() {
        if (!video || !canvas) return;
        
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw video frame to canvas
        context.drawImage(video, 0, 0);
        
        // Convert canvas to blob
        canvas.toBlob(function(blob) {
            capturedImageBlob = blob;
            
            // Show captured image
            const capturedImage = document.getElementById('capturedImage');
            if (capturedImage) {
                capturedImage.src = canvas.toDataURL();
                capturedImage.style.display = 'block';
            }
            
            // Hide video, show captured controls
            video.style.display = 'none';
            captureBtn.style.display = 'none';
            useCapturedBtn.style.display = 'inline-block';
            retakeBtn.style.display = 'inline-block';
            
        }, 'image/jpeg', 0.9);
    }
    
    function useCapturedPhoto() {
        if (!capturedImageBlob || !fileInput) return;
        
        // Create file from blob
        const file = new File([capturedImageBlob], 'camera-capture.jpg', {
            type: 'image/jpeg'
        });
        
        // Create FileList object
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
        
        // Trigger change event
        const changeEvent = new Event('change', { bubbles: true });
        fileInput.dispatchEvent(changeEvent);
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(cameraModal);
        modal.hide();
        
        showSuccess('Ảnh đã được chụp và sẵn sàng để phân tích!');
    }
    
    function retakePhoto() {
        resetCameraUI();
        capturedImageBlob = null;
    }
    
    function resetCameraUI() {
        if (video) video.style.display = 'block';
        if (captureBtn) captureBtn.style.display = 'inline-block';
        if (useCapturedBtn) useCapturedBtn.style.display = 'none';
        if (retakeBtn) retakeBtn.style.display = 'none';
        
        const capturedImage = document.getElementById('capturedImage');
        if (capturedImage) {
            capturedImage.style.display = 'none';
        }
    }
    
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
        
        if (video) {
            video.srcObject = null;
        }
        
        resetCameraUI();
        capturedImageBlob = null;
    }
}

// Export functions for use in other modules
window.SkinAnalysis = {
    validateImageFile,
    previewImage,
    removePreview,
    showError,
    showSuccess,
    getSkinTypeAdvice,
    setupCameraCapture
};
