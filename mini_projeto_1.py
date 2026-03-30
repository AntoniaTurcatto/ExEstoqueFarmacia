from enum import Enum
from datetime import date, datetime
from typing import Callable, Any, Optional

class No:
  def __init__(self, valor):
    self.valor = valor
    self.proximo = None

  def mostrar_no(self):
    print(self.valor)

  def valorStr(self) -> str:
    return str(self.valor)

class ListaEncadeada:
  """
  Lista encadeada simples com nós encadeados por referência direta.

  Attributes:
      primeiro (No | None): Referência ao nó cabeça da lista.
      count (int): Número de elementos presentes na lista.
  """
  def __init__(self):
    self.primeiro = None
    self.count = 0

  def __eq__(self, other: "ListaEncadeada") -> bool:
    """
    Compara duas listas por igualdade estrutural e de valores.

    A comparação percorre os nós em ordem, verificando `valor` par a par.
    Retorna `NotImplemented` se `other` não for instância da mesma classe.

    Args:
        other: Lista a comparar.

    Returns:
        bool: True se ambas tiverem o mesmo tamanho e valores na mesma ordem.
    """
    if not isinstance(other, self.__class__):
        return NotImplemented

    if self.count != other.count:
      return False

    auxSelf = self.primeiro
    auxOther = other.primeiro
    while auxSelf is not None and auxOther is not None:
      if auxSelf.valor != auxOther.valor:
        return False

      auxSelf = auxSelf.proximo
      auxOther = auxOther.proximo

    return True

  def __repr__(self):
    if self.lista_vazia():
      return "[]"

    res = ""
    atual = self.primeiro

    while atual is not None:
      res += str(atual.valor) + "\n"
      atual = atual.proximo

    return res

  def __iter__(self):
    """
    Itera sobre os valores da lista em ordem de inserção.

    Yields:
        Any: Valor de cada nó, do primeiro ao último.
    """
    atual = self.primeiro
    while atual is not None:
      yield atual.valor
      atual = atual.proximo

  def lista_vazia(self):
    return self.primeiro is None

  def mostrar_lista(self):
    if self.lista_vazia():
      print("Lista Vazia!")
      return

    atual = self.primeiro
    while atual is not None:
        print(atual.valor)
        atual = atual.proximo

  def inserir_inicio(self, valor):
    novo = No(valor)
    novo.proximo = self.primeiro
    self.primeiro = novo
    self.count += 1

  def incluir_fim(self, valor):
    novo = No(valor)
    self.count += 1

    if self.lista_vazia():
      self.primeiro = novo
      return

    atual = self.primeiro
    while atual.proximo is not None:
      atual = atual.proximo
    atual.proximo = novo


  def excluir_item(self, valor) -> bool:
    """
    Remove o primeiro nó cujo `valor` satisfaça `==`.

    Args:
        valor: Valor a localizar e remover.

    Returns:
        bool: True se o item foi encontrado e removido, False caso contrário.
    """
    aux = self.primeiro
    ant = None

    while aux is not None:
      if aux.valor == valor:
        if ant is None:
          self.primeiro = aux.proximo
        else:
          ant.proximo = aux.proximo
        self.count -= 1
        return True
      ant = aux
      aux = aux.proximo
    return False


  def pesquisar(self, valor):
    """
    Busca linear pelo primeiro nó com `valor == valor`.

    Args:
        valor: Valor a localizar.

    Returns:
        Any | None: O valor do nó encontrado, ou None se ausente ou lista vazia.
    """
    if self.lista_vazia():
        return None
    atual = self.primeiro
    while atual is not None:
        if atual.valor == valor:
            return atual.valor
        atual = atual.proximo
    return None

Tarja = Enum('Tarja', [
    ('SEM', 0),
    ('VERMELHA', 1),
    ('PRETA', 2),
    ('AMARELA', 3)])

class CondicaoClinica:
  def __init__(self, nome: str, cid: int):
    self.nome = nome
    self.cid = cid

  def __repr__(self):
    return f'Condicao clinica[nome: {self.nome}, CID: {self.cid}]'

class Medicamento:
  def __init__(self, princAtivo, nomeFant, tarja):
    self.princAtivo = princAtivo
    self.nomeFantasia = nomeFant
    self.tarja = tarja
    self.condicoesTratadas = ListaEncadeada()

  def __eq__(self, other) -> bool:
    if not isinstance(other, self.__class__):
        return NotImplemented
    return (self.princAtivo == other.princAtivo and
            self.nomeFantasia.upper() == other.nomeFantasia.upper() and
            self.tarja == other.tarja and
            self.condicoesTratadas == other.condicoesTratadas)

  def __repr__(self):
    return f'Medicamento: \nprincipio ativo: {self.princAtivo}, \nnome fantasia: {self.nomeFantasia}, \ntarja: {self.tarja}, condicoes tratadas: {self.condicoesTratadas}'

class ItemEstoque[T]:
  """
  Item do estoque
  um wrapper para adicionar valor e data de validade a qualquer tipo
  """
  def __init__(self, item: T, valor, dataVal):
    self.itemDetalhes: T = item
    self.itemValor = valor
    self.itemDataValidade = dataVal

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented

    return (self.itemDetalhes == other.itemDetalhes and
            self.itemValor == other.itemValor and
            self.itemDataValidade == other.itemDataValidade)

  def __repr__(self) -> str:
    return (
        f"{self.itemDetalhes!r}"
        f"Preço: R$ {self.itemValor:.2f}\n"
        f"Validade: {self.itemDataValidade.strftime("%d/%m/%Y")}\n"
        f"{'-'*30}"
    )

class Estoque[T]:
  """
  Classe para reunir os itens no estoque
  valores adicionados são envoltos em um ItemEstoque[T]
  """
  def __init__(self):
    self.itens = ListaEncadeada()

  def __repr__(self) -> str:
    return f'Estoque: \n{self.itens}'

  def addItem(self, item: T, valor: float, dataVal: date) -> None:
    """
    Args:
      item: T (item a a adicionar, será encapsulado em um ItemEstoque[T])
      valor: float (valor do item)
      dataVal: date (data de validade)
    returns:
      None
    """
    novoItem = ItemEstoque(item, valor, dataVal)
    self.itens.incluir_fim(novoItem)

  def pesquisar(self, comparador: Callable[[ItemEstoque[T]], bool]) -> Optional[ItemEstoque[T]]:
    """
    Args:
      comparador: Callable[[ItemEstoque[T]], bool]
    returns:
      Optional[ItemEstoque[T]]
    """
    for itemEst in self.itens:
      if comparador(itemEst):
        return itemEst
    return None

  def excluir(self, comparador: Callable[[ItemEstoque[T]], bool]) -> bool:
    """
    Args:
      comparador: Callable[[ItemEstoque[T]], bool]
    returns:
      True Se a exclusão foi bem sucedida
    """
    for itemEst in self.itens:
      if comparador(itemEst):
        return self.itens.excluir_item(itemEst)
    return False

def intInput(texto) -> int:
  try:
    return int(input(texto))
  except:
    print("Digite um número válido!")
    return intInput(texto)

def floatFromLocalized(texto) -> float:
  try:
    return float(input(texto))
  except:
    print("Inválido. Não deve haver separador milhar e o decimal deve ser '.'")
    return floatFromLocalized(texto)

def dateFromStr(txtDisplay, fmt) -> date:
  try:
    entrada = input(txtDisplay).strip()#remove caracteres invalidos
    return datetime.strptime(entrada, fmt).date()
  except:
    print("Inválido")
    return dateFromStr(txtDisplay, fmt)

def inputStrOpc(text: str, opcs: list[str]) -> str:
  opc = input(text).lower()
  if opc in map(lambda x: x.lower(), opcs):
    return opc

  print("Opção inválida")
  return inputStrOpc(text, opcs)

def menuPrincipal() -> Callable[[Any], None] | None:
  """
  Exibe o menu principal e retorna a função correspondente à opção escolhida.

  Fica pedindo uma opção até o usuário digitar um número válido.
  Se o usuário escolher sair (0), retorna None — isso é o sinal para
  o programa encerrar o loop principal.

  Exemplo de uso:
      acao = menuPrincipal()
      if acao is not None:
          acao(estoque)

  Returns:
      Callable: A função que executa a ação escolhida, recebendo o estoque como argumento.
      None: Se o usuário escolher a opção 0 (Sair).
  """
  print("\n============= MENU =============\n")
  print("1 - Inserir Medicamento (Início)")
  print("2 - Mostrar Estoque")
  print("3 - Excluir Registro")
  print("4 - Pesquisar Medicamento")
  print("0 - Sair")

  while True:
    match intInput("Escolha: "):
      case 1:
        return cadastroMed
      case 2:
        return print
      case 3:
        return excluirItem
      case 4:
        return pesquisar
      case 0:
        return None
      case _:
        print("Opção inválida")

def createTarjaLoop() -> Tarja:
  print("Tarja: 0 - SEM | 1 - VERMELHA | 2 - PRETA | 3 - AMARELA")
  try:
    return Tarja(intInput("Escolha: "))
  except:
    print("Valor inválido")
    return createTarjaLoop()

def ObterListaCondClinica() -> ListaEncadeada:
  condscli = ListaEncadeada()
  while True:
    add = inputStrOpc("Adcionar condição clínica? (s/n): ", ["s", "n"])
    if add != 's':
      break

    nomeCond = input("Nome da condição: ")
    cid = intInput("CID: ")
    cond = CondicaoClinica(nomeCond, cid)

    condscli.incluir_fim(cond)

  return condscli

def cadastroMed(estoque):
  princ = input("Princípio Ativo: ")
  nome  = input("Nome Fantasia: ")
  tarja = createTarjaLoop()
  med   = Medicamento(princ, nome, tarja)
  med.condicoesTratadas = ObterListaCondClinica()

  valor = floatFromLocalized("Preço: ")
  validade = dateFromStr("Digite a validade (DD/MM/AAAA): ", "%d/%m/%Y")

  estoque.addItem(med, valor, validade)

  print("Medicamento inserido com sucesso!")

def excluirItem(estoque):
  nome = input("Nome do medicamento que deseja excluir: ")
  if estoque.excluir(lambda item: item.itemDetalhes.nomeFantasia == nome):
    print("Excluido")
  else:
    print("Não foi possível excluir: medicamento não encontrado")

def pesquisar(estoque):
  nome = input("Digite o nome do medicamento que deseja encontrar: ")
  medicamento = estoque.pesquisar(lambda item: item.itemDetalhes.nomeFantasia == nome)
  match medicamento:
    case None:
      print("Medicamento não encontrado")
    case _:
      print(medicamento)

def main():
  estoque = Estoque[Medicamento]()
  while True:
    executor = menuPrincipal()
    if executor is None:
      print("Encerrando...")
      break

    executor(estoque)

if __name__ = "__main__":
    main()

