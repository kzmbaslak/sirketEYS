from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from .models import *
from django.contrib import messages
from .form import *
from ciro.models import *
from calisan.models import Calisan,Yetki,getAuthorization,canAdd,canChange,canDelete,canView
admin_url = "/admin/proje/proje"
admin_talep_url = "/admin/proje/talep"
admin_ekip_url = "/admin/proje/ekip"
admin_ekipuye_url = "/admin/proje/ekipuye"
# Create your views here.
def projeIndex(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"proje")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if canView(yetki):
        projeler = Proje.objects.all()
    else:
        calisan = get_object_or_404(Calisan,user = request.user)
        ekipUyeler = EkipUye.objects.filter(calisan = calisan)
        ekipler = []
        for i in ekipUyeler:
            ekipler.append(Ekip.objects.get(id = i.ekip.id))
        projeler = []
        for i in ekipler:
            projeler.append(Proje.objects.get(id = i.proje.id))
    #</Güvenlik>
    yetkiEkip = getAuthorization(request,"ekip")
    yetkiTalep = getAuthorization(request,"talep")
    context = {
        'projeler':projeler,
        'canAdd':canAdd(yetki),
        'canChange':canChange(yetki),
        'canDelete':canDelete(yetki),
        'canAddEkip':canAdd(yetkiEkip),
        'canAddTalep':canAdd(yetkiTalep),
        
    }
    return render(request,"proje/index.html",context)

def projeDetail(request,slug):
    #<Güvenlik>
    yetki = getAuthorization(request,"proje")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if not canView(yetki):
        messages.warning(request,"Proje bilgilerine erişim yetkiniz yoktur.")
        return redirect("proje:index")
        
    #</Güvenlik>
    #yetkiler
    yetkiEkip = getAuthorization(request,"ekip")
    yetkiTalep = getAuthorization(request,"talep")
    yetkiEkipUye = getAuthorization(request,"ekip uye")

    proje = get_object_or_404(Proje,slug=slug)
    ekipler = False
    ekipUyeler = False
    projeTalepler = False
    if canView(yetkiEkip):
        ekipler = Ekip.objects.filter(proje = proje)
        if canView(yetkiEkipUye):
            ekipUyeler = list()
            for ekip in ekipler:
                ekipUyeler.append(EkipUye.objects.filter(ekip = ekip))
    if canView(yetkiTalep):
        projeTalepler = Talep.objects.filter(proje = proje)
    
    context = {
        'proje':proje,
        'ekipler':ekipler,
        'ekipUyeler':ekipUyeler,
        'projeTalepler':projeTalepler,
        #yetki
        'canAdd':canAdd(yetki),
        'canChangeEkip':canChange(yetkiEkip),
        'canDeleteEkip':canDelete(yetkiEkip),
        'canAddEkipUye':canAdd(yetkiEkipUye),
        'canChangeEkipUye':canChange(yetkiEkipUye),
        'canDeleteEkipUye':canDelete(yetkiEkipUye),
    }
    return render(request,"proje/projedetay.html",context)

def projeCreate(request): 
    #<Güvenlik>
    yetki = getAuthorization(request,"proje")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Proje oluşturma yetkiniz yoktur.")
        return redirect("proje:index")
    #</Güvenlik>
    if request.method == "POST":
        form = ProjeForm(request.POST or None)
        if form.is_valid():
            proje = form.save()
            messages.success(request,'Proje başarılı bir şekilde oluşturuldu.')
            return HttpResponseRedirect(proje.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    else:
        form = ProjeForm()
    context = {
        'form':form,
        'value':'Proje Oluştur',
    }
    return render(request,"proje/form.html",context)

def projeUpdate(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"proje")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canChange(yetki):
        messages.warning(request,"Proje güncelleme yetkiniz yoktur.")
        proje = get_object_or_404(Proje,id=id)
        return HttpResponseRedirect(proje.get_absolute_url())
    #</Güvenlik>
    proje = get_object_or_404(Proje,id=id)
    form = ProjeForm(request.POST or None,instance=proje)
    if request.method == "POST":
        if form.is_valid():
            proje = form.save()
            messages.success(request,'Proje başarılı bir şekilde güncellenmiştir.')
            return HttpResponseRedirect(proje.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    context = {
        'form':form,
        'value':'Güncelle',
    }
    return render(request,'proje/form.html',context)
    return redirect("{}/{}/change".format(admin_url,id))

def projeDelete(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"proje")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canDelete(yetki):
        messages.warning(request,"Proje silme yetkiniz bulunmamaktadır.")
        return redirect("proje:index")
    #</Güvenlik>
    return redirect("{}/{}/delete".format(admin_url,id))

def ekipCreate(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"ekip")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Ekip oluşturma yetkiniz yoktur.")
        return redirect("proje:index")
    #</Güvenlik>
    if request.method == "POST":
        form = EkipForm(request.POST or None)
        if form.is_valid():
            ekip = form.save(commit = False)
            ekip.proje = get_object_or_404(Proje,id = id)
            ekip.save()
            messages.success(request,"Ekip başarılı şekilde oluşturuldu")
            yetki = get_object_or_404(Yetki,id = 7)
            for calisan in form.cleaned_data['calisanlar']:
                EkipUye.objects.create(ekip = ekip, calisan = calisan, yetki = yetki).save()
            messages.success(request,"Ekip üyleri eklendi")
            return redirect("proje:index")
        else:
            messages.warning(request,"Zorunlu alanları dolurunuz")
    else:
        form = EkipForm()
    context = {
        'form':form,
        'value':'Ekip Oluştur',
    }
    return render(request,"proje/form.html",context)
def ekipUpdate(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"ekip")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canChange(yetki):
        messages.warning(request,"Ekip güncelleme yetkiniz yoktur.")
        ekip = get_object_or_404(Ekip,id=id)
        return HttpResponseRedirect(ekip.proje.get_absolute_url())
    #</Güvenlik>
    ekip = get_object_or_404(Ekip,id=id)
    form = EkipForm(request.POST or None,instance=ekip)
    if request.method == "POST":
        if form.is_valid():
            ekip = form.save()
            messages.success(request,'Ekip başarılı bir şekilde güncellenmiştir.')
            return HttpResponseRedirect(ekip.proje.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    context = {
        'form':form,
        'value':'Güncelle',
    }
    return render(request,'proje/form.html',context)

def ekipDelete(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"ekip")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canDelete(yetki):
        messages.warning(request,"Ekip silme yetkiniz bulunmamaktadır.")
        return redirect("proje:index")
    #</Güvenlik>
    return redirect("{}/{}/delete".format(admin_ekip_url,id))

def ekipUyeCreate(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"ekip uye")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Ekip üyesi ekleme yetkiniz yoktur.")
        return redirect("proje:index")
    #</Güvenlik>
    if request.method == "POST":
        form = EkipUyeForm(request.POST or None)
        if form.is_valid():
            uye = form.save(commit=False)
            ekip = get_object_or_404(Ekip,id = id)
            uye.ekip = ekip
            ekipUyeler = EkipUye.objects.filter(ekip = ekip)
            for i in ekipUyeler:
                print(i,uye, i == uye)
                if i.calisan == uye.calisan:
                    messages.warning(request,"Bu kullanıcı zaten bu ekipte mevcut. Tekrar ekleyemezsiniz.")
                    return HttpResponseRedirect(reverse("proje:ekipUyeCreate",kwargs={'id':id}))
            uye.save()
            messages.success(request,"Ekip üyesi eklendi")
            return HttpResponseRedirect(reverse("proje:detail",kwargs={'slug':uye.ekip.proje.slug}))
        else:
            messages.warning(request,"Zorunlu alanları doldurunuz")
    else:
        form = EkipUyeForm()

    context = {
        'form':form,
        'value':'Üye Ekle'
    }
    return render(request,"proje/form.html",context)

def ekipUyeUpdate(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"ekip uye")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canChange(yetki):
        messages.warning(request,"Ekip üyelerini güncelleme yetkiniz yoktur.")
        return redirect("proje:index")
    #</Güvenlik>
    ekipUye = get_object_or_404(EkipUye,id=id)
    form = EkipUyeForm(request.POST or None,instance=ekipUye)
    if request.method == "POST":
        if form.is_valid():
            uye = form.save()
            messages.success(request,'Ekip üye başarılı bir şekilde güncellenmiştir.')
            return HttpResponseRedirect(uye.ekip.proje.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    context = {
        'form':form,
        'value':'Güncelle',
    }
    return render(request,'satim/form.html',context)

def ekipUyeDelete(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"ekip uye")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canDelete(yetki):
        messages.warning(request,"Ekip üyesi silme yetkiniz bulunmamaktadır.")
        return redirect("proje:index")
    #</Güvenlik>
    return redirect("{}/{}/delete".format(admin_ekipuye_url,id))

def talepDetail(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"talep")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if not canView(yetki):
        messages.warning(request,"Talep bilgilerine erişim yetkiniz yoktur.")
        return redirect("proje:index")
        
    #</Güvenlik>
    talep = get_object_or_404(Talep,id = id)
    if request.method == "POST":
        if request.POST.get("kabul"):
            talep.kabulDurumu = True
            talep.save()
            messages.success(request,"Talp Onaylandı.")
        elif request.POST.get("red"):
            talep.kabulDurumu = False
            talep.save()
            messages.success(request,"Talp Reddedildi.")
    context = {
        'talep':talep,
    }
    return render(request,"proje/talepdetay.html",context)

def talepCreate(request,slug):
    #<Güvenlik>
    yetki = getAuthorization(request,"talep")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Talep oluşturma yetkiniz yoktur.")
        return redirect("proje:index")
    #</Güvenlik>
    if request.method == "POST":
        form = TalepForm(request.POST or None)
        if form.is_valid():
            talep = form.save(commit=False)
            calisan = get_object_or_404(Calisan,user = request.user)
            proje = get_object_or_404(Proje,slug = slug)
            talep.calisan = calisan
            talep.proje = proje
            talep.save()
            messages.success(request,"Talep başarılı şekilde oluşturuldu.")
            return HttpResponseRedirect(reverse("proje:index"))
        else:
            messages.warning(request,"Zorunlu alanları dolurunuz.")
    else:
        form = TalepForm()
    context = {
        'form':form,
        'value':'Talep Oluştur'
    }
    return render(request,"proje/form.html",context)