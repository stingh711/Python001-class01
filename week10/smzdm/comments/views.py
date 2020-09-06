from django.shortcuts import render
from comments.models import Product, Comment
import plotly.offline as opy
import plotly.graph_objs as go


def home(request):
    return render(request, "comments/home.html")


def list_products(request):
    products = Product.objects.all()
    return render(request, "comments/products.html", {"products": products})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    affirmative = product.comments.filter(sentiments__gt=0.5).all()
    middle = product.comments.filter(sentiments=0.5).all()
    negative = product.comments.filter(sentiments__lt=0.5).all()
    labels = ["正面", "负面", "中性"]
    values = [affirmative.count(), negative.count(), middle.count()]
    figure = go.Figure(data=[go.Pie(labels=labels, values=values)])
    div = opy.plot(figure, auto_open=False, output_type="div")
    return render(
        request,
        "comments/product.html",
        {
            "product": product,
            "affirmative": affirmative,
            "negative": negative,
            "middle": middle,
            "graph": div,
        },
    )


def list_comments(request):
    comments = Comment.objects.all()
    term = request.GET.get("term", None)
    if term:
        comments = comments.filter(content__icontains=term)

    start_date = request.GET.get("start_date", None)
    if start_date:
        comments = comments.filter(timestamp__gte=start_date)
    end_date = request.GET.get("end_date", None)
    return render(request, "comments/comments.html", {"comments": comments})
