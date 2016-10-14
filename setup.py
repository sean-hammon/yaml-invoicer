from setuptools import setup

setup(name='invoicer',
      version="0.1",
      description='Generate PDF invoices from YAML files.',
      author='Sean Hammon',
      author_email='git@sean-hammon.com',
      license='MIT',
      packages=['invoicer'],
      install_requires=[
          'reportlab',
          'ruamel.yaml',
          'arrow'
      ],
      zip_safe=False)
