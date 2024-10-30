# SacreCOMET

The tool has two functionalities.
First, it creates a signature with your setup and COMET model:

```
pip install sacrecomet

# Without anything will try to detect the local environment and will
# ask you questions about which COMET model you used.
# Example output: Python3.11.8|Comet2.2.2|fp32|unite-mup

sacrecomet 

# Arguments can also be specified non-interactively:

sacrecomet --model unite-mup --prec fp32
```

The other functionality is to find specific citations for COMET models that you're using:

```
sacrecomet cite --model Unbabel/xcomet-xl

https://arxiv.org/abs/2310.10482
@misc{guerreiro2023xcomet,
    title={xCOMET: Transparent Machine Translation Evaluation through Fine-grained Error Detection}, 
    ...
```

You can also list all the available models:
```
sacrecomet list

unbabel/wmt24-qe-task2-baseline
unbabel/wmt22-cometkiwi-da
unbabel/xcomet-xl
unbabel/xcomet-xxl
unbabel/towerinstruct-13b-v0.1
unbabel/towerinstruct-7b-v0.2
unbabel/towerbase-7b-v0.1
...
```

Please open an issue/pull request in the [repository](https://github.com/PinzhenChen/sacreCOMET) if you wish to add models/functionality.


<!-- 
Notes for maintainers:

cd python-tool
# newer version might not work
pip install 'build<0.10.0' twine

python3 -m build

# live
twine upload dist/* -u __token__
# user __token__ as username and the API token generated online
-->