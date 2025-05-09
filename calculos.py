from database import empleados
AUXILIO_TRANSPORTE = 200000  # Constante

def calcular_nomina(documento):
    emp = empleados[documento]
    sb = emp['salario_basico']
    dl = emp['dias_laborados']
    hed = emp['horas_extras_diurnas']
    hen = emp['horas_extras_nocturnas']
    
    # Cálculos
    salario_neto = (sb / 30) * dl
    aux_transporte = (AUXILIO_TRANSPORTE / 30) * dl if sb <= 2 * 1300000 else 0
    
    valor_hora_normal = sb / 240
    valor_hed = (valor_hora_normal * 1.25) * hed
    valor_hen = (valor_hora_normal * 1.75) * hen
    
    total_devengado = salario_neto + aux_transporte + valor_hed + valor_hen + emp['comisiones']
    
    deducciones = {
        'salud': salario_neto * 0.04,
        'pension': salario_neto * 0.04,
        'prestamos': emp['prestamos']
    }
    total_deducido = sum(deducciones.values())
    
    return {
        'devengados': {
            'salario_neto': salario_neto,
            'aux_transporte': aux_transporte,
            'horas_extras_diurnas': valor_hed,
            'horas_extras_nocturnas': valor_hen,
            'comisiones': emp['comisiones'],
            'total': total_devengado
        },
        'deducciones': {
            **deducciones,
            'total': total_deducido
        },
        'total_pagar': total_devengado - total_deducido
    }