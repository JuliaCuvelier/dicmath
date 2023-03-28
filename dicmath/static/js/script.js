document.addEventListener('keydown', function (event) {
  if (event.defaultPrevented) {
    return;
  }

  if (event.key === ' ' || event.key === 'Enter') {
    document.getElementById('start-btn').click();
    event.preventDefault();
  } else if (event.key === 'Backspace' || event.key === 'Delete') {
    document.getElementById('clear-btn').click();
    event.preventDefault();
  } else if ((event.ctrlKey || event.metaKey) && event.key === 's') {
    document.getElementById('export-btn').click();
    event.preventDefault();
  }
});
