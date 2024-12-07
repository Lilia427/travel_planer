// Додає підтвердження перед видаленням елемента
function confirmDelete(message) {
    return confirm(message || "Ви впевнені, що хочете видалити цей елемент?");
}

// Приклади динамічних фільтрів (розширювано за потреби)
document.addEventListener('DOMContentLoaded', function () {
    const filterInput = document.querySelector('#filter-input');
    const tableRows = document.querySelectorAll('table tr');

    if (filterInput) {
        filterInput.addEventListener('input', function () {
            const filterText = filterInput.value.toLowerCase();

            tableRows.forEach(row => {
                const cells = row.querySelectorAll('td');
                const rowText = Array.from(cells).map(cell => cell.textContent).join(' ').toLowerCase();

                if (rowText.includes(filterText)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
});

// Інтерактивне повідомлення після дії
function showToast(message, duration = 3000) {
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.bottom = '20px';
    toast.style.left = '50%';
    toast.style.transform = 'translateX(-50%)';
    toast.style.backgroundColor = '#007bff';
    toast.style.color = 'white';
    toast.style.padding = '10px 20px';
    toast.style.borderRadius = '5px';
    toast.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, duration);
}

// Приклад виклику toast
// showToast('Дія виконана успішно!');
