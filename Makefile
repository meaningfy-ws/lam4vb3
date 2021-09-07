.PHONY: test install lint generate-tests-from-features

#include .env-dev

BUILD_PRINT = \e[1;34mSTEP: \e[0m
#INPUT_EXCEL = resources/input_workbook/LAM_metadata_20200903_JKU.xlsx
#INPUT_EXCEL = resources/input_workbook/LAM_metadata_20210218_ECO.xlsx
#INPUT_EXCEL = resources/input_workbook/LAM_metadata_20210408.xlsx
#INPUT_EXCEL = resources/input_workbook/LAM_metadata_20210413.xlsx
INPUT_EXCEL = resources/input_workbook/LAM_metadata_20210903.xlsx

install:
	@ echo "$(BUILD_PRINT)Installing the requirements"
	@ pip install --upgrade pip
	@ pip install -r requirements.txt
	@ docker pull tinkerpop/gremlin-server

install-dev: install
	@ echo "$(BUILD_PRINT)Installing the requirements"
	@ pip install --upgrade pip
	@ pip install -r requirements-dev.txt

lint:
	@ echo "$(BUILD_PRINT)Linting the code"
	@ flake8 || true

test:
	@ echo "$(BUILD_PRINT)Running the tests"
	@ pytest

start-gremlin:
	@ echo "$(BUILD_PRINT)Starting Test Gremlin server"
	@ docker run -d --name gremlin-server -p 8182:8182 tinkerpop/gremlin-server

stop-gremlin:
	@ echo "$(BUILD_PRINT)Stopping Test Gremlin server"
	@ docker stop gremlin-server || true
	@ docker rm gremlin-server || true

restart-gremlin: | stop-gremlin start-gremlin

# Transformation paipeline

transform-full: | clear transform-excel2rdf transform-rdf2json transform-json2html

transform-excel2rdf:
	@ echo "$(BUILD_PRINT) Transforming Excel file to RDF representation"
	@ python -m lam4vb3.excel2rdf $(INPUT_EXCEL) data

transform-rdf2json:
	@ echo "$(BUILD_PRINT) Transforming RDF into JSON representation"
	@ python -m lam2doc.rdf2json data/celex_project_classes_v2.ttl  data --format json --generate-collections
	@ python -m lam2doc.rdf2json data/lam_project_properties_v2.ttl  data --format json --generate-collections
	@ python -m lam2doc.rdf2json data/lam_project_classes_v2.ttl  data --format json --generate-collections

transform-json2html:
	@ echo "$(BUILD_PRINT) Transforming JSON into HTML representation"
	@ python -m lam2doc.json2html data/celex_project_classes_v2.json --template celex_classes
	@ python -m lam2doc.json2html data/lam_project_properties_v2.json --template lam_properties
	@ python -m lam2doc.json2html data/lam_project_classes_v2.json --template lam_classes

clear:
	@ echo "$(BUILD_PRINT) Clearing the ./data folder, usually useful before a complete transformation chain: Excel-RDF-JSON-HTML"
	@ rm -rf data/*


upload-to-fuseki-meaningfy-ws:
	@ echo "$(BUILD_PRINT) Uploading the datasets to http://srv.meaningfy.ws:3010/"
	@ curl -X DELETE --anyauth --user 'admin:admin' 'http://srv.meaningfy.ws:3010/$$/datasets/lam'
	@ curl --anyauth --user 'admin:admin' -d 'dbType=tdb&dbName=lam'  'http://srv.meaningfy.ws:3010/$$/datasets'
	@ curl -X POST -H content-type:text/turtle -T data/celex_project_classes_v2.ttl -G 'http://srv.meaningfy.ws:3010/lam/data' --data-urlencode 'graph=http://publications.europa.eu/resources/authority/celex/CelexLegalDocument'
	@ curl -X POST -H content-type:text/turtle -T data/lam_project_classes_v2.ttl -G 'http://srv.meaningfy.ws:3010/lam/data' --data-urlencode 'graph=http://publications.europa.eu/resources/authority/lam/LAMLegalDocument'
	@ curl -X POST -H content-type:text/turtle -T data/lam_project_properties_v2.ttl -G 'http://srv.meaningfy.ws:3010/lam/data' --data-urlencode 'graph=http://publications.europa.eu/resources/authority/lam/DocumentProperty'

upload-to-fuseki-localhost:
	@ echo "$(BUILD_PRINT) Uploading the datasets to http://localhost:3010/"
	@ curl -X DELETE --anyauth --user 'admin:admin' 'http://localhost:3010/$$/datasets/lam'
	@ curl --anyauth --user 'admin:admin' -d 'dbType=tdb&dbName=lam'  'http://localhost:3010/$$/datasets'
	@ curl -X POST -H content-type:text/turtle -T data/celex_project_classes_v2.ttl -G 'http://localhost:3010/lam/data' --data-urlencode 'graph=http://publications.europa.eu/resources/authority/celex/CelexLegalDocument'
	@ curl -X POST -H content-type:text/turtle -T data/lam_project_classes_v2.ttl -G 'http://localhost:3010/lam/data' --data-urlencode 'graph=http://publications.europa.eu/resources/authority/lam/LAMLegalDocument'
	@ curl -X POST -H content-type:text/turtle -T data/lam_project_properties_v2.ttl -G 'http://localhost:3010/lam/data' --data-urlencode 'graph=http://publications.europa.eu/resources/authority/lam/DocumentProperty'



# publish-pipy:
#	@ echo "$(BUILD_PRINT)Creating the source distribution"
#	@ python3 setup.py sdist bdist_wheel
#	@ echo "$(BUILD_PRINT)Checking the distribution"
#	@ twine check dist/*
#	@ echo "$(BUILD_PRINT)Uploading the distribution"
#	@ twine upload --skip-existing dist/*
