
const rowsPerPage = 10;
let currentPage = 1;

function displayProducts(page) {
    const productTable = document.getElementById('productTable');
    productTable.innerHTML = '';

    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const paginatedProducts = products.slice(start, end);

    paginatedProducts.forEach(product => {
        const row = document.createElement('tr');
        
        for (const key in product) {
            const cell = document.createElement('td');
            cell.textContent = product[key];
            row.appendChild(cell);
        }

        const actionCell = document.createElement('td');
        actionCell.textContent = '...';
        row.appendChild(actionCell);

        productTable.appendChild(row);
    });

    updatePagination();
}

function updatePagination() {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    const totalPages = Math.ceil(products.length / rowsPerPage);

    const createButton = (label, page) => {
        const button = document.createElement('button');
        button.textContent = label;
        button.className = (page === currentPage) ? 'active' : '';
        button.addEventListener('click', () => {
            currentPage = page;
            displayProducts(currentPage);
        });
        return button;
    };

    // Previous button
    const prevButton = createButton('«', currentPage > 1 ? currentPage - 1 : 1);
    pagination.appendChild(prevButton);

    let startPage = currentPage - 1;
    let endPage = currentPage + 1;

    if (startPage < 1) {
        startPage = 1;
        endPage = Math.min(totalPages, startPage + 2);
    }

    if (endPage > totalPages) {
        endPage = totalPages;
        startPage = Math.max(1, endPage - 2);
    }

    for (let i = startPage; i <= endPage; i++) {
        const button = createButton(i, i);
        pagination.appendChild(button);
    }

    // Next button
    const nextButton = createButton('»', currentPage < totalPages ? currentPage + 1 : totalPages);
    pagination.appendChild(nextButton);
}

displayProducts(currentPage);

