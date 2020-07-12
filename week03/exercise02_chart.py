from bokeh.plotting import figure, output_file, show
import sqlite3


def salaries_of(location):
    with sqlite3.connect("lagou.db") as conn:
        c = conn.cursor()
        c.execute(
            "select salary_low, salary_high from positions where location=? order by salary_low asc",
            (location,),
        )
        return c.fetchall()


if __name__ == "__main__":
    output_file("salaries.html")
    p = figure(title="Python salaries", plot_width=1024)
    gz = salaries_of("广州")
    bj = salaries_of("北京")
    sh = salaries_of("上海")
    sz = salaries_of("深圳")
    p.line(
        list(range(1, len(gz) + 1)),
        [i[0] for i in gz],
        line_color="navy",
        legend_label="广州低",
    )
    p.line(
        list(range(1, len(gz) + 1)),
        [i[1] for i in gz],
        line_color="navy",
        legend_label="广州高",
    )
    p.line(
        list(range(1, len(bj) + 1)),
        [i[0] for i in bj],
        line_color="red",
        legend_label="北京低",
    )
    p.line(
        list(range(1, len(bj) + 1)),
        [i[1] for i in bj],
        line_color="red",
        legend_label="北京高",
    )
    p.line(
        list(range(1, len(sz,) + 1)),
        [i[0] for i in sz],
        line_color="green",
        legend_label="深圳低",
    )
    p.line(
        list(range(1, len(sz) + 1)),
        [i[1] for i in sz],
        line_color="green",
        legend_label="深圳高",
    )
    p.line(
        list(range(1, len(sh) + 1)),
        [i[0] for i in sh],
        line_color="yellow",
        legend_label="上海低",
    )
    p.line(
        list(range(1, len(sh) + 1)),
        [i[1] for i in sh],
        line_color="yellow",
        legend_label="上海高",
    )
    show(p)
