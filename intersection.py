import portion
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from shapely.geometry import Point, LineString
from scipy.spatial import distance
import sys

# Funkcja wizualizuje rozwiązanie
def plot_intersection(x1, y1, x2, y2, x3, y3, x4, y4, i_x=None, i_y=None):
    x_1 = [x1, x2]
    y_1 = [y1, y2]
    x_2 = [x3, x4]
    y_2 = [y3, y4]
    plt.plot(x_1, y_1, c='b', marker='o')
    plt.plot(x_2, y_2, c='g', marker='o')
    plt.title("Wizualizacja")
    plt.xlabel("OŚ-X")
    plt.ylabel("OŚ-Y")
    plt.scatter(i_x, i_y, s=12, c='r')
    plt.plot(x1)
    plt.show()

# Funkcja oblicza wyznacznik
def determinant(x1, y1, x2, y2):
    result = x1 * y2 - y1 * x2
    return result


def dot_product(x1, y1, x2, y2):
    result = x1 * x2 + y1 * y2
    return result

# Funkcja sprawdzająca czy odcinki przecinają się
# oraz dająca użytkownikowi odpowiedź i punkt przecięcia
def intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    # wektory
    first_third_x = x3 - x1
    first_third_y = y3 - y1
    rx = x2 - x1
    ry = y2 - y1
    sx = x4 - x3
    sy = y4 - y3

    # obliczanie wyznaczników potrzebnych do wykorzystania metody Cramer'a
    numerator_t = determinant(first_third_x, first_third_y, sx, sy)
    numerator_u = determinant(first_third_x, first_third_y, rx, ry)
    denominator = determinant(rx, ry, sx, sy)

    try:
        t = numerator_t / denominator
        u = numerator_u / denominator

        if denominator != 0 and 0 <= t <= 1 and 0 <= u <= 1:
            i_x = x1 + t * rx
            i_y = y1 + u * ry
            msg = f"Odcinek przecina się w punkcie: ({i_x}, {i_y})"
            messagebox.showinfo('Odpowiedź', msg)
            plot_intersection(x1, y1, x2, y2, x3, y3, x4, y4, i_x, i_y)
        else:
            msg = "Odcninki nie przecinają się oraz nie są równoległe.\nKliknij 'OK', żeby wyświetlić wizualizację."
            messagebox.showinfo('Odpowiedź', msg)
            plot_intersection(x1, y1, x2, y2, x3, y3, x4, y4)

    except ZeroDivisionError:
        if denominator == 0 and numerator_u != 0:
            msg = "Odcinki są równoległe.\nKliknij 'OK', żeby wyświetlić wizualizację."
            messagebox.showinfo('Odpowiedź', msg)
            plot_intersection(x1, y1, x2, y2, x3, y3, x4, y4)

        if numerator_u == 0 and denominator == 0:

            # parametry potrzebne do ocenienia wspólniniowości odcinków
            t_0 = dot_product(first_third_x, first_third_y, rx, ry) / dot_product(rx, ry, rx, ry)
            t_1 = t_0 + dot_product(sx, sy, rx, ry) / dot_product(rx, ry, rx, ry)

            # zdefiniowanie punktów oraz odcinków (bibliotek shapely)
            segment_AB = LineString([(x1, y1), (x2, y2)])
            segment_CD = LineString([(x3, y3), (x4, y4)])
            point_A = Point(x1, y1)
            point_B = Point(x2, y2)
            point_C = Point(x3, y3)
            point_D = Point(x4, y4)

            if dot_product(sx, sy, rx, ry) > 0:
                # sprawdzenie czy wyliczone t_0 oraz t_1 mają część wspólną z [0,1]
                interval = portion.closed(t_0, t_1)
                if interval.overlaps(portion.closed(0, 1)):

                    if segment_AB.contains(point_C) and segment_AB.contains(point_D):
                        msg = f"Odcinki są współliniowe i odcinek CD zawiera się w odcinku AB.\n" \
                              f"Przedział wspólny: C({x3}, {y3}) - D({x4}, {y4})\nKliknij 'OK', żeby wyświetlić wizualizację."
                        messagebox.showinfo('Odpowiedź', msg)
                    elif segment_CD.contains(point_A) and segment_CD.contains(point_B):
                        msg = f"Odcinki są współliniowe i odcinek AB zawiera się w odcinku CD.\n" \
                              f"Przedział wspólny: D({x1}, {y1}) - B({x2}, {y2})\nKliknij 'OK', żeby wyświetlić wizualizację."
                        messagebox.showinfo('Odpowiedź', msg)

                    elif segment_AB.contains(point_C):
                        if distance.euclidean(point_D, point_A) > distance.euclidean(point_D, point_B):
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale CB\n" \
                                  f"C({x3}, {y3}) - B({x2}, {y2})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)
                        else:
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale AC\n" \
                                  f"A({x1}, {y1}) - C({x3}, {y3})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)

                    elif segment_AB.contains(point_D):
                        if distance.euclidean(point_C, point_A) > distance.euclidean(point_C, point_B):
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale DB\n" \
                                  f"D({x4}, {y4}) - B({x2}, {y2})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)
                        else:
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale AD\n" \
                                  f"A({x1}, {y1}) - D({x4}, {y4})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)

                    elif segment_CD.contains(point_A):
                        if distance.euclidean(point_B, point_C) > distance.euclidean(point_B, point_D):
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale AD\n" \
                                  f"A({x1}, {y1}) - D({x4}, {y4})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)
                        else:
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale CA\n" \
                                  f"C({x3}, {y3}) - A({x1}, {y1})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)

                    elif segment_CD.contains(point_B):
                        if distance.euclidean(point_A, point_C) > distance.euclidean(point_A, point_D):
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale BD\n" \
                                  f"B({x2}, {y2}) - D({x4}, {y4})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)
                        else:
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale CB\n" \
                                  f"C({x3}, {y3}) - B({x2}, {y2})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)
                else:
                    msg = "Odcinki są współliniowe, ale nie nachodzą na siebie.\nKliknij 'OK', żeby wyświetlić wizualizację."
                    messagebox.showinfo('Odpowiedź', msg)
                plot_intersection(x1, y1, x2, y2, x3, y3, x4, y4)

            if dot_product(sx, sy, rx, ry) < 0:
                interval = portion.closed(t_1, t_0)
                if interval.overlaps(portion.closed(0, 1)):

                    if segment_AB.contains(point_C) and segment_AB.contains(point_D):
                        msg = f"Odcinki są współliniowe i odcinek CD zawiera się w odcinku AB.\n" \
                              f"Przedział wspólny: C({x3}, {y3}) - D({x4}, {y4})\nKliknij 'OK', żeby wyświetlić wizualizację."
                        messagebox.showinfo('Odpowiedź', msg)
                    elif segment_CD.contains(point_A) and segment_CD.contains(point_B):
                        msg = f"Odcinki są współliniowe i odcinek AB zawiera się w odcinku CD.\n" \
                              f"Przedział wspólny: D({x1}, {y1}) - B({x2}, {y2})\nKliknij 'OK', żeby wyświetlić wizualizację."
                        messagebox.showinfo('Odpowiedź', msg)

                    elif segment_AB.contains(point_C):
                        if distance.euclidean(point_D, point_A) > distance.euclidean(point_D, point_B):
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale CB\n" \
                                  f"C({x3}, {y3}) - B({x2}, {y2})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)
                        else:
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale AC\n" \
                                  f"A({x1}, {y1}) - C({x3}, {y3})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)

                    elif segment_AB.contains(point_D):
                        if distance.euclidean(point_C, point_A) > distance.euclidean(point_C, point_B):
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale DB\n" \
                                  f"D({x4}, {y4}) - B({x2}, {y2})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)
                        else:
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale AD\n" \
                                  f"A({x1}, {y1}) - D({x4}, {y4})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)

                    elif segment_CD.contains(point_A):
                        if distance.euclidean(point_B, point_C) > distance.euclidean(point_B, point_D):
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale AD\n" \
                                  f"A({x1}, {y1}) - D({x4}, {y4})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)
                        else:
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale CA\n" \
                                  f"C({x3}, {y3}) - A({x1}, {y1})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)

                    elif segment_CD.contains(point_B):
                        if distance.euclidean(point_A, point_C) > distance.euclidean(point_A, point_D):
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale BD\n" \
                                  f"B({x2}, {y2}) - D({x4}, {y4})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)
                        else:
                            msg = f"Odcinki są współliniowe i pokrywają się w przedziale CB\n" \
                                  f"C({x3}, {y3}) - B({x2}, {y2})\nKliknij 'OK', żeby wyświetlić wizualizację."
                            messagebox.showinfo('Odpowiedź', msg)
                else:
                    msg = "Odcinki są współliniowe, ale nie nachodzą na siebie.\nKliknij 'OK', żeby wyświetlić wizualizację."
                    messagebox.showinfo('Odpowiedź', msg)
                plot_intersection(x1, y1, x2, y2, x3, y3, x4, y4)
    sys.exit()

# funkcja przycisku "sprawdź"
def get_values():
    global x1, y1, x2, y2, x3, y3, x4, y4
    try:
        x1 = float(x1.get())
        y1 = float(y1.get())
        x2 = float(x2.get())
        y2 = float(y2.get())
        x3 = float(x3.get())
        y3 = float(y3.get())
        x4 = float(x4.get())
        y4 = float(y4.get())
        intersection(x1, y1, x2, y2, x3, y3, x4, y4)


    except ValueError:
        msg = "Można wprowadzić tylko liczby (int/float).\nUruchom program raz jeszcze i wprowadz poprawne wartości."
        messagebox.showinfo('ERROR', msg)


sub = Tk()

# GUI
Label(sub, text='Wprowadź współrzędne końców odcinka').grid(row=0, column=1)

Label(sub, text='Punkt A').grid(row=2, column=1)
Label(sub, text='X').grid(row=3, column=0)
x1 = Entry(sub)
x1.grid(row=3, column=1)

Label(sub, text='Y').grid(row=4, column=0)
y1 = Entry(sub)
y1.grid(row=4, column=1)

Label(sub, text='Punkt B').grid(row=6, column=1)
Label(sub, text='X').grid(row=7, column=0)
x2 = Entry(sub)
x2.grid(row=7, column=1)

Label(sub, text='Y').grid(row=8, column=0)
y2 = Entry(sub)
y2.grid(row=8, column=1)

Label(sub, text='Punkt C').grid(row=10, column=1)
Label(sub, text='X').grid(row=11, column=0)
x3 = Entry(sub)
x3.grid(row=11, column=1)

Label(sub, text='Y').grid(row=12, column=0)
y3 = Entry(sub)
y3.grid(row=12, column=1)

Label(sub, text='Punkt D').grid(row=14, column=1)
Label(sub, text='X').grid(row=15, column=0)
x4 = Entry(sub)
x4.grid(row=15, column=1)

Label(sub, text='Y').grid(row=16, column=0)
y4 = Entry(sub)
y4.grid(row=16, column=1)

button = Button(sub, text='Sprawdź', command=get_values)
button.grid(row=18, column=3)

sub.mainloop()
