# -*- coding: utf-8 -*-
"""
Sistema 1: Registro de Estudiantes
Tema: Académico (verde/azul), ventana principal QMainWindow
Usa: QLabel, QPushButton, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout,
QGridLayout, QFormLayout, QCheckBox, QRadioButton, QComboBox,
QApplication, QWidget, QMainWindow, QDialog

Funciones: Registrar, Limpiar, Editar, Eliminar, Buscar, Mostrar info,
Validar, Confirmaciones, opciones de selección (carrera, género, intereses).
"""
import sys
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QDialog,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFormLayout,
    QCheckBox,
    QRadioButton,
    QComboBox,
    QGroupBox,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSplitter,
    QFrame,
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt


class DetalleEstudianteDialog(QDialog):
    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detalles del Estudiante")
        self.setFixedSize(420, 380)
        self.setModal(True)

        layout = QVBoxLayout(self)

        titulo = QLabel("Información registrada del estudiante")
        titulo.setAlignment(Qt.AlignCenter)
        f_t = QFont()
        f_t.setPointSize(12)
        f_t.setBold(True)
        titulo.setFont(f_t)
        layout.addWidget(titulo)

        form = QFormLayout()
        form.addRow("Código:", QLabel(datos.get("codigo", "-")))
        form.addRow("Nombre completo:", QLabel(datos.get("nombre", "-")))
        form.addRow("Carrera:", QLabel(datos.get("carrera", "-")))
        form.addRow("Género:", QLabel(datos.get("genero", "-")))
        form.addRow("Teléfono:", QLabel(datos.get("telefono", "-")))
        form.addRow("Correo:", QLabel(datos.get("correo", "-")))
        form.addRow("Fecha de registro:", QLabel(datos.get("fecha", "-")))
        form.addRow("Intereses:", QLabel(datos.get("intereses", "-") or "-"))
        form.addRow("Notas:", QLabel(datos.get("notas", "-") or "-"))
        layout.addLayout(form)

        botones = QHBoxLayout()
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setDefault(True)
        btn_cerrar.clicked.connect(self.accept)
        botones.addStretch()
        botones.addWidget(btn_cerrar)
        layout.addLayout(botones)


class ConfirmacionDialog(QDialog):
    def __init__(self, mensaje, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmación")
        self.setFixedSize(340, 130)
        self.setModal(True)

        v = QVBoxLayout(self)
        lbl = QLabel(mensaje)
        lbl.setWordWrap(True)
        lbl.setAlignment(Qt.AlignCenter)
        v.addWidget(lbl)

        h = QHBoxLayout()
        btn_si = QPushButton("Sí")
        btn_no = QPushButton("No")
        btn_no.setDefault(True)
        btn_si.clicked.connect(self.accept)
        btn_no.clicked.connect(self.reject)
        h.addStretch()
        h.addWidget(btn_si)
        h.addWidget(btn_no)
        h.addStretch()
        v.addLayout(h)


class SistemaEstudiantes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema 1 - Registro de Estudiantes")
        self.setMinimumSize(960, 640)
        self.registros = []
        self.editando_index = -1
        self._setup_ui()
        self._aplicar_estilo()
        self._mostrar_tabla()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # Título
        titulo = QLabel("Registro Académico de Estudiantes")
        f_t = QFont()
        f_t.setPointSize(16)
        f_t.setBold(True)
        titulo.setFont(f_t)
        titulo.setAlignment(Qt.AlignCenter)
        root.addWidget(titulo)

        separador_top = QFrame()
        separador_top.setFrameShape(QFrame.HLine)
        root.addWidget(separador_top)

        splitter = QSplitter(Qt.Horizontal)
        root.addWidget(splitter, stretch=1)

        # Panel izquierdo: formulario
        panel_form = QWidget()
        v_form = QVBoxLayout(panel_form)
        v_form.setContentsMargins(10, 10, 10, 10)
        v_form.setSpacing(10)

        gb_datos = QGroupBox("Datos del Estudiante")
        v_gb = QVBoxLayout(gb_datos)

        # QFormLayout para organizar campos
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_layout.setFormAlignment(Qt.AlignTop)
        form_layout.setHorizontalSpacing(12)
        form_layout.setVerticalSpacing(8)

        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("Ej. ES-001")
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre y apellidos")
        self.txt_telefono = QLineEdit()
        self.txt_telefono.setPlaceholderText("999-999-999")
        self.txt_correo = QLineEdit()
        self.txt_correo.setPlaceholderText("correo@ejemplo.com")

        self.cmb_carrera = QComboBox()
        self.cmb_carrera.addItems(
            ["-- Seleccionar --", "Ingeniería de Sistemas", "Administración", "Contabilidad", "Derecho", "Psicología"]
        )

        # Género con QRadioButton (horizontal)
        self.rb_masc = QRadioButton("Masculino")
        self.rb_fem = QRadioButton("Femenino")
        self.rb_otro = QRadioButton("Otro")
        h_gen = QHBoxLayout()
        h_gen.addWidget(self.rb_masc)
        h_gen.addWidget(self.rb_fem)
        h_gen.addWidget(self.rb_otro)
        h_gen.addStretch()

        form_layout.addRow("Código *:", self.txt_codigo)
        form_layout.addRow("Nombre completo *:", self.txt_nombre)
        form_layout.addRow("Carrera *:", self.cmb_carrera)
        form_layout.addRow("Género *:", h_gen)
        form_layout.addRow("Teléfono:", self.txt_telefono)
        form_layout.addRow("Correo:", self.txt_correo)

        v_gb.addLayout(form_layout)

        # Intereses con QCheckBox (QGridLayout)
        gb_intereses = QGroupBox("Intereses académicos")
        grid_int = QGridLayout(gb_intereses)
        self.chk_progra = QCheckBox("Programación")
        self.chk_redes = QCheckBox("Redes")
        self.chk_ia = QCheckBox("IA")
        self.chk_base = QCheckBox("Base de Datos")
        self.chk_mark = QCheckBox("Marketing")
        grid_int.addWidget(self.chk_progra, 0, 0)
        grid_int.addWidget(self.chk_redes, 0, 1)
        grid_int.addWidget(self.chk_ia, 1, 0)
        grid_int.addWidget(self.chk_base, 1, 1)
        grid_int.addWidget(self.chk_mark, 2, 0, 1, 2)
        v_gb.addWidget(gb_intereses)

        # Notas con QTextEdit
        gb_notas = QGroupBox("Notas / Observaciones")
        v_notas = QVBoxLayout(gb_notas)
        self.txt_notas = QTextEdit()
        self.txt_notas.setPlaceholderText("Escriba observaciones adicionales...")
        self.txt_notas.setFixedHeight(90)
        v_notas.addWidget(self.txt_notas)
        v_gb.addWidget(gb_notas)

        v_form.addWidget(gb_datos)

        # Botones (QHBoxLayout)
        h_botones = QHBoxLayout()
        self.btn_registrar = QPushButton("Registrar")
        self.btn_limpiar = QPushButton("Limpiar campos")
        self.btn_editar = QPushButton("Guardar edición")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_buscar = QPushButton("Buscar")
        self.btn_mostrar = QPushButton("Mostrar información")
        self.btn_cancelar_edit = QPushButton("Cancelar edición")
        self.btn_cancelar_edit.setVisible(False)
        self.btn_editar.setEnabled(False)

        h_botones.addWidget(self.btn_registrar)
        h_botones.addWidget(self.btn_limpiar)
        h_botones.addWidget(self.btn_editar)
        h_botones.addWidget(self.btn_cancelar_edit)
        h_botones.addWidget(self.btn_eliminar)
        h_botones.addWidget(self.btn_buscar)
        h_botones.addWidget(self.btn_mostrar)
        h_botones.addStretch()
        v_form.addLayout(h_botones)

        splitter.addWidget(panel_form)

        # Panel derecho: tabla
        panel_tabla = QWidget()
        v_tab = QVBoxLayout(panel_tabla)
        v_tab.setContentsMargins(8, 8, 8, 8)
        v_tab.setSpacing(8)

        lbl_reg = QLabel("Registros almacenados (en memoria)")
        f_r = QFont()
        f_r.setBold(True)
        lbl_reg.setFont(f_r)
        v_tab.addWidget(lbl_reg)

        self.tabla = QTableWidget(0, 8)
        self.tabla.setHorizontalHeaderLabels(
            ["Código", "Nombre", "Carrera", "Género", "Teléfono", "Correo", "Fecha", "Intereses"]
        )
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setAlternatingRowColors(True)
        v_tab.addWidget(self.tabla)

        h_info = QHBoxLayout()
        self.lbl_total = QLabel("Total de registros: 0")
        h_info.addWidget(self.lbl_total)
        h_info.addStretch()
        v_tab.addLayout(h_info)

        splitter.addWidget(panel_tabla)
        splitter.setSizes([420, 540])

        # Footer
        pie = QHBoxLayout()
        pie.addWidget(QLabel("PySide6 • Sistema 1 • QMainWindow + QDialog"))
        pie.addStretch()
        root.addLayout(pie)

        # Conexiones
        self.btn_registrar.clicked.connect(self.registrar)
        self.btn_limpiar.clicked.connect(self.limpiar_campos)
        self.btn_editar.clicked.connect(self.guardar_edicion)
        self.btn_cancelar_edit.clicked.connect(self.cancelar_edicion)
        self.btn_eliminar.clicked.connect(self.eliminar)
        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_mostrar.clicked.connect(self.mostrar_informacion)
        self.tabla.itemDoubleClicked.connect(lambda: self.cargar_para_editar())

    def _aplicar_estilo(self):
        self.setStyleSheet(
            """
            QMainWindow { background: #f5f9f7; }
            QWidget { font-family: 'Segoe UI', sans-serif; }
            QLabel { color: #1f2937; }
            QGroupBox { border: 1px solid #c9d8e6; border-radius: 8px; padding: 10px; margin-top: 6px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; color: #0f766e; font-weight: bold; }
            QLineEdit, QTextEdit, QComboBox { border: 1px solid #cbd5e1; border-radius: 6px; padding: 6px; background: #ffffff; }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border: 2px solid #0ea5e9; }
            QPushButton { background: #0f766e; color: white; border: none; border-radius: 6px; padding: 7px 12px; }
            QPushButton:hover { background: #115e59; }
            QPushButton:pressed { background: #0b534d; }
            QPushButton:disabled { background: #9ca3af; }
            QTableWidget { background: #ffffff; gridline-color: #e5e7eb; border: 1px solid #e5e7eb; border-radius: 6px; }
            QHeaderView::section { background: #e6f7f5; padding: 6px; border: none; font-weight: bold; }
            QSplitter::handle { background: #d1d5db; width: 3px; }
            QRadioButton, QCheckBox { spacing: 6px; }
            QFrame { color: #d1d5db; }
            """
        )

    def _obtener_genero(self):
        if self.rb_masc.isChecked():
            return "Masculino"
        if self.rb_fem.isChecked():
            return "Femenino"
        if self.rb_otro.isChecked():
            return "Otro"
        return ""

    def _obtener_intereses(self):
        intereses = []
        if self.chk_progra.isChecked():
            intereses.append("Programación")
        if self.chk_redes.isChecked():
            intereses.append("Redes")
        if self.chk_ia.isChecked():
            intereses.append("IA")
        if self.chk_base.isChecked():
            intereses.append("Base de Datos")
        if self.chk_mark.isChecked():
            intereses.append("Marketing")
        return ", ".join(intereses)

    def _establecer_intereses(self, texto):
        t = (texto or "").lower()
        self.chk_progra.setChecked("programación" in t or "programacion" in t)
        self.chk_redes.setChecked("redes" in t)
        self.chk_ia.setChecked("ia" in t)
        self.chk_base.setChecked("base" in t)
        self.chk_mark.setChecked("marketing" in t)

    def _establecer_genero(self, g):
        g = (g or "").lower()
        self.rb_masc.setChecked(g == "masculino")
        self.rb_fem.setChecked(g == "femenino")
        self.rb_otro.setChecked(g == "otro")

    def validar(self, datos):
        if not datos.get("codigo"):
            return False, "El campo 'Código' es obligatorio."
        if not datos.get("nombre"):
            return False, "El campo 'Nombre completo' es obligatorio."
        if datos.get("carrera") == "-- Seleccionar --":
            return False, "Debe seleccionar una carrera."
        if not datos.get("genero"):
            return False, "Debe seleccionar un género."
        correo = datos.get("correo") or ""
        if correo and "@" not in correo:
            return False, "El correo electrónico no es válido."
        return True, ""

    def limpiar_campos(self):
        self.txt_codigo.clear()
        self.txt_nombre.clear()
        self.txt_telefono.clear()
        self.txt_correo.clear()
        self.cmb_carrera.setCurrentIndex(0)
        self.rb_masc.setAutoExclusive(False)
        self.rb_fem.setAutoExclusive(False)
        self.rb_otro.setAutoExclusive(False)
        self.rb_masc.setChecked(False)
        self.rb_fem.setChecked(False)
        self.rb_otro.setChecked(False)
        self.rb_masc.setAutoExclusive(True)
        self.rb_fem.setAutoExclusive(True)
        self.rb_otro.setAutoExclusive(True)
        self.chk_progra.setChecked(False)
        self.chk_redes.setChecked(False)
        self.chk_ia.setChecked(False)
        self.chk_base.setChecked(False)
        self.chk_mark.setChecked(False)
        self.txt_notas.clear()
        self.editando_index = -1
        self.btn_registrar.setEnabled(True)
        self.btn_editar.setEnabled(False)
        self.btn_cancelar_edit.setVisible(False)
        self.tabla.clearSelection()
        self.txt_codigo.setFocus()

    def registrar(self):
        datos = {
            "codigo": self.txt_codigo.text().strip(),
            "nombre": self.txt_nombre.text().strip(),
            "carrera": self.cmb_carrera.currentText(),
            "genero": self._obtener_genero(),
            "telefono": self.txt_telefono.text().strip(),
            "correo": self.txt_correo.text().strip(),
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "intereses": self._obtener_intereses(),
            "notas": self.txt_notas.toPlainText().strip(),
        }
        ok, msg = self.validar(datos)
        if not ok:
            QMessageBox.warning(self, "Validación", msg)
            return
        # evitar duplicado de código
        if any(r["codigo"].lower() == datos["codigo"].lower() for r in self.registros):
            QMessageBox.warning(self, "Validación", "Ya existe un estudiante con ese código.")
            return
        conf = ConfirmacionDialog("¿Confirmas registrar este estudiante?", self)
        if conf.exec() == QDialog.Accepted:
            self.registros.append(datos)
            self.limpiar_campos()
            self._mostrar_tabla()
            QMessageBox.information(self, "Éxito", "Estudiante registrado correctamente.")

    def _mostrar_tabla(self):
        self.tabla.setRowCount(len(self.registros))
        for i, r in enumerate(self.registros):
            self.tabla.setItem(i, 0, QTableWidgetItem(r["codigo"]))
            self.tabla.setItem(i, 1, QTableWidgetItem(r["nombre"]))
            self.tabla.setItem(i, 2, QTableWidgetItem(r["carrera"]))
            self.tabla.setItem(i, 3, QTableWidgetItem(r["genero"]))
            self.tabla.setItem(i, 4, QTableWidgetItem(r["telefono"]))
            self.tabla.setItem(i, 5, QTableWidgetItem(r["correo"]))
            self.tabla.setItem(i, 6, QTableWidgetItem(r["fecha"]))
            self.tabla.setItem(i, 7, QTableWidgetItem(r["intereses"]))
        self.lbl_total.setText(f"Total de registros: {len(self.registros)}")

    def cargar_para_editar(self):
        if not self.registros:
            return
        rows = self.tabla.selectionModel().selectedRows()
        if not rows:
            QMessageBox.information(self, "Editar", "Seleccione una fila para editar.")
            return
        idx = rows[0].row()
        if idx < 0 or idx >= len(self.registros):
            return
        r = self.registros[idx]
        self.editando_index = idx
        self.txt_codigo.setText(r["codigo"])
        self.txt_nombre.setText(r["nombre"])
        self.cmb_carrera.setCurrentText(r["carrera"])
        self._establecer_genero(r["genero"])
        self.txt_telefono.setText(r["telefono"])
        self.txt_correo.setText(r["correo"])
        self._establecer_intereses(r["intereses"])
        self.txt_notas.setPlainText(r.get("notas", ""))
        self.btn_registrar.setEnabled(False)
        self.btn_editar.setEnabled(True)
        self.btn_cancelar_edit.setVisible(True)
        self.txt_codigo.setFocus()

    def guardar_edicion(self):
        if self.editando_index < 0:
            return
        datos = {
            "codigo": self.txt_codigo.text().strip(),
            "nombre": self.txt_nombre.text().strip(),
            "carrera": self.cmb_carrera.currentText(),
            "genero": self._obtener_genero(),
            "telefono": self.txt_telefono.text().strip(),
            "correo": self.txt_correo.text().strip(),
            "fecha": self.registros[self.editando_index].get("fecha", datetime.now().strftime("%d/%m/%Y %H:%M")),
            "intereses": self._obtener_intereses(),
            "notas": self.txt_notas.toPlainText().strip(),
        }
        ok, msg = self.validar(datos)
        if not ok:
            QMessageBox.warning(self, "Validación", msg)
            return
        # duplicado excepto propio
        for i, r in enumerate(self.registros):
            if i != self.editando_index and r["codigo"].lower() == datos["codigo"].lower():
                QMessageBox.warning(self, "Validación", "Ya existe otro estudiante con ese código.")
                return
        conf = ConfirmacionDialog("¿Confirmas guardar los cambios?", self)
        if conf.exec() == QDialog.Accepted:
            self.registros[self.editando_index] = datos
            self.cancelar_edicion()
            self._mostrar_tabla()
            QMessageBox.information(self, "Éxito", "Información editada correctamente.")

    def cancelar_edicion(self):
        self.limpiar_campos()

    def eliminar(self):
        if not self.registros:
            QMessageBox.information(self, "Eliminar", "No hay registros para eliminar.")
            return
        rows = self.tabla.selectionModel().selectedRows()
        if not rows:
            QMessageBox.information(self, "Eliminar", "Seleccione una fila para eliminar.")
            return
        idx = rows[0].row()
        if idx < 0 or idx >= len(self.registros):
            return
        nombre = self.registros[idx]["nombre"]
        conf = ConfirmacionDialog(f"¿Confirmas eliminar al estudiante '{nombre}'?", self)
        if conf.exec() == QDialog.Accepted:
            del self.registros[idx]
            if self.editando_index == idx:
                self.cancelar_edicion()
            elif self.editando_index > idx:
                self.editando_index -= 1
            self._mostrar_tabla()
            QMessageBox.information(self, "Éxito", "Registro eliminado correctamente.")

    def buscar(self):
        texto = self.txt_nombre.text().strip() or self.txt_codigo.text().strip()
        if not texto:
            QMessageBox.information(self, "Buscar", "Ingrese código o nombre a buscar.")
            return
        t = texto.lower()
        resultados = [r for r in self.registros if t in r["codigo"].lower() or t in r["nombre"].lower()]
        if not resultados:
            QMessageBox.information(self, "Buscar", "No se encontraron registros.")
            return
        # mostrar primero resultado en formulario y resaltar en tabla
        r = resultados[0]
        # cargar
        try:
            idx = self.registros.index(r)
        except ValueError:
            idx = -1
        if idx >= 0:
            self.tabla.selectRow(idx)
            self.cargar_para_editar()
        dlg = DetalleEstudianteDialog(r, self)
        dlg.exec()

    def mostrar_informacion(self):
        if not self.registros:
            QMessageBox.information(self, "Información", "No hay registros para mostrar.")
            return
        rows = self.tabla.selectionModel().selectedRows()
        if rows:
            idx = rows[0].row()
            r = self.registros[idx]
            DetalleEstudianteDialog(r, self).exec()
        else:
            QMessageBox.information(self, "Información", "Seleccione un registro para ver su información.")


def main():
    app = QApplication(sys.argv)
    win = SistemaEstudiantes()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# Desarrollado por SARMIENTO

