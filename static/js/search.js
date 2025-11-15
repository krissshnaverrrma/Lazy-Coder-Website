function openSearchModal() {
    const modal = document.getElementById('search-modal');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; 
    setTimeout(() => {
        const input = modal.querySelector('input[name="q"]');
        if (input) {
            input.focus();
        }
    }, 50);
}
function closeSearchModal() {
    const modal = document.getElementById('search-modal');
    modal.style.display = 'none';
    document.body.style.overflow = ''; 
}
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeSearchModal();
    }
});