import os
import sqlite3
from datetime import datetime
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget
from plyer import filechooser
import openpyxl

KV = '''
MDBoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        title: "Control de Cartera y Cobros"
        elevation: 4
        right_action_items: [["file-upload", lambda x: app.seleccionar_excel()]]

    MDBottomNavigation:
        selected_color_background: "orange"

        MDBottomNavigationItem:
            name: 'screen_todos'
            text: 'Todos'
            icon: 'account-group'
            on_tab_press: app.cargar_clientes('Todos')

            MDScrollView:
                MDList:
                    id: lista_todos

        MDBottomNavigationItem:
            name: 'screen_atrasados'
            text: 'Atrasados'
            icon: 'alert-circle'
            on_tab_press: app.cargar_clientes('Atrasados')

            MDScrollView:
                MDList:
                    id: lista_atrasados

        MDBottomNavigationItem:
            name: 'screen_pagados'
            text: 'Pagados'
            icon: 'check-circle'
            on_tab_press: app.cargar_clientes('Pagados')

            MDScrollView:
                MDList:
                    id: lista_pagados
'''

class CarteraApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Red"
        # Obtener ruta de almacenamiento segura según el S.O.
        self.db_path = os.path.join(self.user_data_dir, "cartera_movil.db")
        self.init_db()
        return Builder.load_string(KV)

    def on_start(self):
        self.cargar_clientes('Todos')

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cod_promotor INTEGER,
                    prestamo TEXT,
                    nombre TEXT,
                    fec_cuota TEXT,
                    total_cuota REAL,
                    num_cuota INTEGER,
                    estado_cuota TEXT,
                    UNIQUE(prestamo, num_cuota)
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error iniciando DB: {e}")

    def cargar_clientes(self, filtro='Todos'):
        if not hasattr(self, 'root') or not self.root:
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, prestamo, nombre, fec_cuota, total_cuota, num_cuota, estado_cuota FROM clientes")
            rows = cursor.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error al leer DB: {e}")
            rows = []

        if filtro == 'Atrasados':
            container = self.root.ids.lista_atrasados
        elif filtro == 'Pagados':
            container = self.root.ids.lista_pagados
        else:
            container = self.root.ids.lista_todos

        container.clear_widgets()
        hoy = datetime.now().date()

        for row in rows:
            cid, prestamo, nombre, fec_str, total, num_cuota, estado = row
            
            dias_atraso = 0
            es_mora = False

            if fec_str and estado != 'P':
                try:
                    fecha_c = datetime.strptime(fec_str, "%Y-%m-%d").date()
                    if hoy > fecha_c:
                        dias_atraso = (hoy - fecha_c).days
                        es_mora = True
                except ValueError:
                    pass

            if filtro == 'Atrasados' and not es_mora:
                continue
            if filtro == 'Pagados' and estado != 'P':
                continue

            if estado == 'P':
                subtext = f"PAGADO | Cuota #{num_cuota} - Q.{total:,.2f}"
            elif es_mora:
                subtext = f"⚠️ ATRASADO ({dias_atraso} días) | Venció: {fec_str}"
            else:
                subtext = f"PENDIENTE | Vence: {fec_str} - Q.{total:,.2f}"

            item = TwoLineAvatarIconListItem(
                text=f"{nombre} ({prestamo})",
                secondary_text=subtext
            )

            btn_pago = IconRightWidget(
                icon="checkbox-blank-outline" if estado != 'P' else "check-box-outline",
                on_release=lambda x, cliente_id=cid, est=estado: self.toggle_pago(cliente_id, est, filtro)
            )
            item.add_widget(btn_pago)
            container.add_widget(item)

    def toggle_pago(self, cliente_id, estado_actual, filtro_actual):
        nuevo_estado = 'A' if estado_actual == 'P' else 'P'
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE clientes SET estado_cuota = ? WHERE id = ?", (nuevo_estado, cliente_id))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al actualizar estado: {e}")
        self.cargar_clientes(filtro_actual)

    def seleccionar_excel(self):
        try:
            filechooser.open_file(on_selection=self.importar_excel)
        except Exception as e:
            print(f"Error seleccionando archivo: {e}")

    def importar_excel(self, selection):
        if selection:
            path = selection[0]
            try:
                wb = openpyxl.load_workbook(path)
                sheet = wb.active

                conn = self.get_db_connection()
                cursor = conn.cursor()

                headers = [cell.value for cell in sheet[1]]
                
                idx_promotor = headers.index('COD PROMOTOR') if 'COD PROMOTOR' in headers else 1
                idx_prestamo = headers.index('PRESTAMO') if 'PRESTAMO' in headers else 2
                idx_nombre = headers.index('NOMBRE DEL CLIENTE') if 'NOMBRE DEL CLIENTE' in headers else 3
                idx_fec = headers.index('FEC CUOTA') if 'FEC CUOTA' in headers else 4
                idx_total = headers.index('TOTAL CUOTA') if 'TOTAL CUOTA' in headers else 7
                idx_num = headers.index('NUM CUOTA') if 'NUM CUOTA' in headers else 8
                idx_estado = headers.index('ESTADO CUOTA') if 'ESTADO CUOTA' in headers else 12

                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if not row[idx_prestamo]:
                        continue

                    cod_prom = int(row[idx_promotor]) if row[idx_promotor] else 0
                    prestamo = str(row[idx_prestamo])
                    nombre = str(row[idx_nombre])
                    
                    fec_val = row[idx_fec]
                    if isinstance(fec_val, datetime):
                        fec_str = fec_val.strftime('%Y-%m-%d')
                    else:
                        fec_str = str(fec_val)[:10] if fec_val else ''

                    total_cuota = float(row[idx_total]) if row[idx_total] else 0.0
                    num_cuota = int(row[idx_num]) if row[idx_num] else 1
                    estado_excel = str(row[idx_estado]) if row[idx_estado] else 'A'

                    cursor.execute("SELECT estado_cuota FROM clientes WHERE prestamo = ? AND num_cuota = ?", (prestamo, num_cuota))
                    reg = cursor.fetchone()

                    if reg:
                        est_final = reg[0] if reg[0] == 'P' else estado_excel
                        cursor.execute("""
                            UPDATE clientes SET cod_promotor=?, nombre=?, fec_cuota=?, total_cuota=?, estado_cuota=?
                            WHERE prestamo=? AND num_cuota=?
                        """, (cod_prom, nombre, fec_str, total_cuota, est_final, prestamo, num_cuota))
                    else:
                        cursor.execute("""
                            INSERT INTO clientes (cod_promotor, prestamo, nombre, fec_cuota, total_cuota, num_cuota, estado_cuota)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (cod_prom, prestamo, nombre, fec_str, total_cuota, num_cuota, estado_excel))

                conn.commit()
                conn.close()
                self.cargar_clientes('Todos')
            except Exception as e:
                print(f"Error procesando Excel: {e}")

if __name__ == '__main__':
    CarteraApp().run()
