# app.py (Versión Simplificada con Persistencia en Sesión)

from flask import Flask, render_template, request, redirect, url_for, session, flash
# Importamos la nueva clase de gestión
from gestion_financiera import GestorFinancieroMemoria 

app = Flask(__name__)
# Necesitas una clave secreta para usar sesiones y flash
app.secret_key = 'clave_secreta_simulada_para_vecicuenta' 

# 1. INSTANCIAR EL GESTOR DE MEMORIA
# Ya no necesitamos get_db_connection
gestor_financiero = GestorFinancieroMemoria() 

# --- SIMULACIÓN DE LOGIN / INDEX ---
@app.route('/')
def index(): 
    # Simulamos que el usuario está logueado para mostrar la interfaz
    session['username'] = 'Edwin'
    session['user_id'] = 1 
    
    # El dashboard lee directamente los datos acumulados en la sesión
    resumen = gestor_financiero.obtener_resumen_financiero(session['user_id'])
    
    return render_template('index.html', resumen=resumen)

# --- REGISTRO DE INGRESOS ---
@app.route('/ingresos', methods=['GET', 'POST'])
def ingresos():
    if 'username' not in session: return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            descripcion = request.form['descripcion']
            valor = float(request.form['valor'])
            
            # Registramos el dato en la memoria/sesión
            gestor_financiero.registrar_transaccion(
                user_id=session['user_id'], 
                tipo='ingreso', 
                descripcion=descripcion, 
                valor=valor
            )
            flash("¡Ingreso registrado! El Dashboard se ha actualizado.", 'success')
            return redirect(url_for('ingresos'))
        except ValueError:
            flash("El valor debe ser un número válido.", 'danger')

    transacciones = gestor_financiero.obtener_transacciones(session['user_id'], 'ingreso')
    return render_template('ingresos.html', transacciones=transacciones)


# --- REGISTRO DE EGRESOS ---
@app.route('/egresos', methods=['GET', 'POST'])
def egresos():
    if 'username' not in session: return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            descripcion = request.form['descripcion']
            valor = float(request.form['valor'])
            
            # Registramos el dato en la memoria/sesión
            gestor_financiero.registrar_transaccion(
                user_id=session['user_id'], 
                tipo='egreso', 
                descripcion=descripcion, 
                valor=valor
            )
            flash("¡Egreso registrado! El Dashboard se ha actualizado.", 'success')
            return redirect(url_for('egresos'))
        except ValueError:
            flash("El valor debe ser un número válido.", 'danger')

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


# --- RUTAS DE PLANTILLA (Estáticas) ---
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
    # También borramos la data de simulación para que empiece de nuevo
    if 'transacciones_1' in session: 
        session.pop('transacciones_1')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)