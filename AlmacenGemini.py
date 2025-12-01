from typing import List, Optional, Tuple
from google import genai
from google.genai.errors import APIError
import os
import glob
from google.genai import types

class AlmacenGemini:
    
    def __init__(self, cliente: genai.Client):
        
        self.cliente = cliente
        self.almacen_archivos = None 
        self.archivos_subidos = []
        print("✅ RepositorioAlmacen inicializado, listo para gestionar datos.")

    def crear_almacen_busqueda(self, nombre_almacen: str):
        if self.almacen_archivos:
            print(f"El almacén ya está configurado con ID: {self.almacen_archivos.name}")
            return self.almacen_archivos

        print(f"Creando FileSearchStore: '{nombre_almacen}'...")
        try:
            self.almacen_archivos = self.cliente.file_search_stores.create(
                config={'display_name': nombre_almacen}
            )
            print(f"✅ Almacén creado. ID: {self.almacen_archivos.name}")
            return self.almacen_archivos
        except APIError as e:
            print(f"❌ Error al crear el almacén: {e}")
            return None

    def obtener_rutas_carpeta(self, ruta_carpeta: str, extensiones: List[str] = ['.pdf', '.txt', '.docx']):
        """
        Busca archivos con las extensiones especificadas dentro de una carpeta.
        Devuelve una lista de rutas de archivo.
        """
        if not os.path.isdir(ruta_carpeta):
            print(f"❌ Error: La ruta '{ruta_carpeta}' no es una carpeta válida.")
            return []

        rutas_archivos = []
        
        for ext in extensiones:
            patron_busqueda = os.path.join(ruta_carpeta, f'*{ext}')
            rutas_archivos.extend(glob.glob(patron_busqueda))
            
        return rutas_archivos

    def subir_carpeta(self, ruta_carpeta = "./Documentos"):
        """
        Centraliza la lógica para subir todos los archivos soportados de una carpeta.
        """
        print(f"\n--- Procesando carpeta: {ruta_carpeta} ---")
        
        
        lista_rutas = self.obtener_rutas_carpeta(ruta_carpeta)
        
        if not lista_rutas:
            print("⚠️ No se encontraron archivos soportados en la carpeta.")
            return []
        
        print(f"✅ Encontrados {len(lista_rutas)} archivos para indexar.")
        
        
        return self.subir_e_indexar_archivos(rutas_archivos=lista_rutas)

    def subir_e_indexar_archivos(self, rutas_archivos: list[str]):
        """
        Sube e indexa una lista de archivos al FileSearchStore existente.
        """
        if not self.almacen_archivos:
            print("❌ Error: No hay FileSearchStore configurado.")
            return []

        archivos_indexados = []
        nombre_almacen = self.almacen_archivos.name
        
        
        for ruta_archivo in rutas_archivos:
            
            if not os.path.exists(ruta_archivo):
                print(f"❌ Error: Archivo no encontrado en la ruta: {ruta_archivo}. Saltando...")
                continue 
                
            nombre_archivo = os.path.basename(ruta_archivo)
            print(f"Cargando archivo '{nombre_archivo}'...")

            try:
                uploaded_file = self.cliente.file_search_stores.upload_to_file_search_store(
                    file_search_store_name=nombre_almacen,
                    file=ruta_archivo,
                    config={'display_name': nombre_archivo}
                )

                self.archivos_subidos.append(uploaded_file.name)
                archivos_indexados.append(uploaded_file)
                print(f"✅ Archivo indexado correctamente. ID: {uploaded_file.name}")

            except APIError as e:
                print(f"❌ Error al subir e indexar {nombre_archivo}: {e}")        
        return archivos_indexados

    def eliminar_almacen_busqueda(self):
        if not self.almacen_archivos:
            print("No hay almacén configurado para eliminar.")
            return

        nombre_almacen = self.almacen_archivos.name

        try:
            print(f"Borrando almacén: {nombre_almacen} con force=True...")
            self.cliente.file_search_stores.delete(
                name=nombre_almacen,
                config={'force': True}
            )
            self.almacen_archivos = None
            self.archivos_subidos = []
            print(f"✅ Almacén '{nombre_almacen}' eliminado correctamente.")
        except APIError as e:
            print(f"❌ Error al eliminar el almacén: {e}")

    def iniciar_rag(self, nombre_almacen:"almacenGemini", ruta_carpeta: str = "./Documentos"):
    
        print("\n=== 🚀 INICIANDO PREPARACIÓN RAG ===")
        
        # 1. Crear el FileSearchStore
        almacen = self.crear_almacen_busqueda(nombre_almacen=nombre_almacen)
        
        if not almacen:
            print("🛑 Fallo en la preparación: No se pudo crear el almacén.")
            return False
            
        # 2. Subir e indexar la carpeta
        archivos_indexados = self.subir_carpeta(ruta_carpeta=ruta_carpeta)
        
        if archivos_indexados:
            print(f"=== ✅ RAG LISTO: {len(archivos_indexados)} archivos indexados. ===\n")
            return True
        else:
            print("=== ⚠️ RAG INACTIVO: No se subieron archivos al almacén. ===\n")
            return False
        
    def obtener_almacen_activo_id(self) -> Optional[str]:
        """
        Devuelve el ID canónico del FileSearchStore activo.
        """
        if self.almacen_archivos:
            # Devuelve el ID canónico (ej: filesearchstores/gfs-123xyz)
            return self.almacen_archivos.name 
        return None