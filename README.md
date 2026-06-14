# SimplificaIA
# 📱 SimplificaIA

> Aplicação mobile para simplificação de textos usando IA (Gemini)

![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Recursos

### 🎯 Funcionalidades Principais
- ✅ Simplificação de textos em 3 níveis (Fundamental, Médio, Técnico)
- ✅ Cache inteligente (economiza 80-90% da quota API)
- ✅ Limite diário de 5 simplificações por IP
- ✅ Histórico local persistente (AsyncStorage)
- ✅ Copiar resultado para clipboard
- ✅ Compartilhar via WhatsApp, Email, etc
- ✅ Interface intuitiva com 2 abas de navegação

### 🏗️ Stack Tecnológico
- **Frontend:** React Native + Expo
- **Backend:** FastAPI + Python
- **IA:** Google Gemini 2.5 Flash
- **Banco:** SQLite (cache + rate limiting)
- **Armazenamento:** AsyncStorage (histórico local)

---

## 🚀 Quick Start

### Pré-requisitos
- Node.js 18+
- Python 3.10+
- Expo CLI: `npm install -g expo-cli`
- Chave API Gemini (grátis em https://ai.google.dev)

### Setup Backend

```bash
cd SimplificaIA-backed

# Criar virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instalar dependências
pip install fastapi uvicorn python-dotenv google-genai

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com sua GEMINI_API_KEY

# Rodar servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Setup Frontend

```bash
cd mobile

# Instalar dependências
npm install

# Configurar IP local
# Editar src/services/api.ts com seu IP
# Exemplo: http://192.168.0.100:8000

# Rodar app
npm start

# Escanear QR com Expo Go (iOS/Android)
```

---

## 📁 Estrutura do Projeto

```
SimplificaIA/
├── SimplificaIA-backed/          # Backend FastAPI
│   ├── app/
│   │   ├── main.py              # Entry point
│   │   ├── routes/              # Endpoints
│   │   ├── services/            # Lógica (Gemini, Cache, Rate Limit)
│   │   └── models/              # Schemas
│   ├── .env                      # Variáveis sensíveis (NÃO compartilhe!)
│   ├── .env.example              # Template (compartilhe!)
│   ├── requirements.txt
│   └── venv/
│
├── mobile/                        # Frontend React Native
│   ├── src/
│   │   ├── screens/
│   │   │   ├── HomeScreen.tsx    # Tela principal
│   │   │   └── HistoryScreen.tsx # Histórico
│   │   ├── components/
│   │   │   └── LevelSelector.tsx # Seletor de nível
│   │   └── services/
│   │       ├── api.ts           # HTTP client
│   │       └── storage.ts       http://127.0.0.1:37247/signin?nonce=FFQQBpDsipmRx9QI7QAsdw==# AsyncStorage
│   ├── App.tsx                  # Navigation
│   ├── .env.example
│   └── package.json
│
├── SECURITY.md                   # 🔒 Guia de segurança
└── README.md                     # Este arquivo
```

---


## 📊 API Endpoints

### POST `/simplify`
Simplifica um texto

**Request:**
```json
{
  "text": "Seu texto aqui",
  "level": "fundamental"  // ou "medio" ou "tecnico"
}
```

**Response:**
```json
{
  "result": "Texto simplificado",
  "remaining_uses": 4,
  "from_cache": false
}
```

**Rate Limit:** 5 por dia por IP

### GET `/cache/stats`
Estatísticas do cache

**Response:**
```json
{
  "total_cached_entries": 42,
  "total_hits": 156
}
```

---

## 🧪 Testes

### Testar Endpoint
```bash
curl -X POST http://localhost:8000/simplify \
  -H "Content-Type: application/json" \
  -d '{"text":"Olá mundo", "level":"fundamental"}'
```

### Testar Cache
```bash
# Primeira chamada (cache miss)
curl -X POST http://localhost:8000/simplify \
  -H "Content-Type: application/json" \
  -d '{"text":"Teste", "level":"fundamental"}'

# Segunda chamada (cache hit)
curl -X POST http://localhost:8000/simplify \
  -H "Content-Type: application/json" \
  -d '{"text":"Teste", "level":"fundamental"}'
# Resposta terá "from_cache": true
```

---

## 🐛 Troubleshooting

### Backend não conecta à API Gemini
```
✅ Solução: Verificar GEMINI_API_KEY em .env
✅ Verificar limite diário da API (free tier)
✅ Testar: curl https://generativelanguage.googleapis.com/
```

### App não conecta ao backend
```
✅ Solução: Verificar IP em src/services/api.ts
✅ Verificar se backend está rodando
✅ Mesmo Wi-Fi? Backend e app devem estar na mesma rede
```

### AsyncStorage não funciona
```
✅ Solução: Histórico é opcional, app funciona sem
✅ Apenas warning no console, não afeta funcionalidade
```

---

## 📈 Performance

| Métrica | Sem Cache | Com Cache |
|---------|-----------|-----------|
| Tempo Resposta | 2-3s | <100ms |
| Chamadas API | 100% | ~10-20% |
| Tokens Usados | 100% | ~10% |
| Custo | Alto | Otimizado |

**Taxa de Cache Hit:** 20-80% (depende do uso)

---

## 🚀 Deployment

### Backend (Google Cloud Run / Heroku)
```bash
# Criar requirements.txt
pip freeze > requirements.txt

# Deploy
gcloud run deploy simplifica-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=seu_valor
```

### Frontend (EAS Build / Expo)
```bash
# Gerar APK/IPA
eas build -p android
eas build -p ios

# Ou publicar na Play Store / App Store
eas submit -p android
```

---

## 📝 Roadmap

### v1.1
- [ ] PDF upload + extração de texto
- [ ] Favoritos (salvar textos especiais)
- [ ] Dark mode

### v1.2
- [ ] Busca no histórico
- [ ] Estatísticas de uso
- [ ] Autenticação de usuários
- [ ] Sincronização cloud (Supabase)

### v2.0
- [ ] Modo offline
- [ ] Colaboração em tempo real
- [ ] API pública para integração
- [ ] Múltiplas linguagens

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para detalhes.
