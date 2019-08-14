import json, urllib.request
import requests
import textwrap
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer, Paragraph, Table, TableStyle, CellStyle)
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from io import BytesIO


with urllib.request.urlopen("https://xinternet.co/manifiestos/json/manifest_example.json") as url:
    data = json.loads(url.read().decode())

filename = "ECOCAPITAL COD " + data['manifest']['client']['code_eco'] + ".pdf"

pagesize = (letter)


class Manifiesto(APIView):
    # permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        doc = SimpleDocTemplate("manifiestos/" + filename, pagesize = pagesize, topMargin=1 * cm, bottomMargin=1 * cm, leftMargin=30)    # Directorio raíz de la app.

        def procesoPpal(Story):
            """ Creación del informe. """

            I = Image("manifiestos/manifest/static/manifest/logo-horizontal.jpg", width=136, height=42)
            Comprobante = Paragraph("Comprobantes # " + data['manifest']['id'], estilo['Comprobante'])

            t = Table(
                data = [
                    [Comprobante]
                ],
                style=[
                    ('VALIGN',(0,0),(0,0),'CENTER'),
                    ('BOTTOMPADDING', (0, 0),(0, 0), 25),
                ], 
                colWidths=[550], hAlign='LEFT',
            )

            Story.append(t)

            # Datos del formato

            datoformato1 = Paragraph('''<b>Codigo:</b> OPE_FOR_002''', estilo['datosFormato'])
            datoformato2 = Paragraph('''<b>Version:</b> 03''', estilo['datosFormato'])
            datoformato3 = Paragraph('''<b>Fecha de vigencia:</b> 02/01/2017''', estilo['datosFormato'])

            t = Table(
                data = [
                    [I, datoformato1],
                    ['', datoformato2],
                    ['', datoformato3],
                ],
                style=[
                    ('VALIGN',(0,0),(0,0),'CENTER'),
                    ('GRID',(0,0),(1,2),0.5,colors.gray),
                    ('SPAN', (0, 0),(0, 2)),
                    ('BOX', (0,0), (1,2), 0.5, colors.black),
                ], 
                colWidths=[144, 200], 
                hAlign='LEFT',
            )

            Story.append(t)

            ecoCapital = Paragraph('ECOCAPITAL | NIT 900.487.187-3 | Carrera 19A No 61-11', estilo['datosFormato'])
            planned_date = Paragraph('''<b>FECHA FRECUENCIA: </b>''' + data['manifest']['planned_date'], estilo['datosFormato'])
            date = Paragraph('''<b>Fecha de Recoleccion: </b>''' + data['manifest']['date'] + 
                ''' | <b>Código</b> ''' + data['manifest']['client']['code_eco'], estilo['datosFormato'])
            client = Paragraph(data['manifest']['client']['name'], estilo['client'])
            geoInformacion = Paragraph(data['manifest']['client']['geoinformation']['address'] + 
                ' | ' + '''<b>NIT o CC </b>''' + data['manifest']['client']['id'], estilo['datosFormato'])
            transmDatos = Paragraph('''Transmisión de datos / <b>Inicio: </b>''' + data['manifest']['start_time'] + 
                ''' - <b>Final: </b>''' + data['manifest']['end_time'], estilo['datosFormato'])
            recoge = Paragraph('''<b>Recoge: </b>''' + data['manifest']['fleet']['driver']['name'] + 
                ''' | <b>CC</b> ''' + data['manifest']['fleet']['driver']['id'], estilo['datosFormato'])
            placa = Paragraph('''<b>Placa: </b>''' +  data['manifest']['fleet']['license_plate'] + " " +
                '''<b>Ruta: </b> ''' + data['manifest']['fleet']['route'], estilo['datosFormato'])

            t = Table(
                data = [
                    [ecoCapital],
                    [planned_date],
                    [date],
                    [client],
                    [geoInformacion],
                    [transmDatos],
                    [recoge],
                    [placa],
                ],
                style=[
                    ('VALIGN',(0,0),(-1,-1),'CENTER'),
                    ('TOPPADDING', (0, 0),(-1, -1), 10),
                ], 
                colWidths=[550], 
                hAlign='LEFT',
            )

            Story.append(t)

            produc1 = Paragraph(data['manifest']['production'][0]['units'] + '''<b> Producción </b> ''' + 
                data['manifest']['production'][0]['tag'], estilo['datosRecogida'])
            cantidadProduc1 = Paragraph(data['manifest']['production'][0]['total_value'], estilo['Normal'])
            produc2 = Paragraph(data['manifest']['production'][1]['units'] + '''<b> Producción </b> ''' + 
                data['manifest']['production'][1]['tag'], estilo['datosRecogida'])
            cantidadProduc2 = Paragraph(data['manifest']['production'][1]['total_value'], estilo['Normal'])
            produc3 = Paragraph(data['manifest']['production'][2]['units'] + '''<b> Producción </b> ''' + 
                data['manifest']['production'][2]['tag'], estilo['datosRecogida'])
            cantidadProduc3 = Paragraph(data['manifest']['production'][2]['total_value'], estilo['Normal'])
            produc4 = Paragraph(data['manifest']['production'][3]['units'] + '''<b> Producción </b> ''' + 
                data['manifest']['production'][3]['tag'], estilo['datosRecogida'])
            cantidadProduc4 = Paragraph(data['manifest']['production'][3]['total_value'], estilo['Normal'])

            termoRecambio = Paragraph("# " + data['manifest']['items'][0]['tag'] + " Recambio", estilo['datosRecogida'])
            cantidadTermRecambio = Paragraph(data['manifest']['items'][0]['exchanged'], estilo['Normal'])
            termoRecogido = Paragraph("# " + data['manifest']['items'][0]['tag'] + " Recogidos", estilo['datosRecogida'])
            cantidadTermRecogido = Paragraph(data['manifest']['items'][0]['picked_up'], estilo['Normal'])
            termoAsig = Paragraph("# " + data['manifest']['items'][0]['tag'] + " Asignados", estilo['datosRecogida'])
            cantidadTermAsig = Paragraph(data['manifest']['items'][0]['delivered'], estilo['Normal'])

            estRecambio = Paragraph("# " + data['manifest']['items'][1]['tag'] + " Recambio", estilo['datosRecogida'])
            cantidadEstRecambio = Paragraph(data['manifest']['items'][1]['exchanged'], estilo['Normal'])
            estRecogido = Paragraph("# " + data['manifest']['items'][1]['tag'] + " Recogidos", estilo['datosRecogida'])
            cantidadEstRecogido = Paragraph(data['manifest']['items'][1]['picked_up'], estilo['Normal'])
            estAsig = Paragraph("# " + data['manifest']['items'][1]['tag'] + " Asignados", estilo['datosRecogida'])
            cantidadestAsig = Paragraph(data['manifest']['items'][1]['delivered'], estilo['Normal'])

            textoNovedad = Paragraph("Novedad", estilo['datosRecogida'])
            tipoNovedad = Paragraph(data['manifest']['novelties'][0]['comment'], estilo['Normal'])
            textObs = Paragraph("Observaciones: ", estilo['datosRecogida'])

            t = Table(
                data = [
                    [[produc1], [cantidadProduc1]],
                    [[produc2], [cantidadProduc2]],
                    [[produc3], [cantidadProduc3]],
                    [[produc4], [cantidadProduc4]],
                    [[termoRecambio], [cantidadTermRecambio]],
                    [[termoRecogido], [cantidadTermRecogido]],
                    [[termoAsig], [cantidadTermAsig]],
                    [[estRecambio], [cantidadEstRecambio]],
                    [[estRecogido], [cantidadEstRecogido]],
                    [[estAsig], [cantidadestAsig]],
                    [[textoNovedad], [tipoNovedad]],
                    [[textObs]],
                ],
                style=[
                    ('VALIGN',(0,0),(-1,-2),'CENTER'),
                    ('TOPPADDING', (0, 0),(-1, -1), 10),
                ], 
                colWidths=[250, 250], 
            )

            Story.append(t)
            Story.append(PageBreak())

            textEvidencia = Paragraph(data['manifest']['novelties'][0]['evidence_type'] + " Novedad", estilo['Normal'])
            I = Image(data['manifest']['novelties'][0]['file'])
            textFirma1 = Paragraph("Firma quien entrega", estilo['Normal'])
            signaClient = Image(data['manifest']['signatures'][1]['signature_file'])
            textFirma2 = Paragraph("Firma quien recoge", estilo['Normal'])
            signaEmployee = Image(data['manifest']['signatures'][3]['signature_file'])
            finalText = Paragraph("El presente manifiesto no se constituye como acta de tratamiento y/o disposición final, por tanto su validez únicamente corresponde a la del manifiesto de recolección y transporte de residuos de riesgo biológico", estilo['Normal'])

            t = Table(
                data = [
                    [textEvidencia],
                    [I],
                    [textFirma1],
                    [signaClient],
                    [textFirma2],
                    [signaEmployee],
                    [finalText],
                ],
                style=[
                    ('VALIGN',(0,0),(0,0),'CENTER'),
                    ('TOPPADDING', (0, 0),(0, 0), 10),
                ], 
                colWidths=[500], 
            )

            Story.append(t)

            return Story

        # Código principal

        estilo = getSampleStyleSheet()

        estilo.add(ParagraphStyle(name = "Comprobante", alignment=TA_LEFT, fontSize=18, fontName="Helvetica-Bold"))
        estilo.add(ParagraphStyle(name = "datosFormato", alignment=TA_LEFT, fontSize=9, fontName="Helvetica"))
        estilo.add(ParagraphStyle(name = "client", alignment=TA_LEFT, fontSize=11, fontName="Helvetica-Bold"))
        estilo.add(ParagraphStyle(name = 'datosRecogida', alignment=TA_RIGHT, fontSize=10.5, fontName="Helvetica-Bold"))
        
        Story = []

        procesoPpal(Story)

        doc.build(Story)

        fs = FileSystemStorage("manifiestos")
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type = 'application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + filename
            return response
        
        return response
