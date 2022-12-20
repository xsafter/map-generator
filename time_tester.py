import time
import matplotlib.pyplot as plt
import main

fig, ax = plt.subplots(figsize=(5, 3))
fig.subplots_adjust(bottom=0.15, left=0.2)
ax.set_title('Time to generate a map')
ax.set_ylabel('time (ms)')
ax.set_xlabel('map size')
# make up some data
for i in range(15, 200, 10):
    start = time.time()
    main.generate(i, i, 2)
    end = time.time()
    delta = end - start
    #plot the data
    plt.plot(i, delta, 'ro')

# plot
#plt.plot()

plt.gcf().autofmt_xdate()
plt.savefig('time_tester.png')

plt.show()
