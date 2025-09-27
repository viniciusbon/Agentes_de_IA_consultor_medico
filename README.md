# Analisador de Exames com IA

Este projeto utiliza a API da OpenAI para extrair dados de laudos de exames em formato PDF, estruturá-los em um formato legível por máquina (JSON) e, em seguida, gerar um resumo amigável destacando os resultados que estão fora dos valores de referência.

## Funcionalidades

- **Extração de Texto:** Lê arquivos PDF de laudos de exames e extrai o conteúdo textual.
- **Estruturação com IA:** Envia o texto para o modelo `gpt-3.5-turbo` da OpenAI para identificar e organizar os exames, valores e unidades em um formato JSON estruturado.
- **Análise e Resumo:** Compara os resultados extraídos com uma lista de valores de referência e gera um resumo claro, em linguagem natural, apontando apenas os resultados que estão fora do padrão.

## Pré-requisitos

- Python 3.8 ou superior
- Uma chave de API da OpenAI

## Como Configurar e Executar

Siga os passos abaixo para colocar o projeto em funcionamento.

### 1. Clone o Repositório

```bash
git clone [https://github.com/seu-usuario/analisador-de-exames.git](https://github.com/seu-usuario/analisador-de-exames.git)
cd analisador-de-exames
```

### 2. Crie um Ambiente Virtual (Recomendado)

Isso mantém as dependências do projeto isoladas do seu sistema.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

O arquivo `requirements.txt` contém todas as bibliotecas Python necessárias.

```bash
pip install -r requirements.txt
```

### 4. Configure sua Chave de API

Para que o programa possa se comunicar com a OpenAI, você precisa fornecer sua chave de API.

1.  Renomeie o arquivo `.env.example` para `.env`.
2.  Abra o arquivo `.env` e substitua `"sua_chave_aqui"` pela sua chave de API da OpenAI.

    ```
    OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```

### 5. Prepare os Arquivos de Entrada

1.  **PDF do Exame:** Coloque o arquivo PDF do seu exame na pasta principal do projeto e renomeie-o para `Exame.pdf`.
2.  **Valores de Referência:** O arquivo `valores_referencia.json` já vem com alguns exemplos. Você pode editar este arquivo para adicionar ou modificar os exames e seus respectivos valores de referência.

### 6. Execute o Script

Com tudo configurado, basta executar o arquivo principal:

```bash
python analisador_exames.py
```

O programa irá processar o PDF e exibir o resumo final diretamente no terminal.

---

### **Aviso Importante**

Este projeto é uma ferramenta de automação e auxílio à visualização de dados. **Não é um substituto para aconselhamento médico profissional.** Os resumos gerados pela IA não constituem um diagnóstico. Consulte sempre um médico para a interpretação de seus exames.