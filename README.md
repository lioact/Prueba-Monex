# Pruebas Analista de Riesgo de Crédito – 2026

Proyecto de modelado de riesgo crediticio para evaluar incumplimiento a 12 meses en originación y seguimiento de clientes.

## 🚀 Ejecución Rápida

### Prerrequisitos
- Python 3.12
- PDM (Python Dependency Manager)

### Instalación y Ejecución

```bash
# Instalar PDM
pip install pdm

# 1. Instalar dependencias
pdm install

# 2. Ejecutar análisis exploratorio
Ejecutar notebooks individuales
```


## 📝 Respuestas a las Tareas

### 1. Modelo de Incumplimiento a 12 Meses - Originación

**Objetivo:** Calificar prospectos en el momento del otorgamiento.

**Enfoque:**
- Modelo logístico con variables disponibles al momento de originación
- Target: incumplimiento a 90+ días en los próximos 12 meses
- Variables clave: bureau_score, dti, prev_delin_24m, utilization, variables macro

**Resultado:**
- AUC: [X.XX]
- Gini: [X.XX]
- KS: [XX%]

### 2. Modelo de Incumplimiento a 12 Meses - Seguimiento

**Objetivo:** Monitorear riesgo de clientes existentes durante su ciclo de vida.

**Diferencia clave:** Utiliza información actualizada del comportamiento del cliente en el tiempo (panel data), no solo variables de originación.

**Variables adicionales:**
- Comportamiento de pago histórico
- Evolución de utilización
- Cambios en variables macro desde originación

### 3. Análisis Exploratorio

**Principales hallazgos:**

**Universo de clientes:**
- [Insertar insights sobre distribución de edad, ingresos, productos]
- [Patrones de riesgo por segmento]

**Variables macroeconómicas:**
- [Tendencias de desempleo, tasas, inflación]
- [Correlación con incumplimiento]

**Correlaciones con incumplimiento:**
1. **bureau_score**: correlación negativa fuerte (↓ score → ↑ incumplimiento)
2. **prev_delin_24m**: correlación positiva (historial predice futuro)
3. **dti**: correlación positiva (mayor apalancamiento → mayor riesgo)
4. **unemp**: correlación positiva (desempleo → incumplimiento)
5. **utilization**: correlación positiva (alta utilización → estrés financiero)

### 4. Análisis de Cosechas (Vintage Analysis)

**Observaciones:**
- [Patrones de maduración por cosecha]
- [Comparación cosechas recientes vs tempranas]

**Desempeño del modelo:**
- **Cosechas tempranas (20XX-20XX):** [Métricas de desempeño]
- **Cosechas recientes (20XX-20XX):** [Métricas de desempeño]

**Factores explicativos:**
- Cambios en condiciones macroeconómicas
- Evolución en política de originación
- Cambios en composición de productos/canales

### 5. Evaluación de Modelos

#### a-b. Percentiles de PD

| Percentil | PD Promedio | Default Real | Monto Total | Pérdida Esperada |
|-----------|-------------|--------------|-------------|------------------|
| 1-10      | X.X%        | X.X%         | $XXX,XXX    | $X,XXX          |
| 11-20     | X.X%        | X.X%         | $XXX,XXX    | $X,XXX          |
| ...       | ...         | ...          | ...         | ...             |
| 91-100    | XX.X%       | XX.X%        | $XXX,XXX    | $XX,XXX         |

#### c. Top 5 Variables Explicativas

1. **bureau_score** (-): Clientes con score <600 tienen PD 3x mayor
2. **prev_delin_24m** (+): Cada evento de mora aumenta PD en X%
3. **dti** (+): DTI >50% duplica probabilidad de incumplimiento
4. **unemp** (+): Cada punto de desempleo aumenta PD en X%
5. **utilization** (+): Utilización >80% indica estrés financiero

#### d. Casos Individuales

**Cliente A (Bajo Riesgo - PD: 2%)**
- bureau_score: 780
- dti: 25%
- prev_delin_24m: 0
- Ingreso estable, baja utilización

**Cliente B (Alto Riesgo - PD: 35%)**
- bureau_score: 520
- dti: 60%
- prev_delin_24m: 3
- Historial de mora, alto apalancamiento

### 6. Modelo de Originación - Evaluación Práctica

#### a. ¿Usarías este score para originar hoy?

**Respuesta:** [Sí/No/Con reservas]

**Justificación:**
- [Evaluación de estabilidad temporal]
- [Condiciones actuales vs entrenamiento]
- [Cobertura de segmentos]

#### b. ¿Con qué restricciones?

- Revisar manualmente aplicaciones con PD entre X%-Y%
- Límites de monto para clientes de alto riesgo
- Restricciones por producto/canal si muestran deterioro
- [Otras restricciones específicas]

#### c. ¿Qué monitorearías mensualmente?

1. **PSI (Population Stability Index)** de variables predictoras
2. **Tasas de incumplimiento por cosecha**
3. **Distribución de scores en nuevas originaciones**
4. **Variables macroeconómicas** vs supuestos del modelo
5. **Tasas de aprobación y rechazos**
6. **Concentración por producto/región/canal**

#### d. ¿Qué te preocuparía en 6-12 meses?

- **Recesión económica:** aumento generalizado de desempleo
- **Cambio en política monetaria:** tasas de interés al alza
- **Deterioro de cosechas recientes:** señal temprana de problemas
- **Drift del modelo:** variables perdiendo poder predictivo
- **Cambios en mix de productos:** mayor concentración en alto riesgo

### 7. Stress Testing

#### a. Escenarios Macroeconómicos

**Escenario Base:**
- Desempleo: X.X%
- Tasa de interés: X.X%
- Inflación: X.X%

**Escenario Adverso:**
- Desempleo: +X.X pp (↑)
- Tasa de interés: +X.X pp (↑)
- Inflación: +X.X pp (↑)

#### b. Ajuste de PDs

**Metodología:**
- Sensibilidad de coeficientes macro en el modelo
- PD_stress = PD_base × factor_ajuste
- Factor de ajuste basado en elasticidades estimadas

**Resultados:**
- Aumento promedio de PD: +XX%
- Segmentos más afectados: [alto DTI, bajo score, etc.]

#### c. Pérdida Esperada bajo Estrés

| Escenario | Pérdida Esperada | Incremento vs Base |
|-----------|------------------|-------------------|
| Base      | $X,XXX,XXX       | -                 |
| Adverso   | $X,XXX,XXX       | +XX%              |

**Segmentos críticos:**
- [Identificación de portafolios más vulnerables]

#### d. ¿El modelo sigue siendo útil?

**Respuesta:** [Sí/No/Parcialmente]

**Análisis:**
- Capacidad discriminatoria bajo estrés: [Evaluar si AUC se mantiene]
- Calibración: [Verificar si PDs predichas son realistas]
- Limitaciones: [Identificar rangos donde el modelo pierde precisión]
- Recomendaciones: [Recalibración, nuevas variables, etc.]

## 🔍 Notas Metodológicas

- **Definición de incumplimiento:** 90+ días de mora (dpd_bucket = 90+)
- **Ventana de observación:** 12 meses posteriores a originación
- **LLM utilizado:** [Si aplica, documentar prompts y razonamiento]



## 📧 Contacto

[Tu nombre]  
[Tu correo]

---
