from django.shortcuts import render,redirect
import ast,base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend  # Add this import
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from .models import SignUP
#################################ecnode and decode########################
from PIL import Image
import os
import sys
import os.path
from os import path

def convertToRGB(img):
	try:
		rgba_image = img
		rgba_image.load()
		background = Image.new("RGB", rgba_image.size, (255, 255, 255))
		background.paste(rgba_image, mask = rgba_image.split()[3])
		return background
	except Exception as e:
		print("[red]Couldn't convert image to RGB [/red]- %s"%e)


def getPixelCount(img):
	width, height = Image.open(img).size
	return width*height


def encodeImage(image,message,filename):
		try:
			width, height = image.size
			pix = image.getdata()

			current_pixel = 0 #start from beginning
			tmp=0 #counter

			x=0
			y=0
			for ch in message:
				binary_value = format(ord(ch), '08b')
				
				# For each character, get 3 pixels at a time
				p1 = pix[current_pixel]
				p2 = pix[current_pixel+1]
				p3 = pix[current_pixel+2]

				three_pixels = [val for val in p1+p2+p3] #make them as one list

				for i in range(0,8):
					current_bit = binary_value[i]

					# 0 - Even
					# 1 - Odd
					if current_bit == '0':
						if three_pixels[i]%2!=0:
							three_pixels[i]= three_pixels[i]-1 if three_pixels[i]==255 else three_pixels[i]+1
					elif current_bit == '1':
						if three_pixels[i]%2==0:
							three_pixels[i]= three_pixels[i]-1 if three_pixels[i]==255 else three_pixels[i]+1

				current_pixel+=3 #take next set of pixels
				tmp+=1 #increment counter

				#Set 9th value
				if(tmp==len(message)):
					# Make as 1 (odd) - stop reading
					if three_pixels[-1]%2==0:
						three_pixels[-1]= three_pixels[-1]-1 if three_pixels[-1]==255 else three_pixels[-1]+1
				else:
					# Make as 0 (even) - continue reading
					if three_pixels[-1]%2!=0:
						three_pixels[-1]= three_pixels[-1]-1 if three_pixels[-1]==255 else three_pixels[-1]+1


				three_pixels = tuple(three_pixels)
				
				st=0
				end=3

				for i in range(0,3): #modifying pixels 
					image.putpixel((x,y), three_pixels[st:end])
					st+=3
					end+=3

					if (x == width - 1):
						x = 0
						y += 1
					else:
						x += 1

			encoded_filename = filename.split('.')[0] + "-enc.png"
			image.save(encoded_filename)
			print("\n")
			print("[yellow]Original File: [u]%s[/u][/yellow]"%filename)
			print("[green]Image encoded and saved as [u][bold]%s[/green][/u][/bold]"%encoded_filename)

		except Exception as e:
			print("[red]An error occured - [/red]%s"%e)
			sys.exit(0)



def decodeImage(image):
		try:
			pix = image.getdata()
			current_pixel = 0
			decoded=""
			while True:
				# Get 3 pixels each time
				binary_value=""
				p1 = pix[current_pixel]
				p2 = pix[current_pixel+1]
				p3 = pix[current_pixel+2]
				three_pixels = [val for val in p1+p2+p3] #make them as one list

				for i in range(0,8):
					if three_pixels[i]%2==0:
						# add 0 to msg
						binary_value+="0"
					elif three_pixels[i]%2!=0:
						# add 1 to msg
						binary_value+="1"


				#Convert binary value to ascii and add to string
				binary_value.strip() #strip removes spaces
				ascii_value = int(binary_value,2)
				decoded+=chr(ascii_value)
				current_pixel+=3

				if three_pixels[-1]%2!=0:
					#last letter termination
					break

			# print("Decoded: %s"%decoded)
			return decoded
		except Exception as e:
			print("[red]An error occured - [/red]%s"%e)
			sys.exit()



#################################encode and decode########################
# Create your views here.
def index(request):
    return render(request,'index.html')   
def generate(request):
    return render(request,'generate.html')   
def home(request):
    if(request.user.is_anonymous):
        return render(request,'login.html')
    return render(request,'home.html')   
def profile(request):
    if(request.user.is_anonymous):
        return render(request,'login.html')
    return render(request,'profile.html')   
def passwords(request):
    if(request.user.is_anonymous):
        return render(request,'login.html')
    passwords = ast.literal_eval(base64.b64decode(list(SignUP.objects.filter(uname=uname).values_list())[0][-1].encode('ascii')).decode('utf-8'))
    print(type(passwords))
    return render(request,'passwords.html',{'passwords':passwords})   
def store(request):
    if(request.user.is_anonymous):
        return render(request,'login.html')
    x = Image.open("C:/Users/DELL/Desktop/website/images/hacker.jpg")
    y = x.copy()
    decoded = ast.literal_eval(base64.b64decode(list(SignUP.objects.filter(uname=uname).values_list())[0][-1].encode('ascii')).decode('utf-8'))
    context = {'passwords':decoded} 
    modify =  decoded
    if request.method=='POST':
            l=[ request.POST.get('1'),
            request.POST.get('2'),
            request.POST.get('3'),
            request.POST.get('4'),
            request.POST.get('5'),
            request.POST.get('6'),]  
            print(l)
            c=0 
            for i in modify.keys():
                if(l[c] != 'None'):
                    modify.update({i:l[c]})
                c+=1
            # print(modify) 
            for i in modify.keys():
                if modify[i]=='None':
                    modify[i]=None
            print(modify)
            encodeImage(y,base64.b64encode(str(modify).encode('utf-8')).decode('ascii'),x.filename)
            SignUP.objects.filter(uname=uname).update(passwords=base64.b64encode(str(modify).encode('utf-8')).decode('ascii'))  
            SignUP.objects.filter(uname=uname).update(image='hacker-enc.png')
            return render(request,'storepasswords.html',{'passwords':modify})   
    return render(request,'storepasswords.html',context)   
global uname    
def loginUser(request):
    if(request.method=='POST'):
        global uname
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        print(uname,pwd)
        user= authenticate(username=uname,password=pwd)
        if(user is not None):
            login(request,user)
            # return render(request,'home.html',{'name':uname})
            return redirect('/home')
        else:
            return render(request,'login.html',{'msg':'Invalid Credentials!'})
    return render(request,'login.html')
def signupUser(request):
    if(request.method=='POST'):
        fname= request.POST.get('fname')
        lname= request.POST.get('lname')
        global uname
        uname= request.POST.get('username')
        # email= request.POST.get('email')
        pwd= request.POST.get('password')
        print(uname,pwd,fname,lname)
        user=User.objects.create_user(username=uname,password=pwd)
        user.first_name=fname
        user.last_name=lname
        user.save()
        user = SignUP(uname=uname)
        user.save()
        return render(request,'home.html',{'name':uname})
    return render(request,'signup.html')
def logoutUser(request):
    logout(request)
    return render(request,'index.html')  