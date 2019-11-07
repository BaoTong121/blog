from distutils.core import setup
import glob

setup(name='blog',
      version='1.0',
      description='wwx blog',
      author='wwx',
      author_email='13663020@qq.com',
      url='http://www.wwx.com',
      packages=['blog', 'user', 'post'],
      py_modules=['manage'],
      data_files=glob.glob('templates/*.html') + ['requirements']
    )
