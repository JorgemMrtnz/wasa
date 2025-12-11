import tkinter as tk
from tkinter import messagebox
import chess
import random

class AjedrezApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Ajedrez Python")
        self.root.geometry("850x600") # Ventana un poco más grande
        
        # Configuración de colores y recursos
        self.color_claro = "#F0D9B5"
        self.color_oscuro = "#B58863"
        self.color_resaltado = "#6A9955"
        self.pieces = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
        }
        
        # Estado del juego
        self.modo_juego = None # 'PVP' o 'CPU'
        self.buttons = {}
        self.selected_square = None
        
        # Iniciar mostrando el menú
        self.mostrar_menu()

    def mostrar_menu(self):
        # Limpiar la ventana (borrar el juego anterior si existe)
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Crear frame del menú
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(expand=True)
        
        titulo = tk.Label(menu_frame, text="♞ Ajedrez Python ♜", font=("Helvetica", 30, "bold"))
        titulo.pack(pady=20)
        
        btn_pvp = tk.Button(menu_frame, text="Jugador vs Jugador", font=("Arial", 16), 
                            width=20, bg="#dddddd", command=lambda: self.iniciar_juego("PVP"))
        btn_pvp.pack(pady=10)
        
        btn_cpu = tk.Button(menu_frame, text="Jugador vs IA", font=("Arial", 16), 
                            width=20, bg="#dddddd", command=lambda: self.iniciar_juego("CPU"))
        btn_cpu.pack(pady=10)
        
        footer = tk.Label(menu_frame, text="Selecciona un modo para comenzar", font=("Arial", 10))
        footer.pack(pady=30)

    def iniciar_juego(self, modo):
        self.modo_juego = modo
        self.board = chess.Board() # Tablero nuevo
        self.selected_square = None
        self.juego_terminado = False
        
        # Limpiar menú
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # --- Layout Principal del Juego ---
        main_layout = tk.Frame(self.root)
        main_layout.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Panel Izquierdo: Tablero
        self.board_frame = tk.Frame(main_layout)
        self.board_frame.pack(side=tk.LEFT)
        
        # Panel Derecho: Info, Historial y Botón Volver
        self.info_frame = tk.Frame(main_layout, width=250)
        self.info_frame.pack(side=tk.RIGHT, fill="y", padx=20)
        
        # Botón para volver al menú
        btn_volver = tk.Button(self.info_frame, text="< Volver al Menú", 
                               command=self.mostrar_menu, bg="#ffcccc")
        btn_volver.pack(fill="x", pady=5)
        
        # Etiqueta de Modo
        lbl_modo = tk.Label(self.info_frame, text=f"Modo: {modo}", font=("Arial", 12, "bold"))
        lbl_modo.pack(pady=10)
        
        # Historial
        tk.Label(self.info_frame, text="Historial de Movimientos:").pack(anchor="w")
        self.history_text = tk.Text(self.info_frame, width=25, height=20, state='disabled')
        self.history_text.pack(pady=5)
        
        # Estado
        self.status_label = tk.Label(self.info_frame, text="Turno: Blancas", font=("Arial", 11), fg="blue")
        self.status_label.pack(pady=10)
        
        self.crear_casillas()
        self.actualizar_tablero()

    def crear_casillas(self):
        self.buttons = {}
        for fila in range(8):
            for col in range(8):
                idx = chess.square(col, 7 - fila)
                btn = tk.Button(self.board_frame, text="", font=("Arial", 28), width=2, height=1,
                                command=lambda s=idx: self.on_click(s))
                btn.grid(row=fila, column=col)
                self.buttons[idx] = btn

    def actualizar_tablero(self):
        # 1. Actualizar piezas y colores
        for idx in range(64):
            piece = self.board.piece_at(idx)
            btn = self.buttons[idx]
            
            # Texto (Pieza)
            btn.config(text=self.pieces[piece.symbol()] if piece else "")
            
            # Color de fondo (Tablero vs Selección)
            fila = 7 - chess.square_rank(idx)
            col = chess.square_file(idx)
            color_base = self.color_claro if (fila + col) % 2 == 0 else self.color_oscuro
            
            if self.selected_square == idx:
                btn.config(bg=self.color_resaltado)
            else:
                btn.config(bg=color_base)
        
        # 2. Actualizar texto de estado
        if self.juego_terminado:
            return

        turno_txt = "Blancas" if self.board.turn == chess.WHITE else "Negras"
        self.status_label.config(text=f"Turno: {turno_txt}")

    def agregar_historial(self, move_san):
        n_jugada = self.board.fullmove_number
        if self.board.turn == chess.BLACK: # Blancas acaban de mover
            txt = f"{n_jugada}. {move_san} "
        else: # Negras acaban de mover
            txt = f"{move_san}\n"
            
        self.history_text.config(state='normal')
        self.history_text.insert(tk.END, txt)
        self.history_text.see(tk.END)
        self.history_text.config(state='disabled')

    def on_click(self, square):
        if self.juego_terminado: return
        
        # Si es turno de la CPU, no dejar que el humano haga clic
        if self.modo_juego == "CPU" and self.board.turn == chess.BLACK:
            return

        if self.selected_square is None:
            # Seleccionar pieza
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.actualizar_tablero()
        else:
            # Mover pieza
            if square == self.selected_square:
                self.selected_square = None # Deseleccionar
            else:
                move = chess.Move(self.selected_square, square)
                
                # Promoción simple a Reina
                if self.es_promocion(move):
                    move.promotion = chess.QUEEN
                
                if move in self.board.legal_moves:
                    self.ejecutar_movimiento(move)
                    
                    # Si es contra la IA y el juego no acabó, activar IA
                    if self.modo_juego == "CPU" and not self.juego_terminado:
                        self.root.after(500, self.movimiento_ia)
                else:
                    # Si clic es inválido pero es otra pieza propia, cambiar selección
                    piece = self.board.piece_at(square)
                    if piece and piece.color == self.board.turn:
                        self.selected_square = square
                    else:
                        self.selected_square = None
                        messagebox.showwarning("Error", "Movimiento ilegal")
            
            self.actualizar_tablero()

    def ejecutar_movimiento(self, move):
        san = self.board.san(move)
        self.board.push(move)
        self.agregar_historial(san)
        self.selected_square = None
        self.actualizar_tablero()
        self.verificar_fin()

    def movimiento_ia(self):
        if self.juego_terminado: return
        
        self.status_label.config(text="Pensando...")
        
        # IA: Busca captura o mueve random
        moves = list(self.board.legal_moves)
        mejor_move = None
        
        # Buscar captura
        for m in moves:
            if self.board.is_capture(m):
                mejor_move = m
                break
        
        if not mejor_move:
            mejor_move = random.choice(moves)
            
        self.ejecutar_movimiento(mejor_move)

    def es_promocion(self, move):
        p = self.board.piece_at(move.from_square)
        if p.piece_type == chess.PAWN:
            rank = chess.square_rank(move.to_square)
            if (p.color == chess.WHITE and rank == 7) or (p.color == chess.BLACK and rank == 0):
                return True
        return False

    def verificar_fin(self):
        if self.board.is_game_over():
            self.juego_terminado = True
            res = self.board.result()
            winner = "Nadie"
            if self.board.is_checkmate():
                winner = "Negras" if self.board.turn == chess.WHITE else "Blancas"
                msg = f"¡Jaque Mate! Ganan: {winner}"
            else:
                msg = "Juego terminado (Tablas)"
            
            messagebox.showinfo("Fin", f"{msg}\nResultado: {res}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AjedrezApp(root)
    root.mainloop()