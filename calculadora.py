import tkinter as tk
import ast
import operator
import math
import json
import os

# ======================================================
# OPERADORES SEGUROS
# ======================================================

operadores = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg
}

# ======================================================
# HISTÓRICO
# ======================================================

ARQUIVO_HISTORICO = "historico.json"

historico = []

if os.path.exists(ARQUIVO_HISTORICO):
    try:
        with open(ARQUIVO_HISTORICO, "r") as arquivo:
            historico = json.load(arquivo)
    except:
        historico = []


def salvar_historico():
    with open(ARQUIVO_HISTORICO, "w") as arquivo:
        json.dump(historico, arquivo, indent=4)


# ======================================================
# PARSER MATEMÁTICO SEGURO
# ======================================================

def calcular_seguro(expressao):

    def avaliar(node):

        if isinstance(node, ast.Constant):
            return node.value

        elif isinstance(node, ast.BinOp):

            operador = operadores.get(type(node.op))

            if operador is None:
                raise TypeError("Operador inválido")

            return operador(
                avaliar(node.left),
                avaliar(node.right)
            )

        elif isinstance(node, ast.UnaryOp):

            operador = operadores.get(type(node.op))

            if operador is None:
                raise TypeError("Operador inválido")

            return operador(
                avaliar(node.operand)
            )

        else:
            raise TypeError("Expressão inválida")

    arvore = ast.parse(expressao, mode='eval')

    return avaliar(arvore.body)


# ======================================================
# FUNÇÕES
# ======================================================

expressao_atual = ""


def atualizar_display(texto):
    display_expressao.config(text=texto)


def atualizar_resultado(texto):
    display_resultado.config(text=texto)


def clicar(valor):
    global expressao_atual

    expressao_atual += str(valor)
    atualizar_display(expressao_atual)


def limpar():
    global expressao_atual

    expressao_atual = ""
    atualizar_display("")
    atualizar_resultado("0")


def apagar():
    global expressao_atual

    expressao_atual = expressao_atual[:-1]
    atualizar_display(expressao_atual)


def porcentagem():
    global expressao_atual

    try:
        valor = calcular_seguro(expressao_atual)
        resultado = valor / 100

        expressao_atual = str(resultado)

        atualizar_display(expressao_atual)
        atualizar_resultado(resultado)

    except:
        atualizar_resultado("Erro")


def raiz():
    global expressao_atual

    try:
        valor = calcular_seguro(expressao_atual)
        resultado = math.sqrt(valor)

        expressao_atual = str(resultado)

        atualizar_display(expressao_atual)
        atualizar_resultado(resultado)

    except:
        atualizar_resultado("Erro")


def quadrado():
    global expressao_atual

    try:
        valor = calcular_seguro(expressao_atual)
        resultado = valor ** 2

        expressao_atual = str(resultado)

        atualizar_display(expressao_atual)
        atualizar_resultado(resultado)

    except:
        atualizar_resultado("Erro")


# ======================================================
# ANIMAÇÃO
# ======================================================

def animar_resultado():
    tamanho_original = 28

    for tamanho in [34, 32, 30, 28]:
        display_resultado.config(font=("Segoe UI", tamanho, "bold"))
        window.update()
        window.after(40)


# ======================================================
# CALCULAR
# ======================================================

def calcular():
    global expressao_atual

    try:

        resultado = calcular_seguro(expressao_atual)

        atualizar_resultado(resultado)

        historico.append({
            "expressao": expressao_atual,
            "resultado": resultado
        })

        salvar_historico()

        animar_resultado()

        expressao_atual = str(resultado)

    except ZeroDivisionError:
        atualizar_resultado("Erro")

    except:
        atualizar_resultado("Inválido")


# ======================================================
# HISTÓRICO VISUAL
# ======================================================

def mostrar_historico():

    janela = tk.Toplevel(window)

    janela.title("Histórico")
    janela.geometry("300x400")
    janela.configure(bg="#1e1e1e")

    titulo = tk.Label(
        janela,
        text="Histórico",
        bg="#1e1e1e",
        fg="white",
        font=("Segoe UI", 18, "bold")
    )

    titulo.pack(pady=10)

    frame = tk.Frame(janela, bg="#1e1e1e")
    frame.pack(fill="both", expand=True)

    for item in reversed(historico):

        texto = f'{item["expressao"]} = {item["resultado"]}'

        label = tk.Label(
            frame,
            text=texto,
            bg="#2d2d2d",
            fg="white",
            anchor="w",
            padx=10,
            pady=8,
            font=("Consolas", 12)
        )

        label.pack(fill="x", pady=2, padx=5)


# ======================================================
# JANELA
# ======================================================

window = tk.Tk()

window.title("Calculadora Científica")
window.geometry("420x700")
window.configure(bg="#1e1e1e")
window.resizable(False, False)

# ======================================================
# DISPLAY CUSTOMIZADO
# ======================================================

display_frame = tk.Frame(
    window,
    bg="#252526",
    height=150
)

display_frame.pack(fill="x", padx=10, pady=10)

display_expressao = tk.Label(
    display_frame,
    text="",
    anchor="e",
    bg="#252526",
    fg="#aaaaaa",
    padx=15,
    pady=20,
    font=("Segoe UI", 18)
)

display_expressao.pack(fill="x")

display_resultado = tk.Label(
    display_frame,
    text="0",
    anchor="e",
    bg="#252526",
    fg="white",
    padx=15,
    pady=10,
    font=("Segoe UI", 28, "bold")
)

display_resultado.pack(fill="x")

# ======================================================
# FRAME BOTÕES
# ======================================================

frame_botoes = tk.Frame(window, bg="#1e1e1e")
frame_botoes.pack(expand=True, fill="both", padx=10, pady=10)

# ======================================================
# ESTILO
# ======================================================

COR_BOTAO = "#333333"
COR_OPERADOR = "#ff9500"
COR_ESPECIAL = "#5050aa"
COR_HOVER = "#4d4d4d"

# ======================================================
# BOTÕES
# ======================================================

botoes = [
    ("Hist", 0, 0),
    ("√", 0, 1),
    ("x²", 0, 2),
    ("%", 0, 3),

    ("C", 1, 0),
    ("⌫", 1, 1),
    ("(", 1, 2),
    (")", 1, 3),

    ("7", 2, 0),
    ("8", 2, 1),
    ("9", 2, 2),
    ("/", 2, 3),

    ("4", 3, 0),
    ("5", 3, 1),
    ("6", 3, 2),
    ("*", 3, 3),

    ("1", 4, 0),
    ("2", 4, 1),
    ("3", 4, 2),
    ("-", 4, 3),

    ("0", 5, 0),
    (".", 5, 1),
    ("=", 5, 2),
    ("+", 5, 3),
]

# ======================================================
# HOVER
# ======================================================

def hover_entrar(e):
    e.widget["bg"] = COR_HOVER


def hover_sair(e):

    texto = e.widget["text"]

    if texto in ["+", "-", "*", "/", "="]:
        cor = COR_OPERADOR

    elif texto in ["√", "x²", "%", "Hist"]:
        cor = COR_ESPECIAL

    else:
        cor = COR_BOTAO

    e.widget["bg"] = cor


# ======================================================
# CRIAÇÃO DOS BOTÕES
# ======================================================

for (texto, linha, coluna) in botoes:

    if texto == "=":
        comando = calcular

    elif texto == "C":
        comando = limpar

    elif texto == "⌫":
        comando = apagar

    elif texto == "√":
        comando = raiz

    elif texto == "x²":
        comando = quadrado

    elif texto == "%":
        comando = porcentagem

    elif texto == "Hist":
        comando = mostrar_historico

    else:
        comando = lambda t=texto: clicar(t)

    if texto in ["+", "-", "*", "/", "="]:
        cor = COR_OPERADOR

    elif texto in ["√", "x²", "%", "Hist"]:
        cor = COR_ESPECIAL

    else:
        cor = COR_BOTAO

    botao = tk.Button(
        frame_botoes,
        text=texto,
        command=comando,
        font=("Segoe UI", 16, "bold"),
        bg=cor,
        fg="white",
        bd=0,
        relief="flat",
        cursor="hand2",
        activebackground=COR_HOVER,
        activeforeground="white"
    )

    botao.grid(
        row=linha,
        column=coluna,
        sticky="nsew",
        padx=6,
        pady=6,
        ipadx=10,
        ipady=20
    )

    botao.bind("<Enter>", hover_entrar)
    botao.bind("<Leave>", hover_sair)

# ======================================================
# RESPONSIVIDADE
# ======================================================

for i in range(6):
    frame_botoes.grid_rowconfigure(i, weight=1)

for i in range(4):
    frame_botoes.grid_columnconfigure(i, weight=1)

# ======================================================
# TECLADO
# ======================================================

def teclado(event):

    tecla = event.keysym

    if tecla in "0123456789":
        clicar(tecla)

    elif tecla in ["plus", "KP_Add"]:
        clicar("+")

    elif tecla in ["minus", "KP_Subtract"]:
        clicar("-")

    elif tecla in ["asterisk", "KP_Multiply"]:
        clicar("*")

    elif tecla in ["slash", "KP_Divide"]:
        clicar("/")

    elif tecla == "period":
        clicar(".")

    elif tecla == "parenleft":
        clicar("(")

    elif tecla == "parenright":
        clicar(")")

    elif tecla == "percent":
        clicar("%")

    elif tecla == "Return":
        calcular()

    elif tecla == "BackSpace":
        apagar()

    elif tecla == "Escape":
        limpar()

window.bind("<Key>", teclado)

# ======================================================
# LOOP
# ======================================================

window.mainloop()