# Pruebas Analista de Riesgo de Crédito – 2026

Proyecto de modelado de riesgo crediticio para evaluar incumplimiento a 12 meses en originación y seguimiento de clientes.

## Ejecución Rápida

### Prerrequisitos
- Python 3.12
- PDM (Python Dependency Manager)

### Instalación y Ejecución

```bash
# 1. Instalar gestor de dependencias
pip install pdm
# 2. Instalar dependencias
pdm install

# 3. Ejecutar notebooks individualmente


```


## Respuestas a las Tareas

### 1. Modelo de Incumplimiento a 12 Meses - Originación

**Objetivo:** Calificar prospectos en el momento del otorgamiento.

**Enfoque:**
- Modelo de Regresión Logística Balanceada con 7 variables clave
- Target: incumplimiento a 90+ días en los próximos 12 meses
- Seleccionado por estabilidad y facilidad de explicación en procesos de originación

**Métricas de desempeño:**
- AUC: 0.6361
- Gini: 0.2721
- KS: 0.2101
- Umbral de decisión: 0.64 para clasificación y aprobación

### 2. Modelo de Incumplimiento a 12 Meses - Seguimiento

**Objetivo:** Monitorear riesgo de clientes existentes durante su ciclo de vida.

**Diferencia clave:** Utiliza información actualizada del comportamiento del cliente en el tiempo (panel data), no solo variables de originación.

**Modelos Evaluados:**

1. Regresión Logística (Logit): AUC 0.635, Gini 0.270 - Modelo base
2. Logit Balanced (SELECCIONADO): AUC 0.636, Gini 0.272, KS 0.210
   - Ofrece la mayor estabilidad para el seguimiento de la Probabilidad de Default continua
3. Random Forest: AUC 0.618 - Desempeño ligeramente inferior en ordenamiento
4. XGBoost: AUC 0.588 - Menor capacidad predictiva que modelos lineales en este dataset

**Modelo Seleccionado:** Logit Balanced por su equilibrio entre desempeño y estabilidad para gestión integral del riesgo.

### 3. Análisis Exploratorio

**Principales hallazgos:**

**Universo de clientes y tendencia:**
- Incremento progresivo de morosidad: De 4.1% en 2022 a 7.2% en 2024
- La PD promedio aumenta en línea con el deterioro observado
- Deterioro coincide con cambios en el entorno macroeconómico

**Variables macroeconómicas:**
- Inflación y tasa de interés (rate) muestran correlación positiva con incumplimiento
- Periodos recientes con mayores tasas presentan mayor riesgo
- El entorno macro explica parte del deterioro en cosechas recientes

**Correlaciones con incumplimiento (Top 3):**
1. bureau_score: Correlación negativa fuerte - A menor score, mayor riesgo de incumplimiento
2. rate (Tasa de interés): Correlación positiva - Mayores tasas aumentan probabilidad de impago
3. prev_delin_24m: Correlación positiva - Antecedentes de morosidad predicen comportamiento futuro

### 4. Análisis de Cosechas (Vintage Analysis)

**Observaciones:**
- Deterioro progresivo en la calidad de la cartera
- Las cosechas más recientes muestran mayor tasa de incumplimiento

**Comparación de cosechas:**

| Cosecha   | Default Real | PD Promedio | Característica |
|-----------|--------------|-------------|----------------|
| 2022-01   | 4.13%        | 0.44        | Temprana       |
| 2023-01   | 6.02%        | ~0.50       | Temprana       |
| 2024-01   | 7.28%        | 0.57        | Reciente       |

**Desempeño del modelo:**
El modelo captura adecuadamente la tendencia de deterioro. La PD promedio se incrementa de 0.44 a 0.57 conforme el entorno se vuelve más riesgoso. El modelo es consistente en diferentes cosechas.

**Factores explicativos de las diferencias:**
- Incremento en inflación durante periodos recientes
- Aumento en tasas de interés impacta capacidad de pago
- Deterioro del entorno macroeconómico en cosechas 2023-2024
- El modelo refleja correctamente estos cambios en sus predicciones

### 5. Evaluación de Modelos

#### a-b. Percentiles de PD (Deciles)

La base fue dividida en deciles (0 al 9) para análisis de riesgo:

| Decil | PD Promedio | Default Real | Monto Total | Pérdida Esperada |
|-------|-------------|--------------|-------------|------------------|
| 0 (Bajo Riesgo)  | 28.39% | 2.55%  | $118.8M | $33.7M  |
| 1                | ~35%   | ~4%    | -       | -       |
| 2                | ~40%   | ~5%    | -       | -       |
| ...              | ...    | ...    | ...     | ...     |
| 8                | ~65%   | ~10%   | -       | -       |
| 9 (Alto Riesgo)  | 71.31% | 11.88% | $125.7M | $89.6M  |

Observaciones: Clara separación entre deciles de riesgo. El decil más alto tiene una PD 2.5 veces mayor que el más bajo. La pérdida esperada se concentra en deciles superiores.

#### c. Top 5 Variables Explicativas

Variables ordenadas por coeficiente del modelo:

1. **rate (Tasa de interés)** (0.166): Mayores tasas incrementan significativamente el riesgo
2. **prev_delin_24m** (0.126): Historial de morosidad es predictor fuerte
3. **debt_income (DTI)** (0.121): Alto apalancamiento aumenta probabilidad de incumplimiento
4. **utilization** (0.114): Alta utilización de líneas indica estrés financiero
5. **inflación** (0.060): Presión inflacionaria afecta capacidad de pago

Todas las variables tienen relación positiva con la probabilidad de incumplimiento. Bureau score, aunque no se muestra en la tabla de coeficientes, tiene relación inversa (a menor score, mayor riesgo).

#### d. Casos Individuales Comparados

**Cliente A (Bajo Riesgo - Decil 0)**
- bureau_score: 850
- debt_income: Baja (~20-30%)
- prev_delin_24m: 0
- utilization: Baja
- PD estimada: ~28%
- Perfil: Score excelente, sin historial de mora, bajo apalancamiento

**Cliente B (Alto Riesgo - Decil 9)**
- bureau_score: 512-560
- debt_income: Alta (>50%)
- prev_delin_24m: 2-3 eventos
- utilization: Alta (>70%)
- PD estimada: ~71%
- Perfil: Score deficiente, historial de impago, alto uso de crédito

El cliente B presenta mayor riesgo debido a un score de crédito 40% menor, antecedentes de morosidad, mayor apalancamiento y utilización casi completa de su capacidad crediticia.

### 6. Modelo de Originación - Evaluación Práctica

#### a. ¿Usarías este score para originar hoy?

**Respuesta:** Sí, con reservas

**Justificación:**
- Como **herramienta de segmentación y apoyo a la decisión**
- **NO como único criterio** de originación
- El modelo captura adecuadamente tendencias de riesgo
- Métricas (AUC 0.636, Gini 0.27) son razonables pero moderadas
- Requiere complementarse con otras políticas de crédito

#### b. ¿Con qué restricciones?

1. **Punto de corte conservador:** Usar umbral de 0.64 establecido
2. **Revisiones manuales:** Para perfiles limítrofes (PD entre 50-65%)
3. **Límites de exposición:** Por cliente según políticas adicionales de crédito
4. **Montos ajustados:** Reducir montos en deciles de alto riesgo (8-9)
5. **Segmentación adicional:** Considerar producto, canal y región
6. **No automatizar 100%:** Mantener supervisión humana en casos borderline

#### c. ¿Qué monitorearías mensualmente?

1. **Inflación:** Variable macro con impacto significativo (coef. 0.060)
2. **Tasa de interés (rate):** Mayor driver del modelo (coef. 0.166)
3. **Bureau score de aprobados:** Estabilidad de la distribución
4. **PSI (Population Stability Index):** De las 7 variables del modelo
5. **Tasas de incumplimiento por cosecha:** Detección temprana de deterioro
6. **Distribución de scores:** En nuevas originaciones vs entrenamiento
7. **Tasas de aprobación y rechazo:** Por producto/canal/región
8. **Performance de deciles:** Validar que el ordenamiento se mantiene

#### d. ¿Qué te preocuparía en 6-12 meses?

1. **Impacto rezagado de tasas altas:** Efecto acumulativo en capacidad de pago
2. **Crecimiento de pérdida esperada:** En cohortes más nuevas (2023-2024)
3. **Deterioro continuo:** Si la tendencia de 4.1%→7.2% continúa
4. **Cambio en entorno macro:** Nueva alza en inflación o tasas
5. **Drift del modelo:** Pérdida de poder predictivo por cambios estructurales
6. **Concentración de riesgo:** En productos/regiones más vulnerables
7. **Calibración del modelo:** Si PDs predichas divergen de defaults observados

### 7. Stress Testing

#### a. Escenarios Macroeconómicos

**Escenario Base:**
- Condiciones macroeconómicas actuales del portafolio
- PD promedio según modelo sin ajustes

**Escenario Adverso:**
- **Incremento del 25% en la PD** (simulando deterioro macroeconómico severo)
- Representa impacto de:
  - Aumento significativo en desempleo
  - Alzas en tasas de interés
  - Aceleración de inflación

#### b. Ajuste de PDs bajo Escenarios

**Metodología:**
```
PD_adverso = PD_base × 1.25
PD_final = min(PD_adverso, 1.0)  # Topado en 100%
```

**Justificación:**
- Factor de 1.25 basado en elasticidades observadas de variables macro
- Refleja sensibilidad del modelo a rate e inflación
- Límite superior de 100% para mantener coherencia probabilística

#### c. Pérdida Esperada bajo Estrés

| Escenario | Pérdida Esperada Total | Incremento vs Base |
|-----------|------------------------|-------------------|
| Base      | $625.8 millones        | -                 |
| Adverso   | $782.0 millones        | +$156.2M (+24.96%) |

**Impacto por Decil:**
- El incremento es **consistente (~25%) en todos los deciles**
- Deciles altos (8-9) absorben mayor pérdida absoluta
- Pérdida esperada en decil 9 pasa de ~$89.6M a ~$112M

**Segmentos más afectados:**
- Clientes con DTI alto y bajo bureau_score
- Productos con mayor sensibilidad a tasas (CC, PL)
- Cohortes recientes ya bajo presión

#### d. ¿El modelo sigue siendo útil?

**Respuesta:** Sí, el modelo mantiene su utilidad bajo estrés

**Análisis de robustez:**

**Capacidad discriminatoria:** 
- El impacto es proporcional en todos los deciles (~25%)
- El ordenamiento de riesgo se mantiene intacto
- Decil 9 sigue siendo 2.5x más riesgoso que decil 0

**Estabilidad estructural:**
- Los coeficientes del modelo siguen siendo relevantes
- Variables macro capturan adecuadamente el estrés
- No hay colapso de la capacidad predictiva

**Limitaciones identificadas:**

1. **Calibración:** Las PDs absolutas pueden requerir ajuste
2. **Linealidad:** Asume impacto proporcional (puede no ser cierto en crisis extrema)
3. **Variables no observadas:** Shocks sistémicos no capturados
4. **Techo de PD:** Algunos segmentos ya cerca de 100%

**Recomendaciones:**
- Útil para ordenamiento y priorización de riesgo
- Mantener para seguimiento relativo entre segmentos
- Recalibrar PDs absolutas si el estrés persiste más de 6 meses
- Complementar con análisis cualitativo en escenarios extremos
- Monitorear nuevas variables (empleo, movilidad) en crisis profundas

## Notas Metodológicas

- Definición de incumplimiento: 90+ días de mora (dpd_bucket = 90+)
- Ventana de observación: 12 meses posteriores a originación
- Variables del modelo reducido: 7 variables clave seleccionadas por estabilidad

### Uso de LLMs en el Proyecto

**Herramientas utilizadas:**
1. GitHub Copilot: Autocompletado de código dentro de PyCharm
2. ChatGPT: Generación de gráficos y modelos de boosting

**Descripción del uso:**
Los prompts utilizados fueron principalmente preguntas puntuales al LLM en lugar de prompts estructurados. El uso principal fue la generación de visualizaciones para explicar los resultados de los modelos.

Ejemplos de consultas realizadas:
- Generación de gráficos mostrando distribución de PD por deciles
- Creación de plots comparativos del desempeño entre Random Forest y XGBoost
- Visualización del análisis de cosechas mostrando default rate por vintage
- Implementación de XGBoost para clasificación binaria

Nota: Los prompts específicos no fueron almacenados durante el desarrollo. El patrón de trabajo fue iterativo: consulta, código generado, ajuste manual y validación de resultados.

## Próximos Pasos

1. Calibración trimestral del modelo
2. Incorporar variables alternativas (bureau extendido, comportamiento transaccional)
3. Desarrollar modelos especializados por producto
4. Implementar monitoreo automático de PSI

## Contacto

[Tu nombre]  
[Tu correo]

---

**Nota:** Este README contiene las respuestas completas a las tareas solicitadas. Los resultados numéricos corresponden a los análisis ejecutados sobre el portafolio proporcionado.