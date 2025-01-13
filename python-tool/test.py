# %%
import subprocess

def test_get_citation():
    output = subprocess.check_output(['sacrecomet', 'cite', '--model', 'unbabel/wmt22-comet-da'])
    output = output.decode('utf-8').split("\n")
    assert output[0] == "https://aclanthology.org/2022.wmt-1.52"

def test_get_version():
    output = subprocess.check_output([
        'sacrecomet',
        '--prec', 'fp32',
        '--model', 'custom-v2',
        '--references', '0',

    ])
    output = output.decode('utf-8').strip()
    assert output == "Python3.11.5|Comet2.2.4|fp32|custom-v2|r0"