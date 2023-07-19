words = ['-', ',', '.', '\\', '/', 'fc', 'U21', 'w', 'women', 'FC']
t = "kos koskcoal mmsa., ko fc dcfcqew"

print(t)

for w in words:
    t = t.replace(w, " ")

print(t)
