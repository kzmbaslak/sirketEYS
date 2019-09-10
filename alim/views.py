from django.shortcuts import render,HttpResponseRedirect,get_object_or_404,redirect
from .models import AlimFatura
from django.contrib import messages
from .models import AlimFatura
from calisan.models import Calisan,getAuthorization,canAdd,canChange,canDelete,canView
from .form import AlimForm
# Create your views here.
admin_url = "/admin/alim/alimfatura"
def alimIndex(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"alim fatura")#25 permission idsi dir.
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if not canView(yetki):
        messages.warning(request,"Alım işlemlerine erişim izniniz yoktur.")
        return redirect("home:index")
    #</Güvenlik>
    alimlar = AlimFatura.objects.all()
    context = {
        'alimlar':alimlar,
        'canAdd':canAdd(yetki),
        'canChange':canChange(yetki),
        'canDelete':canDelete(yetki),
    }
    return render(request,'alim/index.html',context)

def alimDetail(request,slug):
    #<Güvenlik>
    yetki = getAuthorization(request,"alim fatura")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if not canView(yetki):
        messages.warning(request,"Alım bilgilerine erişim yetkiniz yoktur.")
        return redirect("alim:index")
        
    #</Güvenlik>
    alim = get_object_or_404(AlimFatura,slug=slug)
    context = {
        'alim':alim,
        'canAdd':canAdd(yetki),
        'canChange':canChange(yetki),
        'canDelete':canDelete(yetki),
    }
    return render(request,"alim/alimdetay.html",context)
"""def alimDetail(request,id):
    return redirect("{}/{}/change".format(admin_url,id))"""

"""def alimCreate(request,id):
    form = AlimForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Alım faturası başarılı şekilde oluşturuldu.')
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    
    context = {
        'form':form,
        'value':'Oluştur',
    }
    return render(request,"form.html",context)
"""
def alimCreate(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"alim fatura")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Alım yapma yetkiniz yoktur.")
        return redirect("alim:index")
    #</Güvenlik>
    if request.method == "POST":
        form = AlimForm(request.POST or None)
        if form.is_valid():
            alim = form.save()
            messages.success(request,'Alım işlemi başarılı bir şekilde gerçekleştirildi.')
            return HttpResponseRedirect(alim.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    else:
        form = AlimForm()
    context = {
        'form':form,
        'value':'Alım Oluştur',
    }
    return render(request,"alim/form.html",context)

def alimUpdate(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"alim fatura")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canChange(yetki):
        messages.warning(request,"Alım işlemlerini güncelleme yetkiniz yoktur.")
        alimFatura = get_object_or_404(AlimFatura,id=id)
        return HttpResponseRedirect(alimFatura.get_absolute_url())
    #</Güvenlik>
    alimFatura = get_object_or_404(AlimFatura,id=id)
    form = AlimForm(request.POST or None,instance=alimFatura)
    if request.method == "POST":
        if form.is_valid():
            alim = form.save()
            messages.success(request,'Duyuru başarılı bir şekilde güncellenmiştir.')
            return HttpResponseRedirect(alim.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    context = {
        'form':form,
        'value':'Güncelle',
    }
    return render(request,'alim/form.html',context)

def alimDelete(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"alim fatura")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canDelete(yetki):
        messages.warning(request,"Alınan ürünleri silme yetkiniz bulunmamaktadır.")
        return redirect("alim:index")
    #</Güvenlik>
    return redirect("{}/{}/delete".format(admin_url,id))

