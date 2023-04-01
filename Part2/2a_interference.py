import numpy as np


### order: none, cpu, l1d, l1i, l2, llc, membw

def get_mean(data):
    return np.mean(data, axis=1)


def interference_slowdown_ratio(data):
    """
    how much slower the service (parsec) is when the interference is applied
    :param data: service time with interference (none, cpu, l1d, l1i, l2, llc, membw)
    :return: slowdown ratio, where every element is the ratio of
    the service time with the interference to the service time without interference (first element)
    """
    slowdown_ratio = [1]
    for i in range(1, len(data)):
        slowdown = data[i] / data[0]
        # 2 decimal places
        slowdown = round(slowdown, 2)
        slowdown_ratio.append(slowdown)
    return slowdown_ratio



if __name__ == '__main__':

    blackscholes = np.array([[0.836, 0.843],
                             [1.057, 1.106],
                             [1.003, 1.059],
                             [1.310, 1.325],
                             [1.049, 0.967],
                             [1.261, 1.279],
                             [1.117, 1.173]], dtype=np.float64)
    canneal = np.array([[10.353, 10.198],
                        [12.428, 11.868],
                        [11.831, 11.950],
                        [12.641, 12.975],
                        [11.887, 12.668],
                        [19.664, 18.924],
                        [12.822, 13.161]], dtype=np.float64)
    dedup = np.array([[28.148, 26.306],
                      [42.860, 41.603],
                      [30.755, 33.935],
                      [54.998, 57.729],
                      [32.211, 31.122],
                      [56.871, 56.639],
                      [42.858, 43.736]], dtype=np.float64)
    ferret = np.array([[6.045, 6.340],
                       [11.648, 12.280],
                       [6.662, 6.465],
                       [14.660, 14.693],
                       [6.655, 6.687],
                       [16.855, 17.354],
                       [12.737, 13.528]], dtype=np.float64)
    freqmine = np.array([[6.392, 6.884],
                         [13.201, 13.080],
                         [6.389, 7.386],
                         [12.781, 13.166],
                         [6.426, 7.723],
                         [11.173, 12.343],
                         [9.820, 10.434]], dtype=np.float64)
    radix = np.array([[59.345, 62.993],
                      [61.131, 60.337],
                      [59.055, 69.840],
                      [61.234, 61.599],
                      [63.287, 59.893],
                      [82.926, 90.182],
                      [65.202, 60.518]], dtype=np.float64)
    vips = np.array([[105.219, 104.122],
                     [175.032, 187.521],
                     [159.565, 181.034],
                     [200.336, 217.871],
                     [160.595, 179.079],
                     [213.267, 250.613],
                     [174.980, 183.946]], dtype=np.float64)


    print("black scholes normalized", interference_slowdown_ratio(get_mean(blackscholes)))
    print("canneal normalized", interference_slowdown_ratio(get_mean(canneal)))
    print("dedup normalized", interference_slowdown_ratio(get_mean(dedup)))
    print("ferret normalized", interference_slowdown_ratio(get_mean(ferret)))
    print("freqmine normalized", interference_slowdown_ratio(get_mean(freqmine)))
    print("radix normalized", interference_slowdown_ratio(get_mean(radix)))
    print("vips normalized", interference_slowdown_ratio(get_mean(vips)))
