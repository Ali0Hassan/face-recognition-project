import face_recognition as fr
import os
import cv2
import face_recognition        
import numpy as np
import base64
from io import BytesIO
from base64 import decodestring
import string #for the random generator  
import random  #for //  //      //


Rran = random.randrange(10)
S = Rran # number of characters in the string.
s = 2  
# call random.choices() string module to find the string in Uppercase + numeric data.  
Ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = s))  

def five_pics_max(ID,n):
    print('pathhhhhh after check 55 ',os.getcwd())
    names_list=[]
    for dirpath, dnames, fnames in os.walk("faces/"+ID):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
              if f.startswith(n+"-"):
                names_list.append(f.split('_')[0])
    if len((names_list))<5:
      return(True)
    else :
      return(False)


def remove_friend(ID,name):
  
  for dirpath, dnames, fnames in os.walk("faces/"+ID):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
              if f.startswith(name +"-"):
                os.remove("Q:\\GP\\faceD\\Run\\version 2_ actual use\\faces\\"+ ID+'\\'+f)
  return (print(name +" removed sucessfully"))


def image_check(base64_pics):
    check_jpg = base64.b64decode(base64_pics)   #** converting base64 into jpg image **#
    print('pathhhhhh image check',os.getcwd())
    os.chdir("./temp_check")

        #saving the image to start processing on them
    with open("ONE_face_test.jpg", "wb") as f:   #saving image
     f.write(check_jpg)
       
    img = cv2.imread("ONE_face_test.jpg")
    faces_in_each_img = len(face_recognition.face_encodings(img))
    laplacian_var = cv2.Laplacian(img,cv2.CV_64F).var()

    os.chdir('..')    #back again

    if faces_in_each_img != 1 or laplacian_var < 5:
        return (False)                                     #the pic is blury or there is NoFaces/ManyFaces
    else:
        return(True)

def ID_Check(ID):
  print('pathhhhhhID before check ',os.getcwd())
  id_list = os.listdir("./faces")
  if ID not in id_list:
    
    print('pathhhhhhID after check',os.getcwd())
    return("ID is unique")
  else:
  
    return("Existed ID")  


def Name_Check (ID,NAME):    
    names_list=[]
    
    for dirpath, dnames, fnames in os.walk("./faces/"+ID):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                names_list.append(f.split('-')[0])
    if NAME not in  names_list:
      return("name is unique")
    else:
      return("Existed name")  

               
def get_encoded_faces(ID_path):
    """
    looks through the faces folders and encodes all
    the faces
    :return: dict of (name, image encoded)
    """
    encoded = {} 
    for dirpath, dnames, fnames in os.walk(ID_path):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file(ID_path+ "/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split("_")[0]] = encoding      #name_0.jpg   name_1.jpg
    return encoded

def unknown_image_encoded(img):
    """
    encode a face given the file name
    """
    face = fr.load_image_file("/faces/"+ img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(ID, name , base64_im):   
 if Name_Check(ID,name) == "Existed name":

    requested_person = name
    requested_image = base64_im
    face_names = []
    requested_decoded = base64.b64decode(requested_image)

    faces = get_encoded_faces("./faces/"+ID)
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    os.chdir('..')
    with open("test.jpg", "wb") as save_test:   #saving image
     save_test.write(requested_decoded)


    img = cv2.imread("test.jpg", 1)
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img,face_locations)   #face_locations 
    
    for face_encoding in unknown_face_encodings:
                        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"
                         # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]    
        face_names.append(name.split('-')[0])

    # results 
    if requested_person not in face_names:
        return(print("Sorry, I couldn't find "+ requested_person))  
    else:
        return(print(requested_person+" is here"))
 else:
    return(print("name error,please try again"))
       
       
def new_friend (ID, name, new_base64):   
 new_face_name = name
  #checking whether it is a new user or not 
 print('pathhhhhh function',os.getcwd())


 if ID_Check(ID)== "ID is unique" and image_check(new_base64) == True: 
   print('pathhhhhh after first check ',os.getcwd())
   os.chdir("./faces/")    
   os.makedirs(ID)
   print('pathhhhhh after ID ',os.getcwd())
   os.chdir("./"+ID)

   new_face_jpg = base64.b64decode(new_base64)                                       #** converting base64 into jpg image **#
   with open(new_face_name + "-" + str(ran) + "_" + str(Ran)+".jpg", "wb") as fnew:   #saving image
     fnew.write(new_face_jpg)     
   return (print("saved successfully"))
   
 elif image_check(new_base64) == False:
   return(print("try to save a clear picture"))

 elif ID_Check(ID)== "Existed ID" and Name_Check(ID,name)== "name is unique" and image_check(new_base64)==True: 

   print('pathhhhhh after ID existed and name is unique ',os.getcwd())

   os.chdir("faces/"+ID)
   new_face_jpg = base64.b64decode(new_base64)                                        #** converting base64 into jpg image **#
   with open(new_face_name + "-" + str(ran) + "_" + str(Ran)+".jpg", "wb") as fnew:   #saving image
     fnew.write(new_face_jpg)     
   return (print("saved successfully"))

 elif ID_Check(ID) == "Existed ID" and Name_Check(ID,name)== "Existed name" and image_check(new_base64)==True and five_pics_max(ID,name) ==True:
    print('pathhhhhh after check ID&name&five ',os.getcwd())
    os.chdir("./faces/"+ ID) 
    new_face_jpg = base64.b64decode(new_base64)                                        #** converting base64 into jpg image **#
    with open(new_face_name + '-' + str(ran) + '_' + str(Ran)+'.jpg', 'wb') as fnew:   #saving image
      fnew.write(new_face_jpg)     

    return (print("saved successfully"))

 elif ID_Check(ID) == "Existed ID" and Name_Check(ID,name)== "Existed name" and image_check(new_base64)==True and five_pics_max(ID,name)==False:
    return(print(name+" have a maxmum number of photos")) 

 elif image_check(new_base64)==False:
    return(print("try to save a clear pictures"))


  # no face in the picture 
classify_face("0001","ali","/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAB4AIkDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD4u02ZpL5Y1BLE4AFeoaT4LZZIZWlaNjggA4rg/DujXC6lFcJEWUNk5Fdrq3i6aG4VArBoxn5RXuSatypHBGDu2V/HVjfWcyAufIXqa5rTZReSyAHdtHQ1oeKvGEup2ZR+WP6VzPhycweaZGyx4FRGVqbJv79kblvop1mGdycKnRc1y8dwLHUBEzFNpwCa29KvrmHVBESY4ZD1NUdZ0I3uvpFGwZeu6ueN29djWduW63NO7uRdRoNmPf1rM1LSZpFWSJiqLyQe9O1RbizuEtlQsynAxW1DZy/2ftdCG967I2jH3WZRm5Sszjri+uYVLrzxtZSOGX0NYOj3y2d49xBD5tszYaM9Yz6H2967O40kLuRuS3NYK6TNpGomSBAytwwboy+h9q20tZl21HTMLi6W5C4AOQuOK9D8K+NI5lNtcJsRRjdXG+XbfbIYYGYmbjy+6H0zW5L4VksdpI4bkkVzT5ZJJj0ejOsurqxu13I+7PvXJaxffY7pRbgnnmte20W3WzxFJiUjnmsi40i6urhWj+YIecd6why3BXizrfC0qS2rSOm1n7mtDWpI47M7to2+nes3S7W5vtPSKOLYUOGI/rVnxVopmtY4YyVmbAyK55b2LcrI42axkv7luNqZzkenrU39m2//AD3aukuvDzaHoPlvLmdhnd6Vw/8AZt//AM/Br0I00ZXvqeiaZ4itNNsWRolZlGKND1LTr5ria7jUFgcbqwVjS2vmDR5iPIyKvSaCNYiVoVMQzjHSuVpzVjS2ljz7xdffZr6QwJmAscYFW/CNu17MhdGEY5Jrv9S8DW8OmqkkYZtuSTVez04Q2ISFVixxnFXJx5OVbmEo2lddTmPHmoW2m3EHkjI4GV65qvpmoCRUuUJJ6D2qfxVaWIs2Mh33APWuattQWNo4ozgD+Gro0/d2DVXudnp7C61aEyldzN1Y12XiJbe2hWNNrccsteWwF5LhJN2HXkV0lxeyyWYyxJPvR7F8yZpFuKM3V2WLfKh5HQZritU1S681Sd2PQc1188X2qNsHB965udY7W4WKZcq5wCR0rtVguangS3k1LUlllG3Z93PU13/iC6kS18qAeZJjj2rldKsJ4SslrhQB1rpNB837ZFHdAMWcAlj2zXn1IXnzroD0MrSBI1vM80giPI+bv9PWqOn+JntNQFpG2xGONzfeP+FdLeeHX1fUEW2y0snoaxpPhvaSa5smvZUkVwjNGBtDZ9zzXPGKUteooJ3uasOvrou4o5Ejc57mtKx1qXUX86VNhXlW7H6ip734TssltCsv2lpWwrDjpWsngeD7XNpyXjrNHH/CvyZ9Otb8sIx5lubtX0Of1W6lvrSSOb5u6sOR+dcdsuf9quuuLiHR2ls5WHnR7g654PHWsL7cnoKUZT6Eyiuh6Smk2XiOyjaEqsyrxirll4bktNLyWAlQ/d9a8w0LXbnT7uPy59itWhrvxCuLNgVnJOcEVskpbEbHVXFnd3ULGU/LXB61dz6bIU3ELXUeDPGkWsyMl64WMD8Km8WafpeqQhrZ1ZgfrQ6etw3PNNQuY9Ttgu3P+171hXvhv+zcTGQh35GK7/S7O3huBBPhQW71U8VJZWshBbIA4xUxquMuWJTj3OTjmkRo2UkqOtdDY3C3FuSTwOtcVc6oIA6R5ZBW74Wl8xEDHCycV6CWnMZX6G5NHFhfKO7PUAVGdBiuJIpJhlFOa0LxLTT7GUCTdM3INY2k6pc3gMEisFBOGNc7kncr1Ohj00zWriyl2sO1ULaPUYdXt0lf+NR096d9nuNNcSxTse+3NbWh6hBcXkU07DzQw4P1rm9oiHHm0Og8LyHT5jM0TyApg7Blhn0rM1qGyh1sXk00ltGD5jQsMOzewrRs/FtpplvLM6Fpdm1FXA+pzWJq/wARPD8kBhnizIRnY0fJPsRTpQ5nzFpNaI3PD/j6TUtSwqbIkjZbdSck8jJPv0pfDb6g2r31/cvsUbz83Tk/4CvL/COtC78VGWORrCNR+6G0sQM9PfNdx4qurySzESXQMUjZZIIymfdqis0pcprK9jzzxFeXWpeKb25VyYn3FcdCMVlfarr3/Kulns/LmbZljsbPr0NZ/P8AcrtpSSjaxjJNvQ6a30uPVJECfu39q5j4l6LLo9nGkUxaRj9TW74iurjwz4mmtwGWGMjB9sVkaxrS662ChZl9azoxcZXWw5RVrHFeGbq/sW8ou2XPvXtfg/w7PBpZmlutw+8Ax5rgtMtYBukkUBx04rTXV7zcsEMzKh42qeMV0TuwXu7m/rVgwuFkB3Hrle1cfr1tdTSFAjOe1ekab4duIdKNzLKZN3RTVZTBbxtJNF06ZFcMnyy2LlK60PJJtPuGUq0eMHoOprU03T5ljTHBBwK7RdPh1iYx2ibpWyQMVBBZixZUcbsmuiE21sZOCk7swrm18xw0pYhT0rY1jULPSdDje2w0jdRjmrl1aW9zMB/qx0rL1jQ1+1eWRtt9ox6H3pyjzNCs5aIs6LeRazCx3bZCvy+maoRaXdtqzPIWigU4ODWlY+GG08RbW/1oBGOldzrnhieTQraW3TzHxiU49O9Ryxb02Kd+h5n461yHT4Y7eIMWCg+avX8fWuBt/P1K8STd5q54ZeR+NdxdeDtT8Sao8VvA7KysQ2MjgZrA8O+FdQ0vUJ38qRWjba+B8vUjB/I11Q9xaD2budX4N02DT7prq4kAK9jXpFrfRatas5TNvH8vA5/+tXn8eiX8khYWrICPmIHI+g7V2/wy8I6pfapLYwI5t5QfNVgc8d64ZU7y5myH72jOObUA15cQpCFjJ/H8TTvssfpXb6t8Pf7F0m4kuI/Jna6McbsMds1yv9l3n91a3jTVty/hVjN8b6hJ4muIpWh8qbYFfHfAxmsRdFOnwiVgTGRnnoK7ebT5NVuLYQxcyr5gx6VseJNJsrzR9IjhKmRoysqjsQT1qOe2iG1fU8evLjc6BDxnn0rsfAOjx6v4itIpMGPPz1k6x4fktWupBGfIiYASY4610/wt01rvxJaPv2RK253HYd81081kZcrbud1Kx0qSWwliK4z5THowrktZt5brRw5jKq0hTcK7P4hXsVxqllFatvjtVALDr1rqfBfhq08ReHZhMFIMvmL/ACrn5r6mrXQ8m+Gekyw+L7KIru35UfiDXTXXhODT9UeG6TLLliMc9a7rT/CsXh3Uk1COH5hJtQYqt4saWTXhIsOJS2whh6//AK6XNfRCseMeItLa9urhdOzhFLYXrgVoaXYreeEYhMN1zETnPXaTXb65o8Gk+KoI4QqhceYB3DdQapzaLbN4ugigysLAYX+EjNX8SBOxX1iyitdC09dhE8TLnjnaRUun+IJ5tMvbQsIWtpCAx5Bz612PxEs7eO+0aK1Cs0p8qTbjA9j71wOvaE+k3WvW0jY8yJZVPvuFEZKUbA073ON0vxEfDniK1laXYFmk81cZG1kx/OjxRcQQ306xsmbmWOZFcEZyWJxj/eqXx1oq6ZqWmztzFdRo+7HHbJrq5LPSvEnjTR3j2fZY4FJbtlBV8ziFmX9Nht9Q1+1s2GxpICsi85ySDn8RXoGjtb+FPEMbecIJJYQIwc7WYdc/zrL1LRYdL8XWepJKBE8O4j/ZCjpXU32ljVtNg1MKMQQPt49uK5784+XlRxvxCQeLjE1rOZLZrlZGwD1ICn9Qavf8Ktt/7x/OotBs57jw1pOxc7brMnHbJ5r0jzH/ALn8q1jLlVkD948X+GFjDceF0n2ZktQwGfQ9qfb/AA9kbz58lCqbh+PNb/w/8NnQ/wC0dO87crsHQZ6ZFdpfWryaekajbKpCuwrKUru6NFsjw/SlgvtB1y1uQoZRhQeuQaf8N/Ds6/aRbAK0kXGRwR3qvr1i+jeIL6PbmCVzk+v+TXrXgvSfL021v7dcw+QFOB371Uo6NkacySOfvvBM+lanh4i0c1uR0yM12HhXTl0PQ7WMDkr8w+pqr4tuNWt9DkkT52aTavGcAmtnQ7OZdJt3vmCyLtLCs5aWTGvIluGEmnyRSkpLHcr5b49cVSvtNbUPEe6SPbHGu8H3xx+tJqV5ML+O3wJILhwVb0wa29buh50ax4Err5ag9zWlrK5DPL9T8PvcX2pzSlpb1Iyyqo5xVrWtJjs/C2ltbOE1NAm+T+6D1H1/lW3D51vfTzEYudhjmPZFx296hsNBj1TSYbo7ivmYCnnoe9Z6qyBaGL4lUWcWnXMXzPDICUbkZI61g+LJBrM1yVJSdrPBA6ZBr0PXvDMt/MFt0BiIGV/usK5TXNHa1axhZCl08TKw7moh3NJXTscFrnhW81r4dJcGTzmsTx6hcgYpnwu8Ny6t4P1O5cNHdWTMYie4/ir12TSzp/w/k2xnzJoslQOpJxXH6bJf+BtUtrH7NuS9t2Z1I4OeufzrqUuaPKtxLqyzeTN4g1LQbZwdjW+xtvbGM16/a2sTaKLRMiPZtA7Vz3hvw5Z3E1rdSJslihYbSOgNb+kXwaP7KTtdNw/XiuaTS0NI3a1Ob8EyJHC1tMgRLd2j57nOc11GLX/nqPzp76HFDMgiADMA7EdzU/8AYY9B+dPRkJM5y2sLZdQaZU23P3VPqMVfuLZ/7PJZsSSNwKs/2eLedZwdw3ZFMvITNc2+DtjXl6nqaPY86+I3hyPUNLS5hKCXzAGYH867HwcY9P0O1tYCJEEQ3HqCcVzNxYzax4kubBcfYVkMhP4V12h6CdLhkiVjtX7m7pitm+hER5uo75GOFaGMHepHRh0pbjSbi8t08xysT85U/pTtPA+wzJLD5bM7bsVp6W0kkexlOzovvWTfcajpoULXTYpXiwNxg5q5f2KTTb1XM8J3Fx0Qe3vT9MWWTVLiC26bcu39w+g9/wCVW7O3ezsZFzkMxBzzWetrMv3XsYq6XDeQywKmxpFHzfWopLU6T4fWyhw8scgJUdcE81tRDaqh12yAYqvJarJeG4jO5hHyv0NaKSuieWyIBut40OSJGXB4qtNoUWt6pb3U5CtErDaa142TVLlFACk0NAjXk0JO35toas433HJJ6Gba+TqUV7Zuny26BRx2zxVebTLTWtQtZ3j3NGu1AR6Vvafa/wBmXV1GFBScD5mHPBq4LK3sriGTAxv6dODWil2I5bHM+Isae1mtsmJJJQj7f7tOks2keaWIbJXG3Nad/p6TXRlzkxyF1zz1qhcXrq4dk2JG+GPSspaG3oLYyXTIkMgInHBrX+y3FXoktGjF/wAcLnHv61H/AGtH6fpVpxFYxFDKrIBvI7Vh+KNRk0+wmTaRJIAof0JNFFZrcroWdN0dVs7eVQPO2gO/c8V0jQr9lt40PzZwT60UVrcmyLuo6faxWKMeTg59+Kj8+K1t0hSMoSM+af4eOg96KKzuGxBotvDp/nSH5VdsD3pb+Ro4nSJTtJ3H9KKKtO4lo7Fi71G2S3RmCtx1H0qtZReY3noBgjke1FFRLYrqFvZpFIkqn5t33aZrcHl27yw581nGR70UVF3YdkalrAt0IGm+WRV+b64rL11i7LGowuQciiitbbMi+gl3GnlRSb+OCwrN1aT7dbTRqmE25JooqahPQZojm+01djMAg2lSetaP7z+5RRWNrpBTbsf/2Q==")

# classify_face("0001","ali","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")   # print(get_encoded_faces())# print(names_list)


# new_friend("0001","ali","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")
#another pic


# remove_friend("0001","ali")

