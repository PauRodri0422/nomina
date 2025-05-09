from calculos import calcular_nomina  # Importamos la función de cálculo
from database import empleados

def mostrar_liquidacion(empleado, documento):
    nomina = calcular_nomina(documento)
    print("\n" + "="*50)
    print(f"FACTURA DE NÓMINA - {empleado['nombre'].upper()}")
    print("="*50)
    print("\nDATOS BÁSICOS:")
    print(f"Documento: {documento}")
    print(f"Días laborados: {empleado['dias_laborados']}")
    print(f"Salario básico: ${empleado['salario_basico']:,.2f}")
    print("\nDEVENGADOS:")
    for concepto, valor in nomina['devengados'].items():
        if concepto != 'total':
            print(f"- {concepto.replace('_', ' ').title():<25} ${valor:,.2f}")
    print("\nDEDUCCIONES:")
    for concepto, valor in nomina['deducciones'].items():
        if concepto != 'total':
            print(f"- {concepto.title():<25} ${valor:,.2f}")
    print("\n" + "-"*50)
    print(f"TOTAL DEVENGADO: {'':<10} ${nomina['devengados']['total']:,.2f}")
    print(f"TOTAL DEDUCIDO: {'':<11} ${nomina['deducciones']['total']:,.2f}")
    print(f"NETO A PAGAR: {'':<14} ${nomina['total_pagar']:,.2f}")
    print("="*50 + "\n")

def agregar_empleado():
    documento = input("Documento: ")
    nombre = input("Nombre completo: ")
    salario_basico = float(input("Salario básico: "))
    dias_laborados = int(input("Días laborados: "))
    horas_extras_diurnas = int(input("Horas extras diurnas: "))
    horas_extras_nocturnas = int(input("Horas extras nocturnas: "))
    comisiones = float(input("Comisiones: "))
    prestamos = float(input("Préstamos: "))
    empleados[documento] = {
        'nombre': nombre,
        'salario_basico': salario_basico,
        'dias_laborados': dias_laborados,
        'horas_extras_diurnas': horas_extras_diurnas,
        'horas_extras_nocturnas': horas_extras_nocturnas,
        'comisiones': comisiones,
        'prestamos': prestamos
    }
    print(f"\nEmpleado {nombre} registrado exitosamente!")
    mostrar_liquidacion(empleados[documento], documento)
