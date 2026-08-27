document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.querySelector('[data-menu-toggle]');
    const nav = document.querySelector('[data-main-nav]');
    menuToggle?.addEventListener('click', () => {
        const isOpen = nav.classList.toggle('nav-open');
        menuToggle.setAttribute('aria-expanded', String(isOpen));
    });

    const modal = document.querySelector('[data-upload-modal]');
    if (modal) {
        const open = () => { modal.hidden = false; modal.querySelector('input')?.focus(); };
        const close = () => { modal.hidden = true; };
        document.querySelectorAll('[data-open-upload]').forEach((button) => button.addEventListener('click', open));
        document.querySelectorAll('[data-close-upload]').forEach((button) => button.addEventListener('click', close));
        modal.addEventListener('click', (event) => { if (event.target === modal) close(); });
        document.addEventListener('keydown', (event) => { if (event.key === 'Escape' && !modal.hidden) close(); });

        const form = modal.querySelector('[data-upload-form]');
        const fileInput = modal.querySelector('input[type="file"]');
        const dropZone = modal.querySelector('[data-drop-zone]');
        const fileName = modal.querySelector('[data-file-name]');
        const submit = modal.querySelector('[data-submit-upload]');
        const showFile = (file) => {
            if (!file) return;
            fileName.textContent = file.name;
            dropZone.classList.add('has-file');
        };
        fileInput?.addEventListener('change', () => showFile(fileInput.files[0]));
        dropZone?.addEventListener('dragover', (event) => { event.preventDefault(); dropZone.classList.add('is-dragging'); });
        dropZone?.addEventListener('dragleave', () => dropZone.classList.remove('is-dragging'));
        dropZone?.addEventListener('drop', (event) => {
            event.preventDefault();
            dropZone.classList.remove('is-dragging');
            const [file] = event.dataTransfer.files;
            if (file) { fileInput.files = event.dataTransfer.files; showFile(file); }
        });
        form?.addEventListener('submit', () => {
            submit.disabled = true;
            submit.textContent = 'Uploading...';
        });
    }

    const sidebar = document.querySelector('[data-chat-sidebar]');
    document.querySelector('[data-sidebar-open]')?.addEventListener('click', () => sidebar.classList.add('sidebar-visible'));
    document.querySelector('[data-sidebar-close]')?.addEventListener('click', () => sidebar.classList.remove('sidebar-visible'));

    const search = document.querySelector('[data-chat-search]');
    search?.addEventListener('input', () => {
        const query = search.value.toLowerCase();
        document.querySelectorAll('[data-conversation-item]').forEach((item) => {
            item.hidden = !item.textContent.toLowerCase().includes(query);
        });
    });

    const messageInput = document.querySelector('[data-message-input]');
    const messageArea = document.querySelector('[data-message-area]');
    const count = document.querySelector('[data-character-count]');
    const thinking = document.querySelector('[data-thinking-state]');
    const sendButton = document.querySelector('[data-send-button]');
    const chatForm = document.querySelector('[data-chat-form]');
    const updateInput = () => {
        if (!messageInput) return;
        if (count) count.textContent = `${messageInput.value.length} / 4000`;
        messageInput.style.height = 'auto';
        messageInput.style.height = `${Math.min(messageInput.scrollHeight, 140)}px`;
    };
    messageInput?.addEventListener('input', updateInput);
    messageInput?.addEventListener('keydown', (event) => {
        if (!chatForm || !messageInput) return;
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            chatForm.requestSubmit();
        }
    });
    document.querySelectorAll('[data-suggestions] button').forEach((button) => button.addEventListener('click', () => {
        if (!messageInput) return;
        messageInput.value = button.textContent;
        updateInput();
        messageInput.focus();
    }));
    chatForm?.addEventListener('submit', () => {
        if (!messageInput || !messageInput.value.trim()) return;
        if (thinking) thinking.hidden = false;
        messageInput.readOnly = true;
        messageInput.setAttribute('aria-disabled', 'true');
        if (sendButton) sendButton.disabled = true;
    });
    document.querySelectorAll('[data-copy-message]').forEach((button) => button.addEventListener('click', async () => {
        const text = button.closest('.message-card').querySelector('p').textContent;
        await navigator.clipboard?.writeText(text);
        button.textContent = 'Copied';
    }));
    updateInput();
    if (messageArea) {
        history.scrollRestoration = 'manual';
        const scrollToLatestMessage = () => {
            messageArea.scrollTop = messageArea.scrollHeight;
            const messages = messageArea.querySelectorAll('.chat-message');
            messages[messages.length - 1]?.scrollIntoView({ block: 'end' });
            messageArea.scrollTop = messageArea.scrollHeight;
        };
        window.addEventListener('load', scrollToLatestMessage, { once: true });
        requestAnimationFrame(() => requestAnimationFrame(scrollToLatestMessage));
        window.setTimeout(scrollToLatestMessage, 150);
    }
});
