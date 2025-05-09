from empleados import agregar_empleado
from calculos import calcular_nomina
from database import empleados

def mostrar_liquidacion(documento):
    if documento not in empleados:
        print("Empleado no encontrado")
        return
    
    nomina = calcular_nomina(documento)
    emp = empleados[documento]
    
    print(f"\n LIQUIDACIÓN DE NÓMINA: {emp['nombre']}")
    print("\n DEVENGADOS:")
    for concepto, valor in nomina['devengados'].items():
        print(f"- {concepto.replace('_', ' ').title()}: ${valor:,.2f}")
    
    print("\n DEDUCCIONES:")
    for concepto, valor in nomina['deducciones'].items():
        if concepto != 'total':
            print(f"- {concepto.title()}: ${valor:,.2f}")
    
    print(f"\n TOTAL A PAGAR: ${nomina['total_pagar']:,.2f}")

def menu_principal():
    while True:
        print("\n=== SISTEMA DE NÓMINA ===")
        print("1. Agregar empleado y Calcular nómina ")
        print("2. Salir")
        
        opcion = input("\nSeleccione opción: ")
        
        if opcion == '1':
            agregar_empleado()
        elif opcion == '2':
            print("👋 Hasta luego!")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu_principal()