document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.querySelector('[data-menu-toggle]');
    const nav = document.querySelector('[data-main-nav]');
    menuToggle?.addEventListener('click', () => {
        const isOpen = nav.classList.toggle('nav-open');
        menuToggle.setAttribute('aria-expanded', String(isOpen));
    });

    const modal = document.querySelector('[data-upload-modal]');
    if (!modal) return;
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
});
