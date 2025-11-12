# gestion_financiera.py

from datetime import datetime
from flask import session # Importamos session para guardar datos en memoria de Flask

class GestorFinancieroMemoria:
    """Gestiona transacciones usando la sesión de Flask (simulación de DB)."""

    def __init__(self):
        # El constructor se mantiene simple, la data estará en session.
        pass

    def _get_user_transactions(self, user_id):
        """Obtiene las transacciones de la sesión del usuario. Inicializa si no existen."""
        key = f'transacciones_{user_id}'
        if key not in session:
            # Inicializamos con data de ejemplo para mostrar en el dashboard
            session[key] = [
                {"id": 1, "tipo": "ingreso", "descripcion": "Venta de muestra (Semana 1)", "valor": 750000.00, "fecha": datetime.now()},
                {"id": 2, "tipo": "egreso", "descripcion": "Compra inicial de insumos", "valor": 300000.00, "fecha": datetime.now()},
            ]
        return session[key]

    def _save_transactions(self, user_id, transactions):
        """Guarda la lista de transacciones actualizada en la sesión."""
        session[f'transacciones_{user_id}'] = transactions

    # ===============================================
    # 1. REGISTRO DE TRANSACCIONES (Ahora Funcional)
    # ===============================================

    def registrar_transaccion(self, user_id, tipo, descripcion, valor):
        """Guarda un nuevo ingreso o egreso en la lista de la sesión."""
        transactions = self._get_user_transactions(user_id)
        
        # Generamos un ID simple y agregamos la nueva transacción
        new_id = len(transactions) + 1
        transactions.append({
            "id": new_id, 
            "tipo": tipo, 
            "descripcion": descripcion, 
            "valor": float(valor), 
            "fecha": datetime.now()
        })
        
        self._save_transactions(user_id, transactions)
        return True

    def obtener_transacciones(self, user_id, tipo):
        """Obtiene la lista de transacciones (Ingresos o Egresos) de la sesión."""
        all_transactions = self._get_user_transactions(user_id)
        # Filtramos y ordenamos por fecha (más reciente primero)
        filtered = [t for t in all_transactions if t['tipo'] == tipo]
        filtered.sort(key=lambda x: x['fecha'], reverse=True)
        return filtered

    # ===============================================
    # 2. CÁLCULO DE RESUMENES (Ahora Dinámico)
    # ===============================================

    def obtener_resumen_financiero(self, user_id):
        """Calcula el total de ingresos, egresos y utilidad neta de la sesión."""
        transactions = self._get_user_transactions(user_id)
        
        ingresos = sum(t['valor'] for t in transactions if t['tipo'] == 'ingreso')
        egresos = sum(t['valor'] for t in transactions if t['tipo'] == 'egreso')
        utilidad = ingresos - egresos

        return {
            "ingresos": ingresos,
            "egresos": egresos,
            "utilidad": utilidad
        }

    # ===============================================
    # 3. LÓGICA DE ALERTAS (Ahora Dinámica con Simulación de Acumulación)
    # ===============================================

    def obtener_ingresos_anuales(self, user_id):
        """Calcula la suma total de ingresos de la sesión (simulando ingresos anuales)."""
        transactions = self._get_user_transactions(user_id)
        ingresos_anuales = sum(t['valor'] for t in transactions if t['tipo'] == 'ingreso')
        
        # Para que el valor de simulación sea creíble para el umbral de 50M, escalamos el total actual
        # Si el usuario ha registrado 750k, lo escalamos a 30M para que las alertas sean útiles.
        if ingresos_anuales > 1000:
             return ingresos_anuales * 40 
        
        return ingresos_anuales

    def generar_alertas_formalizacion(self, ingresos_anuales_estimados):
        """Genera alertas y consejos según los ingresos simulados."""
        UMBRAL_DIAN = 50000000.0 
        alertas = []

        if ingresos_anuales_estimados >= UMBRAL_DIAN:
            alertas.append({"tipo": "danger", "mensaje": f"¡ACCIÓN! Ha superado el umbral de {UMBRAL_DIAN:,.0f} COP en ingresos. Es el momento CLAVE para formalizar."})
        elif ingresos_anuales_estimados >= UMBRAL_DIAN * 0.5:
             alertas.append({"tipo": "warning", "mensaje": f"¡ALERTA! Sus ingresos simulados se acercan al umbral. Le recomendamos contactar a nuestro Asesor Contable Aliado."})
        else:
             alertas.append({"tipo": "info", "mensaje": "Sus registros están en orden. Siga así para acumular más datos y obtener proyecciones más precisas."})
            
        return alertas