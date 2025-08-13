async function loadBooks() {
  const res = await fetch('/api/books');
  const books = await res.json();
  renderBooks(books);
}

function renderBooks(books){
  const tbody = document.querySelector('#booksTable tbody');
  tbody.innerHTML = '';
  books.forEach(b => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${b.id}</td>
      <td>${b.title}</td>
      <td>${b.author || ''}</td>
      <td>${b.isbn || ''}</td>
      <td>${b.copies}</td>
      <td>${b.available_copies}</td>
      <td>
        <button data-id="${b.id}" class="deleteBtn">Delete</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  // delete handlers
  document.querySelectorAll('.deleteBtn').forEach(btn=>{
    btn.onclick = async (e) => {
      const id = e.target.dataset.id;
      if (!confirm('Delete book?')) return;
      await fetch(`/api/books/${id}`, {method: 'DELETE'});
      loadBooks();
    };
  });
}

document.addEventListener('DOMContentLoaded', ()=>{
  loadBooks();

  document.getElementById('addBookForm').addEventListener('submit', async (e)=>{
    e.preventDefault();
    const fd = new FormData(e.target);
    const payload = {
      title: fd.get('title'),
      author: fd.get('author'),
      isbn: fd.get('isbn'),
      publisher: fd.get('publisher'),
      year: fd.get('year') ? parseInt(fd.get('year')) : null,
      copies: fd.get('copies') ? parseInt(fd.get('copies')) : 1,
      available_copies: fd.get('copies') ? parseInt(fd.get('copies')) : 1
    };
    await fetch('/api/books', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    e.target.reset();
    loadBooks();
  });

  document.getElementById('searchBtn').addEventListener('click', async ()=>{
    const q = document.getElementById('searchInput').value.trim();
    if (!q) { loadBooks(); return; }
    const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
    const books = await res.json();
    renderBooks(books);
  });

  document.getElementById('clearBtn').addEventListener('click', ()=>{
    document.getElementById('searchInput').value = '';
    loadBooks();
  });
});
