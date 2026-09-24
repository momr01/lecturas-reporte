import pandas as pd
import matplotlib.pyplot as plt

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)
from reportlab.lib.enums import TA_CENTER

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
import numpy as np
import pandas as pd
#    from reportlab.platypus import (
#         Table,
#         TableStyle,
#         Paragraph,
#         Spacer
#     )

#     from reportlab.lib import colors
#     from reportlab.lib.units import cm
#     from reportlab.lib.styles import ParagraphStyle


from io import BytesIO
import tempfile


# ==========================================
# DATOS EJEMPLO
# ==========================================

df = pd.DataFrame({
    "Dia": [1, 2, 3, 4, 5],
    "Programado": [100, 120, 150, 170, 200],
    "Real": [90, 130, 140, 180, 210]
})


# ==========================================
# GRAFICO MATPLOTLIB
# ==========================================

def generar_grafico_png(path_archivo):

    plt.figure(figsize=(12, 5))

    plt.plot(
        df["Dia"],
        df["Programado"],
        marker="o",
        linewidth=2,
        label="Programado"
    )

    plt.plot(
        df["Dia"],
        df["Real"],
        marker="o",
        linewidth=2,
        label="Real"
    )

    plt.title("Evolución diaria")
    plt.xlabel("Día")
    plt.ylabel("Cantidad")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        path_archivo,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()







# ==========================================
# PDF
# ==========================================

def generar_pdf(
        # realvsprog, 
        # df_filtrado, 
        # kpi_atraso, kpi_reglamentarios, avance_descarga, porcentaje_pendientes, lecturas_descargadas, lecturas_pendientes_total, promedio_requerido, 
        resumen_anomalias, resumen_t1, resumen_t2, df_t1, df_t2, promedio_reglamentarios_t1, promedio_reglamentarios_t2, df_grafico_t1, df_grafico_t2):

    # df_filtrado_t1 = df_filtrado[df_filtrado["tarifa"].isin(["T1"])]
    # df_filtrado_t2 = df_filtrado[df_filtrado["tarifa"].isin(["T2"])]
    # df_filtrado_t1 = df_filtrado[df_filtrado["tarifa"] == "T1" ]
    # df_filtrado_t2 = df_filtrado[df_filtrado["tarifa"] == "T2" ]

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1 * cm,
        leftMargin=1 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm
    )

    doc = SimpleDocTemplate(
    buffer,
    pagesize=landscape(A4)
)

    styles = getSampleStyleSheet()

    elements = []

    # ==========================================
    # TITULO PRINCIPAL
    # ==========================================

    # titulo = Paragraph(
    #     "<b><u>Estado actual de anomalías T2 / descarga de lecturas</u></b>",
    #     styles["Title"]
    # )
    from datetime import datetime

    fecha_actual = datetime.now().strftime("%d/%m/%Y")

    titulo = Paragraph(
        f"<b><u>Estado actual de anomalías T2 / descarga de lecturas {fecha_actual}</u></b>",
        styles["Title"]
    )

    elements.append(titulo)
    elements.append(Spacer(1, 20))




    














    saludo = Paragraph(
        """
        Buenas tardes.
        """,
        styles["BodyText"]
    )

    elements.append(saludo)
    # elements.append(Spacer(1, 20))


    preambulo = Paragraph(
        """
        Comparto el grado de avance de lecturas al día de la fecha:
        """,
        styles["BodyText"]
    )

    elements.append(preambulo)
    elements.append(Spacer(1, 20))




    subt1 = Paragraph(
        """
        <u><b>LECTURAS</b></u>
        """,
        styles["Heading3"]
    )

    elements.append(subt1)
    elements.append(Spacer(1, 10))






    ######################################################################
    #### KPIS

    # from reportlab.platypus import Table, TableStyle, Paragraph
    # from reportlab.lib import colors

#     def crear_kpi_pdf(titulo, valor, color_hex):

#         data = [
#             [Paragraph(f"<b>{titulo}</b>", styles["BodyText"])],
#             [Paragraph(
#                 f"<font color='{color_hex}' size='20'><b>{valor}</b></font>",
#                 styles["BodyText"]
#             )]
#         ]

#         tabla = Table(
#             data,
#             colWidths=5.5*cm,
#             rowHeights=[1.2*cm, 1.8*cm]
#         )

#         tabla.setStyle(TableStyle([
#             ("BOX", (0,0), (-1,-1), 2, colors.HexColor(color_hex)),
#             ("BACKGROUND", (0,0), (-1,-1), colors.white),
#             ("ALIGN", (0,0), (-1,-1), "CENTER"),
#             ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

#             ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
#             ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#6b7280")),

#             ("BOTTOMPADDING", (0,0), (-1,-1), 10),
#             ("TOPPADDING", (0,0), (-1,-1), 10),
#         ]))

#         return tabla


# #     elements.append(
# #     Paragraph(
# #         "<b>Dashboard de Lecturas</b>",
# #         styles["Title"]
# #     )
# # )

#     elements.append(Spacer(1,15))


#     kpi1 = crear_kpi_pdf(
#     "ATRASO",
#     f"{kpi_atraso}",
#     "#f01212"
# )

#     kpi2 = crear_kpi_pdf(
#         "PLAZOS REGLAMENTARIOS",
#         f"{kpi_reglamentarios:.2f}%",
#         "#3b82f6"
#     )

#     kpi3 = crear_kpi_pdf(
#         "AVANCE",
#         f"{avance_descarga:.2f}%",
#         "#22c55e"
#     )

#     kpi4 = crear_kpi_pdf(
#         "% LECTURAS PENDIENTES",
#         f"{porcentaje_pendientes:.2f}%",
#         "#f59e0b"
#     )

#     kpi5 = crear_kpi_pdf(
#         "LECTURAS DESCARGADAS",
#         f"{lecturas_descargadas:,.0f}".replace(",", "."),
#         "#2ed12e"
#     )

#     kpi6 = crear_kpi_pdf(
#         "LECTURAS PENDIENTES",
#         f"{lecturas_pendientes_total:,.0f}".replace(",", "."),
#         "#ff1d1d"
#     )

#     dashboard = Table([
#     [kpi1, kpi2, kpi3, kpi4],
#     [kpi4, kpi5, kpi6, kpi5]
# ])

#     dashboard.setStyle(TableStyle([
#         ("VALIGN", (0,0), (-1,-1), "TOP"),
#         ("LEFTPADDING", (0,0), (-1,-1), 5),
#         ("RIGHTPADDING", (0,0), (-1,-1), 5),
#         ("TOPPADDING", (0,0), (-1,-1), 5),
#         ("BOTTOMPADDING", (0,0), (-1,-1), 5),
#     ]))


#     elements.append(dashboard)
#     elements.append(Spacer(1,20))






    ###########################################################################











#     def crear_kpi_pdf(titulo, valor, color_hex):
#         data = [
#             [Paragraph(f"<b>{titulo}</b>", styles["BodyText"])],
#             [Paragraph(
#                 f"<font color='{color_hex}' size='14'><b>{valor}</b></font>",
#                 styles["BodyText"]
#             )]
#         ]

#         tabla = Table(
#             data,
#             # colWidths=5.2 * cm,
#             # rowHeights=[1.1 * cm, 1.6 * cm]
#             colWidths=2.8*cm,
#     rowHeights=[0.8*cm, 1.2*cm]
#         )

#         tabla.setStyle(TableStyle([
#             ("BOX", (0, 0), (-1, -1), 1.5, colors.HexColor(color_hex)),
#             ("BACKGROUND", (0, 0), (-1, -1), colors.white),
#             ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

#             ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#             ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#6b7280")),

#             ("TOPPADDING", (0, 0), (-1, -1), 6),
#             ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
#         ]))

#         return tabla


#     def build_kpi_column(kpis):
#         """
#         kpis: lista de tablas KPI (crear_kpi_pdf)
#         arma filas de 4 KPIs por fila
#         """
#         rows = []
#         chunk_size = 4

#         for i in range(0, len(kpis), chunk_size):
#             row = kpis[i:i + chunk_size]

#             # completar fila si faltan espacios
#             while len(row) < chunk_size:
#                 row.append("")

#             rows.append(row)

#         table = Table(
#             rows,
#             colWidths=[5.2 * cm] * 4
#         )

#         table.setStyle(TableStyle([
#             ("VALIGN", (0, 0), (-1, -1), "TOP"),
#             ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#             ("LEFTPADDING", (0, 0), (-1, -1), 4),
#             ("RIGHTPADDING", (0, 0), (-1, -1), 4),
#             ("TOPPADDING", (0, 0), (-1, -1), 6),
#             ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
#         ]))

#         return table


#     # =========================
#     # KPI DATA (ejemplo limpio)
#     # =========================

#     kpis_t1 = [
#         crear_kpi_pdf("ATRASO", kpi_atraso, "#f01212"),
#         crear_kpi_pdf("PLAZOS REGLAMENTARIOS", f"{kpi_reglamentarios:.2f}%", "#3b82f6"),
#         crear_kpi_pdf("AVANCE", f"{avance_descarga:.2f}%", "#22c55e"),
#         crear_kpi_pdf("% PENDIENTES", f"{porcentaje_pendientes:.2f}%", "#f59e0b"),
#         crear_kpi_pdf("LECTURAS DESCARGADAS", f"{lecturas_descargadas:,.0f}".replace(",", "."), "#2ed12e"),
#         crear_kpi_pdf("LECTURAS PENDIENTES", f"{lecturas_pendientes_total:,.0f}".replace(",", "."), "#ff1d1d"),
#     ]

#     kpis_t2 = [
#         crear_kpi_pdf("ATRASO", kpi_atraso, "#f01212"),
#         crear_kpi_pdf("PLAZOS REGLAMENTARIOS", f"{kpi_reglamentarios:.2f}%", "#3b82f6"),
#         crear_kpi_pdf("AVANCE", f"{avance_descarga:.2f}%", "#22c55e"),
#         crear_kpi_pdf("% PENDIENTES", f"{porcentaje_pendientes:.2f}%", "#f59e0b"),
#         crear_kpi_pdf("LECTURAS DESCARGADAS", f"{lecturas_descargadas:,.0f}".replace(",", "."), "#2ed12e"),
#         crear_kpi_pdf("LECTURAS PENDIENTES", f"{lecturas_pendientes_total:,.0f}".replace(",", "."), "#ff1d1d"),
#     ]


#     # =========================
#     # COLUMNAS PRINCIPALES
#     # =========================

#     col_t1 = build_kpi_column(kpis_t1)
#     col_t2 = build_kpi_column(kpis_t2)


#     # dashboard = Table(
#     #     [[col_t1, col_t2]],
#     #     colWidths=[9 * cm, 9 * cm]  # separación clara entre T1 y T2
#     # )
#     dashboard = Table(
#         [[col_t1, "", col_t2]],
#         colWidths=[
#         12*cm,
#         1*cm,
#         12*cm
#     ]
#         # colWidths=[9 * cm, 9 * cm]  # separación clara entre T1 y T2
#     )

#     # dashboard.setStyle(TableStyle([
#     #     ("VALIGN", (0, 0), (-1, -1), "TOP"),

#     #     # espacio visual entre columnas (clave)
#     #     ("LEFTPADDING", (0, 0), (-1, -1), 10),
#     #     ("RIGHTPADDING", (0, 0), (-1, -1), 10),
#     #     ("TOPPADDING", (0, 0), (-1, -1), 10),
#     #     ("BOTTOMPADDING", (0, 0), (-1, -1), 10),

#     #     # línea divisoria suave entre T1 y T2 (opcional)
#     #     ("LINEBEFORE", (1, 0), (1, -1), 0.8, colors.HexColor("#e5e7eb")),
#     # ]))
#     dashboard.setStyle(TableStyle([
#     ("VALIGN", (0,0), (-1,-1), "TOP"),
#     ("ALIGN", (0,0), (-1,-1), "CENTER"),
# ]))


#     elements.append(Spacer(1, 15))
#     elements.append(dashboard)
#     elements.append(Spacer(1, 20))









#########################################




# from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
# from reportlab.lib import colors
# from reportlab.lib.units import cm


# ==========================================
# KPI CARD PDF
# ==========================================

    # def crear_kpi_pdf(titulo, valor, color_hex):

    #     data = [
    #         [Paragraph(f"<font size='12'><b>{titulo}</b></font>", styles["BodyText"])],
    #         [Paragraph(
    #             f"<font color='{color_hex}' size='18'><b>{valor}</b></font>",
    #             styles["BodyText"]
    #         )]
    #     ]

    #     tabla = Table(
    #         data,
    #         # colWidths=2.2 * cm,
    #         # colWidths=5.5*cm,
    #         # rowHeights=[1.2*cm, 1.8*cm]
    #          colWidths=3.2 * cm,
    #          rowHeights=[0.8 * cm, 1.2 * cm]
    #     )

    #     tabla.setStyle(TableStyle([
    #         ("BOX", (0, 0), (-1, -1), 2, colors.HexColor(color_hex)),
    #         ("BACKGROUND", (0, 0), (-1, -1), colors.white),

    #         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    #         ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

    #         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    #         ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#6b7280")),

    #         ("TOPPADDING", (0, 0), (-1, -1), 4),
    #         ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    #     ]))

    #     return tabla


    # # ==========================================
    # # CREAR KPIS T1
    # # ==========================================

    # kpi_t1_1 = crear_kpi_pdf("ATRASO", f"{kpi_atraso}", "#f01212")
    # kpi_t1_2 = crear_kpi_pdf("PLAZOS REGLAMENTARIOS", f"{kpi_reglamentarios:.2f}%", "#3b82f6")
    # kpi_t1_3 = crear_kpi_pdf("AVANCE DE DESCARGA", f"{avance_descarga:.2f}%", "#22c55e")
    # kpi_t1_4 = crear_kpi_pdf("% LECTURAS PENDIENTES", f"{porcentaje_pendientes:.2f}%", "#f59e0b")
    # kpi_t1_5 = crear_kpi_pdf("LECTURAS DESCARGADAS", f"{lecturas_descargadas:,.0f}", "#f01212")
    # kpi_t1_6 = crear_kpi_pdf("LECTURAS PENDIENTES", f"{lecturas_pendientes_total:,.0f}", "#3b82f6")
    # kpi_t1_7 = crear_kpi_pdf("PROM REQ A DESCARGAR", f"{promedio_requerido:,.0f} / día", "#22c55e")


    # # ==========================================
    # # CREAR KPIS T2
    # # ==========================================

    # kpi_t2_1 = crear_kpi_pdf("DESCARG", f"{lecturas_descargadas:,.0f}".replace(",", "."), "#2ed12e")
    # kpi_t2_2 = crear_kpi_pdf("PENDIENTES", f"{lecturas_pendientes_total:,.0f}".replace(",", "."), "#ff1d1d")
    # kpi_t2_3 = crear_kpi_pdf("PROMEDIO", f"{porcentaje_pendientes:,.0f}", "#c210ee")
    # kpi_t2_4 = crear_kpi_pdf("ANOMALÍAS", "133", "#aa2f54")


    # # ==========================================
    # # TABLA T1 Y T2 (4 KPIS POR FILA)
    # # ==========================================

    # tabla_t1 = Table([
    #     [kpi_t1_1, kpi_t1_2, kpi_t1_3, kpi_t1_4],
    #     [kpi_t1_5, kpi_t1_6, kpi_t1_7]
    # ])

    # tabla_t2 = Table([
    #     [kpi_t2_1, kpi_t2_2, kpi_t2_3, kpi_t2_4]
    # ])


    # tabla_t1.setStyle(TableStyle([
    #     ("VALIGN", (0, 0), (-1, -1), "TOP"),
    #     ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    # ]))

    # tabla_t2.setStyle(TableStyle([
    #     ("VALIGN", (0, 0), (-1, -1), "TOP"),
    #     ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    # ]))


    # # ==========================================
    # # TITULOS
    # # ==========================================

    # titulo_t1 = Paragraph(
    #     "<para align='center'><b><u>LECTURAS T1</u></b></para>",
    #     styles["Heading3"]
    # )

    # titulo_t2 = Paragraph(
    #     "<para align='center'><b><u>LECTURAS T2</u></b></para>",
    #     styles["Heading3"]
    # )


    # # ==========================================
    # # DASHBOARD PRINCIPAL 2 COLUMNAS
    # # ==========================================

    # dashboard = Table(
    #     [
    #         [titulo_t1, "", titulo_t2],
    #         [tabla_t1, "", tabla_t2]
    #     ],
    #     colWidths=[
    #         # 9 * cm,   # T1
    #         # 1 * cm,   # separación
    #         # 9 * cm    # T2
    #         13 * cm,   # T1
    #         1 * cm,   # separación
    #         13 * cm    # T2
    #     ]
    # )

    # dashboard.setStyle(TableStyle([
    #     ("VALIGN", (0, 0), (-1, -1), "TOP"),
    #     ("ALIGN", (0, 0), (-1, -1), "CENTER"),

    #     ("LEFTPADDING", (0, 0), (-1, -1), 5),
    #     ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    #     ("TOPPADDING", (0, 0), (-1, -1), 5),
    #     ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    # ]))


    # # ==========================================
    # # AGREGAR AL PDF
    # # ==========================================

    # elements.append(dashboard)
    # elements.append(Spacer(1, 20))





















# ============================================================
# IMPORTACIONES
# ============================================================

 


    # ============================================================
    # ESTILO PARA TÍTULOS DE LOS KPI
    # ============================================================
    #
    # Los títulos largos se pueden dividir automáticamente
    # en 2 líneas dentro del ancho disponible.
    # ============================================================

    estilo_titulo_kpi = ParagraphStyle(
        "TituloKPI",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=12,
        textColor=colors.HexColor("#6b7280"),
        alignment=1,
        spaceBefore=0,
        spaceAfter=0,
    )


    # ============================================================
    # ESTILO PARA VALORES DE LOS KPI
    # ============================================================

    estilo_valor_kpi = ParagraphStyle(
        "ValorKPI",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=20,
        alignment=1,
        spaceBefore=0,
        spaceAfter=0,
    )


    # ============================================================
    # FUNCIÓN PARA CREAR UN KPI
    # ============================================================

    def crear_kpi_pdf2(titulo, valor, color_hex, ancho_kpi):

        # --------------------------------------------------------
        # TÍTULO
        #
        # Paragraph permite que los títulos largos se dividan
        # automáticamente en varias líneas.
        # --------------------------------------------------------

        titulo_paragraph = Paragraph(
            titulo,
            estilo_titulo_kpi
        )

        # --------------------------------------------------------
        # VALOR
        # --------------------------------------------------------

        valor_paragraph = Paragraph(
            f'<font color="{color_hex}"><b>{valor}</b></font>',
            estilo_valor_kpi
        )

        data = [
            [titulo_paragraph],
            [valor_paragraph]
        ]

        # --------------------------------------------------------
        # ALTURA FIJA
        #
        # La primera fila tiene suficiente espacio para que
        # los títulos largos ocupen hasta 2 líneas.
        # --------------------------------------------------------

        tabla = Table(
            data,
            colWidths=[ancho_kpi],
            rowHeights=[
                1.20 * cm,   # Título
                1.20 * cm    # Valor
            ]
        )

        tabla.setStyle(TableStyle([

            # ----------------------------------------------------
            # BORDE
            # ----------------------------------------------------

            (
                "BOX",
                (0, 0),
                (-1, -1),
                2,
                colors.HexColor(color_hex)
            ),

            # ----------------------------------------------------
            # FONDO
            # ----------------------------------------------------

            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.white
            ),

            # ----------------------------------------------------
            # ALINEACIÓN
            # ----------------------------------------------------

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            # ----------------------------------------------------
            # PADDING
            # ----------------------------------------------------

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                3
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                3
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
        ]))

        return tabla


    # ============================================================
    # CONFIGURACIÓN DEL DASHBOARD
    # ============================================================

    # El dashboard tiene dos bloques:
    #
    # T1 = 13 cm
    # separación = 1 cm
    # T2 = 13 cm
    #
    # Esto mantiene la estructura que ya tenías.
    # ============================================================

    ancho_t1 = 13 * cm
    ancho_separacion = 1 * cm
    ancho_t2 = 13 * cm


    # ============================================================
    # ANCHO DE CADA KPI
    # ============================================================
    #
    # T1 tiene 4 KPIs por fila.
    #
    # Dejamos pequeños márgenes entre los KPI.
    # ============================================================

    ancho_kpi_t1 = (ancho_t1 - (3 * 0.10 * cm)) / 4

    ancho_kpi_t2 = (ancho_t2 - (3 * 0.10 * cm)) / 4


    # ============================================================
    # CREAR KPIS T1
    # ============================================================

# print(resumen_t1["ATRASO"])
# print(resumen_t1["AVANCE DE DESCARGA"])
# print(resumen_t1["% PENDIENTES"])
# print(resumen_t1["LECTURAS DESCARGADAS"])
# print(resumen_t1["LECTURAS PENDIENTES"])
# print(resumen_t1["PROMEDIO"])


    def crear_kpi_pdf3(titulo, valor, color_hex, ancho_kpi, alto_kpi=None):

        # --------------------------------------------------------
        # ESTILO TÍTULO
        # --------------------------------------------------------

        estilo_titulo_kpi_dinamico = ParagraphStyle(
            "titulo_kpi_dinamico",
            parent=estilo_titulo_kpi,
            alignment=TA_CENTER,
            wordWrap="LTR",
            # wordWrap="CJK",
            splitLongWords=True,
            leading=10
        )

        titulo_paragraph = Paragraph(
            titulo,
            estilo_titulo_kpi_dinamico
        )

        # --------------------------------------------------------
        # VALOR
        # --------------------------------------------------------

        valor_paragraph = Paragraph(
            f'<font color="{color_hex}"><b>{valor}</b></font>',
            estilo_valor_kpi
        )

        data = [
            [titulo_paragraph],
            [valor_paragraph]
        ]

        # --------------------------------------------------------
        # TABLA KPI
        # --------------------------------------------------------

        if alto_kpi is None:

            tabla = Table(
                data,
                colWidths=[ancho_kpi]
            )

        else:

            tabla = Table(
                data,
                colWidths=[ancho_kpi],
                rowHeights=[
                    alto_kpi / 2,
                    alto_kpi / 2
                ]
            )

        tabla.setStyle(TableStyle([

            # Borde
            (
                "BOX",
                (0, 0),
                (-1, -1),
                2,
                colors.HexColor(color_hex)
            ),

            # Fondo
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.white
            ),

            # Alineación
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            # Padding
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                5
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),

        ]))

        return tabla


    def crear_kpi_pdf(titulo, valor, color_hex, ancho_kpi, alto_kpi=None):

        estilo_titulo_kpi_dinamico = ParagraphStyle(
            "titulo_kpi_dinamico",
            parent=estilo_titulo_kpi,
            alignment=TA_CENTER,
            wordWrap="LTR",
            splitLongWords=True,
            leading=10,
            textColor=colors.HexColor("#ffffff"),
        )

        titulo_parrafo = Paragraph(
            str(titulo),
            estilo_titulo_kpi_dinamico
        )

        valor_parrafo = Paragraph(
            str(valor),
            estilo_valor_kpi
        )

        # Si se especifica un alto, todos los KPI tendrán exactamente
        # la misma altura.
        if alto_kpi is not None:

            tabla = Table(
                [
                    [titulo_parrafo],
                    [valor_parrafo]
                ],
                colWidths=[ancho_kpi],
                rowHeights=[
                    alto_kpi / 2,
                    alto_kpi / 2
                ]
            )

        else:

            # Primera creación: altura natural
            tabla = Table(
                [
                    [titulo_parrafo],
                    [valor_parrafo]
                ],
                colWidths=[ancho_kpi]
            )

        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), color_hex),
            ("BACKGROUND", (0, 1), (-1, 1), colors.white),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("BOX", (0, 0), (-1, -1), 0.5, color_hex),

            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))

        return tabla

    kpi_t1_1 = crear_kpi_pdf(
        "ATRASO",
        f"{resumen_t1['ATRASO']}",
       "#1E268D",
        ancho_kpi_t1
    )

    kpi_t1_2 = crear_kpi_pdf(
        "PLAZOS REGLAMENTARIOS",
        f"{promedio_reglamentarios_t1:.0f}%",
       "#1E268D",
        ancho_kpi_t1
    )

    kpi_t1_3 = crear_kpi_pdf(
        "AVANCE DE DESCARGA",
        f"{resumen_t1['AVANCE DE DESCARGA']:.2f}%",
        "#22c55e",
        ancho_kpi_t1
    )

    kpi_t1_4 = crear_kpi_pdf(
        "% LECTURAS PENDIENTES",
        f"{resumen_t1['% PENDIENTES']:.2f}%",
       "#1E268D",
        ancho_kpi_t1
    )

    kpi_t1_5 = crear_kpi_pdf(
        "LECTURAS DESCARGADAS",
        f"{resumen_t1['LECTURAS DESCARGADAS']:,.0f}".replace(",", "."),
        "#22c55e",
        ancho_kpi_t1
    )

    kpi_t1_6 = crear_kpi_pdf(
        "LECTURAS PENDIENTES",
        f"{resumen_t1['LECTURAS PENDIENTES']:,.0f}".replace(",", "."),
       "#1E268D",
        ancho_kpi_t1
    )

    kpi_t1_7 = crear_kpi_pdf(
        "PROM REQ A DESCARGAR",
        f"{resumen_t1['PROMEDIO']:,.0f} / día".replace(",", "."),
       "#1E268D",
        ancho_kpi_t1
    )






    # ============================================================
    # CALCULAR ALTURA MÁXIMA DE LOS 7 KPI
    # ============================================================

    kpis_t1 = [
        kpi_t1_1,
        kpi_t1_2,
        kpi_t1_3,
        kpi_t1_4,
        kpi_t1_5,
        kpi_t1_6,
        kpi_t1_7
    ]

    alturas_t1 = []

    for kpi in kpis_t1:
        _, alto = kpi.wrap(ancho_kpi_t1, 1000)
        alturas_t1.append(alto)

    alto_max_t1 = max(alturas_t1)



    kpi_t1_1 = crear_kpi_pdf(
        "ATRASO",
        f"{resumen_t1['ATRASO']}",
       "#1E268D",
        ancho_kpi_t1,
        alto_max_t1
    )

    kpi_t1_2 = crear_kpi_pdf(
        "PLAZOS REGLAMENTARIOS",
        f"{promedio_reglamentarios_t1:.0f}%",
       "#1E268D",
        ancho_kpi_t1,
        alto_max_t1
    )

    kpi_t1_3 = crear_kpi_pdf(
        "AVANCE DE DESCARGA",
        f"{resumen_t1['AVANCE DE DESCARGA']:.2f}%",
        "#22c55e",
        ancho_kpi_t1,
        alto_max_t1
    )

    kpi_t1_4 = crear_kpi_pdf(
        "% LECTURAS PENDIENTES",
        f"{resumen_t1['% PENDIENTES']:.2f}%",
       "#1E268D",
        ancho_kpi_t1,
        alto_max_t1
    )

    kpi_t1_5 = crear_kpi_pdf(
        "LECTURAS DESCARGADAS",
        f"{resumen_t1['LECTURAS DESCARGADAS']:,.0f}".replace(",", "."),
        "#22c55e",
        ancho_kpi_t1,
        alto_max_t1
    )

    kpi_t1_6 = crear_kpi_pdf(
        "LECTURAS PENDIENTES",
        f"{resumen_t1['LECTURAS PENDIENTES']:,.0f}".replace(",", "."),
       "#1E268D",
        ancho_kpi_t1,
        alto_max_t1
    )

    kpi_t1_7 = crear_kpi_pdf(
        "PROM REQ A DESCARGAR",
        f"{resumen_t1['PROMEDIO']:,.0f} / día".replace(",", "."),
       "#1E268D",
        ancho_kpi_t1,
        alto_max_t1
    )


    # ============================================================
    # CREAR KPIS T2
    # ============================================================

    kpi_t2_1 = crear_kpi_pdf(
        "ATRASO",
        f"{resumen_t2['ATRASO']}",
       "#1E268D",
        ancho_kpi_t2
    )

    kpi_t2_2 = crear_kpi_pdf(
        "PLAZOS REGLAMENTARIOS",
        f"{promedio_reglamentarios_t2:.0f}%",
       "#1E268D",
        ancho_kpi_t2
    )

    kpi_t2_3 = crear_kpi_pdf(
         "AVANCE DE DESCARGA",
        f"{resumen_t2['AVANCE DE DESCARGA']:.2f}%",
        "#22c55e",
        ancho_kpi_t2
    )

    kpi_t2_4 = crear_kpi_pdf(
         "% LECTURAS PENDIENTES",
        f"{resumen_t2['% PENDIENTES']:.2f}%",
       "#1E268D",
        ancho_kpi_t2
    )

    kpi_t2_5 = crear_kpi_pdf(
        "LECTURAS DESCARGADAS",
        f"{resumen_t2['LECTURAS DESCARGADAS']:,.0f}".replace(",", "."),
        "#22c55e",
        ancho_kpi_t2
    )

    kpi_t2_6 = crear_kpi_pdf(
        "LECTURAS PENDIENTES",
        f"{resumen_t2['LECTURAS PENDIENTES']:,.0f}".replace(",", "."),
        "#1E268D",
        ancho_kpi_t2
    )

    kpi_t2_7 = crear_kpi_pdf(
        "PROM REQ A DESCARGAR",
        f"{resumen_t2['PROMEDIO']:,.0f} / día".replace(",", "."),
       "#1E268D",
        ancho_kpi_t2
    )



    # ============================================================
    # KPI T2
    # ============================================================

    kpis_t2 = [
        kpi_t2_1,
        kpi_t2_2,
        kpi_t2_3,
        kpi_t2_4,
        kpi_t2_5,
        kpi_t2_6,
        kpi_t2_7,
    ]

    # ------------------------------------------------------------
    # 1. Medir la altura natural de cada KPI
    # ------------------------------------------------------------

    alturas_t2 = []

    for kpi in kpis_t2:

        _, alto = kpi.wrap(
            ancho_kpi_t2,
            1000
        )

        alturas_t2.append(alto)


    # ------------------------------------------------------------
    # 2. Tomar la mayor altura
    # ------------------------------------------------------------

    alto_max_t2 = max(alturas_t2)


    # ------------------------------------------------------------
    # 3. Recrear TODOS los KPI con la misma altura
    # ------------------------------------------------------------

    kpi_t2_1 = crear_kpi_pdf(
          "ATRASO",
                f"{resumen_t2['ATRASO']}",
               "#1E268D",
        ancho_kpi_t2,
        alto_max_t1
    )

    kpi_t2_2 = crear_kpi_pdf(
        "PLAZOS REGLAMENTARIOS",
               f"{promedio_reglamentarios_t2:.0f}%",
              "#1E268D",
        ancho_kpi_t2,
        alto_max_t1
    )

    kpi_t2_3 = crear_kpi_pdf(
        "AVANCE DE DESCARGA",
              f"{resumen_t2['AVANCE DE DESCARGA']:.2f}%",
              "#22c55e",
        ancho_kpi_t2,
        alto_max_t1
    )

    kpi_t2_4 = crear_kpi_pdf(
       "% LECTURAS PENDIENTES",
              f"{resumen_t2['% PENDIENTES']:.2f}%",
             "#1E268D",
        ancho_kpi_t2,
        alto_max_t1
    )

    kpi_t2_5 = crear_kpi_pdf(
        "LECTURAS DESCARGADAS",
               f"{resumen_t2['LECTURAS DESCARGADAS']:,.0f}".replace(",", "."),
               "#22c55e",
        ancho_kpi_t2,
        alto_max_t1
    )

    kpi_t2_6 = crear_kpi_pdf(
         "LECTURAS PENDIENTES",
                f"{resumen_t2['LECTURAS PENDIENTES']:,.0f}".replace(",", "."),
                "#1E268D",
        ancho_kpi_t2,
        alto_max_t1
    )

    kpi_t2_7 = crear_kpi_pdf(
        "PROM REQ A DESCARGAR",
               f"{resumen_t2['PROMEDIO']:,.0f} / día".replace(",", "."),
              "#1E268D",
        ancho_kpi_t2,
        alto_max_t1
    )


    # ------------------------------------------------------------
    # 4. Tabla de 7 KPI
    # ------------------------------------------------------------

    tabla_t2 = Table(
        [
            [
                kpi_t2_1,
                kpi_t2_2,
                kpi_t2_3,
                kpi_t2_4
            ],
            [
                kpi_t2_5,
                kpi_t2_6,
                kpi_t2_7,
                ""
            ]
        ],
        colWidths=[
            ancho_kpi_t2,
            ancho_kpi_t2,
            ancho_kpi_t2,
            ancho_kpi_t2
        ],
        rowHeights=[
            alto_max_t2,
            alto_max_t2
        ]
    )

    tabla_t2.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))


    # ============================================================
    # TABLA T1
    #
    # 4 KPI arriba
    # 3 KPI abajo
    #
    # La cuarta celda de la segunda fila queda vacía para
    # conservar la estructura de 4 columnas.
    # ============================================================

    tabla_t1 = Table(
        [
            [
                kpi_t1_1,
                kpi_t1_2,
                kpi_t1_3,
                kpi_t1_4
            ],
            [
                kpi_t1_5,
                kpi_t1_6,
                kpi_t1_7,
                ""
            ]
        ],
        colWidths=[
            ancho_kpi_t1,
            ancho_kpi_t1,
            ancho_kpi_t1,
            ancho_kpi_t1
        ],
          rowHeights=[
        alto_max_t1,
        alto_max_t1
    ]
    )


    # ============================================================
    # ESTILO TABLA T1
    # ============================================================

    # tabla_t1.setStyle(TableStyle([

    #     (
    #         "VALIGN",
    #         (0, 0),
    #         (-1, -1),
    #         "TOP"
    #     ),

    #     (
    #         "ALIGN",
    #         (0, 0),
    #         (-1, -1),
    #         "CENTER"
    #     ),

    #     (
    #         "LEFTPADDING",
    #         (0, 0),
    #         (-1, -1),
    #         2
    #     ),

    #     (
    #         "RIGHTPADDING",
    #         (0, 0),
    #         (-1, -1),
    #         2
    #     ),

    #     (
    #         "TOPPADDING",
    #         (0, 0),
    #         (-1, -1),
    #         2
    #     ),

    #     (
    #         "BOTTOMPADDING",
    #         (0, 0),
    #         (-1, -1),
    #         2
    #     ),
    # ]))
    tabla_t1.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))


    # ============================================================
    # TABLA T2
    # ============================================================

    tabla_t2 = Table(
        [
            [
                kpi_t2_1,
                kpi_t2_2,
                kpi_t2_3,
                kpi_t2_4
            ],
              [
                kpi_t2_5,
                kpi_t2_6,
                kpi_t2_7,
                ""
            ]
        ],
        colWidths=[
            ancho_kpi_t2,
            ancho_kpi_t2,
            ancho_kpi_t2,
            ancho_kpi_t2
        ]
    )


    # ============================================================
    # ESTILO TABLA T2
    # ============================================================

    tabla_t2.setStyle(TableStyle([

        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "TOP"
        ),

        (
            "ALIGN",
            (0, 0),
            (-1, -1),
            "CENTER"
        ),

        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            2
        ),

        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            2
        ),

        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            2
        ),

        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            2
        ),
    ]))


    # ============================================================
    # TÍTULO T1
    # ============================================================

    titulo_t1 = Paragraph(
        "<para align='center'><b><u>LECTURAS T1</u></b></para>",
        styles["Heading3"]
    )


    # ============================================================
    # TÍTULO T2
    # ============================================================

    titulo_t2 = Paragraph(
        "<para align='center'><b><u>LECTURAS T2</u></b></para>",
        styles["Heading3"]
    )


    # ============================================================
    # DASHBOARD PRINCIPAL
    #
    # 2 COLUMNAS:
    #
    # ┌──────────────────────┬─────┬──────────────────────┐
    # │      LECTURAS T1     │     │      LECTURAS T2     │
    # │                      │     │                      │
    # │ KPI KPI KPI KPI      │     │ KPI KPI KPI KPI      │
    # │ KPI KPI KPI          │     │                      │
    # └──────────────────────┴─────┴──────────────────────┘
    # ============================================================

    dashboard = Table(
        [
            [
                titulo_t1,
                "",
                titulo_t2
            ],
            [
                tabla_t1,
                "",
                tabla_t2
            ]
        ],
        colWidths=[
            ancho_t1,
            ancho_separacion,
            ancho_t2
        ],
        hAlign="CENTER"
    )


    # ============================================================
    # ESTILO DEL DASHBOARD
    # ============================================================

    dashboard.setStyle(TableStyle([

        # --------------------------------------------------------
        # ALINEACIÓN
        # --------------------------------------------------------

        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "TOP"
        ),

        (
            "ALIGN",
            (0, 0),
            (-1, -1),
            "CENTER"
        ),

        # --------------------------------------------------------
        # PADDING
        # --------------------------------------------------------

        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            2
        ),

        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            2
        ),

        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            3
        ),

        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            3
        ),
    ]))


    # ============================================================
    # AGREGAR DASHBOARD AL PDF
    # ============================================================

    elements.append(dashboard)
    # elements.append(Spacer(1, 20))
    elements.append(PageBreak())















    
#     realvsprog = realvsprog.copy()

#     # realvsprog["prog"] = realvsprog["prog"].map("{:,.0f}".format)
#     # realvsprog["real"] = realvsprog["real"].map("{:,.0f}".format)
#     # realvsprog["prog_ac"] = realvsprog["prog_ac"].map("{:,.0f}".format)
#     # realvsprog["prog_real"] = realvsprog["prog_real"].map("{:,.0f}".format)
#     # realvsprog["dif"] = realvsprog["dif"].map("{:,.0f}".format)
#     # realvsprog["avg_prog"] = realvsprog["avg_prog"].map("{:,.0f}".format)
#     # realvsprog["avg_real"] = realvsprog["avg_real"].map("{:,.0f}".format)
#     # format_number(realvsprog["prog"])
#     # format_number(realvsprog["real"])
#     # format_number(realvsprog["prog_ac"])
#     # format_number(realvsprog["prog_real"])
#     # format_number(realvsprog["dif"])
#     # format_number(realvsprog["avg_prog"])
#     # format_number(realvsprog["avg_real"])
#     realvsprog["prog"] = pd.to_numeric(
#     realvsprog["prog"],
#     errors="coerce"
# )
#     realvsprog["prog"] = realvsprog["prog"].map(
#     lambda x: f"{x:,.0f}".replace(",", ".")
# )

#     # realvsprog["Avance"] = realvsprog["Avance"].map("{:.2f}%".format)
#     # realvsprog["f_lteor"] = pd.to_datetime(realvsprog["f_lteor"], errors="coerce").dt.date
#     # realvsprog["f_lteor"] = pd.to_datetime(realvsprog["f_lteor"], errors="coerce").dt.strftime("%d/%m/%Y")
#     realvsprog["f_lteor"] = pd.to_datetime(
#     realvsprog["f_lteor"],
#     dayfirst=True,
#     errors="coerce"
# ).dt.strftime("%d/%m/%Y")
    
#     n_cols = len(realvsprog.columns)

#     table_data = [realvsprog.columns.tolist()] + realvsprog.values.tolist()
#     tabla_realvsprog = Table(
#     table_data,
#     colWidths=[doc.width / n_cols] * n_cols,
#     repeatRows=1
# )
    
#     tabla_realvsprog.setStyle(TableStyle([

#     ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
#     ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

#     ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

#     ("FONTSIZE", (0, 0), (-1, -1), 9),

#     ("ALIGN", (0, 0), (-1, -1), "CENTER"),

#     ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

#     ("ROWBACKGROUNDS",
#         (0, 1),
#         (-1, -1),
#         [colors.white, colors.HexColor("#f5f5f5")]
#     ),

#     ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

# ]))
    
    # elements.append(tabla_realvsprog)
    # elements.append(Spacer(1, 20))

    n_cols_df_t1 = len(df_t1.columns)

    df_t1["f_lteor"] = pd.to_datetime(
        df_t1["f_lteor"],
        dayfirst=True,
        errors="coerce"
    ).dt.strftime("%d/%m/%Y")

    table_data_df_t1 = [df_t1.columns.tolist()] + df_t1.values.tolist()
    tabla_df_t1 = Table(
    table_data_df_t1,
    colWidths=[doc.width / n_cols_df_t1] * n_cols_df_t1,
    repeatRows=1
)
    
    tabla_df_t1.setStyle(TableStyle([

    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

    ("FONTSIZE", (0, 0), (-1, -1), 9),

    ("ALIGN", (0, 0), (-1, -1), "CENTER"),

    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

    ("ROWBACKGROUNDS",
        (0, 1),
        (-1, -1),
        [colors.white, colors.HexColor("#f5f5f5")]
    ),

    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

]))
    
 

    elements.append(tabla_df_t1)
    # elements.append(Spacer(1, 20))
    elements.append(PageBreak())




################################################################



















# # ============================
# # AVG_PROY
# # ============================

# # Aseguramos que real sea numérico.
# # El 0 es un valor válido y NO se considera vacío.
#     realvsprog["real"] = pd.to_numeric(
#         realvsprog["real"],
#         errors="coerce"
#     )

#     realvsprog["prog_real"] = pd.to_numeric(
#         realvsprog["prog_real"],
#         errors="coerce"
#     )

#     # Equivale a $E$21 de Excel:
#     # último valor de prog_real
#     prog_real_final = realvsprog["prog_real"].iloc[-1]

#     avg_proy = []

#     # Cantidad de blancos de TODO el rango de real
#     cantidad_blancos = realvsprog["real"].isna().sum()

#     for i in range(len(realvsprog)):

#         real_actual = realvsprog["real"].iloc[i]

#         # Si REAL está vacío
#         if pd.isna(real_actual):

#             suma_real_acumulada = (
#                 realvsprog["real"]
#                 .iloc[:i + 1]
#                 .sum(skipna=True)
#             )

#             if cantidad_blancos > 0:
#                 promedio_proyectado = (
#                     prog_real_final - suma_real_acumulada
#                 ) / cantidad_blancos
#             else:
#                 promedio_proyectado = None

#         # Si REAL tiene un valor, incluso si es 0
#         else:

#             promedio_proyectado = (
#                 realvsprog["real"]
#                 .iloc[:i + 1]
#                 .mean()
#             )

#         avg_proy.append(promedio_proyectado)


#     realvsprog["avg_proy"] = avg_proy


#     # ============================
#     # DIF_DIAS_PROY
#     # ============================

#     realvsprog["dif_dias_proy"] = realvsprog.apply(
#         lambda row:
#             row["dif"] / row["avg_proy"]
#             if (
#                 pd.notna(row["dif"])
#                 and pd.notna(row["avg_proy"])
#                 and row["avg_proy"] != 0
#             )
#             else None,
#         axis=1
#     )


#     # ============================
#     # FORMATO PARA PDF
#     # ============================

#     # Columnas enteras
#     for col in ["real", "prog", "prog_real", "dif", "avg_proy"]:

#         realvsprog[col] = realvsprog[col].map(
#             lambda x:
#                 f"{x:,.0f}".replace(",", ".")
#                 if pd.notna(x)
#                 else ""
#         )


#     # DIF_DIAS_PROY → 2 decimales
#     realvsprog["dif_dias_proy"] = realvsprog["dif_dias_proy"].map(
#         lambda x:
#             f"{x:,.2f}"
#             .replace(",", "X")
#             .replace(".", ",")
#             .replace("X", ".")
#             if pd.notna(x)
#             else ""
#     )


#     # Fecha
#     realvsprog["f_lteor"] = pd.to_datetime(
#         realvsprog["f_lteor"],
#         dayfirst=True,
#         errors="coerce"
#     ).dt.strftime("%d/%m/%Y")


#     # ============================
#     # TABLA PDF
#     # ============================

#     n_cols = len(realvsprog.columns)

#     table_data = (
#         [realvsprog.columns.tolist()]
#         + realvsprog.values.tolist()
#     )

#     tabla_realvsprog = Table(
#         table_data,
#         colWidths=[doc.width / n_cols] * n_cols,
#         repeatRows=1
#     )

#     tabla_realvsprog.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
#         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
#         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#         ("FONTSIZE", (0, 0), (-1, -1), 9),
#         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#         ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
#         ("ROWBACKGROUNDS",
#             (0, 1),
#             (-1, -1),
#             [colors.white, colors.HexColor("#f5f5f5")]
#         ),
#         ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
#     ]))

#     elements.append(tabla_realvsprog)
#     elements.append(Spacer(1, 20))


    # ============================================================
# REAL VS PROG
# ============================================================

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


    # # Equivalente a:
    # # CONTAR.BLANCO($D$2:$D$21)
    # #
    # # Se cuentan únicamente los valores realmente vacíos.
    # cantidad_blancos = realvsprog["real"].isna().sum()


    # avg_proy = []


    # for i in range(len(realvsprog)):

    #     # Valor REAL de la fila actual
    #     real_actual = realvsprog["real"].iloc[i]


    #     # --------------------------------------------------------
    #     # Si REAL está vacío
    #     # --------------------------------------------------------

    #     if pd.isna(real_actual):

    #         # Equivalente a:
    #         # SUMA($D$2:D[fila_actual])
    #         suma_real_acumulada = (
    #             realvsprog["real"]
    #             .iloc[:i + 1]
    #             .sum(skipna=True)
    #         )


    #         # Equivalente a:
    #         #
    #         # ($E$21 - SUMA($D$2:Dfila))
    #         # /
    #         # CONTAR.BLANCO($D$2:$D$21)
    #         #
    #         if cantidad_blancos > 0:

    #             promedio_proyectado = (
    #                 prog_real_final - suma_real_acumulada
    #             ) / cantidad_blancos

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


    # # ============================================================
    # # FORMATO DE COLUMNAS PARA EL PDF
    # # ============================================================

    # # ------------------------------------------------------------
    # # Columnas sin decimales
    # # ------------------------------------------------------------

    # for col in [
    #     "real",
    #     "prog",
    #     "prog_real",
    #     "dif",
    #     "avg_proy"
    # ]:

    #     realvsprog[col] = realvsprog[col].map(
    #         lambda x:
    #             f"{x:,.0f}".replace(",", ".")
    #             if pd.notna(x)
    #             else ""
    #     )


    # # ------------------------------------------------------------
    # # DIF_DIAS_PROY
    # #
    # # Esta es la ÚNICA columna que mostramos con 2 decimales.
    # #
    # # Ejemplo:
    # # 2.35 → 2,35
    # # 1234.56 → 1.234,56
    # # ------------------------------------------------------------

    # realvsprog["dif_dias_proy"] = realvsprog[
    #     "dif_dias_proy"
    # ].map(
    #     lambda x:
    #         f"{x:,.2f}"
    #         .replace(",", "X")
    #         .replace(".", ",")
    #         .replace("X", ".")
    #         if pd.notna(x)
    #         else ""
    # )


    # # ============================================================
    # # FORMATO DE FECHA
    # # ============================================================

    # realvsprog["f_lteor"] = pd.to_datetime(
    #     realvsprog["f_lteor"],
    #     dayfirst=True,
    #     errors="coerce"
    # ).dt.strftime("%d/%m/%Y")


    # # ============================================================
    # # TABLA REAL VS PROG
    # # ============================================================

    # n_cols = len(realvsprog.columns)


    # table_data = [
    #     realvsprog.columns.tolist()
    # ] + realvsprog.values.tolist()


    # tabla_realvsprog = Table(
    #     table_data,
    #     colWidths=[doc.width / n_cols] * n_cols,
    #     repeatRows=1
    # )


    # # ============================================================
    # # ESTILO TABLA
    # # ============================================================

    # tabla_realvsprog.setStyle(
    #     TableStyle([
            
    #         # Encabezado
    #         (
    #             "BACKGROUND",
    #             (0, 0),
    #             (-1, 0),
    #             colors.HexColor("#1f4e78")
    #         ),

    #         (
    #             "TEXTCOLOR",
    #             (0, 0),
    #             (-1, 0),
    #             colors.white
    #         ),

    #         (
    #             "FONTNAME",
    #             (0, 0),
    #             (-1, 0),
    #             "Helvetica-Bold"
    #         ),

    #         # Texto
    #         (
    #             "FONTSIZE",
    #             (0, 0),
    #             (-1, -1),
    #             9
    #         ),

    #         # Alineación
    #         (
    #             "ALIGN",
    #             (0, 0),
    #             (-1, -1),
    #             "CENTER"
    #         ),

    #         (
    #             "VALIGN",
    #             (0, 0),
    #             (-1, -1),
    #             "MIDDLE"
    #         ),

    #         # Bordes
    #         (
    #             "GRID",
    #             (0, 0),
    #             (-1, -1),
    #             0.5,
    #             colors.grey
    #         ),

    #         # Filas alternadas
    #         (
    #             "ROWBACKGROUNDS",
    #             (0, 1),
    #             (-1, -1),
    #             [
    #                 colors.white,
    #                 colors.HexColor("#f5f5f5")
    #             ]
    #         ),

    #         # Espaciado encabezado
    #         (
    #             "TOPPADDING",
    #             (0, 0),
    #             (-1, 0),
    #             6
    #         ),

    #         (
    #             "BOTTOMPADDING",
    #             (0, 0),
    #             (-1, 0),
    #             8
    #         ),

    #         # Espaciado filas
    #         (
    #             "TOPPADDING",
    #             (0, 1),
    #             (-1, -1),
    #             5
    #         ),

    #         (
    #             "BOTTOMPADDING",
    #             (0, 1),
    #             (-1, -1),
    #             5
    #         ),
    #     ])
    # )


    # ============================================================
    # AGREGAR AL PDF
    # ============================================================

    # elements.append(tabla_realvsprog)

    # elements.append(
    #     Spacer(1, 20)
    # )





















###########################################################




    subt2 = Paragraph(
        """
        <u><b>EVOLUCIÓN DIARIA T1</b></u>
        """,
        styles["Heading3"]
    )

    elements.append(subt2)
    elements.append(Spacer(1, 10))
    # elements.append(PageBreak())





    
#     temp_img = tempfile.NamedTemporaryFile(
#     suffix=".png",
#     delete=False
# )

#     generar_graf_ev_lect_pdf(
#         df_filtrado_t1,
#         col_leidos="total_leidos_actual",
#         path_archivo=temp_img.name,
#         titulo="Evolución diaria de lecturas s/fecha actual",
#         titulo_col_leidos="Lecturas realizadas",
#         mostrar_val=True
#     )

#     # elements.append(
#     #     Paragraph(
#     #         "<u><b>Evolución diaria de lecturas</b></u>",
#     #         styles["Heading3"]
#     #     )
#     # )

#     elements.append(Spacer(1, 10))

#     elements.append(
#         Image(
#             temp_img.name,
#             width=17 * cm,
#             height=8 * cm
#         )
#     )


    temp_img_t1 = tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False
    )
    temp_img_t1.close()

    generar_graf_ev_lect_pdf(
        # df_filtrado_t1,
        df_grafico_t1,
        col_leidos="total_leidos_actual",
        path_archivo=temp_img_t1.name,
        titulo="Evolución diaria de lecturas s/fecha actual",
        titulo_col_leidos="Lecturas realizadas",
        mostrar_val=True
    )

    elements.append(
        Image(
            temp_img_t1.name,
            # width=17 * cm,
            # height=8 * cm
             width=25 * cm,
            height=11 * cm
        )
    )
    # elements.append(Spacer(1, 20))
    elements.append(PageBreak())















    subt3 = Paragraph(
        """
        <u><b>EVOLUCIÓN DIARIA T2</b></u>
        """,
        styles["Heading3"]
    )

    elements.append(subt3)
    elements.append(Spacer(1, 10))




    
#     temp_img = tempfile.NamedTemporaryFile(
#     suffix=".png",
#     delete=False
# )

#     generar_graf_ev_lect_pdf(
#         df_filtrado_t2,
#         col_leidos="total_leidos_actual",
#         path_archivo=temp_img.name,
#         titulo="Evolución diaria de lecturas s/fecha actual",
#         titulo_col_leidos="Lecturas realizadas",
#         mostrar_val=True
#     )

#     # elements.append(
#     #     Paragraph(
#     #         "<u><b>Evolución diaria de lecturas</b></u>",
#     #         styles["Heading3"]
#     #     )
#     # )

#     elements.append(Spacer(1, 10))

#     elements.append(
#         Image(
#             temp_img.name,
#             width=17 * cm,
#             height=8 * cm
#         )
#     )
    temp_img_t2 = tempfile.NamedTemporaryFile(
    suffix=".png",
    delete=False
)
    temp_img_t2.close()

    generar_graf_ev_lect_pdf(
        df_grafico_t2,
        col_leidos="total_leidos_actual",
        path_archivo=temp_img_t2.name,
        titulo="Evolución diaria de lecturas s/fecha actual",
        titulo_col_leidos="Lecturas realizadas",
        mostrar_val=True
    )

    elements.append(
        Image(
            temp_img_t2.name,
            # width=17 * cm,
            # height=8 * cm
              width=25 * cm,
            height=11 * cm
        )
    )

    # elements.append(Spacer(1, 20))
    elements.append(PageBreak())














    subt4 = Paragraph(
        """
        <u><b>ANOMALÍAS T2</b></u>
        """,
        styles["Heading3"]
    )

    elements.append(subt4)
    elements.append(Spacer(1, 10))



    cantidad_anomalias = resumen_anomalias["Casos"].sum()

    primer_dia_mes = pd.Timestamp.today().replace(day=1)
    hoy = pd.Timestamp.today()

    subt4text = Paragraph(
        f"""
        Actualmente se registran {cantidad_anomalias:,.0f} anomalías T2 pendientes de resolución,
        acumuladas desde el {primer_dia_mes.strftime("%d/%m/%Y")} hasta hoy ({hoy.strftime("%d/%m/%Y")}),
        distribuidas de la siguiente manera:
        """,
        styles["BodyText"]
    )



    # subt4text = Paragraph(
    #     """
    #     Actualmente se registran 130 anomalías T2 pendientes de resolución, acumuladas desde el 01/05/2026 hasta hoy, distribuidas de la siguiente manera:
    #     """,
    #     styles["BodyText"]
    # )

    elements.append(subt4text)
    elements.append(Spacer(1, 20))






    # from reportlab.platypus import Table, TableStyle
    # from reportlab.lib import colors
    # from reportlab.lib.units import cm
    # from reportlab.platypus import Paragraph
    # from reportlab.lib.styles import getSampleStyleSheet

    styles = getSampleStyleSheet()

    # data = [
    #     ["11", Paragraph("<b>Cooperativa Eléctrica</b>", styles["BodyText"]),
    #     Paragraph("<b><i>No debemos resolverlas</i></b>", styles["BodyText"])],
    # ]

    data = [
         ["11", Paragraph("<b>Cooperativa Eléctrica</b>", styles["BodyText"]),
        Paragraph("<b><i>No debemos resolverlas</i></b>", styles["BodyText"])],
        ["11", "Cooperativa Eléctrica", "No debemos resolverlas"],
        ["6", "EDESTE", "No debemos resolverlas"],
        ["39", "Telemedición ESG", "Reclamado a T2 NORTE"],
        ["19", "OSL", "A la espera de resolución de orden"],
        ["2", "Contraste", "A la espera de resolución de orden"],
        ["35", "Cambio de medidor no\nactualizado en OPEN", "Reclamado a T2 NORTE"],
         ["1", Paragraph("<b>Sistemas</b>", styles["BodyText"]),
        Paragraph("<b><i>A la espera de resolución de error en OPEN</i></b>", styles["BodyText"])],
        # ["1", "Sistemas", "A la espera de resolución de error en OPEN"],
        # ["1", "Débito automático", "A la espera de resolución de Créditos y Cobranzas"],
        ["1", Paragraph("Débito automático", styles["BodyText"]),
        Paragraph("<i>A la espera de resolución de Créditos y Cobranzas</i>", styles["BodyText"])],
        ["16", "Pendientes de análisis", "-"],
    ]

    tabla_anomalias = Table(
        data,
        colWidths=[1.5*cm, 6*cm, 7*cm]
    )

    tabla_anomalias.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.8, colors.grey),

        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),

        ("FONTNAME", (1, 0), (1, 4), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, 1), "Helvetica-Bold"),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ALIGN", (1, 0), (-1, -1), "LEFT"),

        ("FONTSIZE", (0, 0), (-1, -1), 11),

        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    # elements.append(tabla_anomalias)
    # elements.append(Spacer(1, 10))


    ######DINAMICOOOOOOOOOOOO
    # data = df_anomalias.values.tolist()

    # tabla_anomalias = Table(
    #     data,
    #     colWidths=[1.5*cm, 6*cm, 7*cm]
    # )


        # ==============================
    # RESUMEN DE ANOMALÍAS
    # ==============================

    resumen_anomalias_pdf = resumen_anomalias.copy()

    for col in resumen_anomalias_pdf.columns:
        if pd.api.types.is_numeric_dtype(resumen_anomalias_pdf[col]):
            resumen_anomalias_pdf[col] = pd.to_numeric(
                resumen_anomalias_pdf[col],
                errors="coerce"
            ).map(
                lambda x: f"{x:,.0f}".replace(",", ".")
                if pd.notna(x) else ""
            )

    n_cols = len(resumen_anomalias_pdf.columns)

    # table_data = (
    #     [resumen_anomalias_pdf.columns.tolist()]
    #     + resumen_anomalias_pdf.values.tolist()
    # )

    # tabla_resumen_anomalias = Table(
    #     table_data,
    #     colWidths=[doc.width / n_cols] * n_cols,
    #     repeatRows=1
    # )

    # tabla_resumen_anomalias.setStyle(TableStyle([
    #     ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
    #     ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    #     ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    #     ("FONTSIZE", (0, 0), (-1, -1), 9),
    #     ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    #     ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    #     ("ROWBACKGROUNDS",
    #         (0, 1),
    #         (-1, -1),
    #         [colors.white, colors.HexColor("#f5f5f5")]
    #     ),
    #     ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    # ]))

    # elements.append(tabla_resumen_anomalias)
    # elements.append(Spacer(1, 20))
    # from reportlab.platypus import Paragraph
# from reportlab.lib.styles import ParagraphStyle

    # Estilo para las celdas
    estilo_celda = ParagraphStyle(
        "celda",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        alignment=1,  # 0 izquierda, 1 centro
    )

    estilo_encabezado = ParagraphStyle(
        "encabezado",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1,
    )

    # Convertir todas las celdas en Paragraph
    table_data = []

    # Encabezados
    table_data.append([
        Paragraph(str(col), estilo_encabezado)
        for col in resumen_anomalias_pdf.columns
    ])

    # Datos
    for _, fila in resumen_anomalias_pdf.iterrows():
        table_data.append([
            Paragraph(str(valor), estilo_celda)
            for valor in fila
        ])

    # Anchos de columnas
    col_widths = [
        doc.width * 0.30,
        doc.width * 0.30,
        doc.width * 0.40
    ]

    tabla_resumen_anomalias = Table(
        table_data,
        colWidths=col_widths,
        repeatRows=1
    )

    tabla_resumen_anomalias.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS",
        (0, 1),
        (-1, -1),
        [colors.white, colors.HexColor("#f5f5f5")]
    ),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
]))

    elements.append(tabla_resumen_anomalias)
    elements.append(Spacer(1, 20))



    # ==========================================
    # TITULO CENTRADO
    # ==========================================

#     titulo2 = Paragraph(
#         """
#         <para align='center'>
#             <u><b>EVOLUCIÓN DIARIA T1</b></u>
#         </para>
#         """,
#         styles["Heading2"]
#     )

#     elements.append(titulo2)
#     elements.append(Spacer(1, 15))






















#     # ==========================================
#     # SUBTITULO
#     # ==========================================

#     subtitulo = Paragraph(
#         """
#         <u><b>Anomalías T2</b></u>
#         """,
#         styles["Heading3"]
#     )

#     elements.append(subtitulo)
#     elements.append(Spacer(1, 10))

#     # ==========================================
#     # TEXTO
#     # ==========================================

#     texto = Paragraph(
#         """
#         Actualmente se registran 130 anomalías T2 pendientes de resolución,
#         acumuladas desde el 01/05/2025 hasta hoy.
#         """,
#         styles["BodyText"]
#     )

#     elements.append(texto)
#     elements.append(Spacer(1, 20))

#     # ==========================================
#     # TABLA KPI
#     # ==========================================

#     kpi_data = [
#         ["Indicador", "Valor"],
#         ["Avance", "30%"],
#         ["Pendientes", "70%"],
#         ["Lecturas", "165.970"]
#     ]

#     kpi_table = Table(
#         kpi_data,
#         colWidths=[8 * cm, 5 * cm]
#     )

#     kpi_table.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9d9d9")),
#         ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
#         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#         ("GRID", (0, 0), (-1, -1), 1, colors.black),
#     ]))

#     elements.append(kpi_table)
#     elements.append(Spacer(1, 25))

#     # ==========================================
#     # GRAFICO
#     # ==========================================

#     temp_img = tempfile.NamedTemporaryFile(
#         suffix=".png",
#         delete=False
#     )

#     generar_grafico_png(temp_img.name)

#     grafico = Image(
#         temp_img.name,
#         width=17 * cm,
#         height=7 * cm
#     )

#     elements.append(grafico)
#     elements.append(Spacer(1, 20))

#     # ==========================================
#     # TABLA DETALLE
#     # ==========================================

#     table_data = [df.columns.tolist()] + df.values.tolist()

#     detail_table = Table(
#         table_data,
#         repeatRows=1
#     )

#     detail_table.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
#         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
#         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#         ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
#         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#         ("ROWBACKGROUNDS",
#          (0, 1),
#          (-1, -1),
#          [colors.white, colors.HexColor("#f2f2f2")]),
#     ]))

#     elements.append(detail_table)

#     elements.append(Spacer(1, 20))

#     # ==========================================
#     # TABLA RESUMEN
#     # ==========================================

#     data = [
#         ["Estado", "Prom", "Avance", "% Lecturas"],
#         ["NORMAL", "97%", "30%", "70%"]
#     ]

#     table = Table(
#         data,
#         colWidths=[100, 80, 80, 80]
#     )

#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#     ]))

#     elements.append(table)







#     ## REAL VS PROGRAMADO
#     elements.append(
#     Paragraph(
#         "<u><b>Real vs Programado</b></u>",
#         styles["Heading3"]
#         )
#     )

#     elements.append(Spacer(1, 10))


#     realvsprog = realvsprog.copy()

#     # realvsprog["prog"] = realvsprog["prog"].map("{:,.0f}".format)
#     # realvsprog["real"] = realvsprog["real"].map("{:,.0f}".format)
#     # realvsprog["prog_ac"] = realvsprog["prog_ac"].map("{:,.0f}".format)
#     # realvsprog["prog_real"] = realvsprog["prog_real"].map("{:,.0f}".format)
#     # realvsprog["dif"] = realvsprog["dif"].map("{:,.0f}".format)
#     # realvsprog["avg_prog"] = realvsprog["avg_prog"].map("{:,.0f}".format)
#     # realvsprog["avg_real"] = realvsprog["avg_real"].map("{:,.0f}".format)
#     # format_number(realvsprog["prog"])
#     # format_number(realvsprog["real"])
#     # format_number(realvsprog["prog_ac"])
#     # format_number(realvsprog["prog_real"])
#     # format_number(realvsprog["dif"])
#     # format_number(realvsprog["avg_prog"])
#     # format_number(realvsprog["avg_real"])
#     realvsprog["prog"] = pd.to_numeric(
#     realvsprog["prog"],
#     errors="coerce"
# )
#     realvsprog["prog"] = realvsprog["prog"].map(
#     lambda x: f"{x:,.0f}".replace(",", ".")
# )

#     # realvsprog["Avance"] = realvsprog["Avance"].map("{:.2f}%".format)



#     table_data = [realvsprog.columns.tolist()] + realvsprog.values.tolist()
#     tabla_realvsprog = Table(
#     table_data,
#     repeatRows=1
# )
    
#     tabla_realvsprog.setStyle(TableStyle([

#     ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e78")),
#     ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

#     ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

#     ("FONTSIZE", (0, 0), (-1, -1), 9),

#     ("ALIGN", (0, 0), (-1, -1), "CENTER"),

#     ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

#     ("ROWBACKGROUNDS",
#         (0, 1),
#         (-1, -1),
#         [colors.white, colors.HexColor("#f5f5f5")]
#     ),

#     ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

# ]))
    
#     elements.append(tabla_realvsprog)
#     elements.append(Spacer(1, 20))








    # ==========================================
    # GENERAR PDF
    # ==========================================

    doc.build(elements,   onFirstPage=header_footer,
    onLaterPages=header_footer)

    buffer.seek(0)

    return buffer








import matplotlib.pyplot as plt
import pandas as pd


def generar_graf_ev_lect_pdf(
    df,
    col_leidos,
    path_archivo,
    titulo="Evolución diaria de lecturas",
    titulo_col_leidos="Lecturas realizadas",
    mostrar_val=False
):

    # ============================================================
    # AGRUPAR POR FECHA COMPLETA
    # ============================================================

    df_evol = df.groupby(
        df["f_lteor"].dt.date
    ).agg({
        "total_programados": "sum",
        col_leidos: "sum"
    }).reset_index()

    df_evol = df_evol.rename(columns={
        "f_lteor": "fecha"
    })

    # ============================================================
    # ASEGURAR FECHA COMPLETA
    # ============================================================

    df_evol["fecha"] = pd.to_datetime(df_evol["fecha"])

    # Día que se va a mostrar en el eje X
    df_evol["dia"] = df_evol["fecha"].dt.strftime("%d")

    # ============================================================
    # DATOS PARA EL GRÁFICO
    # ============================================================

    df_graf = df_evol.rename(columns={
        "total_programados": "Lecturas programadas",
        col_leidos: titulo_col_leidos
    })

    # ============================================================
    # GRÁFICO
    # ============================================================

    plt.figure(figsize=(12, 5))

    plt.plot(
        df_graf["fecha"],
        df_graf["Lecturas programadas"],
        marker="o",
        linewidth=2,
        color="#ff0a0a",
        label="Lecturas programadas"
    )

    plt.plot(
        df_graf["fecha"],
        df_graf[titulo_col_leidos],
        marker="o",
        linewidth=2,
        color="#1322ff",
        label=titulo_col_leidos
    )

    # ============================================================
    # MOSTRAR VALORES
    # ============================================================

    if mostrar_val:

        for x, y in zip(
            df_graf["fecha"],
            df_graf["Lecturas programadas"]
        ):
            plt.text(
                x,
                y,
                f"{y:,.0f}".replace(",", "."),
                fontsize=8,
                ha="center"
            )

        for x, y in zip(
            df_graf["fecha"],
            df_graf[titulo_col_leidos]
        ):
            plt.text(
                x,
                y,
                f"{y:,.0f}".replace(",", "."),
                fontsize=8,
                ha="center"
            )

    # ============================================================
    # EJE X
    # ============================================================

    plt.xticks(
        df_graf["fecha"],
        df_graf["dia"]
    )

    plt.title(titulo)
    plt.xlabel("Día de lectura")
    plt.ylabel("Cantidad de lecturas")

    plt.legend()

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        path_archivo,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def generar_graf_ev_lect_pdf2(
    df,
    col_leidos,
    path_archivo,
    titulo="Evolución diaria de lecturas",
    titulo_col_leidos="Lecturas realizadas",
    mostrar_val=False
):

    df_evol = df.groupby(df["f_lteor"].dt.date).agg({
        "total_programados": "sum",
        col_leidos: "sum"
    }).reset_index()

    df_evol = df_evol.rename(columns={"f_lteor": "fecha"})

    df_graf = df_evol.rename(columns={
        "total_programados": "Lecturas programadas",
        col_leidos: titulo_col_leidos
    })

    df_graf["fecha"] = pd.to_datetime(
        df_graf["fecha"]
    ).dt.strftime("%d")

    plt.figure(figsize=(12, 5))

    plt.plot(
        df_graf["fecha"],
        df_graf["Lecturas programadas"],
        marker="o",
        linewidth=2,
        color="#ff0a0a",
        label="Lecturas programadas"
    )

    plt.plot(
        df_graf["fecha"],
        df_graf[titulo_col_leidos],
        marker="o",
        linewidth=2,
        color="#1322ff",
        label=titulo_col_leidos
    )

    if mostrar_val:

        for x, y in zip(
            df_graf["fecha"],
            df_graf["Lecturas programadas"]
        ):
            plt.text(
                x,
                y,
                f"{y:,.0f}".replace(",", "."),
                fontsize=8,
                ha="center"
            )

        for x, y in zip(
            df_graf["fecha"],
            df_graf[titulo_col_leidos]
        ):
            plt.text(
                x,
                y,
                f"{y:,.0f}".replace(",", "."),
                fontsize=8,
                ha="center"
            )

    plt.title(titulo)
    plt.xlabel("Día de lectura")
    plt.ylabel("Cantidad de lecturas")

    plt.legend()

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        path_archivo,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()




def format_number(column):
    column = pd.to_numeric(
    column,
    errors="coerce"
)
    column = column.map(
    lambda x: f"{x:,.0f}".replace(",", ".")
)
    


def header_footer(canvas, doc):

    canvas.saveState()

    width, height = doc.pagesize

    # =========================
    # HEADER
    # =========================

    canvas.setFont("Helvetica-Bold", 11)
    canvas.setFillColor(colors.HexColor("#1f4e78"))

    canvas.drawString(
        2 * cm,
        height - 1.2 * cm,
        "REPORTE DE CONTROL"
    )

    # =========================
    # LOGO DERECHA
    # =========================

    from pathlib import Path
    from PIL import Image

    BASE_DIR = Path(__file__).resolve().parents[1]
    logo_path = BASE_DIR / "img" / "edemsa_logo.png"

    # Tamaño máximo del logo
    max_width = 3 * cm
    max_height = 1.5 * cm

    # Obtener proporción original
    with Image.open(logo_path) as img:
        img_width, img_height = img.size

    ratio = img_width / img_height

    # Ajustar manteniendo proporción, sin deformar
    if max_width / max_height < ratio:
        logo_width = max_width
        logo_height = max_width / ratio
    else:
        logo_height = max_height
        logo_width = max_height * ratio

    # Posición del logo
    # Queda alineado a la derecha y completamente
    # por encima de la línea separadora.
    logo_x = width - 2 * cm - logo_width
    logo_y = height - 1.65 * cm

    canvas.drawImage(
        str(logo_path),
        logo_x,
        logo_y,
        width=logo_width,
        height=logo_height,
        mask="auto"
    )

    # =========================
    # LÍNEA SEPARADORA
    # =========================

    canvas.setStrokeColor(colors.HexColor("#1f4e78"))
    canvas.setLineWidth(1)

    canvas.line(
        2 * cm,
        height - 1.8 * cm,
        width - 2 * cm,
        height - 1.8 * cm
    )

    # =========================
    # FOOTER
    # =========================

    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)

    # Izquierda
    canvas.drawString(
        2 * cm,
        1 * cm,
        "Confidencial - Uso interno"
    )

    # Derecha
    page_number_text = f"Página {doc.page}"

    canvas.drawRightString(
        width - 2 * cm,
        1 * cm,
        page_number_text
    )

    canvas.restoreState()



def header_footer3(canvas, doc):

    canvas.saveState()

    width, height = doc.pagesize

    # =========================
    # HEADER
    # =========================

    # Título
    canvas.setFont("Helvetica-Bold", 11)
    canvas.setFillColor(colors.HexColor("#1f4e78"))

    canvas.drawString(
        2 * cm,
        height - 1.2 * cm,
        "REPORTE DE CONTROL"
    )

    # =========================
    # LOGO DERECHA
    # =========================

    from pathlib import Path
    from PIL import Image

    BASE_DIR = Path(__file__).resolve().parents[1]
    logo_path = BASE_DIR / "img" / "edemsa_logo.png"

    # Tamaño máximo permitido
    max_width = 2 * cm
    max_height = 1.2 * cm

    # Mantener proporción original
    with Image.open(logo_path) as img:
        img_width, img_height = img.size

    ratio = img_width / img_height

    if max_width / max_height < ratio:
        logo_width = max_width
        logo_height = max_width / ratio
    else:
        logo_height = max_height
        logo_width = max_height * ratio

    # Posición:
    # centrado verticalmente dentro del header
    logo_x = width - 2 * cm - logo_width
    logo_y = height - 1.45 * cm

    canvas.drawImage(
        str(logo_path),
        logo_x,
        logo_y,
        width=logo_width,
        height=logo_height,
        mask="auto"
    )

    # =========================
    # LÍNEA SEPARADORA
    # =========================

    canvas.setStrokeColor(colors.HexColor("#1f4e78"))
    canvas.setLineWidth(1)

    canvas.line(
        2 * cm,
        height - 1.8 * cm,
        width - 2 * cm,
        height - 1.8 * cm
    )

    # =========================
    # FOOTER
    # =========================

    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)

    # Izquierda
    canvas.drawString(
        2 * cm,
        1 * cm,
        "Confidencial - Uso interno"
    )

    # Derecha
    page_number_text = f"Página {doc.page}"

    canvas.drawRightString(
        width - 2 * cm,
        1 * cm,
        page_number_text
    )

    canvas.restoreState()





def header_footer2(canvas, doc):
    canvas.saveState()

    width, height = doc.pagesize

    # =========================
    # HEADER
    # =========================
    canvas.setFont("Helvetica-Bold", 11)
    canvas.setFillColor(colors.HexColor("#1f4e78"))

    canvas.drawString(2 * cm, height - 1.5 * cm, "REPORTE DE CONTROL")

    # línea debajo del header
    canvas.setStrokeColor(colors.HexColor("#1f4e78"))
    canvas.setLineWidth(1)
    canvas.line(2 * cm, height - 1.8 * cm, width - 2 * cm, height - 1.8 * cm)

    import os

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # logo_path = os.path.join(BASE_DIR, "..", "img", "edemsa_logo.png")
    from pathlib import Path

#     BASE_DIR = Path(__file__).resolve().parents[1]  # sube 2 niveles desde reportes/
#     logo_path = BASE_DIR / "img" / "edemsa_logo.png"
#     canvas.drawImage(
#     logo_path,
#     width - 4 * cm,
#     height - 2.2*cm,
#     width=2*cm,
#     height=1.5*cm,
#     mask='auto'
# )
    from PIL import Image

    BASE_DIR = Path(__file__).resolve().parents[1]
    logo_path = BASE_DIR / "img" / "edemsa_logo.png"

    # Tamaño máximo permitido
    max_width = 2 * cm
    max_height = 1.5 * cm

    # Proporción original
    with Image.open(logo_path) as img:
        img_width, img_height = img.size

    ratio = img_width / img_height

    # Ajustar dentro del rectángulo máximo sin deformar
    if max_width / max_height < ratio:
        logo_width = max_width
        logo_height = max_width / ratio
    else:
        logo_height = max_height
        logo_width = max_height * ratio

    canvas.drawImage(
        logo_path,
        width - 4 * cm,
        height - 2.2 * cm,
        width=logo_width,
        height=logo_height,
        mask="auto"
    )
     # =========================
    # LOGO DERECHA
    # =========================
    # BASE_DIR = Path(__file__).resolve().parents[1]
    # logo_path = BASE_DIR / "img" / "edemsa_logo.JPG"

    # logo_width = 2 * cm
    # logo_height = 1.5 * cm

    # canvas.drawImage(
    #     str(logo_path),
    #     width - 2 * cm - logo_width,   # esquina derecha
    #     height - 2.2 * cm,
    #     width=logo_width,
    #     height=logo_height,
    #     mask='auto'
    # )

    # canvas.restoreState()


    # canvas.drawImage("img/edemsa_logo.png", 2*cm, height-2.2*cm, width=2*cm, height=1.5*cm)

    # =========================
    # FOOTER
    # =========================
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)

    # izquierda
    canvas.drawString(2 * cm, 1 * cm, "Confidencial - Uso interno")

    # derecha (paginación)
    page_number_text = f"Página {doc.page}"
    canvas.drawRightString(width - 2 * cm, 1 * cm, page_number_text)

    canvas.restoreState()