# Setup

The project was tested with Python 3.4.3.

It makes use of the following packages which can be install through pip.

```
matplotlib
numpy
PyMySQL
pyaudio
scipy
SQLAlchemy
```

pyaudio provides bindings for the portaudio library. I was able to install it
using ```brew install portaudio```

To store the fingeprints it uses a MySQL database which can be configured in the
```config.py``` file. The schema is automatically created if the tables are not
present in the database.
