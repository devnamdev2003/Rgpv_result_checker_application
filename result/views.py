from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import Data
from bs4 import BeautifulSoup


def captha(text):
    HtmlCode = text.split(" ")
    for i in HtmlCode:
        if 'src="CaptchaImage.axd?guid=' in i:
            url = 'http://result.rgpv.ac.in/result/'+i[5:-1]
            print(url)
            return url


def index(request):
    url = "http://result.rgpv.ac.in/result/ProgramSelect.aspx"
    global s
    s = requests.session()
    data = {
        '__EVENTTARGET': 'radlstProgram$1',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS':'',
        '__VIEWSTATE': '/wEPDwULLTE2MzgyNTE0ODQPZBYCAgMPZBYGAgEPZBYCAgEPEGRkFgBkAgMPZBYCAgEPEGRkFgBkAgUPZBYCAgEPEGRkFgBkZJOEN/LV22cCKi2fsiTS1sXh3GvP',
        '__VIEWSTATEGENERATOR': 'F697B5F5',
        '__EVENTVALIDATION': '/ wEWRAKGmcvHDAKdlJCkBQKclOCnBQKZlJCkBQKclJCkBQKelOSnBQKdlNynBQKblJCkBQKYlJCkBQKKlJCkBQKdlNCnBQKclNCnBQKclNynBQKclOSnBQKflJCkBQKelOCnBQKZlNynBQKclNinBQKZlOSnBQKelJCkBQKelNinBQKblNynBQKS+7rKCQLErciPDwLFrbiMDwLArciPDwLFrciPDwLHrbyMDwLErYSMDwLCrciPDwLBrciPDwLTrciPDwLErYiMDwLFrYiMDwLFrYSMDwLFrbyMDwLGrciPDwLHrbiMDwLArYSMDwLFrYCMDwLArbyMDwLHrciPDwLHrYCMDwLCrYSMDwLLwuLhAwK8gsyWBAK9gryVBAK4gsyWBAK9gsyWBAK/griVBAK8goCVBAK6gsyWBAK5gsyWBAKrgsyWBAK8goyVBAK9goyVBAK9goCVBAK9griVBAK+gsyWBAK/gryVBAK4goCVBAK9goSVBAK4griVBAK/gsyWBAK/goSVBAK6goCVBAKz7eb4CAKkr9z4AV+ftsFVe2Vtz/CzBT/HcCZU9/Wj',
        'radlstProgram': 24,
    }
    response = s.post(url, data=data)
    print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    global viewstate
    viewstate = soup.find('input', id='__VIEWSTATE').get('value')
    global eventvalidation
    eventvalidation = soup.find('input', id='__EVENTVALIDATION').get('value')
    text = soup.prettify()
    # print(text)
    captha0 = captha(text)
    return render(request, "result/index.html", {'link': captha0})


def marks(request):
    if request.method == 'POST':
        roll_number = request.POST['roll']
        semester = request.POST['sem']
        captcha = request.POST['cap']
        data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': '56D9EF13',
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$ContentPlaceHolder1$txtrollno': roll_number,
            'ctl00$ContentPlaceHolder1$drpSemester': semester,
            'ctl00$ContentPlaceHolder1$rbtnlstSType': 'G',
            'ctl00$ContentPlaceHolder1$TextBox1': captcha,
            'ctl00$ContentPlaceHolder1$btnviewresult': 'View Result'
        }
        r = s.post('http://result.rgpv.ac.in/result/BErslt.aspx', data=data)
        data = r.text
        data = data.replace("../CSS/resultsCSS.css",
                            "http://result.rgpv.ac.in/CSS/resultsCSS.css")
        data = data.replace("../images/logo.png",
                            "http://result.rgpv.ac.in/images/logo.png")
        data = data.replace("ProgramSelect.aspx",
                            "/")
        if("JavaScript>alert(" in data):
            return render(request, "result/error.html")
        else:
            with open('./result/templates/result/result.html', 'w') as f:
                f.write(data)
            soup = BeautifulSoup(data, 'html5lib')
            sgpa = soup.find(
                'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblSGPA'}).text
            cgpa = soup.find(
                'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblcgpa'}).text
            result = soup.find(
                'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblResultNewGrading'}).text
            roll = soup.find(
                'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblRollNoGrading'}).text
            name = soup.find(
                'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblNameGrading'}).text
            branch = soup.find(
                'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblBranchGrading'}).text
            sem = soup.find(
                'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblSemesterGrading'}).text

            name = name.replace(" ", "")
            sgpa = sgpa.replace(" ", "")
            cgpa = cgpa.replace(" ", "")
            result = result.replace(" ", "")
            branch = branch.replace(" ", "")
            roll = roll.replace(" ", "")
            sem = sem.replace(" ", "")
            sget = Data.objects.all()
            check = False
            for sdata in sget:
                if(sdata.name == name):
                    break
                else:
                    check = True
                    break
            if(check):
                r = Data(name=name, roll=roll,   branch=branch,
                         sem=sem, sgpa=sgpa, cgpa=cgpa, result=result)
                r.save()
                print("not present")
            else:
                print("present")

            return render(request, "result/result.html")
