import tkinter as tk
from tkinter import messagebox
import sympy

class CalculadoraDerivarIntegrar:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Completa")
        self.root.geometry("500x450")
        self.root.config(bg="#2C3E50")

        # --- TÍTULO ---
        tk.Label(root, text="Calculadora de Análisis", bg="#2C3E50", fg="white", 
                 font=("Helvetica", 18, "bold")).pack(pady=20)

        # --- AYUDA VISUAL (Etiquetas de sintaxis) ---
        info_text = "Soporta: sin, cos, tan, arcsin, arccos, arctan, sqrt, exp..., use ** para potencia, * para multiplicación."
        tk.Label(root, text=info_text, bg="#2C3E50", fg="#BDC3C7", font=("Arial", 9)).pack()

        # --- ENTRADA ---
        self.entrada_func = tk.Entry(root, font=("Arial", 14), width=35, justify='center')
        self.entrada_func.pack(pady=10)
        # Ejemplo por defecto con cuadrado
        self.entrada_func.insert(0, "x**2") 

        # --- BOTONES ---
        frame_botones = tk.Frame(root, bg="#2C3E50")
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Derivar d/dx", command=self.calcular_derivada, 
                  bg="#E74C3C", fg="white", font=("bold", 11), width=15).grid(row=0, column=0, padx=10)

        tk.Button(frame_botones, text="Integrar ∫ dx", command=self.calcular_integral, 
                  bg="#3498DB", fg="white", font=("bold", 11), width=15).grid(row=0, column=1, padx=10)

        # --- RESULTADO ---
        tk.Label(root, text="Resultado:", bg="#2C3E50", fg="white", font=("Arial", 12)).pack(pady=5)
        
        self.salida_res = tk.Entry(root, font=("Arial", 12, "bold"), width=40, 
                                   justify='center', readonlybackground="#ECF0F1")
        self.salida_res.pack(pady=10)

    # ---------------------------------------------------------
    #  1. NORMALIZAR ENTRADA (Traductor Humano -> Python)
    # ---------------------------------------------------------
    def normalizar_entrada(self, texto):
        """Prepara el texto para que SymPy lo entienda"""
        texto = texto.lower() # Todo a minúsculas
        
        # Traducimos lo que el usuario escribe a lo que SymPy quiere
        reemplazos_entrada = {
            "arcoseno": "asin",   "arcsin": "asin",
            "arcocoseno": "acos", "arccos": "acos",
            "arcotangente": "atan", "arctan": "atan",
            "sen": "sin" 
        }
        
        for original, python_code in reemplazos_entrada.items():
            texto = texto.replace(original, python_code)
            
        return texto

    # ---------------------------------------------------------
    #  2. FORMATEAR SALIDA (Traductor Python -> Humano)
    # ---------------------------------------------------------
    def formatear_salida(self, texto_sympy):
        """Embellece la respuesta matemática"""
        texto = texto_sympy
        
        # Devolvemos el nombre bonito
        reemplazos_salida = {
            "**": "^",
            "*": "·",
            "sqrt": "√",
            "asin": "arcsin",  
            "acos": "arccos",
            "atan": "arctan",
            "log": "ln",
            "pi": "π",
            "exp": "e^"
        }
        
        for python_code, bonito in reemplazos_salida.items():
            texto = texto.replace(python_code, bonito)
            
        return texto

    def obtener_expresion(self):
        texto_usuario = self.entrada_func.get()
        # Paso 1: Limpiamos la entrada antes de dársela a SymPy
        texto_limpio = self.normalizar_entrada(texto_usuario)
        
        try:
            return sympy.sympify(texto_limpio, locals={"e": sympy.E, "pi": sympy.pi})
        except:
            messagebox.showerror("Error", "La función tiene escrito un error de syntaxis comprueba si existe algun error.")
            return None

    def calcular_derivada(self):
        expr = self.obtener_expresion()
        if expr:
            x = sympy.symbols('x')
            res = sympy.diff(expr, x)
            # Paso 2: Formateamos la salida antes de mostrarla
            self.mostrar_resultado(self.formatear_salida(str(res)))

    def calcular_integral(self):
        expr = self.obtener_expresion()
        if expr:
            x = sympy.symbols('x')
            res = sympy.integrate(expr, x)
            texto_final = self.formatear_salida(str(res)) + " + C"
            self.mostrar_resultado(texto_final)

    def mostrar_resultado(self, texto):
        self.salida_res.config(state='normal')
        self.salida_res.delete(0, tk.END)
        self.salida_res.insert(0, texto)
        self.salida_res.config(state='readonly')

if __name__ == "__main__":
    ventana = tk.Tk()
    app = CalculadoraDerivarIntegrar(ventana)
    ventana.mainloop()