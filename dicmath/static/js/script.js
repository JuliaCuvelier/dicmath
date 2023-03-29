// Listen for keyboard events
document.addEventListener('keydown', function (event) {
  // Return if event was prevented
  if (event.defaultPrevented) {
    return;
  }

  // Trigger start button on space or enter key press
  if (event.key === ' ' || event.key === 'Enter') {
    document.getElementById('start-btn').click();
    event.preventDefault();
  }
  // Trigger clear button on backspace or delete key press
  else if (event.key === 'Backspace' || event.key === 'Delete') {
    document.getElementById('clear-btn').click();
    event.preventDefault();
  }
  // Trigger export button on ctrl/cmd + s key press
  else if ((event.ctrlKey || event.metaKey) && event.key === 's') {
    document.getElementById('export-btn').click();
    event.preventDefault();
  }
});
