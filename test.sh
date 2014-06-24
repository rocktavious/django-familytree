#pip install to virtual env
pip install -r requirements.txt
pip install -r test_requirements.txt
python setup.py install
#run tests with setup.cfg controlling options to nose
python setup.py nosetests
