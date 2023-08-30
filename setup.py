from setuptools import setup, find_packages

setup(name='clean_folder',
      version='0.0.1',
      packages=find_packages(),
      author='GO_IT_Studen',
      description='Useful package to sort and manage file in required directory',
      entry_points={'console_scripts':['clean-folder = clean_folder.clean:main']})