const input = document.getElementById('image');
const dropzone = document.getElementById('dropzone');
const previewWrap = document.getElementById('previewWrap');
const preview = document.getElementById('preview');
const submitBtn = document.getElementById('submitBtn');
const replaceBtn = document.getElementById('replaceBtn');
const removeBtn = document.getElementById('removeBtn');

// ---- Select image ----
input.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (!file) return;
  showPreview(file);
});

function showPreview(file) {
  const reader = new FileReader();
  reader.onload = (ev) => {
    preview.src = ev.target.result;
    previewWrap.hidden = false;
    dropzone.style.display = 'none';
    submitBtn.disabled = false;
  };
  reader.readAsDataURL(file);
}

// ---- Remove image ----
removeBtn.addEventListener('click', () => {
  input.value = '';
  preview.src = '';
  previewWrap.hidden = true;
  dropzone.style.display = 'block';
  submitBtn.disabled = true;
});

// ---- Replace image ----
replaceBtn.addEventListener('click', () => {
  input.click();   // opens file picker again
});

// ---- Drag & drop ----
['dragenter', 'dragover'].forEach(ev =>
  dropzone.addEventListener(ev, (e) => {
    e.preventDefault();
    dropzone.classList.add('dragging');
  })
);
['dragleave', 'drop'].forEach(ev =>
  dropzone.addEventListener(ev, () => dropzone.classList.remove('dragging'))
);
dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  if (e.dataTransfer.files.length) {
    input.files = e.dataTransfer.files;
    input.dispatchEvent(new Event('change'));
  }
});

// ---- Loading state on submit ----
document.querySelector('form').addEventListener('submit', () => {
  submitBtn.disabled = true;
  submitBtn.textContent = '⏳ Analyzing…';
});