# RastreabilidadeApp - Sistema de Rastreabilidade Rural

> Plataforma web para rastreabilidade de produtos agrícolas, garantindo transparência e segurança alimentar da origem ao consumidor. Desenvolvido em Python com o framework Flask.

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-blue)](https://github.com/seu-usuario/RastreabilidadeApp)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework%20Web-000000)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

## Sobre o Projeto

O **RastreabilidadeApp** é um sistema web projetado para conectar o campo à mesa. A plataforma permite que produtores rurais cadastrem suas propriedades e lotes de colheita, gerando um **QR Code único** para cada lote. Ao ser escaneado pelo consumidor, esse código revela todo o histórico do produto, incluindo informações sobre o produtor, a propriedade, datas de colheita e boas práticas agrícolas.

Construído com Python e Flask, o projeto visa fortalecer a confiança do consumidor, agregar valor aos produtos agrícolas e promover a segurança alimentar através da tecnologia.

## ✨ Funcionalidades

### 👤 Gestão do Produtor
- **Cadastro e Login:** Sistema de autenticação seguro para que cada produtor gerencie suas próprias informações.
- **Perfil do Produtor:** Cadastro de dados pessoais e de contato.
- **Gerenciamento de Propriedades:** O produtor pode registrar múltiplas fazendas ou locais de produção.

### 📦 Controle de Lotes
- **Registro de Lotes:** Cadastro detalhado de cada colheita, incluindo data, validade e um campo para descrever as boas práticas utilizadas.
- **Geração de QR Code:** Para cada lote registrado, o sistema gera automaticamente um QR Code que leva a uma página pública com os detalhes do produto.
- **Histórico de Lotes:** Visualização e gerenciamento de todos os lotes cadastrados por propriedade.

### 📲 Consulta Pública via QR Code
- **Página de Rastreabilidade:** Uma página web limpa e informativa que é acessada ao escanear o QR Code.
- **Transparência Total:** Consumidores podem verificar a origem, data de colheita, validade e práticas de cultivo do produto que estão comprando.

## 🖼️ Demonstração Visual

Aqui você pode inserir imagens da sua aplicação para demonstrar o visual e as funcionalidades. Substitua os links de placeholder pelos links das suas imagens.

| Página Inicial | Cadastro de Lote | Consulta do QR Code |
| :---: | :---: | :---: |
| *<img width="1898" height="1079" alt="Image" src="https://github.com/user-attachments/assets/7c2d0d52-b96a-4921-88eb-b7d0cd0f950b" />* | *<img width="1898" height="1079" alt="Image" src="https://github.com/user-attachments/assets/d31ed80d-25bc-496c-bc81-ab476ff193ec" />* | *Substitua este texto por sua imagem* |

## Tecnologias

### Backend
- **Python 3.8+** - Linguagem principal
- **Flask** - Framework web para a construção da aplicação
- **SQLAlchemy** - ORM para interação com o banco de dados
- **Flask-Migrate** - Para gerenciamento de migrações do banco de dados
- **Werkzeug** - Para hashing de senhas e segurança

### Frontend
- **HTML5**
- **CSS3** (com estilo moderno e responsivo)
- **JavaScript**

### Banco de Dados
- **SQLite3** (padrão de desenvolvimento) ou outro banco de dados relacional.

## Pré-requisitos

- [Python 3.8+](https://python.org/downloads/)
- Git para clonar o repositório

## Instalação

1.  **Clone o repositório**
    ```bash
    git clone https://github.com/seu-usuario/RastreabilidadeApp.git
    cd RastreabilidadeApp
    ```

2.  **Crie e ative um ambiente virtual**
    ```bash
    # Para Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplique as migrações do banco de dados**
    ```bash
    # Inicializa o banco de dados (apenas na primeira vez)
    flask db init 
    flask db migrate -m "Initial migration."
    
    # Aplica a migração para criar as tabelas
    flask db upgrade
    ```

5.  **Execute o sistema**
    ```bash
    python run.py
    ```
    Acesse a aplicação em `http://127.0.0.1:5000`.

## Uso

### Primeiro Acesso
1.  Execute a aplicação.
2.  Crie uma nova conta de usuário na página de registro.
3.  Após o login, cadastre as informações do produtor.
4.  Cadastre uma ou mais propriedades associadas a este produtor.
5.  Comece a registrar os lotes de produtos.

### Operação Diária
1.  **Registrar Colheita**: Crie um novo lote para cada colheita, preenchendo as informações.
2.  **Gerar Etiqueta**: Salve ou imprima o QR Code gerado para o lote.
3.  **Aplicar no Produto**: Cole a etiqueta com o QR Code na embalagem do produto.
4.  **Consulta**: O consumidor final escaneia o código para visualizar a origem e os detalhes do produto.

## Contribuição

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito apreciada**.

1.  Faça um Fork do projeto
2.  Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Faça Commit de suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4.  Faça Push para a Branch (`git push origin feature/AmazingFeature`)
5.  Abra um Pull Request

## Suporte

Para suporte técnico ou dúvidas:

-   **Email**: [g.moreno.souza05@gmail.com](mailto:g.moreno.souza05@gmail.com)

## Licença

Este projeto está licenciado sob uma Licença Proprietária - veja o arquivo [LICENSE](LICENSE) para detalhes.

**Uso Restrito**: Este software é de propriedade exclusiva do autor. Uso comercial ou redistribuição requer autorização expressa.

---

<div align="center">
  Desenvolvido por Gustavo Moreno e Akio Tani
  <br><br>
  <a href="https://www.linkedin.com/in/gustavomoreno05" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24" alt="LinkedIn"/>
  </a>
</div>
