from matplotlib.testing.compare import compare_images
import matplotlib.pyplot as plt
import pytest
import mock
from pathlib import Path
from idealforms.pie import pie


data_dict = {
	'big': 0.5,
	'medium': 0.3,
	'small': 0.13,
	'smaller': 0.04,
	'smallerer': 0.02,
	'smallest': 0.01
}

@pytest.mark.parametrize("data", [data_dict])
class TestPiePlotsOnlyFourValues:
	def test_pie_is_a_plot(self, data):
		fig, ax = pie(
			data, 
			title='Pie', 
			largest_color='xkcd:macaroni and cheese',
			figsize=(4,4)
		)
		assert len(ax.patches) == 4
