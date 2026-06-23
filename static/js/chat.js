// static/js/chat.js
document.addEventListener('DOMContentLoaded', function() {
    let currentSchool = 'huvo';
    const conversations = { huvo: [], biquan: [], khacky: [], hien_sinh: [], maclenin: [] };

    const chatbox = document.getElementById('chatbox');
    const questionInput = document.getElementById('question_input');
    const sendBtn = document.getElementById('send_btn');

    // Chuyển đổi qua lại giữa các Tab trường phái triết học
    document.querySelectorAll('.tab-link').forEach(link => {
        link.addEventListener('click', function() {
            document.querySelectorAll('.tab-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            currentSchool = this.dataset.tab;
            renderChatHistory();
        });
    });

    // Lắng nghe nút gửi tin nhắn
    sendBtn.addEventListener('click', sendMessage);
    questionInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

    function sendMessage() {
        const text = questionInput.value.trim();
        if (!text) return;

        // Thêm tin nhắn của User vào lịch sử chat
        conversations[currentSchool].push({ role: 'user', content: text });
        displayMessage(text, 'user');
        questionInput.value = '';

        // Hiển thị trạng thái Loading
        const loadingDiv = displayMessage('Triết gia đang suy tư...', 'bot loading');

        // Gửi request lên Flask Backend
        fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversation: conversations[currentSchool],
                school: currentSchool
            })
        })
        .then(res => res.json())
        .then(data => {
            loadingDiv.remove();
            if (data.answer) {
                conversations[currentSchool].push({ role: 'bot', content: data.answer });
                displayMessage(data.answer, 'bot');
            } else {
                displayMessage('Đã có lỗi xảy ra.', 'bot');
            }
        });
    }

    function displayMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        msgDiv.innerText = text;
        chatbox.appendChild(msgDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
        return msgDiv;
    }

    function renderChatHistory() {
        chatbox.innerHTML = '';
        conversations[currentSchool].forEach(msg => {
            displayMessage(msg.content, msg.role);
        });
    }

    // Nút chuyển chế độ Dark Mode
    document.getElementById('dark-mode-toggle').addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
    });
});