
# Gestão de Pacientes
Este app é uma ferramenta para gestão de pacientes por profissionais da saúde.

Utiliza Python Flask e SQLite

Para executá-lo localmente:

1. Clone este repositório.
```
git clone https://github.com/moreiracodes/gestao-de-pacientes
```

2. Instale o Flask
```
pip install flask
```

3. Execute
```
flask --app main run
```

# URLs (trabalho em progresso)
Ao executar o servidor flask (comando acima), acesse na seguinte ordem para instalar o ambiente de testes:
## 1. /config
Acesse primeiro /config para instalação e configurações dos parâmetros iniciais.
Obs: Apenas o usuário Maria tem dados vitais cadastrados
## 2. /lista/usuarios
Para visualizar todos os usuários cadastrados 

PS: por enquanto, não há página inicial na raiz (/)