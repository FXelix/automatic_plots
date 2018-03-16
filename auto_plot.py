
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean


def r_squared_calculation(x_values, y_values):
    lin_fit = np.polyfit(x_values, y_values, 1)
    y_mean_line = np.array([mean(y_values) for _ in y_values])
    y_hat = np.array([(np.polyval(lin_fit, x)) for x in x_values])

    rss = sum((y_values - y_hat)**2)
    tss = sum((y_values - y_mean_line)**2)

    return 1 - (rss/tss)


def customisation():
    fit_linear = input("Do you want a linear regression [y/n]?: ")
    linear = True if fit_linear.lower() == "y" else False
    while True:
        try:
            errorbar = float(input("Add y-error size: "))
            break
        except ValueError:
            print("Errorbar size must be an integer or float.")
            continue
    title = input("Input plot title: ")
    legend = input("Input graph description: ")
    x_axis = input("Input X-Axis label: ")
    y_axis = input("Input Y-Axis label: ")
    return linear, errorbar, title, legend, x_axis, y_axis


def get_information():
    print("This program will turn data into plots. You may specify your needs.")
    while True:
        data_format = input("Direct data[y/n]?: ")
        if data_format.lower() == "y":
            x_list = list(map(int, input("Input x values with spaces: ").split()))
            y_list = list(map(int, input("Input y values with spaces: ").split()))

            r_squared = r_squared_calculation(x_list, np.array(y_list))

            linear, errorbar, title, legend, x_axis, y_axis = customisation()
            make_plot(x_list, y_list, linear, r_squared, errorbar, title, legend, x_axis, y_axis)
            break

        if data_format.lower() == "n":
            while True:
                try:
                    data_path = input("Input data path: ")
                    file_delimiter = input("Input file delimiter: ")
                    xs, ys = np.loadtxt(data_path, delimiter=file_delimiter, unpack=True)
                    break
                except ValueError:
                    print("Wrong delimiter.")
                    continue
                except OSError:
                    print("File does not exist.")
                    continue

            r_squared = r_squared_calculation(xs, ys)

            linear, errorbar, title, legend, x_axis, y_axis = customisation()
            make_plot(xs, ys, linear, r_squared, errorbar, title, legend, x_axis, y_axis)
            break

        else:
            print("Invalid answer.")
            continue


def make_plot(x_values, y_values, fig_linear, r_squared, fig_y_error, fig_title, fig_legend, x_axis_desc, y_axis_desc):

    data_plot = plt.scatter(x_values, y_values, color="black")
    plt.errorbar(x_values, y_values, yerr=fig_y_error, fmt="none", capsize=3, color="black")
    plt.xlabel(x_axis_desc)
    plt.ylabel(y_axis_desc)

    if fig_linear:
        plt.title("{}\nR²-Wert={}".format(fig_title, r_squared))

        plt.xlim(min(0, min(x_values) - 1), )
        plt.ylim(min(0, min(y_values) - 1), )

        xp = np.linspace(0, len(y_values))
        lin_fit = np.polyfit(x_values, y_values, 1)

        regression_data = np.polyval(lin_fit, xp)
        regression_plot, = plt.plot(xp, regression_data, color="orangered", linestyle="--")  # das Komma da ist wichtig
        plt.legend([data_plot, regression_plot], [fig_legend, "{:.2f}x + {:.2f}".format(lin_fit[0], lin_fit[1])])
    else:
        plt.title(fig_title)
        plt.legend([data_plot], [fig_legend])

    plt.savefig(fig_title)  # before show is important
    plt.show()


get_information()
