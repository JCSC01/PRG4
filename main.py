"""
Music Manager - Sistema de Gestion Musical
=========================================
Sistema de gestion musical construido con Python 3 y PyQt6.

Este archivo contiene TODO el programa en un solo archivo, ordenado en
secciones para que sea facil de explicar en una exposicion:

    1. Importaciones
    2. Estilos (hoja QSS del tema oscuro)
    3. Modelos y logica de datos      (Cancion, Usuario, Reproduccion, BibliotecaMusical)
    4. Datos de ejemplo
    5. Dialogos secundarios           (los 5 QDialog)
    6. Ventana principal              (QMainWindow con la tabla y los botones)
    7. Funciones de gestion           (metodos de VentanaPrincipal: agregar, buscar,
                                       registrar, finalizar, historial, registro)
    8. Punto de entrada               (main)

Equivalencias con el sistema de videoclub original:
    Pelicula   -> Cancion
    Cliente    -> Usuario
    Alquiler   -> Reproduccion
    Devolucion -> Finalizar reproduccion
    Historial  -> Historial de observaciones

INSTALACION Y EJECUCION:
    pip install PyQt6
    python main.py
"""

from __future__ import annotations

import sys
import unicodedata
from datetime import datetime
from typing import Iterable, List, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QFont, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


# ===========================================================================
# 1. IMPORTACIONES  ->  ver arriba
# ===========================================================================


# ===========================================================================
# 2. ESTILOS: HOJA QSS DEL TEMA OSCURO
# ===========================================================================
# Paleta de colores del tema oscuro
FONDO = "#141220"
PANEL = "#1d1a2b"
PANEL_CLARO = "#262238"
BORDE = "#332d48"
TEXTO = "#ece9f5"
TEXTO_SUAVE = "#a49fc0"
PRIMARIO = "#8b5cf6"
PRIMARIO_OSCURO = "#6d3fe0"
ACENTO = "#ec4899"
EXITO = "#22c55e"
PELIGRO = "#f43f5e"


HOJA_DE_ESTILOS = f"""
/* ---------------------------------------------------------------- Base general */
QWidget {{
    background-color: {FONDO};
    color: {TEXTO};
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}}

QToolTip {{
    background-color: {PANEL_CLARO};
    color: {TEXTO};
    border: 1px solid {PRIMARIO};
    padding: 6px;
    border-radius: 6px;
}}

QDialog {{
    background-color: {FONDO};
}}

/* ------------------------------------------------------------- Barra superior */
QFrame#TopBar {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {PANEL}, stop:0.55 #2a1b45, stop:1 {PANEL});
    border-bottom: 2px solid {PRIMARIO};
}}

QLabel#TituloApp {{
    font-size: 24px;
    font-weight: 700;
    color: {TEXTO};
}}

QLabel#SubtituloApp {{
    font-size: 12px;
    color: {TEXTO_SUAVE};
}}

QLabel#Estadistica {{
    font-size: 13px;
    font-weight: 600;
    color: {TEXTO};
    background-color: rgba(139, 92, 246, 0.18);
    border: 1px solid {PRIMARIO};
    border-radius: 10px;
    padding: 7px 14px;
}}

/* ------------------------------------------------------------------- Paneles */
QFrame#Panel {{
    background-color: {PANEL};
    border: 1px solid {BORDE};
    border-radius: 12px;
}}

QFrame#PanelFormulario {{
    background-color: {PANEL};
    border: 1px solid {BORDE};
    border-radius: 12px;
}}

QLabel#TituloPanel {{
    font-size: 14px;
    font-weight: 700;
    color: {TEXTO};
    letter-spacing: 1px;
}}

QLabel#Etiqueta {{
    color: {TEXTO_SUAVE};
    font-size: 12px;
    font-weight: 600;
}}

QLabel#CampoObligatorio {{
    color: {ACENTO};
    font-size: 12px;
    font-weight: 700;
}}

/* --------------------------------------------------------------- Entrada datos */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox {{
    background-color: {PANEL_CLARO};
    border: 1px solid {BORDE};
    border-radius: 8px;
    padding: 8px 10px;
    color: {TEXTO};
    selection-background-color: {PRIMARIO};
    selection-color: #ffffff;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus {{
    border: 1px solid {PRIMARIO};
    background-color: #2e2942;
}}

QLineEdit::placeholder {{
    color: #6f6a8c;
}}

QLineEdit:disabled, QTextEdit:disabled {{
    color: {TEXTO_SUAVE};
    background-color: #221f30;
}}

QComboBox {{
    background-color: {PANEL_CLARO};
    border: 1px solid {BORDE};
    border-radius: 8px;
    padding: 7px 10px;
    color: {TEXTO};
    min-height: 18px;
}}

QComboBox:hover {{
    border: 1px solid {PRIMARIO};
}}

QComboBox:focus {{
    border: 1px solid {PRIMARIO};
}}

QComboBox::drop-down {{
    border: none;
    width: 22px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {TEXTO_SUAVE};
    margin-right: 8px;
}}

QComboBox QAbstractItemView {{
    background-color: {PANEL_CLARO};
    border: 1px solid {PRIMARIO};
    border-radius: 8px;
    selection-background-color: {PRIMARIO};
    selection-color: #ffffff;
    padding: 4px;
}}

/* ------------------------------------------------------------------- Botones */
QPushButton {{
    background-color: {PANEL_CLARO};
    border: 1px solid {BORDE};
    border-radius: 9px;
    padding: 9px 14px;
    color: {TEXTO};
    font-weight: 600;
}}

QPushButton:hover {{
    background-color: #322c4a;
    border: 1px solid {PRIMARIO};
}}

QPushButton:pressed {{
    background-color: {PRIMARIO_OSCURO};
}}

QPushButton:disabled {{
    color: #625d7a;
    background-color: #1f1c2c;
    border: 1px solid #2a2739;
}}

QPushButton#Primario {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {PRIMARIO}, stop:1 {ACENTO});
    border: none;
    color: #ffffff;
    font-weight: 700;
}}

QPushButton#Primario:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #9d75f8, stop:1 #f35fa8);
}}

QPushButton#Primario:disabled {{
    background: #3a3550;
    color: #7c779a;
}}

QPushButton#Peligro {{
    background-color: rgba(244, 63, 94, 0.16);
    border: 1px solid {PELIGRO};
    color: #fda4b4;
}}

QPushButton#Peligro:hover {{
    background-color: {PELIGRO};
    color: #ffffff;
}}

QPushButton#Exito {{
    background-color: rgba(34, 197, 94, 0.16);
    border: 1px solid {EXITO};
    color: #86efac;
}}

QPushButton#Exito:hover {{
    background-color: {EXITO};
    color: #06240f;
}}

QPushButton#Fantasma {{
    background-color: rgba(236, 72, 153, 0.14);
    border: 1px solid {ACENTO};
    color: #f9a8d4;
}}

QPushButton#Fantasma:hover {{
    background-color: {ACENTO};
    color: #ffffff;
}}

QPushButton#Mini {{
    background-color: rgba(139, 92, 246, 0.14);
    border: 1px solid {PRIMARIO};
    border-radius: 7px;
    padding: 7px 12px;
    font-size: 11px;
    font-weight: 600;
    color: #cdb8fd;
}}

QPushButton#Mini:hover {{
    background-color: {PRIMARIO};
    color: #ffffff;
}}

/* -------------------------------------------------------------------- Tablas */
QTableWidget {{
    background-color: {PANEL};
    alternate-background-color: #221e33;
    border: 1px solid {BORDE};
    border-radius: 10px;
    gridline-color: #2b2640;
    selection-background-color: rgba(139, 92, 246, 0.30);
    selection-color: {TEXTO};
    font-size: 12px;
}}

QTableWidget::item {{
    padding: 7px 8px;
    border: none;
}}

QTableWidget::item:selected {{
    background-color: rgba(139, 92, 246, 0.35);
    color: #ffffff;
}}

QHeaderView::section {{
    background-color: {PRIMARIO_OSCURO};
    color: #ffffff;
    padding: 10px 8px;
    border: none;
    border-right: 1px solid #4b3a8f;
    font-weight: 700;
    font-size: 12px;
}}

QHeaderView::section:hover {{
    background-color: {PRIMARIO};
}}

QTableCornerButton::section {{
    background-color: {PRIMARIO_OSCURO};
    border: none;
}}

/* --------------------------------------------------------------- Listas */
QListWidget {{
    background-color: {PANEL_CLARO};
    border: 1px solid {BORDE};
    border-radius: 10px;
    padding: 6px;
    outline: none;
}}

QListWidget::item {{
    padding: 9px 10px;
    border-radius: 7px;
    margin: 2px 0;
    color: {TEXTO};
}}

QListWidget::item:hover {{
    background-color: #342e4d;
}}

QListWidget::item:selected {{
    background-color: {PRIMARIO};
    color: #ffffff;
}}

/* ------------------------------------------------------------------ Etiquetas */
QLabel#ChipDisponible {{
    background-color: rgba(34, 197, 94, 0.18);
    color: #86efac;
    border: 1px solid {EXITO};
    border-radius: 9px;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: 700;
}}

QLabel#ChipOcupada {{
    background-color: rgba(244, 63, 94, 0.18);
    color: #fda4b4;
    border: 1px solid {PELIGRO};
    border-radius: 9px;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: 700;
}}

QLabel#HistorialVacio {{
    color: {TEXTO_SUAVE};
    font-style: italic;
    font-size: 13px;
    padding: 24px;
}}

QLabel#Aviso {{
    color: {TEXTO_SUAVE};
    font-size: 11px;
}}

/* --------------------------------------------------------------- barra scroll */
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background: #443c63;
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {PRIMARIO};
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 2px;
}}

QScrollBar::handle:horizontal {{
    background: #443c63;
    border-radius: 5px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {PRIMARIO};
}}

QScrollBar::add-line, QScrollBar::sub-line {{
    height: 0;
    width: 0;
}}

QScrollBar::add-page, QScrollBar::sub-page {{
    background: none;
}}

/* ------------------------------------------------------- Pestañas y checkboxes */
QTabWidget::pane {{
    border: 1px solid {BORDE};
    border-radius: 10px;
    top: -1px;
}}

QTabBar::tab {{
    background: {PANEL_CLARO};
    color: {TEXTO_SUAVE};
    padding: 9px 18px;
    border: 1px solid {BORDE};
    border-bottom: none;
    border-top-left-radius: 9px;
    border-top-right-radius: 9px;
    margin-right: 3px;
    font-weight: 600;
}}

QTabBar::tab:selected {{
    background: {PRIMARIO_OSCURO};
    color: #ffffff;
    border-color: {PRIMARIO};
}}

QTabBar::tab:hover:!selected {{
    color: {TEXTO};
    border-color: {PRIMARIO};
}}

QCheckBox {{
    spacing: 8px;
    color: {TEXTO};
}}

QCheckBox::indicator {{
    width: 17px;
    height: 17px;
    border-radius: 5px;
    border: 1px solid {BORDE};
    background: {PANEL_CLARO};
}}

QCheckBox::indicator:checked {{
    background: {PRIMARIO};
    border: 1px solid {PRIMARIO};
}}

QRadioButton {{
    spacing: 8px;
    color: {TEXTO};
}}

QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 9px;
    border: 1px solid {BORDE};
    background: {PANEL_CLARO};
}}

QRadioButton::indicator:checked {{
    background: {PRIMARIO};
    border: 4px solid {PANEL};
}}

/* --------------------------------------------------- Barra de estado y menús */
QStatusBar {{
    background-color: {PANEL};
    color: {TEXTO_SUAVE};
    border-top: 1px solid {BORDE};
}}

QStatusBar::item {{
    border: none;
}}

QMenuBar {{
    background-color: {PANEL};
    color: {TEXTO};
    border-bottom: 1px solid {BORDE};
}}

QMenuBar::item:selected {{
    background: {PRIMARIO_OSCURO};
}}

QMenu {{
    background-color: {PANEL_CLARO};
    border: 1px solid {BORDE};
    border-radius: 8px;
    padding: 6px;
}}

QMenu::item {{
    padding: 8px 22px 8px 14px;
    border-radius: 6px;
}}

QMenu::item:selected {{
    background-color: {PRIMARIO};
    color: #ffffff;
}}

QMenu::separator {{
    height: 1px;
    background: {BORDE};
    margin: 5px 8px;
}}

/* ------------------------------------------- Cajas de mensaje (QMessageBox) */
QMessageBox {{
    background-color: {PANEL};
}}

QMessageBox QLabel {{
    color: {TEXTO};
    font-size: 13px;
}}

QMessageBox QPushButton {{
    min-width: 88px;
}}

QSplitter::handle {{
    background: transparent;
}}
"""


def aplicar_estilos(app) -> None:
    """
    Aplica la hoja de estilos y la fuente base a la aplicación.
    Se llama una sola vez desde main.py.
    """

    app.setStyleSheet(HOJA_DE_ESTILOS)

    # Fuente base del sistema + fuente de emojis para que se vean los iconos.
    fuente = QFont()
    fuente.setFamilies(["Segoe UI", "Inter", "Segoe UI Emoji"])
    fuente.setPointSize(10)
    app.setFont(fuente)


# ===========================================================================
# 3. MODELOS Y LOGICA DE DATOS
# ===========================================================================
# --------------------------------------------------------------------------------------
# Catálogo de géneros disponibles para el QComboBox del formulario de registro
# --------------------------------------------------------------------------------------
GENEROS: List[str] = [
    "Pop",
    "Rock",
    "Reggaetón",
    "Rap",
    "Hip Hop",
    "Electrónica",
    "Salsa",
    "Bachata",
    "Música Clásica",
    "Jazz",
    "Regional",
    "Otro",
]


# --------------------------------------------------------------------------------------
# Utilidades de texto y duración
# --------------------------------------------------------------------------------------
def normalizar_texto(texto: str) -> str:
    """
    Devuelve el texto en minúsculas y SIN tildes.

    Se usa para que el buscador no falle cuando el usuario escribe
    "bad bunny" o "Bachata" en lugar de "Bad Bunny" o "Bachata" con tilde.
    """

    texto = unicodedata.normalize("NFD", texto.lower())
    # Elimina los caracteres de acentuación (categoría "Mn")
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def formatear_duracion(segundos: int) -> str:
    """Convierte segundos a texto m:ss  (225 -> '3:45')."""
    minutos, seg = divmod(int(segundos), 60)
    return f"{minutos}:{seg:02d}"


def interpretar_duracion(texto: str) -> tuple[bool, int, str]:
    """
    Convierte lo que escribe el usuario a segundos.

    Formatos aceptados:
        "3:45"   -> 225 segundos (minutos:segundos)
        "03:45"  -> 225 segundos
        "225"    -> 225 segundos (se interpreta como segundos)

    Returns:
        (ok, valor_en_segundos, mensaje_de_error)
    """
    texto = texto.strip()

    if not texto:
        return False, 0, "Ingresa la duración de la canción."

    if ":" in texto:
        partes = texto.split(":")
        if len(partes) != 2:
            return False, 0, "Duración inválida. Usa el formato minutos:segundos (ejemplo: 3:45)."
        minutos_txt, segundos_txt = partes
        if not minutos_txt.strip().isdigit() or not segundos_txt.strip().isdigit():
            return False, 0, "Duración inválida. Solo se permiten números (ejemplo: 3:45)."
        minutos = int(minutos_txt)
        segundos = int(segundos_txt)
        if segundos > 59:
            return False, 0, "Los segundos no pueden ser mayores a 59 (ejemplo correcto: 3:45)."
    else:
        if not texto.isdigit():
            return False, 0, "Duración inválida. Escribe 3:45 o el total de segundos (ejemplo: 225)."
        minutos, segundos = 0, int(texto)

    if minutos > 99:
        return False, 0, "Duración demasiado larga. El máximo permitido es 99:59."

    total = minutos * 60 + segundos
    if total <= 0:
        return False, 0, "La duración debe ser mayor a 0 segundos."
    return True, total, ""


# --------------------------------------------------------------------------------------
# CLASE CANCIÓN  (equivalente a la clase Película del videoclub)
# --------------------------------------------------------------------------------------
class Cancion:
    """Representa una canción de la colección musical."""

    ESTADO_DISPONIBLE = "Disponible"
    ESTADO_OCUPADA = "Reproduciendo/Reservada"

    def __init__(
        self,
        id_cancion: int,
        titulo: str,
        artista: str,
        album: str,
        genero: str,
        duracion: str,
        disponible: bool = True,
    ) -> None:
        self.id_cancion = id_cancion
        self.titulo = titulo.strip()
        self.artista = artista.strip()
        self.album = album.strip()
        self.genero = genero.strip()
        self.duracion = duracion.strip()          # Se guarda como texto "m:ss"
        self.disponible = bool(disponible)

        # Historial de observaciones (equivale al historial de la película).
        # Cada elemento es un diccionario: {"fecha": str, "usuario": str, "texto": str}
        self.historial_observaciones: List[dict] = []

    # ---------------------------------------------------------------- propiedades
    @property
    def estado(self) -> str:
        """Texto del estado que se muestra en la tabla."""
        return self.ESTADO_DISPONIBLE if self.disponible else self.ESTADO_OCUPADA

    @property
    def total_observaciones(self) -> int:
        return len(self.historial_observaciones)

    # ------------------------------------------------------------------- lógica
    def reservar(self) -> None:
        """Marca la canción como Reproduciendo/Reservada (equivalente a 'alquilar')."""
        self.disponible = False

    def liberar(self) -> None:
        """Devuelve la canción a estado Disponible (equivalente a 'devolver')."""
        self.disponible = True

    def agregar_observacion(self, observacion: str, usuario: str = "Sistema") -> None:
        """Agrega una observación numerada al historial de la canción."""
        self.historial_observaciones.append(
            {
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "usuario": usuario,
                "texto": observacion.strip(),
            }
        )

    def coincide_con(self, texto_busqueda: str) -> bool:
        """True si la canción coincide con el título, artista o álbum buscados."""
        if not texto_busqueda:
            return True
        clave = normalizar_texto(texto_busqueda)
        return (
            clave in normalizar_texto(self.titulo)
            or clave in normalizar_texto(self.artista)
            or clave in normalizar_texto(self.album)
        )

    # ---------------------------------------------------------------- presentation
    def __str__(self) -> str:
        return f"{self.titulo} — {self.artista}"

    def __repr__(self) -> str:
        return f"Cancion(id={self.id_cancion}, titulo={self.titulo!r}, artista={self.artista!r})"


# --------------------------------------------------------------------------------------
# CLASE USUARIO  (equivalente a la clase Cliente del videoclub)
# --------------------------------------------------------------------------------------
class Usuario:
    """Representa a la persona que escucha las canciones."""

    def __init__(self, id_usuario: int, nombre: str, telefono: str = "") -> None:
        self.id_usuario = id_usuario
        self.nombre = nombre.strip()
        self.telefono = telefono.strip() if telefono else ""

    def coincide_con(self, texto_busqueda: str) -> bool:
        if not texto_busqueda:
            return True
        clave = normalizar_texto(texto_busqueda)
        return clave in normalizar_texto(self.nombre) or clave in normalizar_texto(self.telefono)

    def __str__(self) -> str:
        return self.nombre

    def __repr__(self) -> str:
        return f"Usuario(id={self.id_usuario}, nombre={self.nombre!r})"


# --------------------------------------------------------------------------------------
# CLASE REPRODUCCIÓN  (equivalente a la clase Alquiler del videoclub)
# --------------------------------------------------------------------------------------
class Reproduccion:
    """
    Relaciona un Usuario con una o varias Canciones.

    Es el mismo concepto de relación: Cliente -> Alquiler -> Películas,
    adaptado a: Usuario -> Reproducción -> Canciones.
    """

    def __init__(self, id_reproduccion: int, usuario: Usuario, canciones: Iterable[Cancion]) -> None:
        self.id_reproduccion = id_reproduccion
        self.usuario = usuario
        self.canciones: List[Cancion] = list(canciones)
        self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.finalizada = False
        self.total_canciones = len(self.canciones)   # Atributo solicitado en el enunciado

    def agregar_canciones(self, canciones: Iterable[Cancion]) -> None:
        """Agrega canciones a la reproducción y actualiza el total."""
        self.canciones.extend(canciones)
        self.total_canciones = len(self.canciones)

    def titulos_canciones(self) -> List[str]:
        """Devuelve la lista de títulos de las canciones de esta reproducción."""
        return [c.titulo for c in self.canciones]

    def duracion_total(self) -> str:
        """Suma las duraciones de las canciones de la reproducción."""
        total = 0
        for cancion in self.canciones:
            ok, segundos, _ = interpretar_duracion(cancion.duracion)
            if ok:
                total += segundos
        return formatear_duracion(total)

    def __str__(self) -> str:
        return f"Reproducción #{self.id_reproduccion} - {self.usuario.nombre}"

    def __repr__(self) -> str:
        return f"Reproduccion(id={self.id_reproduccion}, usuario={self.usuario.nombre!r})"


# --------------------------------------------------------------------------------------
# BIBLIOTECA MUSICAL  (la "base de datos" en memoria del sistema)
# --------------------------------------------------------------------------------------
class BibliotecaMusical:
    """
    Clase que administra toda la información del sistema.

    Aquí se guardan las canciones, los usuarios creados y las reproducciones.
    Los datos viven en memoria mientras el programa esté abierto.
    """

    def __init__(self) -> None:
        self.canciones: List[Cancion] = []
        self.usuarios: List[Usuario] = []
        self.reproducciones: List[Reproduccion] = []
        self._contador_cancion = 0
        self._contador_usuario = 0
        self._contador_reproduccion = 0

    # ------------------------------------------------------------------ canciones
    def agregar_cancion(
        self,
        titulo: str,
        artista: str,
        album: str,
        genero: str,
        duracion: str,
    ) -> Cancion:
        """Crea una canción con un ID automático y la agrega a la colección."""
        self._contador_cancion += 1
        cancion = Cancion(
            id_cancion=self._contador_cancion,
            titulo=titulo,
            artista=artista,
            album=album,
            genero=genero,
            duracion=duracion,
            disponible=True,
        )
        self.canciones.append(cancion)
        return cancion

    def obtener_cancion(self, id_cancion: int) -> Optional[Cancion]:
        """Busca una canción por su ID. Devuelve None si no existe."""
        for cancion in self.canciones:
            if cancion.id_cancion == id_cancion:
                return cancion
        return None

    def canciones_disponibles(self) -> List[Cancion]:
        return [c for c in self.canciones if c.disponible]

    def filtrar_canciones(
        self,
        texto: str = "",
        genero: str = "Todos",
        estado: str = "Todos",
    ) -> List[Cancion]:
        """
        Filtra la colección por texto (título/artista/álbum), género y estado.
        Se usa tanto en la tabla principal como en los diálogos.
        """
        resultado = []
        for cancion in self.canciones:
            if not cancion.coincide_con(texto):
                continue
            if genero and genero != "Todos" and cancion.genero != genero:
                continue
            if estado and estado != "Todos" and cancion.estado != estado:
                continue
            resultado.append(cancion)
        return resultado

    # -------------------------------------------------------------------- usuarios
    def obtener_o_crear_usuario(self, nombre: str, telefono: str = "") -> Usuario:
        """
        Devuelve el usuario si ya existe con ese nombre; si no, lo crea.
        Evita duplicados cuando la misma persona reproduce varias veces.
        """
        clave = normalizar_texto(nombre)
        for usuario in self.usuarios:
            if normalizar_texto(usuario.nombre) == clave:
                if telefono:
                    usuario.telefono = telefono.strip()
                return usuario
        self._contador_usuario += 1
        usuario = Usuario(self._contador_usuario, nombre, telefono)
        self.usuarios.append(usuario)
        return usuario

    # -------------------------------------------------------------- reproducciones
    def registrar_reproduccion(self, usuario: Usuario, canciones: Iterable[Cancion]) -> Reproduccion:
        """
        Crea la reproducción, reserva las canciones y guarda el registro.
        Devuelve el objeto Reproduccion generado.
        """
        self._contador_reproduccion += 1
        seleccion = list(canciones)
        reproduccion = Reproduccion(self._contador_reproduccion, usuario, seleccion)
        for cancion in seleccion:
            cancion.reservar()
        self.reproducciones.append(reproduccion)
        return reproduccion

    def finalizar_cancion(
        self,
        cancion: Cancion,
        observacion: str = "",
        usuario: str = "Sistema",
    ) -> Optional[Reproduccion]:
        """
        Equivale a la 'devolución' del videoclub: la canción vuelve a estar
        disponible, se cierra la reproducción asociada y se guarda la observación.

        Devuelve la reproducción actualizada o None si la canción ya estaba disponible.
        """
        if cancion.disponible:
            return None

        cancion.liberar()
        if observacion:
            cancion.agregar_observacion(observacion, usuario)

        # Marca como finalizada la reproducción que contenía esta canción.
        for reproduccion in self.reproducciones:
            if cancion in reproduccion.canciones and not reproduccion.finalizada:
                # Si ya no quedan canciones activas en la reproducción, se cierra.
                if all(c.disponible for c in reproduccion.canciones):
                    reproduccion.finalizada = True
                break
        return reproduccion

    def reproduccion_de(self, cancion: Cancion) -> Optional[Reproduccion]:
        """Devuelve la reproducción más reciente que incluye esa canción."""
        for reproduccion in reversed(self.reproducciones):
            if cancion in reproduccion.canciones:
                return reproduccion
        return None

    # ------------------------------------------------------------------ reportes
    def estadisticas(self) -> dict:
        """Calcula los números que se muestran en la parte superior de la ventana."""
        total = len(self.canciones)
        disponibles = sum(1 for c in self.canciones if c.disponible)
        return {
            "total_canciones": total,
            "disponibles": disponibles,
            "reservadas": total - disponibles,
            "total_reproducciones": len(self.reproducciones),
            "total_usuarios": len(self.usuarios),
            "canciones_reproducidas": sum(r.total_canciones for r in self.reproducciones),
            "observaciones": sum(c.total_observaciones for c in self.canciones),
        }


# ===========================================================================
# 4. DATOS DE EJEMPLO
# ===========================================================================
# Lista de canciones de ejemplo: (titulo, artista, album, genero, duracion)
# La duración está en segundos para convertirla con formatear_duracion().
CANCIONES_EJEMPLO = [
    ("Blinding Lights", "The Weeknd", "After Hours", "Pop", 200),
    ("Starboy", "The Weeknd", "Starboy", "Pop", 241),
    ("Shape of You", "Ed Sheeran", "Divide", "Pop", 234),
    ("Smells Like Teen Spirit", "Nirvana", "Nevermind", "Rock", 301),
    ("Billie Jean", "Michael Jackson", "Thriller", "Pop", 294),
    ("Bohemian Rhapsody", "Queen", "A Night at the Opera", "Rock", 355),
    ("Havana", "Camila Cabello", "Camila", "Pop", 217),
    ("Despacito", "Luis Fonsi", "VIDA", "Reggaetón", 229),
    ("Godzilla", "Eminem", "Music to Be Murdered By", "Rap", 236),
    ("HUMBLE.", "Kendrick Lamar", "DAMN.", "Hip Hop", 177),
    ("Titanium", "David Guetta", "Nothing but the Beat", "Electrónica", 245),
    ("Vivir Mi Vida", "Marc Anthony", "3.0", "Salsa", 249),
    ("Bésame Mucho", "Benny Andersson", "Bésame Mucho", "Bachata", 195),
    ("Take Five", "Dave Brubeck", "Time Out", "Jazz", 324),
    ("Clair de Lune", "Claude Debussy", "Suite bergamasque", "Música Clásica", 301),
    ("La Bilirrubina", "Fito Páez", "El Amor Después del Amor", "Regional", 214),
]

# Reproducciones de ejemplo: (nombre usuario, teléfono, [índices de canciones])
REPRODUCCIONES_EJEMPLO = [
    ("Ana Ramírez", "555-0142", [0, 1]),   # Blinding Lights, Starboy
    ("Carlos Mendoza", "555-0198", [4]),   # Billie Jean
]


def cargar_datos_ejemplo(biblioteca: BibliotecaMusical) -> None:
    """
    Llena la BibliotecaMusical con las canciones y reproducciones de ejemplo.
    Se invoca una sola vez al crear la ventana principal.
    """
    # 1) Registrar las canciones de ejemplo
    for titulo, artista, album, genero, segundos in CANCIONES_EJEMPLO:
        biblioteca.agregar_cancion(
            titulo=titulo,
            artista=artista,
            album=album,
            genero=genero,
            duracion=formatear_duracion(segundos),
        )

    # 2) Crear algunas reproducciones para que el sistema muestre estados distintos
    for nombre, telefono, indices in REPRODUCCIONES_EJEMPLO:
        usuario = biblioteca.obtener_o_crear_usuario(nombre, telefono)
        seleccion = [biblioteca.canciones[i] for i in indices if i < len(biblioteca.canciones)]
        if seleccion:
            biblioteca.registrar_reproduccion(usuario, seleccion)

    # 3) Agregar un par de observaciones al historial, para demostrar el historial
    for cancion, texto in (
        (
            biblioteca.canciones[3],   # Smells Like Teen Spirit
            "Audio con buena calidad. Reproducción completa.",
        ),
        (
            biblioteca.canciones[3],
            "Se detectó un problema con el archivo al inicio, se normalizó después.",
        ),
    ):
        # Historial de ejemplo (no cuenta como reproducción, es solo información)
        cancion.agregar_observacion(texto, "Sistema")


# ===========================================================================
# 5. DIALOGOS SECUNDARIOS
# ===========================================================================
# Color de texto secundario usado dentro de los diálogos
TEXTO_SUAVE_DIALOGO = "#a49fc0"


# ======================================================================================
# DIÁLOGO 1: HISTORIAL DE OBSERVACIONES DE UNA CANCIÓN
# ======================================================================================
class HistorialDialog(QDialog):
    """
    Ventana que muestra todas las observaciones registradas para una canción.

    Si la canción no tiene observaciones, muestra el mensaje
    "No hay observaciones registradas para esta canción."
    """

    def __init__(self, cancion: Cancion, parent=None) -> None:
        super().__init__(parent)
        self.cancion = cancion

        # Configuración de la ventana
        self.setWindowTitle(f"Historial - {cancion.titulo}")
        self.setModal(True)
        self.setMinimumSize(560, 420)

        self._construir_interfaz()
        self._cargar_historial()

    # ---------------------------------------------------------------- construcción
    def _construir_interfaz(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        # --- Encabezado con los datos de la canción
        encabezado = QFrame()
        encabezado.setObjectName("Panel")
        layout_encabezado = QVBoxLayout(encabezado)
        layout_encabezado.setContentsMargins(14, 12, 14, 12)

        titulo = QLabel(f"📜 Historial de observaciones")
        titulo.setObjectName("TituloPanel")
        layout_encabezado.addWidget(titulo)

        detalles = QLabel(
            f"<b>{self.cancion.titulo}</b> — {self.cancion.artista}<br>"
            f"<span style='color:#a49fc0'>Álbum: {self.cancion.album} &nbsp;|&nbsp; "
            f"Género: {self.cancion.genero} &nbsp;|&nbsp; "
            f"Duración: {self.cancion.duracion} &nbsp;|&nbsp; Estado: {self.cancion.estado}</span>"
        )
        detalles.setWordWrap(True)
        detalles.setTextFormat(Qt.TextFormat.RichText)
        layout_encabezado.addWidget(detalles)

        layout.addWidget(encabezado)

        # --- Área con la lista de entradas (Entrada #1, Entrada #2, ...)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.contenedor = QWidget()
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setContentsMargins(0, 0, 0, 0)
        self.contenedor_layout.setSpacing(10)
        self.scroll.setWidget(self.contenedor)
        layout.addWidget(self.scroll, 1)

        # --- Botón de cierre
        botones = QHBoxLayout()
        botones.addStretch(1)
        boton_cerrar = QPushButton("Cerrar")
        boton_cerrar.setObjectName("Primario")
        boton_cerrar.clicked.connect(self.accept)
        botones.addWidget(boton_cerrar)
        layout.addLayout(botones)

    # --------------------------------------------------------------------- datos
    def _cargar_historial(self) -> None:
        """Llena el área con las observaciones numeradas de la canción."""
        if not self.cancion.historial_observaciones:
            # Caso: la canción todavía no tiene historial.
            vacio = QLabel("No hay observaciones registradas para esta canción.")
            vacio.setObjectName("HistorialVacio")
            vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.contenedor_layout.addWidget(vacio)
            self.contenedor_layout.addStretch(1)
            return

        for numero, entrada in enumerate(self.cancion.historial_observaciones, start=1):
            tarjeta = QFrame()
            tarjeta.setObjectName("Panel")
            layout_tarjeta = QVBoxLayout(tarjeta)
            layout_tarjeta.setContentsMargins(14, 12, 14, 12)
            layout_tarjeta.setSpacing(6)

            # Encabezado de la entrada: "Entrada #1"
            cabecera = QLabel(f"Entrada #{numero}")
            cabecera.setObjectName("TituloPanel")
            layout_tarjeta.addWidget(cabecera)

            # Fecha y usuario que dejó la observación
            meta = QLabel(f"🗓 {entrada['fecha']} &nbsp;•&nbsp; 👤 {entrada['usuario']}")
            meta.setObjectName("Aviso")
            layout_tarjeta.addWidget(meta)

            # Texto de la observación
            texto = QLabel(entrada["texto"])
            texto.setWordWrap(True)
            texto.setTextFormat(Qt.TextFormat.RichText)
            layout_tarjeta.addWidget(texto)

            self.contenedor_layout.addWidget(tarjeta)

        # Resumen final
        resumen = QLabel(
            f"Total de observaciones: <b>{self.cancion.total_observaciones}</b>"
        )
        resumen.setObjectName("Aviso")
        resumen.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.contenedor_layout.addWidget(resumen)
        self.contenedor_layout.addStretch(1)


# ======================================================================================
# DIÁLOGO 2: REGISTRAR REPRODUCCIÓN
# ======================================================================================
class ReproduccionDialog(QDialog):
    """
    Permite registrar una reproducción:
        1. Escribir el nombre del usuario.
        2. Seleccionar una o varias canciones disponibles (selección múltiple con Ctrl).
    """

    def __init__(self, biblioteca, parent=None) -> None:
        super().__init__(parent)
        self.biblioteca = biblioteca
        self.usuario_nombre = ""
        self.usuario_telefono = ""
        self.canciones_seleccionadas: List[Cancion] = []

        # Lista auxiliar: todas las canciones disponibles (para poder filtrar)
        self.canciones_disponibles: List[Cancion] = biblioteca.canciones_disponibles()

        self.setWindowTitle("Registrar Reproducción")
        self.setModal(True)
        # Solo se fija el tamaño inicial: Qt calcula el mínimo según el contenido,
        # de modo que ningún botón o etiqueta quede recortado.
        self.resize(760, 620)

        self._construir_interfaz()
        self._cargar_lista("")

    # ---------------------------------------------------------------- construcción
    def _construir_interfaz(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        # --- Título
        titulo = QLabel("▶️ Registrar Reproducción")
        titulo.setObjectName("TituloPanel")
        layout.addWidget(titulo)

        # --- Datos del usuario
        panel_usuario = QFrame()
        panel_usuario.setObjectName("PanelFormulario")
        grid_usuario = QGridLayout(panel_usuario)
        grid_usuario.setContentsMargins(14, 12, 14, 12)
        grid_usuario.setHorizontalSpacing(12)
        grid_usuario.setVerticalSpacing(8)

        etiqueta_nombre = QLabel("Usuario *")
        etiqueta_nombre.setObjectName("Etiqueta")
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ejemplo: Juan Pérez")
        self.input_nombre.textChanged.connect(self._actualizar_contador)

        etiqueta_telefono = QLabel("Teléfono / contacto (opcional)")
        etiqueta_telefono.setObjectName("Etiqueta")
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Ejemplo: 555-0123")
        self.input_telefono.textChanged.connect(self._actualizar_contador)

        grid_usuario.addWidget(etiqueta_nombre, 0, 0)
        grid_usuario.addWidget(self.input_nombre, 0, 1)
        grid_usuario.addWidget(etiqueta_telefono, 1, 0)
        grid_usuario.addWidget(self.input_telefono, 1, 1)
        grid_usuario.setColumnStretch(1, 1)

        layout.addWidget(panel_usuario)

        # --- Buscador de canciones dentro del diálogo
        fila_busqueda = QHBoxLayout()
        etiqueta_buscar = QLabel("🔍 Buscar canción:")
        etiqueta_buscar.setObjectName("Etiqueta")
        self.input_filtro = QLineEdit()
        self.input_filtro.setPlaceholderText("Escribe para filtrar por título, artista o álbum...")
        # La tabla se actualiza mientras el usuario escribe
        self.input_filtro.textChanged.connect(self._cargar_lista)

        boton_todas = QPushButton("Seleccionar todas")
        boton_todas.setObjectName("Mini")
        boton_todas.clicked.connect(self._seleccionar_todas)

        boton_ninguna = QPushButton("Quitar selección")
        boton_ninguna.setObjectName("Mini")
        boton_ninguna.clicked.connect(lambda: self.lista.clearSelection())

        # Se fija un ancho mínimo para que el texto de los botones nunca se recorte
        for boton in (boton_todas, boton_ninguna):
            ancho_texto = boton.fontMetrics().horizontalAdvance(boton.text())
            boton.setMinimumWidth(ancho_texto + 34)
            boton.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        fila_busqueda.addWidget(etiqueta_buscar)
        fila_busqueda.addWidget(self.input_filtro, 1)
        fila_busqueda.addWidget(boton_todas)
        fila_busqueda.addWidget(boton_ninguna)
        layout.addLayout(fila_busqueda)

        # --- Lista de canciones disponibles (selección múltiple)
        self.lista = QListWidget()
        # ExtendedSelection = permite seleccionar varios elementos manteniendo Ctrl
        self.lista.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.lista.setAlternatingRowColors(False)
        self.lista.itemSelectionChanged.connect(self._actualizar_contador)
        layout.addWidget(self.lista, 1)

        # --- Contador y ayuda
        self.etiqueta_contador = QLabel()
        self.etiqueta_contador.setObjectName("Aviso")
        layout.addWidget(self.etiqueta_contador)

        ayuda = QLabel("💡 Mantén presionado Ctrl para seleccionar varias canciones.")
        ayuda.setObjectName("Aviso")
        layout.addWidget(ayuda)

        # --- Botones aceptar / cancelar
        self.botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        # Textos personalizados
        self.botones.button(QDialogButtonBox.StandardButton.Ok).setText("Registrar")
        self.botones.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        self.botones.button(QDialogButtonBox.StandardButton.Ok).setObjectName("Primario")
        self.botones.accepted.connect(self.aceptar)
        self.botones.rejected.connect(self.reject)
        layout.addWidget(self.botones)

        self._actualizar_contador()

    # --------------------------------------------------------------------- datos
    def _cargar_lista(self, texto: str = "") -> None:
        """Muestra en la lista las canciones disponibles que coincidan con el filtro."""
        self.lista.clear()
        clave = normalizar_texto(texto)
        for cancion in self.canciones_disponibles:
            if clave and clave not in normalizar_texto(
                f"{cancion.titulo} {cancion.artista} {cancion.album}"
            ):
                continue
            item = QListWidgetItem(f"{cancion.titulo}  —  {cancion.artista}   ({cancion.duracion})")
            # Se guarda el objeto Cancion en el ítem para recuperarlo después
            item.setData(Qt.ItemDataRole.UserRole, cancion)
            self.lista.addItem(item)

        if not self.lista.count():
            vacio = QListWidgetItem("No hay canciones disponibles con ese filtro.")
            vacio.setFlags(Qt.ItemFlag.NoItemFlags)
            self.lista.addItem(vacio)

    def _seleccionar_todas(self) -> None:
        """Selecciona todos los ítems que son canciones reales (no el mensaje vacío)."""
        for indice in range(self.lista.count()):
            item = self.lista.item(indice)
            if item.data(Qt.ItemDataRole.UserRole) is not None:
                item.setSelected(True)

    def _actualizar_contador(self) -> None:
        """Muestra cuántas canciones están seleccionadas en este momento."""
        self.canciones_seleccionadas = self.canciones_seleccionadas_actual()
        total = len(self.canciones_seleccionadas)
        if self.input_nombre.text().strip():
            usuario = self.input_nombre.text().strip()
        else:
            usuario = "Sin usuario"
        self.etiqueta_contador.setText(
            f"Canciones seleccionadas: <b>{total}</b> &nbsp;|&nbsp; Usuario: <b>{usuario}</b>"
        )

    def canciones_seleccionadas_actual(self) -> List[Cancion]:
        """Devuelve la lista de objetos Cancion seleccionados en el QListWidget."""
        seleccion: List[Cancion] = []
        for item in self.lista.selectedItems():
            cancion = item.data(Qt.ItemDataRole.UserRole)
            if isinstance(cancion, Cancion):
                seleccion.append(cancion)
        return seleccion

    # -------------------------------------------------------------- validaciones
    def aceptar(self) -> None:
        """Valida los datos antes de cerrar el diálogo."""
        nombre = self.input_nombre.text().strip()

        # Validación 1: usuario obligatorio
        if not nombre:
            QMessageBox.warning(
                self,
                "Usuario requerido",
                "⚠️ Debes escribir el nombre del usuario para registrar la reproducción.",
            )
            self.input_nombre.setFocus()
            return

        seleccion = self.canciones_seleccionadas_actual()

        # Validación 2: debe haber al menos una canción
        if not seleccion:
            QMessageBox.warning(
                self,
                "Canciones requeridas",
                "⚠️ Debes seleccionar al menos una canción disponible.\n\n"
                "💡 Mantén presionado Ctrl para seleccionar varias.",
            )
            return

        # Validación 3: la canción debe seguir disponible (por si cambió en paralelo)
        no_disponibles = [c.titulo for c in seleccion if not c.disponible]
        if no_disponibles:
            QMessageBox.warning(
                self,
                "Canciones no disponibles",
                "⚠️ Estas canciones ya no están disponibles:\n\n"
                + "\n".join(f"• {t}" for t in no_disponibles),
            )
            return

        # Todo correcto: se guardan los datos y se cierra el diálogo
        self.usuario_nombre = nombre
        self.usuario_telefono = self.input_telefono.text().strip()
        self.canciones_seleccionadas = seleccion
        self.accept()


# ======================================================================================
# DIÁLOGO 3: FINALIZAR REPRODUCCIÓN (devolver)
# ======================================================================================
OBSERVACIONES_SUGERIDAS = [
    "Canción reproducida correctamente.",
    "Se detectó un problema con el archivo.",
    "Audio con buena calidad.",
]


class FinalizarReproduccionDialog(QDialog):
    """
    Devuelve una canción a estado Disponible y permite registrar una observación
    (equivalente a la "devolución" del videoclub, donde se anotaba el estado del película).
    """

    def __init__(self, cancion: Cancion, usuario: str = "Sistema", parent=None) -> None:
        super().__init__(parent)
        self.cancion = cancion
        self.usuario = usuario
        self.observacion = ""
        self.registrar_observacion = True

        self.setWindowTitle("Finalizar Reproducción")
        self.setModal(True)
        self.setMinimumSize(560, 480)

        self._construir_interfaz()

    # ---------------------------------------------------------------- construcción
    def _construir_interfaz(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        titulo = QLabel("⏹️ Finalizar Reproducción")
        titulo.setObjectName("TituloPanel")
        layout.addWidget(titulo)

        # --- Información de la canción que se va a finalizar
        panel_info = QFrame()
        panel_info.setObjectName("PanelFormulario")
        layout_info = QVBoxLayout(panel_info)
        layout_info.setContentsMargins(14, 12, 14, 12)
        layout_info.setSpacing(4)

        nombre = QLabel(f"<b>{self.cancion.titulo}</b> — {self.cancion.artista}")
        nombre.setWordWrap(True)
        nombre.setTextFormat(Qt.TextFormat.RichText)
        layout_info.addWidget(nombre)

        detalle = QLabel(
            f"<span style='color:#a49fc0'>Álbum: {self.cancion.album} &nbsp;|&nbsp; "
            f"Género: {self.cancion.genero} &nbsp;|&nbsp; "
            f"Duración: {self.cancion.duracion}</span>"
        )
        detalle.setWordWrap(True)
        detalle.setTextFormat(Qt.TextFormat.RichText)
        layout_info.addWidget(detalle)

        estado = QLabel(f"Estado actual: <b>{self.cancion.estado}</b>")
        estado.setObjectName("Etiqueta")
        layout_info.addWidget(estado)

        layout.addWidget(panel_info)

        # --- Casilla para decidir si se guarda la observación
        self.check_observacion = QCheckBox("Registrar observación en el historial")
        self.check_observacion.setChecked(True)
        self.check_observacion.toggled.connect(self._cambiar_estado_campos)
        layout.addWidget(self.check_observacion)

        # --- Campo de texto para la observación
        etiqueta = QLabel("Observación (opcional)")
        etiqueta.setObjectName("Etiqueta")
        layout.addWidget(etiqueta)

        self.input_observacion = QTextEdit()
        self.input_observacion.setPlaceholderText("Escribe aquí el resultado de la reproducción...")
        self.input_observacion.setFixedHeight(90)
        layout.addWidget(self.input_observacion)

        # --- Observaciones sugeridas (un clic para usarlas)
        etiqueta_sugeridas = QLabel("Sugerencias rápidas:")
        etiqueta_sugeridas.setObjectName("Etiqueta")
        layout.addWidget(etiqueta_sugeridas)

        fila_sugerencias = QHBoxLayout()
        fila_sugerencias.setSpacing(8)
        for sugerencia in OBSERVACIONES_SUGERIDAS:
            boton = QPushButton(sugerencia)
            boton.setObjectName("Mini")
            boton.setCheckable(True)
            boton.clicked.connect(
                lambda _checked=False, texto=sugerencia: self._usar_sugerencia(texto)
            )
            fila_sugerencias.addWidget(boton)
        layout.addLayout(fila_sugerencias)

        # --- Botones
        self.botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        boton_ok = self.botones.button(QDialogButtonBox.StandardButton.Ok)
        boton_ok.setText("Finalizar")
        boton_ok.setObjectName("Exito")
        self.botones.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        self.botones.accepted.connect(self.aceptar)
        self.botones.rejected.connect(self.reject)
        layout.addWidget(self.botones)

    # ------------------------------------------------------------------ métodos
    def _usar_sugerencia(self, texto: str) -> None:
        """Escribe la sugerencia elegida en el campo de observación."""
        self.input_observacion.setPlainText(texto)
        self.check_observacion.setChecked(True)

    def _cambiar_estado_campos(self, activo: bool) -> None:
        """Activa o desactiva el campo de observación según la casilla."""
        self.input_observacion.setEnabled(activo)

    def aceptar(self) -> None:
        """Guarda lo escrito y cierra el diálogo."""
        self.registrar_observacion = self.check_observacion.isChecked()
        self.observacion = self.input_observacion.toPlainText().strip()
        self.accept()


# ======================================================================================
# DIÁLOGO 4: REGISTRO GLOBAL DE REPRODUCCIONES
# ======================================================================================
class RegistroReproduccionesDialog(QDialog):
    """
    Muestra todos los registros de reproducción creados en el sistema.

    Tabla: ID | Fecha | Usuario | Canciones (QComboBox) | Total de canciones
    """

    def __init__(self, biblioteca, parent=None) -> None:
        super().__init__(parent)
        self.biblioteca = biblioteca
        self._ids_visibles: List[int] = []

        self.setWindowTitle("Registro de Reproducciones")
        self.setModal(True)
        self.resize(880, 560)

        self._construir_interfaz()
        self._cargar_tabla("")

    # ---------------------------------------------------------------- construcción
    def _construir_interfaz(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        # --- Encabezado con título y estadísticas
        panel_titulo = QFrame()
        panel_titulo.setObjectName("Panel")
        layout_titulo = QHBoxLayout(panel_titulo)
        layout_titulo.setContentsMargins(14, 12, 14, 12)

        titulo = QLabel("📋 Registro de Reproducciones")
        titulo.setObjectName("TituloPanel")
        layout_titulo.addWidget(titulo)
        layout_titulo.addStretch(1)

        self.etiqueta_resumen = QLabel()
        self.etiqueta_resumen.setObjectName("Estadistica")
        layout_titulo.addWidget(self.etiqueta_resumen)

        layout.addWidget(panel_titulo)

        # --- Buscador por usuario
        fila_busqueda = QHBoxLayout()
        etiqueta_buscar = QLabel("🔍 Buscar usuario:")
        etiqueta_buscar.setObjectName("Etiqueta")
        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Escribe el nombre del usuario para filtrar...")
        self.input_busqueda.textChanged.connect(self._cargar_tabla)

        boton_limpiar = QPushButton("Limpiar")
        boton_limpiar.setObjectName("Mini")
        boton_limpiar.clicked.connect(self._limpiar_busqueda)

        fila_busqueda.addWidget(etiqueta_buscar)
        fila_busqueda.addWidget(self.input_busqueda, 1)
        fila_busqueda.addWidget(boton_limpiar)
        layout.addLayout(fila_busqueda)

        # --- Tabla de registros
        self.tabla = QTableWidget(0, 5)
        self.tabla.setHorizontalHeaderLabels(
            ["ID", "Fecha", "Usuario", "Canciones", "Total de canciones"]
        )
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        # Doble clic para ver el detalle completo de la reproducción
        self.tabla.cellDoubleClicked.connect(self._ver_detalle)
        layout.addWidget(self.tabla, 1)

        # --- Botones
        botones = QHBoxLayout()
        boton_detalle = QPushButton("🔎 Ver detalle")
        boton_detalle.setObjectName("Fantasma")
        boton_detalle.clicked.connect(self._ver_detalle)

        boton_cerrar = QPushButton("Cerrar")
        boton_cerrar.setObjectName("Primario")
        boton_cerrar.clicked.connect(self.accept)

        botones.addWidget(boton_detalle)
        botones.addStretch(1)
        botones.addWidget(boton_cerrar)
        layout.addLayout(botones)

    # --------------------------------------------------------------------- datos
    def _cargar_tabla(self, texto: str = "") -> None:
        """Llena la tabla con las reproducciones que coincidan con el filtro."""
        self.tabla.setRowCount(0)
        self._ids_visibles = []

        clave = normalizar_texto(texto)
        registros = [
            r
            for r in self.biblioteca.reproducciones
            if not clave or clave in normalizar_texto(r.usuario.nombre)
        ]

        for fila, reproduccion in enumerate(registros):
            self.tabla.insertRow(fila)
            self._ids_visibles.append(reproduccion.id_reproduccion)

            # ID
            item_id = QTableWidgetItem(str(reproduccion.id_reproduccion))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla.setItem(fila, 0, item_id)

            # Fecha
            self.tabla.setItem(fila, 1, QTableWidgetItem(reproduccion.fecha))

            # Usuario (con contacto si existe)
            contacto = reproduccion.usuario.telefono
            texto_usuario = reproduccion.usuario.nombre
            if contacto:
                texto_usuario += f"  ({contacto})"
            self.tabla.setItem(fila, 2, QTableWidgetItem(texto_usuario))

            # Canciones: se usa un QComboBox dentro de la celda para verlas una por una
            combo = QComboBox()
            combo.addItem("Todas las canciones")
            for cancion in reproduccion.canciones:
                combo.addItem(f"{cancion.titulo} — {cancion.artista}")
            combo.setToolTip("Selecciona una canción para verla en detalle")
            self.tabla.setCellWidget(fila, 3, combo)

            # Total de canciones
            item_total = QTableWidgetItem(str(reproduccion.total_canciones))
            item_total.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla.setItem(fila, 4, item_total)

        # Resumen estadístico
        stats = self.biblioteca.estadisticas()
        self.etiqueta_resumen.setText(
            f"Total de reproducciones: <b>{stats['total_reproducciones']}</b> &nbsp;|&nbsp; "
            f"Canciones reproducidas: <b>{stats['canciones_reproducidas']}</b> &nbsp;|&nbsp; "
            f"Usuarios: <b>{stats['total_usuarios']}</b>"
        )

    def _limpiar_busqueda(self) -> None:
        self.input_busqueda.clear()

    # ------------------------------------------------------------------- detalle
    def _ver_detalle(self) -> None:
        """Muestra toda la información de la reproducción seleccionada."""
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.information(
                self,
                "Ver detalle",
                "ℹ️ Selecciona una fila del registro para ver el detalle de la reproducción.",
            )
            return

        id_reproduccion = self._ids_visibles[fila]
        reproduccion = next(
            (r for r in self.biblioteca.reproducciones if r.id_reproduccion == id_reproduccion),
            None,
        )
        if reproduccion is None:
            return

        lista = "\n".join(
            f"• {c.titulo} — {c.artista} ({c.duracion}) [{c.estado}]"
            for c in reproduccion.canciones
        )
        mensaje = (
            f"Reproducción #{reproduccion.id_reproduccion}\n\n"
            f"Usuario: {reproduccion.usuario.nombre}\n"
            f"Contacto: {reproduccion.usuario.telefono or 'no registrado'}\n"
            f"Fecha: {reproduccion.fecha}\n"
            f"Estado del registro: {'Finalizada' if reproduccion.finalizada else 'Activa'}\n\n"
            f"Canciones:\n{lista}\n\n"
            f"Total de canciones: {reproduccion.total_canciones}\n"
            f"Duración total: {reproduccion.duracion_total()}"
        )
        QMessageBox.information(self, "Detalle de reproducción", mensaje)


# ======================================================================================
# DIÁLOGO 5: SOBRE NOSOTROS  (ventana no modal)
# ======================================================================================
class SobreNosotrosDialog(QDialog):
    """
    Ventana informativa independiente.

    No es modal: se puede seguir usando la ventana principal mientras
    esta ventana está abierta (requisito del enunciado).
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Sobre Nosotros")
        self.setModal(False)              # No bloquea la ventana principal
        # Quita el botón de ayuda contextual (?) de la barra de título
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setFixedSize(480, 430)

        self._construir_interfaz()

    def _construir_interfaz(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # --- Icono / título
        icono = QLabel("🎵")
        icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icono.setStyleSheet("font-size: 54px;")
        layout.addWidget(icono)

        titulo = QLabel("🎵 Music Manager")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: 700; color: #ece9f5;")
        layout.addWidget(titulo)

        # --- Descripción
        descripcion = QLabel(
            "Sistema integral para la gestión de canciones, artistas, álbumes "
            "y registros de reproducción."
        )
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descripcion.setWordWrap(True)
        descripcion.setStyleSheet("font-size: 13px; color: #a49fc0; padding: 0 12px;")
        layout.addWidget(descripcion)

        # --- separador
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setStyleSheet("color: #332d48;")
        layout.addWidget(linea)

        # --- Detalle técnico
        detalle = QLabel(
            "<b>Concepto del sistema</b><br>"
            "Canción &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ Película<br>"
            "Usuario &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ Cliente<br>"
            "Reproducción &nbsp;→ Alquiler<br>"
            "Finalizar &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ Devolución<br>"
            "Historial &nbsp;&nbsp;&nbsp;&nbsp;→ Historial"
        )
        detalle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        detalle.setTextFormat(Qt.TextFormat.RichText)
        detalle.setStyleSheet(
            f"font-size: 12px; color: {TEXTO_SUAVE_DIALOGO}; background-color: #1d1a2b;"
            "border: 1px solid #332d48; border-radius: 10px; padding: 14px;"
        )
        layout.addWidget(detalle)

        # --- créditos
        creditos = QLabel("Desarrollado para fines académicos.")
        creditos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        creditos.setStyleSheet("font-size: 12px; color: #ec4899; font-weight: 700;")
        layout.addWidget(creditos)

        # --- Botón cerrar
        boton_cerrar = QPushButton("Cerrar")
        boton_cerrar.setObjectName("Primario")
        boton_cerrar.setMinimumHeight(38)
        boton_cerrar.clicked.connect(self.close)
        layout.addWidget(boton_cerrar)


# ===========================================================================
# 6. VENTANA PRINCIPAL  /  7. FUNCIONES DE GESTION
# ===========================================================================
class VentanaPrincipal(QMainWindow):
    """Ventana principal del sistema de gestión musical."""

    def __init__(self) -> None:
        super().__init__()

        # Modelo de datos en memoria (aquí viven las canciones y reproducciones)
        self.biblioteca = BibliotecaMusical()

        # Lista auxiliar para conservar los botones "Ver Historial" de la tabla
        self._botones_historial: List[QPushButton] = []
        # Referencia a la ventana "Sobre Nosotros" (para que no se cierre sola)
        self._ventana_sobre_nosotros: Optional[SobreNosotrosDialog] = None
        # Permite cerrar la app sin volver a preguntar
        self._salir_confirmado = False

        self._configurar_ventana()
        self._construir_interfaz()
        self._conectar_eventos()
        self._cargar_datos_iniciales()

    # ==============================================================================
    #  CONFIGURACIÓN DE LA VENTANA
    # ==============================================================================
    def _configurar_ventana(self) -> None:
        self.setWindowTitle("Music Manager - Sistema de Gestión Musical")
        self.resize(1000, 650)
        self.setMinimumSize(940, 600)

    # ==============================================================================
    #  CONSTRUCCIÓN DE LA INTERFAZ
    # ==============================================================================
    def _construir_interfaz(self) -> None:
        self.setCentralWidget(self._crear_panel_principal())
        self.statusBar().showMessage("Sistema iniciado. Carga de datos de ejemplo completada.")
        self._crear_menu()

    # ---------------------------------------------------------------- panel raíz
    def _crear_panel_principal(self) -> QWidget:
        """Crea el widget central con todas las secciones."""
        contenedor = QWidget()
        layout_vertical = QVBoxLayout(contenedor)
        layout_vertical.setContentsMargins(0, 0, 0, 0)
        layout_vertical.setSpacing(0)

        layout_vertical.addWidget(self._crear_barra_superior())

        cuerpo = QWidget()
        layout_cuerpo = QVBoxLayout(cuerpo)
        layout_cuerpo.setContentsMargins(14, 12, 14, 10)
        layout_cuerpo.setSpacing(12)

        layout_cuerpo.addWidget(self._crear_formulario_registro())
        layout_cuerpo.addWidget(self._crear_patron_buscador())
        layout_cuerpo.addWidget(self._crear_tabla(), 1)
        layout_cuerpo.addWidget(self._crear_barra_botones())

        layout_vertical.addWidget(cuerpo, 1)
        return contenedor

    # ------------------------------------------------------------ barra superior
    def _crear_barra_superior(self) -> QFrame:
        """
        Cabecera del sistema con dos filas:
            Fila 1 -> Título del sistema + botón "Sobre Nosotros"
            Fila 2 -> Estadísticas (total, disponibles, reservadas, reproducciones)
        """
        barra = QFrame()
        barra.setObjectName("TopBar")
        barra.setFixedHeight(124)

        layout_vertical = QVBoxLayout(barra)
        layout_vertical.setContentsMargins(18, 10, 18, 10)
        layout_vertical.setSpacing(8)

        # ---------------- Fila 1: título y botón
        fila_1 = QHBoxLayout()
        fila_1.setSpacing(14)

        bloque_titulo = QVBoxLayout()
        bloque_titulo.setSpacing(0)

        titulo = QLabel("🎵 Music Manager")
        titulo.setObjectName("TituloApp")
        bloque_titulo.addWidget(titulo)

        subtitulo = QLabel("Sistema de Gestión Musical")
        subtitulo.setObjectName("SubtituloApp")
        bloque_titulo.addWidget(subtitulo)

        fila_1.addLayout(bloque_titulo)
        fila_1.addStretch(1)

        # Botón Sobre Nosotros
        self.boton_sobre_nosotros = QPushButton("ℹ️ Sobre Nosotros")
        self.boton_sobre_nosotros.setObjectName("Fantasma")
        self.boton_sobre_nosotros.setMinimumHeight(40)
        self.boton_sobre_nosotros.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_sobre_nosotros.setToolTip("Muestra la información del sistema")
        fila_1.addWidget(self.boton_sobre_nosotros)

        layout_vertical.addLayout(fila_1)

        # ---------------- Fila 2: estadísticas
        fila_2 = QHBoxLayout()
        fila_2.setSpacing(10)

        # Etiqueta principal con el formato pedido en el enunciado
        self.etiqueta_estadisticas = QLabel()
        self.etiqueta_estadisticas.setObjectName("Estadistica")
        self.etiqueta_estadisticas.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.etiqueta_estadisticas.setMinimumHeight(34)
        fila_2.addWidget(self.etiqueta_estadisticas)

        # Etiqueta secundaria con el total de reproducciones
        self.etiqueta_reproducciones = QLabel()
        self.etiqueta_reproducciones.setObjectName("Estadistica")
        self.etiqueta_reproducciones.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.etiqueta_reproducciones.setMinimumHeight(34)
        fila_2.addWidget(self.etiqueta_reproducciones)

        fila_2.addStretch(1)

        layout_vertical.addLayout(fila_2)

        return barra

    # ------------------------------------------------- formulario de registro
    def _crear_formulario_registro(self) -> QFrame:
        """Formulario para agregar canciones nuevas."""
        panel = QFrame()
        panel.setObjectName("PanelFormulario")

        layout = QHBoxLayout(panel)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        # --- Título del panel
        bloque_titulo = QVBoxLayout()
        titulo_panel = QLabel("＋ Agregar Canción")
        titulo_panel.setObjectName("TituloPanel")
        bloque_titulo.addWidget(titulo_panel)

        subtitulo = QLabel("Registra una canción nueva en la colección")
        subtitulo.setObjectName("Aviso")
        bloque_titulo.addWidget(subtitulo)
        layout.addLayout(bloque_titulo)

        layout.addSpacing(6)

        # --- Campo Título
        self.input_titulo = QLineEdit()
        self.input_titulo.setPlaceholderText("Título *")
        self.input_titulo.setMinimumWidth(150)
        self.input_titulo.setToolTip("Nombre de la canción (obligatorio)")
        layout.addWidget(self.input_titulo, 2)

        # --- Campo Artista
        self.input_artista = QLineEdit()
        self.input_artista.setPlaceholderText("Artista *")
        self.input_artista.setMinimumWidth(130)
        self.input_artista.setToolTip("Artista o grupo (obligatorio)")
        layout.addWidget(self.input_artista, 2)

        # --- Campo Álbum
        self.input_album = QLineEdit()
        self.input_album.setPlaceholderText("Álbum")
        self.input_album.setMinimumWidth(120)
        layout.addWidget(self.input_album, 2)

        # --- Campo Género (QComboBox con el catálogo)
        self.combo_genero = QComboBox()
        self.combo_genero.addItems(GENEROS)
        self.combo_genero.setMinimumWidth(120)
        self.combo_genero.setToolTip("Género musical")
        layout.addWidget(self.combo_genero, 1)

        # --- Campo Duración
        self.input_duracion = QLineEdit()
        self.input_duracion.setPlaceholderText("Duración (3:45)")
        self.input_duracion.setMinimumWidth(110)
        self.input_duracion.setToolTip("Formato: minutos:segundos (ejemplo: 3:45) o total de segundos")
        self.input_duracion.returnPressed.connect(self.registrar_cancion)
        layout.addWidget(self.input_duracion, 1)

        # --- Botón agregar
        self.boton_agregar = QPushButton("＋ Agregar Canción")
        self.boton_agregar.setObjectName("Primario")
        self.boton_agregar.setMinimumHeight(38)
        self.boton_agregar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_agregar.setToolTip("También puedes presionar Enter en el campo Duración")
        layout.addWidget(self.boton_agregar)

        return panel

    # ------------------------------------------------------- buscador y filtros
    def _crear_patron_buscador(self) -> QWidget:
        """Barra con buscador por texto, filtro por género, estado y botón de limpieza."""
        contenedor = QWidget()
        layout = QHBoxLayout(contenedor)
        layout.setContentsMargins(2, 0, 2, 0)
        layout.setSpacing(10)

        # --- Buscador principal
        etiqueta_buscar = QLabel("🔍 Buscar:")
        etiqueta_buscar.setObjectName("Etiqueta")
        layout.addWidget(etiqueta_buscar)

        self.input_buscador = QLineEdit()
        self.input_buscador.setPlaceholderText("Buscar por título, artista o álbum...")
        self.input_buscador.setClearButtonEnabled(True)
        self.input_buscador.setMinimumWidth(240)
        self.input_buscador.setToolTip("La tabla se filtra mientras escribes")
        layout.addWidget(self.input_buscador, 2)

        # --- Filtro por género
        etiqueta_genero = QLabel("Género:")
        etiqueta_genero.setObjectName("Etiqueta")
        layout.addWidget(etiqueta_genero)

        self.combo_filtro_genero = QComboBox()
        self.combo_filtro_genero.addItem("Todos")
        self.combo_filtro_genero.addItems(GENEROS)
        self.combo_filtro_genero.setMinimumWidth(120)
        layout.addWidget(self.combo_filtro_genero, 1)

        # --- Filtro por estado
        etiqueta_estado = QLabel("Estado:")
        etiqueta_estado.setObjectName("Etiqueta")
        layout.addWidget(etiqueta_estado)

        self.combo_filtro_estado = QComboBox()
        self.combo_filtro_estado.addItems(["Todos", Cancion.ESTADO_DISPONIBLE, Cancion.ESTADO_OCUPADA])
        self.combo_filtro_estado.setMinimumWidth(180)
        layout.addWidget(self.combo_filtro_estado, 1)

        # --- Botón limpiar filtros
        self.boton_limpiar = QPushButton("↺ Limpiar")
        self.boton_limpiar.setToolTip("Limpia la búsqueda y los filtros")
        self.boton_limpiar.clicked.connect(self.limpiar_filtros)
        layout.addWidget(self.boton_limpiar)

        # --- Etiqueta con el número de resultados
        self.etiqueta_resultados = QLabel()
        self.etiqueta_resultados.setObjectName("Aviso")
        layout.addWidget(self.etiqueta_resultados)

        return contenedor

    # -------------------------------------------------------------- tabla
    def _crear_tabla(self) -> QTableWidget:
        """Tabla principal con la información de todas las canciones."""
        tabla = QTableWidget(0, 8)
        self.tabla = tabla          # Se guarda como atributo para poder usarla en los métodos
        tabla.setHorizontalHeaderLabels(
            ["ID", "Canción", "Artista", "Álbum", "Género", "Duración", "Estado", "Historial"]
        )
        tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        tabla.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        tabla.setAlternatingRowColors(True)
        tabla.setSortingEnabled(False)
        tabla.verticalHeader().setVisible(False)
        tabla.verticalHeader().setDefaultSectionSize(38)

        # Distribución de columnas
        cabecera = tabla.horizontalHeader()
        cabecera.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for columna, ancho in ((0, 55), (5, 112), (6, 170), (7, 132)):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.Fixed)
            tabla.setColumnWidth(columna, ancho)

        return tabla

    # -------------------------------------------------- barra de botones inferior
    def _crear_barra_botones(self) -> QWidget:
        """Botones de acción del sistema + detalle de la fila seleccionada."""
        contenedor = QFrame()
        contenedor.setObjectName("Panel")
        layout = QHBoxLayout(contenedor)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        # --- Botón registrar reproducción
        self.boton_registrar = QPushButton("▶️ Registrar Reproducción")
        self.boton_registrar.setObjectName("Primario")
        self.boton_registrar.setMinimumHeight(40)
        self.boton_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_registrar.setToolTip("Selecciona canciones disponibles y asígnalas a un usuario")
        layout.addWidget(self.boton_registrar)

        # --- Botón finalizar reproducción
        self.boton_finalizar = QPushButton("⏹️ Finalizar Reproducción")
        self.boton_finalizar.setObjectName("Exito")
        self.boton_finalizar.setMinimumHeight(40)
        self.boton_finalizar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_finalizar.setToolTip("Devuelve la canción seleccionada a estado Disponible")
        layout.addWidget(self.boton_finalizar)

        # --- Botón registro global
        self.boton_registro = QPushButton("📋 Ver Registro de Reproducciones")
        self.boton_registro.setObjectName("Fantasma")
        self.boton_registro.setMinimumHeight(40)
        self.boton_registro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_registro.setToolTip("Muestra todos los registros de reproducción del sistema")
        layout.addWidget(self.boton_registro)

        layout.addStretch(1)

        # --- Detalle de la fila seleccionada
        self.etiqueta_seleccion = QLabel("Sin selección")
        self.etiqueta_seleccion.setObjectName("Aviso")
        layout.addWidget(self.etiqueta_seleccion)

        return contenedor

    # ------------------------------------------------------------------- menú
    def _crear_menu(self) -> None:
        """Menú superior con accesos rápidos a las funciones principales."""
        menu = self.menuBar()

        menu_archivo = menu.addMenu("&Archivo")
        menu_archivo.addAction("Agregar canción", self.abrir_registro_cancion)
        menu_archivo.addSeparator()
        menu_archivo.addAction("Ver registro de reproducciones", self.ver_registro_reproducciones)
        menu_archivo.addSeparator()
        menu_archivo.addAction("Salir", self.close)

        menu_sistema = menu.addMenu("&Sistema")
        menu_sistema.addAction("Registrar reproducción", self.registrar_reproduccion)
        menu_sistema.addAction("Finalizar reproducción", self.finalizar_reproduccion)
        menu_sistema.addSeparator()
        menu_sistema.addAction("Cargar datos de ejemplo", self.cargar_datos_ejemplo)
        menu_sistema.addAction("Vaciar colección", self.vaciar_coleccion)
        menu_sistema.addSeparator()
        menu_sistema.addAction("Sobre Nosotros", self.mostrar_sobre_nosotros)

        menu_ayuda = menu.addMenu("A&yuda")
        menu_ayuda.addAction("Historial de canción", self.abrir_historial_seleccionada)
        menu_ayuda.addAction("Limpiar filtros", self.limpiar_filtros)

    # ==============================================================================
    #  CONEXIÓN DE EVENTOS
    # ==============================================================================
    def _conectar_eventos(self) -> None:
        """Conecta los botones y campos con sus métodos."""
        # Botones
        self.boton_agregar.clicked.connect(self.registrar_cancion)
        self.boton_registrar.clicked.connect(self.registrar_reproduccion)
        self.boton_finalizar.clicked.connect(self.finalizar_reproduccion)
        self.boton_registro.clicked.connect(self.ver_registro_reproducciones)
        self.boton_sobre_nosotros.clicked.connect(self.mostrar_sobre_nosotros)

        # Búsqueda y filtros: se actualizan mientras el usuario escribe
        self.input_buscador.textChanged.connect(self.actualizar_tabla)
        self.combo_filtro_genero.currentTextChanged.connect(self.actualizar_tabla)
        self.combo_filtro_estado.currentTextChanged.connect(self.actualizar_tabla)

        # Enter en el formulario también agrega la canción
        for campo in (self.input_titulo, self.input_artista, self.input_album):
            campo.returnPressed.connect(self.registrar_cancion)

        # Doble clic en una fila abre el historial de esa canción
        self.tabla.cellDoubleClicked.connect(self._doble_clic_fila)
        # Al cambiar la selección se actualiza la etiqueta de detalle inferior
        self.tabla.itemSelectionChanged.connect(self._al_seleccionar_fila)

        # Atajos de teclado
        QShortcut(QKeySequence("Ctrl+F"), self, activated=self.input_buscador.setFocus)
        QShortcut(QKeySequence("F2"), self, activated=self.registrar_reproduccion)
        QShortcut(QKeySequence("F3"), self, activated=self.finalizar_reproduccion)

    def _cargar_datos_iniciales(self) -> None:
        """Carga los datos de ejemplo y muestra la tabla por primera vez."""
        self.cargar_datos_ejemplo()

    # ==============================================================================
    #  FUNCIONES DE GESTIÓN
    # ==============================================================================
    def cargar_datos_ejemplo(self) -> None:
        """Carga las canciones y reproducciones de ejemplo del sistema."""

        if self.biblioteca.canciones:
            # Si la colección ya tiene datos, pregunta antes de duplicar
            respuesta = QMessageBox.question(
                self,
                "Cargar datos de ejemplo",
                "⚠️ La colección ya contiene canciones.\n\n"
                "¿Deseas vaciarla y cargar los datos de ejemplo otra vez?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if respuesta != QMessageBox.StandardButton.Yes:
                return
            self.biblioteca = BibliotecaMusical()

        cargar_datos_ejemplo(self.biblioteca)
        self.limpiar_filtros()
        self.actualizar_tabla()
        self.statusBar().showMessage(
            f"Datos de ejemplo cargados: {len(self.biblioteca.canciones)} canciones."
        )

    def vaciar_coleccion(self) -> None:
        """Borra todas las canciones, usuarios y reproducciones."""
        if not self.biblioteca.canciones:
            QMessageBox.information(
                self, "Colección vacía", "ℹ️ La colección de canciones ya está vacía."
            )
            return

        respuesta = QMessageBox.question(
            self,
            "Vaciar colección",
            "⚠️ Esta acción eliminará TODAS las canciones, usuarios y reproducciones.\n\n"
            "¿Deseas continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if respuesta != QMessageBox.StandardButton.Yes:
            return

        self.biblioteca = BibliotecaMusical()
        self.limpiar_filtros()
        self.actualizar_tabla()
        self.statusBar().showMessage("Colección vaciada correctamente.")

    def limpiar_filtros(self) -> None:
        """Limpia el buscador y los filtros, y vuelve a mostrar todo."""
        self.input_buscador.blockSignals(True)
        self.input_buscador.clear()
        self.input_buscador.blockSignals(False)

        for combo in (self.combo_filtro_genero, self.combo_filtro_estado):
            combo.blockSignals(True)
            combo.setCurrentIndex(0)
            combo.blockSignals(False)

        self.actualizar_tabla()

    # ------------------------------------------------- 1) Registrar canción
    def abrir_registro_cancion(self) -> None:
        """Enfoca el formulario de registro para agregar una canción rápidamente."""
        self.input_titulo.setFocus()
        self.input_titulo.selectAll()
        self.statusBar().showMessage("Escribe el título, artista y duración de la nueva canción.")

    def registrar_cancion(self) -> None:
        """
        Valida el formulario y guarda la canción nueva en la colección.
        Si todo está correcto, la canción aparece inmediatamente en la tabla.
        """
        titulo = self.input_titulo.text().strip()
        artista = self.input_artista.text().strip()
        album = self.input_album.text().strip()
        genero = self.combo_genero.currentText()
        duracion_texto = self.input_duracion.text().strip()

        # --- Validación 1: título obligatorio
        if not titulo:
            self._advertencia(
                "Falta el título",
                "⚠️ El título de la canción es obligatorio.\n\nPor ejemplo: Blinding Lights",
                self.input_titulo,
            )
            return

        # --- Validación 2: artista obligatorio
        if not artista:
            self._advertencia(
                "Falta el artista",
                "⚠️ El artista de la canción es obligatorio.\n\nPor ejemplo: The Weeknd",
                self.input_artista,
            )
            return

        # --- Validación 3: duración válida
        ok, duracion, mensaje_error = interpretar_duracion(duracion_texto)
        if not ok:
            self._advertencia(
                "Duración inválida",
                f"⚠️ {mensaje_error}\n\nEjemplos válidos: 3:45  |  225  |  04:02",
                self.input_duracion,
            )
            return

        # --- Si todo está bien, se guarda la canción
        cancion = self.biblioteca.agregar_cancion(
            titulo=titulo,
            artista=artista,
            album=album if album else "Sin álbum",
            genero=genero,
            duracion=formatear_duracion(duracion),
        )

        # Se limpian los campos del formulario
        self.input_titulo.clear()
        self.input_artista.clear()
        self.input_album.clear()
        self.input_duracion.clear()
        self.input_titulo.setFocus()

        # La tabla y las estadísticas se actualizan al instante
        self.actualizar_tabla()
        self._seleccionar_en_tabla(cancion.id_cancion)

        # Mensaje de confirmación
        QMessageBox.information(
            self,
            "Canción agregada",
            f"✅ Canción agregada correctamente\n\n"
            f"Canción: {cancion.titulo}\n"
            f"Artista: {cancion.artista}\n"
            f"Álbum: {cancion.album}\n"
            f"Género: {cancion.genero}\n"
            f"Duración: {cancion.duracion}\n"
            f"ID asignado: {cancion.id_cancion}",
        )
        self.statusBar().showMessage(f"Canción '{cancion.titulo}' agregada a la colección.")

    def _advertencia(self, titulo: str, mensaje: str, campo=None) -> None:
        """Muestra un QMessageBox de advertencia y enfoca el campo con el error."""
        QMessageBox.warning(self, titulo, mensaje)
        if campo is not None:
            campo.setFocus()
            campo.selectAll()

    # ------------------------------------------- 2) Registrar reproducción
    def registrar_reproduccion(self) -> None:
        """
        Abre el diálogo para registrar una reproducción.
        Al confirmar, se crea el Usuario, la Reproducción y cambian los estados.
        """
        if not self.biblioteca.canciones_disponibles():
            QMessageBox.warning(
                self,
                "Sin canciones disponibles",
                "⚠️ No hay canciones disponibles en este momento.\n\n"
                "Agrega una canción nueva o finaliza alguna reproducción para continuar.",
            )
            return

        dialogo = ReproduccionDialog(self.biblioteca, self)
        if dialogo.exec() != ReproduccionDialog.DialogCode.Accepted:
            return

        # Se crea (o se reutiliza) el objeto Usuario
        usuario = self.biblioteca.obtener_o_crear_usuario(
            dialogo.usuario_nombre, dialogo.usuario_telefono
        )

        # Se crea el objeto Reproducción y se guardan las canciones
        reproduccion = self.biblioteca.registrar_reproduccion(usuario, dialogo.canciones_seleccionadas)

        # Refresco inmediato de la interfaz
        self.actualizar_tabla()
        self._seleccionar_en_tabla(dialogo.canciones_seleccionadas[0].id_cancion)

        # Mensaje de confirmación con el detalle solicitado
        lista_canciones = "\n".join(f"• {titulo}" for titulo in reproduccion.titulos_canciones())
        QMessageBox.information(
            self,
            "Reproducción registrada",
            f"✅ Reproducción registrada correctamente\n\n"
            f"Usuario: {usuario.nombre}\n\n"
            f"Canciones:\n{lista_canciones}\n\n"
            f"Total de canciones: {reproduccion.total_canciones}\n"
            f"Duración total: {reproduccion.duracion_total()}\n"
            f"Número de registro: #{reproduccion.id_reproduccion}",
        )
        self.statusBar().showMessage(
            f"Reproducción #{reproduccion.id_reproduccion} registrada para {usuario.nombre}."
        )

    # ------------------------------------------- 3) Finalizar reproducción
    def finalizar_reproduccion(self) -> None:
        """
        Devuelve la canción seleccionada a estado Disponible (equivalente a la devolución).
        Permite registrar una observación opcional en el historial de la canción.
        """
        cancion = self.cancion_seleccionada()

        # Validación: debe haber una fila seleccionada
        if cancion is None:
            QMessageBox.warning(
                self,
                "Fila no seleccionada",
                "⚠️ Debes seleccionar una canción de la tabla.\n\n"
                "Haz clic en la fila de la canción que deseas finalizar y presiona el botón otra vez.",
            )
            return

        # Validación: la canción debe estar Reproduciendo/Reservada
        if cancion.disponible:
            QMessageBox.warning(
                self,
                "Canción ya disponible",
                f"⚠️ La canción \"{cancion.titulo}\" ya está DISPONIBLE.\n\n"
                "Solo puedes finalizar canciones que estén en estado "
                "\"Reproduciendo/Reservada\".",
            )
            return

        # Se averigua qué usuario tenía la canción para anotarlo en el historial
        reproduccion = self.biblioteca.reproduccion_de(cancion)
        nombre_usuario = reproduccion.usuario.nombre if reproduccion else "Sistema"

        # Se abre el diálogo opcional de observación
        dialogo = FinalizarReproduccionDialog(cancion, nombre_usuario, self)
        if dialogo.exec() != FinalizarReproduccionDialog.DialogCode.Accepted:
            self.statusBar().showMessage("Finalización cancelada.")
            return

        # Se aplica el cambio de estado y se guarda la observación
        self.biblioteca.finalizar_cancion(
            cancion,
            dialogo.observacion if dialogo.registrar_observacion else "",
            nombre_usuario,
        )

        # Refresco de la interfaz
        self.actualizar_tabla()
        self._seleccionar_en_tabla(cancion.id_cancion)

        mensaje = (
            f"✅ Reproducción finalizada correctamente\n\n"
            f"Canción: {cancion.titulo}\n"
            f"Artista: {cancion.artista}\n"
            f"Nuevo estado: {cancion.estado}\n"
            f"Usuario asociado: {nombre_usuario}"
        )
        if dialogo.registrar_observacion and dialogo.observacion:
            mensaje += f"\n\nObservación guardada en el historial:\n\"{dialogo.observacion}\""
        elif not dialogo.registrar_observacion:
            mensaje += "\n\nNo se registró ninguna observación en el historial."

        QMessageBox.information(self, "Reproducción finalizada", mensaje)
        self.statusBar().showMessage(
            f"Reproducción finalizada: '{cancion.titulo}' vuelve a estar Disponible."
        )

    # ------------------------------------------------- 4) Ver historial
    def abrir_historial_seleccionada(self) -> None:
        """Abre el historial de observaciones de la canción seleccionada."""
        cancion = self.cancion_seleccionada()
        if cancion is None:
            QMessageBox.warning(
                self,
                "Fila no seleccionada",
                "⚠️ Debes seleccionar una canción de la tabla para ver su historial.",
            )
            return
        self.abrir_historial(cancion)

    def abrir_historial(self, cancion: Cancion) -> None:
        """Abre la ventana Historial - [nombre de la canción]."""
        dialogo = HistorialDialog(cancion, self)
        dialogo.exec()

    def abrir_historial_por_id(self, id_cancion: int) -> None:
        """Abre el historial usando directamente el ID (usado por el botón de la tabla)."""
        cancion = self.biblioteca.obtener_cancion(id_cancion)
        if cancion is None:
            QMessageBox.warning(
                self,
                "Canción no encontrada",
                "⚠️ No fue posible encontrar la canción con ese identificador.",
            )
            return
        self.abrir_historial(cancion)

    def _doble_clic_fila(self, fila: int, columna: int) -> None:
        """Doble clic en una fila = abrir el historial de esa canción."""
        cancion = self.cancion_de_fila(fila)
        if cancion is not None:
            self.abrir_historial(cancion)

    # --------------------------------------- 5) Registro global de reproducciones
    def ver_registro_reproducciones(self) -> None:
        """Abre la ventana con todos los registros de reproducción."""
        dialogo = RegistroReproduccionesDialog(self.biblioteca, self)
        dialogo.exec()

    # ------------------------------------------------ 6) Sobre nosotros
    def mostrar_sobre_nosotros(self) -> None:
        """
        Abre la ventana "Sobre Nosotros" como ventana independiente (no modal).
        Si ya está abierta, solo la pone al frente.
        """
        if self._ventana_sobre_nosotros is None:
            self._ventana_sobre_nosotros = SobreNosotrosDialog(self)
            # Cuando el usuario la cierre, se elimina la referencia
            self._ventana_sobre_nosotros.destroyed.connect(self._olvidar_ventana_sobre_nosotros)

        self._ventana_sobre_nosotros.show()
        self._ventana_sobre_nosotros.raise_()
        self._ventana_sobre_nosotros.activateWindow()

    def _olvidar_ventana_sobre_nosotros(self, *args) -> None:
        self._ventana_sobre_nosotros = None

    # ==============================================================================
    #  ACTUALIZACIÓN DE LA INTERFAZ
    # ==============================================================================
    def actualizar_tabla(self) -> None:
        """
        Vuelve a llenar la tabla con las canciones que cumplen el filtro actual.
        Se llama después de cada acción para que los cambios se vean al instante.
        """
        tabla = self.tabla

        # 1) Se limpian los datos anteriores
        self._botones_historial.clear()
        tabla.setRowCount(0)

        # 2) Se aplica el filtro de búsqueda, género y estado
        canciones = self.biblioteca.filtrar_canciones(
            texto=self.input_buscador.text(),
            genero=self.combo_filtro_genero.currentText(),
            estado=self.combo_filtro_estado.currentText(),
        )

        # 3) Se agrega una fila por canción
        for fila, cancion in enumerate(canciones):
            tabla.insertRow(fila)
            tabla.setRowHeight(fila, 38)

            # ID
            item_id = QTableWidgetItem(str(cancion.id_cancion))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(fila, 0, item_id)

            # Canción (con ícono)
            tabla.setItem(fila, 1, self._crear_item(f"🎵 {cancion.titulo}"))

            # Artista
            tabla.setItem(fila, 2, self._crear_item(cancion.artista))

            # Álbum
            tabla.setItem(fila, 3, self._crear_item(cancion.album))

            # Género
            tabla.setItem(fila, 4, self._crear_item(cancion.genero))

            # Duración
            item_duracion = QTableWidgetItem(cancion.duracion)
            item_duracion.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(fila, 5, item_duracion)

            # Estado
            item_estado = QTableWidgetItem(cancion.estado)
            item_estado.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if cancion.disponible:
                item_estado.setForeground(Qt.GlobalColor.green)
            else:
                item_estado.setForeground(Qt.GlobalColor.red)
            tabla.setItem(fila, 6, item_estado)

            # Historial: botón "📜 Ver Historial"
            boton_historial = QPushButton("📜 Ver Historial")
            boton_historial.setObjectName("Mini")
            boton_historial.setCursor(Qt.CursorShape.PointingHandCursor)
            boton_historial.setToolTip(
                f"Ver historial de '{cancion.titulo}' "
                f"({cancion.total_observaciones} observaciones)"
            )
            # Al presionarlo se abre el historial de ESA canción
            boton_historial.clicked.connect(
                lambda _checked=False, id_cancion=cancion.id_cancion:
                self.abrir_historial_por_id(id_cancion)
            )
            tabla.setCellWidget(fila, 7, boton_historial)
            self._botones_historial.append(boton_historial)

        # 4) Se actualizan las estadísticas y el contador de resultados
        self._actualizar_estadisticas()
        self._actualizar_contador_resultados(len(canciones))

    def _crear_item(self, texto: str) -> QTableWidgetItem:
        """Crea un QTableWidgetItem con el formato del tema."""
        item = QTableWidgetItem(texto)
        item.setToolTip(texto)
        return item

    def _actualizar_contador_resultados(self, cantidad: int) -> None:
        """Muestra cuántas canciones están visibles con el filtro actual."""
        total = len(self.biblioteca.canciones)
        if cantidad == total:
            self.etiqueta_resultados.setText(f"Mostrando {cantidad} de {total} canciones")
        else:
            self.etiqueta_resultados.setText(f"Mostrando {cantidad} de {total} canciones (filtrado)")

    def _actualizar_estadisticas(self) -> None:
        """Recalcula los números de la parte superior de la ventana."""
        stats = self.biblioteca.estadisticas()
        self.etiqueta_estadisticas.setText(
            f"Total de canciones: <b>{stats['total_canciones']}</b> &nbsp;|&nbsp; "
            f"Disponibles: <b>{stats['disponibles']}</b> &nbsp;|&nbsp; "
            f"Reproduciéndose/Reservadas: <b>{stats['reservadas']}</b>"
        )
        self.etiqueta_estadisticas.setTextFormat(Qt.TextFormat.RichText)

        self.etiqueta_reproducciones.setText(
            f"🎧 Reproducciones: <b>{stats['total_reproducciones']}</b>"
        )
        self.etiqueta_reproducciones.setTextFormat(Qt.TextFormat.RichText)

        self.setWindowTitle(
            "Music Manager - Sistema de Gestión Musical  |  "
            f"{stats['total_canciones']} canciones  |  "
            f"{stats['total_reproducciones']} reproducciones"
        )

    # ==============================================================================
    #  AYUDAS PARA LA TABLA
    # ==============================================================================
    def cancion_de_fila(self, fila: int) -> Optional[Cancion]:
        """Devuelve el objeto Cancion que está en la fila indicada."""
        if fila < 0:
            return None
        item = self.tabla.item(fila, 0)
        if item is None:
            return None
        return self.biblioteca.obtener_cancion(int(item.text()))

    def cancion_seleccionada(self) -> Optional[Cancion]:
        """Devuelve la canción de la fila actualmente seleccionada."""
        tabla = self.tabla
        fila = tabla.currentRow()
        if fila < 0:
            return None
        return self.cancion_de_fila(fila)

    def _seleccionar_en_tabla(self, id_cancion: int) -> None:
        """Selecciona y enfoca la fila de una canción (si está visible)."""
        tabla = self.tabla
        for fila in range(tabla.rowCount()):
            item = tabla.item(fila, 0)
            if item is not None and int(item.text()) == id_cancion:
                tabla.selectRow(fila)
                return

    def _al_seleccionar_fila(self) -> None:
        """Muestra en la barra inferior el detalle de la canción seleccionada."""
        cancion = self.cancion_seleccionada()
        if cancion is None:
            self.etiqueta_seleccion.setText("Sin selección")
            return
        self.etiqueta_seleccion.setText(
            f"Seleccionada: {cancion.titulo} — {cancion.artista} "
            f"({cancion.estado})"
        )

    # ==============================================================================
    #  CIERRE DE LA APLICACIÓN
    # ==============================================================================
    def closeEvent(self, evento: QCloseEvent) -> None:
        """
        Se ejecuta al cerrar la ventana principal.
        Muestra la confirmación "¿Estás seguro que quieres salir del sistema?"
        """
        if self._salir_confirmado:
            evento.accept()
            return

        # Se construye el cuadro de confirmación con botones personalizados
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle("Confirmación de salida")
        mensaje.setIcon(QMessageBox.Icon.Warning)
        mensaje.setText("⚠️ ¿Estás seguro que quieres salir del sistema?")
        mensaje.setInformativeText(
            "Los datos de la colección se perderán al cerrar el programa."
        )

        boton_aceptar = mensaje.addButton("Aceptar", QMessageBox.ButtonRole.AcceptRole)
        boton_cancelar = mensaje.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)
        boton_cancelar.setObjectName("Primario")
        mensaje.setDefaultButton(boton_cancelar)
        mensaje.exec()

        if mensaje.clickedButton() is boton_aceptar:
            self._salir_confirmado = True
            evento.accept()
        else:
            evento.ignore()


# ======================================================================================
#  8. PUNTO DE ENTRADA DE LA APLICACION
# ======================================================================================
def main() -> int:
    """
    Crea y ejecuta la aplicacion.

    1) Instancia de QApplication (obligatoria en toda app de PyQt6).
    2) Se aplica la hoja de estilos (tema oscuro) y la fuente base.
    3) Se crea y muestra la ventana principal.
    4) Se inicia el bucle de eventos de Qt.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("Music Manager")
    app.setApplicationDisplayName("Music Manager")

    aplicar_estilos(app)

    ventana = VentanaPrincipal()
    ventana.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
