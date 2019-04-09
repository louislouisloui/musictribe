# Installation
Download the project
```
git clone <placeholder>
```
To optimize the storage, the data source is not included.  
So copy your data into the directory
```
cp DATA_PATH musictric/data
```
Finally run the script with docker-compose
```
cd musictribe && docker-compose up
```
It will run a mongo server accesible on port 27017 and execute the import script.

# Architecture

The service is made of 2 containers handled in a single docker-compose file:
- The app
- The mongo database

## App

The Dockerfile is based ona lightweight python3.7 image.
It implements:
- A builder: extract and format the samples from the files
- A inserter: process and insert the sample raw data in the database

### Builder
The role of the builder is to extract the samples from the JSON and normalize them adding the metadata and the other features common to all the samples in one single file. 

It  also adds the information from the file_name into the sample features.

Adding multi-processing could possibly improve the performances. It is not obvious however since the I/O of reading files of this size is small.

### Inserter
The role of the inserter is to process the raw sample and save it in the mongo. It has the following features:
- Add dynamically any instrument
- Add dynamically train/test set data
- Add dynamically any sample feature
- Feature validation (POC)
- Feature selection/extraction (POC)

It relies on an ORM (mongoengine) and serialization (marshmallow) to process flexibly the documents. A possible improvement is to switch for pure Pymongo to enjoy the native bullks inserts methods.

Some features are working POC I added since they seem to be obvious features even though there were not required.

This could be handled by two interfaces, but given the absence of actual pre-process there was no need for creating 2 interfaces.

Finally we could eventually improve the I/O of the insertion over the database connection using multi-threading.

# Database

Based on a lightweight mongodb image.
It is designed after kaggle files organisation:
- db: test / train
- collection: instrument
- index: 
  - file_id: extracted from the file_name
  - sample_id: extracted from the samples sample_id

# Improvements

- Test multi-threading and multiprocessing
- Test performance of ORM against pure PyMongo, especially native bulk insert
- Interface for feature selection/extraction
- Deacoplate network configs
- Error handling (retry, logs)

# Requirements

- Git
- Docker