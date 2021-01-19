from setuptools import setup, find_packages
setup(name='nhc2-coco',
      version='0.1',
      packages = find_packages(),
      data_files=[('nhc2_coco', ['nhc2_coco/coco_ca.pem'])]
      )