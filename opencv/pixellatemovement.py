l=[1, 2, 9, 16, 23, 24, 25, 26, 19, 12, 5, 4]
for i in range(len(l)-1):
	if i==0:
		print('s,m')
	else:
		if l[i+1]-l[i]==1 and l[i]-l[i-1]==1 or l[i+1]-l[i]==7 and l[i]-l[i-1]==7:
			print('s,m')
		elif l[i+1]-l[i]==7 and l[i]-l[i-1]==1 or l[i+1]-l[i]==1 and l[i]-l[i-1]==-7:
			print('l,m')
		elif l[i+1]-l[i]==1 and l[i]-l[i-1]==7 or l[i+1]-l[i]==-7 and l[i]-l[i-1]==1:
			print('r,m')
		elif l[i+1]-l[i]==-7 and l[i]-l[i-1]==-7:
			print('s,m')
		elif l[i+1]-l[i]==-1 and l[i]-l[i-1]==-7:
			print('r,m')
		