from django.shortcuts import render,HttpResponseRedirect,get_object_or_404,redirect
from .models import SatimFatura
from django.contrib import messages
from .form import SatimForm
from urun.models import Urun
from calisan.models import getAuthorization,canAdd,canChange,canDelete,canView
# Create your views here.
admin_url = "/admin/satim/satimfatura"
def satimIndex(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"satim fatura")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if not canView(yetki):
        messages.warning(request,"Satışlara erişim yetkiniz yoktur.")
        return redirect("home:index")
    #</Güvenlik>
    satimlar = SatimFatura.objects.all()
    context = {
        'satimlar':satimlar,
        'canAdd':canAdd(yetki),
        'canChange':canChange(yetki),
        'canDelete':canDelete(yetki),
    }
    return render(request,'satim/index.html',context)

def satimDetail(request,slug):
    #<Güvenlik>
    yetki = getAuthorization(request,"satim fatura")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if not canView(yetki):
        messages.warning(request,"Satışlara erişim yetkiniz yoktur.")
        return redirect("satim:index")
        
    #</Güvenlik>
    satim = get_object_or_404(SatimFatura,slug=slug)
    context = {
        'satim':satim,
        'canAdd':canAdd(yetki),
        'canChange':canChange(yetki),
        'canDelete':canDelete(yetki),
    }
    return render(request,"satim/satimdetay.html",context)

def satimCreate(request): 
    #<Güvenlik>
    yetki = getAuthorization(request,"satim fatura")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Satış yapma yetkiniz yoktur.")
        return redirect("satim:index")
    #</Güvenlik>
    if request.method == "POST":
        form = SatimForm(request.POST or None)
        if form.is_valid():
            if form.cleaned_data['adedi'] > 0:
                urun = get_object_or_404(Urun,id = form.cleaned_data['urun'].id)
                if urun.stokMiktari >= form.cleaned_data['adedi']:
                    urun.stokMiktari -= form.cleaned_data['adedi']
                    urun.save()
                    form.save()
                    messages.success(request,"Satış başarılı şekilde gerçekleştirilmiştir.")
                    return redirect("satim:index")
                else:
                    messages.warning(request,"Yeterli stok mevcut değildir. Stok miktarı:{}".format(urun.stokMiktari))
            else:
                messages.warning(request,"adedi 0 dan büyük sayılar giriniz.")
    else:
        form = SatimForm()
    context = {
        'form':form,
        'value':'Satış Yap',
    }

    return render(request,"satim/form.html",context)

def satimUpdate(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"satim fatura")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canChange(yetki):
        messages.warning(request,"Satışları güncelleme yetkiniz yoktur.")
        satimFatura = get_object_or_404(SatimFatura,id=id)
        return HttpResponseRedirect(satimFatura.get_absolute_url())
    #</Güvenlik>
    satimFatura = get_object_or_404(SatimFatura,id=id)
    form = SatimForm(request.POST or None,instance=satimFatura)
    if request.method == "POST":
        if form.is_valid():
            satim = form.save()
            messages.success(request,'Satış başarılı bir şekilde güncellenmiştir.')
            return HttpResponseRedirect(satim.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    context = {
        'form':form,
        'value':'Güncelle',
    }
    return render(request,'satim/form.html',context)

def satimDelete(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"satim fatura")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canDelete(yetki):
        messages.warning(request,"Satış silme yetkiniz bulunmamaktadır.")
        return redirect("satim:index")
    #</Güvenlik>
    satim = get_object_or_404(SatimFatura,id = id)
    urun = get_object_or_404(Urun,id = satim.urun.id)
    urun.stokMiktari += satim.adedi
    urun.save()
    satim.delete()
    messages.success(request,"Satış iptal edilmiştir.")
    return redirect("satim:index")


    

