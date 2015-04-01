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
 * Method `recon` idetifies the malware - put there all of the code you need to make sure you can extract the data.
 * Method  `extract` does the usual extraction. There is no specific format for the extracted data, but it's good to keep it in Python dictionary, so that the ouput processors could read it in a uniform way.
* `processing` - this is were you put classes that inherit from `OutputProcessor` class. They are invoked after the data extraction and get the extracted info.
 * `process` method takes the data and produces some kind of a result (i.e. adds a file or C&amp;C to you database, checks if the C&amp;C is live etc.)

If you want to contribute, write a plugin that decodes some new malware family. It's easy, just look at the existing plugins.

### Usage
So, you have an APK sample and you don't know what it is and where is the C&amp;C? Type:

```
python maldrolyzer.py [sample_path]
```

If maldrolyzer knows the malware family it will display some useful information like:

```
{'c2': ['http://esaphapss.net/bn/save_message.php'],
 'malware': 'xbot007',
 'md5': 'ce17e4b04536deac4672b98fbee905e0',
 'sha1': 'a48a2b8a5e1cae168ea42bd271f5b5a0c65f59a9',
 'sha256': 'c3a24d1df11baf2614d7b934afba897ce282f961e2988ac7fa85e270e3b3ea7d',
 'sha512': 'a47f3db765bff9a8d794031632a3cf98bffb3e833f90639b18be7e4642845da2ee106a8947338b9244f50b918a32f1a6a952bb18a1f86f8c176e81c2cb4862b9'}
```
And you can track the C&Cs from several malware families using http://amtrckr.info
