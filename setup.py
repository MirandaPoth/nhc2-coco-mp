from setuptools import setup, find_packages
setup(name='nhc2-coco',
      version='0.1',
      packages = find_packages(),
      package_data={'nhc2_coco': ['coco_ca.pem']},
      include_package_data=True
      )