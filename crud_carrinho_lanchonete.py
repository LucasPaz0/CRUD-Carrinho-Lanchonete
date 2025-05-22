from prometheus_client import start_http_server, Counter, Gauge
import threading

class Produto:
    def __init__(self, id, nome, preco):
        self.id = id
        self.nome = nome
        self.preco = preco

class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_produto(self, produto):
        self.itens.append(produto)
        produtos_adicionados.inc()
        itens_no_carrinho.set(len(self.itens))
        print(f"Produto '{produto.nome}' adicionado ao carrinho.")

    def remover_produto(self, id_produto):
        for produto in self.itens:
            if produto.id == id_produto:
                self.itens.remove(produto)
                produtos_removidos.inc()
                itens_no_carrinho.set(len(self.itens))
                print(f"Produto '{produto.nome}' removido do carrinho.")
                return
        print("Produto não encontrado no carrinho.")

    def listar_carrinho(self):
        if not self.itens:
            print("Carrinho vazio.")
            return
        print("Itens no carrinho:")
        total = 0
        for produto in self.itens:
            print(f"- {produto.nome} | R$ {produto.preco:.2f}")
            total += produto.preco
        print(f"Total: R$ {total:.2f}")

    def limpar_carrinho(self):
        self.itens.clear()
        carrinho_limpo.inc()
        itens_no_carrinho.set(0)
        print("Carrinho esvaziado.")

# Métricas Prometheus
produtos_adicionados = Counter('produtos_adicionados_total', 'Total de produtos adicionados ao carrinho')
produtos_removidos = Counter('produtos_removidos_total', 'Total de produtos removidos do carrinho')
carrinho_limpo = Counter('carrinho_limpo_total', 'Total de vezes que o carrinho foi esvaziado')
itens_no_carrinho = Gauge('total_itens_no_carrinho', 'Quantidade atual de itens no carrinho')

def iniciar_monitoramento():
    start_http_server(8000)

def iniciar_aplicacao():
    # Cardápio fixo para a lanchonete
    cardapio = [
        Produto(1, "Hambúrguer", 12.50),
        Produto(2, "Batata Frita", 7.00),
        Produto(3, "Refrigerante", 5.00),
        Produto(4, "Milkshake", 10.00)
    ]

    def exibir_cardapio():
        print("\nCardápio:")
        for produto in cardapio:
            print(f"{produto.id} - {produto.nome} | R$ {produto.preco:.2f}")

    carrinho = Carrinho()
    while True:
        print("""
========= MENU =========
1. Ver Cardápio
2. Adicionar Produto ao Carrinho
3. Remover Produto do Carrinho
4. Ver Carrinho
5. Limpar Carrinho
6. Sair
========================
""")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exibir_cardapio()

        elif opcao == "2":
            exibir_cardapio()
            try:
                id_produto = int(input("Informe o ID do produto para adicionar: "))
                produto = next((p for p in cardapio if p.id == id_produto), None)
                if produto:
                    carrinho.adicionar_produto(produto)
                else:
                    print("Produto não encontrado.")
            except ValueError:
                print("Entrada inválida.")

        elif opcao == "3":
            try:
                id_produto = int(input("Informe o ID do produto para remover: "))
                carrinho.remover_produto(id_produto)
            except ValueError:
                print("Entrada inválida.")

        elif opcao == "4":
            carrinho.listar_carrinho()

        elif opcao == "5":
            carrinho.limpar_carrinho()

        elif opcao == "6":
            print("Saindo... Obrigado por usar nossa lanchonete!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    threading.Thread(target=iniciar_monitoramento, daemon=True).start()
    iniciar_aplicacao()
