# PhoenixTeamAyY-zeyiRotaOptimizasyonu
Ay Yuzeyi Guvenli Rota Planlayici (LRO LOLA Pathfinding)
Bu proje, NASA'nın LRO (Lunar Reconnaissance Orbiter) verilerini temel alarak Ay yuzeyindeki egim haritalari uzerinde en guvenli ve dusuk maliyetli rotayi hesaplayan bir A* (A-Star) algoritmasi uygulamasidir. Yazilim, tehlikeli bolgelerden kacinan bir navigasyon simulasyonu sunar.

Proje Hakkinda
Kod, LRO_LOLA_ClrSlope_Global_16ppd.tif adli topografik egim haritasini analiz eder. Belirlenen HSV (Renk, Doygunluk, Parlaklik) degerlerine gore yuzeyi "Guvenli" ve "Tehlikeli" olarak siniflandirir.

Temel Ozellikler:
Goruntu Isleme: OpenCV ve rasterio kutuphaneleri ile yuksek cozunurluklu .tif dosyalarinin islenmesi.

Maliyet Analizi: Yuzey egimine gore dinamik bir maliyet matrisi (cost matrix) olusturulmasi.

A* Algoritmasi: Baslangic noktasindan hedef koordinata (800, 600) en kisa ve guvenli yolun bulunmasi.

Gorsellestirme: Hesaplanan rotanin orijinal harita uzerinde cizilerek ay_sonuc.png olarak kaydedilmesi.

Teknik Detaylar
Renk ve Risk Siniflandirmasi
Algoritma, haritadaki renk tonlarina gore asagidaki risk degerlendirmesini yapar:

Sari-Turuncu: Guvenli Bolge (Maliyet: 1).

Yesil: Orta Risk (Maliyet: 100).

Mavi: Yuksek Risk (Maliyet: 100).

Kirmizi/Mor: Tehlikeli / Gecilemez (Maliyet: 100).

Kullanilan Teknolojiler
Python 3.x.

-NumPy: Matris islemleri ve maliyet hesaplamalari.

-OpenCV (cv2): Goruntu isleme ve gorsellestirme.

-Rasterio: Cografi bilgi sistemleri (GIS) verilerini okuma.

-Heapq: A* algoritmasi icin oncelikli kuyruk yonetimi.

Dosya Yapisi
new1.py: Rotayi hesaplayan ana Python scripti.

LRO_LOLA_ClrSlope_Global_16ppd.tif: Ay yuzeyi egim verilerini iceren kaynak dosya.

ay_sonuc.png: Algoritma tarafindan uretilen rotayi gosteren sonuc gorseli.

Kurulum ve Calistirma
Gerekli kutuphaneleri yukleyin:
pip install numpy opencv-python rasterio

Ana dosyayi calistirin:
python new1.py
