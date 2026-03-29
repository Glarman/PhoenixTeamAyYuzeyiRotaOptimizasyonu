import numpy as np
import cv2
import rasterio
import heapq
import random

DOSYA = 'LRO_LOLA_ClrSlope_Global_16ppd.tif'
BITIS = (800, 600)
LOG_ADIM = 50

def haritayi_hazirla():
    with rasterio.open(DOSYA) as src:
        data = src.read([1, 2, 3]).transpose(1, 2, 0)
        img = cv2.normalize(data, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    border = cv2.addWeighted(img, 0.5, cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB), 0.5, 0)
    mask = cv2.inRange(hsv, np.array([10, 100, 100]), np.array([35, 255, 255]))
    rows, cols = img.shape[:2]
    cost_matrix = np.ones((rows, cols), dtype=np.float32) * 100
    cost_matrix[mask > 0] = 1
    print(f"[HARITA] Boyut: {cols}x{rows} piksel")
    guvenli = np.sum(mask > 0)
    print(f"[HARITA] Guvenli: {guvenli} px | Tehlikeli: {rows*cols-guvenli} px")
    return img, cost_matrix, hsv, cols, rows

def renk_tespit(hsv, x, y):
    h, s, v = hsv[y, x]
    if s < 50:
        return "Beyaz/Gri"
    elif 10 <= h <= 35:
        return "Sari-Turuncu (Guvenli)"
    elif 35 < h <= 85:
        return "Yesil (Orta Risk)"
    elif 85 < h <= 130:
        return "Mavi (Yuksek Risk)"
    else:
        return "Kirmizi/Mor (Tehlikeli)"

def astar(cost_matrix, baslangic, bitis):
    rows, cols = cost_matrix.shape
    sx, sy = baslangic
    ex, ey = bitis
    print(f"\n[A*] Baslangic: {baslangic} -> Hedef: {bitis}")
    print(f"[A*] Baslangic bolgesi: {'guvenli' if cost_matrix[sy,sx]==1 else 'TEHLIKELI'}")
    print(f"[A*] Hedef bolgesi: {'guvenli' if cost_matrix[ey,ex]==1 else 'TEHLIKELI'}")
    heap = []
    heapq.heappush(heap, (0, 0, sx, sy, None))
    g_map = np.full((rows, cols), np.inf)
    g_map[sy, sx] = 0
    parent_map = {}
    visited = set()
    yonler = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    adim = 0
    while heap:
        f, g, x, y, parent = heapq.heappop(heap)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        parent_map[(x, y)] = parent
        adim += 1
        if adim % LOG_ADIM == 0:
            kalan = abs(x - ex) + abs(y - ey)
            bolge = 'guvenli' if cost_matrix[y, x] == 1 else 'TEHLIKELI'
            print(f"[TARAMA #{adim:>5}] Konum: ({x:>4},{y:>4})  | Kalan: {kalan:>4} px | {bolge}")
        if (x, y) == (ex, ey):
            print(f"\n[A*] Hedefe ulasildi! Taranan nokta: {adim}")
            path = []
            node = (ex, ey)
            while node is not None:
                path.append(node)
                node = parent_map[node]
            path.reverse()
            return path, g
        for dx, dy in yonler:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited:
                am = cost_matrix[ny, nx] * (1.414 if dx != 0 and dy != 0 else 1)
                yeni_g = g + am
                if yeni_g < g_map[ny, nx]:
                    g_map[ny, nx] = yeni_g
                    h = abs(nx - ex) + abs(ny - ey)
                    heapq.heappush(heap, (yeni_g + h, yeni_g, nx, ny, (x, y)))
    return [], 0

img, cost_matrix, hsv, cols, rows = haritayi_hazirla()

BASLANGIC = (random.randint(0, cols-1), random.randint(0, rows-1))
renk = renk_tespit(hsv, BASLANGIC[0], BASLANGIC[1])
h, s, v = hsv[BASLANGIC[1], BASLANGIC[0]]
print(f"\n[BASLANGIC] Koordinat: {BASLANGIC}")
print(f"[BASLANGIC] HSV: H={h}, S={s}, V={v}")
print(f"[BASLANGIC] Renk: {renk}")
print(f"[BASLANGIC] Maliyet: {cost_matrix[BASLANGIC[1], BASLANGIC[0]]:.0f}")

path, toplam_maliyet = astar(cost_matrix, BASLANGIC, BITIS)

if path:
    guvenli_adim = sum(1 for (x,y) in path if cost_matrix[y,x] == 1)
    print(f"\n[SONUC] Toplam adim: {len(path)}")
    print(f"[SONUC] Guvenli: {guvenli_adim} | Tehlikeli: {len(path)-guvenli_adim}")
    sonuc = img.copy()
    for (x, y) in path:
        cv2.circle(sonuc, (x, y), 3, (255, 0, 0), -1)
    cv2.circle(sonuc, BASLANGIC, 8, (0, 255, 0), 20)
    cv2.circle(sonuc, BITIS, 8, (0, 0, 255), 20)
    cv2.imwrite("ay_sonuc.png", cv2.cvtColor(sonuc, cv2.COLOR_RGB2BGR))
    print(f"[DOSYA] ay_sonuc.png kaydedildi.")
else:
    print("\n[HATA] Rota bulunamadi!")