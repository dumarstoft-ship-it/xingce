# MK2715X-M2 SAIC 2024
prod = [24.39,18.97,39.02,35.47,32.77,30.72,23.75,26.17,33.67,41.66]
sale = [24.49,20.78,38.14,36.00,33.22,30.05,25.15,25.76,31.33,40.19]
nprod = [7.15,5.93,8.40,7.48,8.22,9.42,6.92,8.78,14.22,16.53]
nsale = [6.43,6.10,8.48,7.46,8.29,9.34,7.11,8.66,12.93,15.71]
print('sums', sum(prod), sum(sale), sum(nprod), sum(nsale))
# Q1
cur = 41.66/306.58; base = (41.66/(1-0.1374))/(306.58/(1-0.2099))
print('Q1', cur, base, (cur-base)*100, 'formula', cur*(-0.1374+0.2099)/(1-0.1374)*100)
# Q2
n23 = 15.71/1.5108; t23 = 40.19/(1-0.1822)
print('Q2', n23, t23, n23/t23)
# Q3
q = [sum(prod[0:3]), sum(prod[3:6]), sum(prod[6:9])]
print('Q3', q)
# Q4
print('Q4', sum(nsale[6:9]), sum(nprod[6:9]), sum(nsale[6:9])/sum(nprod[6:9]))
# Q5
gt = [i+1 for i in range(10) if sale[i] > prod[i]]; lt = [i+1 for i in range(10) if sale[i] < prod[i]]
print('Q5A >1', gt, '<1', lt)
print('Q5B avg 1-9 (cum-oct)', (93.02-16.53)/9, 'avg monthly sum', sum(nprod[:9])/9)
print('Q5C share now', 16.53/41.66, 'base', (16.53/1.6045)/(41.66/(1-0.1374)))
print('Q5D', 93.02/306.58, 90.51/305.12)
