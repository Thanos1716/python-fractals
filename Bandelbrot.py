j = 1000
v = -50
h = -64
s = 25
mat = ""
for r in range(1, 64):
    for d in range(1, 128):
        z = complex(0, 0)
        c = complex((r + v) / s, (d + h) / s)
        for i in range(j):
            z = complex(z.real * z.real - z.imag * z.imag +
                        c.real, 2 * z.real * z.imag + c.imag)
            if abs(z.real) > 2:
                break
            if abs(z.imag) > 2:
                break
        if i + 2 > j:
            mat = mat + "#"  # str(i) + ("" if len(str(i)) < 2 else "")
        else:
            mat = mat + "."
    mat += "\n"

print(mat)
