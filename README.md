# Ideal Forms
## "Some charts I prepared earlier."
Matplotlib charts formatted according to [The Data Visualization Catalogue](https://datavizcatalogue.com/).

## Install
1. ```git checkout https://github.com/ilmcconnell/idealforms.git```
2. ```cd idealforms```
3. ```pip install -e .```

## Bar
```python
import idealforms

categorical_data = dict(apples=500000,
                        oranges=1200000,
                        mangos=2200005)

fig, ax = idealforms.bar(categorical_data,
                         x_label='revenue',
                         y_label='fruit',
                         title='Fruit Revenue',
                         formatter=idealforms.money_formatter)
```
![ideal bar chart image](./docs/demo_fig.png)