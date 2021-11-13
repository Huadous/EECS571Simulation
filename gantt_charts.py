import plotly.express as px
import pandas as pd
import task

def gantt_chart_generate(taskqueue):
    """[Based on the taskqueue and can use the function provided by the scheduler to generate the gantt chart to
    show the scheduling status of each GPU]

    Args:
        taskqueue ([type]): [the queue of tasks and it contains the tasks]
    """