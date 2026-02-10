"""
SCRIPT PRINCIPAL - ANÁLISIS COMPLETO DE RIESGO DE CRÉDITO
==========================================================

Este script ejecuta el análisis completo de riesgo de crédito según 
los requerimientos de las pruebas para Analista de Riesgo de Crédito 2026.

Autor: [Tu Nombre]
Fecha: Febrero 2026

INSTRUCCIONES DE USO:
---------------------
1. Asegúrate de tener los archivos de datos:
   - applications.csv (o similar)
   - performance.csv (o similar)
   - macro.csv (opcional)

2. Actualiza las rutas de los archivos en la sección CONFIGURACIÓN

3. Ejecuta: python main_analysis.py

4. Los resultados se guardarán en:
   - /home/claude/outputs/ (gráficos)
   - /home/claude/results/ (tablas y reportes)
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

# Importar módulos personalizados
from credit_risk_analysis import CreditRiskDataLoader, ExploratoryAnalysis, VintageAnalysis
from credit_risk_models import CreditRiskModel, PDAnalysis
from credit_risk_advanced import StressTesting, IndividualCaseAnalysis, ModelDeploymentAnalysis

# Configuración
import warnings
warnings.filterwarnings('ignore')


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# ACTUALIZAR ESTAS RUTAS CON TUS ARCHIVOS
CONFIG = {
    'applications_path': '/mnt/user-data/uploads/applications.csv',  # Actualizar
    'performance_path': '/mnt/user-data/uploads/performance.csv',     # Actualizar
    'macro_path': None,  # '/mnt/user-data/uploads/macro.csv' si existe
    
    # Configuración del modelo
    'test_size': 0.3,
    'random_state': 42,
    'model_type': 'gradient_boosting',  # 'logistic', 'random_forest', 'gradient_boosting'
    
    # Parámetros de análisis
    'n_percentiles': 10,
    'temporal_split': True,  # True para split temporal, False para aleatorio
}


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def create_output_directories():
    """Crea directorios de salida si no existen"""
    os.makedirs('/home/claude/outputs', exist_ok=True)
    os.makedirs('/home/claude/results', exist_ok=True)
    print("Directorios de salida creados")


def save_dataframe_to_csv(df, filename, folder='/home/claude/results'):
    """Guarda DataFrame a CSV"""
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath, index=False)
    print(f"Guardado: {filepath}")


def print_section_header(title):
    """Imprime encabezado de sección"""
    print("\n" + "="*80)
    print(title.center(80))
    print("="*80 + "\n")


# ============================================================================
# ANÁLISIS PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta todo el análisis"""
    
    print_section_header("ANÁLISIS DE RIESGO DE CRÉDITO - INICIO")
    print(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Crear directorios
    create_output_directories()
    
    # ========================================================================
    # TAREA 1: CARGA Y PREPARACIÓN DE DATOS
    # ========================================================================
    print_section_header("TAREA 1: CARGA Y PREPARACIÓN DE DATOS")
    
    loader = CreditRiskDataLoader(
        applications_path=CONFIG['applications_path'],
        performance_path=CONFIG['performance_path'],
        macro_path=CONFIG['macro_path']
    )
    
    df_applications, df_performance, df_macro = loader.load_data()
    
    # Preparar datasets
    print("\n--- Preparando Dataset de Otorgamiento ---")
    df_origination = loader.prepare_origination_dataset(df_applications, df_performance)
    save_dataframe_to_csv(df_origination, 'df_origination.csv')
    
    print("\n--- Preparando Dataset de Seguimiento ---")
    df_monitoring = loader.prepare_monitoring_dataset(df_applications, df_performance)
    save_dataframe_to_csv(df_monitoring, 'df_monitoring.csv')
    
    # ========================================================================
    # TAREA 2: ANÁLISIS EXPLORATORIO
    # ========================================================================
    print_section_header("TAREA 2: ANÁLISIS EXPLORATORIO DE DATOS")
    
    eda = ExploratoryAnalysis(df_origination)
    
    print("\n--- Estadísticas Descriptivas ---")
    summary_stats = eda.summary_statistics()
    save_dataframe_to_csv(summary_stats, 'summary_statistics.csv')
    
    print("\n--- Análisis de Correlaciones ---")
    correlations = eda.correlation_analysis(target_col='default_12m', top_n=15)
    save_dataframe_to_csv(
        correlations.reset_index().rename(columns={'index': 'variable', 'default_12m': 'correlation'}),
        'correlations.csv'
    )
    
    print("\n--- Análisis Univariado ---")
    eda.univariate_analysis(target_col='default_12m', max_vars=10)
    
    print("\n--- Tendencias Macroeconómicas ---")
    eda.macro_trends_analysis()
    
    # ========================================================================
    # TAREA 3: ANÁLISIS DE COSECHAS (VINTAGE ANALYSIS)
    # ========================================================================
    print_section_header("TAREA 3: ANÁLISIS DE COSECHAS")
    
    vintage = VintageAnalysis(df_origination)
    
    vintage_monthly, vintage_quarterly = vintage.calculate_vintage_default_rates()
    save_dataframe_to_csv(vintage_monthly, 'vintage_monthly.csv')
    save_dataframe_to_csv(vintage_quarterly, 'vintage_quarterly.csv')
    
    # Comparar cosechas (ajustar según tus datos)
    # Identificar periodos disponibles
    available_quarters = sorted(df_origination['orig_month'].dt.to_period('Q').unique().astype(str))
    
    if len(available_quarters) >= 4:
        early_vintages = available_quarters[:2]
        recent_vintages = available_quarters[-2:]
        
        print(f"\nComparando cosechas tempranas {early_vintages} vs recientes {recent_vintages}")
        df_early, df_recent, comparison = vintage.compare_vintages(
            early_vintages, recent_vintages
        )
        save_dataframe_to_csv(comparison, 'vintage_comparison.csv')
    else:
        print("\nNo hay suficientes periodos para comparación de cosechas")
    
    # ========================================================================
    # TAREA 4: MODELO DE INCUMPLIMIENTO - OTORGAMIENTO
    # ========================================================================
    print_section_header("TAREA 4: MODELO DE INCUMPLIMIENTO EN OTORGAMIENTO")
    
    # Preparar datos
    origination_model = CreditRiskModel(
        df=df_origination,
        target_col='default_12m',
        test_size=CONFIG['test_size'],
        random_state=CONFIG['random_state']
    )
    
    X, y = origination_model.prepare_features()
    X_train, X_test, y_train, y_test = origination_model.train_test_split_data(
        X, y, temporal_split=CONFIG['temporal_split']
    )
    
    # Entrenar modelo
    model = origination_model.train_model(
        X_train, y_train, 
        model_type=CONFIG['model_type']
    )
    
    # Evaluar modelo
    origination_results = origination_model.evaluate_model(X_test, y_test)
    
    # Feature importance
    feature_imp = origination_model.feature_importance(top_n=15)
    save_dataframe_to_csv(feature_imp, 'feature_importance_origination.csv')
    
    # ========================================================================
    # TAREA 5: MODELO DE INCUMPLIMIENTO - SEGUIMIENTO
    # ========================================================================
    print_section_header("TAREA 5: MODELO DE INCUMPLIMIENTO EN SEGUIMIENTO")
    
    # Tomar una muestra si el dataset es muy grande
    df_monitoring_sample = df_monitoring.sample(
        n=min(100000, len(df_monitoring)), 
        random_state=CONFIG['random_state']
    )
    
    monitoring_model = CreditRiskModel(
        df=df_monitoring_sample,
        target_col='default_next_12m',
        test_size=CONFIG['test_size'],
        random_state=CONFIG['random_state']
    )
    
    X_mon, y_mon = monitoring_model.prepare_features()
    X_train_mon, X_test_mon, y_train_mon, y_test_mon = monitoring_model.train_test_split_data(
        X_mon, y_mon, temporal_split=False
    )
    
    model_mon = monitoring_model.train_model(
        X_train_mon, y_train_mon,
        model_type=CONFIG['model_type']
    )
    
    monitoring_results = monitoring_model.evaluate_model(X_test_mon, y_test_mon)
    
    feature_imp_mon = monitoring_model.feature_importance(top_n=15)
    save_dataframe_to_csv(feature_imp_mon, 'feature_importance_monitoring.csv')
    
    # ========================================================================
    # TAREA 6: ANÁLISIS DE PD POR PERCENTILES
    # ========================================================================
    print_section_header("TAREA 6: ANÁLISIS DE PD POR PERCENTILES")
    
    # Crear DataFrame de test con información adicional
    df_test_orig = df_origination.loc[X_test.index]
    
    pd_analysis = PDAnalysis(
        y_test=origination_results['y_test'],
        y_pred_proba=origination_results['predictions'],
        df_test=df_test_orig
    )
    
    percentile_analysis, results_df = pd_analysis.create_pd_percentiles(
        n_percentiles=CONFIG['n_percentiles']
    )
    save_dataframe_to_csv(percentile_analysis, 'pd_percentile_analysis.csv')
    
    # ========================================================================
    # TAREA 7: STRESS TESTING
    # ========================================================================
    print_section_header("TAREA 7: STRESS TESTING")
    
    stress_test = StressTesting(
        model=origination_model,
        X_test=X_test,
        y_test=y_test,
        df_test=df_test_orig
    )
    
    stress_results, pd_predictions = stress_test.run_stress_test()
    save_dataframe_to_csv(stress_results, 'stress_test_results.csv')
    
    # ========================================================================
    # TAREA 8: ANÁLISIS DE CASOS INDIVIDUALES
    # ========================================================================
    print_section_header("TAREA 8: ANÁLISIS DE CASOS INDIVIDUALES")
    
    case_analysis = IndividualCaseAnalysis(
        model=origination_model.model,
        X=X_test,
        feature_names=origination_model.feature_names
    )
    
    # Identificar casos de alto y bajo riesgo
    y_pred_all = origination_model.predict(X_test)
    high_risk_indices = np.argsort(y_pred_all)[-5:]  # Top 5 más riesgosos
    low_risk_indices = np.argsort(y_pred_all)[:5]    # Top 5 menos riesgosos
    
    # Comparar algunos casos
    print("\n--- Comparando Top 3 Alto Riesgo vs Top 3 Bajo Riesgo ---")
    cases_data, comparison = case_analysis.compare_cases(
        case_indices=list(high_risk_indices[:3]) + list(low_risk_indices[:3]),
        case_labels=['Alto_1', 'Alto_2', 'Alto_3', 'Bajo_1', 'Bajo_2', 'Bajo_3']
    )
    save_dataframe_to_csv(comparison.T, 'case_comparison.csv')
    
    # Explicar diferencias
    differences = case_analysis.explain_high_vs_low_risk(
        high_risk_idx=high_risk_indices[-1],
        low_risk_idx=low_risk_indices[0]
    )
    save_dataframe_to_csv(differences, 'risk_differences_explanation.csv')
    
    # ========================================================================
    # TAREA 9: RECOMENDACIONES DE DEPLOYMENT
    # ========================================================================
    print_section_header("TAREA 9: RECOMENDACIONES DE DEPLOYMENT")
    
    recommendations = ModelDeploymentAnalysis.generate_deployment_recommendations(
        model_results=origination_results,
        stress_results=stress_results,
        vintage_analysis=vintage_quarterly
    )
    
    # Guardar dashboard template
    dashboard_template = ModelDeploymentAnalysis.create_monitoring_dashboard_template()
    with open('/home/claude/results/monitoring_dashboard_template.txt', 'w') as f:
        f.write(dashboard_template)
    print("\nTemplate de dashboard guardado")
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    print_section_header("RESUMEN EJECUTIVO")
    
    print(f"""
    MODELO DE OTORGAMIENTO:
    ----------------------
    - AUC: {origination_results['auc']:.4f}
    - Observaciones test: {len(y_test):,}
    - Default rate real: {y_test.mean()*100:.2f}%
    - Default rate predicho: {origination_results['predictions'].mean()*100:.2f}%
    
    MODELO DE SEGUIMIENTO:
    ---------------------
    - AUC: {monitoring_results['auc']:.4f}
    - Observaciones test: {len(y_test_mon):,}
    - Default rate real: {y_test_mon.mean()*100:.2f}%
    
    STRESS TESTING:
    --------------
    - Escenario Base - PD promedio: {stress_results.loc[0, 'avg_pd']*100:.2f}%
    - Escenario Adverso - Incremento PD: +{stress_results.loc[1, 'pd_change_pct']:.1f}%
    - Escenario Severo - Incremento PD: +{stress_results.loc[2, 'pd_change_pct']:.1f}%
    
    ARCHIVOS GENERADOS:
    ------------------
    - Gráficos: /home/claude/*.png
    - Tablas: /home/claude/results/*.csv
    - Dashboard template: /home/claude/results/monitoring_dashboard_template.txt
    """)
    
    print_section_header("ANÁLISIS COMPLETADO")
    print(f"Tiempo total: {datetime.now()}")
    print("\n¡Todos los análisis han sido completados exitosamente!")
    print("\nPróximos pasos:")
    print("1. Revisar los gráficos generados en /home/claude/")
    print("2. Analizar las tablas en /home/claude/results/")
    print("3. Preparar presentación con hallazgos clave")
    print("4. Documentar supuestos y limitaciones del modelo")


# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nVerifica:")
        print("1. Las rutas de los archivos en CONFIG")
        print("2. Que los archivos CSV tengan las columnas esperadas")
        print("3. Los mensajes de error anteriores para más detalles")
        import traceback
        traceback.print_exc()
