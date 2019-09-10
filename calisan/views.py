from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from .models import *
from .form import *
from django.contrib import messages
from django.contrib.auth.models import User
from proje.models import *

# Create your views here.

admin_url = "/admin/calisan/calisan"
admin_maas_url = "/admin/calisan/maasodeme"
admin_kart_url = "/admin/calisan/kart"
def calisanIndex(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"calisan")#25 permission idsi dir.
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if canView(yetki):
        calisanlar = Calisan.objects.all()
    else:
        calisanlar = Calisan.objects.filter(user = request.user)
    #</Güvenlik>
    yetkiMaas = getAuthorization(request,"maas odeme")
    yetkiSgk = getAuthorization(request,"sgk prim")
    yetkiIzin = getAuthorization(request,"izin")
    yetkiKart = getAuthorization(request,"kart")
    context = {
        'calisanlar':calisanlar,
        'canAdd':canAdd(yetki),
        'canAddMaas':canAdd(yetkiMaas),
        'canAddSgk':canAdd(yetkiSgk),
        'canAddIzin':canAdd(yetkiIzin),
        'canAddKart':canAdd(yetkiKart),
    }
    return render(request,"calisan/index.html",context)
    
def calisanDetail(request,slug):
    #<Güvenlik>
    yetki = getAuthorization(request,"calisan")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    if not canView(yetki):
        messages.warning(request,"Çalışan bilgilerine erişim yetkiniz yoktur.")
        return redirect("calisan:index")
        
    #</Güvenlik>
    #yetkiler
    yetkiMaas = getAuthorization(request,"maas odeme")
    yetkiSgk = getAuthorization(request,"sgk prim")
    yetkiIzin = getAuthorization(request,"izin")
    yetkiKart = getAuthorization(request,"kart")
    yetkiEkipUye = getAuthorization(request,"ekip uye")
    yetkiTalep = getAuthorization(request,"talep")

    sgkprimler = False
    maaslar = False
    izinler = False
    kartlar = False
    ekipUyeler = False
    projeTalepler = False
    calisan = get_object_or_404(Calisan,slug = slug)
    if canView(yetkiSgk):
        sgkprimler = SgkPrim.objects.filter(calisan=calisan)
    if canView(yetkiMaas):
        maaslar = MaasOdeme.objects.filter(calisan=calisan)
    if canView(yetkiIzin):
        izinler = Izin.objects.filter(calisan=calisan)
    if canView(yetkiKart):
        kartlar = Kart.objects.filter(calisan=calisan)
    if canView(yetkiEkipUye):
        ekipUyeler = EkipUye.objects.filter(calisan=calisan)
    if canView(yetkiTalep):
        projeTalepler = Talep.objects.filter(calisan=calisan)
    elif calisan.user == request.user:
        projeTalepler = Talep.objects.filter(calisan=calisan)

    
    context = {
        'calisan':calisan,
        'sgkprimler':sgkprimler,
        'maaslar':maaslar,
        'izinler':izinler,
        'kartlar':kartlar,
        'ekipUyeler':ekipUyeler,
        'projeTalepler':projeTalepler,
        #yetkiler
        'canAdd':canAdd(yetki),
        'canChange':canChange(yetki),
        'canAddMaas':canAdd(yetkiMaas),
        'canAddSgk':canAdd(yetkiSgk),
        'canAddIzin':canAdd(yetkiIzin),
        'canChangeIzin':canChange(yetkiIzin),
        'canAddKart':canAdd(yetkiKart),
        'canDeleteKart':canDelete(yetkiKart),
    }
    return render(request,"calisan/calisandetay.html",context)

def calisanCreate(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"calisan")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Çalışan ekleme yetkiniz yoktur.")
        return redirect("calisan:index")
    #</Güvenlik>
    if request.method == "POST":
        user_form = UserForm(request.POST or None)
        calisan_form = CalisanForm(request.POST or None)
        if user_form.is_valid() and calisan_form.is_valid():
            user = user_form.save(commit = False)
            #user.set_password('cde12345')
            print('girdi1***********************',user_form.cleaned_data['password'])
            if True:#Şifrenin düzgün girildiğinin kontrolü
                print('girdi2***********************')
                #user.set_password(user.password)
                calisan = calisan_form.save(commit = False)
                #user.save()
                user = User.objects.create_user(user_form.cleaned_data['username'],user_form.cleaned_data['email'],user_form.cleaned_data['password'])
                user.is_staff = user_form.cleaned_data['is_staff']
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.groups.set(user_form.cleaned_data['groups']) 
                user.user_permissions.set(user_form.cleaned_data['user_permissions'])
                user.save()
                calisan.user = user
                calisan.save()
                messages.success(request,'Çalışan ve user başarılı şekilde oluşturuldu')
            else:
                print('girdi3***********************')
                messages.warning(request,'Şifreyi düzgün girin en az 8 karakter')
        else:
            print('girdi4***********************')
            messages.warning(request,'Lütfen zorunlu alanları dolurunuz.')
    else:
        print('girdi5***********************')
        user_form = UserForm()
        calisan_form = CalisanForm()
    context = {
        'userform':user_form,
        'calisanForm':calisan_form,
        'value':'Ekle',
    }
    return render(request,"calisan/form.html",context)
    #return redirect("{}/add/".format(admin_url))

def calisanUpdate(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"calisan")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canChange(yetki):
        messages.warning(request,"Çalışan güncelleme yetkiniz yoktur.")
        calisan = get_object_or_404(Calisan,id=id)
        return HttpResponseRedirect(calisan.get_absolute_url())
    #</Güvenlik>
    calisan = get_object_or_404(Calisan,id=id)
    calisanForm = CalisanForm(request.POST or None,instance=calisan)
    if request.method == "POST":
        if calisanForm.is_valid():
            calisan = calisanForm.save()
            messages.success(request,'Çalışan başarılı bir şekilde güncellenmiştir.')
            return HttpResponseRedirect(calisan.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    context = {
        'calisanForm':calisanForm,
        'value':'Güncelle',
    }
    return render(request,'calisan/form.html',context)

def calisanDelete(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"calisan")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canDelete(yetki):
        messages.warning(request,"Calışanı silme yetkiniz bulunmamaktadır.")
        return redirect("calisan:index")
    #</Güvenlik>
    return redirect("{}/{}/delete".format(admin_url,id))

def calisanPassive(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"calisan")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canChange(yetki):
        messages.warning(request,"Çalışan güncelleme yetkiniz yoktur.")
        calisan = get_object_or_404(Calisan,id=id)
        return HttpResponseRedirect(calisan.get_absolute_url())
    #</Güvenlik>
    calisan = get_object_or_404(Calisan,id=id)
    user = get_object_or_404(User,id=calisan.user.id)
    user.is_active = False
    user.save()
    messages.success(request,"Kullanıcı engellendi.")
    return HttpResponseRedirect(calisan.get_absolute_url())

def calisanActive(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"calisan")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif canChange:
        messages.warning(request,"Çalışan güncelleme yetkiniz yoktur.")
        calisan = get_object_or_404(Calisan,id=id)
        return HttpResponseRedirect(calisan.get_absolute_url())
    #</Güvenlik>
    calisan = get_object_or_404(Calisan,id=id)
    user = get_object_or_404(User,id=calisan.user.id)
    user.is_active = True
    user.save()
    messages.success(request,"Kullanıcı aktifleştirildi.")
    return HttpResponseRedirect(calisan.get_absolute_url())

def maasCreate(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"maas odeme")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Maaş ödeme yetkiniz yoktur.")
        return redirect("calisan:index")
    #</Güvenlik>
    if request.method == "POST":
        
        maasForm = MaasForm(request.POST or None)
        
        if maasForm.is_valid():
            if maasForm.cleaned_data["tumMaas"] == True:
                calisanlar = Calisan.objects.all()
                for i in calisanlar:
                    MaasOdeme.objects.create(calisan=i).save()
                messages.success(request,"Tüm çalışanların maaşları ödendi.")
                return HttpResponseRedirect("/calisan")
            else:
                maasForm.save()
                messages.success(request,"{} ın maaşı ödendi.".format(maasForm.cleaned_data["calisan"]))
                return HttpResponseRedirect(Calisan.objects.get(id = maasForm.cleaned_data["calisan"].id).get_absolute_url())
        else:
            message.warning(request,"Zorunlu alanları doldurun.")
    else:
        maasForm = MaasForm()
    context = {
        'maasForm':maasForm,
        'value':'Maaş Öde',
    }
    return render(request,"calisan/form.html",context)

def sgkprimCreate(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"sgk prim")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Prim ödeme yetkiniz yoktur.")
        return redirect("calisan:index")
    #</Güvenlik>
    if request.method == "POST":
        
        sgkPrimForm = SgkPrimForm(request.POST or None)
        
        if sgkPrimForm.is_valid():
            if sgkPrimForm.cleaned_data["tumPrim"] == True:
                calisanlar = Calisan.objects.all()
                for i in calisanlar:
                    SgkPrim.objects.create(calisan=i).save()
                messages.success(request,"Tüm çalışanların sgk primleri ödendi.")
                return HttpResponseRedirect("/calisan")
            else:
                sgkPrimForm.save()
                messages.success(request,"{} ın sgk primi ödendi.".format(sgkPrimForm.cleaned_data["calisan"]))
                return HttpResponseRedirect(Calisan.objects.get(id = sgkPrimForm.cleaned_data["calisan"].id).get_absolute_url())
        else:
            message.warning(request,"Zorunlu alanları doldurun.")
    else:
        sgkPrimForm = SgkPrimForm()
    context = {
        'sgkPrimForm':sgkPrimForm,
        'value':'Sgk Prim Öde',
    }
    return render(request,"calisan/form.html",context)

def izinCreate(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"izin")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"İzin verme yetkiniz yoktur.")
        return redirect("calisan:index")
    #</Güvenlik>
    if request.method == "POST":
        
        izinForm = IzinForm(request.POST or None)
        
        if izinForm.is_valid():
            if izinForm.cleaned_data["tumIzin"] == True:
                calisanlar = Calisan.objects.all()
                resmiTatil = Kategori.objects.get(id = 5)
                for i in calisanlar:
                    Izin.objects.create(calisan=i,kategori=resmiTatil,izinTarihi=izinForm.cleaned_data["izinTarihi"],gun=izinForm.cleaned_data["gun"]).save()
                messages.success(request,"Tüm çalışanlara resmi izin verildi.")
                return HttpResponseRedirect("/calisan")
            else:
                izinForm.save()
                messages.success(request,"{} a izin verildi.".format(izinForm.cleaned_data["calisan"]))
                return HttpResponseRedirect(Calisan.objects.get(id = izinForm.cleaned_data["calisan"].id).get_absolute_url())
        else:
            message.warning(request,"Zorunlu alanları doldurun.")
    else:
        izinForm = IzinForm()
    context = {
        'izinForm':izinForm,
        'value':'İzin Ver',
    }
    return render(request,"calisan/form.html",context)
def izinUpdate(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"izin")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canChange(yetki):
        messages.warning(request,"İzin güncelleme yetkiniz yoktur.")
        izin = get_object_or_404(Izin,id=id)
        return HttpResponseRedirect(izin.calisan.get_absolute_url())
    #</Güvenlik>
    izin = get_object_or_404(Izin,id=id)
    izinForm = IzinYeniForm(request.POST or None,instance=izin)
    if request.method == "POST":
        if izinForm.is_valid():
            izin = izinForm.save()
            messages.success(request,'İzin başarılı bir şekilde güncellenmiştir.')
            return HttpResponseRedirect(izin.calisan.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    context = {
        'izinForm':izinForm,
        'value':'Güncelle',
    }
    return render(request,'calisan/form.html',context)
def kartCreate(request):
    #<Güvenlik>
    yetki = getAuthorization(request,"kart")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canAdd(yetki):
        messages.warning(request,"Kart oluşturma yetkiniz yoktur.")
        return redirect("calisan:index")
    #</Güvenlik>
    if request.method == "POST":
        kartForm = KartForm(request.POST or None)
        if kartForm.is_valid():
            kart = kartForm.save()
            messages.success(request,'Kart atama işlemi başarılı.')
            return HttpResponseRedirect(kart.calisan.get_absolute_url())
        else:
            messages.warning(request,'Bir hata oluştu. Lütfen zorunlu alanları doldurunuz.')
    else:
        kartForm = KartForm()
    context = {
        'kartForm':kartForm,
        'value':'Kart Ata',
    }
    return render(request,"calisan/form.html",context)

def kartDelete(request,id):
    #<Güvenlik>
    yetki = getAuthorization(request,"kart")
    if yetki == -1:
        messages.warning(request,"Erişim için giriş yapınız.")
        return redirect("/admin")
    elif not canDelete(yetki):
        messages.warning(request,"Kart silme yetkiniz bulunmamaktadır.")
        return redirect("calisan:index")
    #</Güvenlik>
    return redirect("{}/{}/delete".format(admin_kart_url,id))