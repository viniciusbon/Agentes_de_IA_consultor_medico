import fitz  # PyMuPDF
import openai
import json
import os
from dotenv import load_dotenv

# --- Configuração Inicial ---

def configurar_api():
    """
    Carrega a chave da API da OpenAI do arquivo .env e a configura no cliente.
    Retorna True se a chave foi carregada com sucesso, False caso contrário.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Erro: A chave da API da OpenAI não foi encontrada.")
        print("Por favor, crie um arquivo '.env' e adicione a linha: OPENAI_API_KEY='sua_chave_aqui'")
        return False
    openai.api_key = api_key
    return True

# --- Agente 1: Extração e Estruturação de Dados ---

def extrair_texto_de_pdf(caminho_do_arquivo_pdf: str) -> str:
    """
    Abre um arquivo PDF e extrai todo o texto contido nele.
    """
    try:
        with fitz.open(caminho_do_arquivo_pdf) as documento:
            texto_completo = ""
            for pagina in documento:
                texto_completo += pagina.get_text()
        return texto_completo
    except Exception as e:
        print(f"Erro ao ler o PDF '{caminho_do_arquivo_pdf}': {e}")
        return ""

def estruturar_dados_do_exame(texto_do_exame: str) -> list:
    """
    Usa a API da OpenAI para extrair dados de exames de um texto e formatá-los em JSON.
    """
    prompt = f"""
    Você é um assistente de laboratório altamente preciso. Sua tarefa é extrair todos os exames de sangue e seus respectivos resultados do texto abaixo.
    Formate a saída EXCLUSIVAMENTE como uma lista de objetos JSON. Cada objeto deve conter três chaves: "exame", "valor" e "unidade".
    Não inclua nenhum texto, explicação ou formatação além da lista JSON pura.

    Texto do Exame:
    ---
    {texto_do_exame}
    ---

    JSON:
    """

    print("--- Enviando prompt para o Agente 1 (Estruturador de Dados)... ---")
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em extração de dados de laudos médicos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0 # Baixa temperatura para respostas mais determinísticas
        )
        resposta_modelo = response.choices[0].message.content
        
        # Limpeza para garantir que o texto seja um JSON válido
        json_limpo = resposta_modelo.strip().replace("```json", "").replace("```", "")
        dados_estruturados = json.loads(json_limpo)
        return dados_estruturados
        
    except openai.APIError as e:
        print(f"Erro na API da OpenAI: {e}")
    except json.JSONDecodeError:
        print("Erro: O modelo não retornou um JSON válido.")
        print("Resposta recebida:", resposta_modelo)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        
    return []

# --- Agente 2: Análise e Geração de Resumo ---

def analisar_resultados_e_gerar_resumo(resultados_paciente: list, valores_referencia: dict) -> str:
    """
    Usa a API da OpenAI para comparar resultados de exames com valores de referência
    e gerar um resumo amigável.
    """
    json_resultados_str = json.dumps(resultados_paciente, indent=2, ensure_ascii=False)
    json_referencia_str = json.dumps(valores_referencia, indent=2, ensure_ascii=False)

    prompt = f"""
    Você é um assistente médico que ajuda a interpretar exames. Sua tarefa é criar um resumo simples e direto.
    Compare os "Resultados do Paciente" com os "Valores de Referência".
    Em seu resumo, liste APENAS os exames cujos valores estão FORA do intervalo de referência (abaixo do mínimo ou acima do máximo).
    Para cada exame fora do padrão, informe o nome do exame, o valor encontrado pelo paciente e o intervalo de referência correto.
    Se todos os exames estiverem dentro do normal, apenas diga: "Todos os resultados analisados estão dentro dos valores de referência.".
    Seja claro, conciso e use uma linguagem amigável. Não forneça diagnósticos ou conselhos médicos.

    Resultados do Paciente:
    ```json
    {json_resultados_str}
    ```

    Valores de Referência:
    ```json
    {json_referencia_str}
    ```

    Resumo da Análise:
    """
    
    print("--- Enviando prompt para o Agente 2 (Analisador de Resultados)... ---")
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em interpretar e resumir resultados de exames médicos de forma clara para leigos."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        print(f"Erro na API da OpenAI: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    
    return "Não foi possível gerar o resumo da análise."

# --- Orquestrador Principal ---

def main():
    """
    Função principal que orquestra todo o fluxo de trabalho.
    """
    # Arquivos de entrada
    caminho_pdf_exame = "Exame.pdf"
    caminho_referencia = "valores_referencia.json"
    
    # 1. Configurar a API
    if not configurar_api():
        return

    # 2. Extrair texto do PDF
    print(f"\n[PASSO 1/3] Extraindo texto do arquivo '{caminho_pdf_exame}'...")
    texto_exame = extrair_texto_de_pdf(caminho_pdf_exame)
    if not texto_exame:
        print("Processo interrompido devido a falha na leitura do PDF.")
        return
    print("Texto extraído com sucesso.")

    # 3. Estruturar os dados com o Agente 1
    print("\n[PASSO 2/3] Estruturando os dados do exame...")
    dados_estruturados = estruturar_dados_do_exame(texto_exame)
    if not dados_estruturados:
        print("Processo interrompido devido a falha na estruturação dos dados.")
        return
    print("Dados estruturados com sucesso!")
    print(json.dumps(dados_estruturados, indent=2, ensure_ascii=False))

    # 4. Analisar os resultados com o Agente 2
    print("\n[PASSO 3/3] Analisando os resultados...")
    try:
        with open(caminho_referencia, "r", encoding="utf-8") as f:
            valores_referencia = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo de referência '{caminho_referencia}' não encontrado.")
        return
    except json.JSONDecodeError:
        print(f"Erro: O arquivo de referência '{caminho_referencia}' não é um JSON válido.")
        return

    resumo_final = analisar_resultados_e_gerar_resumo(dados_estruturados, valores_referencia)
    
    # 5. Exibir o resultado final
    print("\n" + "="*50)
    print("           R E S U M O   D O S   E X A M E S")
    print("="*50)
    print(resumo_final)
    print("\n" + "="*50)
    print("\n--- ATENÇÃO ---")
    print("Este resumo é gerado por IA e serve apenas para facilitar a visualização dos resultados.")
    print("Procure sempre seu médico para um diagnóstico e orientação profissional.")
    print("="*50)


if __name__ == "__main__":
    main()