from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class WorkloadChart(FigureCanvasQTAgg):

    def __init__(self):

        fig = Figure(figsize=(6,3))

        super().__init__(fig)

        self.axes = fig.add_subplot(111)

    def update_chart(self, rows):

        self.axes.clear()

        if not rows:
            self.draw()
            return

        dates = []

        values = []

        for row in rows:

            dates.append(str(row["date"]))

            values.append(row["patients"])

        self.axes.plot(
            dates,
            values,
            linewidth=3
        )

        self.axes.set_title("Daily Patient Workload")

        self.axes.tick_params(axis="x", rotation=35)

        self.draw()