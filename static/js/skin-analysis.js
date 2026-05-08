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
                        <img src="${e.target.result}" alt="Xem trước" class="preview-image me-3" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px;">
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
            console.log('Camera button clicked');
            try {
                await openCamera();
            } catch (error) {
                console.error('Camera access error:', error);
                let errorMessage = 'Không thể truy cập camera. ';
                
                if (error.name === 'NotAllowedError') {
                    errorMessage += 'Vui lòng cho phép truy cập camera trong trình duyệt.';
                } else if (error.name === 'NotFoundError') {
                    errorMessage += 'Không tìm thấy camera trên thiết bị.';
                } else if (error.name === 'NotSupportedError') {
                    errorMessage += 'Trình duyệt không hỗ trợ camera.';
                } else {
                    errorMessage += 'Vui lòng thử lại hoặc sử dụng tính năng tải ảnh lên.';
                }
                
                showError(errorMessage);
                
                // Close modal if it was opened
                const modal = bootstrap.Modal.getInstance(cameraModal);
                if (modal) {
                    modal.hide();
                }
            }
        });
    } else {
        console.log('Camera button not found');
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
            // Update status
            updateCameraStatus('Đang yêu cầu quyền truy cập camera...', 'warning');
            
            // Show modal first
            const modal = new bootstrap.Modal(cameraModal);
            modal.show();
            
            // Check if camera is available
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                throw new Error('Trình duyệt không hỗ trợ camera');
            }
            
            stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user'
                }
            });
            
            if (video) {
                video.srcObject = stream;
                await video.play();
                
                // Update status
                updateCameraStatus('Camera đã sẵn sàng!', 'success');
                
                // Reset UI
                resetCameraUI();
            }
        } catch (error) {
            updateCameraStatus('Lỗi: ' + error.message, 'danger');
            throw error;
        }
    }
    
    function updateCameraStatus(message, type) {
        const statusEl = document.getElementById('cameraStatus');
        if (statusEl) {
            statusEl.className = `badge bg-${type}`;
            statusEl.innerHTML = `<i class="fas fa-${type === 'success' ? 'check' : type === 'danger' ? 'times' : 'clock'} me-1"></i>${message}`;
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

// Test function for camera feature
function testCameraFeature() {
    console.log('Testing camera feature...');
    console.log('Looking for elements...');
    
    // Debug element search
    const allElements = document.querySelectorAll('*[id]');
    console.log('All elements with IDs:', Array.from(allElements).map(el => el.id));
    
    // Check if camera elements exist
    const cameraBtn = document.getElementById('cameraButton');
    const cameraModal = document.getElementById('cameraModal');
    
    console.log('Camera button:', cameraBtn);
    console.log('Camera modal:', cameraModal);
    
    if (cameraBtn && cameraModal) {
        console.log('Camera elements found, triggering camera...');
        showSuccess('Đang khởi động camera để test...');
        cameraBtn.click();
    } else {
        console.error('Camera elements not found');
        console.log('Available buttons:', document.querySelectorAll('button'));
        console.log('Available modals:', document.querySelectorAll('.modal'));
        showError('Không tìm thấy các thành phần camera. Đang kiểm tra lại...');
        
        // Try to create a simple camera interface
        createSimpleCameraInterface();
    }
}

function createSimpleCameraInterface() {
    // Create a basic camera modal if the original one is missing
    const existingModal = document.getElementById('cameraModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modalHTML = `
        <div class="modal fade" id="cameraModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Chụp ảnh khuôn mặt</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <div class="alert alert-info mb-3">
                            <strong>Hướng dẫn:</strong> Đặt khuôn mặt vào khung camera và nhấn chụp
                        </div>
                        <video id="cameraVideo" autoplay muted class="img-fluid rounded" style="max-width: 100%; height: 300px; background: #000;"></video>
                        <canvas id="cameraCanvas" style="display: none;"></canvas>
                        <img id="capturedImage" class="img-fluid rounded" style="max-width: 100%; height: 300px; display: none;">
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-success" id="captureBtn">Chụp ảnh</button>
                        <button type="button" class="btn btn-primary" id="useCapturedBtn" style="display: none;">Sử dụng ảnh</button>
                        <button type="button" class="btn btn-secondary" id="retakeBtn" style="display: none;">Chụp lại</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Re-setup camera functionality
    setupCameraCapture();
    
    // Try to open camera
    const modal = new bootstrap.Modal(document.getElementById('cameraModal'));
    modal.show();
}

// Visual Analysis Map Rendering
const initVisualMap = () => {
    // Only run on results page
    if (!document.getElementById('analyzedImage') || !document.getElementById('skinLabels')) return;
    
    const img = document.getElementById('analyzedImage');
    if (img) {
        if (img.complete) {
            renderVisualAnalysis();
        } else {
            img.addEventListener('load', renderVisualAnalysis);
        }
    }
};

window.addEventListener('load', initVisualMap);
// Also run it immediately just in case the load event already fired
initVisualMap();

window.addEventListener('resize', () => {
    if (document.getElementById('analyzedImage')?.complete) {
        renderVisualAnalysis();
    }
});

function renderVisualAnalysis() {
    try {
        const img = document.getElementById('analyzedImage');
        const svg = document.getElementById('analysisSvg');
        const markersContainer = document.getElementById('analysisMarkers');
        const labelsContainer = document.getElementById('skinLabels');
        const data = window.skinAnalysisData;

        if (!img || !svg || !data || !labelsContainer) {
            console.warn('Missing required elements for visual map rendering');
            return;
        }

        if (img.naturalWidth === 0) {
            console.warn('Image not fully loaded yet');
            return; // Wait for load event
        }

        // Clear previous elements
        svg.innerHTML = '';
        markersContainer.innerHTML = '';
        labelsContainer.innerHTML = '';

        const imgWidth = img.clientWidth;
        const imgHeight = img.clientHeight;
        const naturalWidth = img.naturalWidth;
        const naturalHeight = img.naturalHeight;

        const scaleX = imgWidth / naturalWidth;
        const scaleY = imgHeight / naturalHeight;

        const concerns = [
            { key: 'acne', label: 'Mụn trứng cá', icon: 'fa-certificate' },
            { key: 'forehead_wrinkle', label: 'Nếp nhăn trán', icon: 'fa-lines-leaning' },
            { key: 'eye_finelines', label: 'Vết chân chim', icon: 'fa-eye' },
            { key: 'dark_circle', label: 'Quầng thâm mắt', icon: 'fa-circle-dot' },
            { key: 'skin_spot', label: 'Đốm nâu/Nám', icon: 'fa-bullseye' },
            { key: 'blackhead', label: 'Mụn đầu đen', icon: 'fa-dot-circle' },
            { key: 'nasolabial_fold', label: 'Rãnh cười', icon: 'fa-smile' }
        ];

        let foundAny = false;

        concerns.forEach((item, index) => {
            try {
                const itemData = data[item.key];
                
                // Some fields are just objects with 'value', some are arrays of rectangles, 
                // and some (Face++ v1) are objects with 'count' or 'list'
                let hasIssue = false;
                if (itemData !== undefined && itemData !== null) {
                    if (typeof itemData === 'object') {
                        // Check for 'value' (confidence/score)
                        if (itemData.value !== undefined && itemData.value > 0) hasIssue = true;
                        // Check for 'count' (Face++ v1 common)
                        if (itemData.count !== undefined && itemData.count > 0) hasIssue = true;
                        // Check for specific lists (acne_list, spot_list, etc.)
                        for (let subKey in itemData) {
                            if (subKey.includes('_list') && Array.isArray(itemData[subKey]) && itemData[subKey].length > 0) {
                                hasIssue = true;
                                break;
                            }
                        }
                    } else if (Array.isArray(itemData) && itemData.length > 0) {
                        hasIssue = true;
                    }
                }

                if (hasIssue) {
                    foundAny = true;
                    
                    // Robust function to recursively find coordinate data in Face++ response
                    function findCoordinate(obj) {
                        if (!obj || typeof obj !== 'object') return null;
                        if ('top' in obj && 'left' in obj && 'width' in obj && 'height' in obj) return obj;
                        if (obj.rectangle) return obj.rectangle;
                        
                        for (let k in obj) {
                            if (typeof obj[k] === 'object') {
                                const res = findCoordinate(obj[k]);
                                if (res) return res;
                            }
                        }
                        return null;
                    }

                    // Determine coordinate
                    let x = null, y = null;
                    const rect = findCoordinate(itemData);
                    
                    if (rect) {
                        x = (rect.left + rect.width / 2) * scaleX;
                        y = (rect.top + rect.height / 2) * scaleY;
                    }
                    
                    // If no exact coordinate, default to a smart fallback location based on concern type
                    if (x === null || y === null || isNaN(x) || isNaN(y)) {
                        // Place them roughly where they usually appear
                        const defaultPositions = {
                            'acne': { x: 0.3, y: 0.6 },
                            'forehead_wrinkle': { x: 0.5, y: 0.2 },
                            'eye_finelines': { x: 0.2, y: 0.45 },
                            'dark_circle': { x: 0.35, y: 0.5 },
                            'skin_spot': { x: 0.25, y: 0.65 },
                            'blackhead': { x: 0.5, y: 0.65 },
                            'nasolabial_fold': { x: 0.35, y: 0.75 }
                        };
                        const pos = defaultPositions[item.key] || { x: 0.5, y: 0.5 };
                        x = imgWidth * pos.x + (Math.random() * 20 - 10);
                        y = imgHeight * pos.y + (Math.random() * 20 - 10);
                    }

                    // Create Marker
                    const marker = document.createElement('div');
                    marker.className = 'analysis-marker';
                    marker.style.left = `${x}px`;
                    marker.style.top = `${y}px`;
                    marker.id = `marker-${item.key}`;
                    markersContainer.appendChild(marker);

                    // Create Label
                    const labelItem = document.createElement('div');
                    labelItem.className = 'skin-label-item animate-fade-in-right';
                    labelItem.style.animationDelay = `${index * 0.1}s`;
                    labelItem.innerHTML = `
                        <div class="skin-label-icon"><i class="fas ${item.icon}"></i></div>
                        <div class="flex-grow-1">
                            <div class="fw-bold small">${item.label}</div>
                            <div class="text-muted" style="font-size: 0.7rem;">AI phát hiện</div>
                        </div>
                        <i class="fas fa-chevron-right text-muted small ms-2"></i>
                    `;
                    labelsContainer.appendChild(labelItem);

                    // Draw Line (Leader line)
                    const drawLine = () => {
                        const svgRect = svg.getBoundingClientRect();
                        const markerRect = marker.getBoundingClientRect();
                        const labelRect = labelItem.getBoundingClientRect();

                        // Fallback if elements not visible
                        if (svgRect.width === 0 || markerRect.width === 0 || labelRect.width === 0) return;

                        // Start from marker center
                        const startX = markerRect.left + markerRect.width / 2 - svgRect.left;
                        const startY = markerRect.top + markerRect.height / 2 - svgRect.top;

                        // End at label left edge
                        const endX = labelRect.left - svgRect.left - 5;
                        const endY = labelRect.top + labelRect.height / 2 - svgRect.top;

                        const line = document.createElementNS("http://www.w3.org/2000/svg", "path");
                        
                        // Elbow path to avoid covering the face: Diagonal out, then horizontal to text
                        const elbowX = endX - 30; // 30px before the label
                        line.setAttribute("d", `M ${startX} ${startY} L ${elbowX} ${endY} L ${endX} ${endY}`);
                        line.setAttribute("class", "leader-line");
                        svg.appendChild(line);
                    };

                    // Draw line after a tiny delay to ensure DOM is fully rendered
                    setTimeout(drawLine, 150);

                    // Hover effects
                    labelItem.addEventListener('mouseenter', () => {
                        labelItem.classList.add('active');
                        marker.style.transform = 'translate(-50%, -50%) scale(1.5)';
                        marker.style.background = 'rgba(216, 27, 96, 0.8)';
                        marker.style.zIndex = '30';
                    });

                    labelItem.addEventListener('mouseleave', () => {
                        labelItem.classList.remove('active');
                        marker.style.transform = 'translate(-50%, -50%) scale(1)';
                        marker.style.background = 'rgba(216, 27, 96, 0.4)';
                        marker.style.zIndex = '20';
                    });
                }
            } catch (itemError) {
                console.error(`Error processing skin concern ${item.key}:`, itemError);
            }
        });

        if (!foundAny) {
            labelsContainer.innerHTML = `
                <div class="text-center p-4">
                    <i class="fas fa-check-circle text-success fa-3x mb-3"></i>
                    <h5 class="fw-bold">Làn da khỏe mạnh!</h5>
                    <p class="text-muted">AI không phát hiện vấn đề nổi bật nào cần đánh dấu trên bề mặt da.</p>
                </div>
            `;
        }
    } catch (err) {
        console.error('Error rendering visual analysis:', err);
        const labelsContainer = document.getElementById('skinLabels');
        if (labelsContainer) {
            labelsContainer.innerHTML = `
                <div class="alert alert-warning m-3">
                    <i class="fas fa-exclamation-triangle me-2"></i>Không thể vẽ bản đồ chỉ dẫn do thiếu dữ liệu tọa độ từ AI.
                </div>
            `;
        }
    }
}
