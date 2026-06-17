(function () {
  'use strict';

  const BACKEND = window.BACKEND_URL;
  let documentId = null;
  let isStreaming = false;

  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file-input');
  const uploadStatus = document.getElementById('upload-status');
  const noDocMsg = document.getElementById('no-doc-msg');
  const chatArea = document.getElementById('chat-area');
  const messages = document.getElementById('messages');
  const questionInput = document.getElementById('question-input');
  const sendBtn = document.getElementById('send-btn');

  // --- Drop zone ---
  dropZone.addEventListener('dragover', function (e) {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });
  dropZone.addEventListener('dragleave', function () {
    dropZone.classList.remove('drag-over');
  });
  dropZone.addEventListener('drop', function (e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    var file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });
  fileInput.addEventListener('change', function () {
    if (fileInput.files[0]) handleFile(fileInput.files[0]);
  });

  // --- File handling ---
  function handleFile(file) {
    var ext = file.name.split('.').pop().toLowerCase();
    if (ext !== 'pdf' && ext !== 'txt') {
      showStatus('error', 'Only PDF and TXT files are supported');
      return;
    }
    showStatus('loading', 'Uploading ' + file.name + '…');

    var formData = new FormData();
    formData.append('file', file);

    fetch('/upload.php', { method: 'POST', body: formData })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (data.success) {
          documentId = data.document_id;
          showStatus('success', '✓ "' + data.filename + '" uploaded — ' + data.chunk_count + ' chunks indexed');
          noDocMsg.classList.add('hidden');
          chatArea.classList.remove('hidden');
        } else {
          showStatus('error', data.error || 'Upload failed');
        }
      })
      .catch(function (err) {
        showStatus('error', 'Upload failed: ' + err.message);
      });
  }

  function showStatus(type, msg) {
    uploadStatus.className = 'upload-status ' + type;
    uploadStatus.textContent = msg;
  }

  // --- Chat ---
  sendBtn.addEventListener('click', sendMessage);
  questionInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  function sendMessage() {
    var question = questionInput.value.trim();
    if (!question || isStreaming || !documentId) return;

    isStreaming = true;
    sendBtn.disabled = true;
    questionInput.value = '';

    appendMessage('user', question);
    var assistantEl = appendMessage('assistant', '');
    var textEl = assistantEl.querySelector('.message-text');
    var citationsEl = assistantEl.querySelector('.citations');

    var cursorEl = document.createElement('span');
    cursorEl.className = 'cursor';
    textEl.appendChild(cursorEl);

    fetch(BACKEND + '/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: question, document_id: documentId }),
    })
      .then(function (res) {
        var reader = res.body.getReader();
        var decoder = new TextDecoder();
        var buffer = '';

        function read() {
          return reader.read().then(function (result) {
            if (result.done) {
              cursorEl.remove();
              isStreaming = false;
              sendBtn.disabled = false;
              return;
            }

            buffer += decoder.decode(result.value, { stream: true });
            var lines = buffer.split('\n');
            buffer = lines.pop();

            lines.forEach(function (line) {
              if (!line.startsWith('data: ')) return;
              var raw = line.slice(6);
              if (raw === '[DONE]') return;
              try {
                var data = JSON.parse(raw);
                if (data.token) {
                  textEl.insertBefore(document.createTextNode(data.token), cursorEl);
                  messages.scrollTop = messages.scrollHeight;
                }
                if (data.citations) {
                  renderCitations(citationsEl, data.citations);
                }
              } catch (_) {}
            });

            return read();
          });
        }

        return read();
      })
      .catch(function (err) {
        cursorEl.remove();
        textEl.textContent = 'Error: ' + err.message;
        isStreaming = false;
        sendBtn.disabled = false;
      });
  }

  function appendMessage(role, text) {
    var div = document.createElement('div');
    div.className = 'message ' + role;

    var content = document.createElement('div');
    content.className = 'message-content';

    var textEl = document.createElement('div');
    textEl.className = 'message-text';
    textEl.textContent = text;
    content.appendChild(textEl);

    if (role === 'assistant') {
      var citationsEl = document.createElement('div');
      citationsEl.className = 'citations';
      content.appendChild(citationsEl);
    }

    div.appendChild(content);
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }

  function renderCitations(el, citations) {
    if (!citations || !citations.length) return;
    var html = '<div class="citations-label">Sources</div>';
    citations.forEach(function (c) {
      html += '<div class="citation">'
        + '<div class="citation-file">📄 ' + esc(c.filename) + '</div>'
        + '<p class="citation-excerpt">' + esc(c.excerpt) + '</p>'
        + '</div>';
    });
    el.innerHTML = html;
  }

  function esc(str) {
    var d = document.createElement('div');
    d.appendChild(document.createTextNode(str));
    return d.innerHTML;
  }
})();
