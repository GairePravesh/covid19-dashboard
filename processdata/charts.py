import plotly.graph_objs as go
from plotly.offline import plot

from django.views.generic import TemplateView


from .getdata import filter_by_gender, filter_by_age


class Graph(TemplateView):
    template_name = "pages/graph.html"

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)
        labels = ["Female", "Male"]
        values = filter_by_gender()
        # print(values)
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        div = fig.to_html(full_html=False)
        context["gendergraph"] = div

        d = filter_by_age()
        labels = [d[i][0] for i in range(len(d))]
        values = [d[i][1] for i in range(len(d))]
        fig = go.Figure(
            data=[go.Bar(x=labels, y=values, offsetgroup=0)],
            layout=go.Layout(xaxis_title="Age", yaxis_title="Cases"),
        )
        div = fig.to_html(full_html=False)
        context["agegraph"] = div
        #  District bar graph

        # d = filter_by_districts()
        # labels = [d[i][0] for i in range(len(d))] 
        # values = [d[i][1] for i in range(len(d))]
        # fig = go.Figure(
        #     data=[go.Bar(x=labels, y=values, offsetgroup=0)],
        #     layout=go.Layout(xaxis_title="District Names", yaxis_title="Cases"),
        # )
        # div = fig.to_html(full_html=False)

        # context["districtgraph"] = div
        
        return context
