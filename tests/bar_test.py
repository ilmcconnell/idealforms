from matplotlib.testing.compare import compare_images
import matplotlib.pyplot as plt
import pytest
import mock
from pathlib import Path
from idealforms.bar import bar


data_dict = dict(apples=500000,
                 oranges=1200000,
                 mangos=2200005)

fail_dict = {500000: 'apples',
             1200000: 'oranges',
             2200005: 'mangos'}

comparison_imgs = Path('tests/bar_test_comparison_images/')


@pytest.mark.parametrize("data", [fail_dict])
class TestBarFails:
    def test_bar_reverse_values_and_keys(self, data):
        with pytest.raises(TypeError):
            fig, ax = bar(data,
                          title='title',
                          x_label='x_label',
                          y_label='y_label'
                          )


@pytest.mark.parametrize("data", [data_dict])
class TestBarBasics:
    def test_bar_tick_count(self, data):
        fig, ax = bar(data,
                      title='title',
                      x_label='x_label',
                      y_label='y_label',
                      tick_count=7
                      )
        assert len(ax.get_xticks()) == 7


@pytest.mark.parametrize("data", [data_dict])
class TestBarImages:
    def test_plot_bar_order_bars_by_name(self, data):
        fig, ax = bar(data,
                      title='title',
                      x_label='x_label',
                      y_label='y_label',
                      sort_on='alpha'
                      )
        current_test_image_path = Path('test_image_sort_alpha.png')
        plt.savefig(current_test_image_path)
        different = compare_images(current_test_image_path,
                                   comparison_imgs / 'test_bar_sort_alpha.png',
                                   tol=50)
        current_test_image_path.unlink()
        assert not different

    def test_plot_bar_order_bars_by_value(self, data):
        fig, ax = bar(data,
                      title='title',
                      x_label='x_label',
                      y_label='y_label',
                      sort_on='values',
                      sort_desc=False
                      )
        current_test_image_path = Path('test_image_sort_value.png')
        plt.savefig(current_test_image_path)
        different = compare_images(current_test_image_path,
                                   comparison_imgs / 'test_bar_sort_values.png',
                                   tol=50)
        current_test_image_path.unlink()
        assert not different

    def test_plot_bar_labels_outside_bars(self, data):
        fig, ax = bar(data,
                      title='title',
                      x_label='x_label',
                      y_label='y_label',
                      in_bar_labels=False,
                      sort_on='values',
                      sort_desc=False
                      )
        current_test_image_path = Path('test_image_out_labels.png')
        plt.savefig(current_test_image_path)
        different = compare_images(current_test_image_path,
                                   comparison_imgs / 'test_bar_out_labels.png',
                                   tol=50)
        current_test_image_path.unlink()
        assert not different


def test_main():
    from idealforms.bar import main
    fig, ax = main()
    assert isinstance(fig, plt.Figure) and isinstance(ax, plt.Axes)


def test_init():
    from idealforms import bar
    with mock.patch.object(bar, "main", return_value=100):
        with mock.patch.object(bar, "__name__", "__main__"):
            with mock.patch.object(bar.sys, 'exit') as mock_exit:
                bar.init()
                assert mock_exit.call_args[0][0] == 100
