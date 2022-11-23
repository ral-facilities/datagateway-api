# Changelog

<!--next-version-placeholder-->

## v6.1.0 (2022-11-23)
### Feature
* Add new entity endpoints for icat5 ([`dc14f9f`](https://github.com/ral-facilities/datagateway-api/commit/dc14f9f8aeb5a9849bc69cf647bf068b04a63d81))

### Documentation
* Updated postman collection with new entities ([`c4b850f`](https://github.com/ral-facilities/datagateway-api/commit/c4b850f913dbded35e6b1a88c8f8d8e1b36cbdec))

## v6.0.0 (2022-11-22)
### Feature
* Enable support for yaml configuration files for DatagatewayAPI ([`46723de`](https://github.com/ral-facilities/datagateway-api/commit/46723de2bf5336244b3dd37808f565e554b5cbdb))
* Add support for yaml configuration ([`02c3e41`](https://github.com/ral-facilities/datagateway-api/commit/02c3e41c92c721d793b27b44c7b27cfb3af6ffbb))

### Breaking
* Remove support for json configuration files  ([`46723de`](https://github.com/ral-facilities/datagateway-api/commit/46723de2bf5336244b3dd37808f565e554b5cbdb))

## v5.3.0 (2022-11-16)
### Feature
* Add warning for no api ([`3c91635`](https://github.com/ral-facilities/datagateway-api/commit/3c91635bc0c3465d456a4a85c8d6c8793df408c2))

## v5.2.0 (2022-11-03)
### Feature
* Add warning that tests only work with ICAT 5 ([`d8825fd`](https://github.com/ral-facilities/datagateway-api/commit/d8825fd71740e2b2d9b387dca175110cee1f9915))
* Changes to tests so they pass with icat 5 ([`73f3c77`](https://github.com/ral-facilities/datagateway-api/commit/73f3c777f8d3841cf09537140922a9bbdd8dad7c))

### Documentation
* Update the poetry installation documentation ([`68d4267`](https://github.com/ral-facilities/datagateway-api/commit/68d426722862613358b0b136188d2b61accdc56f))

## v5.1.1 (2022-09-22)
### Fix
* Update to latest dependencies ([`11a0eeb`](https://github.com/ral-facilities/datagateway-api/commit/11a0eeb3cbc4b5db2a0fa8dcd825dbeceb6ac111))

## v5.1.0 (2022-05-25)
### Feature
* Support skip and limit string parameters on search-api ([`db94b37`](https://github.com/ral-facilities/datagateway-api/commit/db94b375438873969db2d05621d9860a304ca8bd))
* Support skip and limit string parameters on search-api ([`eb74970`](https://github.com/ral-facilities/datagateway-api/commit/eb74970c1a74c6e0bed62460dab5ba5881ba1df7))
* Support skip/limit string parameters on search-api and added testing ([`8c3dde1`](https://github.com/ral-facilities/datagateway-api/commit/8c3dde11deb7614dfd22e6433c24727eeff2f800))
* Support skip/limit string parameters on search-api ([`d601ba7`](https://github.com/ral-facilities/datagateway-api/commit/d601ba7e9b48186e624db4891c503484f8895b2a))

## v5.0.1 (2022-05-16)
### Fix
* Fix internal server error when running DG API on its own #359 ([`b0d3e06`](https://github.com/ral-facilities/datagateway-api/commit/b0d3e064dc842143de7f7f0a31b947122fae9f88))

### Documentation
* Update Swagger Interface section in README ([`e63adf8`](https://github.com/ral-facilities/datagateway-api/commit/e63adf8df372baffe4a3814ea5351eb961064f07))
* Update `flask run` commands in README ([`e85887e`](https://github.com/ral-facilities/datagateway-api/commit/e85887e12bef0a701610c0e198f437a7ff4a8c7b))
* Update README to include note for issue in Python 3.10 ([`72181f6`](https://github.com/ral-facilities/datagateway-api/commit/72181f61677a0fdfb7e5ac9a23a731f55ab4c421))
* Find and replace new instances of master #252 ([`9d6f649`](https://github.com/ral-facilities/datagateway-api/commit/9d6f649538e0e237ff965419737b871cdfd5e1b5))

## v5.0.0 (2022-03-29)
### Feature
* Add configuration option to set authenticator and its credentials in the search API #350 ([`1c30f2f`](https://github.com/ral-facilities/datagateway-api/commit/1c30f2f17c5bdc9a206ce3a41c7da81ce4be3b23))

### Breaking
* This commits adds a mandatory config option, so is a major change.  ([`1c30f2f`](https://github.com/ral-facilities/datagateway-api/commit/1c30f2f17c5bdc9a206ce3a41c7da81ce4be3b23))

## v4.3.0 (2022-03-18)
### Feature
* Allow multiple datetime formats to be used when filtering in search API #338 ([`f20ad24`](https://github.com/ral-facilities/datagateway-api/commit/f20ad24886f85bb3ba70abfd29352b1a7e5c58ff))

### Fix
* Output datetime data in the same format as SciCat #338 ([`4596db9`](https://github.com/ral-facilities/datagateway-api/commit/4596db98808f35488aca86667aa26811d777b58e))

## v4.2.0 (2022-02-28)
### Feature
* Create openapi endpoint for Search API #281 ([`412458c`](https://github.com/ral-facilities/datagateway-api/commit/412458cc4cc73230db0115bdbfdfe6ac815d42c1))

### Documentation
* Add openapi yaml files #281 ([`d4fc795`](https://github.com/ral-facilities/datagateway-api/commit/d4fc79564fec3dd0f128bf30937d8d70c2b03dd3))
* Add docs to `GET` Search API `CountFilesEndpoint` #281 ([`ba367a0`](https://github.com/ral-facilities/datagateway-api/commit/ba367a02f612a042c9c9d274d05b63202534de76))
* Add docs to `GET` Search API `FilesEndpoint` #281 ([`53c2f8c`](https://github.com/ral-facilities/datagateway-api/commit/53c2f8c3d2b71270a881f8ad59aac45a225daadd))
* Add docs to `GET` Search API `CountEndpoint` #281 ([`2e34d7a`](https://github.com/ral-facilities/datagateway-api/commit/2e34d7a0632429baf5c1d48f1044a0f7e979cd0e))
* Add docs to `GET` Search API `EndpointWithID` #281 ([`f211c57`](https://github.com/ral-facilities/datagateway-api/commit/f211c57d668862e469a98c1c4504781fe17e8504))
* Add docs to `GET` Search API `Endpoint` #281 ([`d407f0a`](https://github.com/ral-facilities/datagateway-api/commit/d407f0ad98a72547333f1b1ccb3930c5c39b0926))

## v4.1.5 (2022-02-28)
### Fix
* Fix `AttributeError` when running DG API on its own #345 ([`7479cc3`](https://github.com/ral-facilities/datagateway-api/commit/7479cc3e17ec046082e08b7e71e8e63eb7fa6e28))

## v4.1.4 (2022-02-28)
### Fix
* Improve error handling for search API exceptions #319 ([`935f22d`](https://github.com/ral-facilities/datagateway-api/commit/935f22d31d96c6810cf7938815b25c8822d892fb))

## v4.1.3 (2022-02-28)
### Fix
* Fix `parameters.value` WHERE filter with between operator #270 ([`3fe8dfe`](https://github.com/ral-facilities/datagateway-api/commit/3fe8dfe79ac7e070db369471859b1793e54a0852))

## v4.1.2 (2022-02-28)
### Fix
* Fix requests which include parameters and filter on them #319 ([`598bf9f`](https://github.com/ral-facilities/datagateway-api/commit/598bf9f5c9fbf71b87a3313680617b8addbe5cc9))

### Documentation
* Update README to include resolution to setuptools issue ([`4bab813`](https://github.com/ral-facilities/datagateway-api/commit/4bab813d0897e987e085260d270b0496fe8e85f3))
* Correct markdown URL #320 ([`0a9c05a`](https://github.com/ral-facilities/datagateway-api/commit/0a9c05a4e151e7bf6db5833dfa760d6de576663c))
* Add remaining suggested changes to README #320 ([`d5d358c`](https://github.com/ral-facilities/datagateway-api/commit/d5d358c1f43573be7f0f443d4a20a9bd54a7c634))
* Make suggested changes #320 ([`d04447d`](https://github.com/ral-facilities/datagateway-api/commit/d04447d835e049127ba15ef981f69a63b85ff015))
* Update docs for search API #320 ([`2daf395`](https://github.com/ral-facilities/datagateway-api/commit/2daf3956805dc0476e3d400d52b20a8b51f0e309))

## v4.1.1 (2022-02-17)
### Fix
* Ignore filters on `isPublic` fields #329 ([`d6c10d5`](https://github.com/ral-facilities/datagateway-api/commit/d6c10d56b788ff3c491feaf1fae3a6fadd634a9d))
* Hardcode `isPublic` value to `True` #329 ([`64f62c2`](https://github.com/ral-facilities/datagateway-api/commit/64f62c217de760d22afae3e15d4774173eddbb48))

## v4.1.0 (2022-02-16)
### Feature
* Add search API error formatting as per specification #296 ([`3a5a3e8`](https://github.com/ral-facilities/datagateway-api/commit/3a5a3e83a1a2ce677a50a39b38d71133fea5121a))

## v4.0.1 (2022-02-11)
### Fix
* Use alternative ICAT mapping for Technique pid when pid is None #314 ([`bf1c830`](https://github.com/ral-facilities/datagateway-api/commit/bf1c8305fc73630fbf1e6c4771664d974c72fd93))
* Use alternative ICAT mapping for Instrument pid when pid is None #314 ([`ae7e57a`](https://github.com/ral-facilities/datagateway-api/commit/ae7e57a0c6ece928cbb053ae41ba1214fb3199f8))
* Use alternative ICAT mapping for Document pid when doi is None #314 ([`736c6bd`](https://github.com/ral-facilities/datagateway-api/commit/736c6bdacc06e9ed2f9fff93a157920b66d2b887))
* Use alternative ICAT mapping for Dataset pid when doi is None #314 ([`b813f3d`](https://github.com/ral-facilities/datagateway-api/commit/b813f3d71d312b72c5a602b7520978208bd05754))
* Use alternative ICAT mapping for Sample pid when pid is None #314 ([`7e211f7`](https://github.com/ral-facilities/datagateway-api/commit/7e211f74aa4fa81ab26c339b27806a64510f261c))

## v4.0.0 (2022-02-10)
### Feature
* **config:** Add configuration option for determining public data #312 ([`58e777b`](https://github.com/ral-facilities/datagateway-api/commit/58e777b5c4a562f6945adcd1b55ce1d470f5d816))

### Breaking
* add configuration option for determining public data #312 ([`58e777b`](https://github.com/ral-facilities/datagateway-api/commit/58e777b5c4a562f6945adcd1b55ce1d470f5d816))

## v3.6.1 (2022-02-07)
### Fix
* Convert `isPublic` PaNOSC filter to appropriate ICAT filter #308 ([`6a40307`](https://github.com/ral-facilities/datagateway-api/commit/6a40307ba19d5818bdb6bf1acc79d98abd6a3f83))
* Make WHERE filter without operator work with int and bool #322 ([`6988a5a`](https://github.com/ral-facilities/datagateway-api/commit/6988a5aa5d6dfa71fd4b90a73b050864e8530955))

## v3.6.0 (2022-02-07)
### Feature
* Implement search API endpoints #266, #267, #268 ([`dcc332e`](https://github.com/ral-facilities/datagateway-api/commit/dcc332e352ded8af25dce7dae635bd62417d2c13))

### Fix
* Make get by pid endpoints return data in PaNOSC format #266 ([`0de2b5b`](https://github.com/ral-facilities/datagateway-api/commit/0de2b5b2b713699b66164ca5732888f997230aa5))
* Add logic to deal with `PythonICATIncludeFilter` that could be related for ICAT relations for non-related PaNOSC fields #268 ([`29232c6`](https://github.com/ral-facilities/datagateway-api/commit/29232c6b2c032c61999118b2f69177f3b9bd5d57))
* Correct order of arguments for where filter #266 ([`1e38eae`](https://github.com/ral-facilities/datagateway-api/commit/1e38eaee9f201a45742cf868ad2fa28f4adee065))

### Documentation
* Add docstrings for Flask resource classes #268 ([`a5aee61`](https://github.com/ral-facilities/datagateway-api/commit/a5aee61cc55e70931163371f3c1abecb31b1fb3a))

## v3.5.3 (2022-02-02)
### Fix
* Retrieve non-related fields that have a list of ICAT relations #265 ([`2c5edc5`](https://github.com/ral-facilities/datagateway-api/commit/2c5edc50f9f713b0d15e137ad4a307a90a86b5aa))

## v3.5.2 (2022-02-02)
### Fix
* Make `ne` and `neq` operators work with non-numeric values #315 ([`f5e3b4b`](https://github.com/ral-facilities/datagateway-api/commit/f5e3b4b1bfebd25c6d6fb288eb3f5a79daf87dac))

## v3.5.1 (2022-01-31)
### Fix
* Fix nested relations bug #261 ([`67fcbfe`](https://github.com/ral-facilities/datagateway-api/commit/67fcbfe2a35ca2b7e007a1a6d78105b2e46b0b5f))
* Reference self instead of fixed instance #301 ([`40f5662`](https://github.com/ral-facilities/datagateway-api/commit/40f566279543871c5b7b1eab2c8b74050d8b3525))

## v3.5.0 (2022-01-31)
### Feature
* Implement basic version of `SearchAPIIncludeFilter` #261 ([`f2f53c9`](https://github.com/ral-facilities/datagateway-api/commit/f2f53c92229d052ae697787eb80a35dcd2ea3b45))

### Fix
* Fix list type field checking in Python 3.6 #265 ([`691a59e`](https://github.com/ral-facilities/datagateway-api/commit/691a59ea3f850475572c3a877fb739e5216c6fe7))

### Documentation
* Add new comments and fix existing #265 ([`3f1b1cf`](https://github.com/ral-facilities/datagateway-api/commit/3f1b1cffdd1e57ab4eb1227b13e0906424adefd0))

## v3.4.0 (2022-01-31)
### Feature
* Implement `regexp` operator #297 ([`bf3fe0e`](https://github.com/ral-facilities/datagateway-api/commit/bf3fe0ef2ac582d55dbd881edf6a81a93625ce91))
* Implement `neq` operator #297 ([`9094bbb`](https://github.com/ral-facilities/datagateway-api/commit/9094bbb894ead20a53fadfd0e24b264af29548b9))
* Implement `nin` operator #297 ([`00dbba5`](https://github.com/ral-facilities/datagateway-api/commit/00dbba525d5cd86cb5577f3b1621a7042cdd2fa0))
* Implement `inq` operator #297 ([`fc1cf19`](https://github.com/ral-facilities/datagateway-api/commit/fc1cf194454a4da60652b1f68df278c4624ddc11))
* Implement `between` operator #297 ([`4736888`](https://github.com/ral-facilities/datagateway-api/commit/4736888bf76cda0dbc00f997443ed565f0f5e760))

## v3.3.0 (2022-01-31)
### Feature
* Add function to get PaNOSC to ICAT mapping for where filter #260 ([`34b1d81`](https://github.com/ral-facilities/datagateway-api/commit/34b1d819482aa3efdb4f8da321125d3e40d76617))
* Convert PaNOSC to ICAT for where filter fields #260 ([`ff9595d`](https://github.com/ral-facilities/datagateway-api/commit/ff9595d2f571211db79dea02f702d4148b8879f3))

### Fix
* Fix example mapping file ([`3802cc9`](https://github.com/ral-facilities/datagateway-api/commit/3802cc9ee71a355d0ad87529f65112e8c3f8b881))
* Update `__str__()` for WHERE filter to cope with applying filter #260 ([`8d259d7`](https://github.com/ral-facilities/datagateway-api/commit/8d259d75a28414f26cc569293720ef4e306e6844))

### Documentation
* Add docstring to static function #260 ([`618f6b9`](https://github.com/ral-facilities/datagateway-api/commit/618f6b9fead88f61a346b90cb2b85a90877b0410))

## v3.2.0 (2022-01-31)
### Feature
* Add class to represent nested conditions #259 ([`583cbf2`](https://github.com/ral-facilities/datagateway-api/commit/583cbf29744b72c020429b61ae7442b19acef231))
* Add first pass of query param implementation #259 ([`ee668e3`](https://github.com/ral-facilities/datagateway-api/commit/ee668e38cd43354851163616a93924ad84e14b90))

## v3.1.1 (2021-12-15)
### Fix
* Correct reference to class name #264 ([`fc4c180`](https://github.com/ral-facilities/datagateway-api/commit/fc4c18085ab496d838e8d1e9e3f8c77f07826e9d))

## v3.1.0 (2021-12-06)
### Feature
* Implement session/client handling for search API #258 ([`46a1539`](https://github.com/ral-facilities/datagateway-api/commit/46a1539398f63e9c8a6539d703a164dd7c8749e7))

## v3.0.1 (2021-11-24)
### Fix
* Allow blank extensions and slash extension to be valid ([`70ddb7a`](https://github.com/ral-facilities/datagateway-api/commit/70ddb7a4fd89ba10b06cd71c3ab2a98648cfb773))

## v3.0.0 (2021-11-23)
### Feature
* Configure end part of endpoint urls to contain api extension #283 ([`5bdd72e`](https://github.com/ral-facilities/datagateway-api/commit/5bdd72ea911323cdf0fc7d9ec6fb419b8dd6006c))

### Breaking
* modify endpoint urls to use relevant api extension  ([`5bdd72e`](https://github.com/ral-facilities/datagateway-api/commit/5bdd72ea911323cdf0fc7d9ec6fb419b8dd6006c))

## v2.0.0 (2021-11-22)
### Breaking
* Adding breaking change to correct the version bump which didn't happen when merging #285  ([`44c48e8`](https://github.com/ral-facilities/datagateway-api/commit/44c48e8b772147bfcf395d1430e067730d66df44))

### Documentation
* Adjust versioning documentation ([`44c48e8`](https://github.com/ral-facilities/datagateway-api/commit/44c48e8b772147bfcf395d1430e067730d66df44))

## v1.1.0 (2021-11-19)
### Feature
* Add unimplemented endpoint definitions for search API #257 ([`d0e52d9`](https://github.com/ral-facilities/datagateway-api/commit/d0e52d96dd3b94ce54dcc9b81969e777a196922a))

### Documentation
* Rebuild openapi docs #257 ([`de15357`](https://github.com/ral-facilities/datagateway-api/commit/de1535772db64916f75e16d79be3f3fdf10fc47c))

## v1.0.1 (2021-11-15)
### Fix
* Add PID field for study in DB backend #287 ([`18379be`](https://github.com/ral-facilities/datagateway-api/commit/18379becafd23ff2957e556de2bd3fc210a71f5b))
* Add generation of study.pid #287 ([`f6a8ebc`](https://github.com/ral-facilities/datagateway-api/commit/f6a8ebc6c775ba3f5252d5af5cedc4e1e0e79a40))

### Documentation
* Add study PID to swagger docs #287 ([`89a9e27`](https://github.com/ral-facilities/datagateway-api/commit/89a9e27b72dfe1d474d49a721f128a643ef2ae36))

## v1.0.0 (2021-11-03)
### Breaking
* As the API will be approaching production use soon, this seems like a good opportunity to bump the version to 1.0.0. This also serves as a good test that the introduction of automatic versioning actually works  ([`ccf6d29`](https://github.com/ral-facilities/datagateway-api/commit/ccf6d2974216f8979a03e3e223f7c9e84ced05cb))

### Documentation
* Follow Angular commit message capitalisation #242 ([`d53d85a`](https://github.com/ral-facilities/datagateway-api/commit/d53d85ad46a115ba871c6da8273a242e790c810c))
* Add documentation to explain versioning on this repo #242 ([`ccf6d29`](https://github.com/ral-facilities/datagateway-api/commit/ccf6d2974216f8979a03e3e223f7c9e84ced05cb))
