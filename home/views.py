from django.shortcuts import render,HttpResponse, get_object_or_404, HttpResponseRedirect,redirect
from .models import Duyuru
from django.contrib.auth.models import User
from .form import DuyuruForm
from django.contrib import messages
from calisan.models import Calisan,getAuthorization,canAdd,canChange,canDelete,canView
# Create your views here.

def homeIndex(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"duyuru")#25 permission idsi dir.
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    #if not canView(yetki):
    #    messages.warning(request,"Duyurulara erişim izniniz yoktur.")
    #    return redirect("/admin")
    #</Güvenlik>
    yetkiAlim = getAuthorization(request,"alim fatura")
    yetkiSatim = getAuthorization(request,"satim fatura")
    yetkiUrun = getAuthorization(request,"urun")
    yetkiCiro = getAuthorization(request,"ciro")

    request.session['yetkiAlim'] = canView(yetkiAlim)
    request.session['yetkiSatim'] = canView(yetkiSatim)
    request.session['yetkiUrun'] = canView(yetkiUrun)
    request.session['yetkiCiro'] = canView(yetkiCiro)

    duyuru = Duyuru.objects.all()
    """calisan = get_object_or_404(Calisan,user = request.user)
    if len(request.user.groups.all()) > 0:
        request.session['group'] = request.user.groups.all()[0].name
    else:
        request.session['group'] = "null"
    request.session['slug'] = calisan.slug"""
    context = {
        'duyuru':duyuru,
        'canAdd':canAdd(yetki),
        'canChange':canChange(yetki),
        'canDelete':canDelete(yetki),
    }
    return render(request,'home/index.html',context)


def duyuruDetail(request,slug):
    #<Güvenlik>
    yetki = getAuthorization(request,"duyuru")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if not canView(yetki):
        messages.warning(request,"Duyuru detayına erişim yetkiniz yoktur.")
        return redirect("home:index")
        
    #</Güvenlik>
    duyuru = get_object_or_404(Duyuru,slug = slug)
    context = {
        'duyuru':duyuru,
        'canAdd':canAdd(yetki),
        'canChange':canChange(yetki),
        'canDelete':canDelete(yetki),
    }
    return render(request,"home/duyurudetay.html",context)

def duyuruCreate(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"duyuru")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Duyuru ekleme yetkiniz yoktur.")
        return redirect("home:index")
    #</Güvenlik>
    if request.method == "POST":
        form = DuyuruForm(request.POST or None)
        if form.is_valid():
            duyuru = form.save()
            messages.success(request,'Duyuru başarılı bir şekilde oluşturulmuştur.')
            return HttpResponseRedirect(duyuru.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    else:
        form = DuyuruForm()
    context = {
        'form':form,
        'value':'Gönder',
    }
    return render(request,"home/form.html",context)

def duyuruUpdate(request,slug):
    #<Güvenlik>
    yetki = getAuthorization(request,"duyuru")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canChange(yetki):
        messages.warning(request,"Duyuru güncelleme yetkiniz yoktur.")
        duyuru = get_object_or_404(Duyuru,slug=slug)
        return HttpResponseRedirect(duyuru.get_absolute_url())
    #</Güvenlik>
    duyuru = get_object_or_404(Duyuru,slug=slug)
    form = DuyuruForm(request.POST or None,instance=duyuru)
    if request.method == "POST":
        if form.is_valid():
            duyuru = form.save()
            messages.success(request,'Duyuru başarılı bir şekilde güncellenmiştir.')
            return HttpResponseRedirect(duyuru.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    context = {
        'form':form,
        'value':'Güncelle',
    }
    return render(request,'home/form.html',context)
def duyuruDelete(request,slug):
    #<Güvenlik>
    yetki = getAuthorization(request,"duyuru")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canDelete(yetki):
        messages.warning(request,"Duyuru silme yetkiniz bulunmamaktadır.")
        return redirect("home:index")
    #</Güvenlik>
    duyuru = get_object_or_404(Duyuru,slug = slug)
    duyuru.delete()
    messages.success(request,'Duyuru silindi.')
    return redirect("home:index")
