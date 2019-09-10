from django.shortcuts import render,HttpResponseRedirect,get_object_or_404,redirect
from django.contrib import messages
from .models import *
from alim.models import AlimFatura
from satim.models import SatimFatura
from calisan.models import MaasOdeme,getAuthorization,canAdd,canChange,canDelete,canView
from datetime import date
# Create your views here.
def ciroIndex(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"proje gider")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if not canView(yetki):
        messages.warning(request,"Ciroya erişim izniniz yoktur.")
        return redirect("home:index")
    #</Güvenlik>
    today = date.today()
    if request.method == "POST":
        if request.POST.get("zaman") == "gunluk":
            projeGiderler = ProjeGider.objects.filter(tarih__day =  today.day,tarih__month = today.month,tarih__year = today.year)
            alimlar = AlimFatura.objects.filter(tarih__day =  today.day,tarih__month = today.month,tarih__year = today.year)
            satimlar = SatimFatura.objects.filter(tarihi__day =  today.day,tarihi__month = today.month,tarihi__year = today.year)
            maaslar = MaasOdeme.objects.filter(tarihi__day =  today.day,tarihi__month = today.month,tarihi__year = today.year)
        elif request.POST.get("haftalik"):
            pass
        elif request.POST.get("zaman") == "aylik":
            projeGiderler = ProjeGider.objects.filter(tarih__month = today.month,tarih__year = today.year)
            alimlar = AlimFatura.objects.filter(tarih__month = today.month,tarih__year = today.year)
            satimlar = SatimFatura.objects.filter(tarihi__month = today.month,tarihi__year = today.year)
            maaslar = MaasOdeme.objects.filter(tarihi__month = today.month,tarihi__year = today.year)
        elif request.POST.get("zaman") == "yillik":
            projeGiderler = ProjeGider.objects.filter(tarih__year = today.year)
            alimlar = AlimFatura.objects.filter(tarih__year = today.year)
            satimlar = SatimFatura.objects.filter(tarihi__year = today.year)
            maaslar = MaasOdeme.objects.filter(tarihi__year = today.year)
        elif request.POST.get("zaman") == "tumu":
            projeGiderler = ProjeGider.objects.all()
            alimlar = AlimFatura.objects.all()
            satimlar = SatimFatura.objects.all()
            maaslar = MaasOdeme.objects.all()
    else:
        projeGiderler = ProjeGider.objects.filter(tarih__day =  today.day,tarih__month = today.month,tarih__year = today.year)
        alimlar = AlimFatura.objects.filter(tarih__day =  today.day,tarih__month = today.month,tarih__year = today.year)
        satimlar = SatimFatura.objects.filter(tarihi__day =  today.day,tarihi__month = today.month,tarihi__year = today.year)
        maaslar = MaasOdeme.objects.filter(tarihi__day =  today.day,tarihi__month = today.month,tarihi__year = today.year)
    
    toplamProjeGider = 0
    toplamAlim = 0
    toplamSatim = 0
    toplamMaas = 0
    for i in projeGiderler:
        toplamProjeGider += i.talep.maliyet
    for i in alimlar:
        toplamAlim += i.get_toplam_tutar()
    for i in satimlar:
        toplamSatim += i.get_toplam_tutar()
    for i in maaslar:
        toplamMaas += i.calisan.maas
    ciro = toplamSatim - toplamProjeGider - toplamAlim - toplamMaas
    context = {
        'projeGiderler':projeGiderler,
        'toplamProjeGider':toplamProjeGider,
        'alimlar':alimlar,
        'toplamAlim':toplamAlim,
        'satimlar':satimlar,
        'toplamSatim':toplamSatim,
        'toplamMaas':toplamMaas,
        'ciro':ciro,
    }
    return render(request,"ciro/index.html",context)    