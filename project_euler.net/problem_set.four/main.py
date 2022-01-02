def pvrple():
	ans = max(p * q
		for p in range(100, 1000)
		for q in range(100, 1000)
		if str(p * q) == str(p * q)[ : : -1])
	return str(ans)


if __name__ == "__main__":
	print(pvrple())
