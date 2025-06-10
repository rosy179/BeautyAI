// Chat System JavaScript Module

class BeautyChat {
    constructor() {
        this.chatContainer = document.getElementById('chatMessages');
        this.messageForm = document.getElementById('chatForm');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.isTyping = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupAutoScroll();
        this.setupTypingIndicator();
        this.loadChatHistory();
    }
    
    setupEventListeners() {
        if (this.messageForm) {
            this.messageForm.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }
        
        if (this.messageInput) {
            this.messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.messageForm.dispatchEvent(new Event('submit'));
                }
            });
            
            // Auto-resize textarea
            this.messageInput.addEventListener('input', () => {
                this.autoResizeTextarea();
            });
        }
        
        // Quick question buttons
        document.querySelectorAll('.btn[onclick*="insertQuickQuestion"]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const question = btn.textContent.trim();
                this.insertQuestion(question);
            });
        });
    }
    
    setupAutoScroll() {
        if (this.chatContainer) {
            // Scroll to bottom on page load
            this.scrollToBottom();
            
            // Watch for new messages and auto-scroll
            const observer = new MutationObserver(() => {
                this.scrollToBottom();
            });
            
            observer.observe(this.chatContainer, {
                childList: true,
                subtree: true
            });
        }
    }
    
    setupTypingIndicator() {
        if (this.messageInput) {
            let typingTimer;
            
            this.messageInput.addEventListener('input', () => {
                if (!this.isTyping) {
                    this.showTypingIndicator();
                }
                
                clearTimeout(typingTimer);
                typingTimer = setTimeout(() => {
                    this.hideTypingIndicator();
                }, 1000);
            });
        }
    }
    
    handleFormSubmit(e) {
        const message = this.messageInput.value.trim();
        
        if (!message) {
            e.preventDefault();
            return;
        }
        
        // Show user message immediately
        this.addMessageToChat(message, true);
        
        // Show loading state
        this.setLoadingState(true);
        
        // Clear input
        this.messageInput.value = '';
        this.autoResizeTextarea();
        
        // The form will submit normally, but we enhance the UX
    }
    
    addMessageToChat(message, isFromUser = false) {
        if (!this.chatContainer) return;
        
        const messageWrapper = document.createElement('div');
        messageWrapper.className = `message-wrapper p-3 ${isFromUser ? 'border-bottom' : 'bg-light border-bottom'}`;
        
        const messageHtml = isFromUser ? 
            this.createUserMessageHtml(message) : 
            this.createBotMessageHtml(message);
        
        messageWrapper.innerHTML = messageHtml;
        this.chatContainer.appendChild(messageWrapper);
        
        // Animate new message
        this.animateMessage(messageWrapper);
        
        this.scrollToBottom();
    }
    
    createUserMessageHtml(message) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('vi-VN', { 
            hour: '2-digit', 
            minute: '2-digit' 
        }) + ' - ' + now.toLocaleDateString('vi-VN');
        
        return `
            <div class="d-flex justify-content-end">
                <div class="message-content" style="max-width: 80%;">
                    <div class="d-flex align-items-start justify-content-end">
                        <div class="message-bubble bg-primary text-white rounded p-3 me-2">
                            <div class="message-text">${this.formatMessage(message)}</div>
                            <small class="text-light opacity-75">${timeString}</small>
                        </div>
                        <div class="avatar">
                            <i class="fas fa-user text-primary"></i>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    createBotMessageHtml(message) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('vi-VN', { 
            hour: '2-digit', 
            minute: '2-digit' 
        }) + ' - ' + now.toLocaleDateString('vi-VN');
        
        return `
            <div class="d-flex">
                <div class="message-content" style="max-width: 80%;">
                    <div class="d-flex align-items-start">
                        <div class="avatar me-2">
                            <i class="fas fa-robot text-info"></i>
                        </div>
                        <div class="message-bubble bg-light rounded p-3">
                            <div class="message-text">${this.formatMessage(message)}</div>
                            <small class="text-muted">${timeString}</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    formatMessage(message) {
        // Convert line breaks to <br> tags
        message = message.replace(/\n/g, '<br>');
        
        // Make URLs clickable
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        message = message.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener">$1</a>');
        
        // Make email addresses clickable
        const emailRegex = /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/g;
        message = message.replace(emailRegex, '<a href="mailto:$1">$1</a>');
        
        return message;
    }
    
    animateMessage(messageElement) {
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translateY(20px)';
        
        requestAnimationFrame(() => {
            messageElement.style.transition = 'all 0.3s ease';
            messageElement.style.opacity = '1';
            messageElement.style.transform = 'translateY(0)';
        });
    }
    
    scrollToBottom() {
        if (this.chatContainer) {
            this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
        }
    }
    
    autoResizeTextarea() {
        if (this.messageInput) {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
        }
    }
    
    insertQuestion(question) {
        if (this.messageInput) {
            this.messageInput.value = question;
            this.messageInput.focus();
            this.autoResizeTextarea();
        }
    }
    
    setLoadingState(isLoading) {
        if (this.sendButton) {
            this.sendButton.disabled = isLoading;
            
            if (isLoading) {
                this.sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                this.showTypingIndicator();
            } else {
                this.sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
                this.hideTypingIndicator();
            }
        }
    }
    
    showTypingIndicator() {
        if (this.isTyping) return;
        
        this.isTyping = true;
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator message-wrapper p-3 bg-light border-bottom';
        typingIndicator.innerHTML = `
            <div class="d-flex">
                <div class="message-content" style="max-width: 80%;">
                    <div class="d-flex align-items-start">
                        <div class="avatar me-2">
                            <i class="fas fa-robot text-info"></i>
                        </div>
                        <div class="message-bubble bg-light rounded p-3">
                            <div class="typing-dots">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        if (this.chatContainer) {
            this.chatContainer.appendChild(typingIndicator);
            this.scrollToBottom();
        }
    }
    
    hideTypingIndicator() {
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        this.isTyping = false;
    }
    
    loadChatHistory() {
        // If there are existing messages, animate them on load
        const existingMessages = document.querySelectorAll('.message-wrapper');
        existingMessages.forEach((message, index) => {
            setTimeout(() => {
                this.animateMessage(message);
            }, index * 100);
        });
    }
    
    // Advanced features
    addQuickReply(replies) {
        const quickReplyContainer = document.createElement('div');
        quickReplyContainer.className = 'quick-replies p-3 border-top';
        
        const repliesHtml = replies.map(reply => 
            `<button class="btn btn-sm btn-outline-primary me-2 mb-2 quick-reply-btn" data-reply="${reply}">
                ${reply}
            </button>`
        ).join('');
        
        quickReplyContainer.innerHTML = `
            <small class="text-muted mb-2 d-block">
                <i class="fas fa-lightbulb me-1"></i>Gợi ý câu trả lời:
            </small>
            ${repliesHtml}
        `;
        
        // Add event listeners to quick reply buttons
        quickReplyContainer.querySelectorAll('.quick-reply-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.insertQuestion(btn.dataset.reply);
                quickReplyContainer.remove();
            });
        });
        
        if (this.chatContainer) {
            this.chatContainer.appendChild(quickReplyContainer);
            this.scrollToBottom();
        }
    }
    
    // Beauty-specific chat features
    suggestProducts(skinType, concern) {
        const suggestions = this.getProductSuggestions(skinType, concern);
        
        const suggestionHtml = `
            <div class="product-suggestions">
                <h6><i class="fas fa-shopping-bag me-2"></i>Sản phẩm gợi ý:</h6>
                <div class="row g-2">
                    ${suggestions.map(product => `
                        <div class="col-6">
                            <div class="card card-sm">
                                <div class="card-body p-2">
                                    <h6 class="card-title small">${product.name}</h6>
                                    <p class="card-text small text-muted">${product.description}</p>
                                    <a href="#" class="btn btn-sm btn-primary">Xem chi tiết</a>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        return suggestionHtml;
    }
    
    getProductSuggestions(skinType, concern) {
        // This would normally come from an API
        const suggestions = {
            'oily': [
                { name: 'Sữa rửa mặt BHA', description: 'Kiểm soát dầu, ngăn ngừa mụn' },
                { name: 'Toner cân bằng', description: 'Thu nhỏ lỗ chân lông' }
            ],
            'dry': [
                { name: 'Serum HA', description: 'Cấp ẩm sâu 24h' },
                { name: 'Kem dưỡng ban đêm', description: 'Phục hồi da qua đêm' }
            ]
        };
        
        return suggestions[skinType] || [];
    }
}

// CSS for typing indicator animation
const typingStyles = `
    <style>
    .typing-dots {
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #007bff;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% {
            transform: scale(0.8);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    .quick-replies {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    .quick-reply-btn {
        transition: all 0.2s ease;
    }
    
    .quick-reply-btn:hover {
        transform: translateY(-1px);
    }
    </style>
`;

// Add styles to head
document.head.insertAdjacentHTML('beforeend', typingStyles);

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.beautyChat = new BeautyChat();
});

// Global function for quick questions (backward compatibility)
function insertQuickQuestion(question) {
    if (window.beautyChat) {
        window.beautyChat.insertQuestion(question);
    }
}

// Export for use in other modules
window.BeautyChat = BeautyChat;
