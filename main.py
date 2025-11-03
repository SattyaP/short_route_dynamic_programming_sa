import math

def tsp_iterative(distance, names):

    n = len(distance)
    ALL_VISITED = 1 << n  # total subset bitmask
    dp = [[math.inf] * n for _ in range(ALL_VISITED)]  
    parent = [[-1] * n for _ in range(ALL_VISITED)]   

    
    # Mulai dari node awal (Supplier = index 0)
    dp[1][0] = 0

    # Membangun tabel DP dengan memeriksa semua subset kota
    for mask in range(ALL_VISITED):
        for u in range(n):
            # Lewati jika kota u belum dikunjungi dalam subset ini
            if not (mask & (1 << u)):
                continue

            # Coba kunjungi kota berikutnya (v)
            for v in range(n):
                # Lewati jika kota v sudah dikunjungi
                if mask & (1 << v):
                    continue

                # Lalu tambahkan kota v ke subset (mask baru)
                new_mask = mask | (1 << v)

                # Setelah itu, hitung jarak total baru
                new_dist = dp[mask][u] + distance[u][v]

                # Jika lebih pendek, maka akan memperbarui DP dan simpan parent
                if new_dist < dp[new_mask][v]:
                    dp[new_mask][v] = new_dist
                    parent[new_mask][v] = u  

    # Mencari rute paling pendek dengan kembali ke kota awal
    min_cost = math.inf
    last_city = -1
    for i in range(1, n):
        # total jarak = dp[mask terakhir][kota terakhir] + kembali ke start
        cost = dp[ALL_VISITED - 1][i] + distance[i][0]
        if cost < min_cost:
            min_cost = cost
            last_city = i

    # Rekonstruksi rute dari parent[][]
    path = [0]  # mulai dari Supplier (0)
    mask = (1 << n) - 1
    city = last_city
    stack = []

    # Telusuri rute mundur dari parent[][]
    while city != 0:
        stack.append(city)
        prev = parent[mask][city]
        mask ^= (1 << city)
        city = prev

    # Susun rute secara urut (0 → ... → 0)
    path.extend(reversed(stack))
    path.append(0)

    # Mengubah indeks rute menjadi nama lokasi
    named_route = [names[i] for i in path]

    return min_cost, path, named_route

distance = [
    [0, 10, 15, 20],   # Supplier ke (A, B, C)
    [10, 0, 35, 25],   # Gudang A ke (Supplier, B, C)
    [15, 35, 0, 30],   # Gudang B ke (Supplier, A, C)
    [20, 25, 30, 0],   # Gudang C ke (Supplier, A, B)
]

names = ["Supplier", "Gudang A", "Gudang B", "Gudang C"]

min_cost, route, named_route = tsp_iterative(distance, names)

print("Jarak minimum:", min_cost)
print("Rute (nomor):", " → ".join(map(str, route)))
print("Rute (nama):", " → ".join(named_route))
