#teste_python
# 🐮 Super Vaca — Teste de Python 🎮

Este projeto foi desenvolvido com o objetivo de **explorar conceitos de desenvolvimento de jogos em Python**, buscando criar algo simples, funcional e que possa servir de base para futuras melhorias e aprendizados.

O **Super Vaca** é um jogo de plataforma 2D feito com **Pygame Zero**, onde o jogador controla uma vaquinha corajosa que precisa atravessar um mapa repleto de obstáculos e inimigos (rosquinhas perigosas 🍩🔥) até alcançar o mato da vitória 🌿.

---

## 🌟 Objetivo do Projeto

Este teste foi criado com o propósito de:
- Praticar **conceitos de física e colisão** em jogos 2D  
- Entender o uso de **arquivos CSV** para construção de mapas  
- Aprender a **organizar o código** em funções bem definidas  
- Adicionar **sons, música e animações simples**  
- Criar uma base para projetos maiores em Python e Pygame

---

## ⚙️ Tecnologias e Recursos Usados

- **Python 3**
- **Pygame Zero (pgzrun)**
- **Pygame mixer** (para sons e música)
- **CSV** (para leitura de mapas)
- **Lógica de física simples** (gravidade, pulo, movimento horizontal)
- **Sprites animados** para o herói e inimigos

---

## 🧩 Estrutura do Código

- `main.py` → arquivo principal do jogo  
- `mapas/mapa_geral.csv` → define o layout do cenário  
- `images/` → contém os sprites (vaca, rosquinhas, blocos, fundo etc.)  
- `music/` → contém os efeitos sonoros e músicas do jogo  

O código foi projetado para ser legível e facilmente expandido — é um experimento que mostra o processo de **aprender fazendo**.

---

## 🎮 Como Jogar

1. Execute o jogo com:
   ```bash
   pgzrun main.py
Use as setas ← → para andar.

Pressione espaço para pular.

Evite as rosquinhas e a lava!

Toque o mato verde para vencer.

Aperte R para reiniciar após morrer ou vencer.
