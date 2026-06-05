# Termo

Clone do jogo [termo.ooo](https://term.ooo/) (versão em português do [Wordle](https://www.nytimes.com/games/wordle/index.html)) desenvolvido 
pelo aluno Vinícius G. Mendonça para disciplina de Python Scripting da 
especialização em Engenharia de Serviços e Sistemas de Cloud Computing, turma de 2026.

<img width="75%" height="75%" alt="image" src="https://github.com/user-attachments/assets/ce2982d0-4f8b-41e2-baa7-abfc73eebd01" />


Vídeo explicativo: https://youtu.be/F5sfoBT2qmE

## Instruções

Descubra a palavra oculta em 6 tentativas. A cada tentativa o game te mostrará
o quão perto você está da solução:
* Se a letra ficar verde, ele está na palavra secreta e na posição correta
* Se a letra ficar amarela, ela está na palavra secreta, mas você errou a posição
* Caso contrário, a letra ficará preta

Digite as letras usando o teclado e pressione enter para confirmar.
Você não precisa colocar acentos, o jogo acentuará automaticamente.

# Executando o jogo

1. Clone o repositório ou baixe-o e descompacte-o em algum diretório.

2. Crie o ambiente virtual python

```bash
python -m venv .venv
```

3. Inicie-o

No Windows:
```bash
.venv\\Scripts\\activate
```

No Linux ou macOS:
```bash
source .venv/bin/activate
```

4. Instale as dependências do arquivo requirements.txt

```bash
pip install -r requirements.txt
```

5. Execute o jogo

```bash
cd src
python termo.py
```

## Cheat mode

Para ativar o cheat mode, rode o jogo uma vez para que o arquivo `game.ini` seja gerado.
Adicione a esse arquivo a chave:
`CHEAT=TRUE`

Reinicie o jogo.

No modo cheat, as letras corretas já ficarão pintadas em verde no teclado - o que deixa o jogo 
consideravelmente mais fácil. Se você quiser acertar de primeira, a palavra correta será impressa 
no console.

## Dicionário

As palavras permitidas estão no arquivo `lexico.txt`. 
Entretanto, as palavras sorteáveis encontram-se no arquivo `palavras.csv`.

O game nunca sorteará palavras presentes no arquivo `negativas.txt`.

Os scripts presentes na pasta `scripts` do dicionário foram usados para gerar e higienizar 
esses arquivos.


### Divita-se! :)
