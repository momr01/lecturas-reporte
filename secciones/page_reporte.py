import streamlit as st
import plotly.express as px
from reportes.reportes import generar_pdf
from graficos import graf_ev_lect
import pandas as pd
import unicodedata
import numpy as np
from datetime import datetime






def page_reporte(
        # realvsprog, 
        # df_base, 
        # df_filtrado, 
        # kpi_atraso, 
        # kpi_reglamentarios, 
        # avance_descarga, 
        # porcentaje_pendientes, 
        # lecturas_descargadas, 
        # lecturas_pendientes_total, 
        # promedio_requerido, 
        # anomalias_t2
        ):

     # ============================================================
    # CARGA DE ARCHIVOS OBLIGATORIOS
    # ============================================================
    # st.space("medium")
    st.markdown("## Carga de archivos")

    st.markdown(
        "Para generar el reporte debe cargar obligatoriamente "
        "los dos archivos requeridos."
    )
    st.space("large")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 📄 Archivo de Lecturas")

        st.caption(
        "Formato obligatorio: CSV (.csv). "
        "Debe contener lecturas programadas y realizadas, "
        "incluyendo ftl, tarifa y totales."
    )

        archivo_lecturas = st.file_uploader(
            "Seleccionar archivo de lecturas",
            type=["csv"],
            key="archivo_lecturas"
        )

    with col2:

        st.markdown("### 📄 Archivo de Anomalías T2")

        st.caption(
        "Formato obligatorio: CSV (.csv). "
        "Debe contener las anomalías T2, "
        "incluyendo fechas, datos de ordenes e identificación de anomalías."
    )

        archivo_anomalias = st.file_uploader(
            "Seleccionar archivo anomalías",
            type=["csv"],
            key="archivo_ftl"
        )

    # ============================================================
    # VALIDAR QUE ESTÉN LOS DOS ARCHIVOS
    # ============================================================

    if archivo_lecturas is None or archivo_anomalias is None:

        st.warning(
            "⚠️ Debe cargar ambos archivos para habilitar el reporte."
        )

        return

    # ============================================================
    # A PARTIR DE ACÁ COMIENZA EL REPORTE
    # ============================================================

    st.success("✅ Ambos archivos fueron cargados correctamente.")

    # ------------------------------------------------------------
    # Leer archivos
    # ------------------------------------------------------------

    def cargar_csv_universal(file):

        encodings = [
            "utf-8",
            "utf-8-sig",
            "utf-16",
            "latin1",
            "cp1252"
        ]

        separadores = [",", ";", "\t", "|"]

        for enc in encodings:
            for sep in separadores:
                try:
                    file.seek(0)
                    df = pd.read_csv(
                        file,
                        encoding=enc,
                        sep=sep,
                        engine="python"
                    )

                    # validar que tenga más de una columna
                    if len(df.columns) > 1:
                        
                        # limpiar columnas
                        df.columns = (
                            df.columns
                            .str.strip()
                            .str.lower()
                            .str.replace("\ufeff", "", regex=False)
                        )

                        return df

                except:
                    continue

        raise Exception("No se pudo interpretar el archivo CSV")

    # df_lecturas = pd.read_excel(archivo_lecturas)

    # df_ftl = pd.read_excel(archivo_ftl)
    # df_base = pd.read_csv(archivo_lecturas, sep=";")
    df_base = cargar_csv_universal(archivo_lecturas)

    # limpiar nombres de columnas
    df_base.columns = (
        df_base.columns
        .str.strip()
        .str.lower()
    )
    # -----------------------------------
    # CONVERTIR FECHA
    # -----------------------------------
    df_base["f_lteor"] = pd.to_datetime(
        df_base["f_lteor"],
        format="%d/%m/%Y %H:%M:%S",
        errors="coerce"
    )

    # df_ftl = pd.read_csv(archivo_ftl, sep=";")
    anomalias_t2 = cargar_csv_universal(archivo_anomalias)

   
    st.markdown("""
<style>

.kpi-card{
    //background: linear-gradient(145deg,#111827,#1f2937);
    //background: linear-gradient(145deg,#31405E,#445069);
    border-radius:14px;
    padding:32px;
    text-align:center;
    border:2px solid;
    box-shadow:0 4px 14px rgba(0,0,0,0.35);
    transition:0.2s;
    margin: 20px 0;
}

.kpi-card:hover{
    /*background: red;*/
    transform:translateY(-4px);
    box-shadow:0 10px 22px rgba(0,0,0,0.45);
}

.kpi-title{
    font-size:24px;
    //color:#9ca3af;
    //color: white;
    margin-bottom:6px;
    font-weight: bold;
}

.kpi-value{
    font-size:54px;
    font-weight:700;
}

.kpi-sub{
    font-size:13px;
    //color:#9ca3af;
    color: black;
    margin-top:6px;
}
            

/*div[data-testid="stButton"] button {
    background: transparent;
    border: none;
    height: 100%;
}*/

/* CONTENEDOR DEL MODAL */
div[data-testid="stDialog"] div[role="dialog"] {
    width: 90vw !important;
    max-width: 90vw !important;
}

/* CONTENIDO SCROLLEABLE */
div[data-testid="stDialog"] div[role="dialog"] > div {
    max-height: 85vh;
    overflow-y: auto;
    padding-right: 10px;
}

/* evita ese fondo raro abajo */
div[data-testid="stDialog"] {
    background: rgba(0,0,0,0.4);
}
            

            
            
/* Botones KPI */
div[data-testid="column"] button {
    height: 120px;
    border-radius: 16px;
    border: 2px solid #ddd;
    background: white;
    font-size: 16px;
    font-weight: 500;
    white-space: pre-line; /* 👈 permite \n */
    transition: all 0.2s ease;

}

/* Hover */
div[data-testid="column"] button:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

/* Colores específicos por columna */
div[data-testid="column"]:nth-of-type(1) button {
    border-color: #3b82f6;
    color: #3b82f6;
}

div[data-testid="column"]:nth-of-type(2) button {
    border-color: #22c55e;
    color: #22c55e;
}

div[data-testid="column"]:nth-of-type(3) button {
    border-color: #f59e0b;
    color: #f59e0b;
}

/* Tamaño del número (segunda línea) */
div[data-testid="column"] button br + span {
    font-size: 18px;
    font-weight: bold;
}
            
            button {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

</style>
""", unsafe_allow_html=True)





    def generar_tabla_acumulada(df, tarifa):

        tabla = df[df["tarifa"] == tarifa].copy()

        tabla = tabla.sort_values("f_lteor").reset_index(drop=True)

        # ============================================================
        # PROMEDIO REGLAMENTARIOS
        # ============================================================

        # Buscar el primer registro donde TOTAL_LEIDOS_ACTUAL == 0
        filas_cero = tabla[tabla["total_leidos_actual"] == 0]

        if not filas_cero.empty:

            # Posición del primer 0
            indice_cero = filas_cero.index[0]

            if indice_cero > 0:
                # Promedio de reglamentarios desde el primer registro
                # hasta el registro anterior al primer TOTAL_LEIDOS_ACTUAL = 0
                promedio_reglamentarios = (
                    pd.to_numeric(
                        tabla.loc[:indice_cero - 1, "reglamentarios"],
                        errors="coerce"
                    )
                    .mean()
                )

            else:
                # El primer registro ya tiene TOTAL_LEIDOS_ACTUAL = 0
                promedio_reglamentarios = None

        else:

            # Si nunca aparece TOTAL_LEIDOS_ACTUAL = 0,
            # promedio de todos los reglamentarios
            promedio_reglamentarios = (
                pd.to_numeric(
                    tabla["reglamentarios"],
                    errors="coerce"
                )
                .mean()
            )

        # Redondear
        if pd.notna(promedio_reglamentarios):
            promedio_reglamentarios = round(promedio_reglamentarios, 0)

            
        tabla["f_lteor"] = pd.to_datetime(
            tabla["f_lteor"],
            format="%d/%m/%Y %H:%M:%S",
            errors="coerce"
        )

        # Día incremental
        tabla["dias"] = range(1, len(tabla) + 1)

        # Renombrar columnas originales
        tabla["prog"] = tabla["total_programados"]
        tabla["real"] = tabla["total_leidos_actual"]

        # Acumulados
        tabla["prog_ac"] = tabla["prog"].cumsum()
        tabla["prog_real"] = tabla["real"].cumsum()

        # Diferencia acumulada
        tabla["dif"] = tabla["prog_ac"] - tabla["prog_real"]

        # Promedios acumulados por día
        tabla["avg_prog"] = (tabla["prog_ac"] / tabla["dias"]).round(0)
        tabla["avg_real"] = (tabla["prog_real"] / tabla["dias"]).round(0)

        # Diferencia expresada en días
        tabla["dif_dias"] = (np.where(
            tabla["avg_real"] != 0,
            tabla["dif"] / tabla["avg_real"],
            0
        )).round(2)


        


        tabla = tabla.copy()


        # ============================================================
        # CONVERTIR COLUMNAS A NUMÉRICAS
        # ============================================================

        # REAL:
        # 0 es un valor válido.
        # Solo los valores vacíos/no numéricos se convierten en NaN.
        tabla["real"] = (
            tabla["real"]
            .replace("", np.nan)
        )

        tabla["real"] = pd.to_numeric(
            tabla["real"],
            errors="coerce"
        )

        # PROG
        tabla["prog"] = pd.to_numeric(
            tabla["prog"],
            errors="coerce"
        )

        # PROG_REAL
        tabla["prog_real"] = pd.to_numeric(
            tabla["prog_real"],
            errors="coerce"
        )

        # DIF
        # Importante: se convierte a numérico antes de calcular
        # DIF_DIAS_PROY para evitar el error:
        # unsupported operand type(s) for /: 'str' and 'float'
        tabla["dif"] = pd.to_numeric(
            tabla["dif"],
            errors="coerce"
        )


        # ============================================================
        # AVG_PROY
        # ============================================================

        # Equivalente a $E$21 de Excel:
        # último valor de PROG_REAL
        prog_real_final = tabla["prog_real"].iloc[-1]

        dif_final = tabla["dif"].iloc[-1]


        # Equivalente a:
        # CONTAR.BLANCO($D$2:$D$21)
        #
        # Se cuentan únicamente los valores realmente vacíos.
        # cantidad_blancos = realvsprog["real"].isna().sum()
        # cantidad_blancos = realvsprog["real"].is(0).sum()
        cantidad_blancos = (tabla["real"] == 0).sum()


        avg_proy = []


        for i in range(len(tabla)):

            # Valor REAL de la fila actual
            real_actual = tabla["real"].iloc[i]


            # --------------------------------------------------------
            # Si REAL está vacío
            # --------------------------------------------------------

            # if pd.isna(real_actual):
            if real_actual == 0:

                # Equivalente a:
                # SUMA($D$2:D[fila_actual])
                # suma_real_acumulada = (
                #     realvsprog["real"]
                #     .iloc[:i + 1]
                #     .sum(skipna=True)
                # )

                suma_real_acumulada = dif_final

                # Equivalente a:
                #
                # ($E$21 - SUMA($D$2:Dfila))
                # /
                # CONTAR.BLANCO($D$2:$D$21)
                #
                if cantidad_blancos > 0:

                    # promedio_proyectado = (
                    #     prog_real_final - suma_real_acumulada
                    # ) / cantidad_blancos
                    promedio_proyectado = (dif_final / cantidad_blancos).round(0)

                else:

                    promedio_proyectado = None


            # --------------------------------------------------------
            # Si REAL tiene un valor
            # --------------------------------------------------------
            # IMPORTANTE:
            # Un REAL = 0 entra acá.
            # NO se considera vacío.
            #
            # Equivalente a:
            #
            # PROMEDIO($D$2:D[fila_actual])
            # --------------------------------------------------------

            else:

                promedio_proyectado = (
                    tabla["real"]
                    .iloc[:i + 1]
                    .mean()
                ).round(0)


            avg_proy.append(promedio_proyectado)


        # Agregamos AVG_PROY al DataFrame
        tabla["avg_proy"] = avg_proy


        # ============================================================
        # DIF_DIAS_PROY
        # ============================================================

        # Equivalente a:
        #
        # DIF / AVG_PROY
        #
        # Solo se calcula cuando ambos valores existen
        # y AVG_PROY no es 0.

        tabla["dif_dias_proy"] = tabla.apply(
            lambda row:
                (row["dif"] / row["avg_proy"])
                if (
                    pd.notna(row["dif"])
                    and pd.notna(row["avg_proy"])
                    and row["avg_proy"] != 0
                )
                else None,
            axis=1
        ).round(2)


        # Dejar solamente las columnas necesarias
        tabla = tabla[
            [
                "dias",
                "f_lteor",
                "prog",
                "real",
                "prog_ac",
                "prog_real",
                "dif",
                "avg_prog",
                # "avg_real",
                # "dif_dias",
                "avg_proy",
                "dif_dias_proy"
            ]
        ]

        return tabla, promedio_reglamentarios

    
    df_t1, promedio_reglamentarios_t1 = generar_tabla_acumulada(df_base, "T1")
    df_t2, promedio_reglamentarios_t2 = generar_tabla_acumulada(df_base, "T2")


    def obtener_resumen(tabla):

        # Asegurar que la fecha sea datetime
        tabla = tabla.copy()
        tabla["f_lteor"] = pd.to_datetime(tabla["f_lteor"])

        # Ordenar por fecha
        tabla = tabla.sort_values("f_lteor").reset_index(drop=True)

        # Fecha actual
        hoy = pd.Timestamp.today().normalize()

        # ---------------------------------------------------------
        # ATRASO
        # Buscar la fecha de hoy y tomar la fila anterior
        # ---------------------------------------------------------
        # filas_hoy = tabla[tabla["f_lteor"] == hoy]

        # if not filas_hoy.empty:
        #     indice_hoy = filas_hoy.index[0]

        #     if indice_hoy > 0:
        #         atraso = tabla.loc[indice_hoy - 1, "dif_dias_proy"]
        #     else:
        #         atraso = 0
        # else:
        #     # Si hoy no está en la tabla, tomar la última fecha
        #     # anterior a hoy
        #     filas_anteriores = tabla[tabla["f_lteor"] < hoy]

        #     if not filas_anteriores.empty:
        #         atraso = filas_anteriores.iloc[-1]["dif_dias_proy"]
        #     else:
        #         atraso = 0

        # ---------------------------------------------------------
        # ATRASO
        # Buscar el primer registro donde REAL = 0
        # ---------------------------------------------------------

        filas_real_cero = tabla[tabla["real"] == 0]

        if not filas_real_cero.empty:

            # Índice del primer registro con real = 0
            indice_cero = filas_real_cero.index[0]

            # Si el primer real = 0 NO es el primer registro
            if indice_cero > 0:
                atraso = tabla.iloc[indice_cero - 1]["dif_dias_proy"]

            # Si el primer real = 0 es el primer registro
            else:
                atraso = 0

        else:

            # No existe ningún real = 0:
            # tomar dif_dias_proy del último registro
            atraso = tabla.iloc[-1]["dif_dias_proy"]
        # ---------------------------------------------------------
        # ÚLTIMA FILA
        # ---------------------------------------------------------
        final = tabla.iloc[-1]

        prog_ac_final = final["prog_ac"]
        prog_real_final = final["prog_real"]

        # ---------------------------------------------------------
        # AVANCE DE DESCARGA
        # ---------------------------------------------------------
        if prog_ac_final != 0:
            avance_descarga = (
                prog_real_final / prog_ac_final
            ) * 100
        else:
            avance_descarga = 0

        # ---------------------------------------------------------
        # % PENDIENTES
        # ---------------------------------------------------------
        pendientes = 100 - avance_descarga

        # ---------------------------------------------------------
        # RESTO DE VALORES
        # ---------------------------------------------------------
        lecturas_descargadas = final["prog_real"]
        lecturas_pendientes = final["dif"]
        promedio = final["avg_proy"]

        # ---------------------------------------------------------
        # DEVOLVER LOS 6 VALORES
        # ---------------------------------------------------------
        return {
            "ATRASO": atraso,
            "AVANCE DE DESCARGA": avance_descarga,
            "% PENDIENTES": pendientes,
            "LECTURAS DESCARGADAS": lecturas_descargadas,
            "LECTURAS PENDIENTES": lecturas_pendientes,
            "PROMEDIO": promedio
        }






    resumen_t1 = obtener_resumen(df_t1)
    resumen_t2 = obtener_resumen(df_t2)

    
    
    
    
    st.space("large")
    
    st.title("Reporte")




        
    def kpi_visual(titulo, valor, color, sub=""):
        
        st.markdown(
            f"""
            <div class="kpi-card" style="border-color:{color}">
                <div class="kpi-title">{titulo}</div>
                <div class="kpi-value" style="color:{color}">
                    {valor}
                </div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True
        )



#   f"{resumen_t1['ATRASO']}",
#   f"{promedio_reglamentarios_t1:.2f}%",
#  f"{resumen_t1['AVANCE DE DESCARGA']:.2f}%",
#  f"{resumen_t1['% PENDIENTES']:.2f}%",
#  f"{resumen_t1['LECTURAS DESCARGADAS']:,.0f}".replace(",", "."),
#   f"{resumen_t1['LECTURAS PENDIENTES']:,.0f}".replace(",", "."),
#   f"{resumen_t1['PROMEDIO']:,.0f} / día".replace(",", "."),



    st.space("medium") # Añade un espacio grande

    st.subheader("KPI T1")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_visual(
            "ATRASO",
            f"{resumen_t1['ATRASO']:.2f}%",
            "#000000"
        )
    with col2:
        kpi_visual(
            "PLAZOS REGLAMENTARIOS",
            f"{promedio_reglamentarios_t1:.0f}%",
            "#000000"
        )
    with col3:
        kpi_visual(
            "AVANCE DE DESCARGA",
            f"{resumen_t1['AVANCE DE DESCARGA']:.2f}%",
            "#2cb332"
        )
    with col4:
        kpi_visual(
            "% LECTURAS PENDIENTES",
            f"{resumen_t1['% PENDIENTES']:.2f}%",
           "#000000"
        )


    col5, col6, col7 = st.columns(3)
    with col5:
            kpi_visual(
                "LECTURAS DESCARGADAS",
               f"{resumen_t1['LECTURAS DESCARGADAS']:,.0f}".replace(",", "."),
                  "#2cb332"
            )
    with col6:
            kpi_visual(
                "LECTURAS PENDIENTES",
                f"{resumen_t1['LECTURAS PENDIENTES']:,.0f}".replace(",", "."),
                 "#000000"
            )
    with col7:
            kpi_visual(
                "PROMEDIO REQ A DESCARGAR",
               f"{resumen_t1['PROMEDIO']:,.0f} / día".replace(",", "."),
                 "#000000"
            )




    st.space("medium") # Añade un espacio grande

    st.subheader("KPI T2")
    
    col8, col9, col10, col11 = st.columns(4)
    with col8:
        kpi_visual(
             "ATRASO",
                       f"{resumen_t2['ATRASO']:.2f}%",
                        "#000000"
        )
    with col9:
        kpi_visual(
           "PLAZOS REGLAMENTARIOS",
                      f"{promedio_reglamentarios_t2:.0f}%",
                       "#000000"
        )
    with col10:
        kpi_visual(
          "AVANCE DE DESCARGA",
                     f"{resumen_t2['AVANCE DE DESCARGA']:.2f}%",
                      "#CD42F0"
        )
    with col11:
        kpi_visual(
            "% LECTURAS PENDIENTES",
                      f"{resumen_t2['% PENDIENTES']:.2f}%",
                       "#000000"
        )


    col12, col13, col14 = st.columns(3)
    with col12:
            kpi_visual(
                "LECTURAS DESCARGADAS",
                             f"{resumen_t2['LECTURAS DESCARGADAS']:,.0f}".replace(",", "."),
                               "#CD42F0"
            )
    with col13:
            kpi_visual(
                "LECTURAS PENDIENTES",
                             f"{resumen_t2['LECTURAS PENDIENTES']:,.0f}".replace(",", "."),
                             "#000000"
            )
    with col14:
            kpi_visual(
               "PROMEDIO REQ A DESCARGAR",
                            f"{resumen_t2['PROMEDIO']:,.0f} / día".replace(",", "."),
                              "#000000"
            )
    



    st.space("large") # Añade un espacio grande



























    st.subheader("Atraso y Proyección T1")

    st.dataframe(
        df_t1,
        use_container_width=True,
        hide_index=True
    )


    st.subheader("Atraso y Proyección T2")

    st.dataframe(
        df_t2,
        use_container_width=True,
        hide_index=True
    )


































     # ============================================================
    # COPIA DEL DATAFRAME BASE
    # ============================================================

    df_grafico_t1 = df_base.copy()

    # ============================================================
    # FILTRO DE FECHAS
    # ============================================================

    df_grafico_t1["f_lteor"] = pd.to_datetime(
        df_grafico_t1["f_lteor"],
        errors="coerce"
    )

    # FILTRAR TARIFA PRIMERO
    df_grafico_t1 = df_grafico_t1[
        df_grafico_t1["tarifa"] == "T1"
    ].copy()

    df_grafico_t1 = df_grafico_t1.sort_values(
        "f_lteor"
    ).reset_index(drop=True)

    # BUSCAR PRIMER 0
    leidos = pd.to_numeric(
        df_grafico_t1["total_leidos_actual"],
        errors="coerce"
    )

    indices_cero = df_grafico_t1.index[leidos == 0]

    if len(indices_cero) > 0:
        indice_primer_cero = indices_cero[0]

        if indice_primer_cero > 0:
            fecha_fin = df_grafico_t1.loc[
                indice_primer_cero - 1,
                "f_lteor"
            ]
        else:
            fecha_fin = df_grafico_t1["f_lteor"].min()
    else:
        fecha_fin = df_grafico_t1["f_lteor"].max()

    fecha_inicio = df_grafico_t1["f_lteor"].min()

    # APLICAR FECHA FIN
    df_grafico_t1 = df_grafico_t1[
        (df_grafico_t1["f_lteor"] >= fecha_inicio) &
        (df_grafico_t1["f_lteor"] <= fecha_fin)
    ].copy()





    

     # ============================================================
    # COPIA DEL DATAFRAME BASE
    # ============================================================

    df_grafico_t2 = df_base.copy()

    # ============================================================
    # FILTRO DE FECHAS
    # ============================================================

    df_grafico_t2["f_lteor"] = pd.to_datetime(
        df_grafico_t2["f_lteor"],
        errors="coerce"
    )

    # FILTRAR TARIFA PRIMERO
    df_grafico_t2 = df_grafico_t2[
        df_grafico_t2["tarifa"] == "T2"
    ].copy()

    df_grafico_t2 = df_grafico_t2.sort_values(
        "f_lteor"
    ).reset_index(drop=True)

    # BUSCAR PRIMER 0
    leidos = pd.to_numeric(
        df_grafico_t2["total_leidos_actual"],
        errors="coerce"
    )

    indices_cero = df_grafico_t2.index[leidos == 0]

    if len(indices_cero) > 0:
        indice_primer_cero = indices_cero[0]

        if indice_primer_cero > 0:
            fecha_fin = df_grafico_t2.loc[
                indice_primer_cero - 1,
                "f_lteor"
            ]
        else:
            fecha_fin = df_grafico_t2["f_lteor"].min()
    else:
        fecha_fin = df_grafico_t2["f_lteor"].max()

    fecha_inicio = df_grafico_t2["f_lteor"].min()

    # APLICAR FECHA FIN
    df_grafico_t2 = df_grafico_t2[
        (df_grafico_t2["f_lteor"] >= fecha_inicio) &
        (df_grafico_t2["f_lteor"] <= fecha_fin)
    ].copy()










    st.space("large")
    st.subheader("Evolución diaria T1")


    graf_ev_lect(
        # df_filtrado,
        df_grafico_t1,
        col_leidos="total_leidos_actual",
        titulo="Evolución diaria de lecturas s/fecha actual T1",
        key="ev_filtrado_actual_t1",
        titulo_col_leidos="Lecturas realizadas",
        mostrar_val=True
    )


    # st.space("large")
    st.subheader("Evolución diaria T2")

    graf_ev_lect(
            # df_filtrado,
            df_grafico_t2,
            col_leidos="total_leidos_actual",
            titulo="Evolución diaria de lecturas s/fecha actual T2",
            key="ev_filtrado_actual_t2",
            titulo_col_leidos="Lecturas realizadas",
            mostrar_val=True
        )


    
    #     return df_resumen
    def generar_resumen_anomalias(df):
        resumen = {
            "EDESTE": 0,
            "Cooperativa Eléctrica": 0,
            "Telemedición SMC": 0,
            "Telemedición ESG": 0,
            "OSL": 0,
            "CONTRASTE": 0,
            "CAR": 0,
            "Sistemas": 0,
            "Cambio de medidor no actualizado en OPEN": 0,
            "Pendiente de analisis": 0
        }

        observaciones = {
            "EDESTE": "NO DEBEMOS RESOLVERLAS",
            "Cooperativa Eléctrica": "NO DEBEMOS RESOLVERLAS",
            "Telemedición SMC": "Reclamado a T2 NORTE",
            "Telemedición ESG": "Reclamado a T2 NORTE",
            "OSL": "A la espera de resolución de orden",
            "CONTRASTE": "A la espera de resolución de orden",
            "CAR": "A la espera de resolución de orden",
            "Sistemas": "A la espera de resolución de error / inconsistencia en OPEN",
            "Cambio de medidor no actualizado en OPEN": "Reclamado a T2 Norte",
            "Pendiente de analisis": "-"
        }

        # NIC ya procesados
        nics_procesados = set()

        for _, fila in df.iterrows():

            # --------------------------------------------------
            # NIC
            # --------------------------------------------------

            nic = str(fila.get("nic", "")).strip()

            # Si el NIC está vacío, no lo consideramos
            if not nic:
                continue

            # Si el NIC ya fue procesado, no volver a contarlo
            if nic in nics_procesados:
                continue

            # Marcar NIC como procesado
            nics_procesados.add(nic)

            # --------------------------------------------------
            # DATOS DEL REGISTRO
            # --------------------------------------------------

            cliente = str(fila.get("cliente", "")).strip().upper()

            num_itin = str(fila.get("num_itin", "")).strip()

            personal = str(fila.get("personal", "")).strip()

            # Evitar problemas con 8990.0
            if num_itin.endswith(".0"):
                num_itin = num_itin[:-2]

            osl_trat = str(fila.get("osl_trat", "")).strip()
            osl_pend = str(fila.get("osl_pend", "")).strip()
            osl = osl_trat or osl_pend

            contraste_trat = str(fila.get("contraste_trat", "")).strip()
            contraste_pend = str(fila.get("contraste_pend", "")).strip()

            contraste = contraste_trat or contraste_pend
            # contraste = str(fila.get("contraste_trat", "")).strip()

            car_trat = str(fila.get("car_trat", "")).strip()
            car_pend = str(fila.get("car_pend", "")).strip()
            car = car_trat or car_pend

            # estado_contrato = str(fila.get("desc_est", "")).strip()
            estado = str(fila.get("desc_est", "")).strip().upper()

            estado = ''.join(
                c for c in unicodedata.normalize('NFD', estado)
                if unicodedata.category(c) != 'Mn'
            )

            anom_lect = str(
                fila.get("anom_lect", "")
            ).strip().lower()

            # --------------------------------------------------
            # PRIORIDAD 1 - EDESTE
            # --------------------------------------------------

            if "EDESTE" in cliente:

                resumen["EDESTE"] += 1

            # --------------------------------------------------
            # PRIORIDAD 2 - COOPERATIVA ELÉCTRICA
            # --------------------------------------------------

            elif "COOPERATIVA ELECTRICA" in str(cliente).strip().upper():

                resumen["Cooperativa Eléctrica"] += 1
            
             # --------------------------------------------------
            # PRIORIDAD 3 - TELEMEDICIÓN SMC
            # --------------------------------------------------

            elif num_itin in ["8993", "8994", "8995", "8997", "8999"]:

                resumen["Telemedición SMC"] += 1

            # --------------------------------------------------
            # PRIORIDAD 3 - TELEMEDICIÓN ESG
            # --------------------------------------------------

            elif "MT EDEMSA" in str(personal).strip().upper():
                 resumen["Telemedición ESG"] += 1

            # elif "correcta" not in str(estado_contrato).strip().upper():
            #      resumen["Sistemas"] += 1

            elif "SITUACION CORRECTA" not in estado:
                resumen["Sistemas"] += 1

            
            elif "num.med. no coincide" in anom_lect:

                resumen["Cambio de medidor no actualizado en OPEN"] += 1

            # --------------------------------------------------
            # PRIORIDAD 4 - OSL
            # --------------------------------------------------

            elif osl:

                resumen["OSL"] += 1


            elif contraste:

                resumen["CONTRASTE"] += 1

            # --------------------------------------------------
            # PRIORIDAD 5 - CAR
            # --------------------------------------------------

            elif car:

                resumen["CAR"] += 1

            # --------------------------------------------------
            # PRIORIDAD 6 - CAMBIO DE MEDIDOR
            # --------------------------------------------------

          

            # --------------------------------------------------
            # PRIORIDAD 7 - PENDIENTE DE ANÁLISIS
            # --------------------------------------------------

            else:

                resumen["Pendiente de analisis"] += 1

        # --------------------------------------------------
        # CREAR TABLA RESUMEN
        # --------------------------------------------------

        df_resumen = pd.DataFrame([
            {
                "Casos": cantidad,
                "Identificación": categoria,
                "Observación": observaciones[categoria]
            }
            for categoria, cantidad in resumen.items()
            if cantidad > 0
        ])

        return df_resumen



    st.subheader("Anomalías T2")

    resumen_anomalias = generar_resumen_anomalias(anomalias_t2)

    st.dataframe(
        resumen_anomalias,
        use_container_width=True,
        hide_index=True
    )

  


















    # realvsprog = realvsprog.copy()


    # # ============================================================
    # # CONVERTIR COLUMNAS A NUMÉRICAS
    # # ============================================================

    # # REAL:
    # # 0 es un valor válido.
    # # Solo los valores vacíos/no numéricos se convierten en NaN.
    # realvsprog["real"] = (
    #     realvsprog["real"]
    #     .replace("", np.nan)
    # )

    # realvsprog["real"] = pd.to_numeric(
    #     realvsprog["real"],
    #     errors="coerce"
    # )

    # # PROG
    # realvsprog["prog"] = pd.to_numeric(
    #     realvsprog["prog"],
    #     errors="coerce"
    # )

    # # PROG_REAL
    # realvsprog["prog_real"] = pd.to_numeric(
    #     realvsprog["prog_real"],
    #     errors="coerce"
    # )

    # # DIF
    # # Importante: se convierte a numérico antes de calcular
    # # DIF_DIAS_PROY para evitar el error:
    # # unsupported operand type(s) for /: 'str' and 'float'
    # realvsprog["dif"] = pd.to_numeric(
    #     realvsprog["dif"],
    #     errors="coerce"
    # )


    # # ============================================================
    # # AVG_PROY
    # # ============================================================

    # # Equivalente a $E$21 de Excel:
    # # último valor de PROG_REAL
    # prog_real_final = realvsprog["prog_real"].iloc[-1]

    # dif_final = realvsprog["dif"].iloc[-1]


    # # Equivalente a:
    # # CONTAR.BLANCO($D$2:$D$21)
    # #
    # # Se cuentan únicamente los valores realmente vacíos.
    # # cantidad_blancos = realvsprog["real"].isna().sum()
    # # cantidad_blancos = realvsprog["real"].is(0).sum()
    # cantidad_blancos = (realvsprog["real"] == 0).sum()


    # avg_proy = []


    # for i in range(len(realvsprog)):

    #     # Valor REAL de la fila actual
    #     real_actual = realvsprog["real"].iloc[i]


    #     # --------------------------------------------------------
    #     # Si REAL está vacío
    #     # --------------------------------------------------------

    #     # if pd.isna(real_actual):
    #     if real_actual == 0:

    #         # Equivalente a:
    #         # SUMA($D$2:D[fila_actual])
    #         # suma_real_acumulada = (
    #         #     realvsprog["real"]
    #         #     .iloc[:i + 1]
    #         #     .sum(skipna=True)
    #         # )

    #         suma_real_acumulada = dif_final

    #         # Equivalente a:
    #         #
    #         # ($E$21 - SUMA($D$2:Dfila))
    #         # /
    #         # CONTAR.BLANCO($D$2:$D$21)
    #         #
    #         if cantidad_blancos > 0:

    #             # promedio_proyectado = (
    #             #     prog_real_final - suma_real_acumulada
    #             # ) / cantidad_blancos
    #             promedio_proyectado = dif_final / cantidad_blancos

    #         else:

    #             promedio_proyectado = None


    #     # --------------------------------------------------------
    #     # Si REAL tiene un valor
    #     # --------------------------------------------------------
    #     # IMPORTANTE:
    #     # Un REAL = 0 entra acá.
    #     # NO se considera vacío.
    #     #
    #     # Equivalente a:
    #     #
    #     # PROMEDIO($D$2:D[fila_actual])
    #     # --------------------------------------------------------

    #     else:

    #         promedio_proyectado = (
    #             realvsprog["real"]
    #             .iloc[:i + 1]
    #             .mean()
    #         )


    #     avg_proy.append(promedio_proyectado)


    # # Agregamos AVG_PROY al DataFrame
    # realvsprog["avg_proy"] = avg_proy


    # # ============================================================
    # # DIF_DIAS_PROY
    # # ============================================================

    # # Equivalente a:
    # #
    # # DIF / AVG_PROY
    # #
    # # Solo se calcula cuando ambos valores existen
    # # y AVG_PROY no es 0.

    # realvsprog["dif_dias_proy"] = realvsprog.apply(
    #     lambda row:
    #         row["dif"] / row["avg_proy"]
    #         if (
    #             pd.notna(row["dif"])
    #             and pd.notna(row["avg_proy"])
    #             and row["avg_proy"] != 0
    #         )
    #         else None,
    #     axis=1
    # )

    # st.dataframe(
    #     realvsprog,
    #     use_container_width=True,
    #     hide_index=True
    # )













    


    















    pdf = generar_pdf(
        # realvsprog, 
        # df_filtrado, 
        # kpi_atraso, kpi_reglamentarios, avance_descarga, porcentaje_pendientes, lecturas_descargadas, lecturas_pendientes_total, promedio_requerido, 
          resumen_anomalias, resumen_t1, resumen_t2, df_t1, df_t2, promedio_reglamentarios_t1, promedio_reglamentarios_t2, df_grafico_t1, df_grafico_t2)

    st.download_button(
        label="📄 Descargar Reporte",
        data=pdf,
        file_name=f"lecturas_reporte_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )
    