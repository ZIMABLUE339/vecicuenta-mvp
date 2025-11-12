# gestion_financiera.py

# Importamos solo datetime, ya que no usaremos psycopg2 ni la DB
from datetime import datetime

class GestorFinancieroSimulado:
    def __init__(self):
        # Datos estáticos para simular que hay información
        self.transacciones_simuladas = [
            {"id": 1, "tipo": "ingreso", "descripcion": "Venta de la semana", "valor": 550000.00, "fecha": datetime.now()},
            {"id": 2, "tipo": "ingreso", "descripcion": "Abono Cliente Carlos", "valor": 75000.00, "fecha": datetime.now()},
            {"id": 3, "tipo": "egreso", "descripcion": "Compra de mercancía", "valor": 210000.00, "fecha": datetime.now()},
            {"id": 4, "tipo": "egreso", "descripcion": "Pago de luz", "valor": 80000.00, "fecha": datetime.now()},
        ]

    # ===============================================
    # 1. SIMULACIÓN DE REGISTRO
    # ===============================================

    def registrar_transaccion(self, user_id, tipo, descripcion, valor):
        """Simula que la transacción fue exitosa."""
        return True

    def obtener_transacciones(self, user_id, tipo):
        """Devuelve una lista de transacciones simuladas."""
        return [t for t in self.transacciones_simuladas if t['tipo'] == tipo]


    # ===============================================
    # 2. SIMULACIÓN DE CÁLCULO
    # ===============================================

    def obtener_resumen_financiero(self, user_id):
        """Devuelve datos de resumen simulados para el Dashboard."""
        return {
            "ingresos": 625000.00,  # 550000 + 75000
            "egresos": 290000.00,   # 210000 + 80000
            "utilidad": 335000.00   # 625000 - 290000
        }

    # ===============================================
    # 3. SIMULACIÓN DE ALERTAS
    # ===============================================

    def obtener_ingresos_anuales(self, user_id):
        """Simula ingresos anuales cercanos al umbral."""
        return 40000000.00 # Simula 40 millones COP

    def generar_alertas_formalizacion(self, ingresos_anuales_estimados):
        """Genera alertas basadas en el dato simulado."""
        UMBRAL_DIAN = 50000000.0 
        
        alertas = []
        if ingresos_anuales_estimados >= UMBRAL_DIAN * 0.75:
             alertas.append({
                 "tipo": "warning", 
                 "mensaje": f"¡ALERTA! Sus ingresos simulados se acercan al umbral de {UMBRAL_DIAN:,.0f} COP. Es momento de considerar la formalización."
             })
        return alertas