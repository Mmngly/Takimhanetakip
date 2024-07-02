from django.shortcuts import render, redirect, get_object_or_404
from servis.models import Alet, Teknisyen, AletHareketi, Raf
from django.db.models import Count
from django.db.models.functions import Coalesce
from datetime import datetime, timedelta
from servis.forms import AletForm, TeknisyenForm, RafForm
from dal import autocomplete

def ozel_admin_anasayfa(request):
    bugun = datetime.now().date()
    dun = bugun - timedelta(days=1)
    saat_18_30 = datetime.strptime("18:30", "%H:%M").time()

    # İstatistikler
    toplam_alet_sayisi = Alet.objects.count()
    raftaki_aletler = Alet.objects.filter(durum="Rafta").count()
    teknisyenlerde_aletler = Alet.objects.filter(durum="Teknisyende").count()
    en_cok_alinan_alet = AletHareketi.objects.values('alet__isim').annotate(
        alinma_sayisi=Count('alet')
    ).order_by('-alinma_sayisi').first()

    alinan_aletler = AletHareketi.objects.filter(
        alinma_zamani__date=dun,
        teslim_zamani__isnull=True 
    ) | AletHareketi.objects.filter(
        alinma_zamani__date=dun,
        teslim_zamani__date=dun,
        teslim_zamani__time__gte=saat_18_30 
    )

    # Raflardaki alet dağılımı için verileri hazırla
    raf_dagilimi = Alet.objects.values('raf').annotate(
        alet_sayisi=Coalesce(Count('id'), 0)
    )
    raflar = [item['raf'] for item in raf_dagilimi]
    alet_sayilari = [item['alet_sayisi'] for item in raf_dagilimi]

    # Haftalık alınan alet sayısı
    haftalik_alinan_aletler = AletHareketi.objects.filter(
        alinma_zamani__gte=bugun - timedelta(days=7)
    ).count()

    # Aylık alınan alet sayısı
    aylik_alinan_aletler = AletHareketi.objects.filter(
        alinma_zamani__year=bugun.year,
        alinma_zamani__month=bugun.month
    ).count()

    context = {
        'toplam_alet_sayisi': toplam_alet_sayisi,
        'raftaki_aletler': raftaki_aletler,
        'teknisyenlerde_aletler': teknisyenlerde_aletler,
        'en_cok_alinan_alet': en_cok_alinan_alet,
        'alinan_aletler': alinan_aletler,
        'raflar': raflar,
        'alet_sayilari': alet_sayilari,
        'haftalik_alinan_aletler': haftalik_alinan_aletler,
        'aylik_alinan_aletler': aylik_alinan_aletler,
    }
    return render(request, 'ozel_admin/anasayfa.html', context)


def alet_listesi(request):
    aletler = Alet.objects.all()
    context = {'aletler': aletler}
    return render(request, 'ozel_admin/alet_listesi.html', context)


def alet_ekle(request):
    if request.method == 'POST':
        form = AletForm(request.POST)
        if form.is_valid():
            try:
                yeni_alet = form.save(commit=False)
                if yeni_alet.durum == 'teknisyende':
                    teknisyen_id = request.POST.get('teknisyen')
                    yeni_alet.teknisyen = get_object_or_404(Teknisyen, pk=teknisyen_id)
                yeni_alet.save() # raf seçimi otomatik olarak formdan alınır
                return redirect('alet_listesi')
            except Exception as e:
                print(e) # Hata mesajını konsola yazdırın
                form.add_error(None, 'Bir hata oluştu. Lütfen tekrar deneyin.')
    else:
        form = AletForm()
    teknisyenler = Teknisyen.objects.all()
    raflar = Raf.objects.all() 
    return render(request, 'ozel_admin/alet_ekle.html', {'form': form, 'teknisyenler': teknisyenler, 'raflar': raflar})


def raporlar(request):
    bugun = datetime.now().date()
    bir_hafta_oncesi = bugun - timedelta(days=7)

    # Son 7 günün raporlarını al
    alinan_aletler_listesi = []
    for i in range(7):
        tarih = bugun - timedelta(days=i)
        saat_18_30 = datetime.strptime("18:30", "%H:%M").time()
        alinan_aletler = AletHareketi.objects.filter(
            alinma_zamani__date=tarih,
            teslim_zamani__isnull=True
        ) | AletHareketi.objects.filter(
            alinma_zamani__date=tarih,
            teslim_zamani__date=tarih,
            teslim_zamani__time__gte=saat_18_30
        )
        alinan_aletler_listesi.append({'tarih': tarih, 'alinan_aletler': alinan_aletler})

    context = {'alinan_aletler_listesi': alinan_aletler_listesi}
    return render(request, 'ozel_admin/raporlar.html', context)


def teknisyen_ekle(request):
    if request.method == 'POST':
        form = TeknisyenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teknisyen_listesi')  
    else:
        form = TeknisyenForm()
    return render(request, 'ozel_admin/teknisyen_ekle.html', {'form': form})


class AletAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Alet.objects.all()

        if self.q:
            qs = qs.filter(isim__icontains=self.q)

        return qs


class TeknisyenAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Teknisyen.objects.all()

        if self.q:
            qs = qs.filter(isim__icontains=self.q)

        return qs


class RafAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        qs = Alet.objects.values_list('raf', flat=True).distinct()
        return list(qs)


def raf_ekle(request):
  if request.method == 'POST':
      form = RafForm(request.POST)
      if form.is_valid():
          form.save()
          return redirect('raf_listesi')  # Raf eklendikten sonra raf listesine yönlendir
  else:
      form = RafForm()
  return render(request, 'ozel_admin/raf_ekle.html', {'form': form})