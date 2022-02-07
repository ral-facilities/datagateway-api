# Changelog

<!--next-version-placeholder-->

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
