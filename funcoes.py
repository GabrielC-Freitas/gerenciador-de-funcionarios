import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Função para adicionar um novo funcionário ao banco de dados
def adicionar_funcionario():
    nome = entry_nome.get()
    cargo = entry_cargo.get()
    salario = entry_salario.get()

    # Verificar se todos os campos foram preenchidos
    if not nome or not cargo or not salario:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")
        return

    # Conectar ao banco de dados ou criar se não existir
    conn = sqlite3.connect('funcionarios.db')
    cursor = conn.cursor()

    # Inserir novo funcionário no banco de dados
    cursor.execute("INSERT INTO funcionarios (nome, cargo, salario) VALUES (?, ?, ?)", (nome, cargo, salario))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso.")
    limpar_campos()
    listar_funcionarios()

# Função para listar todos os funcionários
def listar_funcionarios():
    # Limpar a lista de funcionários antes de atualizar
    listbox_funcionarios.delete(0, tk.END)

    # Conectar ao banco de dados
    conn = sqlite3.connect('funcionarios.db')
    cursor = conn.cursor()

    # Selecionar todos os funcionários
    cursor.execute("SELECT * FROM funcionarios")
    funcionarios = cursor.fetchall()

    # Preencher a lista de funcionários na interface gráfica
    for funcionario in funcionarios:
        listbox_funcionarios.insert(tk.END, f"Nome: {funcionario[1]} | Cargo: {funcionario[2]} | Salário: R$ {funcionario[3]:.2f}")

    conn.close()

# Função para limpar os campos após adicionar um funcionário
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_cargo.delete(0, tk.END)
    entry_salario.delete(0, tk.END)

# Criar a interface gráfica
root = tk.Tk()
root.title("Gerenciador de Funcionários")
root.geometry("400x300")
root.configure(bg='#363636')

frame_adicionar = tk.Frame(root, bg='#363636')
frame_adicionar.pack(pady=10)

label_nome = tk.Label(frame_adicionar, text="Nome:", bg='#363636', fg='white')
label_nome.grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_adicionar, bg='#555555', fg='white')
entry_nome.grid(row=0, column=1, padx=5, pady=5)

label_cargo = tk.Label(frame_adicionar, text="Cargo:", bg='#363636', fg='white')
label_cargo.grid(row=1, column=0, padx=5, pady=5)
entry_cargo = tk.Entry(frame_adicionar, bg='#555555', fg='white')
entry_cargo.grid(row=1, column=1, padx=5, pady=5)

label_salario = tk.Label(frame_adicionar, text="Salário:", bg='#363636', fg='white')
label_salario.grid(row=2, column=0, padx=5, pady=5)
entry_salario = tk.Entry(frame_adicionar, bg='#555555', fg='white')
entry_salario.grid(row=2, column=1, padx=5, pady=5)

button_adicionar = tk.Button(frame_adicionar, text="Adicionar Funcionário", bg='#007BFF', fg='white', command=adicionar_funcionario)
button_adicionar.grid(row=3, column=0, columnspan=2, pady=10)

frame_listar = tk.Frame(root, bg='#363636')
frame_listar.pack(pady=10)

label_listar = tk.Label(frame_listar, text="Funcionários:", bg='#363636', fg='white')
label_listar.grid(row=0, column=0, padx=5, pady=5)

# Adicionando uma barra de rolagem horizontal ao retângulo de funcionários
scrollbar = ttk.Scrollbar(frame_listar, orient=tk.HORIZONTAL)
scrollbar.grid(row=1, column=0, sticky='ew')

listbox_funcionarios = tk.Listbox(frame_listar, xscrollcommand=scrollbar.set, bg='#555555', fg='white')
listbox_funcionarios.grid(row=1, column=0, sticky='ew')

scrollbar.config(command=listbox_funcionarios.xview)

# Criar o banco de dados SQLite para armazenar os funcionários
conn = sqlite3.connect('funcionarios.db')
cursor = conn.cursor()

# Criar tabela de funcionários se não existir
cursor.execute('''CREATE TABLE IF NOT EXISTS funcionarios
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT,
                   cargo TEXT,
                   salario REAL)''')

conn.commit()
conn.close()

# Listar os funcionários ao iniciar o aplicativo
listar_funcionarios()

root.mainloop()
