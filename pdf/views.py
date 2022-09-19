import mimetypes
from django.http.response import HttpResponse
import os, io
# Create your views here.
from django.shortcuts import render
import requests
from pdf2image import convert_from_path
from django.http import FileResponse
import os
from django.conf import settings
from django.http import HttpResponse, Http404


def Get_img(request, name):
        
    page = f"{name}.pdf"
    pop = r"Library\bin"
    print(pop)
    # page = convert_from_path(pdf_path=page, poppler_path=pop, last_page=1)
    page = convert_from_path(page, 500)
    for i in page:
        img_name = f"{name}s.jpg"
        rasm = i.save(img_name, "JPEG")
        
def show_pdf(request, link, id):
    # print(link)
    upd = requests.get(f"https://ziyodullo.makkapoya.uz/Search_projects/kitoblar/bookapi.php?id={id}&get=okey")
    data = upd.json()
    if data['Link'] == "non":
        url = f"https://api.telegram.org/bot5280245763:AAGEDFjv4CH28m3_x-ELbcp8S9ra9w0JWlc/getFile?file_id={link}"
        url2 = "https://api.telegram.org/file/bot5280245763:AAGEDFjv4CH28m3_x-ELbcp8S9ra9w0JWlc/"
        get = requests.get(url)
        # print(get.json())
        ll = get.json()
        ll = ll['result']['file_path']
        data = requests.get(f"{url2}{ll}")
        upd = requests.get(f"https://ziyodullo.makkapoya.uz/Search_projects/kitoblar/bookapi.php?id={id}&link={url2}{ll}")
    else:
        # print("salom")
        data = requests.get(data['Link'])
    return FileResponse(data,  content_type='application/pdf')


def download(request, name):
    file_path = os.path.join(settings.MEDIA_ROOT, f'{name}')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404



def GetImg(request):
    if request.method == "GET":
        return render(request, 'getbook.html')
    else:
        book = request.POST['kitob']
        # print(book)
        url1 = "https://api.telegram.org/bot5280245763:AAGEDFjv4CH28m3_x-ELbcp8S9ra9w0JWlc/getFile?file_id="
        url2 = "https://api.telegram.org/file/bot5280245763:AAGEDFjv4CH28m3_x-ELbcp8S9ra9w0JWlc/"
        get = requests.get(f"https://ziyodullo.makkapoya.uz/Search_projects/kitoblar/api.php?title={book}")
        ll = get.json()
        if ll[0]['ok']:
            # name = ll[1]['Title']
            # type = ll[1]['Type']
            # ll = ll[1]['Link']
            # if type == "application/pdf":
            #     get = requests.get(f"{url1}{ll}")
            #     ll = get.json()
            #     if ll["ok"] == True:
            #         ll = ll['result']['file_path']
            #         get = requests.get(f"{url2}{ll}")
            #         # print(ll)
            #         name1 = name.split(" ")
            #         # print(name[-1])
            #         open(f"kitob.pdf", "wb").write(get.content)
            #         # sleep(3)
            #         # Get_img(name[-1])
            #         # page = f"lolasi.pdf.pdf"
            #         # pop = r"Library\bin"
            #         # page = convert_from_path(pdf_path=page, poppler_path=pop, first_page=0, last_page=1)
            #         # for i in page:
            #         #     img_name = f"wqwq.jpg"
            #         #     rasm = i.save(img_name, "JPEG")
            #         # print(name1[-1])
            #         # link = f"{url2}{ll}"
            #         # print(link)
            #         context = {
            #             "ok":True,
            #             "title":"kitob.pdf",
            #             "type":type,
            #             "size":"rasm",
            #             # "kitob":link
            #         }
            #     else:
            #         return render(request, 'page_not.html')
            # else:
            #         return render(request, 'page_not.html')
            # print(ll[3])
            return render(request, 'getbook.html', {'list':ll})


