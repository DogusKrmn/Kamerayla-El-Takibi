# Kamerayla El Takibi
Kamerayla kişinin elini algılayıp kaç parmağın açık olduğunu tespit edip ekrana yazdıran bir el takip sistemi. Pythonla yazılmıştır


Özellikler
Web kamerasından gerçek zamanlı el takibi
Elin 21 eklem noktasını ve bağlantılarını görüntü üzerinde çizme
Açık parmakları sayma ve açık parmakların uçlarını vurgulama
Ekranda parmak sayısına göre bilgisayarın ses seviyesini ayarlama

Nasıl Çalışır?
Kameradan alınan her kare ayna görüntüsüne çevrilir ve MediaPipe Hands modeline verilir.
Model, elin 21 eklem noktasının koordinatlarını döndürür.
Parmaklar, bu koordinatlar karşılaştırılarak sayılır:
İşaret, orta, yüzük ve serçe parmak: Uç noktası, alt ekleminden (PIP) daha yukarıdaysa parmak açıktır.
Başparmak: Uç noktasının serçe kökine olan uzaklığı, bir alttaki eklemin uzaklığından büyükse açıktır. Bu yöntem sağ ve sol elde de çalışır.
Ses seviyesi açık parmak sayısı x %20 olarak hesaplanır.

<img width="781" height="580" alt="image" src="https://github.com/user-attachments/assets/770fd9b1-30b5-4a1b-9b33-893a95dd9e68" />
