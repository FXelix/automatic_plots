
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
from scipy.optimize import curve_fit


def r_squared_calculation(x_values, y_values):
    lin_fit = np.polyfit(x_values, y_values, 1)
    y_mean_line = np.array([mean(y_values) for _ in y_values])
    y_hat = np.array([(np.polyval(lin_fit, x)) for x in x_values])

    rss = sum((y_values - y_hat)**2)
    tss = sum((y_values - y_mean_line)**2)

    return 1 - (rss/tss)


def customisation():

    while True:
            regression_type = input("What type of regression do you want[linear, squared, e]? Else hit enter: ").lower()
            if regression_type not in ["linear", "squared", "e", ""]:
                print("Choose: linear, sqaured, e or hit enter.")
                continue
            break

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
    return regression_type, errorbar, title, legend, x_axis, y_axis


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

            regression_type, errorbar, title, legend, x_axis, y_axis = customisation()
            make_plot(xs, ys, regression_type, r_squared, errorbar, title, legend, x_axis, y_axis)
            break

        else:
            print("Invalid answer.")
            continue


def make_plot(x_values, y_values, regression_type, r_squared, fig_y_error, fig_title, fig_legend, x_axis_desc, y_axis_desc):

    axis = plt.subplot(111)
    axis.spines["left"].set_color("grey")
    axis.spines["right"].set_color("grey")
    axis.spines["top"].set_color("grey")
    axis.spines["bottom"].set_color("grey")
    axis.grid(color="grey", linestyle="-", linewidth=1, alpha=0.3)

    data_plot = plt.scatter(x_values, y_values, color="black")
    plt.errorbar(x_values, y_values, yerr=fig_y_error, fmt="none", capsize=3, color="black")
    plt.xlabel(x_axis_desc)
    plt.ylabel(y_axis_desc)
    if regression_type == "":
        plt.title(fig_title)
        plt.legend([data_plot], [fig_legend])

        plt.xlim(min(0, min(x_values) - 1), )
        plt.ylim(min(0, min(y_values) - 1), )

    else:

        plt.title("{}\nR²-Wert={}".format(fig_title, r_squared))
        xp = np.linspace(0, len(y_values)+round(len(y_values)/5))  # 10% Prediction Vorschau

        if regression_type == "linear":
            lin_fit = np.polyfit(x_values, y_values, 1)
            regression_data = np.polyval(lin_fit, xp)
            regression_plot, = plt.plot(xp, regression_data, color="orangered")  # das Komma da ist wichtig
            plt.legend([data_plot, regression_plot], [fig_legend, "{:.2f}x + {:.2f}".format(lin_fit[0], lin_fit[1])])

        elif regression_type == "squared":
            squared_fit = np.polyfit(x_values, y_values, 2)
            regression_data = np.polyval(squared_fit, xp)
            regression_plot, = plt.plot(xp, regression_data, color="orangered")  # das Komma da ist wichtig
            plt.legend([data_plot, regression_plot], [fig_legend, "{:.2f}x^2 + {:.2f}x + {:.2f}".format(squared_fit[0], squared_fit[1], squared_fit[2])])

        elif regression_type == "e":


            def exponential(x, a, b, c):
                return a*np.exp(b*x)+c


            params, extra = curve_fit(exponential, x_values, y_values)
            regression_plot, = plt.plot(xp, exponential(xp, params[0], params[1], params[2]), color="orangered")
            plt.legend([data_plot, regression_plot], [fig_legend, "{:.2f}*e^({:.2f}x)+{:.2f}".format(params[0], params[1], params[2])])


    plt.savefig(fig_title)  # before show is important
    plt.show()


get_information()
