# app.py (Versión Simplificada SIN DB)

from flask import Flask, render_template, request, redirect, url_for, session, flash
from gestion_financiera import GestorFinancieroSimulado

app = Flask(__name__)
# Necesitas una clave secreta para usar sesiones y flash
app.secret_key = 'clave_secreta_simulada' 

# 1. INSTANCIAR EL GESTOR SIMULADO
gestor_financiero = GestorFinancieroSimulado() 


# =================================================================
#                             RUTAS DE SIMULACIÓN
# =================================================================

# --- SIMULACIÓN DE LOGIN / INDEX ---
@app.route('/')
def index(): 
    # Simulamos que el usuario está logueado para mostrar la interfaz
    session['username'] = 'Edwin'
    session['user_id'] = 1 
    
    resumen = gestor_financiero.obtener_resumen_financiero(session['user_id'])
    
    return render_template('index.html', resumen=resumen)

# --- SIMULACIÓN DE REGISTRO DE INGRESOS ---
@app.route('/ingresos', methods=['GET', 'POST'])
def ingresos():
    if 'username' not in session: return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Simulamos que el registro fue exitoso
        flash("Ingreso registrado correctamente (Simulación).", 'success')
        # Redirigimos para limpiar el formulario, como si la DB se hubiera actualizado
        return redirect(url_for('ingresos')) 

    transacciones = gestor_financiero.obtener_transacciones(session['user_id'], 'ingreso')
    return render_template('ingresos.html', transacciones=transacciones)


# --- SIMULACIÓN DE REGISTRO DE EGRESOS ---
@app.route('/egresos', methods=['GET', 'POST'])
def egresos():
    if 'username' not in session: return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Simulamos que el registro fue exitoso
        flash("Egreso registrado correctamente (Simulación).", 'success')
        return redirect(url_for('egresos'))

    transacciones = gestor_financiero.obtener_transacciones(session['user_id'], 'egreso')
    return render_template('egresos.html', transacciones=transacciones)


# --- ALERTAS DE FORMALIZACIÓN ---
@app.route('/alertas')
def alertas():
    if 'username' not in session: return redirect(url_for('index'))
        
    ingresos_anuales = gestor_financiero.obtener_ingresos_anuales(session['user_id'])
    alertas_list = gestor_financiero.generar_alertas_formalizacion(ingresos_anuales)

    return render_template('alertas.html', 
                           alertas_list=alertas_list, 
                           ingresos_anuales=ingresos_anuales)


# --- RUTAS DE PLANTILLA (Simplemente Renderizan el HTML) ---
@app.route('/reportes')
def reportes():
    if 'username' not in session: return redirect(url_for('index'))
    resumen = gestor_financiero.obtener_resumen_financiero(session['user_id'])
    return render_template('reportes.html', resumen=resumen)

@app.route('/asesoria')
def asesoria():
    if 'username' not in session: return redirect(url_for('index'))
    return render_template('asesoria.html')

@app.route('/contacto')
def contacto():
    if 'username' not in session: return redirect(url_for('index'))
    return render_template('contacto.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index')) # Redirige al index, que simulará un login

if __name__ == '__main__':
    app.run(debug=True)