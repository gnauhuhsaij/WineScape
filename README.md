# WineScape: Wine Quality Prediction and Customization Platform

WineScape is an innovative web application that allows wine enthusiasts to learn about various wine characteristics, create custom wine blends, and receive AI-powered predictive quality ratings.

## Features

- **Interactive Wine Customization**: Adjust characteristics like acidity, sweetness, etc., to create your own wine blend.
- **AI-Driven Quality Prediction**: Get instant quality predictions for your custom blends using our neural network model.
- **Educational Content**: Learn about different aspects of wines and what influences their taste and quality.
- **Community Engagement**: Share and discuss your custom blends with other wine enthusiasts.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You'll need to have Python installed on your system. This project is built using Django, so familiarity with Django's basic concepts is beneficial.

### Installation

1. **Clone the Repository**
   
git clone https://github.com/your-username/winescape.git

2. **Set Up a Virtual Environment** (Optional but recommended)

python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate

3. **Install Required Packages**

pip install -r requirements.txt

4. **Migrate Database** 

python manage.py migrate


5. **Run the Application**

python manage.py runserver


The application will be available at `http://localhost:8000`.

## Usage

- **Home Page**: Start by visiting the home page where you can navigate to different sections of the application.
- **Learn and Explore**: Select existing wines to learn more about wine features.
- **Create Blend**: Select "customize" to customize your wine blend.
- **Quality Prediction**: After customizing, get an instant quality prediction for your blend.
 - Predictions are made by a neural-network-based model. After finetuning, it achieves around 60% accuracy and 96% accuracy within plus and minus one margin of error.
 - Model Training, EDA, and Data Visualization were implemented on SingleStore.


## Authors

- **Jiashu Huang** - *Initial work* - [gnauhuhsaij](https://github.com/gnauhuhsaij)

