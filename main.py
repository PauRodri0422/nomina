import sys
import os
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.core.management import execute_from_command_line

# In-memory database (replace with a real database for production)
empleados_db = {}

# --- Logic from original files integrated here ---

# From empleados.py
def agregar_empleado(documento, nombre, salario_basico, dias_laborados, horas_extras_diurnas, horas_extras_nocturnas, bonificaciones, comisiones, prestamos):
    empleados_db[documento] = {
        'nombre': nombre,
        'salario_basico': salario_basico,
        'dias_laborados': dias_laborados,
        'horas_extras_diurnas': horas_extras_diurnas,
        'horas_extras_nocturnas': horas_extras_nocturnas,
        'bonificaciones': bonificaciones,
        'comisiones': comisiones,
        'prestamos': prestamos
    }

# From calculos.py
def calcular_nomina(documento):
    if documento not in empleados_db:
        return None

    emp = empleados_db[documento]

    salario_diario = emp['salario_basico'] / 30
    salario_devengado = salario_diario * emp['dias_laborados']

    valor_hora = emp['salario_basico'] / 240
    extras_diurnas = emp['horas_extras_diurnas'] * valor_hora * 1.25
    extras_nocturnas = emp['horas_extras_nocturnas'] * valor_hora * 1.75

    total_devengado = salario_devengado + extras_diurnas + extras_nocturnas + emp['bonificaciones'] + emp['comisiones']

    salud = total_devengado * 0.04
    pension = total_devengado * 0.04
    deducciones_totales = salud + pension + emp['prestamos']

    total_pagar = total_devengado - deducciones_totales

    return {
        'devengados': {
            'salario_devengado': salario_devengado,
            'extras_diurnas': extras_diurnas,
            'extras_nocturnas': extras_nocturnas,
            'bonificaciones': emp['bonificaciones'],
            'comisiones': emp['comisiones'],
            'total': total_devengado
        },
        'deducciones': {
            'salud': salud,
            'pension': pension,
            'prestamos': emp['prestamos'],
            'total': deducciones_totales
        },
        'total_pagar': total_pagar
    }

# --- Django Setup ---
settings.configure(
    DEBUG=True,
    SECRET_KEY='dummy-key',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
)

# --- Django Views ---
def index_view(request):
    html = """
    <html>
    <head>
        <title>Sistema de Nómina</title>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            h1, h2 { color: #333; }
            a { margin-right: 15px; text-decoration: none; color: #007bff; }
            a:hover { text-decoration: underline; }
            .container { margin-top: 20px; border: 1px solid #ccc; padding: 15px; }
            .form-group { margin-bottom: 10px; }
            label { display: inline-block; width: 120px; }
            input[type="text"], input[type="number"] { width: 200px; padding: 5px; }
            button { padding: 8px 15px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
            pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>Sistema de Nómina</h1>
        <div>
            <a href="/">Inicio</a>
            <a href="/view/">Ver Empleados</a>
            <a href="/add/">Agregar Empleado</a>
            <a href="/modify/">Modificar Empleado</a>
            <a href="/payroll/">Generate Payroll</a>
        </div>
        <div class="container">
    """
    # Display a welcome or introductory message on the home page
    html += "<h2>Welcome to the Payroll System!</h2>"
    html += "<p>Use the links above to navigate through the system.</p>"
    # Translated welcome message
    html = html.replace("<h2>Welcome to the Payroll System!</h2>", "<h2>¡Bienvenido al Sistema de Nómina!</h2>")
    html = html.replace("<p>Use the links above to navigate through the system.</p>", "<p>Utilice los enlaces de arriba para navegar por el sistema.</p>")

    html += """
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def view_employees_view(request):
    html = """
    <html>
<head>
        <title>Ver Empleados</title>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            h1, h2 { color: #333; }
            a { margin-right: 15px; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .container { margin-top: 20px; border: 1px solid #ccc; padding: 15px; }
            pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>Ver Empleados</h1>
        <div>
            <a href="/">Inicio</a>
            <a href="/view/">Ver Empleados</a>
            <a href="/add/">Agregar Empleado</a>
            <a href="/modify/">Modificar Empleado</a>
            <a href="/payroll/">Generate Payroll</a>
        </div>
        <div class="container">
            <h2>Datos de Empleados</h2>
            <pre>"""
    if not empleados_db:
        html += "No hay empleados agregados aún."
    else:
        for doc, emp in empleados_db.items():
            html += f"Document: {doc}\n"
            for key, value in emp.items():
                html += f"  {key.replace('_', ' ').title()}: {value}\n"
            html += "-" * 20 + "\n"

    html += """</pre>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def add_employee_view(request):
    if request.method == 'POST':
        try:
            documento = request.POST.get('documento')
            nombre = request.POST.get('nombre')
            salario_basico = float(request.POST.get('salario_basico'))
            dias_laborados = int(request.POST.get('dias_laborados'))
            horas_extras_diurnas = int(request.POST.get('horas_extras_diurnas', 0))
            horas_extras_nocturnas = int(request.POST.get('horas_extras_nocturnas', 0))
            bonificaciones = float(request.POST.get('bonificaciones', 0))
            comisiones = float(request.POST.get('comisiones', 0))
            prestamos = float(request.POST.get('prestamos', 0))

            agregar_empleado(documento, nombre, salario_basico, dias_laborados, horas_extras_diurnas, horas_extras_nocturnas, bonificaciones, comisiones, prestamos)
            message = "Employee added successfully!"
        except Exception as e:
            message = f"Error adding employee: {e}"
    else:
        # For GET requests, no message is needed initially
        message = "" 

    html = f"""
    <html>
    <head>
        <title>Agregar Empleado</title>
        <style>
            body {{ font-family: sans-serif; margin: 20px; }}
            h1, h2 {{ color: #333; }}
            a {{ margin-right: 15px; text-decoration: none; color: #007bff; }}
            a:hover {{ text-decoration: underline; }}
            .container {{ margin-top: 20px; border: 1px solid #ccc; padding: 15px; }}
            .form-group {{ margin-bottom: 10px; }}
            label {{ display: inline-block; width: 150px; }}
            input[type="text"], input[type="number"] {{ width: 200px; padding: 5px; }}
            button {{ padding: 8px 15px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }}
            button:hover {{ background-color: #45a049; }}
            .message {{ color: green; margin-top: 10px; }}
            .error {{ color: red; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <h1>Agregar Empleado</h1>
        <div>
            <a href="/">Inicio</a>
            <a href="/view/">Ver Empleados</a>
            <a href="/add/">Agregar Empleado</a>
            <a href="/modify/">Modificar Empleado</a>
            <a href="/payroll/">Generate Payroll</a>
        </div>
        <div class="container">
            <h2>Agregar Nuevo Empleado</h2>
            {f'<p class="message">{message}</p>' if 'success' in message else f'<p class="error">{message}</p>' if message else ''}
            <form method="post">
                <div class="form-group">
                    <label for="documento">Documento:</label>
                    <input type="text" id="documento" name="documento" required>
                </div>
                <div class="form-group">
                    <label for="nombre">Nombre:</label>
                    <input type="text" id="nombre" name="nombre" required>
                </div>
                <div class="form-group">
                    <label for="salario_basico">Salario Básico:</label>
                    <input type="number" id="salario_basico" name="salario_basico" step="0.01" required>
                </div>
                <div class="form-group">
                    <label for="dias_laborados">Días Laborados:</label>
                    <input type="number" id="dias_laborados" name="dias_laborados" required>
                </div>
                <div class="form-group">
                    <label for="horas_extras_diurnas">Horas Extras Diurnas:</label>
                    <input type="number" id="horas_extras_diurnas" name="horas_extras_diurnas" value="0">
                </div>
                <div class="form-group">
                    <label for="horas_extras_nocturnas">Horas Extras Nocturnas:</label>
                    <input type="number" id="horas_extras_nocturnas" name="horas_extras_nocturnas" value="0">
                </div>
                <div class="form-group">
                    <label for="bonificaciones">Bonificaciones:</label>
                    <input type="number" id="bonificaciones" name="bonificaciones" step="0.01" value="0">
                </div>
                <div class="form-group">
                    <label for="comisiones">Comisiones:</label>
                    <input type="number" id="comisiones" name="comisiones" step="0.01" value="0">
                </div>
                <div class="form-group">
                    <label for="prestamos">Préstamos:</label>
                    <input type="number" id="prestamos" name="prestamos" step="0.01" value="0">
                </div>
                <button type="submit">Agregar Empleado</button>
            </form>
        </div>
    </body>
    </html>
    """
    # Ensure an HttpResponse is returned for all cases

    return HttpResponse(html)

def modify_employee_view(request):
    # This view would need a way to select an employee to modify
    # and then display a form pre-filled with their data.
    # For simplicity, this is a placeholder.
    html = """
    <html>
    <head>
        <title>Modificar Empleado</title>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            h1, h2 { color: #333; }
            a { margin-right: 15px; text-decoration: none; color: #007bff; }
            a:hover { text-decoration: underline; }
            .container { margin-top: 20px; border: 1px solid #ccc; padding: 15px; }
        </style>
    </head>
    <body>
        <h1>Modify Employee</h1>
        <div>
            <a href="/">Inicio</a>
            <a href="/view/">Ver Empleados</a>
            <a href="/add/">Agregar Empleado</a>
            <a href="/modify/">Modificar Empleado</a>
            <a href="/payroll/">Generate Payroll</a>
        </div>
        <div class="container">
            <h2>Modify Employee Data</h2>
            <p>This section is under construction. You would select an employee to modify here.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def generate_payroll_view(request):
    html = """
    <html>
<head>
        <title>Generar Nómina</title>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            h1, h2 { color: #333; }
            a { margin-right: 15px; text-decoration: none; color: #007bff; }
            a:hover { text-decoration: underline; }
            .container { margin-top: 20px; border: 1px solid #ccc; padding: 15px; }
            select, button { padding: 8px; margin-right: 10px; }
            button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
            pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>Generar Nómina</h1>
        <div>
            <a href="/">Inicio</a>
            <a href="/view/">Ver Empleados</a>
            <a href="/add/">Agregar Empleado</a>
            <a href="/modify/">Modificar Empleado</a>
            <a href="/payroll/">Generar Nómina</a>
        </div>
        <div class="container">
            <h2>Select Employee to Generate Payroll</h2>
            <form method="post">
                <select name="documento" required>
                    <option value="">-- Select Employee --</option>
                    """
    for doc, emp in empleados_db.items():
        html += f'<option value="{doc}">{emp["nombre"]} ({doc})</option>'

    html += """
                </select>
                <button type="submit">Generate Payroll</button>
            </form>
            <div id="payroll-result">"""

    if request.method == 'POST':
        documento = request.POST.get('documento')
        if documento and documento in empleados_db:
            nomina = calcular_nomina(documento)
            if nomina:
                html += "<h3>Payroll Details:</h3>"
                html += f"<p><strong>Empleado:</strong> {empleados_db[documento]['nombre']} ({documento})</p>"
                html += "<pre>"
                html += "DEVENGADOS:\n"
                for concepto, valor in nomina['devengados'].items():
                    html += f"- {concepto.replace('_', ' ').title().replace('salario Devengado', 'Salario Devengado').replace('extras Diurnas', 'Extras Diurnas').replace('extras Nocturnas', 'Extras Nocturnas')}: ${valor:,.2f}\n"

                html += "\nDEDUCCIONES:\n"
                for concepto, valor in nomina['deducciones'].items():
                     if concepto != 'total':
                         html += f"- {concepto.title()}: ${valor:,.2f}\n"

                html += f"\nTOTAL A PAGAR: ${nomina['total_pagar']:,.2f}"
                html += "</pre>"
            else:
                html += f"<p>Could not calculate payroll for employee {documento}.</p>"
        elif documento:
             html += f"<p>Employee with document {documento} not found.</p>"

    html += """
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

# --- URL Configuration ---
urlpatterns = [
    path('', index_view),
    path('view/', view_employees_view),
    path('add/', add_employee_view),
    path('modify/', modify_employee_view),
    path('payroll/', generate_payroll_view),
]

# --- Run Django Development Server ---
if __name__ == "__main__":
    # This part is typically handled by Django's manage.py
    # We are simulating it here for the single-file setup.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)
    execute_from_command_line(sys.argv)