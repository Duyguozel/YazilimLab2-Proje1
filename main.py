import requests #web üzerindeki isteklerin yönetilmesi için kullanılmıştır.
from bs4 import BeautifulSoup #Bu modül ile bir kaynak içerisindeki HTML kodlarını parse edip,botlar yazabiliriz.
from flask import Flask,render_template,request,redirect,url_for #render_template bizim html template imizi alıp response olarak döndürmemizi sağlıyor
import operator #sozluk oluşturmak ıcın kullanılmıştır.
import nltk 
from nltk.corpus import stopwords #etkisiz kelimeleri bulmak için oluşturuldu. Dizinin ana fikrini oluşturan kelimeler bulunurken gereksiz kelimeleri diziden çıkarmak için kullandık
from nltk.corpus import wordnet #5. isteri tamamlamak için kullanıldı. Kelimelerin eş anlamlısı ve zıt anlamlısını bulmak için kullanılır. İngilizce uyumludur.
"""Request modulü: Bir HTTP kütüphanesidir. Internetteki bilgilerin çekilmesi bu kütüphaneyle yapılmıştır.
Beautiful Soup Kütüphanesi: Request ile çekilen bilgiler bu kütüphane ile işlenir.  """

def createDictionary(allWords): #metindeki kelimelerin adetini hesaplayıp döndüren fonksiyon. kelimelerle bir sözlük oluşturur
    wordCount = {} #hem kelime hem de ne kadar geçtiği bunda tutulacak

    for word in allWords:
        if word in wordCount: #daha önce bu kelime gelmişse
            wordCount[word] += 1 #kelime sayısını arttır
        else: #kelime ilk kez gelmişse
            wordCount[word] = 1 #yeni kelime ekle, adet 1
    return wordCount

def clearSymbols(allWords): #kelimeleri sembollerinden temizleyen fonksiyon
    nonSymbolsWords = [] #Sembolsüz kelimeleri içerisine atmak için oluşturulan boş dizi
    symbols =  "!'^+%&/()=?_-*|\}][{½$#£\"><@.,;’...:\n"+chr(775) #kelimelerden temizlenmesi gereken semboller.
    for word in allWords:
        for sym in symbols:
            if sym in word: #kelimenin icinde sembol varsa
                word = word.replace(sym,"")#eğer kelime içerisinde sembol varsa silinir
        if (len(word)>0): #boyutu 0'dan büyük olan kelimeler sembolsüz kelimeler dizisine atılır. 
            nonSymbolsWords.append(word)
    return nonSymbolsWords

def clearWords(allWords):
    nonSymbolsWords = [] #Edat ve baglac kelimeleri içerisine atmak için oluşturulan boş dizi
    symbols =  list(stopwords.words('english')) #kelimelerden temizlenmesi gereken edat ve baglaclar.
    for word in allWords:
        if word in symbols: #kelimenin icinde edat veya baglac varsa
                word = word.replace(word,"")#eğer kelime içerisinde edat veya baglac varsa silinir
        if (len(word)>0): #boyutu 0'dan büyük olan kelimeler sembolsüz kelimeler dizisine atılır. 
            nonSymbolsWords.append(word)
    return nonSymbolsWords

def synonymsWords(word): #Verilen kelimenin eş anlamlı kelimelerini bulmak için oluşturuldu.
        synonyms = list()
        for i in wordnet.synsets(word):
            synonyms.append(i.lemma_names()[0]) #lemma_names eş anlamlı kelimeleri bulurken lemmas zıt anlamlı kelimeleri bulur.
        return synonyms
def synonymsWords2(url): #Verilen kelimenin eş anlamlı kelimelerini ekrana yazdırmak için oluşturuldu.
        keep_keyWords_url = [] #Ana url'deki anahtar kelimeleri tutar.
        keep_keyCount_url = [] #Ana url'deki anahtar kelimelerin adedini tutar.
        searchWords = [] #Anahtar ve semantik anlam dahil.
        
        keep_keyCount_url, keep_keyWords_url = page2_functions(url) #ana url nin anahtar kelimelerine ulaşıldı ve bunlar kelimeler ve adetleri olmak üzere ikiye ayırıldı.
        synonymAll = [] #ekraba yazdırmak için
        #print("Anahtar kelimeler; ",keep_keyWords_url, "Adetleri: ",keep_keyCount_url)

        for i in range(0,len(keep_keyWords_url)):
            searchWords.clear() #her kelimenin eş anlamlılarını tutmaması için döngüye her girişinde dizi temizlendi
            keep_synonymsWords = [] # eş anlamlı kelimeleri tutmak için oluşturuldu.
            synonymArray =  []
            if(len(synonymsWords(keep_keyWords_url[i]))>0): #eş anlamlı kelimesi olan kelimeler diziye atıldı
                keep_synonymsWords = synonymsWords(keep_keyWords_url[i])

            print("Anahtar Kelime: ",keep_keyWords_url[i],"Eş anlamlı kelimeler: ",keep_synonymsWords)
            synonymArray = "%s%s%s%s%s%s%s"%("Anahtar Kelime= ","[",keep_keyWords_url[i],"]","---","SEMANTIK ANLAMLILARI: " , keep_synonymsWords)
            synonymAll.append(synonymArray)

        return synonymAll   
def page5_Score(url1,url2): #5. isterin skorunu hesaplamak için oluşuruldu.
        keep_keyWords_url = [] #Ana url'deki anahtar kelimeleri tutar.
        keep_keyCount_url = [] #Ana url'deki anahtar kelimelerin adedini tutar.
        searchWords = [] #Anahtar ve semantik anlam dahil.
        searchWords2 = [] #Tekrar edenleri silip Anahtar ve semantik kelimleri tutar.
        keep2_Word_url = [] #Arama yapılacak urlin hem icerigi hem sayısı kelimeleri tutar
        keep2_Word = [] #Arama yapılacak urlin sadece kelimlerini tutar
        keep2_Word_Count = [] #Arama yapılacak urlin sadece kelimlerinin sayısını tutar
        count = 0 #eger ana kelime veya semantik kelimeler arama yapılan url'de varsa count aratacak
        wordSum = 0 #Arama yapılacak url'in toplam kelime sayısı
        sameN = 0 
        synonymArray = [] #ekrana yazdırmak için

            
        keep_keyCount_url, keep_keyWords_url = page2_functions(url1) #ana url nin anahtar kelimelerine ulaşıldı ve bunlar kelimeler ve adetleri olmak üzere ikiye ayırıldı.
        
        print("Anahtar kelimeler; ",keep_keyWords_url, "Adetleri: ",keep_keyCount_url)

        for i in range(0,len(keep_keyWords_url)):
            searchWords.clear() #her kelimenin eş anlamlılarını tutmaması için döngüye her girişinde dizi temizlendi
            searchWords2.clear()
            keep2_Word.clear()
            wordSum = 0
            keep_synonymsWords = [] # eş anlamlı kelimeleri tutmak için oluşturuldu.
            
            if(len(synonymsWords(keep_keyWords_url[i]))>0): #eş anlamlı kelimesi olan kelimeler diziye atıldı
                keep_synonymsWords = synonymsWords(keep_keyWords_url[i])

            print("Anahtar Kelime: ",keep_keyWords_url[i],"Eş anlamlı kelimeler: ",keep_synonymsWords)
            synonymArray = "%s%s%s"%(keep_keyWords_url[i],"SEMANTIK ANLAMLILARI: " , keep_synonymsWords)
        
            searchWords.append(keep_keyWords_url[i])
            if (len(keep_synonymsWords) > 0):
                for j in range(0,len(keep_synonymsWords)):
                       searchWords.append(keep_synonymsWords[j])
                
            for i in range(0,len(searchWords)):
                if searchWords[i] not in searchWords2:
                    searchWords2.append(searchWords[i])    
                

                
            print("ARANAN KELİMELER: ",searchWords2,"\n")
            

    
            keep2_Word_url = page1_functions(url2)
            #print(keep2_Word_url)

            for foundWord,piece in sorted(keep2_Word_url.items(),key = operator.itemgetter(1)):
                keep2_Word.append(foundWord)
                keep2_Word_Count.append(piece)
                wordSum = wordSum + piece
            print(keep2_Word_url)

            for m in range(0,len(searchWords2)):
                if searchWords2[m] in keep2_Word:
                   print("ARANAN KELIME BU URL'DE GECIYOR:",searchWords2[m])
                   sameN = sameN + 1
                   for k in range(0,len(keep2_Word)):
                       if (searchWords2[m] == keep2_Word[k]):
                           count = count + keep2_Word_Count[k]

            print("TOPLAM GECME SAYISI:",count)
        if(wordSum != 0): #sıfıra bölme hatası veriyordu
            a = (int(count) / int (wordSum) )* int(sameN) * 100
            print("COUNT:",count)
            print("SAME",sameN)
            print("WORD SUM",wordSum)
            print("ORAN:",a,"\n\n")
            return int(a)
        else:
            return 0
                
def page1_functions(url):
        allWords = []
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser") #beautifulsoup ile kodun içeriğinden istenilen kısmı ayrıştırmak için kullanılacak
        for paragraphs in soup.find_all("p"): # ulaşılan URL'yi oluşturan kodun içerisindeki <p> etiketi bulunan kısımlar ayrıştırılır.
            content = paragraphs.text #cümledeki sadece kelimeleri alır, <p> gibi şeyleri almaz
            words = content.lower().split() #lower; tüm harfleri küçük harfe dönüştürür büyük küçük harf duyarlılığını engellemek için. split; boşluğa göre kelimeleri ayırır.
            for w in words:
                allWords.append(w)# tümkelimeler in içine kelimeler atıldı

        #print("\n\n------ TEMİZLENMİŞ ------\n\n")
        allWords = clearSymbols(allWords) #tüm kelimeleri içeren dizinin içeriğine temizlenmiş kelimeler atanır
        #for w in allWords:
            #print(w,"---------------------------------------------------")


        #print("\n\n------ SÖZLÜK ------\n\n")
        wordCount = createDictionary(allWords)
        #for foundWord,piece in sorted(wordCount.items(),key = operator.itemgetter(1)): #0:kelimeye göre alfabetik; 1:degere gore sıralar
           #print(foundWord,piece,"-----------------------------------------------------------------------------------------------------")
        
        
        return wordCount

def page2_functions(url):
        allWords = []
        allfoundWords = []
        allPieces = []
        keepIdea = [] 
        keepIdea2 = [] 
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        for paragraphs in soup.find_all("p"):
            content = paragraphs.text #cümledeki sadece kelimeleri alır, <p gibi şeyleri almaz
            words = content.lower().split() #lower; tüm harfleri küçük harfe dönüştürür büyük küçük harf duyarlılığını engellemek için. split; boşluğa göre kelimeleri ayırır.

            for w in words:
                allWords.append(w)# tümkelimeler in içine kelimeler atıldı

        allWords = clearSymbols(allWords)
        allWords = clearWords(allWords)
        #print(allfoundWords)

        wordCount = createDictionary(allWords)

        for foundWord,piece in sorted(wordCount.items(),key = operator.itemgetter(0)): #0:anahtara göre; 1:degere gore sıralar
           allfoundWords.append(foundWord)
           allPieces.append(piece)
        #print(allfoundWords)
        #print(allPieces)

        for i in range (len(allPieces)):
            for j in reversed (range(i+1 , len(allPieces))):
                if(allPieces[j]<allPieces[j-1]):
                   temp = allPieces[j-1]
                   temp2 = allfoundWords[j-1]
                   allPieces[j-1] = allPieces[j]
                   allfoundWords[j-1] = allfoundWords[j]
                   allPieces[j] = temp
                   allfoundWords[j] = temp2
            
       # print(allfoundWords,allPieces)
        for i in range(len(allPieces)-5, len(allPieces)):
            keepIdea.append(allPieces[i]) #ana fikri oluşturan 5 kelimenin adetleri keepIdea dizisinde tutulur
            keepIdea2.append(allfoundWords[i]) #ana fikri oluşturan 5 kelime keepIdea2 diziside tutulur
        #print(keepIdea,keepIdea2)    

        return keepIdea,keepIdea2

    
def page3_functions(url1, url2):
    url1_keepWords = [] #kelime tutuluyor.(ana fikir)
    url1_keppCount = [] #adet tutuluyor(ana fikir)
    url1_keppCount , url1_keepWords = page2_functions(url1)
    #print(url1_keepWords , "duygu")
    print("\n\n***************")

    url2_KeepWords = [] #kelime  tutuluyor.(ana fikir)
    url2_keppCount = [] #adet tutuluyor. (ana fikir)
    url2_keppCount , url2_keepWords = page2_functions(url2)
    #print(url2_keepWords , "duygu")
    print("\n\n***************")
    
    url2_all = [] # hem kelime adet tutulacak.(bütün kelimeler)
    url2_all = page1_functions(url2)
    url2_allWCount = [] #url2'nin her kelime sayısı tutulacak
    url2_allWord = [] #url2'nin her kelimeler tutulacak

    sumAll = 0
    sumSame = 0
    ortaklar = []
    ortakSayisi = 0
    for foundWord,piece in sorted(url2_all.items(),key = operator.itemgetter(0)): #0:anahtara göre; 1:degere gore sıralar
        url2_allWCount.append(piece)
        url2_allWord.append(foundWord)
        sumAll = sumAll + piece
    
    print("-------------",url2_all)
    for i in range(0,5):
        if url1_keepWords[i] in url2_allWord:
            ortaklar.append(url1_keepWords[i])
            ortakSayisi = ortakSayisi + 1
    
    
    for j in range(0,len(ortaklar)):
        for k in range(0,len(url2_allWord)):
            if (ortaklar[j] == url2_allWord[k]):
                 
                 sumSame = sumSame + url2_allWCount[k]

    print("TOPLAM KELİME SAYISI :" , sumAll)

    a = (int(sumSame) / int (sumAll) ) * int (ortakSayisi) * 100
    print("BENZERLİK ORANI: %",a,"\n\n")
    
    return int(a) #url1_keepWords,url2_KeepWords


    
def page4_functions(url):
        skor1 = [] #Derinlik 1: Ana Url ve Url Kümesindeki bir link arasındaki benzerliği hesaplar
        skor2 = [] #Derinlik 2: Ana Url ve Url Kümesindeki alt linkler arasındaki benzerliği hesaplar
        skor3 = [] #Derinlik 3: Ana Url ve Url Kümesindeki altın altı linkler arasındaki benzerliği hesaplar
        all_offSkor = [] 
        urlSet = ["https://www.oscars.org/oscars",
                "https://www.oscars.org/museum"]
        
        skor1_All = [] #Derinlik 1 : Arayüze skorları yazdırmak için oluşturduk
        skor2_All = [] #Derinlik 2 : Arayüze skorları yazdırmak için oluşturduk
        skor3_All = [] #Derinlik 3 : Arayüze skorları yazdırmak için oluşturduk

           
        
        for j in range(0,len(urlSet)):
                print("URL KÜMESİNDEKİ " , j ,". eleman açılıyor.\n\n")
                print("DERİNLİK = 1\n\n")
                r = requests.get(urlSet[j])
                soup = BeautifulSoup(r.content,"html.parser")
                result = page3_functions(url,urlSet[j]) 
                skor1.append(page3_functions(url,urlSet[j]))
                skor1_S = "%s%s%s"%(j+1,". URL : % ",result)
                skor1_All.append(skor1_S)
                all_offSkor.append(page3_functions(url,urlSet[j]))
                links = soup.find_all("a")
                symbols = [] #["#","None"]
                clearLink = [] 
                for link in links:
                        """if link in symbols: #kelimenin icinde edat veya baglac varsa
                                link= link.replace(link,"")#eğer kelime içerisinde edat veya baglac varsa silinir"""
                        if (len(link)>0): #boyutu 0'dan büyük olan kelimeler sembolsüz kelimeler dizisine atılır. 
                            clearLink.append(link)
                
                realLink = []
                for link in clearLink:
                        if (str(link.get("href")).startswith( 'http' , 0 ,4)): #bulunan linkler http ile başlıyorsa gerçek linkler dizisine atılır
                            print("1->",link.get("href"))
                            realLink.append(link.get("href"))


                print("DERINLIK 1'DEKI URL -> ILK LINK ",realLink[j],"\n\n\n\n\n\n\n\n")

                for i in range(0,1):
                        print("\n\nDERİNLİK = 2\n\n")
                        print(i,". girişi")
                        r2 = requests.get(realLink[i])
                        soup2 = BeautifulSoup(r2.content,"html.parser")
                        result2 = page3_functions(url,realLink[i])
                        skor2.append(page3_functions(url,realLink[i]))
                        skor2_S = "%s%s%s%s%s"%(j+1,". Url -> ",i+1,". alt link : % ",result2)
                        skor2_All.append(skor2_S)
                        all_offSkor.append(page3_functions(url,realLink[i]))
                        links2 = soup2.find_all("a")
                        clearLink2 = []
                        if (len(realLink) == 0): #eğer alt link yok ise
                                print("Link bulunamadı")
                                break
                        else:
                                print("Bulunan alt link sayısı:",len(realLink),"\n\n\n\n\n\n")
                                for lin in links2:
                                        """if link in symbols: #kelimenin icinde edat veya baglac varsa
                                                link= link.replace(link,"")#eğer kelime içerisinde edat veya baglac varsa silinir"""
                                        if (len(lin)>0): #boyutu 0'dan büyük olan kelimeler sembolsüz temiz linkler dizisine atılır. 
                                            clearLink2.append(lin)
                                realLink2 = []
                                for lin in clearLink2:
                                        if (str(lin.get("href")).startswith( 'http' , 0 ,4)): #link.get("href")[0:4] == "http"
                                            print("2-> ",lin.get("href"))
                                            realLink2.append(lin.get("href"))

                                print("DERINLIK 2'DEKI URL -> ILK LINK -> LINK ",realLink2[i],"\n\n\n\n\n\n\n\n")
                                for k in range(0,1):
                                        print("DERİNLİK = 3")
                                        print(k,". girişi")
                                        r3 = requests.get(realLink2[k])
                                        soup3 = BeautifulSoup(r3.content,"html.parser")
                                        result3 = page3_functions(url,realLink2[k])
                                        skor3.append(page3_functions(url,realLink2[k]))
                                        skor3_S = "%s%s%s%s%s%s%s%s"%(j+1,". Url ->",i+1,". Alt link ->", k+1, ". Alt link",": %",result3)
                                        skor3_All.append(skor3_S)
                                        all_offSkor.append(page3_functions(url,realLink2[k]))
                                        if (len(realLink2) == 0):
                                                print("Altın altı link bulunamadı")
                                                break
                                        else:
                                                print("Bulunan altın altı link sayısı:",len(realLink2),"\n\n\n\n\n\n\n\n\n\n")
                                
                                for i in range(len(all_offSkor)):
                                    for j in range(i+1, len(all_offSkor)):
                                        if all_offSkor[j] > all_offSkor[i]:
                                            all_offSkor[j], all_offSkor[i] = all_offSkor[i], all_offSkor[j]
        
        return all_offSkor,skor1_All,skor2_All,skor3_All


def page5_functions(url):
        skor1 = [] #Derinlik 1: Ana Url ve Url Kümesindeki bir link arasındaki benzerliği hesaplar
        skor2 = [] #Derinlik 2: Ana Url ve Url Kümesindeki alt linkler arasındaki benzerliği hesaplar
        skor3 = [] #Derinlik 3: Ana Url ve Url Kümesindeki altın altı linkler arasındaki benzerliği hesaplar
        all_offSkor = []
        urlSet = ["https://www.oscars.org/oscars",
                "https://www.oscars.org/governors"]


                
        skor1_All = [] #Derinlik 1 : Arayüze skorları yazdırmak için oluşturduk
        skor2_All = [] #Derinlik 2 : Arayüze skorları yazdırmak için oluşturduk
        skor3_All = [] #Derinlik 3 : Arayüze skorları yazdırmak için oluşturduk
        
        
        for j in range(0,len(urlSet)):
                print("URL KÜMESİNDEKİ " , j ,". eleman açılıyor")

                r = requests.get(urlSet[j])
                soup = BeautifulSoup(r.content,"html.parser")
                result = page5_Score(url,urlSet[j])
                skor1.append(result)
                skor1_S = "%s%s%s"%(j+1,". URL : % ",result)
                skor1_All.append(skor1_S)
                all_offSkor.append(result)
                links = soup.find_all("a")
                symbols = [] #["#","None"]
                clearLink = []
                for link in links:
                        """if link in symbols: #kelimenin icinde edat veya baglac varsa
                                link= link.replace(link,"")#eğer kelime içerisinde edat veya baglac varsa silinir"""
                        if (len(link)>0): #boyutu 0'dan büyük olan kelimeler sembolsüz kelimeler dizisine atılır. 
                            clearLink.append(link)
                
                realLink = []
                for link in clearLink:
                        if (str(link.get("href")).startswith( 'http' , 0 ,4)): #link.get("href")[0:4] == "http"
                            print(link.get("href"))
                            realLink.append(link.get("href"))


                print("URL -> ILK LINK **",realLink[j],"\n\n\n\n\n\n\n\n")

                for i in range(0,3):
                        print(i,". girişi")
                        r2 = requests.get(realLink[i])
                        soup2 = BeautifulSoup(r2.content,"html.parser")
                        result2 = page5_Score(url,realLink[i])
                        skor2.append(result2)
                        skor2_S = "%s%s%s%s%s"%(j+1,". Url -> ",i+1,". alt link : % ",result2)
                        skor2_All.append(skor2_S)
                        all_offSkor.append(result2)
                        #print("ALT LINKKKKKKKKKKK BENZERLIK:",result2)
                        links2 = soup2.find_all("a")
                        clearLink2 = []
                        if (len(realLink) == 0):
                                print("Link bulunamadı")
                                break
                        else:
                                print("Bulunan alt link sayısı:",len(realLink),"\n\n\n\n\n\n\n\n\n\n")
                                for lin in links2:
                                        """if link in symbols: #kelimenin icinde edat veya baglac varsa
                                                link= link.replace(link,"")#eğer kelime içerisinde edat veya baglac varsa silinir"""
                                        if (len(lin)>0): #boyutu 0'dan büyük olan kelimeler sembolsüz temiz linkler dizisine atılır. 
                                            clearLink2.append(lin)
                                realLink2 = []
                                for lin in clearLink2:
                                        if (str(lin.get("href")).startswith( 'http' , 0 ,4)): #link.get("href")[0:4] == "http"
                                            print(lin.get("href"))
                                            realLink2.append(lin.get("href"))

                                print("URL -> ILK LINK -> LINK **",realLink2[i],"\n\n\n\n\n\n\n\n")
                                for k in range(0,3):
                                        print(k,". girişi-----------------------------------------------------")
                                        r3 = requests.get(realLink2[k])
                                        soup3 = BeautifulSoup(r3.content,"html.parser")
                                        result3= page5_Score(url,realLink2[k])
                                        skor3.append(result3)
                                        skor3_S = "%s%s%s%s%s%s%s%s"%(j+1,". Url ->",i+1,". Alt link ->", k+1, ". Alt link",": %",result3)
                                        skor3_All.append(skor3_S)
                                        all_offSkor.append(result3)
                                        #print("ALTIN ALTI LINKKKKKKKKKKK BENZERLIK:",result3)
                                        if (len(realLink2) == 0):
                                                print("Altın altı link bulunamadı")
                                                break
                                        else:
                                                print("Bulunan altın altı link sayısı:",len(realLink2),"\n\n\n\n\n\n\n\n\n\n")
                                
                                for i in range(len(all_offSkor)):
                                    for j in range(i+1, len(all_offSkor)):
                                        if all_offSkor[j] > all_offSkor[i]:
                                            all_offSkor[j], all_offSkor[i] = all_offSkor[i], all_offSkor[j]

        return all_offSkor,skor1_All,skor2_All,skor3_All


app = Flask(__name__) #flask sınıfından uygulama oluştur. name:özel nesne

@app.route("/") #kök dizine erişirse index.html sayfasına yönlendir
def index():
       return render_template("index.html")

@app.route("/page1", methods = ["GET","POST"]) 
def page1_direct():  
    if request.method == "POST":
       return render_template("page1.html")
    else:
        return " PAGE NOT FOUND !"

@app.route("/page2", methods = ["GET","POST"])
def page2_direct():
    if request.method == "POST":
        return render_template("page2.html")
    else:
        return " PAGE NOT FOUND !"
    
@app.route("/page3", methods = ["GET","POST"])
def page3_direct():
    if request.method == "POST":
        return render_template("page3.html")
    else:
        return " PAGE NOT FOUND !"

@app.route("/page4", methods = ["GET","POST"])
def page4_direct():
    if request.method == "POST":
        return render_template("page4.html")
    else:
        return " PAGE NOT FOUND !"


@app.route("/page5", methods = ["GET","POST"])
def page5_direct():
    if request.method == "POST":
        return render_template("page5.html")
    else:
        return " PAGE NOT FOUND !"

@app.route("/frequency" , methods = ["GET","POST"])
def frequency():
    if request.method == "POST":
      
       url1 = request.form.get("urlAlani")
       page1_function_run = page1_functions(url1)
       return render_template("page1.html",page1_function_run = page1_function_run)

    else:
        return render_template("page1.html")

@app.route("/mainIdea",methods = ["GET","POST"])
def mainIdea():
    if request.method == "POST":
        url1 = request.form.get("url1")
        page2_function_run = page2_functions(url1)
        return render_template("page2.html",page2_function_run = page2_function_run)
    else:
        return render_template("")

@app.route("/similarityScore",methods = ["GET","POST"])
def similarityScore():
    if request.method == "POST":
        url1 = request.form.get("url1")
        url2 = request.form.get("url2")
        page3_function_run = page3_functions(url1, url2)
        return render_template("page3.html",page3_function_run = page3_function_run)
    else:
        return render_template("")

@app.route("/siteIndexing",methods = ["GET","POST"])
def  siteIndexing():
    if request.method == "POST":
        url1 = request.form.get("url1")
        page4_function_run , skor1_All , skor2_All,skor3_All = page4_functions(url1)
        return render_template("page4.html",synpage4_function_run = page4_function_run , skor1_All = skor1_All, skor2_All = skor2_All, skor3_All = skor3_All)
    else:
        return render_template("")


@app.route("/synonym",methods = ["GET","POST"])
def  synonym():
    if request.method == "POST":
        url1 = request.form.get("url1")
        synonymsAll = synonymsWords2(url1)
        page5_function_run,skor1_All,skor2_All,skor3_All = page5_functions(url1)
        return render_template("page5.html",synonymsAll=synonymsAll,page5_function_run = page5_function_run,skor1_All = skor1_All,skor2_All = skor2_All,skor3_All = skor3_All)
    else:
        return render_template("")

if __name__ == "__main__": #bu dosya terminalden mi çalıştırılmış evetse(localhost)
    app.run(debug=True) #çalıştır.