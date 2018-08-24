from distutils.core import setup

setup(name='miniflux-cli',
      version='0.0.1',
      description='Small client for miniflux2 RSS reader',
      author='alexcleac',
      author_email='alexcleac@nesterenko.xyz',
      packages=['miniflux_cli', 'miniflux_cli.meta', 'miniflux_cli.contexts'],
      scripts=['bin/mcli'])
