import subprocess

from local_config import script

base_url = 'https://pub-726b01260c98468a9387cc0dfcb7386b.r2.dev'
sources = ['osm', 'wikipedia', 'wikidata']

def run(command):
    print(command)
    subprocess.run(command, shell=True)

def download(source, script):
    command = f'wget {base_url}/{source}-{script}-corpus.txt.zip -O corpus/{source}-{script}-corpus.txt.zip'
    run(command)

def unzip(source, script):
    command = f'unzip corpus/{source}-{script}-corpus.txt.zip -d corpus'
    run(command)

def merge(sources, script):
    paths = [f'corpus/{source}/{source}-{script}-corpus.txt' for source in sources]
    command = f'cat {" ".join(paths)} > corpus/{script}.txt'
    run(command)

def clean(sources):
    for source in sources:
        command = f'rm -rf corpus/{source}'
        run(command)
    command = f'rm -rf corpus/*.zip'
    run(command)

for source in sources:
    download(source, script)
    unzip(source, script)

merge(sources, script)
clean(sources)
