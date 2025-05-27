import matplotlib.pyplot as plt

def generate_bar_chart(data, title, x_label, y_label):
    """
    Gera um gráfico de barras a partir dos dados fornecidos.

    :param data: Um dicionário onde as chaves são os rótulos do eixo X e os valores são os dados do eixo Y.
    :param title: O título do gráfico.
    :param x_label: O rótulo do eixo X.
    :param y_label: O rótulo do eixo Y.
    """
    labels = list(data.keys())
    values = list(data.values())

    plt.bar(labels, values, color='skyblue')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def generate_pie_chart(data, title):
    """
    Gera um gráfico de pizza a partir dos dados fornecidos.

    :param data: Um dicionário onde as chaves são os rótulos e os valores são as proporções.
    :param title: O título do gráfico.
    """
    labels = list(data.keys())
    sizes = list(data.values())

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)
    plt.show()