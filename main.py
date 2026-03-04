import os
import json
import time
from src.generator import GeradorConteudo

def limpar_tela():
    """Limpa o terminal para manter a interface limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho(aluno_atual, topico_atual):
    print("="*50)
    print("🎓 AI ADAPTIVE TUTOR - Motor de Engenharia de Prompt 🎓")
    print("="*50)
    print(f"👤 Aluno Atual: {aluno_atual if aluno_atual else 'Nenhum selecionado'}")
    print(f"📚 Tópico Atual: {topico_atual if topico_atual else 'Nenhum definido'}")
    print("="*50)

def main():
    gerador = GeradorConteudo()
    
    # Estado da aplicação
    aluno_id = None
    nome_aluno = None
    topico = None

    while True:
        limpar_tela()
        exibir_cabecalho(nome_aluno, topico)
        
        print("1. 👥 Selecionar Aluno (Perfil)")
        print("2. ✏️  Definir Tópico de Estudo")
        print("3. 🚀 Gerar Conteúdo Específico (v2 Avançado)")
        print("4. 📦 Gerar Material Completo (Todos os 4 tipos)")
        print("5. ⚖️  Comparar Prompts (v1 Básico vs v2 Avançado)")
        print("0. ❌ Sair")
        print("-" * 50)
        
        opcao = input("Escolha uma opção: ")

        if opcao == '0':
            print("Encerrando o AI Adaptive Tutor. Até logo!")
            break
            
        elif opcao == '1':
            print("\nPerfis Disponíveis:")
            for perfil in gerador.perfis:
                print(f"- [{perfil['id']}] {perfil['nome']} ({perfil['idade']} anos, Nível: {perfil['nivel']}, Estilo: {perfil['estilo_aprendizado']})")
            
            escolha_id = input("\nDigite o ID do aluno (ex: aluno_01): ")
            try:
                perfil_escolhido = gerador._obter_perfil(escolha_id)
                aluno_id = perfil_escolhido['id']
                nome_aluno = perfil_escolhido['nome']
                print(f"\n✅ Aluno {nome_aluno} selecionado com sucesso!")
            except ValueError:
                print("\n❌ ID inválido. Tente novamente.")
            input("\nPressione ENTER para continuar...")

        elif opcao == '2':
            novo_topico = input("\nDigite o tópico que deseja ensinar (ex: 'Fotossíntese', 'Física Quântica', 'Revolução Francesa'): ")
            if novo_topico.strip():
                topico = novo_topico
                print(f"\n✅ Tópico '{topico}' definido com sucesso!")
            else:
                print("\n❌ O tópico não pode ser vazio.")
            input("\nPressione ENTER para continuar...")

        elif opcao in ['3', '4', '5']:
            if not aluno_id or not topico:
                print("\n⚠️  AVISO: Você precisa selecionar um aluno e definir um tópico primeiro (Opções 1 e 2).")
                input("\nPressione ENTER para continuar...")
                continue
                
            tipos_disponiveis = ["explicacao", "exemplos", "perguntas", "resumo_visual"]
            
            if opcao == '3' or opcao == '5':
                print("\nTipos de Conteúdo:")
                for i, tipo in enumerate(tipos_disponiveis, 1):
                    print(f"{i}. {tipo.capitalize()}")
                
                escolha_tipo = input(f"\nEscolha o tipo (1-4): ")
                try:
                    tipo_selecionado = tipos_disponiveis[int(escolha_tipo) - 1]
                except (ValueError, IndexError):
                    print("\n❌ Opção inválida.")
                    input("\nPressione ENTER para continuar...")
                    continue
                
                print("\n⏳ Gerando conteúdo via IA (Isso pode levar alguns segundos)...")
                
                if opcao == '3':
                    # Gera usando v2_avancado
                    arquivo_salvo, _ = gerador.gerar(aluno_id, topico, tipo_selecionado, "v2_avancado")
                    if arquivo_salvo:
                        print(f"\n✅ Sucesso! Conteúdo salvo em: {arquivo_salvo}")
                else: # opcao == '5'
                    # Compara v1 e v2
                    arquivo_salvo, _ = gerador.comparar_prompts(aluno_id, topico, tipo_selecionado)
                    if arquivo_salvo:
                        print(f"\n✅ Comparação concluída! Resultado salvo em: {arquivo_salvo}")
                
                input("\nPressione ENTER para continuar...")
                
            elif opcao == '4':
                print("\n⏳ Gerando Material Completo (4 chamadas à API, aguarde)...")
                arquivos_gerados = []
                for tipo in tipos_disponiveis:
                    print(f"   - Gerando {tipo}...")
                    arquivo, _ = gerador.gerar(aluno_id, topico, tipo, "v2_avancado")
                    if arquivo:
                        arquivos_gerados.append(arquivo)

                    # Tempo de espera para evitar sobrecarga na API
                    if tipo != tipos_disponiveis[-1]:
                        time.sleep(15)

                if arquivos_gerados:    
                    print("\n✅ Sucesso! Todos os materiais foram gerados e salvos:")
                    for arq in arquivos_gerados:
                        print(f"   📂 {arq}")
                else:
                    print("\n❌ Ocorreu um erro ao gerar os materiais.")
                
                input("\nPressione ENTER para continuar...")

        else:
            print("\n❌ Opção inválida. Escolha um número do menu.")
            input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()