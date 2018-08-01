from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
      name = 'PrimeTest',
      ext_modules=[
                   Extension('MaccContourCalculations', ['Dropbox/RamanLISTSchober_v0.1.0/PythonResources/MaccContourCalculations.pyx']),
                   Extension('MaccDataClass', ['Dropbox/RamanLISTSchober_v0.1.0/PythonResources/MaccDataClass.pyx']),
                   Extension('MaccSimplePlot', ['Dropbox/RamanLISTSchober_v0.1.0/PythonResources/MaccSimplePlot.pyx'])
                   ],
      cmdclass = {'build_ext': build_ext}
      )




