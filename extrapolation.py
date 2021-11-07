from scipy import interpolate


def extrapolate(xi: list[float], yi: list[float], x: float, n: int):
    kinds = ["linear", "quadratic", "cubic"]
    f = interpolate.interp1d(xi, yi, kind=kinds[n - 1], fill_value="extrapolate")
    return f(x)


if __name__ == "__main__":
    x_table = [1, 2, 3, 4, 5]
    y_table = [5, 10, 15, 20, 50]
    result = extrapolate(x_table, y_table, 6, 3)
    print(result)
