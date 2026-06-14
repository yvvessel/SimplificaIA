# 🔒 Guia de Segurança - SimplificaIA

## ⚠️ Dados Sensíveis

### Backend (.env)
```
GEMINI_API_KEY=xxx           # Chave da API do Google Gemini
SECRET_KEY=xxx               # Chave secreta para JWT/sessions
DATABASE_CREDENTIALS=xxx     # Credenciais do banco (se usar)
```

### Frontend (.env)
```
EXPO_PUBLIC_API_URL=xxx      # URL do backend (pode ser pública)
```

---

## 🚫 O que NÃO Compartilhar

❌ **NUNCA compartilhe:**
- `.env` (contém GEMINI_API_KEY)
- API keys e tokens
- Credenciais de banco de dados
- Senhas
- URLs privadas de produção

✅ **SIM, compartilhe:**
- `.env.example` (template sem valores)
- `.gitignore` (padrão de exclusão)
- Este arquivo (documentação)
- Código fonte

---

## 📋 Checklist de Segurança

### Antes de Fazer Commit
- [ ] `.env` não está no staging (`git status`)
- [ ] `.env` está no `.gitignore`
- [ ] API keys não estão hardcoded no código
- [ ] `cache.db` e `usage.db` não estão no git

### Antes de Deploy
- [ ] `.env.example` foi atualizado com novas vars
- [ ] Instruções estão em `README.md`
- [ ] Secrets foram configuradas no server
- [ ] Variáveis de ambiente apontam para valores seguros

### Em Caso de Vazamento
1. ⚠️ **IMEDIATAMENTE** revogar a chave comprometida
2. Gerar uma nova GEMINI_API_KEY
3. Atualizar `.env` com a nova chave
4. Fazer commit
5. (Se público) Notificar usuários

---

## 🔧 Setup Local

### Passo 1 - Backend
```bash
cd SimplificaIA-backed
cp .env.example .env
# Editar .env com suas chaves
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Passo 2 - Frontend
```bash
cd mobile
cp .env.example .env
# Editar .env com seu IP local
npm install
npm start
```

---

## 📦 Variáveis por Ambiente

### Development (.env)
```
ENVIRONMENT=development
DEBUG=true
RATE_LIMIT_USES_PER_DAY=100  # Limite maior para testes
```

### Production (.env.production)
```
ENVIRONMENT=production
DEBUG=false
RATE_LIMIT_USES_PER_DAY=5    # Limite menor
```

---

## 🛡️ Práticas Recomendadas

1. **Rotação de Chaves**
   - Trocar GEMINI_API_KEY a cada 90 dias
   - Usar diferentes chaves por ambiente

2. **Versionamento**
   - Nunca commitar `.env` acidentalmente
   - Usar `git hooks` para prevenir

3. **Monitoramento**
   - Verificar logs de acesso à API
   - Alertas para uso anormal

4. **Backups**
   - Guardar `.env` seguro
   - Usar password manager para chaves

---

## 📞 Suporte

Se sua chave foi exposta:
1. Gerar nova chave em https://ai.google.dev
2. Revogar a antiga
3. Atualizar `.env`
4. Fazer redeploy

**Lembre-se:** Segurança é responsabilidade de todos! 🔐
