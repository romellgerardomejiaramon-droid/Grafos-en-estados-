
import tkinter as tk
from tkinter import ttk, messagebox


class Grafo:
    def __init__(self):
        self.grafo = {
            "Yucatan": {
                "Campeche": 386,
                "Quintana Roo": 712
            },
            "Campeche": {
                "Yucatan": 386,
                "Tabasco": 918,
                "Chiapas": 1334,
                "Quintana Roo": 1110
            },
            "Quintana Roo": {
                "Yucatan": 712,
                "Campeche": 1110,
                "Tabasco": 1096
            },
            "Tabasco": {
                "Campeche": 918,
                "Chiapas": 700,
                "Veracruz": 1496,
                "Quintana Roo": 1096
            },
            "Chiapas": {
                "Campeche": 1334,
                "Tabasco": 700,
                "Oaxaca": 1060
            },
            "Oaxaca": {
                "Chiapas": 1060,
                "Veracruz": 1600
            },
            "Veracruz": {
                "Tabasco": 1496,
                "Oaxaca": 1600
            }
        }

    def obtener_estados(self):
        return list(self.grafo.keys())

    def obtener_relaciones(self):
        relaciones = []
        estados = self.obtener_estados()

        for origen in self.grafo:
            for destino, costo in self.grafo[origen].items():
                if estados.index(origen) < estados.index(destino):
                    relaciones.append((origen, destino, costo))

        return relaciones

    def buscar_recorrido_completo(self, cantidad, inicio=None, destino=None):
        rutas = []
        estados = self.obtener_estados()
        inicios = [inicio] if inicio else estados

        def explorar(actual, ruta, costo):
            if len(ruta) == cantidad:
                if len(set(ruta)) != 7:
                    return

                if cantidad == 8 and len(set(ruta)) == len(ruta):
                    return

                if destino and actual != destino:
                    return

                rutas.append({
                    "ruta": ruta.copy(),
                    "costo": costo,
                    "traslados": len(ruta) - 1
                })
                return

            for vecino, precio in self.grafo[actual].items():
                ruta.append(vecino)
                explorar(vecino, ruta, costo + precio)
                ruta.pop()

        for estado in inicios:
            explorar(estado, [estado], 0)

        rutas.sort(key=lambda x: x["costo"])
        return rutas

    def buscar_alternativas(self, inicio=None, destino=None):
        rutas = []
        estados = self.obtener_estados()

        inicios = [inicio] if inicio else estados
        destinos = [destino] if destino else estados

        def explorar(actual, final, ruta, costo):
            if actual == final:
                rutas.append({
                    "ruta": ruta.copy(),
                    "costo": costo,
                    "traslados": len(ruta) - 1
                })
                return

            for vecino, precio in self.grafo[actual].items():
                if vecino not in ruta:
                    ruta.append(vecino)
                    explorar(vecino, final, ruta, costo + precio)
                    ruta.pop()

        for origen in inicios:
            for final in destinos:
                if origen != final:
                    explorar(origen, final, [origen], 0)

        rutas.sort(
            key=lambda x: (
                x["costo"],
                x["traslados"]
            )
        )

        return rutas


class Aplicacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.grafo = Grafo()

        self.ruta = []
        self.alternativas = []
        self.tipo_actual = ""

        self.estado_arrastrado = None
        self.ultima_x = 0
        self.ultima_y = 0

        self.posiciones = {
            "Yucatan": (0.20, 0.18),
            "Campeche": (0.10, 0.48),
            "Quintana Roo": (0.76, 0.18),
            "Tabasco": (0.43, 0.63),
            "Chiapas": (0.66, 0.78),
            "Oaxaca": (0.88, 0.48),
            "Veracruz": (0.91, 0.15)
        }

        self.configurar_ventana()
        self.crear_interfaz()

    def configurar_ventana(self):
        self.ventana.title("Sistema de Grafos - Rutas Mexico")
        self.ventana.state("zoomed")
        self.ventana.minsize(1000, 700)
        self.ventana.configure(bg="#111827")

    def crear_interfaz(self):
        encabezado = tk.Frame(
            self.ventana,
            bg="#172033",
            height=55
        )
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text="RUTAS MEXICO",
            font=("Arial", 20, "bold"),
            bg="#172033",
            fg="#5eead4"
        ).pack(side="left", padx=20, pady=10)

        tk.Label(
            encabezado,
            text="SISTEMA DE RECORRIDOS MEDIANTE GRAFOS",
            font=("Arial", 9, "bold"),
            bg="#172033",
            fg="white"
        ).pack(side="right", padx=20)

        tarjetas = tk.Frame(
            self.ventana,
            bg="#111827"
        )
        tarjetas.pack(fill="x", padx=12, pady=5)

        self.crear_tarjeta(tarjetas, "ESTADOS", "7", 0)
        self.crear_tarjeta(tarjetas, "CONEXIONES", "10", 1)
        self.crear_tarjeta(tarjetas, "RECORRIDO", "Pendiente", 2)
        self.crear_tarjeta(tarjetas, "COSTO TOTAL", "$0", 3)

        controles = tk.Frame(
            self.ventana,
            bg="#172033"
        )
        controles.pack(fill="x", padx=12, pady=5)

        tk.Label(
            controles,
            text="SELECCIONA EL INICIO Y DESTINO",
            font=("Arial", 11, "bold"),
            bg="#172033",
            fg="white"
        ).pack(pady=5)

        seleccion = tk.Frame(
            controles,
            bg="#172033"
        )
        seleccion.pack(pady=4)

        estados = ["Cualquiera"] + self.grafo.obtener_estados()

        tk.Label(
            seleccion,
            text="Inicio:",
            bg="#172033",
            fg="white"
        ).grid(row=0, column=0, padx=5)

        self.origen = ttk.Combobox(
            seleccion,
            values=estados,
            state="readonly",
            width=18
        )
        self.origen.set("Cualquiera")
        self.origen.grid(row=0, column=1, padx=5)

        tk.Label(
            seleccion,
            text="Destino:",
            bg="#172033",
            fg="white"
        ).grid(row=0, column=2, padx=5)

        self.destino = ttk.Combobox(
            seleccion,
            values=estados,
            state="readonly",
            width=18
        )
        self.destino.set("Cualquiera")
        self.destino.grid(row=0, column=3, padx=5)

        botones = tk.Frame(
            controles,
            bg="#172033"
        )
        botones.pack(pady=7)

        opciones = [
            ("A - SIN REPETIR ESTADOS", self.inciso_a, "#2563eb"),
            ("B - CON REPETICION", self.inciso_b, "#7c3aed"),
            ("BUSCAR ALTERNATIVAS", self.recomendar_rutas, "#d97706"),
            ("MOSTRAR RELACIONES", self.mostrar_relaciones, "#0f766e"),
            ("LIMPIAR", self.limpiar, "#475569")
        ]

        for i, (texto, funcion, color) in enumerate(opciones):
            tk.Button(
                botones,
                text=texto,
                command=funcion,
                bg=color,
                fg="white",
                font=("Arial", 8, "bold"),
                width=21,
                height=2
            ).grid(row=0, column=i, padx=3)

        contenido = tk.Frame(
            self.ventana,
            bg="#111827"
        )
        contenido.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=5
        )

        izquierda = tk.Frame(
            contenido,
            bg="#172033"
        )
        izquierda.pack(
            side="left",
            fill="both",
            expand=True
        )

        tk.Label(
            izquierda,
            text="GRAFO DE LOS SIETE ESTADOS",
            bg="#172033",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        self.canvas = tk.Canvas(
            izquierda,
            bg="#f1f5f9",
            highlightthickness=0,
            height=400
        )
        self.canvas.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        self.canvas.bind(
            "<Configure>",
            self.actualizar_grafo
        )

        self.canvas.bind(
            "<ButtonPress-1>",
            self.iniciar_arrastre
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.mover_estado
        )

        self.canvas.bind(
            "<ButtonRelease-1>",
            self.terminar_arrastre
        )

        derecha = tk.Frame(
            contenido,
            bg="#172033",
            width=320
        )
        derecha.pack(
            side="right",
            fill="y",
            padx=(7, 0)
        )
        derecha.pack_propagate(False)

        tk.Label(
            derecha,
            text="RESULTADOS Y ALTERNATIVAS",
            bg="#172033",
            fg="#5eead4",
            font=("Arial", 11, "bold")
        ).pack(pady=7)

        self.lista = tk.Listbox(
            derecha,
            bg="#26364d",
            fg="white",
            selectbackground="#0f766e",
            font=("Arial", 9),
            height=7
        )
        self.lista.pack(fill="x", padx=8, pady=5)

        self.lista.bind(
            "<<ListboxSelect>>",
            self.seleccionar_ruta
        )

        tk.Label(
            derecha,
            text="DETALLE DEL RECORRIDO",
            bg="#172033",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(pady=4)

        self.resultado = tk.Text(
            derecha,
            bg="#26364d",
            fg="white",
            font=("Arial", 9),
            wrap="word",
            relief="flat",
            padx=8,
            pady=8
        )
        self.resultado.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        tk.Label(
            self.ventana,
            text="RELACIONES Y COSTOS DE TRASLADO",
            bg="#111827",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(pady=4)

        self.tabla = ttk.Treeview(
            self.ventana,
            columns=("origen", "destino", "costo"),
            show="headings",
            height=3
        )

        self.tabla.heading("origen", text="Estado de origen")
        self.tabla.heading("destino", text="Estado de destino")
        self.tabla.heading("costo", text="Costo de referencia")

        self.tabla.column("origen", anchor="center")
        self.tabla.column("destino", anchor="center")
        self.tabla.column("costo", anchor="center")

        self.tabla.pack(
            fill="x",
            padx=20,
            pady=5
        )

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background="#26364d",
            foreground="white",
            fieldbackground="#26364d",
            rowheight=22
        )

        estilo.configure(
            "Treeview.Heading",
            background="#0f766e",
            foreground="white"
        )

        self.mostrar_relaciones()

    def crear_tarjeta(self, padre, titulo, valor, columna):
        tarjeta = tk.Frame(
            padre,
            bg="#172033",
            height=60
        )

        tarjeta.grid(
            row=0,
            column=columna,
            sticky="ew",
            padx=5
        )

        padre.grid_columnconfigure(
            columna,
            weight=1
        )

        tk.Label(
            tarjeta,
            text=titulo,
            font=("Arial", 8, "bold"),
            bg="#172033",
            fg="#94a3b8"
        ).pack(pady=(5, 0))

        etiqueta = tk.Label(
            tarjeta,
            text=valor,
            font=("Arial", 14, "bold"),
            bg="#172033",
            fg="#5eead4"
        )
        etiqueta.pack()

        if titulo == "RECORRIDO":
            self.tarjeta_recorrido = etiqueta

        if titulo == "COSTO TOTAL":
            self.tarjeta_costo = etiqueta

    def obtener_seleccion(self):
        inicio = self.origen.get()
        destino = self.destino.get()

        if inicio == "Cualquiera":
            inicio = None

        if destino == "Cualquiera":
            destino = None

        return inicio, destino

    def inciso_a(self):
        self.resolver_inciso(7, "SIN REPETICION")

    def inciso_b(self):
        self.resolver_inciso(8, "CON REPETICION")

    def resolver_inciso(self, cantidad, tipo):
        inicio, destino = self.obtener_seleccion()

        rutas = self.grafo.buscar_recorrido_completo(
            cantidad,
            inicio,
            destino
        )

        self.lista.delete(0, tk.END)
        self.alternativas = rutas[:3]

        if not self.alternativas:
            messagebox.showwarning(
                "Sin resultados",
                "No se encontro un recorrido que cumpla las condiciones."
            )
            return

        self.tipo_actual = tipo

        for i, alternativa in enumerate(self.alternativas, 1):
            self.lista.insert(
                tk.END,
                f"OPCION {i} | ${alternativa['costo']:,} | "
                f"{alternativa['traslados']} traslados"
            )

        self.tarjeta_recorrido.config(text=tipo)
        self.lista.selection_set(0)
        self.seleccionar_ruta()

    def recomendar_rutas(self):
        inicio, destino = self.obtener_seleccion()

        rutas = self.grafo.buscar_alternativas(
            inicio,
            destino
        )

        self.lista.delete(0, tk.END)
        self.alternativas = rutas[:3]

        if not self.alternativas:
            messagebox.showwarning(
                "Sin resultados",
                "No se encontraron rutas posibles."
            )
            return

        self.tipo_actual = "ALTERNATIVAS"

        for i, alternativa in enumerate(self.alternativas, 1):
            self.lista.insert(
                tk.END,
                f"OPCION {i} | ${alternativa['costo']:,} | "
                f"{alternativa['traslados']} traslados"
            )

        menos_traslados = min(
            rutas,
            key=lambda x: (
                x["traslados"],
                x["costo"]
            )
        )

        if menos_traslados not in self.alternativas:
            self.alternativas.append(menos_traslados)

            self.lista.insert(
                tk.END,
                f"MENOS TRASLADOS | ${menos_traslados['costo']:,} | "
                f"{menos_traslados['traslados']} traslados"
            )

        self.tarjeta_recorrido.config(text="ALTERNATIVAS")
        self.lista.selection_set(0)
        self.seleccionar_ruta()

    def seleccionar_ruta(self, evento=None):
        seleccion = self.lista.curselection()

        if not seleccion:
            return

        indice = seleccion[0]

        if indice >= len(self.alternativas):
            return

        alternativa = self.alternativas[indice]
        self.ruta = alternativa["ruta"]

        self.tarjeta_costo.config(
            text=f"${alternativa['costo']:,}"
        )

        self.dibujar_grafo()

        self.resultado.delete("1.0", tk.END)

        self.resultado.insert(
            tk.END,
            f"{self.tipo_actual}\n\n"
        )

        self.resultado.insert(
            tk.END,
            "RECORRIDO:\n"
            + " -> ".join(self.ruta)
            + "\n\n"
        )

        self.resultado.insert(
            tk.END,
            f"Costo total: ${alternativa['costo']:,} MXN\n"
            f"Traslados: {alternativa['traslados']}\n"
            f"Estados diferentes: {len(set(self.ruta))}\n"
            f"Visitas: {len(self.ruta)}\n\n"
            "DETALLE DE TRASLADOS:\n\n"
        )

        for i in range(len(self.ruta) - 1):
            origen = self.ruta[i]
            destino = self.ruta[i + 1]
            precio = self.grafo.grafo[origen][destino]

            self.resultado.insert(
                tk.END,
                f"{origen} -> {destino}\n"
                f"Costo: ${precio:,} MXN\n\n"
            )

    def mostrar_relaciones(self):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        for origen, destino, costo in self.grafo.obtener_relaciones():
            self.tabla.insert(
                "",
                "end",
                values=(
                    origen,
                    destino,
                    f"${costo:,} MXN"
                )
            )

    def obtener_coordenadas(self):
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        margen_x = 65
        margen_y = 45

        espacio_x = max(1, ancho - 2 * margen_x)
        espacio_y = max(1, alto - 2 * margen_y)

        coordenadas = {}

        for estado, (px, py) in self.posiciones.items():
            x = margen_x + px * espacio_x
            y = margen_y + py * espacio_y
            coordenadas[estado] = (x, y)

        return coordenadas

    def actualizar_grafo(self, evento=None):
        self.dibujar_grafo()

    def dibujar_grafo(self):
        if not hasattr(self, "canvas"):
            return

        self.canvas.delete("all")

        coordenadas = self.obtener_coordenadas()

        for origen, destino, costo in self.grafo.obtener_relaciones():
            x1, y1 = coordenadas[origen]
            x2, y2 = coordenadas[destino]

            resaltada = any(
                {self.ruta[i], self.ruta[i + 1]} == {origen, destino}
                for i in range(len(self.ruta) - 1)
            )

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="#dc2626" if resaltada else "#64748b",
                width=4 if resaltada else 2
            )

            xm = (x1 + x2) / 2
            ym = (y1 + y2) / 2

            self.canvas.create_rectangle(
                xm - 30, ym - 11,
                xm + 30, ym + 11,
                fill="white",
                outline="#94a3b8"
            )

            self.canvas.create_text(
                xm, ym,
                text=f"${costo:,}",
                fill="#172033",
                font=("Arial", 8, "bold")
            )

        for estado, (x, y) in coordenadas.items():
            color = "#16a34a" if estado in self.ruta else "#2563eb"

            self.canvas.create_oval(
                x - 48, y - 25,
                x + 48, y + 25,
                fill=color,
                outline="#172033",
                width=2,
                tags=("nodo", estado)
            )

            self.canvas.create_text(
                x, y,
                text=estado,
                fill="white",
                font=("Arial", 9, "bold"),
                tags=("nodo", estado)
            )

        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() - 15,
            text="ARRASTRA LOS ESTADOS CON EL MOUSE",
            fill="#334155",
            font=("Arial", 9, "bold")
        )

    def iniciar_arrastre(self, evento):
        coordenadas = self.obtener_coordenadas()

        self.estado_arrastrado = None
        menor_distancia = float("inf")

        for estado, (x, y) in coordenadas.items():
            distancia = (
                (evento.x - x) ** 2 +
                (evento.y - y) ** 2
            )

            if distancia <= 55 ** 2 and distancia < menor_distancia:
                menor_distancia = distancia
                self.estado_arrastrado = estado

        self.ultima_x = evento.x
        self.ultima_y = evento.y

    def mover_estado(self, evento):
        if not self.estado_arrastrado:
            return

        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        coordenadas = self.obtener_coordenadas()
        x, y = coordenadas[self.estado_arrastrado]

        nuevo_x = max(113, min(ancho - 113, x + evento.x - self.ultima_x))
        nuevo_y = max(70, min(alto - 70, y + evento.y - self.ultima_y))

        margen_x = 65
        margen_y = 45

        espacio_x = max(1, ancho - 2 * margen_x)
        espacio_y = max(1, alto - 2 * margen_y)

        self.posiciones[self.estado_arrastrado] = (
            (nuevo_x - margen_x) / espacio_x,
            (nuevo_y - margen_y) / espacio_y
        )

        self.ultima_x = evento.x
        self.ultima_y = evento.y

        self.dibujar_grafo()

    def terminar_arrastre(self, evento):
        self.estado_arrastrado = None

    def limpiar(self):
        self.ruta = []
        self.alternativas = []

        self.lista.delete(0, tk.END)
        self.resultado.delete("1.0", tk.END)

        self.tarjeta_recorrido.config(text="Pendiente")
        self.tarjeta_costo.config(text="$0")

        self.dibujar_grafo()


ventana = tk.Tk()
app = Aplicacion(ventana)
ventana.mainloop()
