import csv
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.shortcuts import render, get_object_or_404, redirect
from .models import Alet, Teknisyen, AletHareketi, Raf
from .forms import AletHareketiForm, AletForm, TeknisyenForm
from datetime import datetime, timedelta


def takimhane_anasayfa(request):
    alet_hareketleri = AletHareketi.objects.filter(
        teslim_zamani__isnull=True
    ).select_related('alet', 'alet__raf', 'teknisyen')
    context = {'alet_hareketleri': alet_hareketleri}
    return render(request, 'servis/anasayfa.html', context)


def alet_detay(request, alet_id):
    alet = get_object_or_404(Alet, pk=alet_id)
    hareketler = AletHareketi.objects.filter(alet=alet).order_by('-alinma_zamani')

    if request.method == 'POST':
        form = AletHareketiForm(request.POST)
        if form.is_valid():
            hareket = form.save(commit=False)
            hareket.alet = alet
            hareket.save()
            return redirect('alet_detay', alet_id=alet.id)
    else:
        form = AletHareketiForm()

    context = {'alet': alet, 'hareketler': hareketler, 'form': form}
    return render(request, 'servis/alet_detay.html', context)


def alet_teslim_al(request, hareket_id):
    hareket = get_object_or_404(AletHareketi, pk=hareket_id)
    hareket.teslim_zamani = datetime.now()
    hareket.save()
    return redirect('takimhane_anasayfa')


def toplu_teslim_al(request):
    if request.method == 'POST':
        selected_hareketler = request.POST.getlist('selected_hareketler')
        AletHareketi.objects.filter(pk__in=selected_hareketler).update(
            teslim_zamani=datetime.now()
        )
    return redirect('takimhane_anasayfa')


def teknisyen_detay(request, teknisyen_id):
    teknisyen = get_object_or_404(Teknisyen, pk=teknisyen_id)
    aletler = AletHareketi.objects.filter(
        teknisyen=teknisyen, teslim_zamani__isnull=True
    )
    context = {'teknisyen': teknisyen, 'aletler': aletler}
    return render(request, 'servis/teknisyen_detay.html', context)

def alet_aktar(request, hareket_id):
    hareket = get_object_or_404(AletHareketi, pk=hareket_id)
    if request.method == 'POST':
        form = AletForm(request.POST, instance=hareket.alet)  # AletForm kullanılıyor
        if form.is_valid():
            form.save()
            hareket.teknisyen = form.cleaned_data['teknisyen']
            hareket.save()
            return redirect('takimhane_anasayfa')
    else:
        form = AletForm(instance=hareket.alet)
    return render(request, 'servis/alet_aktar.html', {'form': form, 'hareket': hareket})


def olustur_gunluk_rapor(request):
    bugun = datetime.now().date()
    dun = bugun - timedelta(days=1)
    saat_18_30 = datetime.strptime("18:30", "%H:%M").time()

    alinan_aletler = AletHareketi.objects.filter(
        alinma_zamani__date=dun, teslim_zamani__isnull=True
    ) | AletHareketi.objects.filter(
        alinma_zamani__date=dun, teslim_zamani__time__gte=saat_18_30
    )

    format = request.GET.get('format', 'pdf')

    if format == 'pdf':
        # PDF dosyası oluşturma
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'
        ] = f'attachment; filename="gunluk_rapor_{dun}.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        p.drawString(100, 750, f"Günlük Rapor ({dun})")

        y = 700
        for hareket in alinan_aletler:
            p.drawString(
                100,
                y,
                f"{hareket.alet.isim} - {hareket.teknisyen.isim} - {hareket.alinma_zamani}",
            )
            y -= 20  # Satır yüksekliğini ayarla

        p.showPage()
        p.save()
        return response
    elif format == 'excel':
        # Excel dosyası oluşturma
        response = HttpResponse(content_type='application/ms-excel')
        response[
            'Content-Disposition'
        ] = f'attachment; filename="gunluk_rapor_{dun}.xlsx"'

        wb = Workbook()
        ws = wb.active
        ws.append(['Alet', 'Teknisyen', 'Alınma Zamanı'])
        for hareket in alinan_aletler:
            ws.append(
                [hareket.alet.isim, hareket.teknisyen.isim, hareket.alinma_zamani]
            )

        wb.save(response)
        return response
    else:
        return HttpResponse("Geçersiz format")

def alet_ver(request, alet_id):
    alet = get_object_or_404(Alet, pk=alet_id)

    if request.method == 'POST':
        form = AletHareketiForm(request.POST)
        if form.is_valid():
            hareket = form.save(commit=False)
            hareket.alet = alet
            hareket.save()
            return redirect('takimhane_anasayfa')  # Anasayfaya yönlendir
    else:
        form = AletHareketiForm()  # Boş form oluştur

    context = {'form': form, 'alet': alet}
    return render(request, 'servis/alet_ver.html', context)  # Formu göster