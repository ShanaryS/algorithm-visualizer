import matplotlib.pyplot as plt

values = [4, 89, 1, 9, 69, 49, 149, 84, 15, 15, 79, 41, 9, 62, 19]
values.sort()
names = [str(i) for i in values]
key = 51


def linear(v, k):
    for i in range(len(v)):
        if v[i] != k:
            test[i].set_color('r')
            plt.pause(0.1)
        else:
            return i


# test[linear(values, key)].set_color('g')
# plt.show()


def binary(v, k, high=None):
    low = 0
    if not high:
        high = len(v)
    mid = (high + low) // 2

    while high >= low:
        mid = (high + low) // 2
        test[mid].set_color('y')
        plt.pause(1)

        if v[mid] > k:
            if high < len(v)-2:
                upper = high+1
            else:
                upper = high
            for i in range(mid, upper):
                test[i].set_color('r')
            high = mid - 1
        elif v[mid] < k:
            if low > 1:
                lower = low-1
            else:
                lower = low
            for i in range(lower, mid):
                test[i].set_color('r')
            low = mid + 1
        else:
            for i in range(low-1, mid):
                test[i].set_color('r')
            return mid

    return -mid


test = plt.bar(names, values)
plt.suptitle('Yellow is pivot - Red is not valid - Green is found value')
res = binary(values, key)
if res > -1:
    test[res].set_color('g')
else:
    test[-res].set_color('r')
plt.show()
