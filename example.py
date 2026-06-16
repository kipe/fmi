from fmi import FMI

f = FMI(place="Lappeenranta")
print(f.observations())
