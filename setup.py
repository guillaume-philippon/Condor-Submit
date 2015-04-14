#!/usr/bin/env python
# -*- coding: utf8 -*-fr

from distutils.core import setup

setup(name='Condor-Tools',
      version='1.0',
      description='Set of python script to interact with HTCondor',
      author='Guillaume Philippon',
      author_email='guillaume.philippon@lal.in2p3.fr',
      scripts=["csub"],
      dependency_links=['http://research.cs.wisc.edu/htcondor/downloads/'
                        '?state=select_from_mirror_page&version=8.2.7&'
                        'mirror=UW%20Madison&optional_organization_url=http://'],
      )