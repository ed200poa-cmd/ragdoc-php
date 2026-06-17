<?php
$backend_url = rtrim(getenv('BACKEND_URL') ?: 'http://localhost:8000', '/');
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>RAGDoc — AI Document Q&A</title>
  <link rel="stylesheet" href="/assets/style.css" />
</head>
<body>

  <nav>
    <div class="nav-logo">📄 RAGDoc</div>
    <div class="nav-links">
      <a href="#upload">Upload</a>
      <a href="#chat">Chat</a>
      <a href="https://github.com/ed200poa-cmd/ragdoc-php" target="_blank">GitHub</a>
    </div>
    <a href="https://github.com/ed200poa-cmd/ragdoc-php" target="_blank" class="nav-cta">View Source</a>
  </nav>

  <main class="container">

    <section class="hero">
      <div class="hero-badge">Portfolio Project · Edward Kim</div>
      <h1>Ask Your <span>Documents</span></h1>
      <p>
        Upload a PDF or TXT file, then ask questions in natural language.
        Powered by Claude claude-sonnet-4-6 with RAG — answers cite exact passages from your document.
      </p>
    </section>

    <section id="upload" class="card">
      <h2>📤 Upload Document</h2>
      <div id="drop-zone" class="drop-zone" tabindex="0" role="button" aria-label="Upload document">
        <div class="drop-icon">📁</div>
        <p class="drop-main">Drag &amp; drop a PDF or TXT file here</p>
        <p class="drop-sub">or click to browse</p>
        <input type="file" id="file-input" accept=".pdf,.txt" />
      </div>
      <div id="upload-status" class="upload-status hidden"></div>
    </section>

    <section id="chat" class="card chat-card">
      <h2>💬 Ask a Question</h2>
      <div id="no-doc-msg" class="no-doc-msg">
        ↑ Upload a document above to start chatting
      </div>
      <div id="chat-area" class="chat-area hidden">
        <div id="messages" class="messages"></div>
        <div class="chat-input-row">
          <textarea id="question-input" placeholder="Ask something about your document…" rows="2"></textarea>
          <button id="send-btn" class="btn-send" aria-label="Send message">Send</button>
        </div>
      </div>
    </section>

    <section class="tech-section">
      <h3>Tech Stack</h3>
      <div class="tech-pills">
        <span class="pill highlight">Claude claude-sonnet-4-6</span>
        <span class="pill highlight">RAG + pgvector</span>
        <span class="pill highlight">SSE Streaming</span>
        <span class="pill">FastAPI</span>
        <span class="pill">Python 3.12</span>
        <span class="pill">OpenAI Embeddings</span>
        <span class="pill">LangChain</span>
        <span class="pill">PostgreSQL</span>
        <span class="pill">PHP 8.1</span>
        <span class="pill">Railway</span>
      </div>
    </section>

  </main>

  <footer>
    Built by <a href="mailto:ed200.poa@gmail.com">Edward Kim</a> ·
    <a href="https://github.com/ed200poa-cmd/ragdoc-php" target="_blank">GitHub</a>
  </footer>

  <script>window.BACKEND_URL = <?= json_encode($backend_url) ?>;</script>
  <script src="/assets/app.js"></script>
</body>
</html>
