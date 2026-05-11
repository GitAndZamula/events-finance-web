document.addEventListener('DOMContentLoaded', function() {
    const gridView = document.getElementById('gridView');
    const tableView = document.getElementById('tableView');
    const gridBtn = document.getElementById('gridViewBtn');
    const tableBtn = document.getElementById('tableViewBtn');

    if (gridBtn && tableBtn && gridView && tableView) {
        gridBtn.addEventListener('click', function() {
            gridView.style.display = 'block';
            tableView.style.display = 'none';
            gridBtn.classList.add('active');
            tableBtn.classList.remove('active');
            localStorage.setItem('eventView', 'grid');
        });

        tableBtn.addEventListener('click', function() {
            gridView.style.display = 'none';
            tableView.style.display = 'block';
            tableBtn.classList.add('active');
            gridBtn.classList.remove('active');
            localStorage.setItem('eventView', 'table');
        });

        const savedView = localStorage.getItem('eventView');
        if (savedView === 'table') {
            tableBtn.click();
        }
    }
});