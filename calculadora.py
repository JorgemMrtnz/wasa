import tkinter as tk
from tkinter import messagebox #en caso de querer usar mensajes emergentes
import sympy#libreria matematica simbolica(le sabe a derivadas y integrales)
import numpy as np#esta maneja los arreglos y funciones matematicas numericas (numeros)
import matplotlib.pyplot as plt #Hace los graficos epicos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
# esta cosa rara es para meter los graficos de matplotlib dentro de tkinter es decir en vez de abrir otro archivo se ve todo en la misma ventana

class CalculadoraDerivadasIntegrales:
    def __init__(self, root):
        self.root = root # root es la ventana principal
        self.root.title("Calculadora de Derivadas e Integrales")
        self.root.geometry("1200x700") # tamaño inicial
        self.root.config(bg="#ECF0F1")

        # DISPOSICIÓN PRINCIPAL
        frame_izq = tk.Frame(root, bg="#2C3E50", width=350)
        frame_izq.pack(side=tk.LEFT, fill=tk.Y)
        
        frame_der = tk.Frame(root, bg="white")
        frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # PANEL IZQUIERDO (Igual que antes)
        tk.Label(frame_izq, text="Panel de Control", bg="#2C3E50", fg="white", 
                 font=("Helvetica", 16, "bold")).pack(pady=15)

        tk.Label(frame_izq, text="Función f(x):", bg="#2C3E50", fg="#BDC3C7").pack(anchor="w", padx=20)
        self.entrada_func = tk.Entry(frame_izq, font=("Arial", 14), justify='center')
        self.entrada_func.pack(pady=5, padx=20, fill=tk.X)
        self.entrada_func.insert(0, "x**3 - 10*x") 

        # Botones Texto
        frame_btns = tk.Frame(frame_izq, bg="#2C3E50")
        frame_btns.pack(pady=10)
        tk.Button(frame_btns, text="Derivada (Texto)", command=self.mostrar_derivada, bg="#E74C3C", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(frame_btns, text="Integral (Texto)", command=self.mostrar_integral, bg="#3498DB", fg="white").grid(row=0, column=1, padx=5)

        tk.Label(frame_izq, text="Resultado:", bg="#2C3E50", fg="#BDC3C7").pack(anchor="w", padx=20, pady=(10,0))
        self.salida_res = tk.Entry(frame_izq, font=("Arial", 11, "bold"), justify='center', readonlybackground="#95a5a6")
        self.salida_res.pack(pady=5, padx=20, fill=tk.X)

        tk.Frame(frame_izq, height=2, bg="#7F8C8D").pack(fill=tk.X, pady=20, padx=10)

        # Configuración Gráfica
        tk.Label(frame_izq, text="Configuración Gráfica", bg="#2C3E50", fg="white", font=("Helvetica", 14, "bold")).pack(pady=5)

        # Área
        lbl_area = tk.Label(frame_izq, text="🟣 Área (Límites X)", bg="#2C3E50", fg="#BB8FCE", font=("bold", 10))
        lbl_area.pack(pady=(10, 5))
        frame_limites = tk.Frame(frame_izq, bg="#2C3E50")
        frame_limites.pack()
        tk.Label(frame_limites, text="Min:", bg="#2C3E50", fg="white").pack(side=tk.LEFT)
        self.entry_a = tk.Entry(frame_limites, width=5)
        self.entry_a.pack(side=tk.LEFT, padx=5)
        self.entry_a.insert(0, "-5")
        tk.Label(frame_limites, text="Max:", bg="#2C3E50", fg="white").pack(side=tk.LEFT)
        self.entry_b = tk.Entry(frame_limites, width=5)
        self.entry_b.pack(side=tk.LEFT, padx=5)
        self.entry_b.insert(0, "5")

        # Tangente
        lbl_tan = tk.Label(frame_izq, text="🔴 Tangente (Punto X)", bg="#2C3E50", fg="#F1948A", font=("bold", 10))
        lbl_tan.pack(pady=(20, 5))
        self.entry_x0 = tk.Entry(frame_izq, width=10, justify='center')
        self.entry_x0.pack()
        self.entry_x0.insert(0, "2")

        # BOTÓN ACTUALIZAR
        tk.Button(frame_izq, text="🔄 GRAFICAR / REINICIAR VISTA", command=self.actualizar_todo, 
                  bg="#27AE60", fg="white", font=("Arial", 12, "bold"), height=2).pack(pady=30, padx=20, fill=tk.X)

        # =================================================
        # PANEL DERECHO (MATPLOTLIB CON TOOLBAR)
        # =================================================
        self.fig = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # 1. El Canvas (El dibujo)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_der)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 2. ### LA BARRA DE HERRAMIENTAS MÁGICA ###
        # Esto añade los botones de Zoom, Pan, Guardar, etc.
        toolbar = NavigationToolbar2Tk(self.canvas, frame_der)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.actualizar_todo()

    # --- LÓGICA SIMBÓLICA (Igual) ---
    def normalizar_entrada(self, texto):
        texto = texto.lower()
        reemplazos = {"sen": "sin", "arcsin": "asin", "arccos": "acos", "arctan": "atan", "^": "**"}
        for viejo, nuevo in reemplazos.items(): texto = texto.replace(viejo, nuevo)
        return texto

    def formatear_salida(self, texto):
        reemplazos = {"**": "^", "*": "·", "asin": "arcsin", "acos": "arccos", "atan": "arctan", "log": "ln", "exp": "e^", "sqrt": "√"}
        for viejo, nuevo in reemplazos.items(): texto = texto.replace(viejo, nuevo)
        return texto

    def obtener_expresion(self):
        txt = self.normalizar_entrada(self.entrada_func.get())
        locales = {"e": sympy.E, "pi": sympy.pi, "ln": sympy.log, "log": lambda x: sympy.log(x, 10)}
        try: return sympy.sympify(txt, locals=locales)
        except: return None

    def mostrar_derivada(self):
        expr = self.obtener_expresion()
        if expr: self.escribir_res(self.formatear_salida(str(sympy.diff(expr, sympy.symbols('x')))))

    def mostrar_integral(self):
        expr = self.obtener_expresion()
        if expr: self.escribir_res(self.formatear_salida(str(sympy.integrate(expr, sympy.symbols('x')))) + " + C")

    def escribir_res(self, texto):
        self.salida_res.config(state='normal')
        self.salida_res.delete(0, tk.END); self.salida_res.insert(0, texto)
        self.salida_res.config(state='readonly')

    # =================================================
    # LÓGICA GRÁFICA MEJORADA
    # =================================================
    def actualizar_todo(self):
        expr = self.obtener_expresion()
        if not expr: return

        x_sym = sympy.symbols('x')
        try: f_num = sympy.lambdify(x_sym, expr, modules=['numpy'])
        except: return

        self.ax.clear()

        # --- MEJORA 1: DETECCIÓN INTELIGENTE DE LÍMITES ---
        try:
            # Usamos los cuadros de texto "Area" como el control del ZOOM X
            x_min = float(self.entry_a.get())
            x_max = float(self.entry_b.get())
            
            # Si el usuario pone el mismo número o están al revés, lo arreglamos
            if x_min >= x_max: x_max = x_min + 10
        except:
            x_min, x_max = -10, 10

        # --- MEJORA 2: RESOLUCIÓN DINÁMICA ---
        # Si el rango es grande (ej: 0 a 1000), necesitamos más puntos.
        # Calculamos puntos basándonos en la distancia. Mínimo 1000 puntos.
        distancia = abs(x_max - x_min)
        num_puntos = int(max(1000, distancia * 50)) 
        
        x_vals = np.linspace(x_min, x_max, num_puntos)
        
        try:
            y_vals = f_num(x_vals)
            if not isinstance(y_vals, np.ndarray): y_vals = np.full_like(x_vals, y_vals)
        except: return

        # Dibujar función
        self.ax.plot(x_vals, y_vals, color='#2980B9', linewidth=2, label='f(x)')

        # Área (Solo dibujamos si tiene sentido)
        mask = (x_vals >= x_min) & (x_vals <= x_max)
        self.ax.fill_between(x_vals, y_vals, where=mask, color='#9B59B6', alpha=0.2)

        # Tangente
        try:
            x0 = float(self.entry_x0.get())
            # Solo dibujamos tangente si está dentro de la vista (opcional, pero queda mejor)
            if x_min <= x0 <= x_max:
                y0 = float(f_num(np.array([x0])))
                diff_expr = sympy.diff(expr, x_sym)
                f_prime = sympy.lambdify(x_sym, diff_expr, modules=['numpy'])
                m = float(f_prime(np.array([x0])))
                
                # Tangente larga que cubra la pantalla
                delta = (x_max - x_min) * 0.5
                x_tan = np.linspace(x0 - delta, x0 + delta, 100)
                y_tan = m * (x_tan - x0) + y0
                
                self.ax.plot(x_tan, y_tan, color='#E74C3C', linestyle='--', label=f"Tangente (m={m:.2f})")
                self.ax.scatter([x0], [y0], color='#C0392B', zorder=5)
        except: pass

        # --- MEJORA 3: AJUSTE DEL EJE Y (AUTO-Y) ---
        # Calculamos el Y min y max REALES solo en la zona que estamos viendo
        # y filtramos infinitos para que tan(x) no rompa la gráfica
        y_validos = y_vals[np.isfinite(y_vals)] # Quitar infinitos y NaN
        if len(y_validos) > 0:
            y_min_real = np.min(y_validos)
            y_max_real = np.max(y_validos)
            
            # Dejamos un margen del 10% arriba y abajo
            margen = (y_max_real - y_min_real) * 0.1
            if margen == 0: margen = 1 # Para líneas rectas horizontales
            
            self.ax.set_ylim(y_min_real - margen, y_max_real + margen)

        # Configuración final
        self.ax.set_xlim(x_min, x_max) # Forzamos el zoom X que pidió el usuario
        self.ax.axhline(0, color='black', lw=1)
        self.ax.axvline(0, color='black', lw=1)
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.ax.legend()
        
        self.canvas.draw()

if __name__ == "__main__":
    ventana = tk.Tk()
    app = CalculadoraDerivadasIntegrales(ventana)
    ventana.mainloop()