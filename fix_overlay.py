import os, re
filepath = 'redacao-nota-1000.html'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

if 'id="loading-overlay"' not in text:
    overlay_html = """
  <!-- LOADING SCREEN -->
  <div id="loading-overlay">
    <div class="loader-box">
      <div class="loader-ring"></div>
      <div class="loader-ring"></div>
      <div class="loader-ring"></div>
      <div class="loader-logo">
        <iconify-icon icon="ph:lightning-fill" width="40" style="color:var(--primary)"></iconify-icon>
      </div>
    </div>
    <p style="color:var(--white); font-family:'Anton', sans-serif; letter-spacing:3px; margin-top:20px; font-size:14px; opacity:0.8">VERIFICANDO SISTEMA...</p>
  </div>
"""
    text = text.replace('<body>', '<body>' + overlay_html)
    
    loader_styles = """
    .loader-ring {
      position: absolute;
      inset: 0;
      border: 2px solid transparent;
      border-top-color: var(--primary);
      border-radius: 50%;
      animation: spin 1.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
    }
    .loader-ring:nth-child(2) { animation-delay: 0.2s; opacity: 0.5; border-width: 1px; }
    .loader-ring:nth-child(3) { animation-delay: 0.4s; opacity: 0.2; border-width: 1px; }
    .loader-logo {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      animation: pulse 1.5s ease-in-out infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes pulse { 0%, 100% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.1); opacity: 1; } }
"""
    text = text.replace('</style>', loader_styles + '\n    </style>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added missing loading overlay and styles')
else:
    print('Loading overlay already exists')
