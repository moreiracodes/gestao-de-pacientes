
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
Acesse na seguinte ordem:
## 1. /
Acesse primeiro a raiz para instalação e configurações dos parâmetros iniciais.

## 2. /cadastrar-usuario
Acesse esse endereço para configuração de amostra de usuários para fins de testes 

## 3. /cadastrar-dados-vitais/<email_usuario>
Por fim, acesse esse endereço para a vinculação de uma amostra de dados vitais no cujo e-mail será passado na URL.
Por exemplo:
```
http://127.0.0.1:5000/cadastrar-dados-vitais/maria@email.com
```