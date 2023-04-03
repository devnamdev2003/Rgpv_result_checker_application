# Import necessary libraries
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import Data
from bs4 import BeautifulSoup


# Define a function to extract the captcha image URL from the HTML code
def captha(text):

    # Split the HTML response into a list of strings
    HtmlCode = text.split(" ")
    for i in HtmlCode:

        # Check if the string contains the captcha image URL
        if 'src="CaptchaImage.axd?guid=' in i:

            # Extract the URL and return it
            url = 'http://result.rgpv.ac.in/result/'+i[5:-1]
            return url

# Define the main view of the Django application


def index(request):

    # URL of the RGPV result website
    url = "http://result.rgpv.ac.in/result/ProgramSelect.aspx"

    # Create a session object to maintain state across requests
    global s
    s = requests.session()

    # Set a dictionary named "data" that contains various data to be posted to the URL
    data = {
        '__EVENTTARGET': 'radlstProgram$1',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '/wEPDwULLTE2MzgyNTE0ODQPZBYCAgMPZBYGAgEPZBYCAgEPEGRkFgBkAgMPZBYCAgEPEGRkFgBkAgUPZBYCAgEPEGRkFgBkZJOEN/LV22cCKi2fsiTS1sXh3GvP',
        '__VIEWSTATEGENERATOR': 'F697B5F5',
        '__EVENTVALIDATION': '/ wEWRAKGmcvHDAKdlJCkBQKclOCnBQKZlJCkBQKclJCkBQKelOSnBQKdlNynBQKblJCkBQKYlJCkBQKKlJCkBQKdlNCnBQKclNCnBQKclNynBQKclOSnBQKflJCkBQKelOCnBQKZlNynBQKclNinBQKZlOSnBQKelJCkBQKelNinBQKblNynBQKS+7rKCQLErciPDwLFrbiMDwLArciPDwLFrciPDwLHrbyMDwLErYSMDwLCrciPDwLBrciPDwLTrciPDwLErYiMDwLFrYiMDwLFrYSMDwLFrbyMDwLGrciPDwLHrbiMDwLArYSMDwLFrYCMDwLArbyMDwLHrciPDwLHrYCMDwLCrYSMDwLLwuLhAwK8gsyWBAK9gryVBAK4gsyWBAK9gsyWBAK/griVBAK8goCVBAK6gsyWBAK5gsyWBAKrgsyWBAK8goyVBAK9goyVBAK9goCVBAK9griVBAK+gsyWBAK/gryVBAK4goCVBAK9goSVBAK4griVBAK/gsyWBAK/goSVBAK6goCVBAKz7eb4CAKkr9z4AV+ftsFVe2Vtz/CzBT/HcCZU9/Wj',
        'radlstProgram': 24,
    }

    # Send a POST request to the RGPV result website and extract the viewstate and eventvalidation fields from the response
    response = s.post(url, data=data)

    # Create a BeautifulSoup object to parse the HTML response
    soup = BeautifulSoup(response.text, 'lxml')

    # Get the value of the "__VIEWSTATE" ,"__EVENTVALIDATION" input field and store it in a global variable named "viewstate","eventvalidation"
    global viewstate
    viewstate = soup.find('input', id='__VIEWSTATE').get('value')
    global eventvalidation
    eventvalidation = soup.find('input', id='__EVENTVALIDATION').get('value')

    text = soup.prettify()

    # Extract the captcha image URL from the response HTML using the captha() function and pass it to the index.html template
    captha0 = captha(text)
    return render(request, "result/index.html", {'link': captha0})


# Define a view to handle form submission and display the result
def marks(request):
    print(viewstate)
    # check if request method is POST
    if request.method == 'POST':

        # Get the roll number, semester, and captcha entered by the user
        roll_number = request.POST['roll']
        semester = request.POST['sem']
        captcha = request.POST['cap']

        # create a dictionary with form data
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

        # Send a POST request to the RGPV result website with the form data and extract the result HTML from the response
        r = s.post('http://result.rgpv.ac.in/result/BErslt.aspx', data=data)
        data = r.text

        # Replace the relative URLs in the result HTML with absolute URLs and write it to a file
        data = data.replace("../CSS/resultsCSS.css",
                            "http://result.rgpv.ac.in/CSS/resultsCSS.css")
        data = data.replace("../images/logo.png",
                            "http://result.rgpv.ac.in/images/logo.png")
        data = data.replace("ProgramSelect.aspx",
                            "/")

        # check if response HTML contains an alert message (i.e. invalid captcha)
        if("JavaScript>alert(" in data):
            # if alert message is present, render error page
            return render(request, "result/error.html")

        # if alert message is not present, write response HTML to file and parse data
        else:

            # Extract the SGPA, CGPA, and result status from the result HTML using BeautifulSoup and pass them to the result.html template
            with open('./result/templates/result/result.html', 'w') as f:
                f.write(data)

            # # this code is for store result in database

            
            # # get relevant data from parsed HTML
            # soup = BeautifulSoup(data, 'html5lib')
            # sgpa = soup.find(
            #     'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblSGPA'}).text
            # cgpa = soup.find(
            #     'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblcgpa'}).text
            # result = soup.find(
            #     'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblResultNewGrading'}).text
            # roll = soup.find(
            #     'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblRollNoGrading'}).text
            # name = soup.find(
            #     'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblNameGrading'}).text
            # branch = soup.find(
            #     'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblBranchGrading'}).text
            # sem = soup.find(
            #     'span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblSemesterGrading'}).text

            # # clean up data (remove spaces)
            # name = name.replace(" ", "")
            # sgpa = sgpa.replace(" ", "")
            # cgpa = cgpa.replace(" ", "")
            # result = result.replace(" ", "")
            # branch = branch.replace(" ", "")
            # roll = roll.replace(" ", "")
            # sem = sem.replace(" ", "")

            # # check if data already exists in database
            # sget = Data.objects.all()
            # check = False
            # for sdata in sget:
            #     if(sdata.name == name):
            #         break
            #     else:
            #         check = True
            #         break
            # if(check):
            #     r = Data(name=name, roll=roll,   branch=branch,
            #              sem=sem, sgpa=sgpa, cgpa=cgpa, result=result)
            #     r.save()
            #     print("not present")
            # else:
            #     print("present")

            return render(request, "result/result.html")
