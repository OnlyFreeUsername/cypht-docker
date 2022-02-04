#!python
import subprocess
import argparse
from itertools import chain

dockercmd = 'docker'

parser = argparse.ArgumentParser(description='Create cypht images.')
parser.add_argument('tags', metavar='TAG', nargs='+', help='Version tags to build.')

args = parser.parse_args()

platforms = ['linux/amd64', 'linux/arm64', 'linux/arm/v7']

def pull(image):
    subprocess.run([dockercmd, 'pull', baseimage], check=True)

def build(image, directory, platforms, build_args = None):
    if build_args is None:
        build_args = []
    build_args = list(chain.from_iterable(['--build-arg', f'{arg}={val}'] for (arg, val) in build_args))
    platformlist = ','.join(platforms)
    subprocess.run([dockercmd, 'buildx', 'build', '-f', 'image/Dockerfile', '--platform', platformlist, '-t', image] + build_args + ['--push', directory], check=True)
    

for tag in args.tags:
    targetimage = f'chenio/cypht:{tag}'
    
    #print(f'Pulling base image {baseimage}')
    #pull(baseimage)
    print(f'Building image {targetimage}...')
    build(targetimage, 'image', platforms, [('TAG', tag)])
    
