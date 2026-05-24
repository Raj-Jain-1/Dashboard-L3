document.addEventListener('DOMContentLoaded', () => {

    // System Clock
    function updateClock() {
        const clockEl = document.getElementById('systemClock');
        if (clockEl) {
            const now = new Date();
            clockEl.textContent = now.toLocaleTimeString('en-US', { hour12: false });
        }
    }
    setInterval(updateClock, 1000);
    updateClock();

    // Sidebar Toggle
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
        });
    }

    // --- AI Chatbot Widget Logic ---
    const aiToggle = document.getElementById('aiToggle');
    const chatWindow = document.getElementById('chatWindow');
    const closeChat = document.getElementById('closeChat');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendMessage');
    const chatBody = document.getElementById('chatBody');

    if (!aiToggle || !chatWindow) {
        console.warn('NeuroMed AI: Chatbot elements not found in DOM.');
        return;
    }

    // Toggle chat window open/close
    aiToggle.addEventListener('click', () => {
        chatWindow.classList.toggle('active');
        if (chatWindow.classList.contains('active')) {
            chatInput.focus();
        }
    });

    closeChat.addEventListener('click', () => {
        chatWindow.classList.remove('active');
    });

    // Helper: add a message bubble to the chat
    const addMessage = (text, type) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${type}`;
        msgDiv.innerHTML = type === 'ai-message'
            ? `<strong>Sys:</strong> ${text}`
            : `<strong>You:</strong> ${text}`;
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
        return msgDiv;
    };

    // Helper: show a temporary typing indicator
    const showTyping = () => {
        const typingEl = document.createElement('div');
        typingEl.className = 'message ai-message';
        typingEl.id = 'typingIndicator';
        typingEl.innerHTML = `<strong>Sys:</strong> <em style="color:var(--text-muted);">Processing query...</em>`;
        chatBody.appendChild(typingEl);
        chatBody.scrollTop = chatBody.scrollHeight;
    };

    const removeTyping = () => {
        const typingEl = document.getElementById('typingIndicator');
        if (typingEl) typingEl.remove();
    };

    // Main send handler
    const handleSend = () => {
        const query = chatInput.value.trim();
        if (!query) return;

        addMessage(query, 'user-message');
        chatInput.value = '';
        showTyping();

        setTimeout(() => {
            fetch('/api/chatbot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            })
            .then(res => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.json();
            })
            .then(data => {
                removeTyping();
                addMessage(data.response, 'ai-message');
            })
            .catch(err => {
                removeTyping();
                addMessage(`Connection error: ${err.message}. Please ensure the server is running.`, 'ai-message');
                console.error('Chatbot fetch error:', err);
            });
        }, 600);
    };

    sendBtn.addEventListener('click', handleSend);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });

    // ========================
    // Notification Bell Logic
    // ========================
    const notifBell     = document.getElementById('notifBell');
    const notifDropdown = document.getElementById('notifDropdown');
    const notifBadge    = document.getElementById('notifBadge');
    const clearAllBtn   = document.getElementById('clearAllNotifs');

    if (notifBell && notifDropdown) {
        let unreadCount = parseInt(notifBadge.textContent) || 0;

        // Toggle dropdown open/close on bell click
        notifBell.addEventListener('click', (e) => {
            e.stopPropagation();
            notifDropdown.classList.toggle('open');
        });

        // Click on individual notification → mark as read
        document.querySelectorAll('.notif-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                if (item.classList.contains('unread')) {
                    item.classList.remove('unread');
                    item.classList.add('read');
                    unreadCount = Math.max(0, unreadCount - 1);
                    updateBadge();
                }
            });
        });

        // Clear All button
        clearAllBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            document.querySelectorAll('.notif-item').forEach(item => {
                item.classList.remove('unread');
                item.classList.add('read');
            });
            unreadCount = 0;
            updateBadge();
        });

        // Close dropdown when clicking anywhere outside
        document.addEventListener('click', () => {
            notifDropdown.classList.remove('open');
        });

        // Update badge display
        function updateBadge() {
            if (unreadCount > 0) {
                notifBadge.textContent = unreadCount;
                notifBadge.style.display = 'block';
            } else {
                notifBadge.style.display = 'none';
            }
        }
    }

}); // end DOMContentLoaded
