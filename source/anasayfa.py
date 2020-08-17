#region Importlar
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import tkinter as tk
from kivy.core.window import Window
from tkinter import filedialog
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown 
from kivy.base import runTouchApp
import cv2 as cv
import os 
from kivy.uix.image import Image
import numpy as np
from kivy.uix.popup import Popup 
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import shutil
import random
import math
#endregion


globalResim = None
globalonIslemResim =None
globalfiltrelemeResim =None
globalmorfolojikResim =None
globalsegmentasyonResim =None
globalsonresim =None
#region AnasayfaTasarim
class AnasayfaTasarim(Screen):
    
    def openFileDialog(self):
        global globalResim
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        self.imageViewer.source =file_path
        self.imagePath = file_path
        globalResim = cv.imread(file_path)        
        print(file_path)
    def Ileri(self):
        dirName='temp'
        if os.path.exists(dirName):             
            shutil.rmtree('temp', ignore_errors=True)
            try:
                os.mkdir(dirName)
            except:
                os.mkdir(dirName)
            
        else:
            os.mkdir(dirName)
        cv.imwrite('./temp/0.jpg',globalResim)
        cv.imwrite('./temp/1.jpg',globalResim)
        cv.imwrite('./temp/2.jpg',globalResim)
        cv.imwrite('./temp/3.jpg',globalResim)
        cv.imwrite('./temp/4.jpg',globalResim)
        
        
#endregion

#region OnIslemTasarım
class OnIslemTasarim(Screen):

    global globalResim
    global globalonIslemResim
    
    onIslemDurumu=False 
    active = ObjectProperty(True)
    passive = ObjectProperty(False)
    def on_enter(self):
        self.onIslemResim.reload()
    def resmiguncelle(self):
         self.onIslemResim.reload()

    def onIslemIstiyorum(self,veri):
        if(veri.active):
            onIslemDurumu=True
            self.btn.disabled=False
            self.istemiyorum.active=False
        

    def onIslemIstemiyorum(self,veri):
        if(veri.active):
            onIslemDurumu=False
            self.btn.disabled=True
            self.istiyorum.active=False
        
    
    def resimAktar(self):
        global globalonIslemResim
        globalonIslemResim = cv.imread('./temp/1.jpg')

    def RGBtoGray(self):        
        global globalResim
        r = globalResim[:,:,0]
        g = globalResim[:,:,1]
        b = globalResim[:,:,2]
        griSeviye = 0.2989 * r + 0.5870 * g + 0.1140 * b
        griSeviye=griSeviye.astype('uint8')
        cv.imwrite('./temp/1.jpg',griSeviye)
        cv.imwrite('./temp/2.jpg',griSeviye)
        cv.imwrite('./temp/3.jpg',griSeviye)
        cv.imwrite('./temp/4.jpg',griSeviye)
        self.onIslemResim.source='./temp/1.jpg'
        self.onIslemResim.reload()
   
    def HistogramGoster(self): 
        cv.imwrite('./temp/1.jpg',globalResim)
        self.onIslemResim.source='./temp/1.jpg'
        self.onIslemResim.reload()
        layout = GridLayout(cols = 1,rows=7, padding = 10)
        redTable = GridLayout(cols=6,rows=2,padding=10)
        greenTable = GridLayout(cols=6,rows=2,padding=10)
        blueTable = GridLayout(cols=6,rows=2,padding=10)
        r = globalResim[:,:,0]
        g = globalResim[:,:,1]
        b = globalResim[:,:,2]
        sifirelli=0
        elliyuz=0
        yuzyuzelli=0
        yuzelliikiyuz=0
        ikiyuzikiyuzellibes=0
        for katman in range(3):
            sifirelli=0
            elliyuz=0
            yuzyuzelli=0
            yuzelliikiyuz=0
            ikiyuzikiyuzellibes=0
            for satir in range(0,r.shape[0]):
                for sutun in range(0,r.shape[1]):
                    seviye=globalResim[satir,sutun,katman]
                    if(seviye>=0 and seviye<50):
                        sifirelli+=1
                    elif(seviye>=50 and seviye<100):
                        elliyuz+=1
                    elif(seviye>=100 and seviye<150):
                        yuzyuzelli+=1
                    elif(seviye>=150 and seviye<200):
                        yuzelliikiyuz+=1
                    elif(seviye>=200 and seviye<=255):
                        ikiyuzikiyuzellibes+=1
            if(katman==0):
                redTable.add_widget(Label(text='-'))
                redTable.add_widget(Label(text=str(sifirelli)))
                redTable.add_widget(Label(text=str(elliyuz)))
                redTable.add_widget(Label(text=str(yuzyuzelli)))
                redTable.add_widget(Label(text=str(yuzelliikiyuz)))
                redTable.add_widget(Label(text=str(ikiyuzikiyuzellibes)))
            elif(katman==1):
                greenTable.add_widget(Label(text='-'))
                greenTable.add_widget(Label(text=str(sifirelli)))
                greenTable.add_widget(Label(text=str(elliyuz)))
                greenTable.add_widget(Label(text=str(yuzyuzelli)))
                greenTable.add_widget(Label(text=str(yuzelliikiyuz)))
                greenTable.add_widget(Label(text=str(ikiyuzikiyuzellibes)))
            elif(katman==2):
                blueTable.add_widget(Label(text='-'))
                blueTable.add_widget(Label(text=str(sifirelli)))
                blueTable.add_widget(Label(text=str(elliyuz)))
                blueTable.add_widget(Label(text=str(yuzyuzelli)))
                blueTable.add_widget(Label(text=str(yuzelliikiyuz)))
                blueTable.add_widget(Label(text=str(ikiyuzikiyuzellibes)))
                   
        for rValue in range(0,256,50):            
            redTable.add_widget(Label(text=str(rValue)))
        for rValue in range(0,256,50):            
            greenTable.add_widget(Label(text=str(rValue)))
        for rValue in range(0,256,50):            
            blueTable.add_widget(Label(text=str(rValue)))
        
        lblKirmizi = Label(text="Kırmızı Kanal")
        lblYesil = Label(text="Yeşil Kanal")
        lblMavi = Label(text="Mavi Kanal")
        layout.add_widget(lblKirmizi)
        layout.add_widget(redTable)
        layout.add_widget(lblYesil)
        layout.add_widget(greenTable)
        layout.add_widget(lblMavi)
        layout.add_widget(blueTable)
        closeButton = Button(text = "Kapat",width=200,height=50,size_hint_y=None) 
        layout.add_widget(closeButton)
    
        popup = Popup(title ='Histogram', 
                      content = layout, 
                      size_hint =(None, None), size =(500, 800))   
        popup.open()    
        closeButton.bind(on_press = popup.dismiss)
    
    
    def kesmeTiklama(self):
        layout = GridLayout(cols = 1,rows=3, padding = 10)
        bilgilbl = Label(text="Bilgilendirme : x1=10 y1=9 - x2=200 y2=190 \n Enter'a basın")
        koordinattxt = TextInput(text="10,9,200,190",multiline=False)
        closeButton = Button(text = "Kapat",width=200,height=50,size_hint_y=None)
        
        layout.add_widget(bilgilbl)
        layout.add_widget(koordinattxt) 
        
        layout.add_widget(closeButton)   
        popup = Popup(title ='Resim Kesme İşlemi', 
                      content = layout, 
                      size_hint =(None, None), size =(400, 400))   
        popup.open()
                  
        closeButton.bind(on_press = popup.dismiss)
        
        def on_enter(value):
            kordinatlar = value.text
            if(kordinatlar!=None):
                kordinat = str(kordinatlar).split(',')
                genislik = abs(int(kordinat[0])-int(kordinat[2]))
                yukseklik = abs(int(kordinat[1])-int(kordinat[3]))            
                cropImage = []
                for x in range(0,yukseklik):
                    cropImage.append([])
                    for y in range(0,genislik):
                        cropImage[x].append([])
                        for z in range(0,3):                       
                            cropImage[x][y].append(globalResim[x,y,z])                       
                        
                cropImage = np.array(cropImage)
                cv.imwrite('./temp/1.jpg',cropImage)
                cv.imwrite('./temp/2.jpg',cropImage)
                cv.imwrite('./temp/3.jpg',cropImage)
                cv.imwrite('./temp/4.jpg',cropImage)
                self.onIslemResim.source='./temp/1.jpg'
                self.onIslemResim.reload()            
            else:
                print('koordinat bilgisi bulunamadı')
        koordinattxt.bind(on_text_validate=on_enter)
    
    def yenidenBoyutlandir(self):
        layout = GridLayout(cols = 1,rows=3, padding = 10)
        bilgilbl = Label(text="Yeni boyutları girin : 640,480 \n Enter'a basın")
        boyuttxt = TextInput(text="740,500",multiline=False)
        closeButton = Button(text = "Kapat",width=200,height=50,size_hint_y=None)
        
        layout.add_widget(bilgilbl)
        layout.add_widget(boyuttxt) 
        
        layout.add_widget(closeButton)   
        popup = Popup(title ='Resim Yeniden Boyutlandırma İşlemi', 
                      content = layout, 
                      size_hint =(None, None), size =(400, 400))   
        popup.open()
                  
        closeButton.bind(on_press = popup.dismiss)
        
        def on_enter(value):
            boyutlar = value.text
            if(boyutlar!=None):
                boyut = str(boyutlar).split(',')
                genislik = int(boyut[1])
                yukseklik = int(boyut[0])            
                yeniImage = []
                for x in range(0,yukseklik):
                    yeniImage.append([])
                    for y in range(0,genislik):
                        yeniImage[x].append([])
                        for z in range(0,3):                       
                            yeniImage[x][y].append(0)
                yeniImage = np.array(yeniImage)
                sourcewidth = globalResim.shape[1]
                sourceheight = globalResim.shape[0]
                for x in range(0, genislik):  
                    for y in range(0, yukseklik):
                        srcX = int( round( float(x) / float(genislik) * float(sourcewidth) ) )
                        srcY = int( round( float(y) / float(yukseklik) * float(sourceheight) ) )
                        srcX = min( srcX, sourcewidth-1)
                        srcY = min( srcY, sourceheight-1)
                        yeniImage[y,x]=globalResim[srcY,srcX]
                
                print(yeniImage.shape)
                cv.imwrite('./temp/1.jpg',yeniImage)
                cv.imwrite('./temp/2.jpg',yeniImage)
                cv.imwrite('./temp/3.jpg',yeniImage)
                cv.imwrite('./temp/4.jpg',yeniImage)
                self.onIslemResim.source='./temp/1.jpg'
                self.onIslemResim.reload()            
            else:
                print('koordinat bilgisi bulunamadı')
        boyuttxt.bind(on_text_validate=on_enter)

    def resimZoom(self):
        layout = GridLayout(cols = 1,rows=3, padding = 10)
        bilgilbl = Label(text="Zoom miktarını girin ör: 2x \n Enter'a basın")
        miktartxt = TextInput(text="2x",multiline=False)
        closeButton = Button(text = "Kapat",width=200,height=50,size_hint_y=None)
        
        layout.add_widget(bilgilbl)
        layout.add_widget(miktartxt) 
        
        layout.add_widget(closeButton)   
        popup = Popup(title ='Resim büyültme,küçültme işlemleri', 
                      content = layout, 
                      size_hint =(None, None), size =(400, 400))   
        popup.open()
                  
        closeButton.bind(on_press = popup.dismiss)
        
        def on_enter(value):
            miktarbilgisi = value.text
            if(miktarbilgisi!=None):
                boyut = str(miktarbilgisi).split('x')
                miktar = int(boyut[0])
                genislik=globalResim.shape[1]
                yukseklik = globalResim.shape[0] 
                kaynakGenislik = round(globalResim.shape[1]-((globalResim.shape[1]*(miktar*10))/100))  
                kaynakYukseklik = round(globalResim.shape[0]-((globalResim.shape[0]*(miktar*10))/100))         
                kaynakResim=[]
                baslamaYukseklik = round(((globalResim.shape[0]*(miktar*10))/100)/2)
                bitisYukseklik = round(baslamaYukseklik+kaynakYukseklik)
                baslamaGenislik = round(((globalResim.shape[1]*(miktar*10))/100)/2)
                bitisGenislik = round(baslamaGenislik+kaynakGenislik)
               
                for x in range(0,kaynakYukseklik):
                    kaynakResim.append([])
                    for y in range(0,kaynakGenislik):
                        kaynakResim[x].append([])
                        for z in range(0,3):                       
                            kaynakResim[x][y].append(globalResim[baslamaYukseklik,baslamaGenislik,z])
                        baslamaGenislik+=1
                    baslamaYukseklik+=1
                    baslamaGenislik=round(((globalResim.shape[1]*(miktar*10))/100)/2)
                kaynakResim = np.array(kaynakResim)
                yeniImage = []
                for x in range(0,yukseklik):
                    yeniImage.append([])
                    for y in range(0,genislik):
                        yeniImage[x].append([])
                        for z in range(0,3):                       
                            yeniImage[x][y].append(0)
                yeniImage = np.array(yeniImage)
                sourcewidth = kaynakResim.shape[1]
                sourceheight = kaynakResim.shape[0]
                for x in range(0, genislik):  
                    for y in range(0, yukseklik):
                        srcX = int( round( float(x) / float(genislik) * float(sourcewidth) ) )
                        srcY = int( round( float(y) / float(yukseklik) * float(sourceheight) ) )
                        srcX = min( srcX, sourcewidth-1)
                        srcY = min( srcY, sourceheight-1)
                        yeniImage[y,x]=kaynakResim[srcY,srcX]
                
                print(yeniImage.shape)
                cv.imwrite('./temp/1.jpg',yeniImage)
                cv.imwrite('./temp/2.jpg',yeniImage)
                cv.imwrite('./temp/3.jpg',yeniImage)
                cv.imwrite('./temp/4.jpg',yeniImage)
                self.onIslemResim.source='./temp/1.jpg'
                self.onIslemResim.reload()            
            else:
                print('koordinat bilgisi bulunamadı')
        miktartxt.bind(on_text_validate=on_enter)
        

#endregion

#region FiltrelemeTasarim
class FiltrelemeTasarim(Screen):
    global globalResim
    global globalonIslemResim
    global globalmorfolojikResim
    ciktiResim = None
    ciktiResimKenarX=None
    ciktiResimKenarY=None
    bulanikFiltre =[[(1/9),(1/9),(1/9)],[(1/9),(1/9),(1/9)],[(1/9),(1/9),(1/9)]]
    keskinlestirFiltre =[[(-1/9),(-1/9),(-1/9)],[(-1/9),1,(-1/9)],[(-1/9),(-1/9),(-1/9)]]
    keskin2 =[[(0),(-.5),(0)],[(-.5),(3),(-.5)],[(0),(-.5),(0)]]
    laplaceFilter =[[(0),(-1),(0)],[(-1),(4),(-1)],[(0),(-1),(0)]]
    xKenar =[[(-1),(0),(1)],[(-2),(0),(2)],[(-1),(0),(1)]]
    yKenar =[[(-1),(-2),(-1)],[(0),(0),(0)],[(1),(2),(1)]]
    seek=2   
    tXRow=1
    tXColumn=1
    filtreDurumu=False
    def on_enter(self):
        self.filtreResim.reload()
    def filtrelemeIstiyorum(self,veri):
        if(veri.active):
            filtreDurumu=True
            self.btn.disabled=False
            self.filtrelemeistemiyorum.active=False
        

    def filtrelemeIstemiyorum(self,veri):
        if(veri.active):
            filtreDurumu=False
            self.btn.disabled=True
            self.filtrelemeistiyorum.active=False
        
    
    def calculateConv(self,pointOne,pointTwo,filtre,img,ch,filterType,nYukseklik,nGenislik):
        global globalonIslemResim
        counterX=0
        counterY=0
        if(pointOne[0]==0 and pointOne[1]==0):
            self.tXRow=1
            self.tXColumn=1
        for row in range(pointOne[0],pointTwo[0]+1):
            for column in range(pointOne[1],pointTwo[1]+1):
               
                self.ciktiResim[self.tXRow][self.tXColumn][ch] = int((filtre[counterX][counterY]*img[row][column])+self.ciktiResim[self.tXRow][self.tXColumn][ch])
                counterY=counterY+1
            counterX=counterX+1
            counterY=0
        
        self.tXColumn=self.tXColumn+1
        if(self.tXColumn==img.shape[1]-1):            
            self.tXColumn=1            
            self.tXRow=self.tXRow+1
        if((self.tXColumn==1 and self.tXRow==img.shape[0]-1) and ch==2):                
            self.ciktiResim=self.ciktiResim.astype(np.uint8)
            globalonIslemResim=globalonIslemResim.astype(np.uint8)
            if(filterType=='keskinlestirme'):
                self.ciktiResim  = globalonIslemResim+(globalonIslemResim-self.ciktiResim)*2   
                self.ciktiResim=self.ciktiResim.astype(np.uint8)
            cv.imwrite('./temp/2.jpg',self.ciktiResim)
            cv.imwrite('./temp/3.jpg',self.ciktiResim)
            cv.imwrite('./temp/4.jpg',self.ciktiResim)            
            self.filtreResim.source='./temp/2.jpg'
            self.filtreResim.reload() 

    def calculateConvGri(self,pointOne,pointTwo,filtre,img,filterType,nYukseklik,nGenislik):
        global globalonIslemResim
        counterX=0
        counterY=0
        if(pointOne[0]==0 and pointOne[1]==0):
            self.tXRow=1
            self.tXColumn=1
        for row in range(pointOne[0],pointTwo[0]+1):
            for column in range(pointOne[1],pointTwo[1]+1):
               
                self.ciktiResim[self.tXRow][self.tXColumn] = int((filtre[counterX][counterY]*img[row][column])+self.ciktiResim[self.tXRow][self.tXColumn])
                counterY=counterY+1
            counterX=counterX+1
            counterY=0
        
        self.tXColumn=self.tXColumn+1
        if(self.tXColumn==img.shape[1]-1):            
            self.tXColumn=1            
            self.tXRow=self.tXRow+1
        if((self.tXColumn==1 and self.tXRow==img.shape[0]-1)):                
            self.ciktiResim=self.ciktiResim.astype(np.uint8)
            globalonIslemResim=globalonIslemResim.astype(np.uint8)
            if(filterType=='kenarx'):
                self.ciktiResimKenarX  = self.ciktiResim.astype(np.uint8)  
                print("x bulundu")
            elif(filterType=='kenary'):
                self.ciktiResimKenarY  = self.ciktiResim.astype(np.uint8)   
                print("y bulundu")
                self.ciktiResim = self.ciktiResimKenarY+self.ciktiResimKenarX
                self.ciktiResim=self.ciktiResim.astype(np.uint8)
            cv.imwrite('./temp/2.jpg',self.ciktiResim)
            cv.imwrite('./temp/3.jpg',self.ciktiResim)
            cv.imwrite('./temp/4.jpg',self.ciktiResim)            
            self.filtreResim.source='./temp/2.jpg'
            self.filtreResim.reload()        
    def medianFilterExecute(self,pointOne,pointTwo,filtre,img,ch,filterType,nYukseklik,nGenislik):
        global globalonIslemResim
        counterX=0
        counterY=0
        if(pointOne[0]==0 and pointOne[1]==0):
            self.tXRow=1
            self.tXColumn=1
        temp=[]
        for row in range(pointOne[0],pointTwo[0]+1):
            for column in range(pointOne[1],pointTwo[1]+1):
                temp.append(img[row][column]) 
        temp.sort()
        self.ciktiResim[self.tXRow][self.tXColumn][ch] =temp[4]
        
        self.tXColumn=self.tXColumn+1
        if(self.tXColumn==img.shape[1]-1):            
            self.tXColumn=1            
            self.tXRow=self.tXRow+1
        if((self.tXColumn==1 and self.tXRow==img.shape[0]-1) and ch==2):                
            self.ciktiResim=self.ciktiResim.astype(np.uint8)
            cv.imwrite('./temp/2.jpg',self.ciktiResim)
            cv.imwrite('./temp/3.jpg',self.ciktiResim)
            cv.imwrite('./temp/4.jpg',self.ciktiResim)            
            self.filtreResim.source='./temp/2.jpg'
            self.filtreResim.reload() 
    def ciktiResimOlustur(self,ch,nYukseklik,nGenislik):
        self.ciktiResim = []
        for x in range(0,nYukseklik):
            self.ciktiResim.append([])
            for y in range(0,nGenislik):
                self.ciktiResim[x].append([])
                for z in range(0,ch):                       
                    self.ciktiResim[x][y].append(0)    
                         
                        
        self.ciktiResim = np.array(self.ciktiResim)
    def bulaniklastir(self):
        global bulanikFiltre
        global globalonIslemResim
        r = globalonIslemResim[:,:,0]       
        nYukseklik = r.shape[0]-3+1
        nGenislik =r.shape[1]-3+1      
        self.ciktiResimOlustur(3,r.shape[0],r.shape[1])        
        for ch in range(3):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,globalonIslemResim[:,:,ch].shape[0]-2):
                for columnm in range(0,globalonIslemResim[:,:,ch].shape[1]-2):
                    self.calculateConv((rowm,columnm),(rowm+self.seek,columnm+self.seek),self.bulanikFiltre,globalonIslemResim[:,:,ch],ch,'bulaniklastirma',nYukseklik,nGenislik)
                    if(columnm+(self.seek+1)>=globalonIslemResim[:,:,ch].shape[1]):
                        break
                if(rowm+(self.seek+1)>=globalonIslemResim[:,:,ch].shape[0]):
                    break

    def resimAktar(self):
        global globalmorfolojikResim
        globalmorfolojikResim = cv.imread('./temp/2.jpg')

    def keskinlestir(self):
        global keskin2
        global globalonIslemResim
        r = globalonIslemResim[:,:,0]  
        g = globalonIslemResim[:,:,1]
        b = globalonIslemResim[:,:,2]
        nYukseklik = r.shape[0]-(r.shape[0]-3+1)
        nGenislik =r.shape[1]-(r.shape[1]-3+1)     
        self.ciktiResimOlustur(3,r.shape[0],r.shape[1])
         
        for ch in range(3):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,globalonIslemResim[:,:,ch].shape[0]-2):
                for columnm in range(0,globalonIslemResim[:,:,ch].shape[1]-2):
                   
                    self.calculateConv((rowm,columnm),(rowm+self.seek,columnm+self.seek),self.keskin2,globalonIslemResim[:,:,ch],ch,'keskinlestirme',1,1)
                    if(columnm+(self.seek+1)>=globalonIslemResim[:,:,ch].shape[1]):
                        break
                if(rowm+(self.seek+1)>=globalonIslemResim[:,:,ch].shape[0]):
                    break      
        
    def ortancaUygula(self):
        global laplaceFilter
        global globalonIslemResim
        r = globalonIslemResim[:,:,0]  
        g = globalonIslemResim[:,:,1]
        b = globalonIslemResim[:,:,2]
        nYukseklik = r.shape[0]-(r.shape[0]-3+1)
        nGenislik =r.shape[1]-(r.shape[1]-3+1)     
        self.ciktiResimOlustur(3,r.shape[0],r.shape[1])
         
        for ch in range(3):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,globalonIslemResim[:,:,ch].shape[0]-2):
                for columnm in range(0,globalonIslemResim[:,:,ch].shape[1]-2):
                   
                    self.medianFilterExecute((rowm,columnm),(rowm+self.seek,columnm+self.seek),self.laplaceFilter,globalonIslemResim[:,:,ch],ch,'median',1,1)
                    if(columnm+(self.seek+1)>=globalonIslemResim[:,:,ch].shape[1]):
                        break
                if(rowm+(self.seek+1)>=globalonIslemResim[:,:,ch].shape[0]):
                    break  
    def laplaceUygula(self):
        global laplaceFilter
        global globalonIslemResim
        r = globalonIslemResim[:,:,0]  
        g = globalonIslemResim[:,:,1]
        b = globalonIslemResim[:,:,2]
        nYukseklik = r.shape[0]-(r.shape[0]-3+1)
        nGenislik =r.shape[1]-(r.shape[1]-3+1)     
        self.ciktiResimOlustur(3,r.shape[0],r.shape[1])
         
        for ch in range(3):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,globalonIslemResim[:,:,ch].shape[0]-2):
                for columnm in range(0,globalonIslemResim[:,:,ch].shape[1]-2):
                   
                    self.calculateConv((rowm,columnm),(rowm+self.seek,columnm+self.seek),self.laplaceFilter,globalonIslemResim[:,:,ch],ch,'laplas',1,1)
                    if(columnm+(self.seek+1)>=globalonIslemResim[:,:,ch].shape[1]):
                        break
                if(rowm+(self.seek+1)>=globalonIslemResim[:,:,ch].shape[0]):
                    break  
    def kenarBul(self):
        global xKenar
        global yKenar
        global globalonIslemResim
        r = globalonIslemResim[:,:,0]  
        g = globalonIslemResim[:,:,1]
        b = globalonIslemResim[:,:,2]
        griSeviye = 0.2989 * r + 0.5870 * g + 0.1140 * b
        griSeviye=griSeviye.astype('uint8')
        nYukseklik = r.shape[0]-(r.shape[0]-3+1)
        nGenislik =r.shape[1]-(r.shape[1]-3+1)     
        self.ciktiResimOlustur(1,r.shape[0],r.shape[1])
         
        for ch in range(1):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,griSeviye.shape[0]-2):
                for columnm in range(0,griSeviye.shape[1]-2):
                   
                    self.calculateConvGri((rowm,columnm),(rowm+self.seek,columnm+self.seek),self.xKenar,griSeviye,'kenarx',1,1)
                    if(columnm+(self.seek+1)>=griSeviye.shape[1]):
                        break
                if(rowm+(self.seek+1)>=griSeviye.shape[0]):
                    break  

        for ch in range(1):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,griSeviye.shape[0]-2):
                for columnm in range(0,griSeviye.shape[1]-2):
                   
                    self.calculateConvGri((rowm,columnm),(rowm+self.seek,columnm+self.seek),self.yKenar,griSeviye,'kenary',1,1)
                    if(columnm+(self.seek+1)>=griSeviye.shape[1]):
                        break
                if(rowm+(self.seek+1)>=griSeviye.shape[0]):
                    break
#endregion

#region MorfolojiTasarim
class MorfolojiTasarim(Screen):
    global globalmorfolojikResim
    global globalsegmentasyonResim
    siyahBeyazResim=None
    ciktiResim = None
    ciktiResim2 = None
    isFinished=False

    morfolojiDurumu=False
    def on_enter(self):
        self.morfolojiResim.reload()
    def morfolojiIstiyorum(self,veri):
        if(veri.active):
            morfolojiDurumu=True
            self.btn.disabled=False
            self.istemiyorum.active=False

    def morfolojiIstemiyorum(self,veri):
        if(veri.active):
            morfolojiDurumu=False
            self.btn.disabled=True
            self.istiyorum.active=False
       

    def OtsuThresholding(self):
        global globalmorfolojikResim
        r = globalmorfolojikResim[:,:,0]
        g = globalmorfolojikResim[:,:,1]
        b = globalmorfolojikResim[:,:,2]
        griSeviye = 0.2989 * r + 0.5870 * g + 0.1140 * b
        griSeviye=griSeviye.astype('uint8')
        histogram =[]
        varianceList=[]
        totalGriSeviye=0
        for i in range(256):
            histogram.append(0)
            varianceList.append(0)
        for row in range(griSeviye.shape[0]):
            for column in range(griSeviye.shape[1]):
                histogram[griSeviye[row][column]]+=1
                totalGriSeviye+=1        
        for index in range(len(histogram)):
            wB=0            
            for kk in range(index-1,-1,-1):
                wB+=histogram[kk]
            wB=wB/totalGriSeviye

            mean=0
            totalKK=0
            for kk in range(index-1,-1,-1):
                mean+=(kk*histogram[kk])
                totalKK+=histogram[kk]
            if(totalKK!=0):    
                mean = mean/totalKK
            else:
                mean=0

            variance=0
            totalKK=0
            for kk in range(index-1,-1,-1):
                variance+=((kk-mean)*(kk-mean))*histogram[kk]
                totalKK+=histogram[kk]
            if(totalKK!=0):  
                variance = variance/totalKK
            else:
                variance=0

            #----
            wF=0            
            for kb in range(index,len(histogram),1):
                wF+=histogram[kb]
            if(totalGriSeviye!=0):
                wF=wF/totalGriSeviye
            else:
                wF=0

            meanF=0
            totalKB=0
            for kb in range(index,len(histogram),1):
                meanF+=(kb*histogram[kb])
                totalKB+=histogram[kb]
            if(totalKB!=0):  
                meanF = meanF/totalKB
            else:
                meanF=0

            varianceF=0
            totalKB=0
            for kb in range(index,len(histogram),1):
                varianceF+=((kb-meanF)*(kb-meanF))*histogram[kb]
                totalKB+=histogram[kb]
            if(totalKB!=0):  
                varianceF = varianceF/totalKB
            else:
                varianceF=0

            #----
            classVariance = wB*variance+wF*varianceF
            varianceList[index]=classVariance
        sonuc=None
        sonucIndex=0
        for i in range(256):
            if(sonuc==None):
                sonuc = varianceList[i]
                sonucIndex=i
            else:
                if(varianceList[i]<sonuc):
                    sonuc = varianceList[i]
                    sonucIndex=i
       
        print(sonucIndex)
        return(sonucIndex)

    def siyahBeyazYap(self):
        global globalmorfolojikResim
        r = globalmorfolojikResim[:,:,0]
        g = globalmorfolojikResim[:,:,1]
        b = globalmorfolojikResim[:,:,2]
        griSeviye = 0.2989 * r + 0.5870 * g + 0.1140 * b
        griSeviye=griSeviye.astype('uint8')
        esikDeger = self.OtsuThresholding()
        
        siyahBeyazResim = []
        for x in range(0,griSeviye.shape[0]):
            siyahBeyazResim.append([])                      
        for i in range (griSeviye.shape[0]):
            for y in range(griSeviye.shape[1]):
                siyahBeyazResim[i].append(0)                
        siyahBeyazResim = np.array(siyahBeyazResim)
        siyahBeyazResim=siyahBeyazResim.astype('uint8')
        for row in range(griSeviye.shape[0]):
            for column in range(griSeviye.shape[1]):
                if(griSeviye[row][column]>esikDeger):
                    siyahBeyazResim[row][column]=0
                else:
                    siyahBeyazResim[row][column]=255
        return siyahBeyazResim
    def ciktiResimOlustur(self,nYukseklik,nGenislik):
        self.ciktiResim = []
        for x in range(0,nYukseklik):
            self.ciktiResim.append([])                      
        for i in range (nYukseklik):
            for y in range(nGenislik):
                self.ciktiResim[i].append(0)                
        self.ciktiResim = np.array(self.ciktiResim)
        self.ciktiResim=self.ciktiResim.astype('uint8') 
    def resimAktar(self):
        global globalsegmentasyonResim
        globalsegmentasyonResim = cv.imread('./temp/3.jpg')                    
    def ciktiResim2Olustur(self,nYukseklik,nGenislik):
        self.ciktiResim2 = []
        for x in range(0,nYukseklik):
            self.ciktiResim2.append([])                      
        for i in range (nYukseklik):
            for y in range(nGenislik):
                self.ciktiResim2[i].append(0)                
        self.ciktiResim2 = np.array(self.ciktiResim2)
        self.ciktiResim2=self.ciktiResim2.astype('uint8') 
        
    def maskToImageTravel(self,pointOne,pointTwo,img,transactionType):
        global globalmorfolojikResim
        if(transactionType=='genisletme'):
            for row in range(pointOne[0],pointTwo[0]+1):
                for column in range(pointOne[1],pointTwo[1]+1):
                    if(img[row][column]==255):
                        self.ciktiResim[pointOne[0]+1][pointOne[1]+1]=255
        elif(transactionType=='erezyon'):
            isSame=True
            for row in range(pointOne[0],pointTwo[0]+1):
                for column in range(pointOne[1],pointTwo[1]+1):
                    if(img[row][column]!=255):
                        isSame=False
                        break
                if(isSame==False):
                    break
            if(isSame==True):
                self.ciktiResim[pointOne[0]+1][pointOne[1]+1]=255
            else:
                isSame=True
        elif(transactionType=='acma1'):
            isSame=True
            for row in range(pointOne[0],pointTwo[0]+1):
                for column in range(pointOne[1],pointTwo[1]+1):
                    if(img[row][column]!=255):
                        isSame=False
                        break
                if(isSame==False):
                    break
            if(isSame==True):
                self.ciktiResim[pointOne[0]+1][pointOne[1]+1]=255
            else:
                isSame=True
        elif(transactionType=='acma2'):
            for row in range(pointOne[0],pointTwo[0]+1):
                for column in range(pointOne[1],pointTwo[1]+1):
                    if(img[row][column]==255):
                        self.ciktiResim2[pointOne[0]+1][pointOne[1]+1]=255
        elif(transactionType=='kapama1'):
             for row in range(pointOne[0],pointTwo[0]+1):
                for column in range(pointOne[1],pointTwo[1]+1):
                    if(img[row][column]==255):
                        self.ciktiResim[pointOne[0]+1][pointOne[1]+1]=255
        elif(transactionType=='kapama2'):
            isSame=True
            for row in range(pointOne[0],pointTwo[0]+1):
                for column in range(pointOne[1],pointTwo[1]+1):
                    if(img[row][column]!=255):
                        isSame=False
                        break
                if(isSame==False):
                    break
            if(isSame==True):
                self.ciktiResim2[pointOne[0]+1][pointOne[1]+1]=255
            else:
                isSame=True



        if(pointTwo[0] == img.shape[0]-1 and pointTwo[1]==img.shape[1]-1):
            if(transactionType=='acma2'):
                self.ciktiResim2=self.ciktiResim2.astype(np.uint8)
                self.ciktiResim=self.ciktiResim2
            if(transactionType=='kapama2'):
                self.ciktiResim2=self.ciktiResim2.astype(np.uint8)
                self.ciktiResim=self.ciktiResim2
            self.ciktiResim=self.ciktiResim.astype(np.uint8)
            cv.imwrite('./temp/3.jpg',self.ciktiResim)
            cv.imwrite('./temp/4.jpg',self.ciktiResim)            
            self.morfolojiResim.source='./temp/3.jpg'
            self.morfolojiResim.reload()    
            
    def genisletme(self):
        siyahBeyazResim=self.siyahBeyazYap()
        self.ciktiResimOlustur(siyahBeyazResim.shape[0],siyahBeyazResim.shape[1])
        for ch in range(1):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,siyahBeyazResim.shape[0]-2):
                for columnm in range(0,siyahBeyazResim.shape[1]-2):
                   
                    self.maskToImageTravel((rowm,columnm),(rowm+self.seek,columnm+self.seek),siyahBeyazResim,'genisletme')
                    if(columnm+(self.seek+1)>=siyahBeyazResim.shape[1]):
                        break
                if(rowm+(self.seek+1)>=siyahBeyazResim.shape[0]):
                    break  
    def erozyon(self):
        siyahBeyazResim=self.siyahBeyazYap()
        self.ciktiResimOlustur(siyahBeyazResim.shape[0],siyahBeyazResim.shape[1])
        for ch in range(1):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,siyahBeyazResim.shape[0]-2):
                for columnm in range(0,siyahBeyazResim.shape[1]-2):
                   
                    self.maskToImageTravel((rowm,columnm),(rowm+self.seek,columnm+self.seek),siyahBeyazResim,'erezyon')
                    if(columnm+(self.seek+1)>=siyahBeyazResim.shape[1]):
                        break
                if(rowm+(self.seek+1)>=siyahBeyazResim.shape[0]):
                    break  
    def acma(self):
        siyahBeyazResim=self.siyahBeyazYap()
        self.ciktiResimOlustur(siyahBeyazResim.shape[0],siyahBeyazResim.shape[1])
        self.ciktiResim2Olustur(siyahBeyazResim.shape[0],siyahBeyazResim.shape[1])
        for ch in range(1):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,siyahBeyazResim.shape[0]-2):
                for columnm in range(0,siyahBeyazResim.shape[1]-2):
                   
                    self.maskToImageTravel((rowm,columnm),(rowm+self.seek,columnm+self.seek),siyahBeyazResim,'acma1')
                    if(columnm+(self.seek+1)>=siyahBeyazResim.shape[1]):
                        break
                if(rowm+(self.seek+1)>=siyahBeyazResim.shape[0]):
                    break  
        for ch in range(1):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,self.ciktiResim.shape[0]-2):
                for columnm in range(0,self.ciktiResim.shape[1]-2):
                   
                    self.maskToImageTravel((rowm,columnm),(rowm+self.seek,columnm+self.seek),self.ciktiResim,'acma2')
                    if(columnm+(self.seek+1)>=self.ciktiResim.shape[1]):
                        break
                if(rowm+(self.seek+1)>=self.ciktiResim.shape[0]):
                    break  
    def kapama(self):
        siyahBeyazResim=self.siyahBeyazYap()
        self.ciktiResimOlustur(siyahBeyazResim.shape[0],siyahBeyazResim.shape[1])
        self.ciktiResim2Olustur(siyahBeyazResim.shape[0],siyahBeyazResim.shape[1])
        for ch in range(1):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,siyahBeyazResim.shape[0]-2):
                for columnm in range(0,siyahBeyazResim.shape[1]-2):
                   
                    self.maskToImageTravel((rowm,columnm),(rowm+self.seek,columnm+self.seek),siyahBeyazResim,'kapama1')
                    if(columnm+(self.seek+1)>=siyahBeyazResim.shape[1]):
                        break
                if(rowm+(self.seek+1)>=siyahBeyazResim.shape[0]):
                    break  
        for ch in range(1):
            self.seek=2
            self.xRow=0
            self.xColumn =0
            for rowm in range(0,self.ciktiResim.shape[0]-2):
                for columnm in range(0,self.ciktiResim.shape[1]-2):
                   
                    self.maskToImageTravel((rowm,columnm),(rowm+self.seek,columnm+self.seek),self.ciktiResim,'kapama2')
                    if(columnm+(self.seek+1)>=self.ciktiResim.shape[1]):
                        break
                if(rowm+(self.seek+1)>=self.ciktiResim.shape[0]):
                    break  
#endregion

#region SegmentasyonTasarim
class SegmentasyonTasarim(Screen):
    global globalsegmentasyonResim
   


    segmentasyonDurumu=False
    def on_enter(self):
        self.segmentasyonResim.reload()
    def segmentasyonIstiyorum(self,veri):
        if(veri.active):
            segmentasyonDurumu=True
            self.btn.disabled=False
            self.istemiyorum.active=False

    def segmentasyonIstemiyorum(self,veri):
        if(veri.active):
            segmentasyonDurumu=False
            self.btn.disabled=True
            self.istiyorum.active=False
    def OtsuThresholding(self):
        global globalsegmentasyonResim
        r = globalsegmentasyonResim[:,:,0]
        g = globalsegmentasyonResim[:,:,1]
        b = globalsegmentasyonResim[:,:,2]
        griSeviye = 0.2989 * r + 0.5870 * g + 0.1140 * b
        griSeviye=griSeviye.astype('uint8')
        histogram =[]
        varianceList=[]
        totalGriSeviye=0
        for i in range(256):
            histogram.append(0)
            varianceList.append(0)
        for row in range(griSeviye.shape[0]):
            for column in range(griSeviye.shape[1]):
                histogram[griSeviye[row][column]]+=1
                totalGriSeviye+=1        
        for index in range(len(histogram)):
            wB=0            
            for kk in range(index-1,-1,-1):
                wB+=histogram[kk]
            if(totalGriSeviye!=0):
                wB=wB/totalGriSeviye
            else:
                wB=0

            mean=0
            totalKK=0
            for kk in range(index-1,-1,-1):
                mean+=(kk*histogram[kk])
                totalKK+=histogram[kk]
            if(totalKK!=0):    
                mean = mean/totalKK
            else:
                mean=0

            variance=0
            totalKK=0
            for kk in range(index-1,-1,-1):
                variance+=((kk-mean)*(kk-mean))*histogram[kk]
                totalKK+=histogram[kk]
            if(totalKK!=0):  
                variance = variance/totalKK
            else:
                variance=0

            #----
            wF=0            
            for kb in range(index,len(histogram),1):
                wF+=histogram[kb]
            if(totalGriSeviye!=0):
                wF=wF/totalGriSeviye
            else:
                wF=0

            meanF=0
            totalKB=0
            for kb in range(index,len(histogram),1):
                meanF+=(kb*histogram[kb])
                totalKB+=histogram[kb]
            if(totalKB!=0):  
                meanF = meanF/totalKB
            else:
                meanF=0

            varianceF=0
            totalKB=0
            for kb in range(index,len(histogram),1):
                varianceF+=((kb-meanF)*(kb-meanF))*histogram[kb]
                totalKB+=histogram[kb]
            if(totalKB!=0):  
                varianceF = varianceF/totalKB
            else:
                varianceF=0

            #----
            classVariance = wB*variance+wF*varianceF
            varianceList[index]=classVariance
        sonuc=None
        sonucIndex=0
        for i in range(256):
            if(sonuc==None):
                sonuc = varianceList[i]
                sonucIndex=i
            else:
                if(varianceList[i]<sonuc):
                    sonuc = varianceList[i]
                    sonucIndex=i
       
        print(sonucIndex)
        return(sonucIndex)
    
    def esikDegerBul(self):
        layout = GridLayout(cols = 1,rows=3, padding = 10)
        bilgilbl = Label(text="Eşik Değer")
        deger = self.OtsuThresholding()
        esikDeger = Label(text=str(deger))
        closeButton = Button(text = "Kapat",width=200,height=50,size_hint_y=None)
        
        layout.add_widget(bilgilbl)
        layout.add_widget(esikDeger) 
        
        layout.add_widget(closeButton)   
        popup = Popup(title ='Eşik Değer', 
                      content = layout, 
                      size_hint =(None, None), size =(300, 300))   
        popup.open()
                  
        closeButton.bind(on_press = popup.dismiss)
    def siyahBeyazYap(self):
        global globalsegmentasyonResim
        r = globalsegmentasyonResim[:,:,0]
        g = globalsegmentasyonResim[:,:,1]
        b = globalsegmentasyonResim[:,:,2]
        griSeviye = 0.2989 * r + 0.5870 * g + 0.1140 * b
        griSeviye=griSeviye.astype('uint8')
        esikDeger = self.OtsuThresholding()
        
        siyahBeyazResim = []
        for x in range(0,griSeviye.shape[0]):
            siyahBeyazResim.append([])                      
        for i in range (griSeviye.shape[0]):
            for y in range(griSeviye.shape[1]):
                siyahBeyazResim[i].append(0)                
        siyahBeyazResim = np.array(siyahBeyazResim)
        siyahBeyazResim=siyahBeyazResim.astype('uint8')
        for row in range(griSeviye.shape[0]):
            for column in range(griSeviye.shape[1]):
                if(griSeviye[row][column]>=esikDeger):
                    siyahBeyazResim[row][column]=0
                else:
                    siyahBeyazResim[row][column]=255
        return siyahBeyazResim
    def ciktiResimOlustur(self,ch,nYukseklik,nGenislik):
        self.ciktiResim = []
        for x in range(0,nYukseklik):
            self.ciktiResim.append([])
            for y in range(0,nGenislik):
                self.ciktiResim[x].append([])
                for z in range(0,ch):                       
                    self.ciktiResim[x][y].append(0)    
                         
                        
        self.ciktiResim = np.array(self.ciktiResim)
        self.ciktiResim=self.ciktiResim.astype('uint8')
    def siyahBeyazNesneDetect(self,img):
        global globalmorfolojikResim
        
        for row in range(img.shape[0]):
            for column in range(img.shape[1]):
                if(img[row][column]==255):
                    # if(column+1!=img.shape[1] and (self.ciktiResim[row][column][0]==0 and self.ciktiResim[row][column][1]==0 and self.ciktiResim[row][column][2]==0)):
                    #     if(img[row][column+1]==255 and (self.ciktiResim[row][column+1][0]!=0 or self.ciktiResim[row][column+1][1]!=0 or self.ciktiResim[row][column+1][2]!=0)):
                    #         self.ciktiResim[row][column] = self.ciktiResim[row][column+1]
                    if(row-1>=0 and (self.ciktiResim[row][column][0]==0 and self.ciktiResim[row][column][1]==0 and self.ciktiResim[row][column][2]==0)):
                        if(img[row-1][column]==255 and (self.ciktiResim[row-1][column][0]!=0 or self.ciktiResim[row-1][column][1]!=0 or self.ciktiResim[row-1][column][2]!=0)):
                            self.ciktiResim[row][column] = self.ciktiResim[row-1][column]
                    if(column-1>=0 and (self.ciktiResim[row][column][0]==0 and self.ciktiResim[row][column][1]==0 and self.ciktiResim[row][column][2]==0)):
                        if(img[row][column-1]==255 and (self.ciktiResim[row][column-1][0]!=0 or self.ciktiResim[row][column-1][1]!=0 or self.ciktiResim[row][column-1][2]!=0)):
                            self.ciktiResim[row][column] = self.ciktiResim[row][column-1]
                    # if(row+1!=img.shape[0] and (self.ciktiResim[row][column][0]==0 and self.ciktiResim[row][column][1]==0 and self.ciktiResim[row][column][2]==0)):
                    #     if(img[row+1][column]==255 and (self.ciktiResim[row+1][column][0]!=0 or self.ciktiResim[row+1][column][1]!=0 or self.ciktiResim[row+1][column][2]!=0)):
                    #         self.ciktiResim[row][column] = self.ciktiResim[row+1][column]
                    if(self.ciktiResim[row][column][0]==0 and self.ciktiResim[row][column][1]==0 and self.ciktiResim[row][column][2]==0):
                        self.ciktiResim[row][column][0]=random.randint(128,255)
                        self.ciktiResim[row][column][1]=random.randint(128,255)
                        self.ciktiResim[row][column][2]=random.randint(128,255)
        


        self.ciktiResim=self.ciktiResim.astype('uint8')        
        cv.imwrite('./temp/4.jpg',self.ciktiResim)            
        self.segmentasyonResim.source='./temp/4.jpg'
        self.segmentasyonResim.reload()    
                    
            
    def siyahBeyazNesneBul(self):
        siyahBeyazResim=self.siyahBeyazYap()
        self.ciktiResimOlustur(3,siyahBeyazResim.shape[0],siyahBeyazResim.shape[1])
        self.siyahBeyazNesneDetect(siyahBeyazResim) 

    def griNesneBul(self):
        layout = GridLayout(cols = 1,rows=3, padding = 10)
        bilgilbl = Label(text="k değerini giriniz \n Enter'a basın")
        kDegeri = TextInput(text="3",multiline=False)
        closeButton = Button(text = "Kapat",width=200,height=50,size_hint_y=None)
        
        layout.add_widget(bilgilbl)
        layout.add_widget(kDegeri) 
        
        layout.add_widget(closeButton)   
        popup = Popup(title ='Gri Nesne Bulma', 
                      content = layout, 
                      size_hint =(None, None), size =(400, 400))   
        popup.open()
                  
        closeButton.bind(on_press = popup.dismiss)
        
        def on_enter(value):
            k_value = value.text
            if(k_value!=None):
                global globalsegmentasyonResim
                self.ciktiResimOlustur(3,globalsegmentasyonResim.shape[0],globalsegmentasyonResim.shape[1])
                r = globalsegmentasyonResim[:,:,0]
                g = globalsegmentasyonResim[:,:,1]
                b = globalsegmentasyonResim[:,:,2]
                griSeviye = 0.2989 * r + 0.5870 * g + 0.1140 * b
                griSeviye=griSeviye.astype('uint8')
                kumeMerkezleri=[]
                kumeler =[]
                k_value =int(k_value)
                for i in range(k_value):
                    kumeMerkezleri.append(random.randint(0,255))
                    kumeler.append([])
                kMeansDevam =True
                degisim=False
                while(kMeansDevam):
                    for row in range(griSeviye.shape[0]):
                        for column in range(griSeviye.shape[1]):
                            tempUzakliklar=[]
                            for merkez in kumeMerkezleri:
                                tempUzakliklar.append(math.sqrt((merkez-griSeviye[row][column])**2))
                            enKucuk = min(tempUzakliklar)
                            kumeIndex = tempUzakliklar.index(enKucuk)
                            kumeler[kumeIndex].append(griSeviye[row][column])
                    for i in range(len(kumeMerkezleri)):
                        toplam=0
                        for item in kumeler[i]:
                            toplam+=item
                        if(len(kumeler[i])!=0):
                            ortalama = int(toplam/len(kumeler[i]))
                        else:
                            ortalama=0
                        if(kumeMerkezleri[i]!=ortalama):
                            degisim=True
                            kumeMerkezleri[i] = ortalama
                    if(degisim==False):
                        kMeansDevam=False
                    else:
                        degisim=False
                        kumeler=[]
                        for x in range(k_value):
                            kumeler.append([])
                renkler = []
                for i in range(k_value):
                    renkler.append([random.randint(128,255),random.randint(128,255),random.randint(128,255)])
                for row in range(griSeviye.shape[0]):
                    for column in range(griSeviye.shape[1]):
                        griseviyeDegeri = griSeviye[row][column]
                        for i in range(k_value):
                            if(griseviyeDegeri in kumeler[i]):
                                self.ciktiResim[row][column] = renkler[i]
                                break
                self.ciktiResim=self.ciktiResim.astype('uint8')        
                cv.imwrite('./temp/4.jpg',self.ciktiResim)            
                self.segmentasyonResim.source='./temp/4.jpg'
                self.segmentasyonResim.reload()    

            else:
                print('k değeri yok')
        kDegeri.bind(on_text_validate=on_enter)
        

    def resimAktar(self):
        global globalsonresim
        globalsonresim = cv.imread('./temp/4.jpg')  
    def renkliNesneBul(self):
        layout = GridLayout(cols = 1,rows=3, padding = 10)
        bilgilbl = Label(text="k değerini giriniz \n Enter'a basın")
        kDegeri = TextInput(text="3",multiline=False)
        closeButton = Button(text = "Kapat",width=200,height=50,size_hint_y=None)
        
        layout.add_widget(bilgilbl)
        layout.add_widget(kDegeri) 
        
        layout.add_widget(closeButton)   
        popup = Popup(title ='Renkli Resim Nesne Bulma', 
                      content = layout, 
                      size_hint =(None, None), size =(400, 400))   
        popup.open()
                  
        closeButton.bind(on_press = popup.dismiss)
        
        def on_enter(value):
            k_value = value.text
            if(k_value!=None):
                global globalsegmentasyonResim
                self.ciktiResimOlustur(3,globalsegmentasyonResim.shape[0],globalsegmentasyonResim.shape[1])
                kumeMerkezleri=[]
                kumeler =[]
                k_value =int(k_value)
                for i in range(k_value):
                    kumeMerkezleri.append([random.randint(0,255),random.randint(0,255),random.randint(0,255)])
                    kumeler.append([])
                kMeansDevam =True
                degisim=False
                while(kMeansDevam):
                    for row in range(globalsegmentasyonResim.shape[0]):
                        for column in range(globalsegmentasyonResim.shape[1]):
                            tempUzakliklar=[]
                            for merkez in kumeMerkezleri:
                                tempUzakliklar.append(
                                    math.sqrt(
                                        ((merkez[0]-globalsegmentasyonResim[row][column][0])**2)+
                                        ((merkez[1]-globalsegmentasyonResim[row][column][1])**2)+
                                        ((merkez[2]-globalsegmentasyonResim[row][column][2])**2)
                                        
                                        )
                                    )
                            enKucuk = min(tempUzakliklar)
                            kumeIndex = tempUzakliklar.index(enKucuk)
                            kumeler[kumeIndex].append([globalsegmentasyonResim[row][column][0],globalsegmentasyonResim[row][column][1],globalsegmentasyonResim[row][column][2]])
                    for i in range(len(kumeMerkezleri)):
                        toplamR=0
                        toplamG=0
                        toplamB=0
                        for item in kumeler[i]:
                            toplamR+=item[0]
                            toplamG+=item[1]
                            toplamB+=item[2]
                        if(len(kumeler[i])!=0):
                            ortalamaR = int(toplamR/len(kumeler[i]))
                            ortalamaG = int(toplamG/len(kumeler[i]))
                            ortalamaB = int(toplamB/len(kumeler[i]))
                        else:
                            ortalamaR=0
                            ortalamaG =0
                            ortalamaB=0
                        
                        if(kumeMerkezleri[i][0]!=ortalamaR and kumeMerkezleri[i][1]!=ortalamaG and kumeMerkezleri[i][2]!=ortalamaB):
                            degisim=True
                            kumeMerkezleri[i][0] = ortalamaR
                            kumeMerkezleri[i][1] = ortalamaG
                            kumeMerkezleri[i][2] = ortalamaB
                    if(degisim==False):
                        kMeansDevam=False
                    else:
                        degisim=False
                        kumeler=[]
                        for x in range(k_value):
                            kumeler.append([])
                renkler = []
                for i in range(k_value):
                    renkler.append([random.randint(128,255),random.randint(128,255),random.randint(128,255)])
                for row in range(globalsegmentasyonResim.shape[0]):
                    for column in range(globalsegmentasyonResim.shape[1]):
                        griseviyeDegeri = [globalsegmentasyonResim[row][column][0],globalsegmentasyonResim[row][column][1],globalsegmentasyonResim[row][column][2]]
                        for i in range(k_value):
                            if(griseviyeDegeri in kumeler[i]):
                                self.ciktiResim[row][column] = renkler[i]
                                break
                self.ciktiResim=self.ciktiResim.astype('uint8')        
                cv.imwrite('./temp/4.jpg',self.ciktiResim)            
                self.segmentasyonResim.source='./temp/4.jpg'
                self.segmentasyonResim.reload()    

            else:
                print('k değeri yok')
        kDegeri.bind(on_text_validate=on_enter)

#endregion
#region KaydetSayfası
class KaydetTasarim(Screen):
    global globalsonresim
    uzanti=None
  
    def on_enter(self):
        self.kaydetResim.reload()
    def kaydetmeIslemi(self):
        cv.imwrite('./son.'+str(self.uzanti),globalsonresim)
        print('Kaydedildi.')
    def jpgKaydet(self):
        self.uzanti='jpg'
    def bmpKaydet(self):
        self.uzanti='bmp'
    def tifKaydet(self):
        self.uzanti='tif'
    def pngKaydet(self):
        self.uzanti='png'
#endregion
#region WindowManager
class WindowManager(ScreenManager):
    pass

#endregion

#region AnasayfaApp
anasayfa = Builder.load_file("anasayfa.kv")     

class AnasayfaApp(App):    
    def build(self):
        return anasayfa

if __name__ == '__main__':   
    AnasayfaApp().run()

#endregion