function toggleReaders() {
  const content = document.getElementById('readers_content');
  const button = document.getElementById('toggle-readers-btn');
  
  if (content.style.display === 'none') {
    content.style.display = 'block';
    button.textContent = 'Скрыть';
    button.className = 'red_btn';
  } else {
    content.style.display = 'none';
    button.textContent = 'Показать';
    button.className = 'green_btn';
  }
}

function toggleBooks() {
  const content = document.getElementById('books_content');
  const button = document.getElementById('toggle-books-btn');
  
  if (content.style.display === 'none') {
    content.style.display = 'block';
    button.textContent = 'Скрыть';
    button.className = 'red_btn';
  } else {
    content.style.display = 'none';
    button.textContent = 'Показать';
    button.className = 'green_btn';
  }
}
