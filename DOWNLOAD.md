Dataset **WoodScape: RGB Fisheye** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMzA5MV9Xb29kU2NhcGU6IFJHQiBGaXNoZXllL3dvb2RzY2FwZS1yZ2ItZmlzaGV5ZS1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJpa05haU1RRlhaTHBjckY1T2kvUU54MCs0T2pNNXhHbVpnQ3U4aEkrSkFBPSJ9?response-content-disposition=attachment%3B%20filename%3D%22woodscape-rgb-fisheye-DatasetNinja.tar%22)

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