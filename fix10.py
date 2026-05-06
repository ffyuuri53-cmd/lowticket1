import os, re
filepath = 'redacao-nota-1000.html'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

mobile_css = """
    /* ===== MOBILE RESPONSIVENESS ===== */
    @media (max-width: 768px) {
      .container { width: 90%; }
      
      .hero-grid {
        grid-template-columns: 1fr;
        text-align: center;
        gap: 40px;
      }
      
      .hero-personagem-wrap {
        margin: 0 auto;
        width: 250px;
        height: 250px;
      }
      
      .hero-personagem {
        scale: 1.4;
        bottom: -20px;
      }
      
      .cta-row {
        justify-content: center;
      }
      
      .admin-modal {
        width: 95%;
        grid-template-columns: 1fr;
        max-height: 90vh;
        overflow-y: auto;
      }
      
      .toast-modern {
        width: 90vw;
        left: 5vw !important;
        bottom: 10px !important;
      }
      
      h1 { font-size: 38px !important; }
      .section-title { font-size: 28px !important; }
    }
"""

# Append mobile CSS to the first style block
text = text.replace('</style>', mobile_css + '\n    </style>', 1)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('Added mobile responsiveness CSS')
