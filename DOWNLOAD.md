Dataset **WoodScape: RGB Fisheye** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/S/e/ZO/QQHjXv25qOhE6cQkjXHY4b5PZMovWaqnsfkD2NhRuoKvTzULptJ7QL7BrnpEgD2GRaZpT5yU67aZW7RSZ7lAvUsakry8r0YgPYOCh8EvrMVvefGxFNo1O77wgaM2.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='WoodScape: RGB Fisheye', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://woodscape.valeo.com/woodscape/download).