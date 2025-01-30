Dataset **WoodScape: RGB Fisheye** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzMwOTFfV29vZFNjYXBlOiBSR0IgRmlzaGV5ZS93b29kc2NhcGUtcmdiLWZpc2hleWUtRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiY0lWWXJFdFQwSGZvRlB2R1Vmd29OcjNjVzFveEc2czF6Ri93ZkVjWTY0RT0ifQ==)

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