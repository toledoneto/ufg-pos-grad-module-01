const API_URL = (typeof CONFIG !== 'undefined') ? CONFIG.API_URL : 'http://127.0.0.1:8000/api/gerar-senha';

const lengthSlider  = document.getElementById('lengthSlider');
const lengthValue   = document.getElementById('lengthValue');
const chkUppercase  = document.getElementById('chkUppercase');
const chkLowercase  = document.getElementById('chkLowercase');
const chkNumbers    = document.getElementById('chkNumbers');
const chkSpecials   = document.getElementById('chkSpecials');
const generateBtn   = document.getElementById('generateBtn');
const passwordText  = document.getElementById('passwordText');
const copyBtn       = document.getElementById('copyBtn');
const strengthFill  = document.getElementById('strengthFill');
const strengthLabel = document.getElementById('strengthLabel');
const errorMsg      = document.getElementById('errorMsg');

const CHECKBOXES = [chkUppercase, chkLowercase, chkNumbers, chkSpecials];

const STRENGTH = {
  'fraca':       { width: '25%',  color: 'var(--strength-fraca)',       label: 'Fraca'       },
  'média':       { width: '50%',  color: 'var(--strength-media)',       label: 'Média'       },
  'forte':       { width: '75%',  color: 'var(--strength-forte)',       label: 'Forte'       },
  'muito forte': { width: '100%', color: 'var(--strength-muito-forte)', label: 'Muito Forte' },
};

// ── Slider ──────────────────────────────────────────────────────────────────

lengthSlider.addEventListener('input', () => {
  lengthValue.textContent = lengthSlider.value;
});

// ── Validação de checkboxes ──────────────────────────────────────────────────

function validarCriterios() {
  const algumMarcado = CHECKBOXES.some(cb => cb.checked);
  generateBtn.disabled = !algumMarcado;
  errorMsg.textContent  = algumMarcado ? '' : 'Selecione pelo menos um tipo de caractere.';
}

CHECKBOXES.forEach(cb => cb.addEventListener('change', validarCriterios));

// ── Indicador de força ───────────────────────────────────────────────────────

function exibirForca(forca) {
  const cfg = STRENGTH[forca] ?? STRENGTH['fraca'];
  strengthFill.style.width           = cfg.width;
  strengthFill.style.backgroundColor = cfg.color;
  strengthLabel.style.color          = cfg.color;
  strengthLabel.textContent          = cfg.label;
}

function limparForca() {
  strengthFill.style.width  = '0';
  strengthLabel.textContent = '';
}

// ── Gerar senha ──────────────────────────────────────────────────────────────

generateBtn.addEventListener('click', async () => {
  errorMsg.textContent      = '';
  generateBtn.disabled      = true;
  generateBtn.textContent   = 'Gerando…';

  const payload = {
    tamanho:    parseInt(lengthSlider.value, 10),
    maiusculas: chkUppercase.checked,
    minusculas: chkLowercase.checked,
    numeros:    chkNumbers.checked,
    especiais:  chkSpecials.checked,
  };

  try {
    const resp = await fetch(API_URL, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });

    const data = await resp.json();

    if (!resp.ok) {
      errorMsg.textContent = 'Erro ao gerar a senha. Verifique os critérios e tente novamente.';
      limparForca();
      return;
    }

    passwordText.textContent = data.senha;
    passwordText.classList.remove('placeholder');
    copyBtn.disabled = false;
    exibirForca(data.forca);

  } catch {
    errorMsg.textContent = 'Não foi possível conectar ao servidor. Verifique se o backend está em execução.';
    limparForca();
  } finally {
    generateBtn.disabled    = false;
    generateBtn.textContent = 'Gerar Senha';
  }
});

// ── Copiar senha ─────────────────────────────────────────────────────────────

copyBtn.addEventListener('click', async () => {
  const senha = passwordText.textContent;

  try {
    await navigator.clipboard.writeText(senha);
  } catch {
    // Fallback para contextos não-seguros (file://)
    const tmp = document.createElement('textarea');
    tmp.value = senha;
    tmp.style.position = 'fixed';
    tmp.style.opacity  = '0';
    document.body.appendChild(tmp);
    tmp.select();
    document.execCommand('copy');
    document.body.removeChild(tmp);
  }

  copyBtn.textContent = 'Copiado!';
  setTimeout(() => { copyBtn.textContent = 'Copiar'; }, 2000);
});
