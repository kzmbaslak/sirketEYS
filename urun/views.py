from django.shortcuts import render,HttpResponseRedirect,get_object_or_404,redirect,reverse
from django.contrib import messages
from .models import Urun
from .form import *
from calisan.models import getAuthorization,canAdd,canChange,canDelete,canView
# Create your views here.

admin_url = "/admin/urun/urun"
def urunIndex(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"urun")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if not canView(yetki):
        messages.warning(request,"Ürünlere erişim yetkiniz yoktur.")
        return redirect("home:index")
        
    #</Güvenlik>
    urunler = Urun.objects.all()
    context = {
        'urunler':urunler,
        'canAdd':canAdd(yetki),
        'canChange':canChange(yetki),
        'canDelete':canDelete(yetki),
    }
    return render(request,'urun/index.html',context)

"""def urunDetail(request,slug):
    urun = get_object_or_404(Urun,slug=slug)
    context = {
        'urun':urun,
    }
    return render(request,"urun/urundetay.html",context)
"""
def urunCreate(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"urun")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Ürün ekleme yetkiniz yoktur.")
        return redirect("urun:index")
    #</Güvenlik>
    if request.method == "POST":
        form = UrunYeniForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,'Ürün başarılı bir şekilde oluşturuldu.')
            return HttpResponseRedirect(reverse("urun:index"))
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    else:
        form = UrunYeniForm()
    context = {
        'form':form,
        'value':'Ürün Oluştur',
    }
    return render(request,"urun/form.html",context)

def urunUpdate(request,slug):
    #<Güvenlik>
    yetki = getAuthorization(request,"urun")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canChange(yetki):
        messages.warning(request,"Ürün güncelleme yetkiniz yoktur.")
        return redirect("urun:index")
    #</Güvenlik>
    if request.method == "POST":
        urun = get_object_or_404(Urun,slug=slug)
        form = UrunForm(request.POST or None,instance = urun)
        if form.is_valid():
            if form.cleaned_data['stok'] > 0:
                urun = form.save(commit=False)
                urun.stokMiktari += form.cleaned_data['stok']
                urun.save()
                messages.success(request,"Stok artırıldı")
                return redirect('urun:index')
            else:
                messages.warning(request,"Lütfen 0 da büyük bir stok miktarı girin")
        else:
            messages.warning(request,"Lütfen zorunlu alanları doldurun")
    else:
        form = UrunForm()
    context = {
        'form':form,
        'value':'Stok Ekle',
    }
    return render(request,"urun/form.html",context)

def urunDelete(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"urun")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canDelete(yetki):
        messages.warning(request,"Ürün silme yetkiniz bulunmamaktadır.")
        return redirect("urun:index")
    #</Güvenlik>
    return redirect("{}/{}/delete".format(admin_url,id))

