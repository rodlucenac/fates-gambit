# 🎲 Fate's Gambit - Jogo Estatístico em Python

## 📖 Sobre o Projeto

Jogo educativo que demonstra conceitos de **probabilidade e estatística** através de combate baseado em dados, com visualização gráfica **em tempo real**.

### 🎯 Objetivos Educacionais

- Demonstrar distribuições de probabilidade (uniforme e normal)
- Comparar resultados teóricos vs empíricos
- Visualizar Lei dos Grandes Números
- Análise de eventos aleatórios em tempo real

---

## 🎮 Como Funciona

### **Tela Dividida:**
- **Metade Esquerda:** Jogo (combate RPG com dados)
- **Metade Direita:** Gráficos estatísticos em tempo real

### **Mecânica:**
1. Escolha uma arma (cada uma usa dados diferentes)
2. Ataque o monstro
3. Veja os gráficos atualizarem instantaneamente
4. Compare teoria vs prática

---

## 📊 Conceitos Demonstrados

### ✅ **Distribuição de Probabilidade**
- **1d6 (Adaga):** Distribuição uniforme
- **2d6 (Espada):** Distribuição normal (aproximada)
- **1d20 (Crítico):** Alta variância

### ✅ **Comparação Teórico vs Empírico**
- Curva teórica (vermelho) vs observado (azul)
- Quanto mais você joga, mais convergem!

### ✅ **Lei dos Grandes Números**
- Dano médio converge para o valor esperado
- Visualização em tempo real

---

## 🛠️ Instalação

### **Requisitos:**
- Python 3.8+
- pip

### **Passo 1: Instalar dependências**

```bash
pip install -r requirements.txt
```

Ou manualmente:
```bash
pip install pygame matplotlib numpy
```

---

## 🚀 Como Executar

```bash
python main.py
```

ou

```bash
python3 main.py
```

---

## 🎮 Controles

### **Mouse:**
- Clique nas armas para selecionar
- Clique em "ATACAR!" para atacar

### **Teclado:**
- **↑ / ↓**: Selecionar arma
- **ESPAÇO / ENTER**: Atacar
- **ESC**: Sair (na tela de fim de jogo)

---

## ⚔️ Sistema de Armas

| Arma | Dados | Dano Médio | Distribuição |
|------|-------|------------|--------------|
| 🗡️ Adaga Rápida | 1d6 | 3.5 | Uniforme |
| ⚔️ Espada Comum | 2d6 | 7.0 | Normal |
| 🔨 Martelo Pesado | 3d4 | 7.5 | Concentrada |
| 🏹 Arco Longo | 1d12 | 6.5 | Alta variância |
| ⚡ Cajado Mágico | 4d3 | 8.0 | Muito concentrada |
| 🔥 Crítico Lendário | 1d20 | 10.5 | Máxima variância |

---

## 👹 Monstros

1. **🐀 Rato Gigante** - HP: 15
2. **🧟 Zumbi Podre** - HP: 30
3. **🦴 Esqueleto Guerreiro** - HP: 45
4. **👻 Espectro Sombrio** - HP: 60
5. **🐺 Lobisomem Feroz** - HP: 80
6. **🐉 Dragão de Variância** (CHEFE) - HP: 150

---

## 📊 Gráficos em Tempo Real

### **Gráfico 1: Distribuição de Dano**
- Histograma do dano observado (azul)
- Curva teórica esperada (vermelho)
- Mostra convergência em tempo real

### **Gráfico 2: Histórico de Dano**
- Linha do tempo de todos os ataques
- Média móvel (linha tracejada)
- Permite ver tendências

### **Gráfico 3: Comparação por Arma**
- Barras comparando teoria vs prática
- Para cada arma utilizada
- Vermelho = teórico, Azul = observado

---

## 🎓 Uso Educacional

### **Para Professores:**

Este jogo demonstra:
1. **Distribuições de probabilidade** de forma visual
2. **Lei dos Grandes Números** em ação
3. **Comparação estatística** teoria vs prática
4. **Eventos aleatórios** em tempo real

### **Conceitos Abordados:**
- Distribuição uniforme
- Distribuição normal (aproximada)
- Média, variância e desvio padrão
- Convergência estatística
- Análise de dados em tempo real

---

## 🏗️ Estrutura do Código

```python
main.py
├── Game (classe principal)
│   ├── __init__()           # Inicialização
│   ├── attack()             # Sistema de combate
│   ├── draw_game_panel()    # Desenha jogo (esquerda)
│   ├── draw_stats_panel()   # Desenha stats (direita)
│   ├── create_stats_graph() # Gera gráficos matplotlib
│   └── run()                # Loop principal
│
├── roll_dice()              # Função para rolar dados
└── calculate_theoretical_prob() # Calcula probabilidades teóricas
```

---

## 🐛 Solução de Problemas

### **Erro: "No module named 'pygame'"**
```bash
pip install pygame
```

### **Erro: "No module named 'matplotlib'"**
```bash
pip install matplotlib
```

### **Jogo lento / travando**
- Reduza FPS (linha 14): `FPS = 30`
- Simplifique gráficos (comente alguns plots)

### **Gráficos não aparecem**
- Verifique se matplotlib está instalado
- Teste: `python -c "import matplotlib; print('OK')"`

---

## 📝 Requisitos do Trabalho Atendidos

✅ **Tela dividida** - Jogo à esquerda, gráficos à direita

✅ **Simulação em tempo real** - Dados rolam a cada ataque

✅ **Resultados atualizados em tempo real** - Gráficos atualizam instantaneamente

✅ **Probabilidades teóricas vs empíricas** - Comparação visual em todos os gráficos

---

## 🎨 Personalização

### **Mudar cores:**
```python
# Linha 19-25
COLOR_BG = (15, 5, 30)      # Fundo
COLOR_PANEL = (50, 25, 75)  # Painéis
COLOR_GOLD = (255, 215, 0)  # Títulos
```

### **Adicionar mais armas:**
```python
# Linha 27
WEAPONS.append({
    "name": "Nova Arma",
    "dice": "2d8",
    "num_dice": 2,
    "sides": 8,
    "avg": 9.0
})
```

### **Mudar dificuldade:**
```python
# Linha 46 - aumentar/diminuir HP dos monstros
MONSTERS[0]["hp"] = 30  # Era 15
```

---

## 📄 Licença

MIT License - Livre para uso educacional

---

## 👤 Autor

Trabalho de Estatística - Demonstração de Probabilidades

---

## 🎉 Divirta-se!

**Explore as probabilidades, veja a matemática acontecer em tempo real!** 🎲📊