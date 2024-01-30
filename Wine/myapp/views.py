# myapp/views.py
from django.shortcuts import render, redirect
from .forms import WineSelectionForm
from .utils import get_wine_data_from_csv
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
from .utils import extract_wine_features





def home(request):
    form = WineSelectionForm()
    return render(request, 'home.html', {'form': form})

def wine_details(request, wine_name, customize):
    # Read the wine data from the CSV file
    if (customize != "0"):
        context = {
            'wine_name': wine_name,
            'wine_features': extract_wine_features(customize),  # Assuming the first column is wine_name
        }
    else:
        wine_data = get_wine_data_from_csv(wine_name)  # You'll need to implement this function
        context = {
            'wine_name': wine_name,
            'wine_features': wine_data,  # Assuming the first column is wine_name
        }

    return render(request, 'wine_details.html', context)

def feature_details(request, wine_name, feature_name):
    # Assume you have a DataFrame `wine_df` with your wine data
    # and a way to get the specific value for the current wine's feature
    wine_data = pd.read_csv("datasetup/wine.csv", index_col=0)
    feature_value = wine_data.get(feature_name)[wine_name]
    wine_quality = wine_data.loc[wine_name, 'quality']

    # Create a histogram & KDE plot
    fig = px.histogram(wine_data, x=feature_name, color="quality", marginal="rug", histnorm="percent", barmode ="overlay")

    for trace in fig.data:
        trace.update(opacity=1)

    for trace in fig.data:
        if int(trace.name) == wine_quality:
            vcolor = trace.marker.color
            break

    # Add KDE lines for each quality
    qualities = wine_data['quality'].unique()
    for quality in qualities:
        quality_data = wine_data[wine_data['quality'] == quality][feature_name]
        kde = gaussian_kde(quality_data)
        x_range = quality_data.max() - quality_data.min()
        kde_line = go.Scatter(x=np.linspace(quality_data.min(), quality_data.max(), 200),
                            y=2*x_range*kde(np.linspace(quality_data.min(), quality_data.max(), 200)),
                            mode='lines',
                            line=dict(width=2),
                            showlegend=False)

        # Find color for this quality
        for trace in fig.data:
            if trace.name == str(quality):
                kde_line.line.color = trace.marker.color
                break

        fig.add_trace(kde_line)

    fig.add_vline(x=feature_value, line_width=3, line_dash="dash", line_color=vcolor)

    # Convert Plotly figure to HTML
    plot_div = plot(fig, output_type='div')

    context = {
        'wine_name': wine_name,
        'feature_name': feature_name,
        'feature_value': feature_value,
        'plot_div': plot_div,
    }
    return render(request, 'feature_details.html', context)

def quality(request, wine_name):
    # Assume you have a DataFrame `wine_df` with your wine data
    # and a way to get the specific value for the current wine's feature
    wine_data = pd.read_csv("datasetup/wine.csv", index_col=0)
    wine_quality = wine_data.loc[wine_name, 'quality']

    q = wine_data.groupby(by=["quality"]).size().reset_index(name="counts")
    # Create a histogram & KDE plot
    fig = px.bar(q, x='quality', y = 'counts', color = 'counts', title='Count of Wines by Quality')
    quality_values = wine_data['quality'].unique()
    quality_index = list(quality_values).index(wine_quality)

    # Default color sequence in Plotly (or use your custom color sequence)
    color_sequence = px.colors.qualitative.Plotly
    vline_color = color_sequence[quality_index % len(color_sequence)]

    # Add the vertical line
    fig.add_vline(x=wine_quality, line_width=3, line_dash="dash", line_color=vline_color)
    # Convert Plotly figure to HTML
    plot_div = plot(fig, output_type='div')

    context = {
        'wine_name': wine_name,
        'feature_name': "quality",
        'feature_value': wine_quality,
        'plot_div': plot_div,
    }
    return render(request, 'quality.html', context)

def features(request, wine_name, feature_name):
    # Load your dataset
    wine_data = pd.read_csv("datasetup/wine.csv", index_col=0)
    columns = list(wine_data.columns)
    description = ["Fixed acidity refers to the total amount of non-volatile acids present in the wine, primarily tartaric acid. It plays a significant role in determining the wine's overall acidity and taste profile.",
                "Volatile acidity measures the presence of volatile acids, such as acetic acid, in the wine. High levels can result in unpleasant vinegar-like flavors and aromas.",
                "Citric acid is a naturally occurring acid found in citrus fruits. In wine, it can contribute to acidity and add a refreshing, citrusy quality.",
                "Residual sugar is the amount of sugar remaining in the wine after fermentation. It influences the wine's sweetness, with higher levels resulting in sweeter wines.",
                "Chlorides in wine can contribute to its saltiness or minerality. Excessive levels can negatively affect the wine's balance and flavor.",
                "Free sulfur dioxide is used as a preservative in winemaking to prevent spoilage and oxidation. It helps maintain the wine's freshness and stability.",
                "Total sulfur dioxide includes both free and bound sulfur dioxide. It is an important measure of a wine's sulfur dioxide content, which affects its shelf life and aging potential.",
                "Density is a measure of how heavy the wine is compared to an equal volume of water. It can provide insights into the wine's body and texture.",
                "pH measures the acidity or alkalinity of the wine. It affects the wine's stability and influences the taste, with lower pH wines being more acidic.",
                "Sulphates, specifically potassium sulfate, are used in winemaking as a stabilizer and antioxidant. They can enhance the wine's color and protect it from spoilage.",
                "Alcohol content is the percentage of alcohol by volume in the wine. It contributes to the wine's body, sweetness, and overall balance.",
                "Quality is a subjective measure that assesses the overall excellence of the wine. It takes into account various sensory characteristics, including taste, aroma, and mouthfeel, to determine the wine's overall appeal and grade."]
    subtexts = {}
    for i in range(len(columns)):
        subtexts[columns[i]] = description[i]

    # Extract the feature values and find wines with extreme values
    max_wine = wine_data.nlargest(3, feature_name)
    min_wine = wine_data.nsmallest(3, feature_name)
    
    # Assuming 'wine_name' is a column in your dataset
    max_wine_name = list(max_wine.index)
    min_wine_name = list(min_wine.index)

    # Generate the boxplot
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    fig = px.box(wine_data, x="quality", y=feature_name, color="quality", color_discrete_sequence=colors)
    plot_div = plot(fig, output_type='div')

    # Subtext or description for the feature (update as needed)
    subtext = subtexts[feature_name]

    context = {
        'feature_name': feature_name,
        'subtext': subtext,
        'max1': max_wine_name[0],
        'max2': max_wine_name[1],
        'max3': max_wine_name[2],
        'min1': min_wine_name[0],
        'min2': min_wine_name[1],
        'min3': min_wine_name[2],
        'plot_div': plot_div,
        'wine_name': wine_name,
    }

    return render(request, 'features.html', context)

def customize(request):
    wine_data = pd.read_csv("datasetup/wine.csv", index_col=0)
    columns = list(wine_data.columns)
    context = {
        'wine_features': columns,
    }
    return render(request, 'customize.html', context)

def process_form(request):
    if request.method == 'POST':
        # Get the selected wine from the form data (replace 'wine_select' with the actual field name)
        selected_wine_name = request.POST.get('wine_select')
        # Perform any necessary processing here
        # Redirect to the wine details page for the selected wine
        if (selected_wine_name == "CUSTOM"):
            return redirect('customize')
        else:
            return redirect('wine_details', wine_name=selected_wine_name, customize = 0)
    else:
        return render(request, 'error_page.html', {'message': 'Invalid form submission'})