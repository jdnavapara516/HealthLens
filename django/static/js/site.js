document.addEventListener('DOMContentLoaded', () => {
    const modal = document.querySelector('[data-upload-modal]');
    if (!modal) return;
    const open = () => { modal.hidden = false; modal.querySelector('input')?.focus(); };
    const close = () => { modal.hidden = true; };
    document.querySelectorAll('[data-open-upload]').forEach((button) => button.addEventListener('click', open));
    document.querySelectorAll('[data-close-upload]').forEach((button) => button.addEventListener('click', close));
    modal.addEventListener('click', (event) => { if (event.target === modal) close(); });
});
