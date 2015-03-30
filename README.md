# maldrolyzer
Simple framework to extract "actionable" data from Android malware (C&amp;Cs, phone numbers etc.)

### Installation
You have to install the following packets before you start using this project:

* Androguard (https://github.com/androguard/androguard)
* PyCrypto (`easy_install pycrypto`)
* pyelftools (`easy_install pyelftools`)

### Architecture
Idea is really simple and modular. The project has couple of directories, which host a place for you static analysis or output processing:
* `plugins` - this is were the code responsible for the malware identification and data extraction is. Every class has to inherit from `Plugin` class from `templates`. 
** Method `recon` idetifies the malware - put there all of the code you need to make sure you can extract the data.
** Method  `extract` does the usual extraction. There is no specific format for the extracted data, but it's good to keep it in Python dictionary, so that the ouput processors could read it in a uniform way.
* `processing` - this is were you put classes that inherit from `OutputProcessor` class. They are invoked after the data extraction and get the extracted info.
** `process` method takes the data and produces some kind of a result (i.e. adds a file or C&amp;C to you database, checks if the C&amp;C is live etc.)

If you want to contribute, write a plugin that decodes some new malware family. It's easy, just look at the existing plugins.

### Usage
So, you have an APK sample and you don't know what it is and where is the C&amp;C? Type:

```
python maldrolyzer.py [sample_path]
```

If maldrolyzer knows the malware family it will display some useful information like:

```
Recognized as Z3Core
Extracted: {'c2': ['http://bn.bmcart.ru/test.php',
        'http://lexsmilefux.link/news/news.php']}
Processor data: {'md5': '03fa8fae3c54989cacc1426b5716eb07',
 'sha1': 'b1eaa55a7402fdcbd6c46e80c066a1400ce6cdc3',
 'sha256': '901979e1d02c9a355fbe80a6a863e6c7684d0e15ec458935e67b1418a00e43d8',
 'sha512': 'f3050de945e44ad2b7945e0f9a163c8bbd98af7b1e08625dfd487c2e79fa31ae28723f77f0ef2114d2190045b43ca9791ddf93981581f1378370483601120301'}
```
