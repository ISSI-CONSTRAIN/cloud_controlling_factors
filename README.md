# Pipeline to retrieve cloud controlling factors (CCF)

## Access CCFs
Access to the retrieved and calculated CCF is provided through an intake catalog:

```python
import intake
cat = intake.open_catalog("catalog.yaml")  # in case this repo is cloned locally
cat = intake.open_catalog("https://raw.githubusercontent.com/ISSI-CONSTRAIN/cloud_controlling_factors/main/catalog.yaml")  # in case this repo is public
```

The cloud controling dataset of ERA5 can then be opened with
```python
ds = cat['ERA5_CCF_aws_dvc']
```

## Update CCFs
The cloud controlling factors are retrieved and calculated as defined in the [DVC-pipeline](dvc.yaml).
CCFs can be recomputed by running the pipeline again:
```bash
dvc repro
```
In case changed files should be released, they need to be pushed to the remote with `dvc push`.
The `rev`-entry in the `catalog.yaml` needs to be updated as well if present.
