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

Se desarrolló un modelo de Regresión Logística utilizando un conjunto reducido de 7 variables a las que se llegaron gracias 
a los p-values generados por el modelo. Este modelo fue seleccionado por su estabilidad y facilidad de explicación en procesos de originación.

**Métricas de desempeño:**
- AUC: 0.6361
- Gini: 0.2721
- KS: 0.2101

**Umbral de decisión:** Se estableció un punto de corte de 0.64 para clasificar y decidir la aprobación.

### 2. Modelo de Incumplimiento a 12 Meses - Seguimiento

Para el seguimiento y monitoreo de la evolución del riesgo, se evaluaron cuatro arquitecturas distintas. Aunque el modelo de Regresión Logística fue seleccionado por su equilibrio, la comparación con los demás modelos permite una gestión integral.

**Modelos Desarrollados y Resultados:**

1. Regresión Logística (Logit): AUC 0.62, Gini 0.270. Es el modelo base.
2. Logit Balanced (Seleccionado): AUC 0.636, Gini 0.272, KS 0.210. Ofrece la mayor estabilidad para el seguimiento de la Probabilidad de Default (PD) continua.
3. Random Forest: AUC 0.618. Mostró un desempeño ligeramente inferior en términos de ordenamiento (Gini).
4. XGBoost: AUC 0.588. En este dataset específico, presentó menor capacidad predictiva que los modelos lineales.

### 3. Análisis de la Información

**¿Cuáles son los principales puntos por observar del universo de clientes, de las variables macroeconómicas y de su tendencia?**

- Universo y Tendencia: Se observa un incremento en la morosidad real en las cosechas más recientes (de 4.1% en 2022 a 7.2% en 2024), coincidiendo con un aumento en la PD promedio.
- Variables Macroeconómicas: La inflación y la tasa de interés (rate) muestran una correlación positiva con el incumplimiento.

**¿Qué variables tienen mayor correlación con el target de incumplimiento?**

- Bureau Score: Es la variable con mayor relación inversa (a menor score, mucho mayor riesgo).
- Rate (Tasa): Relación positiva; mayores tasas aumentan la probabilidad de impago.
- Prev_delin_24m: Antecedentes de morosidad previa incrementan el riesgo.

### 4. Análisis de Cosechas

**¿Qué observas?**

Se observa un deterioro progresivo en la calidad de la cartera:
- Cosechas Tempranas (2022-01, 2023-01): Default real de 4.13% y 6.02% respectivamente.
- Cosechas Recientes (2023-01, 2024-01): El default en 2024-01 sube a 7.28%.

**¿Cómo funciona tu modelo con distintas cosechas, 2 recientes 2 tempranas? ¿Hay algún factor que explique las diferencias?**

El modelo captura esta tendencia, incrementando la avg_pd de 0.44 a 0.57 conforme el entorno se vuelve más riesgoso. El incremento en la inflación y tasas de interés en los periodos recientes explica el aumento del riesgo.

### 5. Evaluación de Modelos

#### a-b. Crear percentiles de PD y calcular métricas

Se dividió la base en deciles (0 al 9).
- Decil 0 (Bajo Riesgo): PD promedio 28.39%, Default real 2.55%, Pérdida esperada $33.7M.
- Decil 9 (Alto Riesgo): PD promedio 71.31%, Default real 11.88%, Pérdida esperada $89.6M.

#### c. Top 5 Variables que explican el modelo

5 Variables Principales (Coeficientes): 
1. Rate (0.166)
2. Prev_delin_24m (0.126)
3. Debt_income (0.121)
4. Utilization (0.114)
5. Inflación (0.060)

#### d. Casos individuales comparados

Los clientes más riesgosos presentan bajos bureau_scores (aprox. 512-560) y alta relación debt_income, mientras que los menos riesgosos tienen scores de 850 y menor uso de líneas.

### 6. Modelo de Originación - Evaluación Práctica

#### a. ¿Usarías este score para originar hoy?

Sí, como herramienta de segmentación y apoyo a la decisión, no como único criterio de originación.

#### b. ¿Con qué restricciones?

Aplicar un punto de corte conservador, realizar revisiones manuales en perfiles limítrofes y establecer límites de exposición por cliente según sus políticas adicionales de crédito.

#### c. ¿Qué monitorearías mensualmente?

Seguimiento de la inflación y la estabilidad del bureau score de los aprobados de igual forma la tasa de interés.

#### d. ¿Qué te preocuparía en 6-12 meses?

El impacto rezagado de las tasas altas y el crecimiento de la pérdida esperada en las cohortes más nuevas, nueva alza en inflación o tasas.

### 7. Stress Testing

#### a. Construir al menos dos escenarios macroeconómicos 1 base y uno adverso

Se definió un escenario base y uno adverso con incremento del 25% en la PD.

#### b. ¿Cómo ajustarías tus PDs bajo estos escenarios?

Se multiplicó la PD base por 1.25, topando el resultado en 1.0 (100%).

#### c. Calcula la pérdida esperada bajo estrés

La pérdida total sube de $625.8M (base) a $782.0M (adverso), un incremento del 24.96%.

#### d. ¿El modelo sigue siendo útil para predecir incumplimientos?

El modelo sigue siendo útil porque el impacto es consistente en todos los deciles (aprox. 25%), lo que valida que el modelo mantiene su capacidad de ordenamiento del riesgo incluso bajo estrés.

## Notas Metodológicas

- Definición de incumplimiento: 90+ días de mora (dpd_bucket = 90+)
- Ventana de observación: 12 meses posteriores a originación

### Uso de LLMs en el Proyecto

Para este trabajo se hizo uso de Copilot como autocompletado dentro de PyCharm y se hizo uso de ChatGPT para la generación de gráficos y los modelos de boosting. El prompt se perdió ya que más que un prompt estructurado eran preguntas puntuales al LLM, pero principalmente fue el generar gráficos que pudieran explicar los resultados de los modelos que se muestran en los notebooks.

## Contacto

[Tu nombre]  
[Tu correo]

---

**Nota:** Este README contiene las respuestas completas a las tareas solicitadas. Los resultados numéricos corresponden a los análisis ejecutados sobre el portafolio proporcionado.