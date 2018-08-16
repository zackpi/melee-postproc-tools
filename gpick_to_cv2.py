import sys

low = [int(i) for i in sys.argv[1].split(",")]
high = [int(i) for i in sys.argv[2].split(",")]

low = 255*low[0]//360, 255*low[1]//100, 255*low[2]//100
high = 255*high[0]//360, 255*high[1]//100, 255*high[2]//100

print(low,",",high)
