# CHANGELOG



## v9.0.2 (2024-01-04)

### Ci

* ci: Ignore Safety vulnerabilities #467

- As normal, we can&#39;t upgrade because all patched versions have dropped support for Python 3.6 ([`05b3e13`](https://github.com/ral-facilities/datagateway-api/commit/05b3e13c64fef1913b5cc15ba9d32fe112f322a6))

* ci: Add job to test that the API can be installed via Pip #467 ([`8c2258d`](https://github.com/ral-facilities/datagateway-api/commit/8c2258d3c9abe2ba149a893b335465efa67cb6e5))

### Fix

* fix: Pin Flask to 2.0.3 in `pyproject.toml` #467

- This will ensure this version is used when the API is installed via Pip ([`50dd13c`](https://github.com/ral-facilities/datagateway-api/commit/50dd13cdde39fbddd04a2504578d3ecf57cb5f33))

### Unknown

* Merge pull request #468 from ral-facilities/pip-install-#467

Fix Pip Install Issues ([`2d7736f`](https://github.com/ral-facilities/datagateway-api/commit/2d7736f7300ae0640772b57333638a2d3a962e34))


## v9.0.1 (2023-09-07)

### Ci

* ci: fix Safety CI job

- As ever, we&#39;re having to ignore these vulnerabilities as patched versions don&#39;t support Python 3.6 ([`04c3eaf`](https://github.com/ral-facilities/datagateway-api/commit/04c3eaf6a35466ad77d2b0551ca2b994be8ea040))

### Fix

* fix: Make `DataPublicationDate.date` to be different to `DataPublication.publicationDate` #444 ([`312c466`](https://github.com/ral-facilities/datagateway-api/commit/312c466030c0e12131fd575011da273c8b5a267c))

### Unknown

* Merge pull request #447 from ral-facilities/bugfix/data-publication-dates-#444

 fix: #444 Generate publication dates between two specific dates ([`b21002e`](https://github.com/ral-facilities/datagateway-api/commit/b21002ee55d869a69f178267ff12368f428776c0))


## v9.0.0 (2023-09-01)

### Breaking

* feat!: Remove code and references to ISIS specific table endpoints #432 ([`12e0304`](https://github.com/ral-facilities/datagateway-api/commit/12e030494c1fc658b36c23c55bd73be780079dba))

### Build

* build(deps): bump python-semantic-release/python-semantic-release

Bumps [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release) from 7.34.4 to 8.0.8.
- [Release notes](https://github.com/python-semantic-release/python-semantic-release/releases)
- [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.md)
- [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/1aed73030dfc573d11ac590f7b7243a0f390b0fc...3abfb7ac216b9ad439de24fda60eca84038e850e)

---
updated-dependencies:
- dependency-name: python-semantic-release/python-semantic-release
  dependency-type: direct:production
  update-type: version-update:semver-major
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`7216beb`](https://github.com/ral-facilities/datagateway-api/commit/7216beb0dc6fd43de41bf37d9163b4c14f85fd3e))

* build(deps): bump actions/checkout from 3.5.2 to 3.6.0

Bumps [actions/checkout](https://github.com/actions/checkout) from 3.5.2 to 3.6.0.
- [Release notes](https://github.com/actions/checkout/releases)
- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
- [Commits](https://github.com/actions/checkout/compare/8e5e7e5ab8b370d6c329ec480221332ada57f0ab...f43a0e5ff2bd294095638e18286ca9a3d1956744)

---
updated-dependencies:
- dependency-name: actions/checkout
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`806367d`](https://github.com/ral-facilities/datagateway-api/commit/806367df1cb0a2cd7cfe84eaaa25a62aecd9215c))

* build(deps): bump actions/setup-java from 3.11.0 to 3.12.0

Bumps [actions/setup-java](https://github.com/actions/setup-java) from 3.11.0 to 3.12.0.
- [Release notes](https://github.com/actions/setup-java/releases)
- [Commits](https://github.com/actions/setup-java/compare/5ffc13f4174014e2d4d4572b3d74c3fa61aeb2c2...cd89f46ac9d01407894225f350157564c9c7cee2)

---
updated-dependencies:
- dependency-name: actions/setup-java
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`291abff`](https://github.com/ral-facilities/datagateway-api/commit/291abff791bd4f6388d7e6e1e2721eaa681d8876))

* build(deps): bump actions/setup-python from 4.6.0 to 4.7.0

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 4.6.0 to 4.7.0.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/57ded4d7d5e986d7296eab16560982c6dd7c923b...61a6322f88396a6271a6ee3565807d608ecaddd1)

---
updated-dependencies:
- dependency-name: actions/setup-python
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`5d0f4eb`](https://github.com/ral-facilities/datagateway-api/commit/5d0f4eba36c6d4dc078e54a6d7b40549ded28084))

* build(deps): bump codecov/codecov-action from 3.1.3 to 3.1.4

Bumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 3.1.3 to 3.1.4.
- [Release notes](https://github.com/codecov/codecov-action/releases)
- [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md)
- [Commits](https://github.com/codecov/codecov-action/compare/894ff025c7b54547a9a2a1e9f228beae737ad3c2...eaaf4bedf32dbdc6b720b63067d99c4d77d6047d)

---
updated-dependencies:
- dependency-name: codecov/codecov-action
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`52683d6`](https://github.com/ral-facilities/datagateway-api/commit/52683d6baa399d4781af1cac056e7b616c5da173))

* build: Update PyYAML to fix 3.10 CI tests ([`82c3495`](https://github.com/ral-facilities/datagateway-api/commit/82c3495a9e883e2119d658f18b5bf976151ef007))

* build(deps): bump python-semantic-release/python-semantic-release

Bumps [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release) from 7.33.2 to 7.34.4.
- [Release notes](https://github.com/python-semantic-release/python-semantic-release/releases)
- [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.md)
- [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/bfa503c3ef98d240a6d9cb09a8a8603e84200b42...1aed73030dfc573d11ac590f7b7243a0f390b0fc)

---
updated-dependencies:
- dependency-name: python-semantic-release/python-semantic-release
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`c07bf92`](https://github.com/ral-facilities/datagateway-api/commit/c07bf9296fe4242e49b0104f05cec40dfcaafac8))

### Ci

* ci: Ignore new vulernabilties that cannot be fixed ([`97cb59e`](https://github.com/ral-facilities/datagateway-api/commit/97cb59e15dadeb3fc225f07d2b7d9f0fa7b42f1e))

* ci: fix GitHub Actions error ([`2319b35`](https://github.com/ral-facilities/datagateway-api/commit/2319b35efe117db994ef4bf764f14234b410c0c1))

* ci: remove reference to setuptools issue across CI

- This is no longer needed as Python ICAT 1.0 is now used, which doesn&#39;t require an older version of setuptools ([`bd0a1ad`](https://github.com/ral-facilities/datagateway-api/commit/bd0a1adec903326daa187204e0893b4f29220764))

### Fix

* fix: #444 Generate publication dates between two specific dates

- This should stop relative generation causing different data to be generated on different days ([`7908c10`](https://github.com/ral-facilities/datagateway-api/commit/7908c10422ec859d9c923366731897ee859035f0))

### Unknown

* Merge pull request #448 from ral-facilities/remove-isis-endpoints-#432

feat!: Remove code and references to ISIS specific table endpoints ([`2825ea2`](https://github.com/ral-facilities/datagateway-api/commit/2825ea2fb3f3061dfe0ab7d6f02ed730691a4c32))

* Merge branch &#39;main&#39; into bugfix/data-publication-dates-#444 ([`9916813`](https://github.com/ral-facilities/datagateway-api/commit/99168139fe01959740247abbfb26b88f0d82688e))

* Merge branch &#39;main&#39; into remove-isis-endpoints-#432 ([`e667c78`](https://github.com/ral-facilities/datagateway-api/commit/e667c78508e9a4532a3b4654aa15aa94d0947e61))

* Merge pull request #445 from ral-facilities/dependabot/github_actions/python-semantic-release/python-semantic-release-8.0.8

build(deps): bump python-semantic-release/python-semantic-release from 7.34.4 to 8.0.8 ([`60c539c`](https://github.com/ral-facilities/datagateway-api/commit/60c539ccbd7f1e3c4ccbd07c4356e93796c48906))

* Merge pull request #446 from ral-facilities/dependabot/github_actions/actions/checkout-3.6.0

build(deps): bump actions/checkout from 3.5.2 to 3.6.0 ([`4e83e6b`](https://github.com/ral-facilities/datagateway-api/commit/4e83e6bac4cb2831f6c0423c7f19ab3cd617d146))

* Merge pull request #441 from ral-facilities/dependabot/github_actions/actions/setup-java-3.12.0

build(deps): bump actions/setup-java from 3.11.0 to 3.12.0 ([`9761870`](https://github.com/ral-facilities/datagateway-api/commit/97618707da97edbcb7510ad5682d61e83ece36b1))

* Merge pull request #436 from ral-facilities/dependabot/github_actions/actions/setup-python-4.7.0

build(deps): bump actions/setup-python from 4.6.0 to 4.7.0 ([`b4d3c27`](https://github.com/ral-facilities/datagateway-api/commit/b4d3c27ce9019261e186f7be7bba0ec57f2d54d4))

* Merge pull request #423 from ral-facilities/dependabot/github_actions/codecov/codecov-action-3.1.4

build(deps): bump codecov/codecov-action from 3.1.3 to 3.1.4 ([`ea38bbc`](https://github.com/ral-facilities/datagateway-api/commit/ea38bbcc4652b656c62e856a085bb9145a15e28f))

* Containerize application and configure GitHub Actions to build and push Docker image to Harbor (#426)

* Set python image #354

* Upgrade pip #354

* Install Poetry #354

* Install a different version of setuptools #354

* Install Gunicorn #354

* Install the app dependencies #354

* Serve the app on a Gunicorn server #354

* Pin Poetry version #354

* Define Actions job for building and pushing Docker image to Harbor #355

* Configure job to only run after other jobs succeed #355

* Configure job to login to Harbor #355

* Configure job to extract Docker metadata #355

* Configure job to build image #355

* Configure job to push image to Harbor on pushes to k8s-deployment branch #355

* Add job documentation and TODOs #355

* Configure dependabot to maintain GH Actions dependencies #355

* Add TODO for branch name of push events #355

* Update Dockerfile and add entrypoint script

* Use specific python and alpine versions in the base image

* Pin python package versions in Dockerfile

* Use a cache mount to speed up pip and poetry

* Comment the RUN step

* Move things out of the datagateway-api-run directory

* Remove workaround that is no longer needed

* log_location value should not be quoted

* Only copy necessary files to build container

* Improve readability of RUN instructions

* Use a temp file instead of sed -i in entrypoint script

* Create a symlink to the installed python module

* Address TODOs

* Change default value of ICAT_CHECK_CERT ENV

* Upgrade and pin actions to commit SHAs

* ci(docker): bump actions/checkout to 3.5.3 in docker job

* Update README

---------

Co-authored-by: Alan Kyffin &lt;alan.kyffin@stfc.ac.uk&gt; ([`176417b`](https://github.com/ral-facilities/datagateway-api/commit/176417b84571f02f24aeae4afb8642a0700c771e))

* Merge pull request #449 from ral-facilities/ci-failures

Fix CI failures ([`c503f9c`](https://github.com/ral-facilities/datagateway-api/commit/c503f9c3b402262a147eabb67221e54b095c5dc0))

* Merge pull request #419 from ral-facilities/relax-codecov-checks

Relax codecov checks ([`34a2662`](https://github.com/ral-facilities/datagateway-api/commit/34a26623a141b2ac42225a2ade47e9d5242da629))

* Merge pull request #434 from ral-facilities/dependabot/github_actions/python-semantic-release/python-semantic-release-7.34.4 ([`f4bafa6`](https://github.com/ral-facilities/datagateway-api/commit/f4bafa6d52cef1f4da2815329aba4284b93f9f70))

* Merge pull request #427 from ral-facilities/fix-gh-action-errors

Fix GitHub Actions Errors ([`ea2db01`](https://github.com/ral-facilities/datagateway-api/commit/ea2db014156e9dafb7aacea537bfb0d075ebaa3b))

* Ignore flask vulnerability ([`623a4b3`](https://github.com/ral-facilities/datagateway-api/commit/623a4b36b0afabf002eb17bcde949ff8032af46d))

* Ignore werkzeug vulnerability ([`be37a71`](https://github.com/ral-facilities/datagateway-api/commit/be37a7156e08673b4fbe56891c9d7fd62a144fdd))

* Merge pull request #416 from RKrahl/doc/readme-setuptools-version

Remove outdated paragraph on constraints on the setuptools version ([`c1c49b9`](https://github.com/ral-facilities/datagateway-api/commit/c1c49b9a7e7f9ad16cd56ee1e365e050c4be6a49))

* Merge pull request #415 from ral-facilities/dependabot/github_actions/actions/checkout-3.5.2

Bump actions/checkout from 3.5.0 to 3.5.2 ([`8338dd0`](https://github.com/ral-facilities/datagateway-api/commit/8338dd0cc229bbab58bbc2c83c88e9470c6591d9))

* Merge pull request #417 from ral-facilities/dependabot/github_actions/actions/setup-python-4.6.0

Bump actions/setup-python from 4.5.0 to 4.6.0 ([`d3ee311`](https://github.com/ral-facilities/datagateway-api/commit/d3ee311b9ad1601974826b34aec061efcc37e5b7))

* Merge pull request #418 from ral-facilities/dependabot/github_actions/codecov/codecov-action-3.1.3

Bump codecov/codecov-action from 3.1.1 to 3.1.3 ([`26415bf`](https://github.com/ral-facilities/datagateway-api/commit/26415bf9110941da0f5546bd9904ba9289f42cc7))


## v8.0.0 (2023-04-25)

### Breaking

* fix!: add url_prefix param to fix swagger docs at non-root paths #408 ([`49632ea`](https://github.com/ral-facilities/datagateway-api/commit/49632ea19f6dc24e0174c2dfa47ffc253261db3d))

### Ci

* ci: Relax codecov checks

- These checks match the checks that happen on SciGateway ([`65f9a39`](https://github.com/ral-facilities/datagateway-api/commit/65f9a39da3d59c72152b42a61cf72592955cb430))

### Unknown

* Merge pull request #409 from ral-facilities/bugfix/improve-url-prefix-handling-408

Fix swagger docs at non-root paths #408 ([`d557d04`](https://github.com/ral-facilities/datagateway-api/commit/d557d04818a6bf026608628292228983787a77ab))

* Add url_prefix to paths in OpenAPI definition ([`0ed0078`](https://github.com/ral-facilities/datagateway-api/commit/0ed0078e88a2dec7eb43f6452fb63d6d24674ab9))

* Bump codecov/codecov-action from 3.1.1 to 3.1.3

Bumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 3.1.1 to 3.1.3.
- [Release notes](https://github.com/codecov/codecov-action/releases)
- [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md)
- [Commits](https://github.com/codecov/codecov-action/compare/d9f34f8cd5cb3b3eb79b3e4b5dae3a16df499a70...894ff025c7b54547a9a2a1e9f228beae737ad3c2)

---
updated-dependencies:
- dependency-name: codecov/codecov-action
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`ea6cd29`](https://github.com/ral-facilities/datagateway-api/commit/ea6cd2933ef6a790d24b03e86422246189f69650))

* Bump actions/setup-python from 4.5.0 to 4.6.0

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 4.5.0 to 4.6.0.
- [Release notes](https://github.com/actions/setup-python/releases)
- [Commits](https://github.com/actions/setup-python/compare/d27e3f3d7c64b4bbf8e4abfb9b63b83e846e0435...57ded4d7d5e986d7296eab16560982c6dd7c923b)

---
updated-dependencies:
- dependency-name: actions/setup-python
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`457cb3c`](https://github.com/ral-facilities/datagateway-api/commit/457cb3c3aca67ba122113b11bb11c6aa6115f698))

* Remove outdated paragraph on constraints on the setuptools version ([`c24d980`](https://github.com/ral-facilities/datagateway-api/commit/c24d98007bd5dbc22b46287c7177a9705ba71fe0))

* Bump actions/checkout from 3.5.0 to 3.5.2

Bumps [actions/checkout](https://github.com/actions/checkout) from 3.5.0 to 3.5.2.
- [Release notes](https://github.com/actions/checkout/releases)
- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
- [Commits](https://github.com/actions/checkout/compare/8f4b7f84864484a7bf31766abe9204da3cbe65b3...8e5e7e5ab8b370d6c329ec480221332ada57f0ab)

---
updated-dependencies:
- dependency-name: actions/checkout
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`f2b3e1d`](https://github.com/ral-facilities/datagateway-api/commit/f2b3e1d357e722fe13e8bddb3ce00b55c4f35dce))

* Merge branch &#39;main&#39; into bugfix/improve-url-prefix-handling-408 ([`d88d295`](https://github.com/ral-facilities/datagateway-api/commit/d88d2959605d1cece26bd2502f6c74f67709fae4))

* Fix linting ([`d4f2545`](https://github.com/ral-facilities/datagateway-api/commit/d4f2545b5f5ecf13539c31eb5789cc68ddc029f7))

* Add integration test for Swagger UI ([`1daa60d`](https://github.com/ral-facilities/datagateway-api/commit/1daa60d49d8eabbcc129d48a23afc64d509f3260))

* Fix linting errors &amp; update existing unit tests ([`fb3d05a`](https://github.com/ral-facilities/datagateway-api/commit/fb3d05a06ef5197e03d673d2e392ea72e62adfe0))

* Merge pull request #413 from ral-facilities/dependabot/github_actions/actions/setup-java-3.11.0 ([`5258698`](https://github.com/ral-facilities/datagateway-api/commit/52586989b9990a62f42eabc11635d0323f64bd56))

* Merge pull request #412 from ral-facilities/dependabot/github_actions/actions/checkout-3.5.0 ([`b072c5c`](https://github.com/ral-facilities/datagateway-api/commit/b072c5cef759c5fef68456276a13d33dec975241))

* Bump actions/setup-java from 3.10.0 to 3.11.0

Bumps [actions/setup-java](https://github.com/actions/setup-java) from 3.10.0 to 3.11.0.
- [Release notes](https://github.com/actions/setup-java/releases)
- [Commits](https://github.com/actions/setup-java/compare/3f07048e3d294f56e9b90ac5ea2c6f74e9ad0f98...5ffc13f4174014e2d4d4572b3d74c3fa61aeb2c2)

---
updated-dependencies:
- dependency-name: actions/setup-java
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`db27fff`](https://github.com/ral-facilities/datagateway-api/commit/db27fff081b967987dd4057b7c9bc852d2e861e5))

* Bump actions/checkout from 3.3.0 to 3.5.0

Bumps [actions/checkout](https://github.com/actions/checkout) from 3.3.0 to 3.5.0.
- [Release notes](https://github.com/actions/checkout/releases)
- [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
- [Commits](https://github.com/actions/checkout/compare/ac593985615ec2ede58e132d2e21d2b1cbd6127c...8f4b7f84864484a7bf31766abe9204da3cbe65b3)

---
updated-dependencies:
- dependency-name: actions/checkout
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`b31d769`](https://github.com/ral-facilities/datagateway-api/commit/b31d769d08a6f7954f44275b228c2fdffd0d15f4))

* Merge pull request #406 from ral-facilities/fix/address-github-actions-warnings-#397

Address GitHub Actions warnings ([`5807986`](https://github.com/ral-facilities/datagateway-api/commit/5807986b579613d2439bbec106392d55b9f0ca19))


## v7.1.0 (2023-03-23)

### Build

* build: deal with Safety errors #405 ([`1f528bd`](https://github.com/ral-facilities/datagateway-api/commit/1f528bdbdce295190ca8037c05e2a415d85edd76))

### Ci

* ci: pin Python Semantic Release action to commit SHA #397 ([`53a6993`](https://github.com/ral-facilities/datagateway-api/commit/53a6993211d58c7c3327fdfccdca18bb31f03929))

* ci: specify distribution for setup-java action #397 ([`200d842`](https://github.com/ral-facilities/datagateway-api/commit/200d842454f18c6aa148d4c07c9d3ebb9500f909))

* ci: address warnings by updating and pinning actions to commit SHAs #397 ([`2a1a05f`](https://github.com/ral-facilities/datagateway-api/commit/2a1a05ffd4d3602a906bdac476240d769b1bd70a))

### Feature

* feat: Add icat 5 entity generation to the data generator script ([`579e321`](https://github.com/ral-facilities/datagateway-api/commit/579e321d9ae368d5840e602154bdb155e902478b))

### Unknown

* Merge pull request #407 from ral-facilities/feature/icat-5-entity-generation

Feature/icat 5 entity generation ([`194afcc`](https://github.com/ral-facilities/datagateway-api/commit/194afcc348d3c908b12ce5e68fb9d8b769a5f759))

* Change entity name to camelCase

- The previous version works for Python ICAT 1.0, but this is how all the other entities are cased and it means the script is compatible with Python ICAT &lt; 1.0 ([`07a4e23`](https://github.com/ral-facilities/datagateway-api/commit/07a4e235e8007222a9975459b0255de4719c3a6d))

* fix DataPublciation ([`12975aa`](https://github.com/ral-facilities/datagateway-api/commit/12975aa1f83821bdb940f3d1b5da475bf2789474))

* configure Dependabot version updates for actions #397 ([`7c58f2f`](https://github.com/ral-facilities/datagateway-api/commit/7c58f2fc6f1acd85a95cfc8d1a511be3a22e7d3b))

* Add RelatedItems ([`27701de`](https://github.com/ral-facilities/datagateway-api/commit/27701decd8154af377b95dd5077d9ca43c25aadb))

* Datapublications and Datasets ([`768f9d9`](https://github.com/ral-facilities/datagateway-api/commit/768f9d9bff31485cb98cdc6d95e4680e8d15d70e))


## v7.0.0 (2023-02-24)

### Documentation

* docs: add search scoring information to README #398 ([`a4f833e`](https://github.com/ral-facilities/datagateway-api/commit/a4f833e41ad9a5a0227ee0e04504091d1f05f1cf))

### Unknown

* Merge pull request #399 from ral-facilities/398-adapt-search-query-filter-and-scoring-to-v5

Query filter and scoring ([`a09748c`](https://github.com/ral-facilities/datagateway-api/commit/a09748c78ae2b88054071b719d3a9cd9f2a5ba50))

* Merge branch &#39;main&#39; into 398-adapt-search-query-filter-and-scoring-to-v5 ([`d47a45d`](https://github.com/ral-facilities/datagateway-api/commit/d47a45dd675b4a31ff6dfc1bfbf70560571e93aa))


## v6.3.2 (2023-02-24)

### Fix

* fix: add triggers for later stages of consistency test ([`2d7d677`](https://github.com/ral-facilities/datagateway-api/commit/2d7d677fbab85a93fb36fc12afb434ba74dbfc27))

### Unknown

* Merge pull request #404 from ral-facilities/fix/add-triggers-consistency-test

fix: add triggers for later stages of consistency test ([`390ec3c`](https://github.com/ral-facilities/datagateway-api/commit/390ec3c48a117eba1f550629cf01c7c39fd52395))

* Remove tmate ([`3447d9c`](https://github.com/ral-facilities/datagateway-api/commit/3447d9ce49bae0597671b6efa17837b27b1353cd))

* Use sudo for adding triggers ([`d8e185e`](https://github.com/ral-facilities/datagateway-api/commit/d8e185e069aa73f6e36297f461c9c5dfca594977))

* tmate before dummy data ([`8288cc4`](https://github.com/ral-facilities/datagateway-api/commit/8288cc44bc29b7c0c023cc0fc426b90f069a037f))

* Fix database triggers script command ([`0362d81`](https://github.com/ral-facilities/datagateway-api/commit/0362d8163f622f44a21dff0b23ad15dc4db3cee5))

* Change user to be root ([`65fa5c4`](https://github.com/ral-facilities/datagateway-api/commit/65fa5c4a17a5580d7cca1531d1ad457cee93793e))


## v6.3.1 (2023-02-23)

### Fix

* fix: Remove dataset filesize generator ([`fb466dd`](https://github.com/ral-facilities/datagateway-api/commit/fb466dd6012088fb25f575f3c7198a9d7d28e070))

### Refactor

* refactor: remove `str_conditions` param from `get_search` method #398 ([`79fe589`](https://github.com/ral-facilities/datagateway-api/commit/79fe589c4ed18114286fa7dd1ad0e6990a0d2f2a))

### Unknown

* Merge pull request #403 from ral-facilities/fix/remove-dataset-filesize

Fix/remove dataset filesize ([`d530145`](https://github.com/ral-facilities/datagateway-api/commit/d530145593dd8fea30e6ab277bff6a7768a9f22a))

* remove commented line #398 ([`5b9db5e`](https://github.com/ral-facilities/datagateway-api/commit/5b9db5ecb6c6952a3cb225654fba57d4d65a1220))

* Fix test differences ([`5dce490`](https://github.com/ral-facilities/datagateway-api/commit/5dce490bad0dfc43036f2ab2c829357650bfee99))

* Merge branch &#39;main&#39; into 398-adapt-search-query-filter-and-scoring-to-v5 ([`52e1343`](https://github.com/ral-facilities/datagateway-api/commit/52e1343dbac04f4e2dfefff21660cde3ccf80198))


## v6.3.0 (2023-02-17)

### Breaking

* refactor(api): modify Search API endpoint URL paths #398

The Search endpoint URL paths have been modified to follow the format
that the PaNOSC Federated Search API sets out. These changes were made:
- The Datasets endpoint URL was modified from /datasets to /Datasets
- The Documents endpoint URL was modified from /documents to /Documents
- The Instruments endpoint URL was modified from /instruments to
    /Instruments

BREAKING CHANGE: modify Search API endpoint URL paths ([`1dc815b`](https://github.com/ral-facilities/datagateway-api/commit/1dc815bfcd0316e92471e0f8a24ae19a753c1405))

* feat(config): add scoring related values to config #398

BREAKING CHANGE: add scoring related values to config ([`0472d96`](https://github.com/ral-facilities/datagateway-api/commit/0472d9617b6771c6b64ebbaa49953b5583d1d3c9))

### Feature

* feat: Refactor icat generator to use python-icat ([`ae6ae0b`](https://github.com/ral-facilities/datagateway-api/commit/ae6ae0b2a2ce375fb0d47851b3091c952735f5c6))

* feat: add support for scoring results #398 ([`dd58a8b`](https://github.com/ral-facilities/datagateway-api/commit/dd58a8b4bef706b343144ab8fe14a8b4737b3781))

### Refactor

* refactor: move search scoring logic to a separate module #398 ([`70cd754`](https://github.com/ral-facilities/datagateway-api/commit/70cd7544892e9c1b38df49a780bf310a7a69acc4))

* refactor: refactor logic for adding scores to results #398 ([`c328a0d`](https://github.com/ral-facilities/datagateway-api/commit/c328a0d729cf1d3a7f3b87a6c4124e1f0a797daa))

* refactor: refactor handling of errors when getting scores #398 ([`4f810fd`](https://github.com/ral-facilities/datagateway-api/commit/4f810fdeb329246ed1af498bb9ec4ee87ea4e486))

* refactor: refactor logic for creating `SearchAPIScoringFilter` #398 ([`505802a`](https://github.com/ral-facilities/datagateway-api/commit/505802ab6988f90d5a330c0c7bdc6d2edf186733))

* refactor: refactor implementation of `SearchAPIScoringFilter` #398 ([`9277dd3`](https://github.com/ral-facilities/datagateway-api/commit/9277dd3e45ba096d5d88f7f848b98295b49897aa))

### Test

* test: fix tests following the changes to endpoint URLs #398 ([`5be35cd`](https://github.com/ral-facilities/datagateway-api/commit/5be35cd699cf8c6df3490a196c1acee45a6275f9))

* test: rename test_helpers.py to test_search_scoring.py #398 ([`4ac95b6`](https://github.com/ral-facilities/datagateway-api/commit/4ac95b6d02c31d47279dc85f33586593bedc8608))

* test: fix failing integration test #398 ([`042049f`](https://github.com/ral-facilities/datagateway-api/commit/042049f1aac8142ac9377bebc47700170d312040))

* test: add tests for scoring functionality #398 ([`22325f4`](https://github.com/ral-facilities/datagateway-api/commit/22325f4f4ba96c3e631e236a22bdd2cfb8464076))

* test: fix failing tests #398 ([`c40414e`](https://github.com/ral-facilities/datagateway-api/commit/c40414e777b673f310645d920108ca5428982756))

* test: fix tests #398 ([`4637d48`](https://github.com/ral-facilities/datagateway-api/commit/4637d480450e9e22a36d7adce1ef10e628cbf5f8))

### Unknown

* Merge pull request #401 from ral-facilities/feature/icat-backend-generator#369

Feature/icat backend generator#369 ([`31aad3e`](https://github.com/ral-facilities/datagateway-api/commit/31aad3eec204be60da44324ccf107a7516ac9320))

* raise an error if query filter value is not string #398 ([`83a3222`](https://github.com/ral-facilities/datagateway-api/commit/83a32220910929ab9b12ba6cc89327b56b950ad0))

* move and rename sql script, fix path ([`f14bccb`](https://github.com/ral-facilities/datagateway-api/commit/f14bccbe3ef645b995d6e178077e51b71457b9ea))

* Consistency test drop mod/createTime ([`9e4da17`](https://github.com/ral-facilities/datagateway-api/commit/9e4da172a8c0996ac0e73b00d2d513cab030bd08))

* Add function to remove creationDate from responses ([`cf7d8a2`](https://github.com/ral-facilities/datagateway-api/commit/cf7d8a2fb367082e2e1bd11de0e261171ad39b9d))

* Merge branch &#39;main&#39; into 398-adapt-search-query-filter-and-scoring-to-v5 ([`4ac42b0`](https://github.com/ral-facilities/datagateway-api/commit/4ac42b057e814b588a922e29299544eacd20cef5))

* add scoring related values to config #398

BREAKING CHANGE: add scoring related values to config ([`b3fffc2`](https://github.com/ral-facilities/datagateway-api/commit/b3fffc25804e90a97b0106cb1d49d298880095b1))

* Fix lock file ([`b060ffe`](https://github.com/ral-facilities/datagateway-api/commit/b060ffe865d4396450484b98fc811b25ca56ac54))

* Merge branch &#39;main&#39; into feature/icat-backend-generator#369

Conflicts:
	poetry.lock ([`9616219`](https://github.com/ral-facilities/datagateway-api/commit/9616219ec2088370032573633f836195190fb936))

* Fix search-api tests and linting ([`d28919e`](https://github.com/ral-facilities/datagateway-api/commit/d28919e39629e30396e1f5583d8a2a2e061456d7))

* FIx dg-api tests ([`1ef9eb2`](https://github.com/ral-facilities/datagateway-api/commit/1ef9eb2a8d7755d9b1fcbee30dec400cf76856c0))

* Merge pull request #393 from ral-facilities/tests/reorganise-tests#375

Tests/reorganise tests#375 ([`b08022a`](https://github.com/ral-facilities/datagateway-api/commit/b08022a62b0592575d3d538599f36f7a97fbe6b3))

* Update for safety ([`619d3e4`](https://github.com/ral-facilities/datagateway-api/commit/619d3e4fe05eeca04f31bc9891e864ac05335dc8))

* Changes to filters, endpoints and queries ([`21b0233`](https://github.com/ral-facilities/datagateway-api/commit/21b0233514c960b5adc0b969539f732f48a66e53))

* Merge pull request #396 from ral-facilities/tests/python_icatv1

Tests/python icatv1 ([`8627dbb`](https://github.com/ral-facilities/datagateway-api/commit/8627dbb5c8a21da6ecddfbdc1c2fa1186de83a6c))

* Merge branch &#39;tests/reorganise-tests#375&#39; into tests/python_icatv1 ([`fe6b137`](https://github.com/ral-facilities/datagateway-api/commit/fe6b137ca89bcb2fb5542782270f9730c28e9f6f))

* Run black ([`0a3c166`](https://github.com/ral-facilities/datagateway-api/commit/0a3c1669f68e0b66a13b9f95cdf5a6663a21c534))

* Merge branch &#39;398-adapt-search-query-filter-and-scoring-to-v5&#39; of https://github.com/ral-facilities/datagateway-api into 398-adapt-search-query-filter-and-scoring-to-v5 ([`ca94487`](https://github.com/ral-facilities/datagateway-api/commit/ca94487e2c463b2f61d8ada093f6d81f12f911a3))

* Fixing confTest with the mising values ([`84313ff`](https://github.com/ral-facilities/datagateway-api/commit/84313ff023af8aecbaf035821247d8c02922c4e3))

* Fixing confTest with the mising values ([`7eac557`](https://github.com/ral-facilities/datagateway-api/commit/7eac55786486b6c63e9fcf03a724257cd25a373f))

* Added scoring to the query filter ([`7cb0747`](https://github.com/ral-facilities/datagateway-api/commit/7cb0747f88ee24606046bd34114ba29324e95cf7))

* Fix import error for ScoringQueryFilter #398 ([`d5d5dba`](https://github.com/ral-facilities/datagateway-api/commit/d5d5dbacc0b5a54d75813fb9526ff683bcbafad5))

* Merge branch &#39;398-adapt-search-query-filter-and-scoring-to-v5&#39; of https://github.com/ral-facilities/datagateway-api into 398-adapt-search-query-filter-and-scoring-to-v5 ([`27c301f`](https://github.com/ral-facilities/datagateway-api/commit/27c301fd3a4402e41854df0b74f06ed1463fa7fa))

* Implementation of Query filter

This allows to search by a keyword. Example:
```
/search-api/documents?filter={&#34;query&#34;:&#34;diffraction&#34;}
```

This should returns the document that are related to diffraction ([`1fee761`](https://github.com/ral-facilities/datagateway-api/commit/1fee7610cd518b463325710a6cdc11d1c4a78c92))

* Fixed linting errors ([`bef75ca`](https://github.com/ral-facilities/datagateway-api/commit/bef75cae2b21c6633c1aff13dd53e3f5fc2ac177))

* Revert change of the case of endpoints, implementation of the query filter ([`933fcf7`](https://github.com/ral-facilities/datagateway-api/commit/933fcf7026dd465c8fd3e3c4b26c3f2dfec0b596))

* panosc aggregator uses endpoints starting by capital letter ([`30ebd12`](https://github.com/ral-facilities/datagateway-api/commit/30ebd124a5ab0166b18365484869181d95c698a9))

* Remove commas after mappings in YAML config #398 ([`ae05f29`](https://github.com/ral-facilities/datagateway-api/commit/ae05f2941328b310dc9f62fbbaa369b3e71acc71))

* Added scoring configuration parameters ([`2f6a120`](https://github.com/ral-facilities/datagateway-api/commit/2f6a1200d03e5c94f1fb56052b6e6b2273124d75))

* Remove multiprocessing ([`a4fa2e7`](https://github.com/ral-facilities/datagateway-api/commit/a4fa2e70f14e6a39d8c265442c463d1f19955b70))

* Add prep for api for integration tests ([`35780bb`](https://github.com/ral-facilities/datagateway-api/commit/35780bbb066662b2751c5312c14a6b125539082f))

* Remove second checkout ([`c2e3f77`](https://github.com/ral-facilities/datagateway-api/commit/c2e3f77949a4e6fb211236301c229f4771451b6f))

* Poetry install needed for generator ([`5f11ba2`](https://github.com/ral-facilities/datagateway-api/commit/5f11ba2542ff8a11a717e42a82653b3589d98e45))

* Readd fix for python 3.10 ([`f9eb154`](https://github.com/ral-facilities/datagateway-api/commit/f9eb154626be953b63ecf433587eafa77689463a))

* Remove poetry install and setuptools install ([`985aa02`](https://github.com/ral-facilities/datagateway-api/commit/985aa02bf097a916a4305a293ffb5aa8cfe6ca97))

* Clean up ([`a0349ba`](https://github.com/ral-facilities/datagateway-api/commit/a0349baf54e417cfa386ddbf87c36a43cb36ffa2))

* Cut number of datacollections ([`71f3b8b`](https://github.com/ral-facilities/datagateway-api/commit/71f3b8b20568c081e393581614a4c1b1630521c1))

* Less data generation ([`3f5e6be`](https://github.com/ral-facilities/datagateway-api/commit/3f5e6be129a4fbbb86b563e684338fced123d9be))

* Update readme for new test runners. ([`aa4350c`](https://github.com/ral-facilities/datagateway-api/commit/aa4350c3b9c8e95cfdb3cdb5465f5dba958f8373))

* Update python icat to full release ([`a0e9527`](https://github.com/ral-facilities/datagateway-api/commit/a0e952744d415144d20f27846d7b2418f6c8ef2f))

* Fix datafile parameter generator ([`9940720`](https://github.com/ral-facilities/datagateway-api/commit/9940720088d929e2568d0637dade25d88543d990))

* Fix linting ([`24c3bd7`](https://github.com/ral-facilities/datagateway-api/commit/24c3bd78c34c4b842cc472867df631dba5ca702a))

* Fix datafileparamter range ([`25e9c29`](https://github.com/ral-facilities/datagateway-api/commit/25e9c29d3902caedac90edb27671662b301dcb84))

* remove get_icat_entity_name_as_camel_case ([`e7b8794`](https://github.com/ral-facilities/datagateway-api/commit/e7b8794a16ac0f9beed62c33d9b3456e1506ea1d))

* Multithread large generators ([`3d9954d`](https://github.com/ral-facilities/datagateway-api/commit/3d9954dada4884d4ca1a7e4dce153e3a5c806d59))

* assert correct values for v1 ([`86b9a11`](https://github.com/ral-facilities/datagateway-api/commit/86b9a11e96224335bfe0c366e329eded46ec900b))

* update to v1 ([`ebd60b6`](https://github.com/ral-facilities/datagateway-api/commit/ebd60b6e751cb546a981ef388fe45fd750d686b9))

* refresh id for long generators ([`f89fe2a`](https://github.com/ral-facilities/datagateway-api/commit/f89fe2ad6c66d62827f4d0965ae67f898aa9b3ce))

* Multiple codecov uploads ([`a6f5d06`](https://github.com/ral-facilities/datagateway-api/commit/a6f5d06742e090aa7f5beed8702a78715cf761e3))

* Use latest codecov action ([`b3d0fc5`](https://github.com/ral-facilities/datagateway-api/commit/b3d0fc5693673b0cbfb8bd47de535188af767d4f))

* Ignore sqlalchemy vulnerability ([`da66fac`](https://github.com/ral-facilities/datagateway-api/commit/da66facce1abbd0379c8671385f9593ee07b1d03))

* Create config earlier and dependency updates ([`4e275f6`](https://github.com/ral-facilities/datagateway-api/commit/4e275f680f88e3cf2bf6ffe5196cf34577eb6a47))

* Checkout api earlier ([`ebcb7a6`](https://github.com/ral-facilities/datagateway-api/commit/ebcb7a6408c99cb2c1f1d6d134c9a736befd3cc2))

* Split unit and integration test runs ([`c0595ba`](https://github.com/ral-facilities/datagateway-api/commit/c0595bac1e4e5aaa59529281a4472349a084c819))

* Optimisation and cleanup of unused code ([`23ee841`](https://github.com/ral-facilities/datagateway-api/commit/23ee84156147a01f4b649289ee939fed58da7492))

* Working generator ([`d2c697a`](https://github.com/ral-facilities/datagateway-api/commit/d2c697ac99b572de81bbcbf37d95dd3074e6ede6))

* Add panosc mapping to unit tests ([`4ebeb77`](https://github.com/ral-facilities/datagateway-api/commit/4ebeb7753ef7a6416e001ad7ef63862b9198f7a7))

* Initial refactor ([`0dc5a03`](https://github.com/ral-facilities/datagateway-api/commit/0dc5a03be879a134de36ee02bc43861829a04734))


## v6.2.0 (2022-11-23)

### Unknown

* Merge pull request #385 from ral-facilities/tests/db-backend-tests-#370

Tests/db backend tests #370 ([`41c1586`](https://github.com/ral-facilities/datagateway-api/commit/41c1586ed256a499064bef5b4906f8979fbd52ff))

* Merge branch &#39;main&#39; into tests/db-backend-tests-#370 ([`b9831bd`](https://github.com/ral-facilities/datagateway-api/commit/b9831bd701f1b43b9f3a36e110c28eafb3e5d926))


## v6.1.1 (2022-11-23)

### Unknown

* Merge pull request #390 from ral-facilities/bugfix/related-entities-creation-#387

Creation of related entities attempted when not specified to be included ([`1e6c600`](https://github.com/ral-facilities/datagateway-api/commit/1e6c6008fd0bfcf8e18f381d7b9af3fb31ea161e))


## v6.1.0 (2022-11-23)

### Unknown

* Merge pull request #383 from ral-facilities/feature/icat5-endpoints#373

Add icat5 endpoints ([`3943ec4`](https://github.com/ral-facilities/datagateway-api/commit/3943ec45df76fbfca9645db040cb91f72a04a3f9))

* Merge pull request #391 from ral-facilities/fix/icat-generator-workflow

ci: Main branch uses yaml config not json ([`849a4aa`](https://github.com/ral-facilities/datagateway-api/commit/849a4aa3bf0c444560775cd8641ea28453a8726d))


## v6.0.0 (2022-11-22)

### Ci

* ci: Main branch uses yaml config not json ([`0b6151b`](https://github.com/ral-facilities/datagateway-api/commit/0b6151babd1c111c70c8c9755f5abdbedcbdad57))

### Fix

* fix: do not attempt to create related entities if not included #387 ([`819e7a1`](https://github.com/ral-facilities/datagateway-api/commit/819e7a1582d8d108fe5f18b210c08d67cd0a3845))

### Test

* test: fix failing tests #387 ([`fcbfb0f`](https://github.com/ral-facilities/datagateway-api/commit/fcbfb0ff8bb58b676d7ba4ea83f8d480b5c6c910))

### Unknown

* Merge pull request #388 from ral-facilities/feature/use-yaml-config#372

Feature/use yaml config#372 ([`5060d5e`](https://github.com/ral-facilities/datagateway-api/commit/5060d5e7aae4d2f0f8b126f78f6988c1c57dc1d6))

* reorganise new DB tests ([`7ffc4b8`](https://github.com/ral-facilities/datagateway-api/commit/7ffc4b8fa7af07f741d340face9dcc178ee5f95c))

* Fix linting ([`aa39a81`](https://github.com/ral-facilities/datagateway-api/commit/aa39a81c7a1ebb5d7c9c3f39ed7f79a7693f78e0))

* Initial reorganisation

Tests have been organised into ones that immediately work with no icat stack and ones that don&#39;t. ([`185e304`](https://github.com/ral-facilities/datagateway-api/commit/185e3048c62bffe127419df137e249145d473f08))

* Requested changes from review ([`9cfa727`](https://github.com/ral-facilities/datagateway-api/commit/9cfa72704c144474a8de6f8b1d1964d92cbdae54))

* Generator script workflow changes ([`5a63e70`](https://github.com/ral-facilities/datagateway-api/commit/5a63e70c08e3f3de83f91bf898a67af38d433e56))

* Requested changes ([`c8567ef`](https://github.com/ral-facilities/datagateway-api/commit/c8567efd859b2ce763fc8585dfce97233dfb6c39))

* linting and safety ([`6549b3e`](https://github.com/ral-facilities/datagateway-api/commit/6549b3e617e9441d9d24a012fe0e383fd12797db))

* Ignore vulnerability and change generator workflow ([`1e08ed9`](https://github.com/ral-facilities/datagateway-api/commit/1e08ed90d1243bd335590a42e93ef99c34a57e05))

* fix generator script ([`f224aca`](https://github.com/ral-facilities/datagateway-api/commit/f224aca61890a0ed2c0a2d1693a42be24172fc80))

* Add exstension change ([`3e59c86`](https://github.com/ral-facilities/datagateway-api/commit/3e59c8618ba0106f1e240e6a1290f7a4c117c723))

* Merge branch &#39;main&#39; into feature/use-yaml-config#372 ([`8921643`](https://github.com/ral-facilities/datagateway-api/commit/89216434464c2cff46e06de5fda5c17b7fe7c06b))

* Add explanation for why test might fail ([`2eb6e11`](https://github.com/ral-facilities/datagateway-api/commit/2eb6e117514ae04fb6b595d4c6abb1667c0438c6))


## v5.3.0 (2022-11-16)

### Documentation

* docs: Updated postman collection with new entities ([`4dd4895`](https://github.com/ral-facilities/datagateway-api/commit/4dd489574245f4f6020c490d5cddeb3fc3c65c91))

### Feature

* feat: Add warning for no api ([`3c91635`](https://github.com/ral-facilities/datagateway-api/commit/3c91635bc0c3465d456a4a85c8d6c8793df408c2))

* feat: Add new entity endpoints for icat5 ([`dd18e18`](https://github.com/ral-facilities/datagateway-api/commit/dd18e18bc19f87c5aa7c99c144f262b68e4fe0c6))

### Unknown

* Merge pull request #386 from ral-facilities/feature/no-api-warning#380

feat: Add warning for no api ([`962dd80`](https://github.com/ral-facilities/datagateway-api/commit/962dd806bf765816ce91e93c37526080191c9edf))

* Add login test ([`e3e2005`](https://github.com/ral-facilities/datagateway-api/commit/e3e20058763319cf6c5ce621a2e8701d6fede553))

* Remove print statement ([`a24d429`](https://github.com/ral-facilities/datagateway-api/commit/a24d4299c1e805d53c1ac5ce48463235d6c3b03c))

* Fix linting ([`7dee9f6`](https://github.com/ral-facilities/datagateway-api/commit/7dee9f6f3df4deb245770001890cd59e2f5f7126))

* Set example to be configured for datagateway tests ([`c18b669`](https://github.com/ral-facilities/datagateway-api/commit/c18b6697f00ec3a630f4557fde74f94d456b2c87))

* Fix example log location ([`fe1271a`](https://github.com/ral-facilities/datagateway-api/commit/fe1271aee368e1cf7bfef37be77dd33317ed1c6f))

* Make user_credentials a dict ([`7854093`](https://github.com/ral-facilities/datagateway-api/commit/78540934131a551a68a563263d9b270a76262814))

* No dg api extension ([`7246e4b`](https://github.com/ral-facilities/datagateway-api/commit/7246e4b595c032038644ec545aaca208b24f6df3))

* Change test_user_credentials ([`a38dc89`](https://github.com/ral-facilities/datagateway-api/commit/a38dc8993aba0c5451a02e70be77ca1ea5d861aa))

* Fix log location ([`196dadc`](https://github.com/ral-facilities/datagateway-api/commit/196dadc885e6e2244c2defcc086e93c108d58d07))

* figure out strange behaviour, make tests more useful ([`652d1db`](https://github.com/ral-facilities/datagateway-api/commit/652d1db3be323f280bff7b7b976bb5af419434f3))

* Revert changes to invalid update with id ([`b311637`](https://github.com/ral-facilities/datagateway-api/commit/b311637d03b0263cfb7beb2847ac1c2cd1d7e988))

* Fix tests for icat5 ([`55574cb`](https://github.com/ral-facilities/datagateway-api/commit/55574cbcf1e1a9aa6aac132e6449234154e4c3f8))

* Add tests for where filter ([`3a5a4a3`](https://github.com/ral-facilities/datagateway-api/commit/3a5a4a31173652b1984f032d498043ed58dc78d3))

* Fix sessions and linting ([`6972dcc`](https://github.com/ral-facilities/datagateway-api/commit/6972dccad2eee634980a8a133dd6f0e0c6b255e0))

* test_update_vallid encounters a datetime faillure ([`0e7fc3d`](https://github.com/ral-facilities/datagateway-api/commit/0e7fc3df3e26da400758e9669c71dfe94f956731))

* test_create_data encountering datetime error ([`b31d037`](https://github.com/ral-facilities/datagateway-api/commit/b31d037a90be3a88f80678dca56662e9d5691d9b))

* Implement more tests ([`9cc8757`](https://github.com/ral-facilities/datagateway-api/commit/9cc875761e470277a2e348bc51eefe4371ac2283))

* Add tests for multiple updates ([`451e618`](https://github.com/ral-facilities/datagateway-api/commit/451e6180937f9c1d7d0f2a450b501d6447c9c74e))

* Add test for updating data ([`5dc78c3`](https://github.com/ral-facilities/datagateway-api/commit/5dc78c3a49b9f062455f344c4090fa02602c47d9))

* address linter issues ([`c434218`](https://github.com/ral-facilities/datagateway-api/commit/c4342185ae52dd4ba49de8b9020b9704b4571a76))

* Test all models and fix issues ([`df446d6`](https://github.com/ral-facilities/datagateway-api/commit/df446d6781dcd805a027e0c4d090ee2752a8123c))

* generate openapi and fix model references ([`92f8682`](https://github.com/ral-facilities/datagateway-api/commit/92f868202bd27f08784195f7518363702c86260a))

* Change dates backref as causing KeyErrors ([`99fb986`](https://github.com/ral-facilities/datagateway-api/commit/99fb986387cbb56318bd5fb76afc383af55b7cf4))

* change nulls and backrefs ([`0ce5727`](https://github.com/ral-facilities/datagateway-api/commit/0ce5727fa1360ee8074fc8a8fbb6bac6c4ff38d2))

* Fix linting ([`49f31b3`](https://github.com/ral-facilities/datagateway-api/commit/49f31b335de3d76c8a2cc636483c9c8c7b1b028e))


## v5.2.0 (2022-11-03)

### Breaking

* feat: Enable support for yaml configuration files for DatagatewayAPI

BREAKING CHANGE: Remove support for json configuration files ([`46723de`](https://github.com/ral-facilities/datagateway-api/commit/46723de2bf5336244b3dd37808f565e554b5cbdb))

### Documentation

* docs: Updated postman collection with new entities ([`c4b850f`](https://github.com/ral-facilities/datagateway-api/commit/c4b850f913dbded35e6b1a88c8f8d8e1b36cbdec))

* docs: Update the poetry installation documentation ([`68d4267`](https://github.com/ral-facilities/datagateway-api/commit/68d426722862613358b0b136188d2b61accdc56f))

### Feature

* feat: Add new entity endpoints for icat5 ([`dc14f9f`](https://github.com/ral-facilities/datagateway-api/commit/dc14f9f8aeb5a9849bc69cf647bf068b04a63d81))

* feat: Add warning that tests only work with ICAT 5 ([`d8825fd`](https://github.com/ral-facilities/datagateway-api/commit/d8825fd71740e2b2d9b387dca175110cee1f9915))

* feat: Changes to tests so they pass with icat 5 ([`73f3c77`](https://github.com/ral-facilities/datagateway-api/commit/73f3c777f8d3841cf09537140922a9bbdd8dad7c))

* feat: Add support for yaml configuration ([`02c3e41`](https://github.com/ral-facilities/datagateway-api/commit/02c3e41c92c721d793b27b44c7b27cfb3af6ffbb))

### Unknown

* Merge pull request #378 from ral-facilities/docs/new-poetry-installer-#376

docs: Update the poetry installation documentation ([`2c64b7d`](https://github.com/ral-facilities/datagateway-api/commit/2c64b7d2b2eac72666e8face7205231f2ba92c86))

* Merge pull request #381 from ral-facilities/feature/icat5-tests#374

Changes to tests so they pass with icat 5 ([`9bb898d`](https://github.com/ral-facilities/datagateway-api/commit/9bb898d95a114beb0fc9f2d60f065cddea6b30fa))

* address linter issues ([`6f10cb3`](https://github.com/ral-facilities/datagateway-api/commit/6f10cb386cce572757473a449d7a869af1b2f979))

* Test all models and fix issues ([`63c2faa`](https://github.com/ral-facilities/datagateway-api/commit/63c2faa3aad72c55d26bbc1d00c24e80f38524e4))

* generate openapi and fix model references ([`b7fdbe0`](https://github.com/ral-facilities/datagateway-api/commit/b7fdbe0027d86b152b80898d4ae2ad652b87b037))

* Change dates backref as causing KeyErrors ([`0e75fef`](https://github.com/ral-facilities/datagateway-api/commit/0e75fef4ae4346249c4f8974b00fe0a2a3d85453))

* change nulls and backrefs ([`8e69dd9`](https://github.com/ral-facilities/datagateway-api/commit/8e69dd923f2a6504d58a2d501336edb5c1d602d6))

* Fix linting ([`30b8907`](https://github.com/ral-facilities/datagateway-api/commit/30b89075f84e0de24244b64c17106e596e7c9233))

* pin flake8-black to 0.2.4

0.2.5 causes flake8 to fail due to unexpected keyword argument &#39;magic_trailing_comma&#39;.
0.3 and greater require python 3.7 ([`4d6b066`](https://github.com/ral-facilities/datagateway-api/commit/4d6b06688dd3a5fde169de08ac41eb7c57f2df2b))

* Update for dparse ([`ab160a8`](https://github.com/ral-facilities/datagateway-api/commit/ab160a82751a30d5e6b02fa8667b8a150691cc12))

* Fix linting ([`f59ca0f`](https://github.com/ral-facilities/datagateway-api/commit/f59ca0ff67b4d027d10a3de85041f3cac1a1402f))

* Address requested changes ([`5495195`](https://github.com/ral-facilities/datagateway-api/commit/5495195b1e775f24ca15ed3e4082cc0bf0507780))

* use / as api url ([`8ee7f27`](https://github.com/ral-facilities/datagateway-api/commit/8ee7f27ac2111e03bd782d2fb0b3ba4211f630eb))

* safety fix ([`a9e5816`](https://github.com/ral-facilities/datagateway-api/commit/a9e5816abbbd6e431ea28a1ffc780be3baa90907))

* Test user credentials to yaml ([`2be2282`](https://github.com/ral-facilities/datagateway-api/commit/2be22827b8cf9b49c03145f7472f045e9c95f15c))

* update poetry lock file ([`bc47a65`](https://github.com/ral-facilities/datagateway-api/commit/bc47a65952371290dd927d053371bd166540ba95))

* use icat5 ansible ([`023e7c7`](https://github.com/ral-facilities/datagateway-api/commit/023e7c734e0a77d33d0d7088eb22665776824091))

* make changes from review ([`1d43086`](https://github.com/ral-facilities/datagateway-api/commit/1d4308608a948fd073f2953ecdde5ea3d298f644))

* generate swagger to false ([`cff0177`](https://github.com/ral-facilities/datagateway-api/commit/cff017709bf48250ce38b5ebe94928dea4512f6d))

* Correct example config ([`b60b39e`](https://github.com/ral-facilities/datagateway-api/commit/b60b39ebb2ca63d91fb0ebb0e354f8f8738ae689))

* use poetry 1.1 for github actions ([`1d3059b`](https://github.com/ral-facilities/datagateway-api/commit/1d3059bb469c11863940315cbce38902438107d5))

* Fix linter and safety ([`5d09b14`](https://github.com/ral-facilities/datagateway-api/commit/5d09b14cc4a78e37c6d12cf451bd582ff99ae956))

* Change log file creation in actions to use yq instead of jq ([`94dc710`](https://github.com/ral-facilities/datagateway-api/commit/94dc710797a79dcc21a02ef327d9dab988407119))

* Debug github actions ([`7f26f2d`](https://github.com/ral-facilities/datagateway-api/commit/7f26f2d411e02317870626cab469bf2f8c89617b))

* Update github actions and readme ([`432b940`](https://github.com/ral-facilities/datagateway-api/commit/432b9408884fa5b0b525f259e636105a1b92bf89))

* add yaml configurations to gitignore ([`2ae0a20`](https://github.com/ral-facilities/datagateway-api/commit/2ae0a20c3e7d5f4563d2e782e2a32cc07e5b0e90))

* create example yaml config ([`be34683`](https://github.com/ral-facilities/datagateway-api/commit/be3468388d1c1eab564480005c13f8d27e735fc7))


## v5.1.1 (2022-09-22)

### Fix

* fix: update to latest dependencies ([`11a0eeb`](https://github.com/ral-facilities/datagateway-api/commit/11a0eeb3cbc4b5db2a0fa8dcd825dbeceb6ac111))

### Unknown

* Merge pull request #382 from ral-facilities/dependency/dparse

fix: update dparse to 0.5.2 ([`71625f8`](https://github.com/ral-facilities/datagateway-api/commit/71625f81a964f17ac5e32c52a9fc555e73b38aac))

* Minimise dependencies changed ([`75646db`](https://github.com/ral-facilities/datagateway-api/commit/75646dbe88acf78bf4c20b8f4487617af9492e80))


## v5.1.0 (2022-05-25)

### Feature

* feat: support skip and limit string parameters on search-api ([`db94b37`](https://github.com/ral-facilities/datagateway-api/commit/db94b375438873969db2d05621d9860a304ca8bd))

* feat: support skip and limit string parameters on search-api ([`eb74970`](https://github.com/ral-facilities/datagateway-api/commit/eb74970c1a74c6e0bed62460dab5ba5881ba1df7))

* feat: support skip/limit string parameters on search-api and added testing ([`8c3dde1`](https://github.com/ral-facilities/datagateway-api/commit/8c3dde11deb7614dfd22e6433c24727eeff2f800))

* feat: support skip/limit string parameters on search-api ([`d601ba7`](https://github.com/ral-facilities/datagateway-api/commit/d601ba7e9b48186e624db4891c503484f8895b2a))

### Test

* test: check for a different exception for invalid values ([`ab3839a`](https://github.com/ral-facilities/datagateway-api/commit/ab3839aba863756b0cdbd5e266d8d4e25576923e))

### Unknown

* Merge pull request #364 from antolinos/issue_363

This fixes the problem with limit when it is not a number ([`076e805`](https://github.com/ral-facilities/datagateway-api/commit/076e8059f83394ac124a1ed33a0bff15c192f1dc))

* Added test ([`a87b2e6`](https://github.com/ral-facilities/datagateway-api/commit/a87b2e62c78c3986d88302e7b3fd30b3573a6934))

* This fixes the problem with limit when it is not a number ([`562e458`](https://github.com/ral-facilities/datagateway-api/commit/562e45860430d4753b75db0076d2bafd687a6728))


## v5.0.1 (2022-05-16)

### Fix

* fix: fix internal server error when running DG API on its own #359 ([`b0d3e06`](https://github.com/ral-facilities/datagateway-api/commit/b0d3e064dc842143de7f7f0a31b947122fae9f88))

### Unknown

* Merge pull request #360 from ral-facilities/bugfix/500-internal-server-error-#359

500 Internal server error when running DG API on its own and sending Investigations request ([`ca638a7`](https://github.com/ral-facilities/datagateway-api/commit/ca638a77ab40d7c1a2efcae00874b9ddb8a1dc09))

* Merge pull request #253 from ral-facilities/rename-master-#252

Rename instances of &#34;master&#34; to &#34;main&#34; ([`c674205`](https://github.com/ral-facilities/datagateway-api/commit/c67420548dd4cf951c31195362557496880ce7bb))

* Merge pull request #353 from ral-facilities/swagger-readme

Update Swagger Interface README ([`29eabfd`](https://github.com/ral-facilities/datagateway-api/commit/29eabfd2f7e423e39f7c7ffd2ba4f3fbbeb31a37))

* Merge pull request #351 from ral-facilities/ci/python-3-10

Add Python 3.10 to CI Testing ([`c737a44`](https://github.com/ral-facilities/datagateway-api/commit/c737a44f29fb95293ec6548fd1293cce83c25782))


## v5.0.0 (2022-03-29)

### Breaking

* feat: add configuration option to set authenticator and its credentials in the search API #350

BREAKING CHANGE: This commits adds a mandatory config option, so is a major change. ([`1c30f2f`](https://github.com/ral-facilities/datagateway-api/commit/1c30f2f17c5bdc9a206ce3a41c7da81ce4be3b23))

### Build

* build: add Python 3.10 to tests nox session ([`9fa0b60`](https://github.com/ral-facilities/datagateway-api/commit/9fa0b605cc66b91a15f62fbdf551a392c109312b))

* build: upgrade `pycparser` version for Python 3.10 support ([`e07e6df`](https://github.com/ral-facilities/datagateway-api/commit/e07e6dfea7821f3f68a53df8be2e42dbaa8b2e1f))

### Ci

* ci: disable Poetry&#39;s new installer for Poetry 1.1.x ([`caf1861`](https://github.com/ral-facilities/datagateway-api/commit/caf186144e1d96d91ca2209b8aa434ef12de589c))

* ci: add Python 3.10 to GitHub Actions ([`9eb4526`](https://github.com/ral-facilities/datagateway-api/commit/9eb4526d18fb4d4f1c835ad09ac201b5675da0ad))

* ci: remove existing mysql install on GitHub Actions ([`5c1aa98`](https://github.com/ral-facilities/datagateway-api/commit/5c1aa98206e6d8ac94ba94247b89e37b0f7ce642))

### Documentation

* docs: update Swagger Interface section in README ([`e63adf8`](https://github.com/ral-facilities/datagateway-api/commit/e63adf8df372baffe4a3814ea5351eb961064f07))

* docs: update `flask run` commands in README ([`e85887e`](https://github.com/ral-facilities/datagateway-api/commit/e85887e12bef0a701610c0e198f437a7ff4a8c7b))

* docs: update README to include note for issue in Python 3.10 ([`72181f6`](https://github.com/ral-facilities/datagateway-api/commit/72181f61677a0fdfb7e5ac9a23a731f55ab4c421))

### Refactor

* refactor: change terminology from &#39;plugin&#39; to &#39;mechanism&#39; #350

- This just keeps the terminology in line with what we use in DataGateway API and more generally within ICAT ([`4a92ac0`](https://github.com/ral-facilities/datagateway-api/commit/4a92ac0d83c0129b2853fee9c8ffcada381518f3))

### Style

* style: fix linting as per CI results #350 ([`78d76c1`](https://github.com/ral-facilities/datagateway-api/commit/78d76c105a4fb1bba72187f9407ed9e9ea0b52fa))

### Test

* test: add new config options to mocked config #350

- This should allow the tests to pass now ([`75560b3`](https://github.com/ral-facilities/datagateway-api/commit/75560b365078246360c71adb8152745b51e38f08))

### Unknown

* Merge pull request #352 from antolinos/Allow-the-configuration-of-authentication-mechanisms-#350

Allow configuration of the authentication for the search api ([`1a1ee12`](https://github.com/ral-facilities/datagateway-api/commit/1a1ee1249181c985d1a240809b25dbb2a8bd0456))

* Merge branch &#39;master&#39; into Allow-the-configuration-of-authentication-mechanisms-#350 ([`8761800`](https://github.com/ral-facilities/datagateway-api/commit/876180054c021ada2fcdef87b7cb2b35f13b9e78))

* Merge pull request #349 from ral-facilities/ci/remove-mysql-icat-ansible

ci: remove existing mysql install on GitHub Actions ([`c6aa15e`](https://github.com/ral-facilities/datagateway-api/commit/c6aa15ea01545f7a8e58e656c569523c60f7e4ef))


## v4.3.0 (2022-03-18)

### Ci

* ci: move back to ICAT Ansible master branch ([`b1f46cf`](https://github.com/ral-facilities/datagateway-api/commit/b1f46cf66d1113636667725cb2631c2de2a580ac))

* ci: change ICAT Ansible host references to use underscores

- This relates to the changes made in https://github.com/icatproject-contrib/icat-ansible/issues/23 ([`a24e032`](https://github.com/ral-facilities/datagateway-api/commit/a24e03227a410e32bb11fecf8eba8e81fd85ea1c))

* ci: change ICAT Ansible branch ([`32554f6`](https://github.com/ral-facilities/datagateway-api/commit/32554f6c8d00babd2397a2f5e11bf46f46862b2e))

### Documentation

* docs: find and replace new instances of master #252 ([`9d6f649`](https://github.com/ral-facilities/datagateway-api/commit/9d6f649538e0e237ff965419737b871cdfd5e1b5))

### Test

* test: convert datetime formats on search endpoint tests #338 ([`939fc77`](https://github.com/ral-facilities/datagateway-api/commit/939fc77287f4c6bcbcae8c16a9a5e5a0627fe71d))

* test: fix datetime formatting on search API tests #338 ([`01968c0`](https://github.com/ral-facilities/datagateway-api/commit/01968c0a19ba38b75dc577a82046bc43cdd2edab))

### Unknown

* Merge pull request #340 from ral-facilities/feature/search-api-datetime-format-#338

Search API Datetime Format ([`a5cc190`](https://github.com/ral-facilities/datagateway-api/commit/a5cc190c9c973e2b0975a5b82ddb388939e24690))

* Merge branch &#39;master&#39; into feature/search-api-datetime-format-#338 ([`0fd45d0`](https://github.com/ral-facilities/datagateway-api/commit/0fd45d0cb122a64c936ed80f5a22afc1db6d4e85))

* Merge branch &#39;master&#39; into rename-master-#252 ([`ad0176e`](https://github.com/ral-facilities/datagateway-api/commit/ad0176e86162d269479096df0b71096ede93a351))

* Merge pull request #348 from ral-facilities/icat-ansible-dashes

ICAT Ansible Dashes to Underscores ([`464d754`](https://github.com/ral-facilities/datagateway-api/commit/464d754153f093ea32a786c632d26e8a427ca4a7))

* Change ICAT Ansible branch ([`3c622d5`](https://github.com/ral-facilities/datagateway-api/commit/3c622d5c2753ad4e8e2d729e11f95441206e0870))


## v4.2.0 (2022-02-28)

### Unknown

* Merge pull request #344 from ral-facilities/add-openapi-docs-for-search-api-#281

Add OpenAPI docs for Search API ([`aa98c51`](https://github.com/ral-facilities/datagateway-api/commit/aa98c51255d0500a2f306f541e922b42067209f5))


## v4.1.5 (2022-02-28)

### Unknown

* Merge pull request #346 from ral-facilities/bugfix/attribute-error-when-running-DG-API-on-its-own-#345

Fix AttributeError when trying to run DG API on its own ([`9cc9cdb`](https://github.com/ral-facilities/datagateway-api/commit/9cc9cdb2614aa442e942667dce695ee7afb46978))


## v4.1.4 (2022-02-28)

### Unknown

* Merge pull request #343 from ral-facilities/bugfix/validation-error-code-#319

Improve Search API Error Handling ([`982518a`](https://github.com/ral-facilities/datagateway-api/commit/982518a6afa019a9a1544b7b45a78f7a9c389ae5))


## v4.1.3 (2022-02-28)

### Unknown

* Merge pull request #342 from ral-facilities/example-query-tests-#270

Add Missing Endpoint Tests &amp; Fix parameters.value bug ([`6d5edf5`](https://github.com/ral-facilities/datagateway-api/commit/6d5edf5e7f5b6b0fc5977d83c810b1fa58e919de))


## v4.1.2 (2022-02-28)

### Build

* build: set Python ICAT as default backend in example config file #318 ([`6d92917`](https://github.com/ral-facilities/datagateway-api/commit/6d92917ecd6fb29e7394cecdfe19996918f94082))

### Documentation

* docs: add openapi yaml files #281 ([`d4fc795`](https://github.com/ral-facilities/datagateway-api/commit/d4fc79564fec3dd0f128bf30937d8d70c2b03dd3))

* docs: Add docs to `GET` Search API `CountFilesEndpoint` #281 ([`ba367a0`](https://github.com/ral-facilities/datagateway-api/commit/ba367a02f612a042c9c9d274d05b63202534de76))

* docs: Add docs to `GET` Search API `FilesEndpoint` #281 ([`53c2f8c`](https://github.com/ral-facilities/datagateway-api/commit/53c2f8c3d2b71270a881f8ad59aac45a225daadd))

* docs: Add docs to `GET` Search API `CountEndpoint` #281 ([`2e34d7a`](https://github.com/ral-facilities/datagateway-api/commit/2e34d7a0632429baf5c1d48f1044a0f7e979cd0e))

* docs: Add docs to `GET` Search API `EndpointWithID` #281 ([`f211c57`](https://github.com/ral-facilities/datagateway-api/commit/f211c57d668862e469a98c1c4504781fe17e8504))

* docs: Add docs to `GET` Search API `Endpoint` #281 ([`d407f0a`](https://github.com/ral-facilities/datagateway-api/commit/d407f0ad98a72547333f1b1ccb3930c5c39b0926))

* docs: update README to include resolution to setuptools issue ([`4bab813`](https://github.com/ral-facilities/datagateway-api/commit/4bab813d0897e987e085260d270b0496fe8e85f3))

* docs: correct markdown URL #320

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`0a9c05a`](https://github.com/ral-facilities/datagateway-api/commit/0a9c05a4e151e7bf6db5833dfa760d6de576663c))

* docs: add remaining suggested changes to README #320 ([`d5d358c`](https://github.com/ral-facilities/datagateway-api/commit/d5d358c1f43573be7f0f443d4a20a9bd54a7c634))

* docs: make suggested changes #320

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`d04447d`](https://github.com/ral-facilities/datagateway-api/commit/d04447d835e049127ba15ef981f69a63b85ff015))

### Feature

* feat: create openapi endpoint for Search API #281 ([`412458c`](https://github.com/ral-facilities/datagateway-api/commit/412458cc4cc73230db0115bdbfdfe6ac815d42c1))

* feat: allow multiple datetime formats to be used when filtering in search API #338 ([`f20ad24`](https://github.com/ral-facilities/datagateway-api/commit/f20ad24886f85bb3ba70abfd29352b1a7e5c58ff))

### Fix

* fix: fix `AttributeError` when running DG API on its own #345 ([`7479cc3`](https://github.com/ral-facilities/datagateway-api/commit/7479cc3e17ec046082e08b7e71e8e63eb7fa6e28))

* fix: improve error handling for search API exceptions #319 ([`935f22d`](https://github.com/ral-facilities/datagateway-api/commit/935f22d31d96c6810cf7938815b25c8822d892fb))

* fix: fix `parameters.value` WHERE filter with between operator #270 ([`3fe8dfe`](https://github.com/ral-facilities/datagateway-api/commit/3fe8dfe79ac7e070db369471859b1793e54a0852))

* fix: fix requests which include parameters and filter on them #319 ([`598bf9f`](https://github.com/ral-facilities/datagateway-api/commit/598bf9f5c9fbf71b87a3313680617b8addbe5cc9))

* fix: output datetime data in the same format as SciCat #338 ([`4596db9`](https://github.com/ral-facilities/datagateway-api/commit/4596db98808f35488aca86667aa26811d777b58e))

### Refactor

* refactor: change `LRUCache` import #321 ([`e1fd0a4`](https://github.com/ral-facilities/datagateway-api/commit/e1fd0a40da16630215eae5176d925207c06420f3))

### Test

* test: improve code coverage for search API error formatting #319 ([`1e42981`](https://github.com/ral-facilities/datagateway-api/commit/1e4298107c489f3927fd3b7b31cdaf10e37db0f4))

* test: add missing endpoint tests for example implementation queries #270

- Some tests rely on ICAT 5 so have been skipped until this is released ([`2c21bab`](https://github.com/ral-facilities/datagateway-api/commit/2c21bab1a1a539ea10656254f9e4a315d712b262))

* test: use original test data #313 ([`20c43b6`](https://github.com/ral-facilities/datagateway-api/commit/20c43b6ef6dffb1f8bf83e124cf53616dc06a7a2))

* test: fix nox tests session on Windows #307 ([`f6d2520`](https://github.com/ral-facilities/datagateway-api/commit/f6d25203d93fdcfeac7296e4ac370d2f765e65ad))

* test: fix nox tests session on Windows #307 ([`b65cf0e`](https://github.com/ral-facilities/datagateway-api/commit/b65cf0e1f4b152c52b209bb0ea43f32f7b821e3c))

### Unknown

* Merge pull request #341 from ral-facilities/bugfix/including-parameters-#319

Fix requests which include parameters and filter on them ([`6741c8b`](https://github.com/ral-facilities/datagateway-api/commit/6741c8b32313679440da6c5bb20d329dbdbe13d8))

* create and initialise Search API spec #281 ([`5e249d9`](https://github.com/ral-facilities/datagateway-api/commit/5e249d9fcb7389ca12e4c6ae2d3191bb2c0cc0cc))

* create swaggerui blueprint for Search API #281 ([`d358d94`](https://github.com/ral-facilities/datagateway-api/commit/d358d941bd48f820d816327b96994a289ef25de5))

* Merge pull request #339 from ral-facilities/setuptools-docs

Add Setuptools Issue to README ([`dd8bc51`](https://github.com/ral-facilities/datagateway-api/commit/dd8bc51ef4b09c9f59c2a1aeb380fd1f7c2c9f8f))

* Merge pull request #333 from ral-facilities/search-api-docs-#320

Search API Documentation ([`60a599e`](https://github.com/ral-facilities/datagateway-api/commit/60a599eab9182bcf4a1bce1218d1bfd9bd02b97b))

* Merge pull request #335 from ral-facilities/test-coverage-search-api

Increase Search API Code Coverage ([`e9deada`](https://github.com/ral-facilities/datagateway-api/commit/e9deada2306c5c3419378d4a27617b0fb3f7d918))

* Merge pull request #337 from ral-facilities/fix-nox-test-session-on-windows-#307

Fix failing Nox tests session on Windows ([`8b613da`](https://github.com/ral-facilities/datagateway-api/commit/8b613dacaf12b5f711a5362c6dc8d88a99fc8375))

* Merge branch &#39;fix-nox-test-session-on-windows-#307&#39; of github.com:ral-facilities/datagateway-api into fix-nox-test-session-on-windows-#307 ([`3416127`](https://github.com/ral-facilities/datagateway-api/commit/3416127382f462e4a861e39f9b1e46e707cf6ac2))

* Merge pull request #336 from ral-facilities/fix-lrucache-deprecation-warning-#321

Fix cachetools.LRUCache DeprecationWarning ([`c8d7939`](https://github.com/ral-facilities/datagateway-api/commit/c8d793940c353e8f8121e6f169bbe3dca28e0d33))

* Merge pull request #334 from ral-facilities/change-default-dg-api-backend-#318

Change Default DataGateway API Backend to Python ICAT ([`8d2264d`](https://github.com/ral-facilities/datagateway-api/commit/8d2264d160dc5a8d14c0f15b945bf21ec1f15569))

* Merge branch &#39;master&#39; into test-coverage-search-api ([`6a048c0`](https://github.com/ral-facilities/datagateway-api/commit/6a048c02db408ae29882d01028b4ed21601267b2))

* Merge branch &#39;change-default-dg-api-backend-#318&#39; of github.com:ral-facilities/datagateway-api into change-default-dg-api-backend-#318 ([`f15522f`](https://github.com/ral-facilities/datagateway-api/commit/f15522f3fcbbb2b592d1c0e6317511323c81a8a4))

* set Python ICAT as default backend in example config file #318 ([`23dacb3`](https://github.com/ral-facilities/datagateway-api/commit/23dacb380685f732f82186f9bcf303fae4228dc2))


## v4.1.1 (2022-02-17)

### Build

* build: omit certain lines/files from code coverage #313

- This commit adds a dev dependency which is used to conditionally exclude lines of code from test coverage reporting. There is a particular line of code in `models.py` which is only used in Python 3.7+, so for 3.6, this line can be excluded from coverage checks ([`0587a66`](https://github.com/ral-facilities/datagateway-api/commit/0587a66488a331522f093f7ccf54db3a016f041f))

### Test

* test: increase test coverage for search API #313 ([`d62e45a`](https://github.com/ral-facilities/datagateway-api/commit/d62e45a700f65631a62783c22cb36615cd8847a8))

### Unknown

* Merge pull request #330 from ral-facilities/bugfix/wrong-calculation-for-ispublic-fields-#329

Wrong calculation for isPublic field values ([`41962c7`](https://github.com/ral-facilities/datagateway-api/commit/41962c7389ee80a64876599362aa6f8e6607b9be))

* Merge branch &#39;bugfix/wrong-calculation-for-ispublic-fields-#329&#39; into test-coverage-search-api ([`e1ee64c`](https://github.com/ral-facilities/datagateway-api/commit/e1ee64cdf77ee80704199e868e0f65cd24f12948))


## v4.1.0 (2022-02-16)

### Chore

* chore: move Postman collection to `util/` #320 ([`4e17c6a`](https://github.com/ral-facilities/datagateway-api/commit/4e17c6abbb07a201638fcbcc83519a55e3c3d90f))

### Documentation

* docs: update docs for search API #320 ([`2daf395`](https://github.com/ral-facilities/datagateway-api/commit/2daf3956805dc0476e3d400d52b20a8b51f0e309))

### Feature

* feat: add search API error formatting as per specification #296 ([`3a5a3e8`](https://github.com/ral-facilities/datagateway-api/commit/3a5a3e83a1a2ce677a50a39b38d71133fea5121a))

### Fix

* fix: ignore filters on `isPublic` fields #329 ([`d6c10d5`](https://github.com/ral-facilities/datagateway-api/commit/d6c10d56b788ff3c491feaf1fae3a6fadd634a9d))

* fix: hardcode `isPublic` value to `True` #329 ([`64f62c2`](https://github.com/ral-facilities/datagateway-api/commit/64f62c217de760d22afae3e15d4774173eddbb48))

### Refactor

* refactor: return empty list when filtering for non-public data #329 ([`5f65725`](https://github.com/ral-facilities/datagateway-api/commit/5f65725dc73bcacbb54bd4bada3f8eec95303806))

### Test

* test: test where filter on isPublic fields #329 ([`c70b9e9`](https://github.com/ral-facilities/datagateway-api/commit/c70b9e9fa1b7551243722dda93b9fbb70d8e4c10))

* test: fix failing tests #329 ([`d8725ab`](https://github.com/ral-facilities/datagateway-api/commit/d8725abe9086dea1b9d1867ff2d2f37f52f32ddc))

* test: improve tests for `@queries_records` #296

- Previously, asserting the status code was unreachable ([`dd94c1a`](https://github.com/ral-facilities/datagateway-api/commit/dd94c1a86492edc6a3cb0f0b8799aaa2d065601e))

* test: add tests for search API error signalling #296 ([`5193af1`](https://github.com/ral-facilities/datagateway-api/commit/5193af199ef4e66645312b58553c5c4190ee98b3))

* test: fix failing tests #329 ([`e8beb57`](https://github.com/ral-facilities/datagateway-api/commit/e8beb57eb43bff604b2fc8b2a3007097a73e177c))

* test: remove `test_valid_where_filter` tests added in bugfix/filters-on-ispublic-panosc-field-#308 #329 ([`f8c823e`](https://github.com/ral-facilities/datagateway-api/commit/f8c823e093b9fa3919842b4241de12a80fa0795b))

* test: remove ICAT mappings for isPublic fields in mappings fixture #329 ([`df5bfce`](https://github.com/ral-facilities/datagateway-api/commit/df5bfce361d3f8c1d20ef6834aefc9b9d31e57c4))

### Unknown

* Merge pull request #331 from ral-facilities/error-signalling

Search API Error Signalling/Formatting ([`aefafcc`](https://github.com/ral-facilities/datagateway-api/commit/aefafcc10cbcdc21cccceaa5883b02a5ef47161b))

* remove config value added in make-num-years-determining-public-data-configurable-#312 #329 ([`05ad0e6`](https://github.com/ral-facilities/datagateway-api/commit/05ad0e6bc0f85417009fc1d3581bc32e7dca990b))

* remove ICAT mappings for `isPublic` fields #329 ([`d7bba35`](https://github.com/ral-facilities/datagateway-api/commit/d7bba355335ce7b71d8ff66ee663bd7feb0eec89))

* remove `isPublic` field changes from bugfix/filters-on-ispublic-panosc-field-#308 #329 ([`8d0496d`](https://github.com/ral-facilities/datagateway-api/commit/8d0496dafc8b3ae2b2500ebca734c83a9b6ac05c))


## v4.0.1 (2022-02-11)

### Fix

* fix: use alternative ICAT mapping for Technique pid when pid is None #314 ([`bf1c830`](https://github.com/ral-facilities/datagateway-api/commit/bf1c8305fc73630fbf1e6c4771664d974c72fd93))

* fix: use alternative ICAT mapping for Instrument pid when pid is None #314 ([`ae7e57a`](https://github.com/ral-facilities/datagateway-api/commit/ae7e57a0c6ece928cbb053ae41ba1214fb3199f8))

* fix: use alternative ICAT mapping for Document pid when doi is None #314 ([`736c6bd`](https://github.com/ral-facilities/datagateway-api/commit/736c6bdacc06e9ed2f9fff93a157920b66d2b887))

* fix: use alternative ICAT mapping for Dataset pid when doi is None #314 ([`b813f3d`](https://github.com/ral-facilities/datagateway-api/commit/b813f3d71d312b72c5a602b7520978208bd05754))

### Test

* test: fix failing tests #314 ([`35569fb`](https://github.com/ral-facilities/datagateway-api/commit/35569fbce0d94e6b92b2480011cd5b9362af6453))

* test: test logic related to setting of Technique pid #314 ([`393156a`](https://github.com/ral-facilities/datagateway-api/commit/393156a523495ade3833b1184dcecddf8ebaee68))

* test: update Technique mappings in mappings fixture #314 ([`7640e8d`](https://github.com/ral-facilities/datagateway-api/commit/7640e8dbf3bbf8c9be227e61143390c45b80febd))

* test: test logic related to setting of Instrument pid #314 ([`29583b1`](https://github.com/ral-facilities/datagateway-api/commit/29583b1ad37750535c81796af5750a31858ae8bf))

* test: update Instrument mappings in mappings fixture #314 ([`3385282`](https://github.com/ral-facilities/datagateway-api/commit/338528277edc4562d755597e834cade8c57503da))

* test: test logic related to setting of Document pid #314 ([`07d6a8e`](https://github.com/ral-facilities/datagateway-api/commit/07d6a8ef6de284e1c475d4668a7e7426596a87c4))

* test: update Document mappings in mappings fixture #314 ([`341ee51`](https://github.com/ral-facilities/datagateway-api/commit/341ee5156db537d5bd4384d5fff95f9d4a0b31d7))

* test: test logic related to setting of Dataset pid #314 ([`559e8b8`](https://github.com/ral-facilities/datagateway-api/commit/559e8b82dce4c96eacc1be44723090886ecd089b))

* test: update `Dataset` mappings in mappings fixture #314 ([`6206e9c`](https://github.com/ral-facilities/datagateway-api/commit/6206e9c732c68c782069f000f283ae7f5bcc1004))

### Unknown

* Merge pull request #324 from ral-facilities/bugfix/validation-error-sample-pid-panosc-field-#314

Validation error for Sample pid field when ICAT value is None ([`48c1e29`](https://github.com/ral-facilities/datagateway-api/commit/48c1e297967e9af9765a28e36ff43016da6718f6))

* add alternative ICAT mapping field to Technique pid PaNOSC field #314 ([`2a4a54c`](https://github.com/ral-facilities/datagateway-api/commit/2a4a54c700f9e5623afa78fb549707429bb415cd))

* add alternative ICAT mapping field to Instrument pid PaNOSC field #314 ([`62a7a7f`](https://github.com/ral-facilities/datagateway-api/commit/62a7a7f9d026907a08445397610a6d75f976e0a9))

* add alternative ICAT mapping field to Document pid PaNOSC field #314 ([`3801417`](https://github.com/ral-facilities/datagateway-api/commit/3801417b639070ab9b40c663946dccb7bb0460c9))

* add alternative ICAT mapping field to Dataset pid PaNOSC field #314 ([`faab544`](https://github.com/ral-facilities/datagateway-api/commit/faab5442b6914f5fd8ed938fc0ce1f51e7f2f43a))

* Merge branch &#39;master&#39; into bugfix/validation-error-sample-pid-panosc-field-#314 ([`bed6dec`](https://github.com/ral-facilities/datagateway-api/commit/bed6dec1090ba11e799defa500a087f123718bf4))


## v4.0.0 (2022-02-10)

### Breaking

* feat(config)!: add configuration option for determining public data #312 ([`58e777b`](https://github.com/ral-facilities/datagateway-api/commit/58e777b5c4a562f6945adcd1b55ce1d470f5d816))

### Refactor

* refactor: apply suggestions from PR review #314

Co-authored-by: Matthew Richards &lt;32678030+MRichards99@users.noreply.github.com&gt; ([`e7fa1b1`](https://github.com/ral-facilities/datagateway-api/commit/e7fa1b12abd80fb783f0b5ced199cf9c274aea38))

### Test

* test: fix failing count with `isPublic` condition tests #312 ([`20e3cb1`](https://github.com/ral-facilities/datagateway-api/commit/20e3cb1445e62a35a44e175ec578358ef3b5b769))

### Unknown

* Merge pull request #325 from ral-facilities/make-num-years-determining-public-data-configurable-#312

Make Number of Years to Determine Public Data Configurable ([`9e2fb9a`](https://github.com/ral-facilities/datagateway-api/commit/9e2fb9a98f111fae15a4e5a136ffc89978260cc5))

* determine public data based on config value #312 ([`1021c80`](https://github.com/ral-facilities/datagateway-api/commit/1021c802f84e298a8a61dc6563804ce8a6eade72))


## v3.6.1 (2022-02-07)

### Unknown

* Merge pull request #323 from ral-facilities/bugfix/filters-on-ispublic-panosc-field-#308

Cannot Use Filters on isPublic Field ([`9ee06a4`](https://github.com/ral-facilities/datagateway-api/commit/9ee06a494dff9fa79330f7f04f30b0e0c8db237a))


## v3.6.0 (2022-02-07)

### Ci

* ci: add anon user to ICAT Server rootUserNames #268 ([`22a0ea8`](https://github.com/ral-facilities/datagateway-api/commit/22a0ea850435d0f4ca4326b7525c5a0fa1d1d8a5))

### Fix

* fix: use alternative ICAT mapping for Sample pid when pid is None #314 ([`7e211f7`](https://github.com/ral-facilities/datagateway-api/commit/7e211f74aa4fa81ab26c339b27806a64510f261c))

* fix: convert `isPublic` PaNOSC filter to appropriate ICAT filter #308 ([`6a40307`](https://github.com/ral-facilities/datagateway-api/commit/6a40307ba19d5818bdb6bf1acc79d98abd6a3f83))

* fix: make WHERE filter without operator work with int and bool #322 ([`6988a5a`](https://github.com/ral-facilities/datagateway-api/commit/6988a5aa5d6dfa71fd4b90a73b050864e8530955))

* fix: make get by pid endpoints return data in PaNOSC format #266 ([`0de2b5b`](https://github.com/ral-facilities/datagateway-api/commit/0de2b5b2b713699b66164ca5732888f997230aa5))

### Refactor

* refactor: refactor entity relations code #268 ([`4343a2c`](https://github.com/ral-facilities/datagateway-api/commit/4343a2c67cdba63a0b21e552b7d630eaf0b46cd6))

* refactor: move ICAT relations call to filter handler #268 ([`8840a6c`](https://github.com/ral-facilities/datagateway-api/commit/8840a6cfe4134421d60fa2acdf329d4d737e151c))

* refactor: make `get_with_pid()` more efficient by calling `get_search()` #266 ([`73b70bd`](https://github.com/ral-facilities/datagateway-api/commit/73b70bd756949fc23b7d4e58d6cdf5c3038a219b))

### Test

* test: correct order of actual and expected results in test #314 ([`5d6dab9`](https://github.com/ral-facilities/datagateway-api/commit/5d6dab9f394cf2d23a02d02a5aaa3834cc0d736d))

* test: test logic related to setting of `Sample` `pid` #314 ([`c390d73`](https://github.com/ral-facilities/datagateway-api/commit/c390d733c9993bff2ea4a353fd3669fda24fa500))

* test: update `Sample` mappings in mappings fixture #314 ([`c96a34a`](https://github.com/ral-facilities/datagateway-api/commit/c96a34a65033d42aa899c59b9146d0819fb7b29d))

* test: fix failing `isPublic` field endpoint tests #308 ([`c40639d`](https://github.com/ral-facilities/datagateway-api/commit/c40639dd0ee3234577ed806fb98c09119643bcd2))

* test: test conversion of `isPublic` PaNOSC filter #308 ([`dc85ca4`](https://github.com/ral-facilities/datagateway-api/commit/dc85ca4889dd8ff64e75cc6e2a1cc03c8407d1c4))

* test: unskip endpoint tests and inject data #266, #268 ([`de26303`](https://github.com/ral-facilities/datagateway-api/commit/de2630327bdc9806409cb75871e9712cbe086a2e))

* test: update pid type on endpoint rules #268 ([`e428328`](https://github.com/ral-facilities/datagateway-api/commit/e428328e3281c4a75ee6979850db157b3efb58d1))

* test: fix tests after fixing bug #268 ([`f1539db`](https://github.com/ral-facilities/datagateway-api/commit/f1539db866400caa8cee4080b4c0e4e906f8af22))

### Unknown

* Merge pull request #302 from ral-facilities/feature/search-endpoints-#268

Implement Search API Endpoints ([`afad6de`](https://github.com/ral-facilities/datagateway-api/commit/afad6de63cf184b24d31fffaa851c422fd055f43))

* add alternative ICAT mapping field to Sample pid PaNOSC field #314 ([`58b3850`](https://github.com/ral-facilities/datagateway-api/commit/58b385046f4d96d4940e7e2f678a337dd6b5acbd))

* raise `FilterError` when invalid operator is used with bool value #308 ([`184c894`](https://github.com/ral-facilities/datagateway-api/commit/184c8944d97f9899ad2d632eda1118fde325ea97))

* Merge branch &#39;master&#39; into feature/search-endpoints-#268 ([`efdc2a6`](https://github.com/ral-facilities/datagateway-api/commit/efdc2a61fce57b44920f513dbb7f2c9d7dc8d3a5))


## v3.5.3 (2022-02-02)

### Unknown

* Merge pull request #304 from ral-facilities/include-icat-relations-for-non-related-panosc-fields

Include ICAT relations for non-related PaNOSC fields ([`fad4c3e`](https://github.com/ral-facilities/datagateway-api/commit/fad4c3e9748feeb7c2e529a72b15a3ba5142ec2a))


## v3.5.2 (2022-02-02)

### Fix

* fix: make `ne` and `neq` operators work with non-numeric values #315 ([`f5e3b4b`](https://github.com/ral-facilities/datagateway-api/commit/f5e3b4b1bfebd25c6d6fb288eb3f5a79daf87dac))

### Test

* test: fix failing `ne` and `neq` operator tests #315 ([`f74efc0`](https://github.com/ral-facilities/datagateway-api/commit/f74efc0861fe0a5230a39444a640ad5f9084a0ba))

### Unknown

* Merge pull request #316 from ral-facilities/bugfix/non-numeric-values-with-neq-operator-#315

Make ne and neq operators work with non-numeric values ([`a13e699`](https://github.com/ral-facilities/datagateway-api/commit/a13e699f71ebca76deeb789f46584038a2c00553))

* Merge branch &#39;master&#39; into include-icat-relations-for-non-related-panosc-fields ([`1faba30`](https://github.com/ral-facilities/datagateway-api/commit/1faba3024b27844fdd0a5ff3d20e6fc0f42eb17e))


## v3.5.1 (2022-01-31)

### Unknown

* Merge pull request #301 from ral-facilities/feature/search-api-include-filter-#261

Implement Include Filter for Search API ([`10d1ca8`](https://github.com/ral-facilities/datagateway-api/commit/10d1ca826d5d2a285aaec689a6a71052eef8f354))


## v3.5.0 (2022-01-31)

### Style

* style: remove unused import #261 ([`5da48f8`](https://github.com/ral-facilities/datagateway-api/commit/5da48f8393bf9c52de38bd2410d63dd85508a023))

### Unknown

* Merge pull request #300 from ral-facilities/feature/icat-to-panosc-data-model-conversion-#265

ICAT to PaNOSC Data Model Conversion ([`2609aae`](https://github.com/ral-facilities/datagateway-api/commit/2609aaeec6ee5b7b34fbb23baa0a728afceadd43))

* Merge branch &#39;master&#39; into feature/search-endpoints-#268 ([`2fe980d`](https://github.com/ral-facilities/datagateway-api/commit/2fe980d05b8355ca93c0624588cea074d73ad257))

* Merge branch &#39;master&#39; into feature/search-api-include-filter-#261 ([`e0b2d95`](https://github.com/ral-facilities/datagateway-api/commit/e0b2d95e8ab60aae1b50309456b754bd7488ce66))

* Merge branch &#39;master&#39; into feature/icat-to-panosc-data-model-conversion-#265 ([`f17038d`](https://github.com/ral-facilities/datagateway-api/commit/f17038dfef55ee95e6bc00b057ce781958edc172))


## v3.4.0 (2022-01-31)

### Refactor

* refactor: update PaNOSC Parameter name mapping in example file #265 ([`358ac22`](https://github.com/ral-facilities/datagateway-api/commit/358ac22504b6869686c4caf6b47282fda916cb60))

### Test

* test: correct query params on tests #268 ([`2fed560`](https://github.com/ral-facilities/datagateway-api/commit/2fed560a82794c68850e1e94f156bc8d96685226))

* test: remove test that&#39;s no longer needed #261 ([`950b9aa`](https://github.com/ral-facilities/datagateway-api/commit/950b9aae6cec0aa8e2eabd04ffa0561ad74c1185))

### Unknown

* Merge pull request #303 from ral-facilities/implement-search-api-where-filter-operators-#297

Implement Search API WHERE Filter Operators ([`4946d8e`](https://github.com/ral-facilities/datagateway-api/commit/4946d8ec7de9ae828fee266c996f221378d72eb3))

* Merge branch &#39;master&#39; into implement-search-api-where-filter-operators-#297 ([`92918ac`](https://github.com/ral-facilities/datagateway-api/commit/92918ac492ef3b50bbf499d7be0cb76b526c4621))

* Merge branch &#39;master&#39; into feature/search-api-include-filter-#261 ([`1af6e38`](https://github.com/ral-facilities/datagateway-api/commit/1af6e381d5623b24f835920a6993f4b377770b2a))

* Merge branch &#39;master&#39; into feature/icat-to-panosc-data-model-conversion-#265 ([`fca1a59`](https://github.com/ral-facilities/datagateway-api/commit/fca1a593f00f0ba9d5f3827d56ed3c3467578e06))


## v3.3.0 (2022-01-31)

### Build

* build: update example mappings ([`f94d361`](https://github.com/ral-facilities/datagateway-api/commit/f94d361d3050dcfa62a2a600917cb59721715e3f))

### Style

* style: fix typo #265 ([`3f1b2d6`](https://github.com/ral-facilities/datagateway-api/commit/3f1b2d6a1d216d9596e5cda2c261e0911324f541))

### Test

* test: update mappings on tests #260 ([`63d7c21`](https://github.com/ral-facilities/datagateway-api/commit/63d7c21e87f1a793b309f9c031d2a921d8f3ede8))

* test: tweak query params tests to avoid Parameter entity #259 ([`2f0afa0`](https://github.com/ral-facilities/datagateway-api/commit/2f0afa05101b411510bbb5f15c91c78fdc9db243))

### Unknown

* Merge pull request #298 from ral-facilities/filter-input-conversion

Start Defining PaNOSC to ICAT Mapping and Implement WHERE Filter ([`942b3cf`](https://github.com/ral-facilities/datagateway-api/commit/942b3cf051658b69a0efc5a2348a938c43f893d9))

* Merge branch &#39;master&#39; into filter-input-conversion ([`a34786c`](https://github.com/ral-facilities/datagateway-api/commit/a34786c21447439d10ec991f634a06f9c9688f5b))


## v3.2.0 (2022-01-31)

### Build

* build: upgrade `python-icat` to 0.21.0 #305 ([`8e472cf`](https://github.com/ral-facilities/datagateway-api/commit/8e472cff813cd2b5953824c763909dd904276321))

* build: use older version of `setuptools` when running tests ([`2b66602`](https://github.com/ral-facilities/datagateway-api/commit/2b66602cbeae0d74aff77df33f810ff1188fe579))

### Ci

* ci: use older version of `setuptools` to solve Python ICAT build issue ([`e4cfb38`](https://github.com/ral-facilities/datagateway-api/commit/e4cfb383f846bdec3aed14d9a0837f5d3f629156))

* ci: add steps to make mapping file in GitHub Actions #265 ([`6845659`](https://github.com/ral-facilities/datagateway-api/commit/68456590d38e785a81f02e5d08a0c34451cefc02))

### Documentation

* docs: add new comments and fix existing #265 ([`3f1b1cf`](https://github.com/ral-facilities/datagateway-api/commit/3f1b1cffdd1e57ab4eb1227b13e0906424adefd0))

* docs: add docstrings for Flask resource classes #268

- Also updated the existing ones for DataGateway API ([`a5aee61`](https://github.com/ral-facilities/datagateway-api/commit/a5aee61cc55e70931163371f3c1abecb31b1fb3a))

* docs: add docstring to static function #260 ([`618f6b9`](https://github.com/ral-facilities/datagateway-api/commit/618f6b9fead88f61a346b90cb2b85a90877b0410))

### Feature

* feat: implement `regexp` operator #297 ([`bf3fe0e`](https://github.com/ral-facilities/datagateway-api/commit/bf3fe0ef2ac582d55dbd881edf6a81a93625ce91))

* feat: implement `neq` operator #297 ([`9094bbb`](https://github.com/ral-facilities/datagateway-api/commit/9094bbb894ead20a53fadfd0e24b264af29548b9))

* feat: implement `nin` operator #297 ([`00dbba5`](https://github.com/ral-facilities/datagateway-api/commit/00dbba525d5cd86cb5577f3b1621a7042cdd2fa0))

* feat: implement `inq` operator #297 ([`fc1cf19`](https://github.com/ral-facilities/datagateway-api/commit/fc1cf194454a4da60652b1f68df278c4624ddc11))

* feat: implement `between` operator #297 ([`4736888`](https://github.com/ral-facilities/datagateway-api/commit/4736888bf76cda0dbc00f997443ed565f0f5e760))

* feat: implement search API endpoints #266, #267, #268 ([`dcc332e`](https://github.com/ral-facilities/datagateway-api/commit/dcc332e352ded8af25dce7dae635bd62417d2c13))

* feat: implement basic version of `SearchAPIIncludeFilter` #261 ([`f2f53c9`](https://github.com/ral-facilities/datagateway-api/commit/f2f53c92229d052ae697787eb80a35dcd2ea3b45))

* feat: add function to get PaNOSC to ICAT mapping for where filter #260 ([`34b1d81`](https://github.com/ral-facilities/datagateway-api/commit/34b1d819482aa3efdb4f8da321125d3e40d76617))

### Fix

* fix: fix list type field checking in Python 3.6 #265 ([`691a59e`](https://github.com/ral-facilities/datagateway-api/commit/691a59ea3f850475572c3a877fb739e5216c6fe7))

* fix: add logic to deal with `PythonICATIncludeFilter` that could be related for ICAT relations for non-related PaNOSC fields #268 ([`29232c6`](https://github.com/ral-facilities/datagateway-api/commit/29232c6b2c032c61999118b2f69177f3b9bd5d57))

* fix: retrieve non-related fields that have a list of ICAT relations #265 ([`2c5edc5`](https://github.com/ral-facilities/datagateway-api/commit/2c5edc50f9f713b0d15e137ad4a307a90a86b5aa))

* fix: fix nested relations bug #261 ([`67fcbfe`](https://github.com/ral-facilities/datagateway-api/commit/67fcbfe2a35ca2b7e007a1a6d78105b2e46b0b5f))

* fix: fix example mapping file ([`3802cc9`](https://github.com/ral-facilities/datagateway-api/commit/3802cc9ee71a355d0ad87529f65112e8c3f8b881))

* fix: reference self instead of fixed instance #301

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`40f5662`](https://github.com/ral-facilities/datagateway-api/commit/40f566279543871c5b7b1eab2c8b74050d8b3525))

* fix: correct order of arguments for where filter #266 ([`1e38eae`](https://github.com/ral-facilities/datagateway-api/commit/1e38eaee9f201a45742cf868ad2fa28f4adee065))

* fix: update `__str__()` for WHERE filter to cope with applying filter #260 ([`8d259d7`](https://github.com/ral-facilities/datagateway-api/commit/8d259d75a28414f26cc569293720ef4e306e6844))

### Refactor

* refactor: refactor `from_icat` abstract method #265 ([`71765a5`](https://github.com/ral-facilities/datagateway-api/commit/71765a590d996b9935299ebfb3de305660542ca1))

* refactor: refactor `_get_icat_field_value` logic #265 ([`1d730d1`](https://github.com/ral-facilities/datagateway-api/commit/1d730d1d07a523d2b636d905911a5073aa51d305))

* refactor: replace `fromisoformat` with `str_to_datetime_object` #265 ([`0bbcc0d`](https://github.com/ral-facilities/datagateway-api/commit/0bbcc0d4f762c52b9fa4a4b558fff1a44fbd40b7))

* refactor: update PaNOSC `Parameter` mappings in example file #265 ([`601c51b`](https://github.com/ral-facilities/datagateway-api/commit/601c51b29cd29fbad687d83084202996e7eb4714))

* refactor: move logic for including ICAT relations of non-related fields of related entities #265 ([`49cfe08`](https://github.com/ral-facilities/datagateway-api/commit/49cfe084426bfcf5b7f5e0620a708b3959367cbd))

* refactor: move `filter_order_handler.py` to `common` #265 ([`ff637e7`](https://github.com/ral-facilities/datagateway-api/commit/ff637e7d65a4758ed96c7b803da5e6789ce2f097))

* refactor: update PaNOSC `Parameter` mappings in example file #265 ([`524f8a9`](https://github.com/ral-facilities/datagateway-api/commit/524f8a953af0f3bf9a9b2e52289e245fea582589))

* refactor: add argument for `required_related_fields` on endpoint #268 ([`68fa3b3`](https://github.com/ral-facilities/datagateway-api/commit/68fa3b3763e2745f3c365d9390777fe327ddd6de))

* refactor: update PaNOSC mappings

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`c13c0db`](https://github.com/ral-facilities/datagateway-api/commit/c13c0db07a1a23a662d5ce32d7fb2f4709bc282d))

* refactor: implement new Python ICAT changes for read-only queries #260

- This removes lots of the complexities of the previous way to build complex WHERE clauses ([`2478ffa`](https://github.com/ral-facilities/datagateway-api/commit/2478ffafee4b5ee4854d24b224c4c812ebd6c179))

* refactor: make changes for new Python ICAT implementation #259 ([`f61ed00`](https://github.com/ral-facilities/datagateway-api/commit/f61ed00c69853e4b4d00d5d610c93dcd5aa9057a))

* refactor: merge logic for `in` and `inq` operators #297 ([`3211dfb`](https://github.com/ral-facilities/datagateway-api/commit/3211dfb277e4466895f89af70b770f262b2581c7))

* refactor: merge logic for `ne` and `neq` operators #297

Co-authored-by: Matthew Richards &lt;32678030+MRichards99@users.noreply.github.com&gt; ([`8b344ef`](https://github.com/ral-facilities/datagateway-api/commit/8b344ef9d7bf04cbe55467c2b6eabcff325a8a33))

* refactor: remove duplicated code for `between` operator validation #297 ([`bd15023`](https://github.com/ral-facilities/datagateway-api/commit/bd15023dc7ed56126540eab49fc34b454544b52c))

* refactor: update PaNOSC mappings

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`80c066c`](https://github.com/ral-facilities/datagateway-api/commit/80c066cb1e5c70cedcd37aa8f598bbdf557692ac))

* refactor: deal with case when list of ICAT field values are found #265 ([`98f9157`](https://github.com/ral-facilities/datagateway-api/commit/98f9157938abc829493569e32672640b30645304))

* refactor: deal with case when list of ICAT field names are found #265 ([`956a902`](https://github.com/ral-facilities/datagateway-api/commit/956a9023fd56678e5e461a70208898ce566f4138))

* refactor: make field types non-strict #265 ([`3cbf11b`](https://github.com/ral-facilities/datagateway-api/commit/3cbf11b5be6aeb371ba7210893db87ab7358dcdf))

* refactor: address TODO in `models.py` #265 ([`b0983bb`](https://github.com/ral-facilities/datagateway-api/commit/b0983bb0baa0bf0848d21d759fd3d5cb9dabddeb))

* refactor: change expected data type of pid #268

- This matches the PaNOSC data model ([`71a0852`](https://github.com/ral-facilities/datagateway-api/commit/71a0852707cd34773f04c2c3baecbe1e2df9cf7a))

* refactor: change method signatures of search API endpoint helpers #268

- The endpoint name won&#39;t actually be used in the endpoint code, only the entity name will be
- Also changed `get_with_id()` to `get_with_pid()` as all use cases will be with a persistent identifier ([`b0f4b13`](https://github.com/ral-facilities/datagateway-api/commit/b0f4b1358abb309656eb7b206cc025b516254094))

* refactor: Pass kwargs into query class #268

- This allows the `COUNT` keyword to be specified during a search API endpoint ([`34fa7d9`](https://github.com/ral-facilities/datagateway-api/commit/34fa7d9896985da0bc3c1686cf40a28109d48b1f))

* refactor: make query params more efficient to create less include filter objects for multiple and nested related entities #261 ([`eab7f3d`](https://github.com/ral-facilities/datagateway-api/commit/eab7f3d9d10eb36a998653a492c99476fc7f46d9))

* refactor: small refactors based on PR review comments #260 ([`d368778`](https://github.com/ral-facilities/datagateway-api/commit/d3687781fb880ce716618e9df94288ab2b45c25c))

* refactor: move `get_icat_mapping()` into `PaNOSCMappings` #261

- I&#39;ve moved the code which deals with the parameter value field name list away from this function to make the function more generic/reusable. That code has been moved to applying the WHERE filter, where it&#39;ll be used. The mapping will not be reached by an include filter (under a valid API request) because the parameter values are for a field name/attribute, not a related entity ([`00ee21d`](https://github.com/ral-facilities/datagateway-api/commit/00ee21d1bf0489b344fb58d092cc57154a3983e3))

* refactor: move text operator fields into the entity classes #260 ([`5b71f09`](https://github.com/ral-facilities/datagateway-api/commit/5b71f0947303dae3061347a69cd064b4a4096700))

* refactor: make mapping file the example file #265

- Added filename of the &#39;actual&#39; mapping file to git ignore ([`b20c9b4`](https://github.com/ral-facilities/datagateway-api/commit/b20c9b439bbae937c5f770b09546db3621c09992))

* refactor: remove unused function and place functionality within `SearchAPIWhereFilter.apply_filter()` #260

- This commit also has fixes for tests relevant to this change ([`4f16776`](https://github.com/ral-facilities/datagateway-api/commit/4f16776f206340ec931eebed75480b731de8dc6b))

* refactor: make `filters` mandatory #260

- When called from an endpoint, `filters` will always be passed in, even if it is an empty list ([`b256eaf`](https://github.com/ral-facilities/datagateway-api/commit/b256eaf251130988ac7d0f404508583ea7758ffd))

* refactor: change `SearchAPIQuery` attribute name for better readability #260 ([`5f2c2be`](https://github.com/ral-facilities/datagateway-api/commit/5f2c2be8e9d158c252b95c92f34255db7e3f8c33))

* refactor: rename function #260 ([`33e92e7`](https://github.com/ral-facilities/datagateway-api/commit/33e92e7d816e4e91d8d9812411aa6b08b5f84413))

* refactor: add improved error message for Python ICAT WHERE filter issues #260 ([`4e05d64`](https://github.com/ral-facilities/datagateway-api/commit/4e05d64f25d5483be8557f461f92ff127876a2ca))

### Style

* style: address linting warnings #265 ([`a253422`](https://github.com/ral-facilities/datagateway-api/commit/a2534223af50b68c4195f843e8bac13d8d988bef))

* style: general linting fixes #268 ([`d14c327`](https://github.com/ral-facilities/datagateway-api/commit/d14c327cd40a665697b420747e113b44310dcd36))

* style: fix linting issues #260 ([`8267de0`](https://github.com/ral-facilities/datagateway-api/commit/8267de0435d88d0a34843a033b46ba95cfd95f1d))

* style: make suggested changes from PR review #260 ([`3afccd2`](https://github.com/ral-facilities/datagateway-api/commit/3afccd2e938b7d718bc9b8b5140ab9088f0268d8))

* style: add logging to WHERE filter work #260 ([`7dd4fd2`](https://github.com/ral-facilities/datagateway-api/commit/7dd4fd2839addd75af5ded11325544a735f3f808))

* style: fix linting issues #260 ([`bfad399`](https://github.com/ral-facilities/datagateway-api/commit/bfad39985757a23af500fd1c2643fad41190a0e8))

* style: remove unneeded code #260 ([`cba6482`](https://github.com/ral-facilities/datagateway-api/commit/cba6482519e112bba2ae21ff320728a5a631b184))

* style: fix linting issues #260 ([`9ee5395`](https://github.com/ral-facilities/datagateway-api/commit/9ee539563038c8af5bfe2b55ab252b23b3d5ac2a))

### Test

* test: add additional `isPublic` test for endpoints #268 ([`12bdde5`](https://github.com/ral-facilities/datagateway-api/commit/12bdde5bdd164a1f7e2c69329c90b084f1f3cb52))

* test: remove code for replacing datetime timezone #265 ([`5571722`](https://github.com/ral-facilities/datagateway-api/commit/557172212c07efea7a7d7ea85793446cc0f80566))

* test: add search API endpoints #268

- Lots of skips have been added for bugs I&#39;ve found and need to be fixed ([`bc2aabd`](https://github.com/ral-facilities/datagateway-api/commit/bc2aabd0199766a883d25ba099aa5be98c511b2c))

* test: fix tests following updates to PaNOSC `Parameter` mappings #265 ([`d595ceb`](https://github.com/ral-facilities/datagateway-api/commit/d595cebf354e95cd3d4fa229229594ec131e4441))

* test: update `Parameter` mappings in mappings fixture #265 ([`1e8badb`](https://github.com/ral-facilities/datagateway-api/commit/1e8badb9fae458ee5d0be2a67d3774ef9a198e10))

* test: test logic for including ICAT relations of non-related fields of related entities #265 ([`8a33bf3`](https://github.com/ral-facilities/datagateway-api/commit/8a33bf38eac273b6e71edaf1adc0d51680e89d1d))

* test: move `test_filter_order_handler.py` to `test` dir #265 ([`e3b28e4`](https://github.com/ral-facilities/datagateway-api/commit/e3b28e468ef72286a93d95f7e44921889abdb344))

* test: remove invalid test case #265

A Document cannot have parameters that have dataset ([`23200cd`](https://github.com/ral-facilities/datagateway-api/commit/23200cd9e69230cb9aaad5634a0144899bde2122))

* test: update `Parameter` mappings in mappings fixture #265 ([`cdacc7b`](https://github.com/ral-facilities/datagateway-api/commit/cdacc7b97a84f61972cad1614770522dd7ec5509))

* test: fix existing endpoint test data #268 ([`7ba059c`](https://github.com/ral-facilities/datagateway-api/commit/7ba059cfe3b027be7ed003df58f7965addddd589))

* test: unit test method for getting ICAT relations for non-related fields of PaNOSC relation #265 ([`516a9e2`](https://github.com/ral-facilities/datagateway-api/commit/516a9e266330a7f7f50b4bb35acb1d0f237b5f85))

* test: unit test method for getting ICAT relations of PaNOSC non-related fields #265 ([`5fccba7`](https://github.com/ral-facilities/datagateway-api/commit/5fccba78e5a109c4289414a66212ae63e1cbab6e))

* test: unit test method for getting non related field names of PaNOSC entity #265 ([`b8178a2`](https://github.com/ral-facilities/datagateway-api/commit/b8178a2b903475b0f7e6db039fec1e8d52cdf838))

* test: unit test logic for nested required related fields #265 ([`e52d595`](https://github.com/ral-facilities/datagateway-api/commit/e52d5958bd8c8fe0b1dab79f91f2e95787723cc7))

* test: test `regexp` operator #297 ([`f25333f`](https://github.com/ral-facilities/datagateway-api/commit/f25333f25791d927ab4601e942fa5e63bac3df6c))

* test: test `neq` operator #297 ([`5817491`](https://github.com/ral-facilities/datagateway-api/commit/5817491ea90dc4dca5868b0e35475e534ad95878))

* test: test `nin` operator #297 ([`8d57256`](https://github.com/ral-facilities/datagateway-api/commit/8d572564fbb48714df5276543259aadeb26cb2f4))

* test: test `inq` operator #297 ([`1b14214`](https://github.com/ral-facilities/datagateway-api/commit/1b142143fb27750e4745d73a5eeb12ce6267849b))

* test: test `between` operator #297 ([`f5525c9`](https://github.com/ral-facilities/datagateway-api/commit/f5525c9230240671744534f34919d9511a118374))

* test: unit test `from_icat` raises `ValidationError` #265 ([`701eb74`](https://github.com/ral-facilities/datagateway-api/commit/701eb740ce09a98424bf72088a45c2adf8419797))

* test: unit test `from_icat` `Technique` entity creation #265 ([`fb836c7`](https://github.com/ral-facilities/datagateway-api/commit/fb836c7ebb7305d87b05f9322465fea4c7edf9d0))

* test: unit test `from_icat` `Sample` entity creation #265 ([`077c279`](https://github.com/ral-facilities/datagateway-api/commit/077c27952d883b96c560cf67e01eb1218ba5a991))

* test: unit test `from_icat` `Person` entity creation #265 ([`c05a70d`](https://github.com/ral-facilities/datagateway-api/commit/c05a70d40e271aede4ae0c4ebdb724536dbb8b33))

* test: unit test `from_icat` `Parameter` entity creation #265 ([`faed594`](https://github.com/ral-facilities/datagateway-api/commit/faed59477105b9dcfe75bf018d6b8229ff048a2e))

* test: unit test `from_icat` `Member` entity creation #265 ([`f2845e3`](https://github.com/ral-facilities/datagateway-api/commit/f2845e31a1530a56e006e5d455e985bf621c1ea9))

* test: unit test `from_icat` `Instrument` entity creation #265 ([`0d0a1e4`](https://github.com/ral-facilities/datagateway-api/commit/0d0a1e4875952175ad63dc9882058051f4dcf2d2))

* test: unit test `from_icat` `File` entity creation #265 ([`0554bea`](https://github.com/ral-facilities/datagateway-api/commit/0554bea8082735780a1c8edef24ebf171df04bea))

* test: unit test `from_icat` `Dataset` entity creation #265 ([`8f2a6c1`](https://github.com/ral-facilities/datagateway-api/commit/8f2a6c1a5104a38132f173dd131a0a01dec63a26))

* test: unit test `from_icat` `Dataset` entity creation #265 ([`3631c61`](https://github.com/ral-facilities/datagateway-api/commit/3631c616e44ffaf4a177f3ba3fec00a1965217f4))

* test: unit test `from_icat` `Affiliation` entity creation #265 ([`07058a0`](https://github.com/ral-facilities/datagateway-api/commit/07058a047ee1dcd48d85c1369393361684aea9ad))

* test: define test data #265 ([`66f0261`](https://github.com/ral-facilities/datagateway-api/commit/66f026129955fb12e979c145563db5b4995843a1))

* test: add basic valid tests for search API endpoints #266, #267, #268 ([`a17fb9a`](https://github.com/ral-facilities/datagateway-api/commit/a17fb9a0f0b3a2deb91c3c244d3749d994d64cbd))

* test: add tests for `SearchAPIIncludeFilter` #261 ([`fc4556c`](https://github.com/ral-facilities/datagateway-api/commit/fc4556cf6a63715928c847b125e55c187818b281))

* test: add tests for `PaNOSCMappings` #260 ([`985d433`](https://github.com/ral-facilities/datagateway-api/commit/985d433f3c4a5a1b5a6af30af3d9f9606f800a4a))

* test: move `TestDataGatewayAPIQueryFilterFactory` into non-backend specific directory #260 ([`0944d39`](https://github.com/ral-facilities/datagateway-api/commit/0944d39cb48542d6691ee04aa7831970dfe51d67))

* test: fix test caused by lack of ICAT 5.0 #260

- The mapping file contains ICAT field names which will only be present in the upcoming release of ICAT 5.0, therefore the test gets an error from Python ICAT when trying to use them ([`cf70161`](https://github.com/ral-facilities/datagateway-api/commit/cf701615127cd213fd9f3327ef4daced7c3c6d70))

* test: change pytest fixture to `SearchAPIQuery` #260 ([`9937c36`](https://github.com/ral-facilities/datagateway-api/commit/9937c361a3ee97d0be90e7a76a0a6802807fe0c0))

* test: add more PaNOSC hop test cases #260 ([`40320f2`](https://github.com/ral-facilities/datagateway-api/commit/40320f2b5a19b0aec841d5c3c6557807d5429d75))

* test: add test cases to cover ICAT parameter values #260 ([`08605af`](https://github.com/ral-facilities/datagateway-api/commit/08605afe7e0aba134a6e7d5fe1af50393091b370))

* test: fix tests for changes made to the class #260

- Input to init is now expected to be different, so this has been changed to suit ([`bcd5ec3`](https://github.com/ral-facilities/datagateway-api/commit/bcd5ec39b7d99761860196dd113bb570fd76c46a))

* test: rename filter test files and fix them for recent changes made #260 ([`6b82732`](https://github.com/ral-facilities/datagateway-api/commit/6b82732cec3e47abf9092659f84573260e49ad7b))

* test: make further changes to WHERE filter tests #260 ([`ebb7528`](https://github.com/ral-facilities/datagateway-api/commit/ebb7528fe894af038b4f94f83a6fe76a3fc75cca))

### Unknown

* Merge pull request #292 from ral-facilities/feature/query-params-search-api-#259

Query Parameters Inputs for Search API ([`d6506ac`](https://github.com/ral-facilities/datagateway-api/commit/d6506ac504b3761441e2ebde2586642747a66614))

* Merge branch &#39;master&#39; into feature/query-params-search-api-#259 ([`d913af1`](https://github.com/ral-facilities/datagateway-api/commit/d913af186aab87803a74b5e3ec99bb5a7a05020d))

* Merge branch &#39;master&#39; into filter-input-conversion ([`dbe684e`](https://github.com/ral-facilities/datagateway-api/commit/dbe684ea355ee1fbeda069359ca90e3220228853))

* Merge pull request #306 from ral-facilities/upgrade-python-icat-#305

Upgrade Python ICAT to 0.21.0 ([`c4bd953`](https://github.com/ral-facilities/datagateway-api/commit/c4bd953f76b726f91e3b9ecb2ae6d8eaa13ac991))

* Merge branch &#39;feature/icat-to-panosc-data-model-conversion-#265&#39; of github.com:ral-facilities/datagateway-api into feature/icat-to-panosc-data-model-conversion-#265 ([`3f463fb`](https://github.com/ral-facilities/datagateway-api/commit/3f463fb51164b11a5b33d5c4b72736117d798b50))

* Apply suggestions from code review #265

Co-authored-by: Matthew Richards &lt;32678030+MRichards99@users.noreply.github.com&gt; ([`299cbcd`](https://github.com/ral-facilities/datagateway-api/commit/299cbcdd46672eb4424066d44891e03fd7c41115))

* add logging #265 ([`e1f199d`](https://github.com/ral-facilities/datagateway-api/commit/e1f199d5c62a317140c3c72f30d12e50a686b8cb))

* Merge branch &#39;filter-input-conversion&#39; into include-icat-relations-for-non-related-panosc-fields ([`2beb861`](https://github.com/ral-facilities/datagateway-api/commit/2beb8616f1efe66ec9981827bebda59d66e70ba7))

* Merge branch &#39;include-icat-relations-for-non-related-panosc-fields&#39; into feature/search-endpoints-#268 ([`003bf40`](https://github.com/ral-facilities/datagateway-api/commit/003bf405d46d8f7788a07d0240f0841c80c954bb))

* Merge branch &#39;feature/icat-to-panosc-data-model-conversion-#265&#39; into feature/search-endpoints-#268 ([`4648c5a`](https://github.com/ral-facilities/datagateway-api/commit/4648c5af32279a459fbcf2630651c2a31345a266))

* Merge branch &#39;filter-input-conversion&#39; into feature/search-api-include-filter-#261 ([`80a5ca7`](https://github.com/ral-facilities/datagateway-api/commit/80a5ca7d5bef76cce70afc2f162fe01121ae786d))

* Merge branch &#39;filter-input-conversion&#39; of github.com:ral-facilities/datagateway-api into filter-input-conversion ([`7cc6c5a`](https://github.com/ral-facilities/datagateway-api/commit/7cc6c5a8d54d7cfdd195938e960757786b855605))

* Merge branch &#39;filter-input-conversion&#39; into feature/icat-to-panosc-data-model-conversion-#265 ([`7f4cd96`](https://github.com/ral-facilities/datagateway-api/commit/7f4cd96a3790ed559995df738f882d0ed8e138c3))

* Merge branch &#39;feature/query-params-search-api-#259&#39; into filter-input-conversion ([`d7e2d81`](https://github.com/ral-facilities/datagateway-api/commit/d7e2d81532a17cc9159d755a6f88cfa3b10aea52))

* Merge branch &#39;implement-search-api-where-filter-operators-#297&#39; of github.com:ral-facilities/datagateway-api into implement-search-api-where-filter-operators-#297 ([`b8ca890`](https://github.com/ral-facilities/datagateway-api/commit/b8ca890bcadebae5b8892cf5a29f06627ad10566))

* include all ICAT relations of non-related fields when querying ICAT #265 ([`27866f9`](https://github.com/ral-facilities/datagateway-api/commit/27866f93a711742f0ab3e9ff38011171b59418e9))

* implement method for getting ICAT relations for non-related fields of PaNOSC related entities #265 ([`d888053`](https://github.com/ral-facilities/datagateway-api/commit/d88805393ca9b124152214f5fbc9bd70fcd05ac7))

* implement method for getting ICAT relations for non-related fields of PaNOSC entity #265 ([`a314849`](https://github.com/ral-facilities/datagateway-api/commit/a314849030ab0314bdf7f359d598d3f122d23c73))

* implement method for getting non related field names of PaNOSC entity #265 ([`4ced97a`](https://github.com/ral-facilities/datagateway-api/commit/4ced97a21a74ad18989621b8a22028ba40169796))

* add logic for dealing with nested required related fields #265 ([`d606d6b`](https://github.com/ral-facilities/datagateway-api/commit/d606d6b1514e95aecc423b9aa33fae3e0eb86136))

* validate values supplied with `nin` operator #297 ([`92b5f36`](https://github.com/ral-facilities/datagateway-api/commit/92b5f36389d16f5c79f0199d7dd1408eda688d7a))

* validate values supplied with `inq` operator #297 ([`b0134b8`](https://github.com/ral-facilities/datagateway-api/commit/b0134b8882c2c75f666b9c5516c49e1f06c4d72d))

* validate values supplied with `between` operator #297 ([`d254642`](https://github.com/ral-facilities/datagateway-api/commit/d254642c4cf28168c47c8eacdc8fcbf90e1c1943))

* update `Parameter` mappings in example file #265 ([`e691f24`](https://github.com/ral-facilities/datagateway-api/commit/e691f249d5a0b13534396cf0fef9868726b1a562))

* work out if dataset or document is public #265 ([`eca0a46`](https://github.com/ral-facilities/datagateway-api/commit/eca0a46ec6c649cb0786bad7b145efd7f9910775))

* disable dataset and document validator in Parameter entity #265 ([`94dcfba`](https://github.com/ral-facilities/datagateway-api/commit/94dcfbaed9ea5206979bdc51db466ee2a88790cb))

* feature: deal with required related entity cases #265 ([`3ceb365`](https://github.com/ral-facilities/datagateway-api/commit/3ceb36549daec7b48bde1084114fd8e395f96263))

* set plural entity fields to default to empty list #265 ([`ce9e2af`](https://github.com/ral-facilities/datagateway-api/commit/ce9e2afe48b45cc4ed61d1e1ae4f4ed4bbef4e78))

* set signular related entity fields to default to `None` #265 ([`ea29f47`](https://github.com/ral-facilities/datagateway-api/commit/ea29f47a214bd00f398ad3381ed2b54ed2e2b833))

* set non-related optional entity fields to default to `None` #265 ([`c183a85`](https://github.com/ral-facilities/datagateway-api/commit/c183a850376b213ecce6379a854b4168573e7f99))

* Merge branch &#39;feature/search-api-include-filter-#261&#39; into feature/icat-to-panosc-data-model-conversion-#265 ([`3d8447e`](https://github.com/ral-facilities/datagateway-api/commit/3d8447ece89cd8eb901a089e6d49ee0c59b3d725))

* Merge branch &#39;feature/search-api-include-filter-#261&#39; into feature/search-endpoints-#268 ([`e0b54ea`](https://github.com/ral-facilities/datagateway-api/commit/e0b54ea17c775aea256450ce788f85268ff2a02d))

* Merge branch &#39;filter-input-conversion&#39; into feature/search-api-include-filter-#261 ([`95319a8`](https://github.com/ral-facilities/datagateway-api/commit/95319a8c81fb610fb4522955e54ca59d2f59664c))

* conversion proof of concept #265 ([`85c4bfc`](https://github.com/ral-facilities/datagateway-api/commit/85c4bfc94cffc7c0c1664b78bb0824921aa286db))

* Merge pull request #299 from ral-facilities/ci/setuptools-fix

Fix CI for Python ICAT Build Issue ([`f3e5c20`](https://github.com/ral-facilities/datagateway-api/commit/f3e5c203fa96fec3ce673509457e0ef6b3221323))

* resolve TODOs for PaNOSC to ICAT mapping file #265 ([`5aa4510`](https://github.com/ral-facilities/datagateway-api/commit/5aa451094a5c3293e79e4910ee2f61bef9dd761d))

* add functionality for applying WHERE filter #260 ([`694f7f2`](https://github.com/ral-facilities/datagateway-api/commit/694f7f283321597aa0f026a2354e120dc29abe94))

* fix various edge cases for `SearchAPIQueryFilterFactory` #260 ([`e820c31`](https://github.com/ral-facilities/datagateway-api/commit/e820c3139dba5bad4f383849a82dbb115da6d3f3))

* change text operator fields to entity name format #260

- This change is prompted because the `entity_name` will always be in entity name format, rather than field name format ([`c5f2e74`](https://github.com/ral-facilities/datagateway-api/commit/c5f2e74cdd6a388f0c67aed1bcdc7b20bff30001))

* add init code to deal with `self.search_api_query` #260 ([`9d95948`](https://github.com/ral-facilities/datagateway-api/commit/9d95948a2ee03be25fbabba531352f081c4a6119))

* add function to fetch entity name from a related field name #260 ([`9a9e957`](https://github.com/ral-facilities/datagateway-api/commit/9a9e957469c495714a4310910541c15292e830ec))

* add TODOs for additional operators that need to be implemented #260 ([`f91a4ef`](https://github.com/ral-facilities/datagateway-api/commit/f91a4ef2de10a0cb6c1397356ea325d8951bb67a))

* add code to search endpoints to handle filters #260

- This code has been added to manually test how the filters are working looking at an entire request from start to finish ([`82ae018`](https://github.com/ral-facilities/datagateway-api/commit/82ae0189905bca38d382401a4b4f43f35a01c2b8))

* make nested WHERE filters more supportive of applying their data to Python ICAT #260 ([`eb96b09`](https://github.com/ral-facilities/datagateway-api/commit/eb96b092db4e580812ba4c4d9dbc7f86076108d9))

* add related entity mappings #265

- I&#39;ve added TODOs where there are things I&#39;m still slightly unsure about ([`29ddbf4`](https://github.com/ral-facilities/datagateway-api/commit/29ddbf4885aa6c59908d93f7292a9550985b168b))

* Merge branch &#39;feature/query-params-search-api-#259&#39; into filter-input-conversion ([`e1bd6cd`](https://github.com/ral-facilities/datagateway-api/commit/e1bd6cdfdadbfdc9f60cbc56d75f0d41b9475ea6))

* Merge branch &#39;master&#39; into feature/query-params-search-api-#259 ([`cafabc5`](https://github.com/ral-facilities/datagateway-api/commit/cafabc5bd5e3a88ed3f4cd333c508e3229d17d3c))

* Merge branch &#39;master&#39; into filter-input-conversion ([`8b4c216`](https://github.com/ral-facilities/datagateway-api/commit/8b4c21642b004a94742958b3b0c36c38eaf40986))


## v3.1.1 (2021-12-15)

### Feature

* feat: convert PaNOSC to ICAT for where filter fields #260 ([`ff9595d`](https://github.com/ral-facilities/datagateway-api/commit/ff9595d2f571211db79dea02f702d4148b8879f3))

### Fix

* fix: correct reference to class name #264 ([`fc4c180`](https://github.com/ral-facilities/datagateway-api/commit/fc4c18085ab496d838e8d1e9e3f8c77f07826e9d))

### Refactor

* refactor: set `get_condition_values` to return `tuple` #259 ([`229a6c8`](https://github.com/ral-facilities/datagateway-api/commit/229a6c80b55e2806d0cf9a82c662392c522760af))

* refactor: use alternative query for search API filters #265 ([`45a972a`](https://github.com/ral-facilities/datagateway-api/commit/45a972a1e8b64a811affc1914d01280874116be9))

* refactor: pass in endpoint and entity name into helper functions #265

- Entity name will be the format used in the mapping json file ([`d2eed60`](https://github.com/ral-facilities/datagateway-api/commit/d2eed600308f79406fab82d5ddb453c2773c7023))

* refactor: correct models following updates to data model guide #264 ([`6b18d63`](https://github.com/ral-facilities/datagateway-api/commit/6b18d63b2f9b69aca5290d82dba044c58470b664))

* refactor: remove `to_icat()` functions #264 ([`2753e6e`](https://github.com/ral-facilities/datagateway-api/commit/2753e6eb26db8a11b38a58e646775823f855daee))

* refactor: reference not-yet constructed models using string #264 ([`f2f0826`](https://github.com/ral-facilities/datagateway-api/commit/f2f0826fb513c1c94599d07a2aa2604aefc703b5))

* refactor: edit model to follow deliverable document more #264

- Where the deliverable document hasn&#39;t given sufficient detail, we have fallen back on the data models markdown. ([`84116af`](https://github.com/ral-facilities/datagateway-api/commit/84116af3a78538682ecaaa71cf69af7e70293174))

### Style

* style: change some variable names to increase code readability #259

- `filter_input` meant multiple things in that file so I&#39;ve gone and given new names in places ([`d0b949b`](https://github.com/ral-facilities/datagateway-api/commit/d0b949bb10a2e47b976941fcb0678fca3f7f3c3f))

* style: remove irrelevant comment #264 ([`b43db8a`](https://github.com/ral-facilities/datagateway-api/commit/b43db8a1369cda10c4b9d7dcc1ab33ff95992966))

* style: add docstrings to functions #259 ([`ed72451`](https://github.com/ral-facilities/datagateway-api/commit/ed7245195bf2cde391c35693f80a789fb95c2290))

* style: remove comments #264 ([`46c15cc`](https://github.com/ral-facilities/datagateway-api/commit/46c15cc35535332850fba3af528632f636b7f2f5))

### Test

* test: add tests to increase test coverage #259

- `test_get_condition_values()` didn&#39;t resolve the partial branch coverage but I thought I&#39;d commit it regardless because it might help us later on ([`e014af6`](https://github.com/ral-facilities/datagateway-api/commit/e014af6eee54f2e345a73ef29d4f310d4475c077))

* test: add tests for applying WHERE filters #260 ([`f326e02`](https://github.com/ral-facilities/datagateway-api/commit/f326e0288eb818c96fc7dcc464db7fb4f6c855e8))

* test: add limit and skip inside scope filter cases #259 ([`3f4eaa6`](https://github.com/ral-facilities/datagateway-api/commit/3f4eaa667a296a0e437b3da8a5a5bfa9b7500aa8))

* test: correct text operator tests #259 ([`072c3f0`](https://github.com/ral-facilities/datagateway-api/commit/072c3f023d93ae007e26380dc695bf482cfa975b))

* test: correct nested include filter tests #259 ([`3f6bd7d`](https://github.com/ral-facilities/datagateway-api/commit/3f6bd7d65db0dc2d2b3971cbc8abd938e9de565d))

* test: correct false fail test #259 ([`cd0a86e`](https://github.com/ral-facilities/datagateway-api/commit/cd0a86efc5af8386ab938e40fa9c1fc4543eb558))

* test: move filter tests to specific directory #260 ([`31e9e16`](https://github.com/ral-facilities/datagateway-api/commit/31e9e160c6bbcbe00d943dad45cea86ef00c56d1))

* test: fix imports #262 #263 ([`7310707`](https://github.com/ral-facilities/datagateway-api/commit/7310707b307e7d82d0bb6da49dbcac0ff6c692cf))

### Unknown

* Merge pull request #289 from ral-facilities/add-panosc-search-api-data-model-#264

Add PaNOSC Search API Data Model ([`206cea8`](https://github.com/ral-facilities/datagateway-api/commit/206cea8d3f7dece888ed99424210b6d5ea9799e9))

* Merge remote-tracking branch &#39;origin/add-panosc-search-api-data-model-#264&#39; into filter-input-conversion ([`ff745ec`](https://github.com/ral-facilities/datagateway-api/commit/ff745ec547ecf8384504c4c940dadd4053951b5f))

* raise `FilterError` if scope filter has a limit or skip filter #259 ([`bc4d3ba`](https://github.com/ral-facilities/datagateway-api/commit/bc4d3baa9be7fe277a5f600fd04e5cae4e2f58da))

* use `like` operation when creating where filter from text operator #259 ([`e2850d0`](https://github.com/ral-facilities/datagateway-api/commit/e2850d093ae8a86aeea2b502177e38cf156913f4))

* only create a single include filter object per nested include #259 ([`d2b3826`](https://github.com/ral-facilities/datagateway-api/commit/d2b3826a8026cdb5faf90e33f5fb88ae3a63a94f))

* prefix all where filters inside include filter with entity name #259 ([`c6d7ab5`](https://github.com/ral-facilities/datagateway-api/commit/c6d7ab5d3e2e7b50a24d40c599d111b4b910a958))

* Merge branch &#39;master&#39; into feature/query-params-search-api-#259 ([`7ae6e77`](https://github.com/ral-facilities/datagateway-api/commit/7ae6e77d8372b37b14efd4fcc2ccb0c0af188540))

* add basic implementation of `SearchAPIQuery` #265 ([`8479d23`](https://github.com/ral-facilities/datagateway-api/commit/8479d23c332fb95aa88fa450c2eb6792c78fce1a))

* add ISIS mappings for PaNOSC to ICAT models #265 ([`a081f4c`](https://github.com/ral-facilities/datagateway-api/commit/a081f4c16f59772a8e4962b34cf548d841ae14f6))

* add class to load PaNOSC mappings into the code #265 ([`f9bb6de`](https://github.com/ral-facilities/datagateway-api/commit/f9bb6deb3ffdb6d87d940a35a3455ef5a1518379))

* add blank mapping file #265 ([`978a8bd`](https://github.com/ral-facilities/datagateway-api/commit/978a8bd6fb2260597474da199817baa8c9b4f6bd))

* Merge branch &#39;add-panosc-search-api-data-model-#264&#39; into filter-input-conversion ([`9473782`](https://github.com/ral-facilities/datagateway-api/commit/9473782db97fd3a25bd3eaa34d6222643f9f24db))

* Merge branch &#39;feature/query-params-search-api-#259&#39; into filter-input-conversion ([`75f8a91`](https://github.com/ral-facilities/datagateway-api/commit/75f8a91acf62a3bb7fab37f24eb38d8fe2112e6d))

* Merge pull request #295 from ral-facilities/implement-limit-and-skip-filters

Implement Limit and Skip filters ([`dd23cce`](https://github.com/ral-facilities/datagateway-api/commit/dd23cce935102c99526668736a0ccbe0e8bf27d5))

* Merge branch &#39;master&#39; into implement-limit-and-skip-filters ([`a01072c`](https://github.com/ral-facilities/datagateway-api/commit/a01072c33c435477096282237ce11565bb5a3c81))


## v3.1.0 (2021-12-06)

### Feature

* feat: add class to represent nested conditions #259 ([`583cbf2`](https://github.com/ral-facilities/datagateway-api/commit/583cbf29744b72c020429b61ae7442b19acef231))

* feat: implement session/client handling for search API #258 ([`46a1539`](https://github.com/ral-facilities/datagateway-api/commit/46a1539398f63e9c8a6539d703a164dd7c8749e7))

### Refactor

* refactor: rename `PythonICATSkipFilter` use variable #263 ([`a474cfa`](https://github.com/ral-facilities/datagateway-api/commit/a474cfaa566057cd6e6e8cc5ae8a5a5b08891b06))

* refactor: remove `boolean_operator` from `SearchAPIWhereFilter` #259

- This is no longer used, boolean operators are managed by `NestedWhereFilters` ([`60cc5d1`](https://github.com/ral-facilities/datagateway-api/commit/60cc5d1006e6e9f0591531014bf36c4c4b44509e))

* refactor: clean up `SearchAPIQueryFilterFactory` #259 ([`4134a16`](https://github.com/ral-facilities/datagateway-api/commit/4134a1673a4cf239f32fe9dfce03fed903b4693d))

* refactor: allow `PythonICATSkipFilter` to use Search API config #263 ([`5ab60de`](https://github.com/ral-facilities/datagateway-api/commit/5ab60de0c48b7a2e63330b6278d547d29157bcce))

* refactor: move config to its own class #258

- This change has been made so the config can be mocked in tests ([`1cf73e4`](https://github.com/ral-facilities/datagateway-api/commit/1cf73e40c390532f0580156f0f6de442e5c3fd57))

* refactor: allow `ICATClient` to use search API config where appropriate #258

- This change will not impact the existing use of the class in DataGateway API ([`8dba0e1`](https://github.com/ral-facilities/datagateway-api/commit/8dba0e126ec00170eb9e4664b70ed1b461dd8a85))

### Style

* style: fix linting issues #259 ([`b0a4c47`](https://github.com/ral-facilities/datagateway-api/commit/b0a4c47416da78cbc093c4137f3f50c034abc518))

* style: make changes to satisfy flake8 #258 ([`a261774`](https://github.com/ral-facilities/datagateway-api/commit/a261774a6d31e351d5ac9ed313714ed103250550))

### Test

* test: remove print statement

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`67a119b`](https://github.com/ral-facilities/datagateway-api/commit/67a119b751ac9245b94595a7bc7b669a5c917ecd))

* test: fix imports #258 ([`8508af0`](https://github.com/ral-facilities/datagateway-api/commit/8508af015f0c16bf0d2a1d5fd9c441c6e24a7689))

* test: use alternate fixture

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`00c76b9`](https://github.com/ral-facilities/datagateway-api/commit/00c76b978634f6e73ef121e3c0b6e57a3df98688))

* test: refactor more query params tests #259 ([`605315c`](https://github.com/ral-facilities/datagateway-api/commit/605315c64cc3f8c445ca0bf83b73813bada785fd))

* test: refactor tests for where filter in include #259 ([`d6c62ea`](https://github.com/ral-facilities/datagateway-api/commit/d6c62ea64443eb8ee0f2c248d873d13ef8d4a9d1))

* test: remove test cases on things we&#39;re not going to support #259 ([`38d17a5`](https://github.com/ral-facilities/datagateway-api/commit/38d17a53cd7e58e72dbe1d4c1b9804331e2f5c51))

* test: refactor `TestSearchAPIQueryFilterFactory` #259 ([`1abaf66`](https://github.com/ral-facilities/datagateway-api/commit/1abaf6689e8f96af598f408d8106eeb3813390f0))

* test: fix text operator tests for query params #259 ([`9e404ed`](https://github.com/ral-facilities/datagateway-api/commit/9e404ed15b5a0501e19406daf9b1fb606c33d867))

* test: fix some query param tests #259

- It&#39;s a big ol&#39; file this! ([`2106e99`](https://github.com/ral-facilities/datagateway-api/commit/2106e9960da40aca18a913e29d9c2c7c6f6512d9))

* test: fix tests for `NestedWhereFilters` #259 ([`46cb5c3`](https://github.com/ral-facilities/datagateway-api/commit/46cb5c3bd72cea6f34f9b62084d17275941d72a2))

* test: add tests for `SearchAPISkipFilter` #263 ([`d8572ed`](https://github.com/ral-facilities/datagateway-api/commit/d8572eda0004192731b34e295cbff79e82856ead))

* test: add tests for `TestSearchAPILimitFilter` #262 ([`7257672`](https://github.com/ral-facilities/datagateway-api/commit/72576723c9e568a9686ce2dffb8e2c225e204596))

* test: create ICAT related test fixtures #262 #263 ([`2eb14cf`](https://github.com/ral-facilities/datagateway-api/commit/2eb14cf282ced9711dba6a4ca84501a9e261b056))

* test: add test cases for filter input with all filters #259 ([`60c3bad`](https://github.com/ral-facilities/datagateway-api/commit/60c3bade2374a599720f300fa380e11ac4ca1209))

* test: add more test cases for include filter with scope #259 ([`0f06917`](https://github.com/ral-facilities/datagateway-api/commit/0f0691782c10a2f805cf11d8ca8d90d0db4e6b36))

* test: add more test cases for where filters with boolean operators  #259 ([`8f90ac5`](https://github.com/ral-facilities/datagateway-api/commit/8f90ac5049ab9e7f009c894029d9a3bc1626b929))

* test: add initial tests for `NestedWhereFilters` #259

- I will likely add more tests to this class in the future, particularly to cover a mixture of `SearchAPIWhereFilter` and `NestedWhereFilters` ([`530f024`](https://github.com/ral-facilities/datagateway-api/commit/530f0242ed61e14d5bd360f6a3bd5faf873a252b))

* test: correct unit tests #259 ([`c39795c`](https://github.com/ral-facilities/datagateway-api/commit/c39795c4b5e4b04403f8bd1270f20267e7cb4269))

* test: fix failing tests and add more text operator test cases #259 ([`68b85ef`](https://github.com/ral-facilities/datagateway-api/commit/68b85efa8a9209219e8a64e0debe17a2005a4d08))

* test: add tests for search API session/client handling #258 ([`b7dea73`](https://github.com/ral-facilities/datagateway-api/commit/b7dea7378be9fee6c0323b7ec8b9608ff87996a3))

* test: move test config fixtures so they can be accessed by search API tests #258 ([`75bb983`](https://github.com/ral-facilities/datagateway-api/commit/75bb98382b0a4ab15a17217c1157aaa371e260a0))

* test: change output of endpoint helper function for load testing #258

- Testing done with Apache JMeter ([`71cc98a`](https://github.com/ral-facilities/datagateway-api/commit/71cc98a8aef0d0dfb85c4b988597f330793d7b8c))

### Unknown

* Merge pull request #294 from ral-facilities/feature/session-handling-#258

Search API Session/Client Handling ([`93905e3`](https://github.com/ral-facilities/datagateway-api/commit/93905e3a71ed6633a4fc582aa4e6aac23f47363b))

* make LHS and RHS support lists of WHERE filters #259

- Relevant for request filter inputs that come with 3 or more
- Test cases have been added to cover this as well as edge cases such as lists with a single filter in them ([`31c07ab`](https://github.com/ral-facilities/datagateway-api/commit/31c07abed5c35215f2e1a1de5d890270442a758f))

* add functionality to deal with an empty RHS #259

- Relevant when a filter input has a boolean operator but there&#39;s only one condition in that list. Makes the boolean operator redundant but is still an edge case we should support
- Additional test cases have been added to cover this ([`ea5deb0`](https://github.com/ral-facilities/datagateway-api/commit/ea5deb0bbeebe6955d9cf7a05d6fba2ff03d46fc))

* add `__repr__` functions for easier testing #259 ([`df323fe`](https://github.com/ral-facilities/datagateway-api/commit/df323fecd78dc0d37c84176597401db882c9233f))

* add string representation function to `SearchAPIWhereFilter` #259

- To be used by `NestedWhereFilters` when LHS or RHS has an input of this type ([`490470e`](https://github.com/ral-facilities/datagateway-api/commit/490470e1a92c046d567600c30911ccad23ebe3e2))

* add initial usage of `NestedWhereFilters into query params factory class #259 ([`2114858`](https://github.com/ral-facilities/datagateway-api/commit/211485817e91626d82a13002630572b04621db8d))

* move string conversion to `__str__()` #259

- This means when the input is of type `SearchAPIWhereFilter`, it won&#39;t execute Python ICAT code until the filter needs to be applied/processed ([`0c4f9ac`](https://github.com/ral-facilities/datagateway-api/commit/0c4f9ac194aea8b3393e203f6acf68de1ab53975))

* remove unused config items from example file #258 ([`67c308d`](https://github.com/ral-facilities/datagateway-api/commit/67c308d8373d8aa4bde214143bae32b6aa90d849))

* pass in entity name to `get_query_filter()` to be used by text operator #259 ([`1d24021`](https://github.com/ral-facilities/datagateway-api/commit/1d24021ce32fe7fa9843de7c438aa6713d4eb44e))

* use OR boolean operator for WHERE filters in text operator #259 ([`865bf97`](https://github.com/ral-facilities/datagateway-api/commit/865bf977623d93018a653aa13d0b9ea74c91041e))

* add support for nested AND/ OR #259 ([`a590514`](https://github.com/ral-facilities/datagateway-api/commit/a5905148e524fec250c1d381440cca0dc3fab7a7))

* move text operator logic to WHERE filter #259 ([`cdb30ff`](https://github.com/ral-facilities/datagateway-api/commit/cdb30ff0d4ebc8a0901e385d14bbd623f7c96fbb))

* Merge branch &#39;master&#39; into feature/query-params-search-api-#259 ([`434aeeb`](https://github.com/ral-facilities/datagateway-api/commit/434aeeb546bca4f171e4cd88b861c5ed29b705cc))

* add helper functions for each endpoint type for search API #258 ([`1049a5f`](https://github.com/ral-facilities/datagateway-api/commit/1049a5f82feef3f5909440e4e928a43f969c4219))


## v3.0.1 (2021-11-24)

### Fix

* fix: allow blank extensions and slash extension to be valid ([`70ddb7a`](https://github.com/ral-facilities/datagateway-api/commit/70ddb7a4fd89ba10b06cd71c3ab2a98648cfb773))

### Test

* test: correct test data

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`f4339f2`](https://github.com/ral-facilities/datagateway-api/commit/f4339f24d3f297323d215173a411873bd6920a84))

* test: add tests for extension validation logic ([`36b42c0`](https://github.com/ral-facilities/datagateway-api/commit/36b42c0899b298e4d7a546383dff3dbb06cce924))

### Unknown

* Merge pull request #293 from ral-facilities/bugfix/api-extension-validation

Extension Validation Bugfix ([`1a10fd4`](https://github.com/ral-facilities/datagateway-api/commit/1a10fd4f4a81e128d07435dbe5b89500f23a6dc7))


## v3.0.0 (2021-11-23)

### Breaking

* feat: configure end part of endpoint urls to contain api extension #283

BREAKING CHANGE: modify endpoint urls to use relevant api extension ([`5bdd72e`](https://github.com/ral-facilities/datagateway-api/commit/5bdd72ea911323cdf0fc7d9ec6fb419b8dd6006c))

### Style

* style: fix formatting and remove TODO #283 ([`9129288`](https://github.com/ral-facilities/datagateway-api/commit/9129288bd8b2d2080419720d62d5716a0983a7f2))

### Test

* test: fix failing tests #283 ([`6aac97b`](https://github.com/ral-facilities/datagateway-api/commit/6aac97b183e9ee3c43bd02cb986f8fb3ef017b6b))

### Unknown

* Merge pull request #290 from ral-facilities/respect-config-for-search-api-endpoints-#283

Respect Config for Search API Endpoints ([`20c46a1`](https://github.com/ral-facilities/datagateway-api/commit/20c46a15020e4294d6dbd291d9f9c31615e8e3fd))

* Merge branch &#39;respect-config-for-search-api-endpoints-#283&#39; of github.com:ral-facilities/datagateway-api into respect-config-for-search-api-endpoints-#283 ([`c029aae`](https://github.com/ral-facilities/datagateway-api/commit/c029aae951b1152022bb36d34983fd733f99b344))

* Merge branch &#39;master&#39; into respect-config-for-search-api-endpoints-#283 ([`0edfb2e`](https://github.com/ral-facilities/datagateway-api/commit/0edfb2e083b4426f50913479a67ff0fad68c5e48))

* Merge branch &#39;master&#39; into respect-config-for-search-api-endpoints-#283 ([`a5ce9fa`](https://github.com/ral-facilities/datagateway-api/commit/a5ce9fa4642aaed564cb967557f3771f2f7d1189))


## v2.0.0 (2021-11-22)

### Breaking

* docs: adjust versioning documentation

BREAKING CHANGE: Adding breaking change to correct the version bump which didn&#39;t happen when merging #285 ([`44c48e8`](https://github.com/ral-facilities/datagateway-api/commit/44c48e8b772147bfcf395d1430e067730d66df44))

### Chore

* chore: add pattern to gitignore

- I&#39;ve got a few different config files as I&#39;m switching between the old and new config style, so this change keeps them from Git worrying about them ([`b851f96`](https://github.com/ral-facilities/datagateway-api/commit/b851f969b0e5503d341c6251e7057c1cb7856c0c))

### Style

* style: make `get_query_filter()` less complex #259

- I&#39;ve moved most of the functionality into separate functions, so flake8 doesn&#39;t complain that `get_query_filter()` is too complex ([`c09c982`](https://github.com/ral-facilities/datagateway-api/commit/c09c982977dcb70a8ed8a82a21be607b47cca19c))

* style: add logging to satisfy linter #259 ([`f7d9829`](https://github.com/ral-facilities/datagateway-api/commit/f7d98297c3b100dedffe0e68f3a3c40d65086042))

* style: clean up comments #259 ([`94af185`](https://github.com/ral-facilities/datagateway-api/commit/94af185d4f8cd1bc270e99354f2eb4c3105b29ad))

### Test

* test: unit test api extension validations #256 ([`c068bf3`](https://github.com/ral-facilities/datagateway-api/commit/c068bf3defd9b3b80a898781286dfe9f33c96685))

* test: add remaining test cases for query parameter inputs #259 ([`d211278`](https://github.com/ral-facilities/datagateway-api/commit/d2112786cb96c731557d2a9eea585afea84b3d77))

* test: add test for OR operator on WHERE filter #259 ([`f56465c`](https://github.com/ral-facilities/datagateway-api/commit/f56465c18443afbd8914d6f41cc3243ba03835de))

* test: add boolean operator assertion #259 ([`7b3d039`](https://github.com/ral-facilities/datagateway-api/commit/7b3d039570c9b748cab9c2893078b712f4b7ada1))

### Unknown

* Merge branch &#39;master&#39; into respect-config-for-search-api-endpoints-#283 ([`1ba2b5e`](https://github.com/ral-facilities/datagateway-api/commit/1ba2b5e555f907d43fdc12fafcb61beb176a079c))

* Merge pull request #285 from ral-facilities/add-datagateway-and-panosc-modes-#256

Add DataGateway and PaNOSC Modes ([`5fd00c4`](https://github.com/ral-facilities/datagateway-api/commit/5fd00c4555547482154ddfde1f030048caa7c75c))

* validate api extensions #256 ([`8774537`](https://github.com/ral-facilities/datagateway-api/commit/8774537c7998ffd5769d1648e117b36ecc0748a5))

* Merge branch &#39;master&#39; into add-datagateway-and-panosc-modes-#256 ([`72201a3`](https://github.com/ral-facilities/datagateway-api/commit/72201a30f4a0e0b9bcf12de1d1c3ec709d90b202))

* add support for text operator in query params #259 ([`19ff841`](https://github.com/ral-facilities/datagateway-api/commit/19ff8418d04104abcf92b9ba443b4449fd6c076c))

* add support for WHERE filters coming from count endpoints #259 ([`f9d1e57`](https://github.com/ral-facilities/datagateway-api/commit/f9d1e577848b0302bee570f65e0ed1eb00adbad0))

* add boolean operator to WHERE filter creation #259 ([`6882b9f`](https://github.com/ral-facilities/datagateway-api/commit/6882b9fa4c571ec7d6d20f7183f7c50e08879077))

* Merge branch &#39;master&#39; into feature/query-params-search-api-#259 ([`cab9f3f`](https://github.com/ral-facilities/datagateway-api/commit/cab9f3f4870fbd957c4e912f901e1fc9b897aeca))


## v1.1.0 (2021-11-19)

### Feature

* feat: add first pass of query param implementation #259 ([`ee668e3`](https://github.com/ral-facilities/datagateway-api/commit/ee668e38cd43354851163616a93924ad84e14b90))

### Refactor

* refactor: make use of pydantic in data models #264 ([`54196da`](https://github.com/ral-facilities/datagateway-api/commit/54196da6e6dbe4be81d2307965a75ad354112d0a))

### Style

* style: change import order #257 ([`896d3b8`](https://github.com/ral-facilities/datagateway-api/commit/896d3b8e42f7a05697e15ce52e7998830d5d14c3))

### Test

* test: add some tests for search API query params #259 ([`9a5e02b`](https://github.com/ral-facilities/datagateway-api/commit/9a5e02bbeb5b20d7b16b45e33bc6244cba1543d9))

* test: fix failing tests #283 ([`e69af78`](https://github.com/ral-facilities/datagateway-api/commit/e69af7806cb92bd0be9ca85141c355d9b432bd85))

### Unknown

* Merge pull request #284 from ral-facilities/feature/search-api-endpoint-definition-#257

Define Endpoints for Search API ([`9e137c6`](https://github.com/ral-facilities/datagateway-api/commit/9e137c66953577cd7ab9573c1c7491561809bd60))

* Merge pull request #274 from ral-facilities/expands-search-api-structure

Search API Structure ([`14dfc2a`](https://github.com/ral-facilities/datagateway-api/commit/14dfc2a1f9424ae21e45078a3c2257976268034f))

* Merge branch &#39;expands-search-api-structure&#39; into feature/search-api-endpoint-definition-#257 ([`39f7c4b`](https://github.com/ral-facilities/datagateway-api/commit/39f7c4b2b0c4faaf7e81f81fadd9727b6c09dbbf))

* Merge branch &#39;master&#39; into expands-search-api-structure ([`a2de545`](https://github.com/ral-facilities/datagateway-api/commit/a2de545bfbdf724dc99f9a6d65475c3e36c4bdea))

* add fetch filters to search API endpoints #259 ([`22e8a73`](https://github.com/ral-facilities/datagateway-api/commit/22e8a738385cb77f5cfa2cfff616590cfa571638))

* add boolean operator to WHERE filter #259 ([`12c680f`](https://github.com/ral-facilities/datagateway-api/commit/12c680fdcea546e594e463a26205a743399d0623))

* configure end part of endpoint urls to contain api extension #283

BREAKING CHANGE: modify endpoint urls to use relevant api extension ([`81fa469`](https://github.com/ral-facilities/datagateway-api/commit/81fa46907673d95e954be275acdb7b28b02892ae))

* create api endpoints based on config objects #283 ([`cbdaed6`](https://github.com/ral-facilities/datagateway-api/commit/cbdaed6632c2ffb53ad50c58004608fcfab86f3e))

* Merge branch &#39;feature/search-api-endpoint-definition-#257&#39; into respect-config-for-search-api-endpoints-#283 ([`0b685e8`](https://github.com/ral-facilities/datagateway-api/commit/0b685e85e300f688f6f2e3da41efb3f47e140394))

* Merge branch &#39;expands-search-api-structure&#39; into add-datagateway-and-panosc-modes-#256 ([`c23b0e5`](https://github.com/ral-facilities/datagateway-api/commit/c23b0e5856340e5b2f201643737e45dfb5fedfc2))

* Merge branch &#39;expands-search-api-structure&#39; of github.com:ral-facilities/datagateway-api into expands-search-api-structure ([`dc6dba4`](https://github.com/ral-facilities/datagateway-api/commit/dc6dba4976b1e9d441660332d520f30379331563))


## v1.0.1 (2021-11-15)

### Build

* build: fix poetry.lock issue #256 ([`59eca6e`](https://github.com/ral-facilities/datagateway-api/commit/59eca6e8cb0254731ba8cab5796ba6d9ff4bc993))

* build: add pydantic dependency #256 ([`d7f7bef`](https://github.com/ral-facilities/datagateway-api/commit/d7f7bef4fc2422be6ca1e657fe17478fd11fb45d))

* build: set min python version to 3.6.1 #256 ([`fd4e70c`](https://github.com/ral-facilities/datagateway-api/commit/fd4e70ccd8000c5a9705cf21a8eed503041dd900))

### Ci

* ci: specify Python 3.9.7 to fix issue found with 3.9.8

Details of error encountered can be seen at: https://www.mail-archive.com/debian-bugs-dist@lists.debian.org/msg1829077.html ([`f257c3c`](https://github.com/ral-facilities/datagateway-api/commit/f257c3c314fa9760edb390c60f408e9ec649f2c7))

### Documentation

* docs: add study PID to swagger docs #287 ([`89a9e27`](https://github.com/ral-facilities/datagateway-api/commit/89a9e27b72dfe1d474d49a721f128a643ef2ae36))

### Fix

* fix: add PID field for study in DB backend #287 ([`18379be`](https://github.com/ral-facilities/datagateway-api/commit/18379becafd23ff2957e556de2bd3fc210a71f5b))

* fix: add generation of study.pid #287 ([`f6a8ebc`](https://github.com/ral-facilities/datagateway-api/commit/f6a8ebc6c775ba3f5252d5af5cedc4e1e0e79a40))

### Refactor

* refactor: change imports for new directory structure ([`4be29a5`](https://github.com/ral-facilities/datagateway-api/commit/4be29a578f2a4552c6cc3639193da7af6d6522af))

* refactor: move PID specific Faker instance into relevant generator class #287 ([`4f282dc`](https://github.com/ral-facilities/datagateway-api/commit/4f282dc9f1c6d96f5a14d04dc275681b61b87042))

* refactor: fix typo #256 ([`615f4d5`](https://github.com/ral-facilities/datagateway-api/commit/615f4d53b0c500cae2cb4e444d946d287155e96d))

* refactor: make non-mandatory production config options optional ([`7d68501`](https://github.com/ral-facilities/datagateway-api/commit/7d68501a3c805302fa73df0faa6e10b4f0a85bbe))

* refactor: use pydantic for configuration handling #256 ([`0cca696`](https://github.com/ral-facilities/datagateway-api/commit/0cca696ac8e4cf42385d7a3dbd2deb0191cde52c))

* refactor: make fetching filters from request more generic #259

- The function will now work for DataGateway API and Search API variants ([`600ddf7`](https://github.com/ral-facilities/datagateway-api/commit/600ddf7189edfda936a8bf0f466ef80c6cff4539))

* refactor: add in `SearchAPIQueryFilterFactory` #259

- Added in a generic `QueryFilterFactory` object which inherits from the search API and DataGateway API versions
- Also fixed imports of the DataGateway API specific implementation ([`bbc9412`](https://github.com/ral-facilities/datagateway-api/commit/bbc9412ef0d8e858381da202a753512090abbcf0))

* refactor: make `QueryFilterFactory` return a list of filters #259

- This is in preparation to add a `SearchAPIQueryFilterFactory` where a single query parameter will have multiple filters
- This commit also fixes the tests which impact this change ([`04d92f7`](https://github.com/ral-facilities/datagateway-api/commit/04d92f76001b107fc36452057106a0a13124d517))

* refactor: #257: Add unimplemented endpoint classes

- Matching DataGateway API&#39;s class structure, with relevant TODOs to add in code when endpoints are defined and implemented ([`f2f5edc`](https://github.com/ral-facilities/datagateway-api/commit/f2f5edcbc412d205eafdd9bfe4a0603386063e75))

### Style

* style: reorder import statements to satisfy flake8 ([`c0acd33`](https://github.com/ral-facilities/datagateway-api/commit/c0acd33212e654c7f5fdc42d42915163f0b4ac7b))

### Test

* test: fix failing tests #256 ([`f64a94c`](https://github.com/ral-facilities/datagateway-api/commit/f64a94cd609170d43c29bf078f3fe2c21c0d0e10))

* test: have DataGateway API and search API separated tests ([`4c32759`](https://github.com/ral-facilities/datagateway-api/commit/4c327599e4cb62ba6713a72a7983822dd3e224c7))

* test: unit test config logic #256

The test that was creating a temporary file was failing (even without
the config changes) due to Windows file permission issue. Though a unit
test should run in isolation and should not touch the file system at
all therefore I instead mocked the `builtins.open` to fake `with open`. ([`fab9ce7`](https://github.com/ral-facilities/datagateway-api/commit/fab9ce726075f3df9b35cf4a174127c0ebbaf8f7))

* test: fix failing unit tests #256 ([`ca9d600`](https://github.com/ral-facilities/datagateway-api/commit/ca9d600bad1a5819e1205c49704e1861587aa13b))

### Unknown

* Merge pull request #288 from ral-facilities/bugfix/study-pids-generator-#287

Add Study PIDs to Generator Script ([`a9a6d13`](https://github.com/ral-facilities/datagateway-api/commit/a9a6d134415dd0a70444cfc3fbb8285203fb2ffc))

* change directory structure of API ([`bf35193`](https://github.com/ral-facilities/datagateway-api/commit/bf35193c57d36b7af9df44a9746ad95ab9df9b12))

* use new Faker instance to generate study PIDs #287 ([`cf7c40b`](https://github.com/ral-facilities/datagateway-api/commit/cf7c40bde611337936ebf0773bda60f498b0062a))

* Merge pull request #286 from ral-facilities/ci/use-python-3.9.8

ci: specify Python 3.9.7 to fix issue found with 3.9.8 ([`254249f`](https://github.com/ral-facilities/datagateway-api/commit/254249faa75457580742105b6032b477e8c929f8))

* add configuration option for datagateway and panosc mode #256

BREAKING CHANGE: extend configuration to allow for different API modes ([`be64faf`](https://github.com/ral-facilities/datagateway-api/commit/be64faf9c2bb641d207a2b8a22a03ba68217682c))

* Merge branch &#39;expands-search-api-structure&#39; into add-datagateway-and-panosc-modes-#256 ([`b57c127`](https://github.com/ral-facilities/datagateway-api/commit/b57c127bdc4a6b63c9fcc3a43e627276f2313370))

* Merge branch &#39;expands-search-api-structure&#39; of github.com:ral-facilities/datagateway-api into expands-search-api-structure ([`f51a7b3`](https://github.com/ral-facilities/datagateway-api/commit/f51a7b301200277841b02318f4ee33c16bdda468))

* Merge branch &#39;feature/search-api-endpoint-definition-#257&#39; into feature/query-params-search-api-#259 ([`78ec0fc`](https://github.com/ral-facilities/datagateway-api/commit/78ec0fcbeca0fb43ed16540486b2bbfa0954fe54))

* Merge branch &#39;expands-search-api-structure&#39; into feature/search-api-endpoint-definition-#257 ([`754136a`](https://github.com/ral-facilities/datagateway-api/commit/754136a4408133f541ff36377a37ebea363d5cae))

* Merge branch &#39;expands-search-api-structure&#39; into add-datagateway-and-panosc-modes-#256 ([`fb738dd`](https://github.com/ral-facilities/datagateway-api/commit/fb738dd04dcad730a7020a81957c4574dfebfebf))

* Merge branch &#39;expands-search-api-structure&#39; of github.com:ral-facilities/datagateway-api into expands-search-api-structure ([`01d86fd`](https://github.com/ral-facilities/datagateway-api/commit/01d86fd54950ba99e50bc3abb06fa0164a6abdbb))

* Merge branch &#39;expands-search-api-structure&#39; into feature/search-api-endpoint-definition-#257 ([`8ea6e2d`](https://github.com/ral-facilities/datagateway-api/commit/8ea6e2dec9f3da389415c424f59ed67b1e66d544))

* Merge branch &#39;master&#39; into expands-search-api-structure ([`c87b6cd`](https://github.com/ral-facilities/datagateway-api/commit/c87b6cdf435b5c2254ce8ca46c6187ac3a78cc26))

*  #243: Upgrade Python ICAT version ([`b59abba`](https://github.com/ral-facilities/datagateway-api/commit/b59abba226d8673639403d6cb0f6b2066056b6cc))

*  #243: Add tests for ilike and nilike operators ([`bb8098f`](https://github.com/ral-facilities/datagateway-api/commit/bb8098ff5d89921ebd5eef18a633af344315b584))

*  #243: Add ilike and nilike operators ([`f594790`](https://github.com/ral-facilities/datagateway-api/commit/f5947901721a3b3b38a0611091755cab95f95547))

*  #243: Fix tests for changes in Python ICAT 0.20.0 ([`c4ca364`](https://github.com/ral-facilities/datagateway-api/commit/c4ca364fad1f22da347d63425e577778785aeb29))

* Upgrade Flask-RESTful

- To fix issue described in a Flask RESTful PR: https://github.com/flask-restful/flask-restful/pull/913 ([`c81eda1`](https://github.com/ral-facilities/datagateway-api/commit/c81eda1cb9ef03444494957bc72c09b5b9d16ca5))

* Upgrade version of `werkzeug` via Flask ([`b0d8b4d`](https://github.com/ral-facilities/datagateway-api/commit/b0d8b4dae587e995d282a4ea0571e7fb292dfb2c))

* Add flake8 ignore comments to long imports ([`5431c95`](https://github.com/ral-facilities/datagateway-api/commit/5431c95f4021370c60c2c69d5c81a1eec813818e))

* Fix spacing in PR template ([`bcb84b1`](https://github.com/ral-facilities/datagateway-api/commit/bcb84b1465b2ce887aef54c08f0b837cc5d7faea))

* Use Python 3.9 on CI jobs ([`12a45ba`](https://github.com/ral-facilities/datagateway-api/commit/12a45ba4ce63d5dd3ee468b9fa52e84d15a7b219))

* Fix imports for new directory structure

- Directory structure due to implementation of search API ([`bca8d22`](https://github.com/ral-facilities/datagateway-api/commit/bca8d2294eb459ff5e79bea092dfba0017858e1b))

* Change ignore paths for new directory structure ([`8caccfd`](https://github.com/ral-facilities/datagateway-api/commit/8caccfdaa7161f7105875a59060e7778adecaeaf))

*  #256: Revert back to old example config format

- Reverting back so the tests pass until I re-implement the config ([`f563380`](https://github.com/ral-facilities/datagateway-api/commit/f5633806a50d0cbb09d1498d56a6d5286b10004b))

*  #256: Change directory structure to suit search API

- Since this repository will support DataGateway API and the Search API, there needs to be some changes in directory structure to split the different files up. Essentially this means adding `datagateway_api/` and `search_api/` in `common/` and `src/resources/`
- The imports will be fixed in a future commit ([`b57b92d`](https://github.com/ral-facilities/datagateway-api/commit/b57b92d19155f554c533b526922aa483a8ef9f09))


## v1.0.0 (2021-11-03)

### Breaking

* docs: Add documentation to explain versioning on this repo #242

BREAKING CHANGE: As the API will be approaching production use soon, this seems like a good opportunity to bump the version to 1.0.0. This also serves as a good test that the introduction of automatic versioning actually works ([`ccf6d29`](https://github.com/ral-facilities/datagateway-api/commit/ccf6d2974216f8979a03e3e223f7c9e84ced05cb))

### Build

* build: Add dependency to help with versioning releases #242 ([`1afbd71`](https://github.com/ral-facilities/datagateway-api/commit/1afbd71b169f068b58c14332513ccaa27569e4e8))

* build: Add config for `semantic_release` #242

- Used so the tool can make a release via our CI ([`ceef3be`](https://github.com/ral-facilities/datagateway-api/commit/ceef3bebeb0573b646f44322347e3afede7c617e))

### Ci

* ci: use admin personal access token to automate releases ([`fd76315`](https://github.com/ral-facilities/datagateway-api/commit/fd763154c31ad183a989f807bfbf2926a2de4ae4))

* ci: Add file to create releases and do automatic versioning #242 ([`4358f68`](https://github.com/ral-facilities/datagateway-api/commit/4358f686dbacf9d6e19be913dd8fcd9e66693be9))

* ci: Add config file for `semantic-pull-requests` #242 ([`7223be1`](https://github.com/ral-facilities/datagateway-api/commit/7223be10646d3cd7c9137f37cdfdacf9a431f500))

### Documentation

* docs: rebuild openapi docs #257 ([`de15357`](https://github.com/ral-facilities/datagateway-api/commit/de1535772db64916f75e16d79be3f3fdf10fc47c))

* docs: follow Angular commit message capitalisation #242

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`d53d85a`](https://github.com/ral-facilities/datagateway-api/commit/d53d85ad46a115ba871c6da8273a242e790c810c))

### Feature

* feat: add unimplemented endpoint definitions for search API #257 ([`d0e52d9`](https://github.com/ral-facilities/datagateway-api/commit/d0e52d96dd3b94ce54dcc9b81969e777a196922a))

### Test

* test: add tests for search API endpoints #257 ([`bc1d09d`](https://github.com/ral-facilities/datagateway-api/commit/bc1d09d69aeb2378a7ec65a0f0350de3bb96deb5))

### Unknown

* Merge pull request #282 from ral-facilities/bugfix/releases-permissions

Fix Automated Releases ([`12d3fc9`](https://github.com/ral-facilities/datagateway-api/commit/12d3fc9ba6b9865d8d49864137ffbd7249403c6c))

* Merge pull request #279 from ral-facilities/feature-versioning-#242

Semantic Versioning ([`a24b330`](https://github.com/ral-facilities/datagateway-api/commit/a24b3309cf5c76364c36229894fbab7d718e57d0))

* Merge branch &#39;master&#39; into expands-search-api-structure ([`0e35684`](https://github.com/ral-facilities/datagateway-api/commit/0e356848cf24461482a18fa7fe03cd0d63c5cd85))

* Merge branch &#39;master&#39; into feature-versioning-#242 ([`fe53174`](https://github.com/ral-facilities/datagateway-api/commit/fe53174b18d72629f32c2b76cd0907df6b7c4e9a))

* Merge pull request #273 from ral-facilities/feature/ilike-operator-#243

Add Insensitive Like Operator to WHERE Filter ([`822408b`](https://github.com/ral-facilities/datagateway-api/commit/822408bddcdc992b4404c29ac215309421916fa2))

* add explicit endpoint names to avoid collisions #257

- Collisions were occurring between `/datasets` between DataGateway API and the Search API despite the `/search_api` extension ([`47d3c47`](https://github.com/ral-facilities/datagateway-api/commit/47d3c479ad0788b992f015a23bf025ee21a61d7e))

* change endpoint function names to avoid import collisions #257

- These functions had the same function names as the ones defined for DataGateway API ([`63ba953`](https://github.com/ral-facilities/datagateway-api/commit/63ba95369cee785c518c47e1f961b37533c680eb))

* Merge pull request #275 from ral-facilities/bugfix/default-python-version

Use Python 3.9 on CI jobs ([`06e28dd`](https://github.com/ral-facilities/datagateway-api/commit/06e28ddb9cc426aee154925255f379b8c1116566))

* Merge pull request #278 from ral-facilities/upgrade-werkzeug

Upgrade `werkzeug` for security reasons ([`9ef4f8e`](https://github.com/ral-facilities/datagateway-api/commit/9ef4f8e08ee28c96d5b60cb2b2a73a7f70615de8))

* Merge branch &#39;bugfix/default-python-version&#39; into feature/ilike-operator-#243 ([`550de36`](https://github.com/ral-facilities/datagateway-api/commit/550de3651fe4778427894bb0cb744f597d153e22))

* Upgrade Flask-RESTful

- To fix issue described in a Flask RESTful PR: https://github.com/flask-restful/flask-restful/pull/913 ([`ca14c35`](https://github.com/ral-facilities/datagateway-api/commit/ca14c35ca8eda6e1c89bb9573c14c62d9194e552))

* Upgrade version of `werkzeug` via Flask ([`4ce184f`](https://github.com/ral-facilities/datagateway-api/commit/4ce184fad159f1647142482ef1d97439b6d4c869))

*  #243: Upgrade Python ICAT version ([`39424fa`](https://github.com/ral-facilities/datagateway-api/commit/39424fa05581e934112c9cafd415cc58b22c1a22))

* Add flake8 ignore comments to long imports ([`b60f532`](https://github.com/ral-facilities/datagateway-api/commit/b60f5322c0805fbc22fcb8e94579961c2a67950e))

* Merge branch &#39;bugfix/default-python-version&#39; into expands-search-api-structure ([`0b7c9fd`](https://github.com/ral-facilities/datagateway-api/commit/0b7c9fd8efba77744837c24020322fbce65cd15b))

* Fix imports for new directory structure

- Directory structure due to implementation of search API ([`ea68ce3`](https://github.com/ral-facilities/datagateway-api/commit/ea68ce306a89eaddc4568434a3914e32ac8af57c))

* Change ignore paths for new directory structure ([`ef5973e`](https://github.com/ral-facilities/datagateway-api/commit/ef5973e34aac54d209e030bab0ae1e64e751341b))

*  #256: Revert back to old example config format

- Reverting back so the tests pass until I re-implement the config ([`b99cd4a`](https://github.com/ral-facilities/datagateway-api/commit/b99cd4af8a5128e7040f83718b5fb4ffcd14bc3d))

* Fix spacing in PR template ([`42c29be`](https://github.com/ral-facilities/datagateway-api/commit/42c29bef80ebec2584983603e629584ff21e601f))

* Use Python 3.9 on CI jobs ([`5da8994`](https://github.com/ral-facilities/datagateway-api/commit/5da8994ce4b7aa8ef36617a6bfa7f8d7f6bb5199))

*  #256: Change directory structure to suit search API

- Since this repository will support DataGateway API and the Search API, there needs to be some changes in directory structure to split the different files up. Essentially this means adding `datagateway_api/` and `search_api/` in `common/` and `src/resources/`
- The imports will be fixed in a future commit ([`568af6d`](https://github.com/ral-facilities/datagateway-api/commit/568af6dab2093f87631622a1299a64a95278ece4))

*  #257: Add unimplemented endpoint classes

- Matching DataGateway API&#39;s class structure, with relevant TODOs to add in code when endpoints are defined and implemented ([`4dd84e0`](https://github.com/ral-facilities/datagateway-api/commit/4dd84e06b1add7ee7e6bc08f2817333694f5d005))

*  #258: Set out file for search API session handling

- Unimplemented idea to have a singleton which controls a Python ICAT client with an anon user session ID which will be monitored and refreshed as needed, perhaps using a decorator similar to DataGateway API which checks for a valid session ID at the start of processing an incoming request ([`32a42c9`](https://github.com/ral-facilities/datagateway-api/commit/32a42c9bc876dd1406ad596cf7ca6723989253c3))

*  #260: Add class definitions for search API filters

- This just inherits from the Python ICAT versions for now as they&#39;re unimplemented for the time being ([`5a9aba9`](https://github.com/ral-facilities/datagateway-api/commit/5a9aba9f14eec79d17532dd125e618f8be6167f8))

*  #264, #265: Add unimplemented search API data models

- Comments represent mappings to ICAT data model
- This commit also adds a base class for a search API entity (`PaNOSCAttribute`) which has two abstract methods, which will be used to convert between data models when implemented ([`01b2a25`](https://github.com/ral-facilities/datagateway-api/commit/01b2a25176979ad0a541e0f9653211544a16dfb8))

*  #256: Change example config for search API

- This format of config has not been implemented at time of commit ([`858fcbd`](https://github.com/ral-facilities/datagateway-api/commit/858fcbd5ebe343395aad673b5a6780aaaedcb036))

*  #243: Fix spacing on PR template ([`f8a3a9b`](https://github.com/ral-facilities/datagateway-api/commit/f8a3a9bc56779a8ced661507064d77404077fbb4))

* Merge branch &#39;master&#39; into feature/ilike-operator-#243 ([`f69f136`](https://github.com/ral-facilities/datagateway-api/commit/f69f1361603eaa92b31ac1000e0776a77afd3bec))

* Merge pull request #272 from ral-facilities/icat-ansible-ci-#271

Change ICAT Ansible back to master ([`a426ec7`](https://github.com/ral-facilities/datagateway-api/commit/a426ec73bbb3535d656ee863925f018aac6412bf))

*  #243: Add tests for ilike and nilike operators ([`19c48a5`](https://github.com/ral-facilities/datagateway-api/commit/19c48a560dbd331c370b9f5a4afdfde768eef348))

*  #243: Add ilike and nilike operators ([`e352812`](https://github.com/ral-facilities/datagateway-api/commit/e3528129a5523ec916a07e9a8b875e34cbc559a7))

*  #243: Fix tests for changes in Python ICAT 0.20.0 ([`a6156e3`](https://github.com/ral-facilities/datagateway-api/commit/a6156e3f568d76b35a44a1373b94717eb5865f78))

*  #271: Update version of Poetry used

- Hopefully this will fix the `&#39;Link&#39; object has no attribute &#39;is_absolute&#39;` error seen on GitHub Actions when installing the API&#39;s dependencies ([`0b02151`](https://github.com/ral-facilities/datagateway-api/commit/0b021510e622f2319daeea0ea8211bcf6f839b61))

*  #271: Only run unit tests on matrix version ([`621df10`](https://github.com/ral-facilities/datagateway-api/commit/621df104bafe7397d0a44d8d9757453bb7945252))

*  #271: Change ICAT Ansible back to master ([`a7da072`](https://github.com/ral-facilities/datagateway-api/commit/a7da072ef8adc87fbfa44558a6bfa6f5817354f5))

* Merge pull request #254 from ral-facilities/ubuntu-20-ci-#239

Use Ubuntu 20 on CI ([`4167fbf`](https://github.com/ral-facilities/datagateway-api/commit/4167fbfbe4c436efb43e115b07e062dd239b7548))

*  #239: Correct OS version ([`0439c0d`](https://github.com/ral-facilities/datagateway-api/commit/0439c0d9b9b7ae14394a92433b8677020525689f))

*  #252: Find and replace `master` for default branch change ([`f2f7794`](https://github.com/ral-facilities/datagateway-api/commit/f2f77947f7af7fa3ed55c5f46b3c81072c1396d0))

*  #239: Use ICAT Ansible branch compatible with Ubuntu 20 ([`0d642a9`](https://github.com/ral-facilities/datagateway-api/commit/0d642a9ccb51603a4a1a1dd1300ecd5b837db11c))

*  #239: Change CI to use Ubuntu 20 ([`f3e77c5`](https://github.com/ral-facilities/datagateway-api/commit/f3e77c51a2dbe7464634d02685b8b44e20cabd6f))

* Merge pull request #251 from ral-facilities/increase-test-coverage

Increase Test Coverage ([`87fbbeb`](https://github.com/ral-facilities/datagateway-api/commit/87fbbeb5049bf1035fab1e0c20943cc6a9d3c352))

* Merge pull request #249 from ral-facilities/feature/ping-endpoint-#241

Ping Endpoint ([`f48b471`](https://github.com/ral-facilities/datagateway-api/commit/f48b471b3269b3c85c0897447a920210217df531))

*  #241: Remove print statement ([`c902750`](https://github.com/ral-facilities/datagateway-api/commit/c9027505ec9ebd84923b5aa3bc6c96a82c1a6ae4))

*  #250: Add test class for ICATClient

- Class used to create object pools of Python ICAT&#39;s client class ([`9e0977d`](https://github.com/ral-facilities/datagateway-api/commit/9e0977d534c02dcd7ebbe098c058352574c56558))

*  #250: Add test to mock Python ICAT data update failure ([`01cb60c`](https://github.com/ral-facilities/datagateway-api/commit/01cb60cc0a6152a745eab04b312fa4d07708a35d))

*  #250: Add test to mock invalid backend on query filter getter ([`f6e8ebd`](https://github.com/ral-facilities/datagateway-api/commit/f6e8ebd5d887d12e8b58dfe55ee3226331ea34f5))

*  #250: Add tests for OpenAPI type conversion ([`b946467`](https://github.com/ral-facilities/datagateway-api/commit/b94646723bd1799a55abce1caeee85df3982c112))

*  #250: Add test to mock session with &lt; 0 mins remaining ([`4a3cf7e`](https://github.com/ral-facilities/datagateway-api/commit/4a3cf7ec53f006649b90607b5ceb854eaf25312b))

*  #250: Add test to mock TypeError when setting query limits

- All possible through the use of mocking! ([`e0cb2e0`](https://github.com/ral-facilities/datagateway-api/commit/e0cb2e06817e9a511fa157b8d38b780cd9a9c00c))

*  #241: Add tests for ping endpoint ([`7e89e29`](https://github.com/ral-facilities/datagateway-api/commit/7e89e295bd2a4c48a932fdec03bdc21b04a40fce))

*  #241: Add /ping to generated swagger docs ([`0439247`](https://github.com/ral-facilities/datagateway-api/commit/043924756636e531dfa737beba2e1dc81dd79045))

*  #241: Implement /ping on ICAT backend ([`05fdc70`](https://github.com/ral-facilities/datagateway-api/commit/05fdc70939f7b59f90658b043407b9a8d7c661ea))

*  #241: Implement /ping on DB backend ([`7384a88`](https://github.com/ral-facilities/datagateway-api/commit/7384a881724fd010b41c083f47b28b243698b221))

*  #241: Add non-backend specific infrastructure for /ping ([`1cf4972`](https://github.com/ral-facilities/datagateway-api/commit/1cf4972ac421455dca4d3ef35d42fd81ae8834aa))

*  #241: Remove init from ICAT backend

- This is no longer used (was used for client handling previously before the object-pool-cache design was implemented) ([`0c57614`](https://github.com/ral-facilities/datagateway-api/commit/0c57614f854e0d0402220917364af1f7168ce074))

* Merge pull request #247 from ral-facilities/feature/ci-generator-script-compare

Add CI Generator Script Comparison ([`a393483`](https://github.com/ral-facilities/datagateway-api/commit/a393483897593c3289a5a41531c00717e55bf9c0))

*  #246: Add continue-on-error keyword to generator script CI job ([`d66512a`](https://github.com/ral-facilities/datagateway-api/commit/d66512a1d961c973895874accc25ed0681aaf0c1))

*  #246: Add notes to make potential non-issue failures clear ([`4c41b71`](https://github.com/ral-facilities/datagateway-api/commit/4c41b718e2ffd49c285025ddec21e0d86a84a9a5))

*  #246: Remove debugging ([`4957dd3`](https://github.com/ral-facilities/datagateway-api/commit/4957dd31e38e39de85c2cea6b232d17d4a2b5e9b))

*  #246: Add setup for API&#39;s master version ([`d62e9b7`](https://github.com/ral-facilities/datagateway-api/commit/d62e9b71e253207dc07483f407fdc405f273e152))

*  #246: Add second test to CI generator script job

- This is to compare data from master and the branch where the CI job was started from ([`86eeaeb`](https://github.com/ral-facilities/datagateway-api/commit/86eeaeb2ba16368341e19b814b9760e812e8a75d))

* Merge pull request #245 from ral-facilities/documentation/generator-script-timezones

Add timezone workaround to docs ([`97d74b6`](https://github.com/ral-facilities/datagateway-api/commit/97d74b676bdc7ff1affa2d9a69605456eaa19a99))

*  #244: Add note about inconsistent timezones for generator script ([`1130f4e`](https://github.com/ral-facilities/datagateway-api/commit/1130f4e9f901436384691c2b9f63f07501128c36))

* Merge pull request #240 from ral-facilities/bugfix/join-specs-order-#238

Allow One-Many Related Orderings to not miss out blank results ([`34a8c42`](https://github.com/ral-facilities/datagateway-api/commit/34a8c420b42ca8f0105556043664c7f4b349d75a))

*  #238: Update README with info about generator script ([`33f895f`](https://github.com/ral-facilities/datagateway-api/commit/33f895f0488d494b71e65cead5917aa3bfa640fa))

*  #238: Use default generator args for CI

- This will line up the CI&#39;s data with what I have locally and what is on SciGateway preprod&#39;s icatdb
- This means the failing query test from a commit or two ago will work on CI ([`724acdf`](https://github.com/ral-facilities/datagateway-api/commit/724acdf39a83dd0524b16ce6f8e8535c6d8743a6))

*  #238: Update Python ICAT to 0.19.0 ([`9bb24f3`](https://github.com/ral-facilities/datagateway-api/commit/9bb24f3a015b33e7c55afed604f711d4c9c77e2e))

*  #238: Add test cases for one-to-many related ordering ([`1b17a29`](https://github.com/ral-facilities/datagateway-api/commit/1b17a29925eaf7312a150c82d4232fec4a4709f8))

*  #238: Update comment for accuracy

- 1-many related ordering is now supported as of 0.19.0 of Python ICAT ([`ad3f52d`](https://github.com/ral-facilities/datagateway-api/commit/ad3f52d1ce006c03232ecbd498dfc71cce566f47))

*  #238: Edit expected data on query test

- Not too sure why this is happening, perhaps the generator script fixes? Would&#39;ve thought it would&#39;ve brought this up in the relevant PR though but I&#39;ll monitor this via CI on this branch ([`6cd0d8d`](https://github.com/ral-facilities/datagateway-api/commit/6cd0d8d8cb8b5365297dd2ab67cb5dbb030fc2b6))

*  #238: Implement join specs on queries with one-to-many ordering

- This feature is currently still in PR (therefore unreleased) so I haven&#39;t updated the dependency version, I will do so when Python ICAT is released for 0.19.0 ([`cbef7b9`](https://github.com/ral-facilities/datagateway-api/commit/cbef7b9274a931dd023e034233961fe67c052519))

* Merge pull request #237 from ral-facilities/bugfix/icatdb-generator-data-#236

Make Generator Script Consistent ([`369e38c`](https://github.com/ral-facilities/datagateway-api/commit/369e38c086d712529d7d6fdff9934787bfc09218))

*  #236: Move InvestigationParameter method into its generator class

- No functionality change, just to make this function styled like all the others ([`f211b44`](https://github.com/ral-facilities/datagateway-api/commit/f211b447ed9ffcc21ce3714979e5b9671f621267))

*  #236: Change seeding for Faker ([`28fd5eb`](https://github.com/ral-facilities/datagateway-api/commit/28fd5eb6e8d2928834d754b096768b86f233f292))

*  #236: Update Faker to latest version

- Version kept constant to help the generator script stay consistent over time ([`ede12bf`](https://github.com/ral-facilities/datagateway-api/commit/ede12bf49be374f6655a3339c53dfd0834df153c))

*  #236: Add skip comments option to satisfy diff ([`04c033a`](https://github.com/ral-facilities/datagateway-api/commit/04c033ae56c44085e59a55d0fbd54bfb03efcb5e))

*  #236: Change credentials for mysql commands ([`80afd12`](https://github.com/ral-facilities/datagateway-api/commit/80afd12b1bbd3801e367ca89abc009bfcdecd09f))

*  #236: Choose Python version on new Actions job ([`61d8b7f`](https://github.com/ral-facilities/datagateway-api/commit/61d8b7f6c4e90578c3da79fecef3d4bb044d9ce0))

*  #236: Add job to CI workflow to test generator script ([`c44506d`](https://github.com/ral-facilities/datagateway-api/commit/c44506d6d9746bff5b19163dacd3b2836a38c3da))

*  #236: Use faker to generate foriegn key data ([`7671a7d`](https://github.com/ral-facilities/datagateway-api/commit/7671a7d8acb78f791e7f26464ace2823e4fbb2fc))

*  #236: Use faker to generate non-foreign key integer data

- This appears to give consistent data, unlike `randrange()` ([`327557f`](https://github.com/ral-facilities/datagateway-api/commit/327557ff59de14954c13d1a66cea99118d478d98))

*  #236: Remove multiprocessing pool implementation

- Removing this and just using for loops fixes the inconsistent ordering of data, referred to as IDs being juggled in the original issue ([`556faa0`](https://github.com/ral-facilities/datagateway-api/commit/556faa0c2dcd9a88cbbf09196c3df76f5464cc13))

* Merge pull request #235 from ral-facilities/bugfix/nested-include-filter-inputs-#234

Fix complex include filters ([`d72e473`](https://github.com/ral-facilities/datagateway-api/commit/d72e473754d227212ff8d3f079940bcaadce06df))

*  #234: Fix missing brackets on include filter logic

- `join()` only accepts iterables, not multiple strings
- This commit also adds a test case to cover this ([`2961b18`](https://github.com/ral-facilities/datagateway-api/commit/2961b186dd150a8e0d132b9b243bc4cd49f9389b))

*  #234: Add tests for bugfix ([`b18da3b`](https://github.com/ral-facilities/datagateway-api/commit/b18da3b3504555e5fc839de1045fa3cb902b9112))

*  #234: Fix bug with include filters on ICAT backend ([`58056db`](https://github.com/ral-facilities/datagateway-api/commit/58056db9222f33fbaa6197dcd8750f8226f451eb))

* Merge pull request #233 from ral-facilities/feature/distinct-filter-related-entities-#223

Allow related entities on DB distinct filter ([`205f155`](https://github.com/ral-facilities/datagateway-api/commit/205f1550c90286926b89ecb5df14b1490bc267da))

*  #223: Remove irrelevant docstring ([`da118af`](https://github.com/ral-facilities/datagateway-api/commit/da118af4e7040dba0a3ac457c0cdec12a99a550f))

*  #223: Remove underscore prefixes

- `_get_field()` is the only function in that class that&#39;s used internally, so I&#39;ve remvoed the underscores from the other functions as I&#39;m not sure I&#39;ve used them correctly ([`0a202d3`](https://github.com/ral-facilities/datagateway-api/commit/0a202d3d739aceac0e07e3cc06533753bc9da5ed))

*  #223: Add test cases for the bug fixed in previous commit ([`f16cb15`](https://github.com/ral-facilities/datagateway-api/commit/f16cb15a4360e6fb818db8409508d6f9352127e0))

*  #223: Fix bug with related distinct field with no unrelated fields

- This fix replaces the distinct flag and as a result, that flag has been removed. Quite happy with this fix, much better than what I achieved on Friday ([`9021fc8`](https://github.com/ral-facilities/datagateway-api/commit/9021fc865872586441fe710b29f7cfbd9ca87522))

*  #223: Remove commented code

- This was the best solution I could find, particularly as the two init&#39;s have different method signatures ([`c9aa20b`](https://github.com/ral-facilities/datagateway-api/commit/c9aa20b1f92cb0471ebacc138e2fa601d525d92e))

*  #225: Fix timezone-related issues found by merging master

- These issues were a result of writing new code that involved timezones before master got merged in, which had the original fixes for timezones on DB backend ([`dc583a8`](https://github.com/ral-facilities/datagateway-api/commit/dc583a8155c0e2f20017cf996f6aeded94baedb1))

* Merge branch &#39;master&#39; into feature/distinct-filter-related-entities-#223 ([`bfa8c84`](https://github.com/ral-facilities/datagateway-api/commit/bfa8c84de7bf9d4acf8aa6521e265be976051e72))

*  #223: Add tests for distinct filter with related entities ([`f261f7b`](https://github.com/ral-facilities/datagateway-api/commit/f261f7b893d791b6a312b4251b88c1481c919fd2))

*  #223: Improve assertion on distinct test case ([`2623b18`](https://github.com/ral-facilities/datagateway-api/commit/2623b1838c59cb02faf2d21750182807799b12aa))

*  #223: Fix bug where single related distinct field was given

- This fixes requests such as: `/investigations?distinct=[&#34;investigationtype.createTime&#34;]` ([`0dfa7a3`](https://github.com/ral-facilities/datagateway-api/commit/0dfa7a384fe637bf3427ad40446bff196547d993))

*  #223: Add tests for _get_entity_model_for_filter() ([`3916a56`](https://github.com/ral-facilities/datagateway-api/commit/3916a561ce7af57eac13eaeeec488364bdfbc760))

*  #223: Separate out `_add_query_join()`

- This function used to have two purposes - the returning of the entity model/field has been moved to another function
- Separating out these two jobs means the SQLAlchemy warning has been fixed/no longer appears ([`a2538cc`](https://github.com/ral-facilities/datagateway-api/commit/a2538ccba6810fbd23c6f2c9d1d09ea89ba8498b))

*  #223: Add tests for DatabaseFilterUtilities ([`bc96351`](https://github.com/ral-facilities/datagateway-api/commit/bc9635153bae681e89962fb37d71c14cf16056e7))

* Merge pull request #229 from ral-facilities/bugfix/optional-config-options-#228

Make certain config options optional ([`5901e03`](https://github.com/ral-facilities/datagateway-api/commit/5901e037f713f5541ce091573306bde1044e8606))

*  #223: Fix linting issues ([`4a79940`](https://github.com/ral-facilities/datagateway-api/commit/4a799407b5f43de4a0f4ac1fe533594d649efe95))

*  #223: Move tests for distinct attr mapping ([`d21bd67`](https://github.com/ral-facilities/datagateway-api/commit/d21bd670a1931304c9bb87f3c7b413ac9bf5abe6))

*  #223: Finish detail on docstring ([`d3bda6e`](https://github.com/ral-facilities/datagateway-api/commit/d3bda6ecd60fdebae24c485bc389453d3155ce8f))

*  #223: Allow data from related entities from distinct filters to be nested correctly

- This is using the functions moved to common.helpers in the previous commit ([`dec86b7`](https://github.com/ral-facilities/datagateway-api/commit/dec86b71326248b91843a56f845ec9b268b3527a))

*  #223: Move map distinct attrs to results to common.helpers

- These two functions will now also be used in the DB backend, so should be moved to a more common location ([`e67ee26`](https://github.com/ral-facilities/datagateway-api/commit/e67ee26b4c291ad7fe2feb5285c2c21586f7556b))

* Merge pull request #232 from ral-facilities/refactor/datehandler-db-backend-#225

Add Timezone Data to DB Backend ([`827454b`](https://github.com/ral-facilities/datagateway-api/commit/827454b09b6e22c120f2bcf1dd0bdcffd1bb38d6))

*  #223: Allow related entities to be given in ICAT schema form ([`4bc637a`](https://github.com/ral-facilities/datagateway-api/commit/4bc637a158536246b6c3ce2d4a4f63256edd8a05))

*  #223: Implement DatabaseFilterUtilities into DatabaseWhereFilter

- Similar implemenation as DatabaseDistinctFieldFilter ([`11f75a2`](https://github.com/ral-facilities/datagateway-api/commit/11f75a20a2dba6aac446fbaeb8d61a3f8a436233))

*  #223: Allow DatabaseDistinctFilter to recognise related entity inputs

- This takes existing code from the DatabaseWhereFilter and makes it generic. Future commits will get the WhereFilter to also use this generic version in the same way as the DistinctFilter ([`1b7f132`](https://github.com/ral-facilities/datagateway-api/commit/1b7f1325c433cf0917bdbc8e557468a1f110296e))

* Merge pull request #231 from ral-facilities/update-dependencies-#230

Update dependencies to prevent Poetry warning ([`f8b1136`](https://github.com/ral-facilities/datagateway-api/commit/f8b11365af130b8344affd55cd48ed4b963b0f06))

*  #230: Update dependencies to prevent Poetry warning ([`3ef5f3a`](https://github.com/ral-facilities/datagateway-api/commit/3ef5f3ae0955ffc59346e6c4429d780c1bb5f2f2))

*  #225: Fix tests involving timezone data ([`9b2dc7d`](https://github.com/ral-facilities/datagateway-api/commit/9b2dc7d895a45f3007f7818b455f9e4fe4816247))

*  #225: Add timezone info to session details on ICAT backend ([`26b7bd6`](https://github.com/ral-facilities/datagateway-api/commit/26b7bd651a570bc761de98c1f23e3722a4802455))

*  #225: Add timezone info to datetimes on DB backend ([`f30caa6`](https://github.com/ral-facilities/datagateway-api/commit/f30caa61ad6ccea5cc6ce4ad7f1eb2f732e5d0b2))

*  #228: Make certain config options optional

- Explained in the docstring ([`302042f`](https://github.com/ral-facilities/datagateway-api/commit/302042f557083cc583ba3dd9f161a68e6fa1f086))

* Merge pull request #222 from ral-facilities/refactor/config-backend-specific-#210

Refactor config to be aware of the backend in use ([`0c68549`](https://github.com/ral-facilities/datagateway-api/commit/0c68549a857553f5aa6c934c16356aedf8286ac3))

* Merge branch &#39;master&#39; into refactor/config-backend-specific-#210 ([`5d83b92`](https://github.com/ral-facilities/datagateway-api/commit/5d83b9203be6b873bf350f873a4ae85aba02cf15))

* Merge pull request #216 from ral-facilities/bugfix/client-cache-#209

Improve Client Handling ([`99450bc`](https://github.com/ral-facilities/datagateway-api/commit/99450bca14c029939bd65225889bcffa0893b610))

*  #210: Apply suggested change from PR ([`150f647`](https://github.com/ral-facilities/datagateway-api/commit/150f64794bf45e4ab847241ccd12ee2c795bdf8c))

* #210: Apply suggestions from code review

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`2ffe5a9`](https://github.com/ral-facilities/datagateway-api/commit/2ffe5a9e8c853fbce2f23820c54b004ff30a6365))

* Merge branch &#39;master&#39; into bugfix/client-cache-#209 ([`a643145`](https://github.com/ral-facilities/datagateway-api/commit/a643145b5b4d1d7efe4b2cf203a7414e760663b1))

* Merge pull request #219 from ral-facilities/bugfix/fix-distinct-filter-#141

Fix Distinct Filter on ICAT Backend ([`c3c607f`](https://github.com/ral-facilities/datagateway-api/commit/c3c607f85cfdc273ca858dd8d3578a5f18865653))

* Merge branch &#39;master&#39; into bugfix/fix-distinct-filter-#141 ([`68abaff`](https://github.com/ral-facilities/datagateway-api/commit/68abaff5be990a59bcc2568b3429e74811b8de1b))

*  #210: Fix linting issues ([`d5c536f`](https://github.com/ral-facilities/datagateway-api/commit/d5c536f0c996dbb8ac3bc5ec571c5740d299dea5))

*  #210: Remove client handling config options

- These aren&#39;t in the current branch, they&#39;ll need to be added back when the client handling PR gets merged in ([`01ab8e1`](https://github.com/ral-facilities/datagateway-api/commit/01ab8e13dd7f222e42a1cf7536bc54c3e428d7d7))

*  #210: Add leading underscore to instance variables ([`1cb1003`](https://github.com/ral-facilities/datagateway-api/commit/1cb1003a1459700cac5d5b9640f4661e6912b0b8))

*  #210: Update test_config.py to reflect refactor ([`5f2b33e`](https://github.com/ral-facilities/datagateway-api/commit/5f2b33e77d6ef9dbc2c8d0995150de14c6767c76))

*  #210: Implement config enum class ([`76bcb7d`](https://github.com/ral-facilities/datagateway-api/commit/76bcb7d783b8c8f52978a044863e764e63111b2b))

*  #210: Add enum class for config options

- Similar to what now happens in SciGateway Auth ([`171dbdf`](https://github.com/ral-facilities/datagateway-api/commit/171dbdfee702e8760bd4e130c0738a29675b8618))

*  #210: Add function to check existence of config options ([`cab681b`](https://github.com/ral-facilities/datagateway-api/commit/cab681b5e663bcd214aa4f386c45928f8e9a5390))

*  #210: Replace old config getters with calls to generic

- This commit also removes the old getters, as they&#39;re no longer being used ([`9ad2f57`](https://github.com/ral-facilities/datagateway-api/commit/9ad2f574ff461e66a59ad0ea2b072d71bf78533b))

*  #210: Make all config keys use same casing ([`c1a02e5`](https://github.com/ral-facilities/datagateway-api/commit/c1a02e5e0aac93906bf4589a17b51657d59c7163))

*  #210: Add generic config getter

- Following how SciGateway Auth does this, should reduce code in this file ([`3c40ccb`](https://github.com/ral-facilities/datagateway-api/commit/3c40ccb546f0434d82366d9a521ac625e6020220))

*  #210: Remove config calls from being added as a constant

- No real reason for this to happen, once the JSON is loaded, the values aren&#39;t changed until API restart and not modified elsewhere currently
- It&#39;s probably a good thing the request behind ICAT_PROPERTIES actually gets called on demand in case the values get changed before the API is restarted
- Ultimately, this is the cause of the issue (requiring DB_URL despite using ICAT backend) ([`79d00e8`](https://github.com/ral-facilities/datagateway-api/commit/79d00e8b61509f5dc92b008057d9b3bb91ead3b2))

* Merge pull request #221 from ral-facilities/bugfix/fix-ci-#220

Fix Broken CI ([`5d99cd3`](https://github.com/ral-facilities/datagateway-api/commit/5d99cd3de27ef8fcb7b425df45aed8fee77e7ab3))

*  #220: Force hostname to localhost ([`ab09e13`](https://github.com/ral-facilities/datagateway-api/commit/ab09e13d33af5218b485e77fbb8095ae5b658a3f))

*  #141: Update Python ICAT to 0.18.1 ([`fdd04b0`](https://github.com/ral-facilities/datagateway-api/commit/fdd04b0683d0a32e5ea04b58ca24d8e355301c66))

*  #141: Change data structures to match behaviour of Python ICAT 0.18.1 ([`c7789bd`](https://github.com/ral-facilities/datagateway-api/commit/c7789bd5e64f6f0c8b458915089160f27a5043f5))

*  #141: Fix linting issues ([`891f520`](https://github.com/ral-facilities/datagateway-api/commit/891f520499dc72b5dd452dc0255333cc70965c18))

*  #141: Remove previous implementation for distinct fields ([`677424d`](https://github.com/ral-facilities/datagateway-api/commit/677424d8bdf80d65ea6d8ce425f33fde995ee96d))

*  #141: Fix issue with count test cases ([`4057126`](https://github.com/ral-facilities/datagateway-api/commit/4057126e251937d3a215beab738efe9c8baac1fe))

*  #141: Fix bug when a count endpoint with distinct filter should get 0 results but caused an IndexError

- Test case to cover this edge case also added in this commit ([`44b707a`](https://github.com/ral-facilities/datagateway-api/commit/44b707a73a415901b30fa8205f780d8c40b06577))

*  #141: Add test cases for query exeuction ([`1b7cb60`](https://github.com/ral-facilities/datagateway-api/commit/1b7cb6093ddbaa669728dda5e015732a51e58718))

*  #141: Fix GET requests w/ distinct filters ([`8504fd1`](https://github.com/ral-facilities/datagateway-api/commit/8504fd15278fd4f001aa8597a6ce4be5fa69294e))

*  #141: Add flag to mark ISIS endpoints

- This flag is needed to distinguish ISIS endpoints (that use DISTINCT, but don&#39;t select multiple fields) from queries that use a distinct filter (DISTINCT and select multiple fields) ([`504e94f`](https://github.com/ral-facilities/datagateway-api/commit/504e94feef9a608796197e1ae2ac9b67019ec843))

*  #141: Add test cases for distinct attribute mapping ([`ede08f2`](https://github.com/ral-facilities/datagateway-api/commit/ede08f2050dce3e8f1637b0d35a96285085ebbf2))

*  #141: Make distinct requests work with related entities ([`3401027`](https://github.com/ral-facilities/datagateway-api/commit/340102739ca3ec7b54f13ef025af1543dad24833))

*  #141: Add tests for new functions in query.py ([`916e3d1`](https://github.com/ral-facilities/datagateway-api/commit/916e3d1da4e9884f7072c5c253e3c3d0ba65484e))

* Merge pull request #218 from ral-facilities/refactor/increase-test-coverage

Increase Test Coverage ([`1b7944c`](https://github.com/ral-facilities/datagateway-api/commit/1b7944c30df352b0e52c6f9be3cb92c7641b006c))

*  #141: Edit test data to make sense

- Behaviour of 404s was changed, but the test data wasn&#39;t, so it could be confusing why test data saying a 404 should occur then isn&#39;t tested that happens (which it shouldn&#39;t now) ([`552f743`](https://github.com/ral-facilities/datagateway-api/commit/552f7431941e7a328b7bbb9190ef2518c077e709))

*  #141: Add test case for distinct filter on count endpoint ([`1d63692`](https://github.com/ral-facilities/datagateway-api/commit/1d63692ac65d3461e956eccc0d88155ee90c1241))

*  #141: Remove unused functions ([`0322a99`](https://github.com/ral-facilities/datagateway-api/commit/0322a99c4738a356cbec89f65eaccf5a89c918fc))

*  #141: Extend test cases for ICATQuery init ([`9a6d7bc`](https://github.com/ral-facilities/datagateway-api/commit/9a6d7bcf893486f0c6f1a61633ce33dd86449425))

*  #141: Remove irrelevant ICATQuery test ([`63c4506`](https://github.com/ral-facilities/datagateway-api/commit/63c4506989031936794d070f71228ae718d3cd3e))

*  #141: Fix tests for ICAT distinct filter

- Also adds a test for manual_count ([`9d14566`](https://github.com/ral-facilities/datagateway-api/commit/9d1456631d485a28957c3aba08e557d66007decb))

*  #141: Remove checks for related entities on a distinct filter

- Python ICAT is smart enough to add JOINs to the JPQL queries in the situation where a related entity is used in a distinct filter ([`1530ca6`](https://github.com/ral-facilities/datagateway-api/commit/1530ca69b3f892349eeb2ba4ed9df94cce441d34))

*  #141: Fix manual count flag ([`f5c3bbe`](https://github.com/ral-facilities/datagateway-api/commit/f5c3bbef2c7f1ea11845e95906d11d7627e22d15))

*  #141: Change function to fetch distinct attributes

- I haven&#39;t deleted the original function yet, but it&#39;s very likely I will at the end of this work as there are no other calls to that function ([`42dea33`](https://github.com/ral-facilities/datagateway-api/commit/42dea337c95215e41f7e94f4561e0db2a12b0983))

*  #141: Add manual_count flag

- Flag used for a count request that has a distinct filter ([`abb31bd`](https://github.com/ral-facilities/datagateway-api/commit/abb31bd0c36a809146484a78c8c6d9864fdf561a))

*  #141: Add function to map distinct attrs to results ([`5f11db2`](https://github.com/ral-facilities/datagateway-api/commit/5f11db28ea4a470142378ed78c9f3dce84726bc2))

* Merge pull request #215 from ral-facilities/bugfix/configurable-reloader-#214

Make Flask Reloader Configurable ([`7626a92`](https://github.com/ral-facilities/datagateway-api/commit/7626a92bf11da9e5927e9b851557a941cbdeded7))

*  #217: Fix linting issue ([`e6aee90`](https://github.com/ral-facilities/datagateway-api/commit/e6aee902f2a1ec437f150804bc2a8415011634c3))

*  #217: Add tests for rollback functionality on update and create endpoints ([`63b3537`](https://github.com/ral-facilities/datagateway-api/commit/63b3537df9409705d1a95adf29176671888698dd))

*  #217: Add test case for invalid backend name ([`af49cd1`](https://github.com/ral-facilities/datagateway-api/commit/af49cd181546759aa1e5b58111387327c4718129))

*  #217: Add tests for custom API exceptions ([`0aec6da`](https://github.com/ral-facilities/datagateway-api/commit/0aec6da8af043c981f68676c40b585a03455db63))

*  #217: Add tests for camelCase ICAT entity name function ([`285362a`](https://github.com/ral-facilities/datagateway-api/commit/285362ae539c3ee24752bb3521c698e18c88ec69))

*  #217: Add tests for get_entity_object_from_name() ([`b9fc454`](https://github.com/ral-facilities/datagateway-api/commit/b9fc4548b714461e8e7f72c708652bbd932dfc6a))

*  #217: Update a date attribute on update by ID endpoint ([`550bd41`](https://github.com/ral-facilities/datagateway-api/commit/550bd41b6560c4efc81b131c70cc0dd1294f943a))

*  #217: Add test case for empty list where filter ([`7e723be`](https://github.com/ral-facilities/datagateway-api/commit/7e723be753d263d9b9ed0840a618e6cd3bc0ee4d))

*  #217: Add tests for QueryFilter abstract class

- Similar testing principle to testing the abstract backend class ([`fb57cee`](https://github.com/ral-facilities/datagateway-api/commit/fb57cee963fecdd7829ff185a06addc2825bbb9d))

*  #217: Correct config test function call ([`20e4b68`](https://github.com/ral-facilities/datagateway-api/commit/20e4b688ed0d9871dc48df7774d17fbb2bb794ec))

*  #217: Improve comments ([`6eedca5`](https://github.com/ral-facilities/datagateway-api/commit/6eedca5251d8458089e099cd6f6880ae035547a9))

* Add heading to contents ([`85e52f0`](https://github.com/ral-facilities/datagateway-api/commit/85e52f05eeb439d39ddbd75c41418f5ef8c4bac4))

*  #141: Make use of setAttributes() for distinct filter

- Also moved the log.debug() to the start of the function. When it was at the end, it would not be logged out if there was an exception, the situation where you want that debug statement ([`e3169e1`](https://github.com/ral-facilities/datagateway-api/commit/e3169e107e8eea053b798a6a475ee467cc67ad12))

*  #141: Update python-icat

- The new version specified contains the changes for setAttributes() ([`c0f5fde`](https://github.com/ral-facilities/datagateway-api/commit/c0f5fded6dcb400e99cc04d12a6b3cb1de60381a))

*  #214: Add documentation for configurable flask reloader

- I&#39;ve mentioned the new solution for client handling which isn&#39;t currently in this branch, but when those changes are merged, the documentation will make full sense ([`1ed467d`](https://github.com/ral-facilities/datagateway-api/commit/1ed467deb1033c77b9a08488e758a5bb10c4e4ec))

*  #214: Add config option for code reloading ([`089ace3`](https://github.com/ral-facilities/datagateway-api/commit/089ace3667c7907d0c4aeeae7557bed985b992ca))

*  #209: Remove irrelevant TODO ([`4ed8061`](https://github.com/ral-facilities/datagateway-api/commit/4ed8061affba0cb1727bc2cbbd32ecb850d5a587))

*  #209: Fix LRU cache test ([`c6e34e8`](https://github.com/ral-facilities/datagateway-api/commit/c6e34e8e20dc0f007fbd5db52d6a1ba1b559881a))

*  #209: Increase test coverage for extended cache ([`bdc72fb`](https://github.com/ral-facilities/datagateway-api/commit/bdc72fbae49ef9f2622c0433444de54c8099367a))

*  #209: Add tests for custom LRU cache ([`cad5677`](https://github.com/ral-facilities/datagateway-api/commit/cad5677a650b2bc6d282c9ff25cf54b510963f72))

*  #209: Remove create client function

- Client creation is handled by `ICATClient` ([`6acfd48`](https://github.com/ral-facilities/datagateway-api/commit/6acfd482c208c15ac8de94c08c9c327a4606bc93))

*  #209: Remove executor

- This was never used and won&#39;t be needed for the solution to client handling ([`1a1064c`](https://github.com/ral-facilities/datagateway-api/commit/1a1064cd361c4bfb8c25e355f6cfe4c119967166))

*  #209: Remove client defensiveness

- This is no longer needed due to the new solution for client handling ([`a9600e9`](https://github.com/ral-facilities/datagateway-api/commit/a9600e945a8764c9a27fb7ff68e2aa20fdd52e01))

*  #209: Fix linting issues ([`7a885d2`](https://github.com/ral-facilities/datagateway-api/commit/7a885d20b84846361f9f3f9493013684aba65d51))

* Merge branch &#39;master&#39; into bugfix/client-cache-#209 ([`904ded8`](https://github.com/ral-facilities/datagateway-api/commit/904ded8b1dfa81f75e563f4a7707580fd8b2e948))

*  #209: Add documentation for client handling ([`400b6b5`](https://github.com/ral-facilities/datagateway-api/commit/400b6b5070ae361f94fe8b5d3a1ebabfa66f3a4f))

*  #209: Flush session ID before putting client back into pool ([`e0fff60`](https://github.com/ral-facilities/datagateway-api/commit/e0fff60d0f7fb0bcd5b401e114dba42117161295))

*  #209: Fix API on DB backend

- The client pool design wasn&#39;t working on DB backend, but now it does ([`b0350c9`](https://github.com/ral-facilities/datagateway-api/commit/b0350c9afc99d7b2c73ab36d7c1ef9a7991aab89))

*  #209: Change &#39;max capacity&#39; to &#39;max size&#39;

- This change should just help make things a bit clearer due to &#39;init size&#39;, make the terminology more similar ([`33bdcd1`](https://github.com/ral-facilities/datagateway-api/commit/33bdcd11f617f1d1fbe10d696bedb7ebce4773b5))

*  #209: Make client handling values configurable ([`e4abe88`](https://github.com/ral-facilities/datagateway-api/commit/e4abe888a2330ed619567880f46dac5649c15456))

*  #209: Add comments and move code to a more logical location ([`416288c`](https://github.com/ral-facilities/datagateway-api/commit/416288cb8bfbc8809207baa329d7b23d2389e3ee))

* Merge pull request #205 from ral-facilities/feature/camel-case-db-backend-#119

Make DB Backend use camelCase ([`0601fb2`](https://github.com/ral-facilities/datagateway-api/commit/0601fb28094a8d5cd919394a9ca9fd7f6f1138dd))

*  #119: Implement client object pool using LRU cache to hold &#39;in use&#39; clients

- LRU cache allows recently used client objects to be kept around. This means there&#39;s a 1 client object to 1 session ID ratio, more resource sensitive than a 1 client object for every request ratio
- Workflow: client pool is created at startup, incoming request fetches client from LRU cache, which pulls a client from the pool. Client is kept in the cache until it becomes least recently used, at which point it&#39;s then put back into the pool
- POST to /sessions uses the same workflow, passing a (pretend) session ID of None to get the same client from the cache each time
- The first time a new session ID is passed in the request headers, there is no slowdown in the request like before (where a client was being created for that ID). The client is fetched from the pool
- I&#39;ve ran this commit against some e2e tests on the frontend and the performance from the API was good, similar to the branch which uses a single client object, passed around using kwargs. I have no concerns regarding a &#39;slow API&#39; with the pool and cache
- This is just a rough proof of concept, there&#39;s lots of cleaning up to do, including making the resource stats on the pool accurate and not just passing the default ones each time. One potential solution is to make something similar to the `Executor` class in the pool library. I experiemented with this (think the class I mocked up is in this commit?) but I wanted to get a basic example working before worrying about the stats (which the API doesn&#39;t make use of, but it might be useful to keep accurate stats if they ever need to be logged out. All part of the cleanup process
- This doesn&#39;t use the context manager as this wouldn&#39;t allow me to implement the LRU cache in the way I have ([`74f1edd`](https://github.com/ral-facilities/datagateway-api/commit/74f1edd78b56b10618ec1c57f8016eb6b5073ad7))

*  #119: Add comments to related entity logic ([`a0c966e`](https://github.com/ral-facilities/datagateway-api/commit/a0c966ef7614874277b511dc8005b341b9e16c41))

* Merge pull request #212 from ral-facilities/bugfix/include-distinct-requests-#211

Bugfix/include distinct requests #211 ([`671b33d`](https://github.com/ral-facilities/datagateway-api/commit/671b33da75ff164a8a0c05dc5341293ea2154844))

*  #211: Increase test coverage for POST /sessions

- Unrelated to the issue tagged in the commit, but after my previous commit I noticed this would be an easy win for test coverage percentages so quickly modified the tests to get the increased test coverage ([`02778a2`](https://github.com/ral-facilities/datagateway-api/commit/02778a2356ff0fe8df3deac75b661b04dff97ad0))

* Merge branch &#39;master&#39; into feature/camel-case-db-backend-#119 ([`ae63c89`](https://github.com/ral-facilities/datagateway-api/commit/ae63c8906e221d18a4fa7030538007b6ffb7375b))

*  #211: Update dependencies as identified by safety ([`622eebb`](https://github.com/ral-facilities/datagateway-api/commit/622eebb6ac8009154dd957d4919854cfe3eefaaf))

*  #211: Add unit tests for distinct attribute mapping

- This should give a nice increase in test coverage, hopefully codecov agrees! ([`d3980e2`](https://github.com/ral-facilities/datagateway-api/commit/d3980e2774cc753a4a3959f64d4b9b47c4562b8d))

*  #211: Fix bug with nested-included distinct attributes

- Also expands the unit test now those nested input values are possible to occur in the API ([`8b31f5d`](https://github.com/ral-facilities/datagateway-api/commit/8b31f5d6a0e431631cbd9af1d07b4941f468e0b3))

*  #211: Fix distinct/include bug and add test for it ([`623a494`](https://github.com/ral-facilities/datagateway-api/commit/623a494e06976ca7c5ef9cc30b6cc6cd3c49a538))

*  #209: Add client cache size as a configurable option ([`fb20095`](https://github.com/ral-facilities/datagateway-api/commit/fb2009590a028f3f31deb9f4337b51775fc5b143))

*  #209: Make login() use client cache

- Extra attention should be paid to the flushing of session ID on the client object to previous users being logged out the next time backend.login() is called ([`3c202a8`](https://github.com/ral-facilities/datagateway-api/commit/3c202a87ba83958c7f04b272a9792285e482ed19))

*  #209: Add infomration of how credentials should be structured in request body of POST /sessions ([`10fceff`](https://github.com/ral-facilities/datagateway-api/commit/10fceff7fa96647a95b98497334a030fbb859ece))

*  #209: Change ICATSessionError exception to output exception message

- When running the API, it was difficult to distinguish between the AuthenticationError affected in this commit, and the one a couple of lines above it ([`a81c145`](https://github.com/ral-facilities/datagateway-api/commit/a81c1455db8186a5a559f7d0b40300723b870649))

*  #209: Add client caching function

- This uses an LRU caching algorithm to determine which client objects should remain cached when the cache is full ([`d1559a6`](https://github.com/ral-facilities/datagateway-api/commit/d1559a6ed1988fb07a75355edf6b45511050c799))

* Merge pull request #207 from ral-facilities/feature/wsgi

Add WSGI script and fix errors with pip install ([`04eafd5`](https://github.com/ral-facilities/datagateway-api/commit/04eafd5afd8051bbf0b591f913c35cf455db45c1))

* Don&#39;t write to openapi.yaml when generate_swagger set to false ([`611c227`](https://github.com/ral-facilities/datagateway-api/commit/611c227879bd149a4976dcb1a5c3440098b0b9d1))

* Add missing python-dateutil dependency ([`1572c0c`](https://github.com/ral-facilities/datagateway-api/commit/1572c0cf9a118cbffc26b6006fdff28e148afda9))

*  #119: Fix tests for change to no results behaviour

- A couple of commits ago, the ICAT backend was changed so that 404s no longer occur when no results are found. This is because no results being found is correct behaviour, so should give a 200 ([`268dac3`](https://github.com/ral-facilities/datagateway-api/commit/268dac3b2e90b5caa0fce66fb470eac96b63d565))

*  #119: Make icatdb generator script use camelCase foreign keys ([`1ee7961`](https://github.com/ral-facilities/datagateway-api/commit/1ee79619f0a97cf4dc9c72a8f0979c44bceca750))

*  #119: Fix linting issues ([`47e430d`](https://github.com/ral-facilities/datagateway-api/commit/47e430dc2e882be6599389b1683ed299416135e3))

*  #119: Fix tests for entities referencing foreign keys ([`7912f96`](https://github.com/ral-facilities/datagateway-api/commit/7912f9628cf7eebfbca3a01439fdf70c8d88a052))

*  #119: Change foreign keys to use camelCase ([`85b76b6`](https://github.com/ral-facilities/datagateway-api/commit/85b76b6c7da691cd9059f304554d0d59104b93a5))

*  #119: Remove irrelevant 404s when no data is found ([`c1fc105`](https://github.com/ral-facilities/datagateway-api/commit/c1fc105446aebcd9b393ec9d2135fe6fad49f791))

*  #119: Add NULL to an empty list when using the in operator of a where filter

- This will allow the ICAT backend to return a 200 when something like the following is sent as a where filter - `{&#34;id&#34;: {&#34;in&#34;: []}}` ([`6662f86`](https://github.com/ral-facilities/datagateway-api/commit/6662f86bff60397140d77d996b95ae981bc5073b))

* Merge branch &#39;master&#39; into feature/wsgi

Conflicts:
	poetry.lock
	pyproject.toml ([`521a1ab`](https://github.com/ral-facilities/datagateway-api/commit/521a1abc54922eb78fd2606be35081a977b2d78c))

* Merge pull request #204 from ral-facilities/bugfix/improve-db-sessions

Bugfix/improve db sessions ([`856c31e`](https://github.com/ral-facilities/datagateway-api/commit/856c31e861093060ef4e80765f3c477ca58357f9))

* Ignore linter errors in wsgi.py ([`8f3ffc6`](https://github.com/ral-facilities/datagateway-api/commit/8f3ffc696e18b3cec655475b36051071dc4d1bd9))

* Add trailing comma to appease linter ([`2b87c76`](https://github.com/ral-facilities/datagateway-api/commit/2b87c760f98cbe85f0afc3da6fc73d5f0538eb0c))

* Add requests as a dependency ([`668d0e9`](https://github.com/ral-facilities/datagateway-api/commit/668d0e9fe26d0ba21444c1c932d92b143191ec73))

* Add wsgi.py ([`8afe25a`](https://github.com/ral-facilities/datagateway-api/commit/8afe25a1337185ca6f00f8f41507bdd2716afb76))

* Move config.json to datagateway_api directory ([`6b8e1e9`](https://github.com/ral-facilities/datagateway-api/commit/6b8e1e94fafa6d850598cd52d1353cb92302c7f4))

* Merge pull request #206 from ral-facilities/bugfix/codecov-path-fixing

Fix 404s on Codecov File Views ([`339174f`](https://github.com/ral-facilities/datagateway-api/commit/339174fc48b6d9c88ff048f0fee156b84c011156))

*  #119: Change attribute names to camelCase ([`6377ad5`](https://github.com/ral-facilities/datagateway-api/commit/6377ad5ea7d149fc5d0f24360dfad0b229ce3020))

* Use old session management for icat_db_generator script ([`9e8bed2`](https://github.com/ral-facilities/datagateway-api/commit/9e8bed2e17c86f4934eb7680aa00e036b422ef88))

* Fix tests by manually pushing app context ([`582817a`](https://github.com/ral-facilities/datagateway-api/commit/582817aae28e72ec278f161216a65a6c1c24836a))

* Fix SQLALCHEMY_TRACK_MODIFICATIONS warning ([`825c2dd`](https://github.com/ral-facilities/datagateway-api/commit/825c2dd37a476e3498d9e66b2f4f3e38aa0f028b))

* Fix import typo ([`5f1c2b2`](https://github.com/ral-facilities/datagateway-api/commit/5f1c2b2d0335c24896ff6659a9041099c2aa0809))

* Fix styling issues ([`9d3ddc6`](https://github.com/ral-facilities/datagateway-api/commit/9d3ddc6419ffc20640f2cb2d68338285f5312a25))

* Move session init code to more sensible places ([`38dc28e`](https://github.com/ral-facilities/datagateway-api/commit/38dc28e445c78e36a1bd2b1e701a6cd2a1360eaa))

* Merge branch &#39;master&#39; into bugfix/improve-db-sessions

Conflicts:
	datagateway_api/src/main.py
	poetry.lock ([`5f9c318`](https://github.com/ral-facilities/datagateway-api/commit/5f9c31898199c763d1cf13c4b97e1289713ee7ba))

*  #203: Apply path fixing solution to other workflow jobs

- This commit has no effect on codecov path fixing, but it makes the entire workflow consistent in how the API is cloned onto the Actions runner ([`f6a4853`](https://github.com/ral-facilities/datagateway-api/commit/f6a48531d2d53db8570a34141e1383cd50bee886))

*  #203: Stop API being cloned into a separate directory

- This should help fix path issues with codecov ([`1d64040`](https://github.com/ral-facilities/datagateway-api/commit/1d6404038acfde129adacf0f9c63d5c6f43894d7))

*  #203: Test codecov path fixing ([`f3498a8`](https://github.com/ral-facilities/datagateway-api/commit/f3498a8dd32e6fb54116060c96046664ec27491a))

*  #119: Fix OpenAPI docs for related entities ([`346731c`](https://github.com/ral-facilities/datagateway-api/commit/346731c80d9f01e33d173d934ecd3544964e4968))

*  #119: Fix entity_helper tests ([`fc73642`](https://github.com/ral-facilities/datagateway-api/commit/fc736424293ef6f1256dab5dc131a98629cb31c7))

*  #119: Fix ISIS endpoints on DB backend

- They became broken due to the change to camelCase within the backend ([`3393f58`](https://github.com/ral-facilities/datagateway-api/commit/3393f58818c97cec10dddbcb13243114367c2e93))

*  #119: Set response body keys based on field name rather than table name

- This change also allows related entities to be retrieved on with plural field name
- Related entities with a singular field name also typically have a foreign key attribute in the class. When an include filter is used in this situation, the included entity will be returned in the response body, rather than the foreign key. This had a better outcome than I thought it would&#39;ve done :) ([`ce5e763`](https://github.com/ral-facilities/datagateway-api/commit/ce5e7632a3c0bb41476ba5c5bf3f23ddd2324028))

*  #119: Allow relationships to be accessed from camelCase input

- The addition of __singularfieldname__ and __pluralfieldname__ will be used in the following commit, where these will be used to set JSON response body keys (so they&#39;re camelCase, not SNAKE_CASE) ([`b9e52d9`](https://github.com/ral-facilities/datagateway-api/commit/b9e52d91120624729d08ecc74c51e80132453e30))

*  #119: Allow entity objects to be fetched from plural field names

- This feature will be needed when there&#39;s camelCase field names for related entities, e.g. for user input on include filters
- This change also moves the location of get_entity_object_from_name() to prevent any issues with circular imports. Since the function no longer makes use of globals(), there&#39;s no requirement for the function to be in models.py ([`f543007`](https://github.com/ral-facilities/datagateway-api/commit/f543007246fcdc040aaa048d84ba4d8c10ab85e0))

*  #119: Move endpoints dict to a separate file

- This change is to prevent a circular import when get_entity_object_from_name is modified
- Also removes a TODO comment that has previously addressed - it was regarding camelCasing of modId etc. ([`5b6f055`](https://github.com/ral-facilities/datagateway-api/commit/5b6f0550d0b5a87c6d61da15df8dc56ca08b0123))

*  #119: Ensure rotated log files are ignored by git ([`170baa4`](https://github.com/ral-facilities/datagateway-api/commit/170baa44f874226e86f0176d7bc94fbfbcf14ca1))

*  #119: Fix foreign keys not being added to dictionary conversions

- The edits to test data return the tests back to how they should be, where they were edited to test what was going on ([`42739e4`](https://github.com/ral-facilities/datagateway-api/commit/42739e47588ae8caa4e3fc2dead3ae31ec721c68))

*  #119: Correct return class in docstring ([`1f05f6c`](https://github.com/ral-facilities/datagateway-api/commit/1f05f6ce5dff708483d36846ccf06d513b26a13c))

*  #119: Fix OpenAPI YAML to use camelCase attribute names ([`3c086a6`](https://github.com/ral-facilities/datagateway-api/commit/3c086a6bc14a08ae93403ae262e8015960796ada))

* Merge pull request #202 from ral-facilities/bugfix/fix-teardown-icat-create-tests-#201

Add teardown for POST entity endpoint tests ([`460b680`](https://github.com/ral-facilities/datagateway-api/commit/460b6807b51b1d4a68e6ad7b990ef5514040ec35))

*  #119: Add flake8 file ignore due to DB backend camelCase attribute names ([`edba864`](https://github.com/ral-facilities/datagateway-api/commit/edba864c1f02f169007c8b5e661571f70cec684f))

*  #119: Add missing trailing commas ([`382de45`](https://github.com/ral-facilities/datagateway-api/commit/382de454295c0d87912722fc6d4546d9332e4a06))

*  #119: Edit entity conversion to work with most camelCase attribute names

- This doesn&#39;t work with foreign key attribute keys yet - e.g. &#34;DATACOLLECTION_ID&#34; will be changed to &#34;datacollectionid&#34; and this doesn&#39;t match the variable names in the entities ([`0d0c5d0`](https://github.com/ral-facilities/datagateway-api/commit/0d0c5d0c7843bd74ab0cf85dd07f4b8a76d51d21))

*  #119: Edit DB backend tests to use camelCase

- Most DB tests pass now, but a decision needs to be made regarding foreign keys to allow the tests in test_entity_helper.py to pass ([`279681a`](https://github.com/ral-facilities/datagateway-api/commit/279681a93393d756990fc9ad8b69a27d58fb941f))

*  #119: Change attribute name usage to camelCase ([`58ae900`](https://github.com/ral-facilities/datagateway-api/commit/58ae9006544f54fccd2a1fcaa9f17336b0ccfb25))

*  #119: Edit attribute names to be camelCase ([`28cfc72`](https://github.com/ral-facilities/datagateway-api/commit/28cfc724abe19136e429db99825f52ed3bd2a052))

*  #201: Add teardown for POST entity endpoint tests

- This replaces the data deletion loop that was after the assert statement, which wouldn&#39;t run if the an AssertionError was raised, resulting in undeleted test data ([`71a65b3`](https://github.com/ral-facilities/datagateway-api/commit/71a65b3d06bd727a5d0e3d613daa610f6f2d730b))

* Merge pull request #200 from ral-facilities/feature/remove-sql-dependency-from-backends-#154

Recreate SQL Dependency PR ([`89b9d19`](https://github.com/ral-facilities/datagateway-api/commit/89b9d1993ff68d20e230590e64daef158527751a))

*  #154: Fix broken tests ([`c84eccf`](https://github.com/ral-facilities/datagateway-api/commit/c84eccf88efa4461677ffd5b252fa56422d74310))

* Merge branch &#39;master&#39; into feature/remove-sql-dependency-from-backends-#154 ([`deb1539`](https://github.com/ral-facilities/datagateway-api/commit/deb1539a53ccc22d1768f14a782bb13621e40882))

* Merge pull request #196 from ral-facilities/feature/implement-ci-#163

Implement GitHub Actions Workflow ([`fae9695`](https://github.com/ral-facilities/datagateway-api/commit/fae9695d6a96fee941dbc07db979e16f4481cf59))

* Merge pull request #197 from ral-facilities/feature/code-coverage-#167

Add Code Coverage Reports ([`bccce12`](https://github.com/ral-facilities/datagateway-api/commit/bccce121e46e9590b78124d02c7a9cfaaa295362))

*  #163: Update PR template ([`d012130`](https://github.com/ral-facilities/datagateway-api/commit/d01213013712c82aad13afe52fadc3e624bd4e8f))

*  #167: Remove codecov as a dependency

- This is no longer needed, I&#39;ve opted to use the GitHub Actions codecov plugin ([`9542fc8`](https://github.com/ral-facilities/datagateway-api/commit/9542fc808562d57b5070fa0f73c79b3830ead6f0))

*  #167: Remove coverage nox session

- This was not used, with the codecov GitHub Actions plugin used instead ([`680a5e7`](https://github.com/ral-facilities/datagateway-api/commit/680a5e74ff68e5c0aeeb123712421a8f9ef4f18b))

*  #167: Remove current branch to launch CI build ([`ce6f2fc`](https://github.com/ral-facilities/datagateway-api/commit/ce6f2fcab52eaa9462b7aa137b599141faade8f9))

*  #167: Remove coverage workflow ([`3c8ba50`](https://github.com/ral-facilities/datagateway-api/commit/3c8ba505578eac996e216a789ff3d58b4ead2425))

*  #167: Add coverage steps in build and test ([`b5c22a2`](https://github.com/ral-facilities/datagateway-api/commit/b5c22a26202a13b2811ed08a11ec7ae9c0215533))

*  #167: Add arg for noxfile.py ([`16e434b`](https://github.com/ral-facilities/datagateway-api/commit/16e434b4ec40d14460a8d496222b4c0a24c29588))

*  #167: Add coverage Actions workflow ([`55ecf7a`](https://github.com/ral-facilities/datagateway-api/commit/55ecf7a2de6cf56e884a28eb7558c49f35437dc9))

*  #167: Add status badge for codecov ([`e43b39e`](https://github.com/ral-facilities/datagateway-api/commit/e43b39e7a27d16cfcf14987179105a237bdbd298))

*  #167: Add coverage nox session ([`a938083`](https://github.com/ral-facilities/datagateway-api/commit/a9380830a4543afede3752bb7541023d9078ae33))

*  #167: Add codecov dependency ([`dd223c5`](https://github.com/ral-facilities/datagateway-api/commit/dd223c5dbadda824df61d867731bec06a9fa6079))

*  #163: Allow CI to be triggered manually ([`689c2a1`](https://github.com/ral-facilities/datagateway-api/commit/689c2a1f5ff5882355dc8445f564cc025590e4e0))

* Merge pull request #175 from ral-facilities/feature/improve-logging-icat-backend-#164

Improve Logging Throughout Python ICAT Backend ([`d5ea7ba`](https://github.com/ral-facilities/datagateway-api/commit/d5ea7ba18d7c73138245436cc4a1e98919e9a2e3))

*  #163: Disable current branch from running CI when pushed ([`5281922`](https://github.com/ral-facilities/datagateway-api/commit/528192200db479e7dd95d5b19727c64967c3fe70))

*  #163: Change conditional for when CI runs ([`d0c3a0a`](https://github.com/ral-facilities/datagateway-api/commit/d0c3a0a341cefda765b868a21c90c54eb3c1d3f1))

*  #162: Disable fail-fast on test jobs

- It can be useful to let all versions complete to give a better picture of the issues ([`d5a40a5`](https://github.com/ral-facilities/datagateway-api/commit/d5a40a510508825c43a57c237ccb7e055ba896fa))

*  #163: Remove unneeded nox sessions from tests job ([`7117e61`](https://github.com/ral-facilities/datagateway-api/commit/7117e61de284ac0aec95de049ae1921b79dbda56))

*  #163: Add separate jobs for each nox session ([`9a19073`](https://github.com/ral-facilities/datagateway-api/commit/9a19073220b4712fb54258d4d2a5eb80dcc1fef2))

*  #163: Remove Python 3.5 support

- Some dependencies require Python &gt;=3.6 ([`b04abbd`](https://github.com/ral-facilities/datagateway-api/commit/b04abbdd7e64c1831d12e3dce0266db6d2cd3051))

*  #163: Allow Poetry to use Python 3.5 ([`5ab6c93`](https://github.com/ral-facilities/datagateway-api/commit/5ab6c93a31e58e507a8d26c170f957fad50876e8))

*  #163: Remove Python 3.4 from CI build ([`9ebc58c`](https://github.com/ral-facilities/datagateway-api/commit/9ebc58cbb759a7df3b31388d02fb66871925013a))

*  #163: Remove non-working Python versions ([`8391a5c`](https://github.com/ral-facilities/datagateway-api/commit/8391a5cd95ed08d37591911b31d63cc0ea2612cb))

*  #163: Update setup-python Action ([`e1341cd`](https://github.com/ral-facilities/datagateway-api/commit/e1341cd3ab31fe79c7decc560dc59d580ffd7ee7))

*  #163: Remove specific python version on non-specific nox sessions ([`2792e7d`](https://github.com/ral-facilities/datagateway-api/commit/2792e7d474984c1f3503496fac36ecc95e7b1ce5))

*  #163: Add more versions of Python to build against ([`0a50a69`](https://github.com/ral-facilities/datagateway-api/commit/0a50a69e63ab66eeb7bd450ad9ae76ce3374c5e6))

*  #163: Update pymysql ([`31e3002`](https://github.com/ral-facilities/datagateway-api/commit/31e3002c7ccbb9f73626673af86c0e2b9758ce36))

*  #154: Fix issue with the API when served via WSGI ([`abae518`](https://github.com/ral-facilities/datagateway-api/commit/abae5185f8d88b6c9fc10ac25849628fdd286c7a))

*  #154: Make EntityHelper into an abstract class ([`f6181d3`](https://github.com/ral-facilities/datagateway-api/commit/f6181d3b60334bdfacde59580ab105c8f24af27e))

*  #163: Remove parallel restriction ([`a7d5193`](https://github.com/ral-facilities/datagateway-api/commit/a7d51935e39a9460a6f1072a4f59eac58bc4101a))

*  #163: Update SQLAlchemy

- See if this fixes the Python 3.8 build ([`d672986`](https://github.com/ral-facilities/datagateway-api/commit/d672986bf88a0484bf1a33c3167dedaed461105e))

*  #163: Add comments to workflow ([`a3c6963`](https://github.com/ral-facilities/datagateway-api/commit/a3c69633f93ff4397c43b9a53a5c9d3166eeda50))

*  #163: Remove debugging steps ([`23e5c77`](https://github.com/ral-facilities/datagateway-api/commit/23e5c776e00936f962d1f10aa7a1f1d10a743ad3))

*  #163: Change debug to localhost ([`6079255`](https://github.com/ral-facilities/datagateway-api/commit/6079255f69c8f197f95aa3d14be046db897b81e3))

*  #163: Correct sed command ([`9ac5ec0`](https://github.com/ral-facilities/datagateway-api/commit/9ac5ec06dcb3bb0eb94fb50e28d9874972df315b))

*  #163: Remove blank step ([`c084d98`](https://github.com/ral-facilities/datagateway-api/commit/c084d9836d8ca4ae6712f279d54c4fff5c12115b))

*  #163: Replace default payara user ([`ec72663`](https://github.com/ral-facilities/datagateway-api/commit/ec7266360c24e3d0c0d77778a1c3b9da7e7044f3))

*  #163: Change inventory file ([`585afbf`](https://github.com/ral-facilities/datagateway-api/commit/585afbfe55a6e7d5483aa82a600544f67cb0c9a5))

*  #163: Change icat-ansible to use non-forked version ([`64ab5ba`](https://github.com/ral-facilities/datagateway-api/commit/64ab5ba8fcc463793facf0b526e4bab6b40e0066))

*  #163: Comment out Ansible Actions usage ([`71e70e8`](https://github.com/ral-facilities/datagateway-api/commit/71e70e8e5ea7de7838234280ca790be0d3bd3291))

*  #163: Debugging for Actions workflow ([`d4c1163`](https://github.com/ral-facilities/datagateway-api/commit/d4c1163522cc16e1a37e687ac9485bc998d9d5a1))

* Fix session handling for db backend using Flask-SQLAlchemy ([`f67ad95`](https://github.com/ral-facilities/datagateway-api/commit/f67ad95f484363e46fb226402bd5c526e9eb2ec6))

*  #163: Update py dependency ([`9299cf7`](https://github.com/ral-facilities/datagateway-api/commit/9299cf7dc71e28fe0261d51142c7b365ce970e70))

*  #163: Change test_valid_db_url to new DB_URL ([`83714a1`](https://github.com/ral-facilities/datagateway-api/commit/83714a15d3db2ef11815ed3ee4f1990122603848))

*  #163: Edit dummy data cmd ([`7b43ead`](https://github.com/ral-facilities/datagateway-api/commit/7b43ead83cfb81c64ed81141bed516552e9be2ff))

*  #163: Change dummy data cmd ([`ed470b3`](https://github.com/ral-facilities/datagateway-api/commit/ed470b3511c64863e803e8b89510ab8496275310))

*  #163: Add step to use icat_db_generator ([`22d987e`](https://github.com/ral-facilities/datagateway-api/commit/22d987e19bfd1b27d24873108cc77ec207962dc3))

*  #163: Change example ICAT_URL to localhost ([`7d1d0b4`](https://github.com/ral-facilities/datagateway-api/commit/7d1d0b4c0d3df5dff22dc8a908cbad371ee0a050))

*  #163: Change debug to localhost ([`cfa20d8`](https://github.com/ral-facilities/datagateway-api/commit/cfa20d81410da705d0afca3d71dddd6c7c23e584))

*  #163: Correct sed command ([`5c78a76`](https://github.com/ral-facilities/datagateway-api/commit/5c78a763ae149e7463ed6beb5e72e0e958314111))

*  #163: Remove blank step ([`5d246d8`](https://github.com/ral-facilities/datagateway-api/commit/5d246d84b1e04ca540263d9c2d94413bc0b21f2f))

*  #163: Replace default payara user ([`05cd039`](https://github.com/ral-facilities/datagateway-api/commit/05cd03924ab82d19c3a3b9651aca78ab5b282037))

*  #163: Change inventory file ([`71ad07b`](https://github.com/ral-facilities/datagateway-api/commit/71ad07b9fa026c9d22481e072e7ef216e5be80e2))

*  #163: Update example config to use localhost values ([`c2391c2`](https://github.com/ral-facilities/datagateway-api/commit/c2391c2671128e0c8c91ecc273c83bac87fd0e74))

*  #163: Specify noxfile ([`30ec28f`](https://github.com/ral-facilities/datagateway-api/commit/30ec28f8c5b6cb59ed1166ad9598a3b4437afea5))

*  #163: Change icat-ansible to use non-forked version ([`d6ac7b2`](https://github.com/ral-facilities/datagateway-api/commit/d6ac7b22ba4b0529c673a866ada7b645452673b2))

*  #163: Comment out Ansible Actions usage ([`4672e03`](https://github.com/ral-facilities/datagateway-api/commit/4672e0372a83130f1a89c351f65032523fe69b9a))

*  #163: Lots of debugging ([`c9d290d`](https://github.com/ral-facilities/datagateway-api/commit/c9d290d8a7994403bdfe60ab10930eda3dc15ae8))

* Merge pull request #171 from ral-facilities/feature/remaining-icat-endpoints-#145

Implement Remaining Standard Endpoints for Python ICAT Backend ([`e9a9173`](https://github.com/ral-facilities/datagateway-api/commit/e9a9173c6913153e2ea40511e3519f82cd821e21))

*  #163: Make path explict ([`1e7a9ce`](https://github.com/ral-facilities/datagateway-api/commit/1e7a9cecb658f78ffea75182d1472251135d9b64))

*  #163: Add missing uses line ([`cdf2b1c`](https://github.com/ral-facilities/datagateway-api/commit/cdf2b1cd014720321cad39c05c4d63628d25c9aa))

*  #163: Add steps to build a local instance of ICAT ([`05b2337`](https://github.com/ral-facilities/datagateway-api/commit/05b2337f2fa76868b0cac4baef0241790343c39f))

* Merge pull request #194 from ral-facilities/feature/add-not-like-filter-#193

Add NOT Like Operator to WHERE Filter ([`a6c35ae`](https://github.com/ral-facilities/datagateway-api/commit/a6c35ae1926f54d4bd08b8c4781363224ca762f3))

*  #193: Add NOT like operatior for WHERE filter to DB backend ([`9455685`](https://github.com/ral-facilities/datagateway-api/commit/9455685c48c3a823af3a1ecfacff2f0476a8d4dc))

*  #193: Add NOT like operation to WHERE filter on ICAT backend ([`2d33c0c`](https://github.com/ral-facilities/datagateway-api/commit/2d33c0c1dfe16281a78284d69e79255f87865979))

*  #163: Force each Python version build to run sequentially

- With using preprod as the ICAT URL, there&#39;s issues with the 3 jobs (3 python versions) running tests at the same time meaning that they fail. This is a workaround for the time being, though I think a move to icat-ansible and using a local ICAT instance could prevent this from being a problem because jobs run on different hosted runners, so each job would use a different &#39;local&#39; ICAT instance ([`d8b618d`](https://github.com/ral-facilities/datagateway-api/commit/d8b618d0acb8ee043f24cdf0f32564eb611770b4))

*  #163: Set log location for exampple config file

- This will prevent tests related to testing log location from failing ([`33b7531`](https://github.com/ral-facilities/datagateway-api/commit/33b7531bf71eb92bda3ae39e16cecedf2d8fd6fb))

*  #163: Add GH Actions status badge ([`2500207`](https://github.com/ral-facilities/datagateway-api/commit/2500207e3f245d708b8e49716efb97366bc681c6))

*  #163: Use jq to edit log location ([`4e4fac1`](https://github.com/ral-facilities/datagateway-api/commit/4e4fac11971f7fede0d67df1d6033b1f2b9c77dd))

*  #163: Actually add the value and file envs ([`617aff1`](https://github.com/ral-facilities/datagateway-api/commit/617aff1de0d6f2b7bd5c5148af37255271d962aa))

*  #163: Change key to lowercase, to match the actual key

- Also test if jq exists on the machines, as an alternative to json-edit-action ([`bd7bbc0`](https://github.com/ral-facilities/datagateway-api/commit/bd7bbc0a21b53a878a25a79ed4cf468146d88320))

*  #163: Separate log file location and log_location config change ([`feaedf4`](https://github.com/ral-facilities/datagateway-api/commit/feaedf4a97467ad8377c8b1e9e7856a3adc206b2))

*  #163: Add step to create log file for testing ([`0823e12`](https://github.com/ral-facilities/datagateway-api/commit/0823e12d8d64d410503f22f407ebc92bf2db4fc2))

*  #163: Change example ICAT_URL to SciGateway preprod

- Perhaps a temporary change just to get some automated tests running on GH Actions ([`8a4fcd0`](https://github.com/ral-facilities/datagateway-api/commit/8a4fcd0c98fa5acb0790cd5332ae9bf77a5737f4))

*  #163: Add conditionals to nox sessions

- This is to get all nox sessions to run even if one has failed - nox sessions do not depend on each other ([`47d1c01`](https://github.com/ral-facilities/datagateway-api/commit/47d1c0175dd69e8fceab5c8467777f2e71ff48ca))

*  #163: Copy the example config to config.json

- This commit also adds &#39;name&#39; tags to everything to make things more understandable ([`81acc92`](https://github.com/ral-facilities/datagateway-api/commit/81acc928c3b6163d2fd4d1852a43502fde6928fa))

*  #163: Add baseline GitHub Actions workflow ([`863d1f2`](https://github.com/ral-facilities/datagateway-api/commit/863d1f23a06c4773ae5dd72950e92c0898b8f789))

* Merge pull request #191 from ral-facilities/feature/test-multiple-backends-#150

Add Tests for ICAT Backend ([`b11001d`](https://github.com/ral-facilities/datagateway-api/commit/b11001d361c3a4477d923dd907b6a61667ba0602))

* Merge pull request #192 from ral-facilities/feature/add-icat-backend-documentation-#190

Add ICAT Backend Documentation ([`5301cfd`](https://github.com/ral-facilities/datagateway-api/commit/5301cfd2f398286d7f67221ea2b6d735c330ec06))

*  #145: Improve the GET /sessions helper function

- Remove rounding on the expireDateTime value and ensure it always returns a consistent, accurate result
- Change the keys to camelCase, in line with the rest of the API ([`d6bff57`](https://github.com/ral-facilities/datagateway-api/commit/d6bff57de7a0071f294d61af71579d1c1859f5d2))

*  #145: Improve datetime conversion

- The &#39;accepted_date_format&#39; constant is removed since it&#39;s no longer used. Datetime to string conversion will convert to ISO format and string to datetime can be converted using the same format (allowing for easy-tripping of datetimes for API users). ([`e8c13e9`](https://github.com/ral-facilities/datagateway-api/commit/e8c13e9ad184fdabb231b6647e40b964fe909a6c))

*  #190: Add --without-hashes options to poetry export cmd

- This commit also adds the &#34;tests&#34; session to the list of Nox sessions ([`fb3900b`](https://github.com/ral-facilities/datagateway-api/commit/fb3900b25334aa141c36b33efb17bc71e137c043))

*  #190: Add link to icat.manual repo for tutorials on setting up an ICAT instance ([`73bb72d`](https://github.com/ral-facilities/datagateway-api/commit/73bb72d186a321b81bfba4e02484aed37d81e604))

*  #190: Make requested changes from PR linked to this issue ([`f320600`](https://github.com/ral-facilities/datagateway-api/commit/f320600cade44ea7ecfe4d3264a05b9dcc1da269))

* Merge pull request #185 from ral-facilities/feature/add-code-linting-#165

Add Code Linting and Implementation of Hypermodern Python ([`ca0efc6`](https://github.com/ral-facilities/datagateway-api/commit/ca0efc66da3a5a19bf0ea82c4b9ada685afdd8ef))

* Merge pull request #186 from ral-facilities/feature/fix-code-linting-#184

Apply Fixes suggested by Linting Tools ([`9b4907c`](https://github.com/ral-facilities/datagateway-api/commit/9b4907c77b76b50cb1d4d7818f34ab40cbf45c1a))

* Merge branch &#39;feature/test-multiple-backends-#150&#39; of github.com:ral-facilities/datagateway-api into feature/test-multiple-backends-#150 ([`6dea07e`](https://github.com/ral-facilities/datagateway-api/commit/6dea07edabd350b8291810489dbafa5032ef9ad3))

*  #150: Make requested changes on PR review ([`e826e20`](https://github.com/ral-facilities/datagateway-api/commit/e826e207c439da7a6597df1fe30fc32bf3497292))

* Update datagateway_api/common/backends.py

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`baff80d`](https://github.com/ral-facilities/datagateway-api/commit/baff80dd02f6a6f40d217ac5b0aff438d02fb123))

* Merge branch &#39;feature/fix-code-linting-#184&#39; into feature/test-multiple-backends-#150 ([`01449cc`](https://github.com/ral-facilities/datagateway-api/commit/01449cc63e05797b398760384bbf017bc4f00b78))

* Merge branch &#39;feature/add-code-linting-#165&#39; into feature/fix-code-linting-#184 ([`c4b63eb`](https://github.com/ral-facilities/datagateway-api/commit/c4b63eb344f6e13979e83976f4d05130747403ae))

* Merge branch &#39;feature/remove-sql-dependency-from-backends-#154&#39; into feature/add-code-linting-#165 ([`821e8b9`](https://github.com/ral-facilities/datagateway-api/commit/821e8b93fd6ecacc591bcff4b4e683f78574a872))

*  #165: Remove details regarding tmpdir cmd option

- This has been removed in a different branch so I&#39;ve removed the documented details about it in this branch and adjusted it according to the new solution found ([`135965c`](https://github.com/ral-facilities/datagateway-api/commit/135965c02c1384d1350fe4052c759041b561a273))

* Merge branch &#39;feature/improve-logging-icat-backend-#164&#39; into feature/remove-sql-dependency-from-backends-#154 ([`ec1dd64`](https://github.com/ral-facilities/datagateway-api/commit/ec1dd6466efe266a5901d27c0ee8cf12d3c1b87a))

* Merge branch &#39;feature/improve-logging-icat-backend-#164&#39; into feature/remove-sql-dependency-from-backends-#154 ([`adc1f40`](https://github.com/ral-facilities/datagateway-api/commit/adc1f40713cd1f056b44f8eb4e9615b39fae8c53))

* Merge branch &#39;feature/fix-code-linting-#184&#39; into feature/test-multiple-backends-#150 ([`91f90a1`](https://github.com/ral-facilities/datagateway-api/commit/91f90a14a0f7350cd9e27f8349823ba66008c9d4))

* Merge pull request #177 from ral-facilities/feature/add-postman-collection-#162

Add Postman Collection to Repo ([`0578120`](https://github.com/ral-facilities/datagateway-api/commit/0578120f715fe593441865dc3120a549f59da7fc))

* Merge branch &#39;feature/add-code-linting-#165&#39; into feature/fix-code-linting-#184 ([`36dfeb0`](https://github.com/ral-facilities/datagateway-api/commit/36dfeb060219f056b15b2154e1a05a2f747d2517))

*  #165: Disable auto file deletion for NamedTemporaryFile

- This fixes a PermissionError that was found when using these Nox sessions on Windows
- This is a replacement solution for the tmp_dir option/fix, so that&#39;s now been removed ([`ed448ca`](https://github.com/ral-facilities/datagateway-api/commit/ed448ca98aa42b03d17485707ce44eaa7da1a1de))

*  #162: Make changes requested to collection

- Make variables work for the collection, not the environment
- Set default port to 5000, matching the default port on the API ([`493ac65`](https://github.com/ral-facilities/datagateway-api/commit/493ac650b56b4ba1e832aa4c537ccfe5fb499126))

*  #190: Make change to project tree based on previous commit ([`93d0980`](https://github.com/ral-facilities/datagateway-api/commit/93d09807b6c631e6607a94d2964b5e0bf45b8018))

*  #190: Rename query_filter_factory.py ([`60c56f6`](https://github.com/ral-facilities/datagateway-api/commit/60c56f62ec877d1d6f934b24173b9cd40b9b06f8))

*  #165: Add a note to remind users to have user&#39;s Python added to PATH ([`f2f7f55`](https://github.com/ral-facilities/datagateway-api/commit/f2f7f55eff5ea86202471ea7b709d24747d7a606))

*  #190: Update README.md for ICAT backend ([`8b24725`](https://github.com/ral-facilities/datagateway-api/commit/8b2472514df420ea6546b860e95394dfd22ad1e9))

*  #190: Make small changes to existing docs ([`96f5aec`](https://github.com/ral-facilities/datagateway-api/commit/96f5aecc5fdf37917899cf2c67aa42b7d25f94e5))

* Merge branch &#39;feature/fix-code-linting-#184&#39; into feature/test-multiple-backends-#150 ([`5f10ecc`](https://github.com/ral-facilities/datagateway-api/commit/5f10eccad53239c51ad23604867f88e02658296d))

* Merge branch &#39;feature/add-code-linting-#165&#39; into feature/fix-code-linting-#184 ([`1013e82`](https://github.com/ral-facilities/datagateway-api/commit/1013e82fb413c5b3eef16c454669c17a77cf8027))

*  #184: Make response descriptions have consistent syntax

- The commit also includes a rebuilt openapi.yaml ([`fe88196`](https://github.com/ral-facilities/datagateway-api/commit/fe88196f2f7ed7291bbce6fa8108836345bbe65b))

*  #184: Fix linting issues as brought up in PR

- Most likely caused when I merged other branches after I created the PR ([`b01eaf5`](https://github.com/ral-facilities/datagateway-api/commit/b01eaf503210d84cfe63fd3077d8d7cae2ad910f))

* Merge branch &#39;feature/fix-code-linting-#184&#39; into feature/test-multiple-backends-#150 ([`3b6251c`](https://github.com/ral-facilities/datagateway-api/commit/3b6251c5a5768f1ca9e221421ca103b1e60d2501))

*  #150: Add documentation for running the tests ([`4039233`](https://github.com/ral-facilities/datagateway-api/commit/40392333b159de0d3c2034e8ede2ab46d705a2dd))

*  #165: Allow tmp directory to be configured for nox sessions ([`0366d08`](https://github.com/ral-facilities/datagateway-api/commit/0366d08d0b531c98d229e9ce3c849e00c2d8f043))

* Merge branch &#39;feature/add-code-linting-#165&#39; of github.com:ral-facilities/datagateway-api into feature/add-code-linting-#165 ([`3682165`](https://github.com/ral-facilities/datagateway-api/commit/3682165ade132dc05b76d002bb5636df13429b29))

*  #165: Update repo tree structure

- Also added a command to generate this tree in the future (I just used to update it manually). ([`b80347f`](https://github.com/ral-facilities/datagateway-api/commit/b80347ff5ba975e0a370704e47eeb90ec4fa57b1))

*  #150: Add ISIS endpoint testing for DB backend ([`0c59b58`](https://github.com/ral-facilities/datagateway-api/commit/0c59b58b27e44c4258986602779579e7507c13e4))

*  #150: Actually fix openapi YAML creation

- This is essentially an undo of 8c1941dfbda5d77092a19a61c2e14a2a300f5786 as I&#39;ve realised the backend must get parsed into the endpoint classes for testing reasons ([`c5a867c`](https://github.com/ral-facilities/datagateway-api/commit/c5a867c6c8d101fc639ae6a7e138ddb58f60d29a))

*  #150: Add findone tests for DB backend

- This commit also includes a fixes a bug found on the 404 of that test class ([`3eec346`](https://github.com/ral-facilities/datagateway-api/commit/3eec3464e9badaccd69981e5b6dd09c652a520fe))

*  #150: Fix openapi YAML creation

- I&#39;ve reverted the setup for the ISIS and session endpoints back to way it was done at the start of this branch, there&#39;s no need to parse backend now the test backend is set in the config object, just create it locally on each endpoint file ([`8c1941d`](https://github.com/ral-facilities/datagateway-api/commit/8c1941dfbda5d77092a19a61c2e14a2a300f5786))

*  #150: Add get with filter tests for DB backend ([`1b91217`](https://github.com/ral-facilities/datagateway-api/commit/1b9121749a3e5cb2d7ee5fd900fbb72bfc6d4a5b))

*  #150: Add remaining data creation fixtures for DB backend tests

- These fixtures haven&#39;t been tested, they will when I write the remaining endpoint tests for the DB backend ([`b2af27d`](https://github.com/ral-facilities/datagateway-api/commit/b2af27dabe656b392aeb936d7abed7a7f3dfa745))

*  #150: Create localised conftest files

- Local to each backend, with a shared file in test/ ([`42359fc`](https://github.com/ral-facilities/datagateway-api/commit/42359fc0ca156db134f7ae732f24f1488e94e20d))

*  #150: Ensure filenames are unique across test suite

- pytest requires that all filenames are unique, even if they&#39;re stored in different directories ([`578f897`](https://github.com/ral-facilities/datagateway-api/commit/578f897268e02f9ad619df4d3b6c8612300d5653))

*  #150: Move endpoint rules tests

- This aren&#39;t backend-specific ([`6baf55d`](https://github.com/ral-facilities/datagateway-api/commit/6baf55dd797f5811bef65dd4300b88296f3cef55))

*  #150: Add tests for /count for DB backend ([`bbca31c`](https://github.com/ral-facilities/datagateway-api/commit/bbca31cd3291f6433baf10c6c5c6372a6204faac))

*  #150: Add get by ID tests for DB backend ([`b6c7c66`](https://github.com/ral-facilities/datagateway-api/commit/b6c7c66cd53cb73ddb220141ace3ee5a27e4d92e))

* Update README.md

Co-authored-by: Viktor Bozhinov &lt;45173816+VKTB@users.noreply.github.com&gt; ([`a4ca2df`](https://github.com/ral-facilities/datagateway-api/commit/a4ca2df69c2adc1859e8df592596c303b6272277))

*  #150: Add test to ensure all required abstract methods are present for Backend ([`f5c4558`](https://github.com/ral-facilities/datagateway-api/commit/f5c4558f084ac3f4fe9b02a43b5d885480831ff9))

*  #150: Rewrite queries_records tests ([`97bf1a4`](https://github.com/ral-facilities/datagateway-api/commit/97bf1a4f5edab0f2c467b6bb64d6b8c60396a889))

*  #150: Rewrite get_filter_from_query_string tests ([`d6f6ab8`](https://github.com/ral-facilities/datagateway-api/commit/d6f6ab8c82851c1adcf36b54ab44d21590685b4d))

*  #150: Complete TODOs from &#39;backend can be set for tests&#39; work ([`74215cd`](https://github.com/ral-facilities/datagateway-api/commit/74215cdbfda4d1b4e4c417be3cd2d568d4143bb4))

*  #150: Rewrite session ID from header tests ([`e8f1139`](https://github.com/ral-facilities/datagateway-api/commit/e8f113975077b463f62c78be71778d20b2c8be3d))

*  #150: Rename valid ICAT creds header

- This has been renamed due to the addition of a valid credentials header for the DB backend ([`89d58d6`](https://github.com/ral-facilities/datagateway-api/commit/89d58d6b7c361404821503df86f5fd9a7dc5386f))

*  #150: Rewrite DB session decorator tests ([`a07f0db`](https://github.com/ral-facilities/datagateway-api/commit/a07f0dbd4ed432862458d311cd8689e5488e60c6))

*  #150: Rewrite JSON validity tests ([`b97b19b`](https://github.com/ral-facilities/datagateway-api/commit/b97b19bff6b74239f3f6d49f92acb2bdf98ea3e9))

*  #150: Rewrite database helper tests
- The file has been renamed to reflect these tests actually test the QueryFilterFactory ([`cf89d7e`](https://github.com/ral-facilities/datagateway-api/commit/cf89d7e15d4b5c084feefef299058ee73cc6bf0b))

*  #150: Rewrite DB entity helper tests in pytest ([`cff2ce4`](https://github.com/ral-facilities/datagateway-api/commit/cff2ce477ec9fcc446ba10ad362966ae45cfbbca))

*  #150: Restructure test files

- Before this commit, I kept the pytest tests I&#39;ve created in this branch separate from the unittest tests that were there beforehand to keep them isolated. This restructure means that non-backend specific tests are together, and backend specific tests are put in the correctly named directories ([`b8324db`](https://github.com/ral-facilities/datagateway-api/commit/b8324db630ad77a20e094f9b40ef0ff90c6d49b6))

*  #150: General cleanup of recent work

- Sort out linting and remove a few lines of code used for logging etc. ([`c866be3`](https://github.com/ral-facilities/datagateway-api/commit/c866be37400bdfe27aab65984431d70258c4f1d8))

*  #150: Fix FlaskAppTest based on changes to main.py

- This is a temporary fix before rewriting the original tests in pytest ([`bcea7ec`](https://github.com/ral-facilities/datagateway-api/commit/bcea7ec46e0c1819d8a7ae1d55e2f1d0b78fc5d7))

*  #150: Remove unneeded import ([`dce47c1`](https://github.com/ral-facilities/datagateway-api/commit/dce47c1d2117196b1183699cb931857ac2ddaf85))

*  #150: Fix logging issues when dealing with session IDs which are strings, not numbers

- When dealing with session IDs, you cannot assume they are numbers, since they&#39;re in the format of UUIDs, so %s is more suitable ([`c29f68e`](https://github.com/ral-facilities/datagateway-api/commit/c29f68e9452a9f5835c2ebe0ab0c54bdc762e393))

*  #150: Fix imports on test helpers ([`c676f46`](https://github.com/ral-facilities/datagateway-api/commit/c676f46c8c9a6df9d03d2892bfaba8ad780524ff))

*  #150: Correct import for QueryFilterFactory ([`dd9a92a`](https://github.com/ral-facilities/datagateway-api/commit/dd9a92ae3f6e8be1fd1eddaae5e605298aab56f5))

*  #150: Fix imports on database helpers ([`adc48d1`](https://github.com/ral-facilities/datagateway-api/commit/adc48d181371de4a1ac84302296a9e86112b44b4))

*  #150: Fix failing endpoint rule tests

- The tests were looking at the flask app from src.main which is only setup if running the file as per README.md. So a generic flask app fixture has been created and that&#39;s used to check endpoint rules ([`db97d8a`](https://github.com/ral-facilities/datagateway-api/commit/db97d8a2934de943457b373cb56fb6e97f1bbb81))

*  #150: Add separate flask app fixtures for each backend

- The DB app will be used when I rewrite the old tests into pytest, tests which will remain for testing the DB backend ([`3890c55`](https://github.com/ral-facilities/datagateway-api/commit/3890c5522cce5914f7064e1fc8764d4fa8f1298a))

*  #150: Allow backend type to be set when a flask test fixture runs

- This will allow tests to run on a backend set by the fixture instead of relying on the contents of config.json. This means both backends can be tested in one test session and the contents of the config file doesn&#39;t matter ([`70dc393`](https://github.com/ral-facilities/datagateway-api/commit/70dc3937243eee3825beef48b291fea93f2a2771))

*  #150: Move QueryFilterFactory to its own file

- It used to be in the database helpers file, but this class is used across both backends
- The imports have been moved inside the staticmethod because the Flask TEST_BACKEND config option won&#39;t have been set by the time QueryFilterFactory has been imported, so the imports which decide which set of filters to import must be put in some code. ([`7a6a8ef`](https://github.com/ral-facilities/datagateway-api/commit/7a6a8ef2e0ee46f8de60c7823091818dc9d51619))

*  #150: Expand flask test app so the backend can be configured

- This doesn&#39;t fully work yet because filters are still created based on contents of config.json ([`6902921`](https://github.com/ral-facilities/datagateway-api/commit/69029214a0d0a2c12351632e32f92e608ad37453))

*  #150: Checkpoint in making backend configurable for testing ([`9532d91`](https://github.com/ral-facilities/datagateway-api/commit/9532d910ffd4491506f221a33b2cd0a22c70763e))

* Merge branch &#39;feature/add-code-linting-#165&#39; into feature/fix-code-linting-#184 ([`116ca2a`](https://github.com/ral-facilities/datagateway-api/commit/116ca2a00d4c9cc6bf1d63b78a843a5fe9cedba7))

* Merge branch &#39;feature/remove-sql-dependency-from-backends-#154&#39; into feature/add-code-linting-#165 ([`9e34729`](https://github.com/ral-facilities/datagateway-api/commit/9e34729c3ab813e3aacff197f6fbafc395750f3c))

* Merge pull request #172 from ral-facilities/feature/isis-specific-endpoints-icat-#146

Implment ISIS Specific Endpoints for Python ICAT Backend ([`fc2c48c`](https://github.com/ral-facilities/datagateway-api/commit/fc2c48cea634cc72df29bff3b509a39205b79c84))

* Merge pull request #178 from ral-facilities/feature/fix-swagger-data-parsing-#166

Update Swagger/OpenAPI Docs for New Backend ([`864e020`](https://github.com/ral-facilities/datagateway-api/commit/864e02073936ac697e8f4018730d2f149c55d806))

* Merge branch &#39;feature/isis-specific-endpoints-icat-#146&#39; into feature/improve-logging-icat-backend-#164 ([`4acfc92`](https://github.com/ral-facilities/datagateway-api/commit/4acfc92ccfb1396a4c1000b7ef6abe93f9b4ff2d))

*  #146: Correct mistake made in merge conflict resolution ([`1a16451`](https://github.com/ral-facilities/datagateway-api/commit/1a16451f79d0f247205102a7b70eb3f32e0727dd))

*  #145: Correct mistake made in merge conflict resolution ([`ed3fe4f`](https://github.com/ral-facilities/datagateway-api/commit/ed3fe4f29f3ffa7412a027f4c1b81d8241f6d614))

* Merge branch &#39;feature/remaining-icat-endpoints-#145&#39; into feature/isis-specific-endpoints-icat-#146 ([`7532606`](https://github.com/ral-facilities/datagateway-api/commit/75326067e1bb3e676316122f1a63227766542f0c))

* Merge pull request #180 from ral-facilities/feature/fix-exception-handling-#147

Fix Exception Handling for Non-Debug Mode ([`b12e7cd`](https://github.com/ral-facilities/datagateway-api/commit/b12e7cdb5213d44e494f61211b10e8728b91b420))

* Merge branch &#39;master&#39; into feature/remaining-icat-endpoints-#145 ([`4d00fb2`](https://github.com/ral-facilities/datagateway-api/commit/4d00fb2f56a9cae2f941b757fb2ef25bb1bdfb44))

* Merge branch &#39;master&#39; into feature/remaining-icat-endpoints-#145 ([`69f96bd`](https://github.com/ral-facilities/datagateway-api/commit/69f96bd76e7502891cdb4543e665b36711d78353))

* Merge pull request #170 from ral-facilities/feature/distinct-filter-included-columns-#148

Update the distinct filter to accept &#39;included&#39; fields ([`7b72dc9`](https://github.com/ral-facilities/datagateway-api/commit/7b72dc9dd884854f03567e8298453b122aac4e22))

*  #164: Move logging for consistency ([`d0104eb`](https://github.com/ral-facilities/datagateway-api/commit/d0104eb7d41f3fd517da997a565e6e5fe99d0b33))

*  #150: Move Flask/API setup into functions

- This will help to specify whether a unit test should use the db or python_icat backend, to be fully implemented in future commits ([`64f9981`](https://github.com/ral-facilities/datagateway-api/commit/64f9981d339cb175f19cc6dcb95fbf62b03e823a))

* Merge branch &#39;feature/remove-sql-dependency-from-backends-#154&#39; into feature/add-code-linting-#165 ([`c977be0`](https://github.com/ral-facilities/datagateway-api/commit/c977be0867aa4f5af08df4e269357571c1d1a652))

*  #150: Remove planning comments made at start of branch ([`2c37baa`](https://github.com/ral-facilities/datagateway-api/commit/2c37baa0687cba125a03940b757327af1a0da173))

*  #150: Solve linting issues ([`e85f378`](https://github.com/ral-facilities/datagateway-api/commit/e85f3785d3e4028da7701bc30ffb788bafb4860d))

*  #150: Fix order filter test failures

- test_direction_is_uppercase() wasn&#39;t being destroyed correctly ([`90f14a1`](https://github.com/ral-facilities/datagateway-api/commit/90f14a12e55c3e7457d188a2bc8e406889e0e457))

*  #150: Increase coverage of PythonICATIncludeFilter ([`49ef7f8`](https://github.com/ral-facilities/datagateway-api/commit/49ef7f807129a069ff7beeaa2dbb66663d969be5))

*  #150: Add valid tests for table endpoints ([`5910404`](https://github.com/ral-facilities/datagateway-api/commit/5910404c9bd08ccd113b3bd0aff274c4a7b62efc))

*  #150: Fix test failures due to refactor ([`9ed2694`](https://github.com/ral-facilities/datagateway-api/commit/9ed26940fdeb668ebb1e573dd7d6d4e7eab162c5))

*  #150: Refactor creation of investigation test data ([`7aae8c8`](https://github.com/ral-facilities/datagateway-api/commit/7aae8c8bf9a9a1dd5922c9c13ad4908d96f3eafa))

*  #150: Use one-off session ID for logout test

- Once this test had completed, any tests afterwards using the icat_client fixture (or valid_credentials_header) would fail because those credentials had been deleted from icatdb ([`275cb43`](https://github.com/ral-facilities/datagateway-api/commit/275cb43d45d0c23a6d46367230ec44d0359c36c0))

*  #150: Simplify icat_query fixture ([`25f2282`](https://github.com/ral-facilities/datagateway-api/commit/25f22825c875fba0506c9d3d67e6ee423ebabf80))

*  #150: Add invalid tests for ISIS specific endpoints ([`1470b22`](https://github.com/ral-facilities/datagateway-api/commit/1470b2218650070cd7c7682eacee1d4a867d171d))

*  #150: Add session handling tests for ICAT backend ([`861b4f8`](https://github.com/ral-facilities/datagateway-api/commit/861b4f8ac3f57e71d50346a964dd1ce7c8a5965a))

*  #150: Add tests to check all endpoints exist and have correct HTTP methods on them ([`79bdbbe`](https://github.com/ral-facilities/datagateway-api/commit/79bdbbe4f8e4c768127a3e05468fc1a112032af1))

* Merge pull request #179 from ral-facilities/feature/update-swagger-genaration-in-readme-#134

Update Swagger Generation Section in README.md ([`5125106`](https://github.com/ral-facilities/datagateway-api/commit/5125106e000418b5725183dc2f177c354bad2ae6))

* Merge pull request #174 from ral-facilities/feature/make-swagger-yaml-stay-same-on-startup

Make swagger YAML stay the same on startup ([`58f995b`](https://github.com/ral-facilities/datagateway-api/commit/58f995befad845c8a0fc0a471dff8fa24563e809))

*  #150: Move endpoint tests to their own files/classes ([`ba59926`](https://github.com/ral-facilities/datagateway-api/commit/ba5992645411fd16a12d4432c22e083dc3d2256b))

*  #150: Add test to create single investigation

- Also remove assertion for data deletion in these tests - I&#39;ve changed the name of the data used in these tests so they don&#39;t have an impact on later tests, so there&#39;s no need to highlight any failures in data deletion ([`b16098e`](https://github.com/ral-facilities/datagateway-api/commit/b16098e4c4f2663d0beac1202d0763863397359b))

*  #150: Add invalid tests for data creation ([`e1f07b7`](https://github.com/ral-facilities/datagateway-api/commit/e1f07b7362161ff5300068d95cbff9b4dcac7c68))

*  #150: Add valid test for data creation ([`e358ec7`](https://github.com/ral-facilities/datagateway-api/commit/e358ec7d8b37498e9c422ba7bdf46a1dd7e38b10))

*  #150: Fix data creation ([`ce048da`](https://github.com/ral-facilities/datagateway-api/commit/ce048da69af5012775cfffbc00563e4e062ffa41))

*  #150: Add pytest plugin to improve assertion diffs ([`9edd0e9`](https://github.com/ral-facilities/datagateway-api/commit/9edd0e92e2b833d25fb9afd24e08a31091d5b195))

*  #150: Add tests for DELETE endpoints ([`03c7c8f`](https://github.com/ral-facilities/datagateway-api/commit/03c7c8fd8230b2e15e03e723d3c39630ff45970e))

*  #150: Add tests for no result requests

- This was trying to cover 404s but I&#39;m not sure how I&#39;d get a count query to 404.. ([`a2fd644`](https://github.com/ral-facilities/datagateway-api/commit/a2fd64413e3057a60ad6df4e5cbfa3304bd78c6f))

*  #150: Add more invalid tests for update endpoint ([`bead8cf`](https://github.com/ral-facilities/datagateway-api/commit/bead8cfd5a10d2214601a57cb25ae7f8fc983c45))

*  #150: Change ICATValidationError to raise a BadRequestError

- An exception raised as an alternative to the database going into an invalid state will usually be due to invalid user input
- This fixes the failing test created in the previous commit ([`ba62e44`](https://github.com/ral-facilities/datagateway-api/commit/ba62e445df879fa7b55eb3c5e1cd7c3487b7fb8a))

*  #150: Add invalid update by ID test

- Currently fails, request gets a 500, not a 400 despite the user input actually being the issue ([`451e4d7`](https://github.com/ral-facilities/datagateway-api/commit/451e4d713db29f3b3a160fc827c2526fa70f3f1c))

*  #150: Modify existing test to actually point to an update by ID endpoint

- I got the function names mixed up when originally doing that function... ([`6477491`](https://github.com/ral-facilities/datagateway-api/commit/6477491be0f8f3d90cb4620c7f8b9764a9ec6eda))

*  #150: Add invalid test for data updates ([`510943e`](https://github.com/ral-facilities/datagateway-api/commit/510943e94f9dfa9eae5aabdc61a7221064db054a))

*  #150: Add tests for PATCH endpoints

- Single and multiple update tests ([`fc7f3a1`](https://github.com/ral-facilities/datagateway-api/commit/fc7f3a15063bedd11cffd9366104c85e60ac13aa))

*  #150: Add test for skip &amp; limit filter merge ([`fdafb7a`](https://github.com/ral-facilities/datagateway-api/commit/fdafb7a79764919286a959cdc83fd9168158c326))

*  #150: Add fixture to inject multiple investigation results

- Add test to utilise said fixture
- Add invalid test ([`9c3ece5`](https://github.com/ral-facilities/datagateway-api/commit/9c3ece577a9610792e58180fadaff6e7b6ccd9d9))

*  #150: Add update test

- Added some logging to the API to make logging a bit better ([`9e0c56b`](https://github.com/ral-facilities/datagateway-api/commit/9e0c56b93e458b89bc366130c0d3dc7d0813b72b))

*  #150: Add tests for valid GET requests

- Test to see if all endpoints have been added to the API failed, hence the block comment around it ([`833f8e9`](https://github.com/ral-facilities/datagateway-api/commit/833f8e9787a752d7d37b4d4f13ff510ffaab0628))

*  #150: Add fixture for flask test app ([`00923bd`](https://github.com/ral-facilities/datagateway-api/commit/00923bd59227a981b18f546e897b8257cb8cf726))

*  #150: Add fixture to return auth header ([`08b8fb6`](https://github.com/ral-facilities/datagateway-api/commit/08b8fb6ecf9ee4316af408a99d9c8fc0c75d2b68))

*  #150: Add test to break a query ([`6de60c7`](https://github.com/ral-facilities/datagateway-api/commit/6de60c71c7c5bd4bccd7341128c3e20c49dca481))

*  #150: Add function to remove ICAT meta attributes and new test ([`367eebb`](https://github.com/ral-facilities/datagateway-api/commit/367eebb246f37ac65fb656a17abcfe7aead7a6e9))

*  #150: Correct argument case ([`df48005`](https://github.com/ral-facilities/datagateway-api/commit/df48005ebefbc3efa12ec1592085ff85ec0e1b55))

*  #150: Rename pytest fixture for ICAT data injection ([`a3c16e1`](https://github.com/ral-facilities/datagateway-api/commit/a3c16e14117b1ac91c2da5ee29e59ce6b4ce6cd1))

*  #150: Fix failing filter tests

- This adds validation on skip and limit values on the respective filters ([`ebf8b2e`](https://github.com/ral-facilities/datagateway-api/commit/ebf8b2e0e6055a7c70adb6c1ba1ebb720def7c96))

* Merge pull request #176 from ral-facilities/test-existing-bug-issues

Make Distinct Field Filters Apply Correctly on ISIS Endpoints ([`eadd9fc`](https://github.com/ral-facilities/datagateway-api/commit/eadd9fc863e53beab77ea90fab65782e417fa700))

*  #145: Add attempt to restore old data if an update goes wrong

- This is a solution to a comment made on the PR for this branch
- This solution doesn&#39;t need to be applied to update by ID because if an error occurs there, there&#39;s no other data that could possibly be updated ([`3224a27`](https://github.com/ral-facilities/datagateway-api/commit/3224a277ab03e3beeda74e1afe167ae90e4e5212))

*  #145: Ensure the database remains in a similar state to what it started in if POST returns an error

- Similar purpose to the previous commit but expanded so changes are &#39;rolled back&#39; if an exception occurs on the .create() ([`b6395e5`](https://github.com/ral-facilities/datagateway-api/commit/b6395e5b1737b126b93e8d11af14f604bf3103fb))

*  #145: Ensure updated data is pushed at the end of the request

- This will prevent an issue where you&#39;re updating multiple pieces of data and the request returns a 400, you don&#39;t know which pieces of data have been updated ([`ed562e8`](https://github.com/ral-facilities/datagateway-api/commit/ed562e8940c0838a26e023b1f76312466d9bf1f5))

*  #150: Add skeleton classes for remaining ICAT backend tests ([`07e42ec`](https://github.com/ral-facilities/datagateway-api/commit/07e42ec8527b3db951e9ca92a4cdfa9ec63a4f4c))

*  #150: Add beginning of tests for ICATQuery

- This commit also includes a skeleton for the remaining tests for this class ([`d7b88dd`](https://github.com/ral-facilities/datagateway-api/commit/d7b88dd049726b76aed87d4c276b8a5d81c3bcbb))

*  #150: Add way of injecting data into ICAT for testing endpoint and ICATQuery

- This fixture also removes the data from ICAT at the end of the test ([`5444bd5`](https://github.com/ral-facilities/datagateway-api/commit/5444bd59d0fac9e185bb470f8939daaeacb4e7b6))

*  #150: Ensure list flatten always returns the list in the same order

- That function would return the elements of a list in different order each time (despite identical inputs each time) so this could prove more difficult to test ([`7bf1141`](https://github.com/ral-facilities/datagateway-api/commit/7bf11413cabbb3560b826828b0eb51d287323c62))

* Merge pull request #187 from ral-facilities/feature/disable-openapi-yaml-write-#183

Disable openapi.yaml Generation ([`2caae79`](https://github.com/ral-facilities/datagateway-api/commit/2caae797bb10e54c756b944669409d38ea76364c))

* Merge pull request #188 from ral-facilities/feature/configure-log-file-location-#182

Allow Log File Location to be Configurable ([`463e3db`](https://github.com/ral-facilities/datagateway-api/commit/463e3db89abaa01cd6778806152e828ec23a2430))

* Merge pull request #159 from ral-facilities/feature/add-issue-templates-#133

Adding issue/PR templates ([`7fffd18`](https://github.com/ral-facilities/datagateway-api/commit/7fffd18536e12815d80607323708fc8a182c6d82))

*  #133: Add template for which issue a PR will automatically close ([`de159f8`](https://github.com/ral-facilities/datagateway-api/commit/de159f8a02e2b85459d69269b02f5cdccd35c4ef))

*  #148: Make suggested changes to distinct attribute mapping ([`84164c9`](https://github.com/ral-facilities/datagateway-api/commit/84164c9282c8c49297b044d9baf9c3c488b0c82f))

*  #150: Add tests for filter handler ([`e621f42`](https://github.com/ral-facilities/datagateway-api/commit/e621f423e38a0538ae51cd9fa66ab84be6b299e9))

* Merge branch &#39;master&#39; into feature/test-multiple-backends-#150 ([`9625cc1`](https://github.com/ral-facilities/datagateway-api/commit/9625cc1137bcaf7f840b24d991fb8b9ada93ab55))

*  #150: Add test for backend creation ([`55397e5`](https://github.com/ral-facilities/datagateway-api/commit/55397e56a1090ee35ac9fcb81b5724326cfbbe91))

*  #150: Add tests for ICAT limit filters ([`f4ef19f`](https://github.com/ral-facilities/datagateway-api/commit/f4ef19f4e898406515f58b24d252393d744787c6))

*  #150: Add tests for ICAT skip filters ([`34d46ba`](https://github.com/ral-facilities/datagateway-api/commit/34d46bacc9c7736c3f654ff63eedc4c1ee0716e6))

*  #150: Add tests for ICAT include filters ([`7fe62ff`](https://github.com/ral-facilities/datagateway-api/commit/7fe62ff135c710626fe6c5915635fc1fe30c9a7e))

*  #150: Add tests for ICAT distinct filters ([`90f3b4b`](https://github.com/ral-facilities/datagateway-api/commit/90f3b4b684607c9b0bc012ee9f47681b467ccd18))

*  #150: Add tests for ICAT order filters ([`3c350ee`](https://github.com/ral-facilities/datagateway-api/commit/3c350ee1a2a6e772f54c9ac4c9ee7e6725888065))

*  #150: Add tests for ICAT where filters ([`d5b189b`](https://github.com/ral-facilities/datagateway-api/commit/d5b189b08b85b47aa8504c775ea938878b074fa6))

*  #150: Add pytest fixtures for filter testing

- Since they&#39;re placed in conftest.py, pytest will automatically pick these up, they don&#39;t need to be imported into the places I use them in ([`71720d0`](https://github.com/ral-facilities/datagateway-api/commit/71720d0e657703550701041192fcd3ff3442f543))

*  #150: Combine config test username and password

- This will make it more convenient to use through the tests in the repo ([`572e89c`](https://github.com/ral-facilities/datagateway-api/commit/572e89cd36db1cfe15857c7e40da0c7e3df3c402))

*  #150: Add tests for test configuration options ([`7455c48`](https://github.com/ral-facilities/datagateway-api/commit/7455c480f88aa255322cff29258ca4562c101b1f))

*  #150: Add configuration options required for repo&#39;s tests

- This commit also adds getters in config.py ([`57fcd68`](https://github.com/ral-facilities/datagateway-api/commit/57fcd682dbe17532f37b3850cb7937b9c3a0e4fb))

*  #150: Add pytest-cov to the repo

- nox -s tests -- --cov is a good starting point for usage
- I&#39;m not sure how much I trust the output - there&#39;s around half coverage for both DB &amp; ICAT backend&#39;s helper files, even though I&#39;ve currently got the ICAT backend configured... ([`257082e`](https://github.com/ral-facilities/datagateway-api/commit/257082e3d517d58c468022bf66ad7f834a8430a6))

*  #150: Add tests for config ([`d1b045f`](https://github.com/ral-facilities/datagateway-api/commit/d1b045fbeb9734169c92c9cdd39d6d846fe71590))

*  #150: Make config file path configurable

- This will make testing the configuration easier since you cannot guarantee what the contents of config.json will be
- Default is what it was before ([`230eaca`](https://github.com/ral-facilities/datagateway-api/commit/230eaca266bb124f44c26f01151f2bf5a6c47dbc))

*  #150: Add tests for DateHandler ([`343f8d4`](https://github.com/ral-facilities/datagateway-api/commit/343f8d4fe609417bc51245cde9fce99126bf7b9c))

* Merge branch &#39;feature/fix-code-linting-#184&#39; into feature/test-multiple-backends-#150 ([`b655de1`](https://github.com/ral-facilities/datagateway-api/commit/b655de1ec2ca0f2a6905698177c4f9fef5ddab7f))

*  #184: Fix previous changes to log.exception() lines ([`b752c85`](https://github.com/ral-facilities/datagateway-api/commit/b752c854b16d1b4774ab47468175655918eefd9b))

*  #150: Add nox &#39;tests&#39; session

- This will run the discovered unit tests in multiple versions of Python (unless nox is specified with -p [version_num] which is probably what I&#39;ll do for the majority of the time, just useful to test multi-version compatability) ([`29f8111`](https://github.com/ral-facilities/datagateway-api/commit/29f811127ad4885b115214da61e985e829b01508))

*  #150: Add pytest to dev dependencies

- This also updates a couple of dependencies as marked by safety, which didn&#39;t get merged in from a recent git merge ([`96b3728`](https://github.com/ral-facilities/datagateway-api/commit/96b37283cc1ecdb2f4e652477b85256f89a30e86))

* Merge branch &#39;feature/configure-log-file-location-#182&#39; into feature/test-multiple-backends-#150 ([`04f25f1`](https://github.com/ral-facilities/datagateway-api/commit/04f25f1878c57fc4784fb7dd3e6721844ca71794))

*  #182: Allow log file to be configured

- In production, this will be used to store the API&#39;s logs in /var/log/
- Also remove an unused variable that I noticed ([`45b5896`](https://github.com/ral-facilities/datagateway-api/commit/45b5896be4c0201b1704a719c6e59a4706781b80))

*  #182: Add log location configuration option ([`7723d69`](https://github.com/ral-facilities/datagateway-api/commit/7723d69f25b53725871e22608478108ba2bee5e7))

*  #184: Update dependencies with security issues found by safety ([`82aa40d`](https://github.com/ral-facilities/datagateway-api/commit/82aa40df10ee47ca4bdc56c5c7e214019632196a))

*  #183: Allow openapi.yaml generation to be disabled

- This will mean this configurable parameter can be disabled when running the API in production, thereby avoiding any issues with read-only directories ([`1596f73`](https://github.com/ral-facilities/datagateway-api/commit/1596f73b73187d131c18cb36d0f366be65818c9b))

*  #184: Make certain function less complex

- I&#39;ve had to increase the max complexity in .flake8 because there&#39;s not much you can do with a couple of the functions. Still made some improvements though! ([`a694129`](https://github.com/ral-facilities/datagateway-api/commit/a6941295d6e9ef1060a734d03b1b54e21dc98c41))

*  #184: Fix G200 from flake8-logging-format

- This linting status code is regarding passing an exception object directly into log.exception() ([`af816bf`](https://github.com/ral-facilities/datagateway-api/commit/af816bf12b5c26076531ed0839646109a7338c65))

*  #184: Ensure all test classes names use PascalCase ([`de6255d`](https://github.com/ral-facilities/datagateway-api/commit/de6255d5f21dff0784bbbced3c50fea00d98ce35))

*  #184: Fix misc. linting issues ([`ed8aa34`](https://github.com/ral-facilities/datagateway-api/commit/ed8aa343f6c1290de50e4c000197e2b68bf0b53d))

* Merge pull request #169 from ral-facilities/feature/where-filter-included-columns-#144

Allow WHERE Filter to use Included Fields for Python ICAT Backend ([`8e3e161`](https://github.com/ral-facilities/datagateway-api/commit/8e3e161fb10ad9c02f1dd68b140395d2141b5ae8))

*  #184: Add file specific ignore for &#39;random&#39; usage

- S311 (from Bandit) states &#34;Standard pseudo-random generators are not suitable for security/cryptographic purposes.&#34;. The generator script doesn&#39;t generate data that would be vulnerable to security (no keys or anything of that nature is created using the random library) hence this status code is ignored ([`33193de`](https://github.com/ral-facilities/datagateway-api/commit/33193de961d7294b3571feafa53688420f769c44))

*  #184: Rebuild openapi.yaml file to reflect recent changes ([`93e1e3b`](https://github.com/ral-facilities/datagateway-api/commit/93e1e3bf851d3a96349a6b1242d838dfea54a63f))

*  #184: Edit docs to reflect Nox session renaming ([`4846a3d`](https://github.com/ral-facilities/datagateway-api/commit/4846a3d3e270fa6d1f9d2ab54c3dd87e72946ade))

*  #184: Ensure every line meets 88 character length

- This is the suggested line length defined by Black, which flake8 is configured to also follow ([`81671f4`](https://github.com/ral-facilities/datagateway-api/commit/81671f4d4fd94b956a7976ed6a788e40a1fa661a))

*  #184: Avoid catching bare exceptions ([`9b85ea7`](https://github.com/ral-facilities/datagateway-api/commit/9b85ea7be70d09289f4066e0943f300e4b5c568e))

* Merge pull request #168 from ral-facilities/feature/icat-include-filter-#143

Implement Include Filter for Python ICAT Backend ([`f4e3e6c`](https://github.com/ral-facilities/datagateway-api/commit/f4e3e6c554b57aceb9715267cbc9ce11aee35ffa))

*  #184: Remove reassignment of Python builtins ([`51fabee`](https://github.com/ral-facilities/datagateway-api/commit/51fabee7c47a4ca782a9a29230785a5812b57bfa))

*  #184: Reorder import statements ([`ffe23fe`](https://github.com/ral-facilities/datagateway-api/commit/ffe23fe7d7c16e18263211b98b38280720097672))

*  #184: Fix local import names

- This is so flake8 can correctly detect which import statements are bringing in local code, so said statements can be ordered in a consistent style ([`3b208a0`](https://github.com/ral-facilities/datagateway-api/commit/3b208a0a2c54574621f496957e1bc1f680cb1704))

*  #184: Add trailing commas to meet flake8 output ([`a9f3b08`](https://github.com/ral-facilities/datagateway-api/commit/a9f3b08fca2e0214af2ef804bf385e59f0cbb20f))

* Merge pull request #156 from ral-facilities/feature/fix-session-handling-#135

Fix session handling for ICAT backend ([`bf64e9b`](https://github.com/ral-facilities/datagateway-api/commit/bf64e9b2beb08dd47ef1d2d174ff0567d7cb6450))

*  #165: Change README&#39;s project structure ([`0f232dd`](https://github.com/ral-facilities/datagateway-api/commit/0f232dd0f56448a56067fa9a66f2edbc16abe280))

*  #165: Add dev environment creation summary ([`e32543b`](https://github.com/ral-facilities/datagateway-api/commit/e32543be39dbeb82c9b8d5364b0d35daf6ab22af))

*  #165: Make small formatting changes to README ([`b4aa172`](https://github.com/ral-facilities/datagateway-api/commit/b4aa17253ecdf354938141e250f156a35e719272))

*  #165: Add documentation to the new dev environment created by the changes on this branch ([`4077f10`](https://github.com/ral-facilities/datagateway-api/commit/4077f1051fc47557ddce75bc8611be5f6d299244))

*  #165: Remove unused requirements files

- These files have been replaced by the use of Poetry to store the API&#39;s dependencies ([`be6e229`](https://github.com/ral-facilities/datagateway-api/commit/be6e2298e7564c11c6995c085c8fbd911e93d219))

*  #165: Add flake8 plugins to Poetry and nox session ([`b28446c`](https://github.com/ral-facilities/datagateway-api/commit/b28446c7d391f04477e1c51d20eae4207101c728))

*  #165: Update version of standard pre commit hooks used ([`21dcee2`](https://github.com/ral-facilities/datagateway-api/commit/21dcee213562680c81aaeeba3532c38665e3b053))

*  #165: Add additional pre-commit hooks ([`14276a4`](https://github.com/ral-facilities/datagateway-api/commit/14276a4eefd9aacf94f4a97c5c98a8d438627866))

*  #165: Apply pre-commit hooks to all files
- Done by `pre-commit run --all-files` ([`7e7154c`](https://github.com/ral-facilities/datagateway-api/commit/7e7154c8f2bf8b6df8438be778e9498b8954c269))

*  #165: Add pre-commit hook config ([`348acf1`](https://github.com/ral-facilities/datagateway-api/commit/348acf15f9086528d6f287be963aaff3f602897c))

*  #165: Allow dependencies to be installed according to Poetry&#39;s dependencies

- This will help keep consistent versions of flake8 etc being installed between developers, to prevent incosistent linting/safety outputs ([`b890d98`](https://github.com/ral-facilities/datagateway-api/commit/b890d981a5c7f1bc83769606e70ffb973b797e57))

*  #165: Add flake8 config changes needed from additional plugins used ([`a478ab1`](https://github.com/ral-facilities/datagateway-api/commit/a478ab113856b4cefa0e5910b9303056076ca7b6))

*  #165: Add .python-version to gitignore ([`90badd6`](https://github.com/ral-facilities/datagateway-api/commit/90badd6af2b070386b846b9236101e61644a6ab9))

*  #165: Add Poetry configuration ([`baa1768`](https://github.com/ral-facilities/datagateway-api/commit/baa17685e617caf5ae58330e2b01732abb2feda3))

*  #165: Edit target for config file due to previous commit ([`5761dc6`](https://github.com/ral-facilities/datagateway-api/commit/5761dc666e0bbbd123942ed4e18efbb1267a93fd))

*  #165: Make this repo pip installable

- As suggested by Alan, a top level directory is required to make this repo ready for production use. This is also required for Poetry ([`9796ddf`](https://github.com/ral-facilities/datagateway-api/commit/9796ddffeea4313e1dbd9d76f6573571ae274529))

*  #165: Install Black before running the command ([`d4911c5`](https://github.com/ral-facilities/datagateway-api/commit/d4911c5fe9cd51ff587dc2f50c5bed79f9d8d2cc))

*  #165: Add skeleton linting functionality

- As per Hypermodern Python guide ([`fb3f320`](https://github.com/ral-facilities/datagateway-api/commit/fb3f3204c1fbc52b65528282965662e323f0d636))

* Merge branch &#39;feature/remove-sql-dependency-from-backends-#154&#39; into feature/test-multiple-backends-#150 ([`79e6e88`](https://github.com/ral-facilities/datagateway-api/commit/79e6e8858c18185a70a9fc7904207d529e903e5c))

*  #147: Override handle_error on extended Api class ([`511a8ef`](https://github.com/ral-facilities/datagateway-api/commit/511a8ef6c26625dd7f9289a5a101962b9a4b3b3f))

*  #154: Add rebuilt openapi.yaml due to changes made for this issue ([`66d0ab1`](https://github.com/ral-facilities/datagateway-api/commit/66d0ab19ba6e003433bfdf5e1500e120ce209769))

*  #154: Convert get_python_icat_entity_name() to a camel case only returning function

- Due to removing the SQL dependency, there is no use for the primary aim of this function. As a result, it&#39;s now only used once in this repo. It has been renamed (and modified) since the function only returns a camelCase version of its input ([`08ee87d`](https://github.com/ral-facilities/datagateway-api/commit/08ee87d00847ffb0a8e1514a096b56e0f852d27b))

*  #154: Adapt Swagger docs for entity_type

- This commit re-enables the Swagger docs and adapts them for the non-backend specific contents of entity_type
- This also fixes some issues where example values wouldn&#39;t show in PATCH and POST endpoints ([`ac095e1`](https://github.com/ral-facilities/datagateway-api/commit/ac095e1fb7570a98549b5e86ac530c27df6584ac))

*  #154: Misc. code formatting changes made by Black ([`c7cc4c1`](https://github.com/ral-facilities/datagateway-api/commit/c7cc4c1b107899fb333d3614e2e0a2fc55695682))

*  #154: Make ICAT backend entity_type non-backend specific
- Same aim as the previous commit, but for the Python ICAT backend this time ([`bc17502`](https://github.com/ral-facilities/datagateway-api/commit/bc175029f7ed8eff82a022e20bd9aa1362eb67a0))

*  #154: Make DB backend entity_type non-backend specific
- Instead of parsing an instance of something like `common.database.models.USER`, the field name is parsed into the DB backend function instead, and an instance of that entity is created in the DB backend functions, to make that data parsing non-backend specific ([`06522be`](https://github.com/ral-facilities/datagateway-api/commit/06522be734e658c1b711a815dca7c6996c8471bd))

*  #154: Disable most of the Swagger generation for dev purposes

- This will be modified later on ([`f0ff0a1`](https://github.com/ral-facilities/datagateway-api/commit/f0ff0a1982708aee83abb8bbb9f165211412242f))

*  #154: Change endpoints dict to contain field name

- This is a change from containng an instance of the entity model, to make entities parsed round the API non-backend specific ([`669a558`](https://github.com/ral-facilities/datagateway-api/commit/669a55886992a907ecb8af21c954bc9a8edc93ee))

*  #154: Add function to get instance of DB model entity from a name ([`17f9eec`](https://github.com/ral-facilities/datagateway-api/commit/17f9eec1dce4b2dca584b1c4c6e7b0d51a074eb0))

*  #147: Misc. code formatting changes ([`80943ad`](https://github.com/ral-facilities/datagateway-api/commit/80943adebfdb2ffa3ae8677d1f6d327197e5f136))

*  #134: Misc. changes of existing sections in README

- Also updated `requirements.in` (with a freshly compiled `requirements.txt`) to reflect the requirement of Python ICAT ([`da21adb`](https://github.com/ral-facilities/datagateway-api/commit/da21adb735c842b72da6bcb4e6806e286f974786))

*  #134: Edit Swagger doc section of README to reflect changes in generation ([`c2e8099`](https://github.com/ral-facilities/datagateway-api/commit/c2e8099f00861e3c61cf945415091ecc03131c3b))

*  #134: Make file adhere to Black&#39;s 88 character/line rule

- Since the Python files in the repo adhere to this limit, it seems sensible that the README file also following this formatting rule where possible ([`efb732c`](https://github.com/ral-facilities/datagateway-api/commit/efb732c9c5ba670e10cb7edbdf584649f4604094))

*  #166: Add modified OpenAPI YAML from recent modifications ([`588158c`](https://github.com/ral-facilities/datagateway-api/commit/588158c3e20de986baaa74a4a2141175ca7a2209))

*  #166: Add examples to match all possible WHERE filter operations

- Also modified description to aid users if they&#39;re having issues getting example values to work ([`2724911`](https://github.com/ral-facilities/datagateway-api/commit/27249111d892468e9b659e7a76e780e0bbd4e1c0))

*  #166: Add not equal to DB where filter

- This will match the functionality seen in the Python ICAT version of the WHERE filter, so I can put an example of this operation in the Swagger docs ([`6666f29`](https://github.com/ral-facilities/datagateway-api/commit/6666f292d1a412d244f809b8495e4f8bde98632d))

*  #166: Adapt example filter inputs for ICAT backend ([`7d0205c`](https://github.com/ral-facilities/datagateway-api/commit/7d0205c8e3ea8c4d5715e972a852234222e3ec02))

*  #166: Fix Swagger data parsing for entity by ID endpoints ([`fe9623b`](https://github.com/ral-facilities/datagateway-api/commit/fe9623b9f618a43ea6772f5094190209916ced2c))

*  #154: Move session_manager to common.database

- This is code for the database backend, so it seems fitting to move it there
- This commit also includes the changes in imports and updates to documentation ([`c2e7497`](https://github.com/ral-facilities/datagateway-api/commit/c2e7497329cf264a92f65fa13c238e9ef85a0672))

*  #154: Move common.models to common.database

- The only model in common.models was for the database backend (there&#39;s no model for the Python ICAT backend), hence the change
- This commit also includes the changes required to correctly import the file from the new location
- Updated the file tree in the README ([`56b7606`](https://github.com/ral-facilities/datagateway-api/commit/56b760615dd37bcf90540e36eaf18387bfa9d424))

*  #162: Add Postman Collection compiled for ICAT backend

- This is a Postman Collection I&#39;ve built up over the past few months, containing 320 requests. The requests are aimed at the Python ICAT backend (with query params created for that backend) but can be used for the DB backend by changing parameters to SNAKE_CASE where needed. The collection has been exported as v2.1 and is ready to be imported into Postman ([`cf83b3f`](https://github.com/ral-facilities/datagateway-api/commit/cf83b3f2bc88e4b26064bfe552b5446474412962))

*  #114: Remove logging used for development purposes ([`7aa794e`](https://github.com/ral-facilities/datagateway-api/commit/7aa794e120f9a8ec9996a1c93aec25941c994379))

*  #114: Remove isis_endpoint attribute from ICATQuery

- Due to the previous commit there is now no need for this parameter ([`c9e80c0`](https://github.com/ral-facilities/datagateway-api/commit/c9e80c0c50743c43543604f0f0fb110e32625b58))

*  #114: Allow distinct filters to correct apply to ISIS endpoints ([`5e19893`](https://github.com/ral-facilities/datagateway-api/commit/5e198933d4855dbd400d5445de7c24c37a8e4492))

*  #164: Add logging throughout Python ICAT backend ([`4aa1331`](https://github.com/ral-facilities/datagateway-api/commit/4aa13315a26f74a818acc186718f7bb13921cd45))

*  #173: Add OpenAPI YAML file ordered alphabetically ([`537cafc`](https://github.com/ral-facilities/datagateway-api/commit/537cafc3a7650e41a9ca954fabb18ccaf677c4ed))

*  #173: Order OpenAPI YAML request types alphabetically

- Things like get, patch, post, delete etc. weren&#39;t alphabetically ordered as changing the order of the YAML file on startup ([`88c623a`](https://github.com/ral-facilities/datagateway-api/commit/88c623a1c507694b2d6b7f34025df933687759bf))

*  #146: Add to ICATQuery docstring ([`adcb7a6`](https://github.com/ral-facilities/datagateway-api/commit/adcb7a6d3ed9e3414eba22efc4b55591a5ec38c6))

*  #146: Add logging for ISIS endpoints ([`1652048`](https://github.com/ral-facilities/datagateway-api/commit/16520486550a9a4051c1297c99106f22c7a159ab))

*  #146: Add DISTINCT aggregate to all ISIS specific queries

- Testing on dev ISIS ICAT determined this was needed ([`b52634a`](https://github.com/ral-facilities/datagateway-api/commit/b52634aed38be8a7c9ad5df1181c8ba9e351197c))

*  #146: Implement second ISIS specific endpoint ([`e28c39b`](https://github.com/ral-facilities/datagateway-api/commit/e28c39b61ce6d2bbc02834e510b70290b7605659))

*  #146: Apply count query flag logic to second ISIS endpoint

- It should be noted that the affected endpoint doesn&#39;t currently do anything ([`8d1dba2`](https://github.com/ral-facilities/datagateway-api/commit/8d1dba20c01b1f7669f6427775e1448bdfdf7fec))

*  #146: Add count functionality for 1st ISIS endpoint

- Makes use of the existing function but adds a flag to detect whether the function should be used as a count query or not ([`68bd282`](https://github.com/ral-facilities/datagateway-api/commit/68bd282312ad4f81bcd8d8d9fa4d5d19674f719f))

*  #146: Fix missing logging import ([`5944932`](https://github.com/ral-facilities/datagateway-api/commit/5944932f6a90f9ba8b9ce48d51e8a6b727def95d))

*  #146: Correct facility cycle ISIS endpoint

- This ensures the correct DB tables are joined together, to match the output of the request in the DB backend. This has been compared with a query from TopCat and also gives an identical output for my test data ([`be35d4b`](https://github.com/ral-facilities/datagateway-api/commit/be35d4b8fc27e899274540c1bac05814cba0a5ab))

*  #146: Fix issue with RHS of where filters being a reference

- This fixed is used for the ISIS endpoints ([`397602d`](https://github.com/ral-facilities/datagateway-api/commit/397602dc395444556604833e5f6ee9a0be1b35ec))

*  #146: Add flag for ISIS endpoints in ICATQuery

- ISIS endpoints require use of the DISTINCT aggregate, which is different to the DISTINCT filter in this API ([`10679bb`](https://github.com/ral-facilities/datagateway-api/commit/10679bb999615cc590531882122d54b1f98a2e3e))

*  #146: Add skeleton to an ISIS endpoint

- This endpoint does not work currently, there are issues with speech marks in WHERE filter of the startDate conditions and a DISTINCT aggregate needs to be added (with a flag in ICATQuery to mark an ISIS endpoint so the aggregate doesn&#39;t behave like a distinct filter - these are two different things) ([`b6333e9`](https://github.com/ral-facilities/datagateway-api/commit/b6333e9f8917e6a49bfc87ddaa5f519e5d4afbb8))

* Merge branch &#39;feature/remaining-icat-endpoints-#145&#39; into feature/isis-specific-endpoints-icat-#146 ([`eb2382d`](https://github.com/ral-facilities/datagateway-api/commit/eb2382d84b5a7c53e420021c161305c2c91ab282))

*  #146: Change where include filter data is referenced ([`a089db4`](https://github.com/ral-facilities/datagateway-api/commit/a089db4f148c6838596263b1927177eeb55134f8))

* Merge branch &#39;feature/distinct-filter-included-columns-#148&#39; into feature/remaining-icat-endpoints-#145 ([`3702123`](https://github.com/ral-facilities/datagateway-api/commit/3702123dd976bf482b48198690ca9194cc79973c))

*  #148: Fix ImportError ([`88908f4`](https://github.com/ral-facilities/datagateway-api/commit/88908f45f98e2cdbd67f0a56c875da7963d5139f))

* Merge branch &#39;feature/distinct-filter-included-columns-#148&#39; into feature/remaining-icat-endpoints-#145 ([`c1e5480`](https://github.com/ral-facilities/datagateway-api/commit/c1e5480b906666086ea7098fba9ff30f828b595b))

*  #146: Add docstrings to each of the ISIS endpoint helper functions ([`2c8842c`](https://github.com/ral-facilities/datagateway-api/commit/2c8842ca4493d663bcab086090fc7dddb021438e))

*  #146: Create skeleton functions for ISIS endpoints for ICAT backend ([`1ee4f0e`](https://github.com/ral-facilities/datagateway-api/commit/1ee4f0ef50cad340b3f3aebad7fd6ab27b72771d))

*  #146: Fix ISIS endpoints for DB backends

- The function calls were to functions that didn&#39;t exist in the backend files, so I&#39;ve corrected them so they do exist and also slightly renamed them during this change ([`90a2e28`](https://github.com/ral-facilities/datagateway-api/commit/90a2e28c59ce673b5fe52399a5ed6ce6707b2adb))

* Merge branch &#39;feature/distinct-filter-included-columns-#148&#39; into feature/remaining-icat-endpoints-#145 ([`6de7c73`](https://github.com/ral-facilities/datagateway-api/commit/6de7c73edc44da440bef21e7b5eecdd88bedab85))

* Merge branch &#39;feature/icat-include-filter-#143&#39; into feature/distinct-filter-included-columns-#148 ([`8b6cfad`](https://github.com/ral-facilities/datagateway-api/commit/8b6cfadcb191c9742771c61ee5eb3ded6556d28b))

* Merge branch &#39;master&#39; into feature/icat-include-filter-#143 ([`a023678`](https://github.com/ral-facilities/datagateway-api/commit/a023678cc4468fcea1631ed260b266ffb83668b5))

*  #145: Remove logging statement from development work ([`8e046f6`](https://github.com/ral-facilities/datagateway-api/commit/8e046f65ba72da282c8f117fa690ae8741e5df05))

*  #145: Move filter-specific functions to FilterOrderHandler

- This will help clean up common.icat.helpers and move filter-specific functions to the relevant file
- This commit also adds a function that calls other functions in its class to reduce code duplication
- This is a &#39;leave the code in a better state than you found it&#39; kind of commit ([`8c8a241`](https://github.com/ral-facilities/datagateway-api/commit/8c8a2419b3356ff5900bbff72342c3e7779cb8c8))

*  #145: Remove return_first_value_only flag

- This functionality has been replaced with a limit filter as per the previous commit ([`2d2f4f1`](https://github.com/ral-facilities/datagateway-api/commit/2d2f4f1da70f5103d2ee461e805f00ae5e854fc8))

*  #145: Add LIMIT filter into /findone endpoints

- This helps to make these types of requests more snappy, without impacting the output ([`264c130`](https://github.com/ral-facilities/datagateway-api/commit/264c130e97a431df53954ad7eebbcc32aa228312))

*  #145: Make small changes to date handler ([`b8534e4`](https://github.com/ral-facilities/datagateway-api/commit/b8534e437f8ed26d18d1f1f52b1e4edc18987019))

*  #145: Add logging ([`1f866f1`](https://github.com/ral-facilities/datagateway-api/commit/1f866f16a7ead87ea96c50101ad50f2fa21ce0bc))

*  #145: Move date-related functions to a separate class

- In the future, these could be used by other backends so I&#39;ve moved these 3 functions into their own utility class. This change helps clean up common.icat.helpers a bit which is another reason this change has been made ([`2a88aae`](https://github.com/ral-facilities/datagateway-api/commit/2a88aaedc78e68931972064ba389dbeced9a6266))

*  #145: Add exception to be caught when creating ICAT data ([`d7741f7`](https://github.com/ral-facilities/datagateway-api/commit/d7741f74f390b92f7a95a634976af085050295ad))

*  #145: Remove unused code

- Recursing through related objects is no longer required ([`be3c797`](https://github.com/ral-facilities/datagateway-api/commit/be3c7978fda17fe0abf501b331a0924aca5eb704))

*  #145: Deal with attributes that have MANY relationships

- This code needs to be recursed over, since multiple &#39;levels&#39; of mandatory MANY relationships don&#39;t happen currently and this results in a database related error ([`85860ff`](https://github.com/ral-facilities/datagateway-api/commit/85860ff112b19190819556d4a80ed343a9fc19a8))

*  #145: Remove parameter from str_to_datetime_object()

- I&#39;ve also made use of this in create_entities() which made me notice that said parameter wasn&#39;t used ([`5eed66e`](https://github.com/ral-facilities/datagateway-api/commit/5eed66ea64da1b3f7496f382d74c85fdb1a4bb00))

*  #145: Allow Python ICAT names to be fetched as camelCase

- This is required for created ICAT objects in Python ICAT ([`5cb5068`](https://github.com/ral-facilities/datagateway-api/commit/5cb5068c30a282ccf1cf1d92c01758a3239899d4))

*  #145: Add first implementation of POST request (create) for entities

- This has only been tested on /investigations so far, so further changes may be needed when I test on the rest of the entities ([`944b877`](https://github.com/ral-facilities/datagateway-api/commit/944b877e6d6263a1e260e40f9c7d551c7201d33c))

*  #145: Add docstring for ICAT PATCH helper function ([`b33de8a`](https://github.com/ral-facilities/datagateway-api/commit/b33de8a8834436d405c97496fa1f208e7dd46709))

*  #145: Prevent related entities from displaying in response of a PATCH request

- Related entities (i.e. includes=&#34;1&#34;) must be retrieved when updating data to avoid an IcatException which highlights that a related entity field is trying to be set to null which is invalid ([`2970dde`](https://github.com/ral-facilities/datagateway-api/commit/2970dde9478bdf9f5ab334a638a3f9f11c2cb03f))

*  #145: Add basic implementation of updating multiple entities in one request

- This works some of the time, but not all as of this commit ([`4f549bc`](https://github.com/ral-facilities/datagateway-api/commit/4f549bce1c8977831abb883c85b0cd80791794d8))

*  #145: Fix bug where GET requests without distinct filter sometimes return a 400 ([`d3a0f0b`](https://github.com/ral-facilities/datagateway-api/commit/d3a0f0bebbb9f135643fd628e2b56efe6959b876))

*  #145: Remove to_dict() conversion on PATCH entity endpoints

- Python ICAT backend doesn&#39;t need this conversion, so this has been moved into the relevant DB backend helper function ([`a4baba3`](https://github.com/ral-facilities/datagateway-api/commit/a4baba30c16f3310f763732f221903b5191c2a39))

* Merge pull request #161 from ral-facilities/feature/icat-distinct-filter-#141

Implement Distinct Filter for Python ICAT Backend ([`e419d8c`](https://github.com/ral-facilities/datagateway-api/commit/e419d8cc0ae606d1bd49ec01e8a90ffdffe1ebce))

*  #145: Implement /findone for all entities ([`0747c5b`](https://github.com/ral-facilities/datagateway-api/commit/0747c5b35a0adb93665d0135b76ff0ea36c23889))

*  #145: Fix bug on non-count queries ([`692ac0f`](https://github.com/ral-facilities/datagateway-api/commit/692ac0f4c0013dba60263634d1b7598924f227e5))

*  #145: Allow /count to work with distinct filters ([`86c6f27`](https://github.com/ral-facilities/datagateway-api/commit/86c6f27075f89620548efc8aa0f48b737391ac0c))

*  #145: Basic implementation of `/count`

- Currently breaks when you add a distinct filter so that needs fixing ([`5fd2622`](https://github.com/ral-facilities/datagateway-api/commit/5fd2622e4c008d628696154b58e2bbb485d67d9e))

*  #141: Set LIKE operator on WHERE filter to do wildcard searches

- This should allow these types of searches to provide more accurate results, where previously none could be found ([`acc9672`](https://github.com/ral-facilities/datagateway-api/commit/acc96727aa4f2be59b3336b8df44ab3871e702e4))

*  #148: Fix bug where no distinct filter is present ([`f6df659`](https://github.com/ral-facilities/datagateway-api/commit/f6df6597b7d5a32bb7e7947c5f1fdc1eee3ab324))

*  #150: Allow backends to be created for testing purposes

- Currently getting a 403 on these changes but I&#39;m not sure the code is at fault... ([`2dee8f0`](https://github.com/ral-facilities/datagateway-api/commit/2dee8f0b3881830853ef794f608f9e523cfc8e0b))

*  #150: Work out how the existing tests will work with the new test structure

- Just a few comments to help me work out what to do with the existing tests for DB backend. These will be moved to work with Pytest once the new test structure has been defined ([`db43d3d`](https://github.com/ral-facilities/datagateway-api/commit/db43d3d93b51e8629f3ca55468fc29cdd34f0294))

* Merge branch &#39;master&#39; into feature/fix-session-handling-#135 ([`f1fd838`](https://github.com/ral-facilities/datagateway-api/commit/f1fd8386ce75444fa71bf82e87e3cbd2ac208acb))

* Merge pull request #153 from ral-facilities/feature/python-icat-where-filter-#142

Change structure of Filters and Implement Basic WHERE Filter for Python ICAT backend ([`767aef1`](https://github.com/ral-facilities/datagateway-api/commit/767aef1964a714b3a41ccb8ae098861410e385e2))

*  #148: Allow distinct fields to work correctly with included columns of &gt;1 depth ([`0760556`](https://github.com/ral-facilities/datagateway-api/commit/0760556cfe5bbdba286dd3bf3f539fc94e1ab286))

*  #148: Move checking WHERE filters for distinctiveness to its own function

- This commit also moves the separation and flattening of the included field sets into its own function
- Various bits of documentation adding too
- Replace icat_query.attribute_names with a non instance variable ([`20a886d`](https://github.com/ral-facilities/datagateway-api/commit/20a886d3fed534ac8ffc907444335080b82a9fc5))

*  #148: Check that included-distinct fields have included entities in the include filter

- The appended docstring in this commit explains the change far better than the commit message.. ([`571f720`](https://github.com/ral-facilities/datagateway-api/commit/571f720d93ddc637d9278fe1b418e05b54a12cb8))

*  #148: Add docstrings and general comments ([`2a300d5`](https://github.com/ral-facilities/datagateway-api/commit/2a300d5d2f5a8cb6ef668f75237fe57a963708c3))

*  #148: Move duplicated code to its own function

- This involves moving the distinct fields belonging to the entity that&#39;s going to be sent into entity_to_dict() (via recursion) to be moved to the base so it can be checked when that recursion call executes ([`f4b89db`](https://github.com/ral-facilities/datagateway-api/commit/f4b89dbf1436827d9e0dbfbc1de945a3f0232641))

*  #148: Allow included fields to be specified as distinct fields ([`4470944`](https://github.com/ral-facilities/datagateway-api/commit/4470944571bb946defcc0fec4bad094ad25475d7))

*  #148: Map distinct fields to the entity they belong to

- These fields can be picked out so they are the only ones returned in a query result
- This is put into a separate function unlike before, where similar functionality was in entity_to_dict() ([`96814f1`](https://github.com/ral-facilities/datagateway-api/commit/96814f147087f8aeadc8912b72642396b1f9753e))

* Merge pull request #160 from ral-facilities/feature/icat-limit-skip-filters-#139

Implement Skip/Limit Filters for Python ICAT Backend ([`04db3d5`](https://github.com/ral-facilities/datagateway-api/commit/04db3d5679bec36d3ef3f178deecee0fcae807cd))

*  #148: Map distinct entities to attribute names

- This data will be used later on in the function to filter the distinct fields from the rest of the data ([`e55fbeb`](https://github.com/ral-facilities/datagateway-api/commit/e55fbebc4e9d5512c64da6181d74175870ed3571))

* Merge branch &#39;feature/icat-limit-skip-filters-#139&#39; into feature/icat-distinct-filter-#141 ([`e58cbae`](https://github.com/ral-facilities/datagateway-api/commit/e58cbae97c9be758e035ea5f60f0e600a1964e63))

*  #141: Rename ICATQuery and move it to a separate file ([`4f84e52`](https://github.com/ral-facilities/datagateway-api/commit/4f84e52847a7b3c7ceb72b32169f3e7449aa4aff))

*  #139: Send a request for ICAT properties at start-up only ([`7256627`](https://github.com/ral-facilities/datagateway-api/commit/7256627fd227213ca0a959c62c4d6258c3f4e191))

*  #144: Add documentation and style changes ([`9a1b060`](https://github.com/ral-facilities/datagateway-api/commit/9a1b060a9e4b21df051fe48ff86c87d58ebdffc3))

*  #144: Move extraction of filter fields to specific backend

- This makes the WHERE filter interact well with included fields for the Python ICAT backend - e.g. {&#39;investigationUsers.id&#39;: &#34;= &#39;6&#39;&#34;} ([`d3b08e4`](https://github.com/ral-facilities/datagateway-api/commit/d3b08e4377cd56f7aa6b13d2efa9e9cc2e6ebdd5))

*  #143: Remove unused import ([`6fa0d9a`](https://github.com/ral-facilities/datagateway-api/commit/6fa0d9ae496a4ffeb3e43aabd104aadeff4c09c2))

*  #143: Minor docstring/logging changes ([`1e7572a`](https://github.com/ral-facilities/datagateway-api/commit/1e7572a1ae792590b506a6ceabddadbfecd3ef69))

*  #143: Improve structure of execute_query()

- This commit will also add some info logging to track what happens to the query during its lifecycle ([`26f303a`](https://github.com/ral-facilities/datagateway-api/commit/26f303af4c59c4f7d6da90a342cb2c08d9974b06))

*  #143: Make entity_to_dict() more readable ([`2210fdb`](https://github.com/ral-facilities/datagateway-api/commit/2210fdbaf1a80e4bc5c17db6d5f3268cd3272589))

*  #143: Allow dates to be converted to strings in nested structures

- Nice reduction in lines :) ([`3381e82`](https://github.com/ral-facilities/datagateway-api/commit/3381e82c6acd6328498867e804b0b1dc936c8b02))

*  #143: Allow included fields to be added to response to n levels deep

- A nice recursive function allows dictionary-based include filters to be correctly added to the request&#39;s response
- Requests are still currently broken because of date conversion still not happening correctly, but the log message which shows `data` before being returned shows the data structure is correct, near identical to the way its assembled in the database backend ([`bba6a23`](https://github.com/ral-facilities/datagateway-api/commit/bba6a23d5bb01fa091bdf72e8b2d54d560785b96))

*  #143: Checkpoint for making data nested

- Written a specific solution for the data I&#39;ve been looking at.
- This now uncovered another issue, with the way I search dict_result to convert datetime objects to strings ([`0064ac8`](https://github.com/ral-facilities/datagateway-api/commit/0064ac8670b600a1e06950c60a4d5ecf4c3a305a))

*  #143: Checkpoint for adding included data to response

- Data is now added when dictionaries are used within an include filter, however it&#39;s not nested correctly ([`b89baea`](https://github.com/ral-facilities/datagateway-api/commit/b89baea6680cf03c88e9a9a31cafedcd1db85b13))

*  #143: Deal with included fields which are joined by dots

- Also add some comments in `execute_query()` ([`c32dd5e`](https://github.com/ral-facilities/datagateway-api/commit/c32dd5e4fdbc094aa5e8e5116ca2b22a920aa9cc))

*  #143: Convert lists and dicts into a form compatible with Python ICAT ([`3d0f59c`](https://github.com/ral-facilities/datagateway-api/commit/3d0f59cfad994e62f5dfb26c51d19e9f02ff43c5))

*  #143: Solve warnings by VS Code

- Warning were caused by missing import statements ([`3257204`](https://github.com/ral-facilities/datagateway-api/commit/32572044a67ebea17913c49e16b08a07a4b29186))

*  #143: Checkpoint for dealing with include filter input

- Input for PythonICATIncludeFilter ([`9d52037`](https://github.com/ral-facilities/datagateway-api/commit/9d5203705b40e92741a88d3d816eeec2ca5463ca))

*  #143: Start to improve how include filter input is adapted for Python ICAT

- This deals with strings and lists very well, work is needed on handling dictionaries ([`da3ac2c`](https://github.com/ral-facilities/datagateway-api/commit/da3ac2c49c74584f3b54185a3524a948f60424b6))

*  #143: Allow dictionary of include filter to be converted to Python ICAT format

- This change doesn&#39;t make dictionary include filter work, but they&#39;re now converted to a notation that Python ICAT accepts ([`9b8e08e`](https://github.com/ral-facilities/datagateway-api/commit/9b8e08e528fbc145f254a05ad60b4455f338cd33))

*  #143: Add basic implementation of include filter

- This filter currently accepts a single entity name, or a list of entity names. Dictionaries are not yet supported ([`c724f72`](https://github.com/ral-facilities/datagateway-api/commit/c724f721a0e5905a38a48cb8b8a66c52f137c5f3))

* Merge branch &#39;feature/icat-limit-skip-filters-#139&#39; into feature/icat-distinct-filter-#141 ([`32e6927`](https://github.com/ral-facilities/datagateway-api/commit/32e69278b3a1d047d4e3820d7b75d35a734d77fd))

* Merge pull request #158 from ral-facilities/feature/icat-order-filter-#140

Implement Order Filter for Python ICAT Backend ([`a014b11`](https://github.com/ral-facilities/datagateway-api/commit/a014b113918ce249c437030f0406b4214fcf23be))

*  #141: Fix bug on IN operation of WHERE filter with single element value

- This change fixes a bug where if a value used for a WHERE filter with an IN operation had only a single element in a list, it would cause a JPQL error. This happened because the list was converted into a tuple (to satisfy JPQL formatting of array based data). With single element tuples, Python adds a trailing comma, something which is invalid in JPQL. The value is now converted into a string, with the square brackets being replaced with normal brackets before being sent off to JPQL.
- Also added type checking on the value if an IN operation is used to ensure the value is a list ([`2aea37c`](https://github.com/ral-facilities/datagateway-api/commit/2aea37c6800f590b8eac6709437b62d1cfd2e7fc))

* Merge branch &#39;feature/icat-order-filter-#140&#39; into feature/icat-limit-skip-filters-#139 ([`61b63a2`](https://github.com/ral-facilities/datagateway-api/commit/61b63a26fdf473fa48ce02603f2d3aa1de0dcd8d))

*  #140: Make suggested changes as per PR comments ([`8c1dcd7`](https://github.com/ral-facilities/datagateway-api/commit/8c1dcd7e68146b31e950156499ce92010eecaa9f))

*  #135: Simplify assignment of client in ICAT backend functions ([`074d4da`](https://github.com/ral-facilities/datagateway-api/commit/074d4da296b446c3041c041978fb98e3cfeeb7d1))

*  #141: Fix bug where JSON serialisable dates wouldn&#39;t be applied when using distinct filter ([`2d7eeff`](https://github.com/ral-facilities/datagateway-api/commit/2d7eeff9415fedb9e605b5001ac2b6c6e550d4a3))

*  #141: Fix where distinct filter doesn&#39;t show field because of overlapping WHERE filter

- This change means that if there&#39;s a distinct filter of an attribute, and a WHERE filter specifying a condition of the same attribute, the distinct filter will act as intended (where before the data of that attribute wasn&#39;t added to the response) ([`92d6b01`](https://github.com/ral-facilities/datagateway-api/commit/92d6b01b905664449b08de80f534f2a66e6a6038))

*  #141: Refactor ICAT creation and execution

- Turned the two functions into a class, since these are related operations
- This change has been made so I can add another function to this class later on ([`0029978`](https://github.com/ral-facilities/datagateway-api/commit/002997827f572a60db105abf9deee4a144f3d49d))

*  #141: Refactor the distinct filter aspects of execute_icat_query()

- Combine some of the logic with the existing logic where `return_json_formattable` is True - this will ensure that datetimes are converted to an appropriate format when using distinct filters
- This commit also adds checking of the query&#39;s conditions to only select attribute names of those which are &#34;!= null&#34; as set by the distinct filter ([`7031f59`](https://github.com/ral-facilities/datagateway-api/commit/7031f5981b144fb7567b639beec541f229c070c5))

*  #141: Allow multiple fields to be used in a distinct filter

- Inside a PythonICATDistinctFieldFilter, a where filter is created for each field in the request. These are then searched for in execute_icat_query() and the data is compiled to only include data from those fields ([`26b7893`](https://github.com/ral-facilities/datagateway-api/commit/26b7893c60284f606df16063d6bf955874c72eb1))

*  #141: First trial of dealing with distinct filters using conditions from helper side

- This requires the addition of creating WHERE filters within a distinct filter to deal with multiple fields within a single distinct filter ([`eedc803`](https://github.com/ral-facilities/datagateway-api/commit/eedc8034ad9afba234fb005464da42769da385d2))

*  #141: Add &#39;not equal&#39; operation to ICAT WHERE filter

- The primary used for this operation will be to add WHERE filters when a distinct filter is in a request, so distinct filters can accomodate multiple fields ([`bda22f4`](https://github.com/ral-facilities/datagateway-api/commit/bda22f40e48d846beb7d262ae4b0f5c4e7022f7f))

*  #141: Add distinct aspect of ICAT distinct filter ([`d41359f`](https://github.com/ral-facilities/datagateway-api/commit/d41359f8a3ac02c8f5b341e9e7ae1513b3f1c652))

*  #141: Implement distinct filter

- This changes the output of the data to a list of values, rather than the traditional list of dictionaries, containing attribute name and its value ([`20c7120`](https://github.com/ral-facilities/datagateway-api/commit/20c712045ad8df1396f6f3cca70c71ea3eb7a5c6))

*  #139: Code formatting changes made by Black ([`0888686`](https://github.com/ral-facilities/datagateway-api/commit/088868605412a7370ab5b88ae94e467ab63811b1))

*  #139: Fix independent use of skip filter

- Grabs max num of entities from ICAT properties and applies that to the count element of the tuple - the currently configured number is 10000, which should be more than enough for any applicable use cases of this API ([`39ab528`](https://github.com/ral-facilities/datagateway-api/commit/39ab528583e782d16795f657b95b4f79d5f0009c))

*  #139: Allow a request to have both limit and skip filters

- The skip filter will be merged into the limit filter, with the skip filter being removed from the filter handler
- There is a bug when using a skip filter on it&#39;s own, as it&#39;ll always return a 404 ([`93eb468`](https://github.com/ral-facilities/datagateway-api/commit/93eb4686670299b75e8e164ba878a4106374b30c))

* Adding issue/PR templates ([`921c9d9`](https://github.com/ral-facilities/datagateway-api/commit/921c9d949f276993e7e5f37ca65cb3d770e6b972))

*  #140: Add docstrings ([`182d054`](https://github.com/ral-facilities/datagateway-api/commit/182d05472e11ed0be7f0c837cb4cdd7dea21ac34))

*  #140: Allow multiple order filters to be used in conjunction ([`aec81f1`](https://github.com/ral-facilities/datagateway-api/commit/aec81f1f27d72655005d4cdd0d5135b2fd54ff92))

*  #140: Move create_condition() to PythonICATWhereFilter

- This is to remove a circular dependency that I found while implementing an order filter
- Also added a couple of __init__.py files which didn&#39;t previously exist ([`51924f8`](https://github.com/ral-facilities/datagateway-api/commit/51924f8bf0efac50a2b93f3f2978f54608512db8))

*  #140: Remove unused imports ([`19a286b`](https://github.com/ral-facilities/datagateway-api/commit/19a286b794a6d1e1373bdce4b0711f60ece34a88))

*  #140: Basic implementation of ICAT order filter

- If there&#39;s more than one order filter in a request, the others get overwritten due to the way setOrder() works in Python ICAT ([`578ac21`](https://github.com/ral-facilities/datagateway-api/commit/578ac214b56e5086483ca5f0a13fca0aad036234))

*  #140: Move FilterOrderHandler into its own file

- This will remove circular imports in a later change
- Also helps to tidy up the code base by separating the filter handler from the abstract classes of the filters ([`78ef98e`](https://github.com/ral-facilities/datagateway-api/commit/78ef98e33809c65902299413c5c200ba34fa518c))

*  #140: Fix DB order filter from an import error ([`4bee04b`](https://github.com/ral-facilities/datagateway-api/commit/4bee04b70f3fbffbb00158c7825cc9319d8f6570))

* Merge branch &#39;master&#39; into feature/fix-session-handling-#135 ([`f4a06ce`](https://github.com/ral-facilities/datagateway-api/commit/f4a06ce50145d660ce19f3b27066a28546ac7ead))

*  #135: Make client objects bound to an endpoint, not a backend

- This will prevent the same client object being used across different endpoints, which could be a security concern. This means that for each request, the client object is built with the session ID assigned each time, so each request checks that the user has a valid, active session ID ([`853b0a1`](https://github.com/ral-facilities/datagateway-api/commit/853b0a1a98a686fe21bae2b4291d361b8ef97430))

*  #142: Rebuild Swagger docs

- They&#39;ve changed a little since they&#39;ve last been committed ([`6d225d6`](https://github.com/ral-facilities/datagateway-api/commit/6d225d6d7b669824c43e1d451d42754f8a23d740))

*  #142: Make changes as requested in PR review ([`537d4c6`](https://github.com/ral-facilities/datagateway-api/commit/537d4c688c9fbb6f9e5438acfaf78759fc4d2f98))

* Merge branch &#39;feature/python-icat-where-filter-#142&#39; of github.com:ral-facilities/datagateway-api into feature/python-icat-where-filter-#142

- Caused by not doing a git pull before a made changes... ([`a70ee2b`](https://github.com/ral-facilities/datagateway-api/commit/a70ee2b307a402846db9ed59eff22ea34f67bfd3))

*  #142: Change &#39;BadFilterError&#39; to &#39;FilterError&#39;

- Part of PR review for this branch ([`e27c887`](https://github.com/ral-facilities/datagateway-api/commit/e27c887515012faefe6054cc0fdd695e6bb3d086))

*  #142: Add &#39;gt&#39; &amp; &#39;lt&#39; operations to WHERE filter

- This change affects both database and Python ICAT backends ([`4707be6`](https://github.com/ral-facilities/datagateway-api/commit/4707be6958426200511636ae149ee10345e97fb5))

* Merge pull request #151 from ral-facilities/feature/python-icat-entity-id-endpoints-#136

Entity by ID Methods ([`0600a0a`](https://github.com/ral-facilities/datagateway-api/commit/0600a0ae9e5e4641d5adffbe93e8d2f4a0dd2bd7))

* Merge pull request #157 from ral-facilities/feature/linter-black-#155

Implement Black (code formatter) into repo&#39;s development cycle ([`358b74b`](https://github.com/ral-facilities/datagateway-api/commit/358b74bcdb5a919fc38bdb45dad349a2eee9abac))

* Merge branch &#39;master&#39; into feature/python-icat-entity-id-endpoints-#136 ([`6c1dd4c`](https://github.com/ral-facilities/datagateway-api/commit/6c1dd4cf9abffbb8289337d26d02817d096ed7cf))

* Merge branch &#39;feature/python-icat-where-filter-#142&#39; into feature/linter-black-#155 ([`aeb05dc`](https://github.com/ral-facilities/datagateway-api/commit/aeb05dc531e4fc9d2f00b3411f6e6b3ae6ed3c59))

* Merge branch &#39;feature/python-icat-get-with-filters-#137&#39; into feature/python-icat-where-filter-#142 ([`26b8033`](https://github.com/ral-facilities/datagateway-api/commit/26b8033133ffdf79021ffec6b2c760607af5d8e6))

*  #142: Change project structure in README

- This has changed as a result of having directories for each type of backend: database and python_icat ([`3290f08`](https://github.com/ral-facilities/datagateway-api/commit/3290f08a1f69c52c3dc8d5b5ba9db0fccfd95f9d))

*  #155: Add documentation regarding code formatter ([`d7f726d`](https://github.com/ral-facilities/datagateway-api/commit/d7f726d488d7ebc16af28cdefb6a53b61924f8b7))

*  #155: Prevent internal ICAT exceptions from occurring

- Bug introduced when I implemented the WHERE filter ([`a22e8f4`](https://github.com/ral-facilities/datagateway-api/commit/a22e8f4ed14663c2e0d45e0a2305f3887eadb81b))

*  #155: Put longer strings onto multiple lines to keep with 88 character line length

- A couple have been left alone as they&#39;re only 1/2 characters over 88 (as defined by Black). It seemed better to keep them on a single line for readability reasons ([`0f67fc7`](https://github.com/ral-facilities/datagateway-api/commit/0f67fc798e42b8fcb49ef7c1fb3b7e5a36554034))

*  #155: Make things missed by Black mostly abide by 88 characters

- Black mostly missed docstrings and some really long strings, but that&#39;s understandable. Black doesn&#39;t directly edit strings for fear of editing their contents ([`4aff02d`](https://github.com/ral-facilities/datagateway-api/commit/4aff02d1e7dabd9c9dcf29be1ffbc0df23a5f089))

*  #155: Changes made by Black code formatter

- This is directly after doing `black .` on the root directory. It&#39;ll be interesting to see if any corrections are needed ([`93b4d85`](https://github.com/ral-facilities/datagateway-api/commit/93b4d85496abe282257f26b4b391fff0f52c6311))

*  #135: Fix failing unit test

- Unit test was failing due to null session data being entered to the database ([`e662c48`](https://github.com/ral-facilities/datagateway-api/commit/e662c48833d89a1b628e9d25c8bd3dea8294e397))

*  #135: Fix session handling

- This will mean a valid session ID can be used straight away, instead of having to use the login endpoint to create a new session ID and use the API using that. This will help when prod users use session IDs which have come from other auth services ([`662fc3c`](https://github.com/ral-facilities/datagateway-api/commit/662fc3c9f20d12ad83f8a185d73839910d849b71))

* Merge branch &#39;feature/python-icat-get-with-filters-#137&#39; into feature/python-icat-entity-id-endpoints-#136 ([`cc75ec0`](https://github.com/ral-facilities/datagateway-api/commit/cc75ec07dca8583171fa28f7ea2bac73decb5793))

* Merge branch &#39;feature/python-icat-entity-id-endpoints-#136&#39; into feature/python-icat-get-with-filters-#137

Conflicts:
	common/python_icat_helpers.py ([`80b89e9`](https://github.com/ral-facilities/datagateway-api/commit/80b89e95a0a8ee1cc8319cbe60d0e6813a8af57f))

*  #142: Implement like and in expressions for WHERE filter ([`95e8c37`](https://github.com/ral-facilities/datagateway-api/commit/95e8c378778cd43c480b78d4315e0888f3fe9784))

*  #136: Allow round-tripping of datetime data

- Added an ICAT exception where data modification was stopped to prevent icatdb from being put into an invalid state ([`511655e`](https://github.com/ral-facilities/datagateway-api/commit/511655e7fa652c53760b0f888ebd7aba4c751749))

*  #142: Implement aspects of WHERE filter for ICAT backend

- &#39;like&#39; and &#39;in&#39; operations don&#39;t work yet ([`9d2b4b5`](https://github.com/ral-facilities/datagateway-api/commit/9d2b4b559b6dc4cc0733dc79b6640df22588c2c5))

*  #136: Changes made as requested in pull request ([`9611a11`](https://github.com/ral-facilities/datagateway-api/commit/9611a1143b4e27b441d676db342b20b55d84c469))

*  #142: Remove duplicated constructor for DB filters ([`b6224db`](https://github.com/ral-facilities/datagateway-api/commit/b6224dbf06a4469e2b9ff5bc87424eac408b9fa6))

*  #137: Make improvements as per PR for this issue ([`f6ac645`](https://github.com/ral-facilities/datagateway-api/commit/f6ac645272049a2f5876814c66680f00cbc1c3c0))

*  #136: Make improvements as per PR for this issue ([`bc1cdf9`](https://github.com/ral-facilities/datagateway-api/commit/bc1cdf910245965a1398503fd89227e744ad9709))

*  #142: Move ICAT files and skeleton for filters ([`8ac7efc`](https://github.com/ral-facilities/datagateway-api/commit/8ac7efcfba3223fcbc1b8203a3cd878da5be8a4e))

*  #142: Move DB filters to their own directory

- This change also moves the database implementation of the backend and the helper functions to a specific database folder. The same will be done with the python_icat versions of these
- Unit tests still pass when using the database backend ([`ea45b66`](https://github.com/ral-facilities/datagateway-api/commit/ea45b6620576e49e83d0248daed6b12d62e0521c))

*  #142: Move skeleton filters implementation to separate files

- This adds filters.py to be able to implement filters using Python ICAT ([`01bd4bb`](https://github.com/ral-facilities/datagateway-api/commit/01bd4bbcaf3cc7aa7a05fa61f93caf0fb7f620da))

*  #137: Pass error messages from Python ICAT to PythonICATError ([`e0180d3`](https://github.com/ral-facilities/datagateway-api/commit/e0180d35dcf4aa7e2a03b797fc05c0d70af943ba))

*  #137: Basic implementation of GET endpoint for entities

- Implementation for the Python ICAT backend
- This implementation ignores any filter parameters in the request as this haven&#39;t been implemented for the Python ICAT backend. As a result, this endpoint just gets all the records for a specified entity ([`cc4358e`](https://github.com/ral-facilities/datagateway-api/commit/cc4358efb5065998500fb81ec441004093c6501b))

*  #136: Catch exception when an attribute cannot be found

- API now returns a 400 with a message to the user ([`cac1003`](https://github.com/ral-facilities/datagateway-api/commit/cac10036e0a51bad4cba07068837b68fdcc822fa))

*  #136: Add Python ICAT exception and docstrings across helpers

- Python ICAT exception returns a 500 to users when something Python ICAT related may have gone wrong (e.g. creating a Query object). This has been implemented for that example
- Added docstrings to the session related functions to match with the ones for entity by ID helper function
- Removed an empty queries_records function inside the ICAT helper file as it&#39;s not needed ([`785adde`](https://github.com/ral-facilities/datagateway-api/commit/785addea1e43ed4db692f4b6b1a6f2993152dbe2))

*  #136: Resolve ICAT error where related entity were trying to be set to null

- The code to convert request body values into dates has been tested and is fully working. ([`4b15a05`](https://github.com/ral-facilities/datagateway-api/commit/4b15a056cc2d98a948a4da63e430901cbe8a6232))

*  #136: Add support for delete entity by ID on new backend ([`f072c1d`](https://github.com/ral-facilities/datagateway-api/commit/f072c1de3240af49103a663e3b588bf43d96e428))

*  #136: Allow relevant updated data to be converted into datetime objects

- Code is currently untested due to issues I&#39;m having with Python ICAT. The code will be tested before review. ([`8a1728b`](https://github.com/ral-facilities/datagateway-api/commit/8a1728b0cb64a2b977f24919669170dcfb8df1d4))

*  #136: Add basic implementation for PATCH entity by ID

- Basic implementation, work needs doing to allow dates and other unusual types to be updated ([`53acd2a`](https://github.com/ral-facilities/datagateway-api/commit/53acd2a4998a07fc272d49e217eb97c89bd43907))

* Update LICENSE ([`412cf1b`](https://github.com/ral-facilities/datagateway-api/commit/412cf1b73b095cec4d779e2f1bfb13fcaf95c17d))

*  #136: Allow get_entity_by_id() to return data in different formats

- A flag is used to determine whether the data will be returned in a manner ready to be converted to JSON, or whether to leave it in a Python ICAT state ready to be edited/changed ([`8627e8b`](https://github.com/ral-facilities/datagateway-api/commit/8627e8b6d7f1e94926dedcd286fcc5cc2fe6b20c))

*  #136: Refactor get entity by ID helper function and associated infrastructure

- This change is mostly about moving code into their own functions, but also making the id_condition more generic so it can be used throughout the helper functions. A design decision needs to be made about how to best structure the code creating conditions
- Added docstrings throughout, documenting the accepted parameters and their types ([`f747bae`](https://github.com/ral-facilities/datagateway-api/commit/f747baeaa4c09e64f8ad7d4ba3f66162cd454a82))

*  #136: Add framework for PATCH entity by ID endpoints ([`9bfefcf`](https://github.com/ral-facilities/datagateway-api/commit/9bfefcfed8d3ccca1b9626bbd2b1a4999a65f46d))

*  #136: Allow any entity by ID request to correctly get data

- Added docstrings to the functions related to this work. Some of them are incomplete but have TODO marked against them where that&#39;s the case
- Removed the hardcoded &#39;User&#39; entity so any entity can be used. This compares the table name to each of the entity names from Python ICAT and passes the Python ICAT entity name to the query builder. This is due to Python ICAT being case sensitive. A 400 is thrown if an entity cannot be found within Python ICAT
- Moved query execution into a generic function for use elsewhere in the codebase
- Changed a blanket string conversion just to converting datetimes to strings. This was causing IDs to be converted to strings which isn&#39;t correct behaviour. Datetimes must be converted to strings so they become JSON serializable ([`0b0bc20`](https://github.com/ral-facilities/datagateway-api/commit/0b0bc208a6c71618910766868cd0fcc9aad910bb))

*  #136: Add functionality to get a user by their ID

- The &#39;User&#39; entity is currently hardcoded into get_entity_by_id, due to facing an issue with case sensitivity on Python ICAT&#39;s side. In the future, any entity should be able to use this code ([`3cc1301`](https://github.com/ral-facilities/datagateway-api/commit/3cc1301ee6eaa6897344d87705ce6ba1669f8900))

* Merge pull request #149 from ral-facilities/feature/python-icat-backend-login-endpoints-#135

Python ICAT Backend: Login endpoints &amp; session validation ([`ddca280`](https://github.com/ral-facilities/datagateway-api/commit/ddca2807ac60edf99015f02e8f5f53550d68e49d))

*  #135: Allow session IDs to not be overwritten in the database

- This is done by creating a new client object each time users login. If the same object is used for every login, the session ID will just be overwritten, even if logging in as a different user ([`5195edb`](https://github.com/ral-facilities/datagateway-api/commit/5195edb6c0f474f27b8c8510116bb7e8407e82a8))

*  #135: Add mechanism parameter to login endpoint for Swagger docs ([`851166c`](https://github.com/ral-facilities/datagateway-api/commit/851166c0ee0e9cf8201af64f25ce858836de7949))

*  #135: Implement refresh session logic for Python ICAT backend ([`95bcb7b`](https://github.com/ral-facilities/datagateway-api/commit/95bcb7b905ddcf58fe70392595b665a0869ba88b))

*  #135: Allow users to logout from Python ICAT backend ([`8ca17eb`](https://github.com/ral-facilities/datagateway-api/commit/8ca17eb063fc95a12277ccb2f6e8845e4c2dcd48))

*  #135: Further tweaks for Python ICAT session decorator

- This also moves some of the DB helper code into the relevant file
- These changes cause one of the tests in test_helper.py to fail when using the Python ICAT backend. This is because @requires_session_id only really tests if a session ID is valid when it&#39;s actually doing an API call. I&#39;m not 100% happy with this but the feature does function ([`dbe8ba1`](https://github.com/ral-facilities/datagateway-api/commit/dbe8ba1d16899e6fa3631339e86e28ab2087dedc))

*  #135: Add Python ICAT decorator to ensure valid session ID ([`168ba94`](https://github.com/ral-facilities/datagateway-api/commit/168ba94b07806e8e15c240a369fbeac74e70a443))

*  #135: Add config option for whether certs for ICAT

- Moved the client object into the constructor so it can be accessed by all functions in the class, though this might mean a session ID becomes useless? ([`93d2305`](https://github.com/ral-facilities/datagateway-api/commit/93d2305a89897a47ca2820727e5df60c464b8fe1))

*  #135: Implement login function for python ICAT backend

- Because this backend can use different mechanisms, I&#39;ve changed the DB backend so it can use a mechanism as per the request body
- Any installed mechanism can be used, though if one isn&#39;t supplied, it defaults to simple ([`9755e0b`](https://github.com/ral-facilities/datagateway-api/commit/9755e0b16aeeb5c8e532bbfddd9e56d71bb65d0c))

*  #135: Add skeleton outline for new python-icat backend ([`c2e09bf`](https://github.com/ral-facilities/datagateway-api/commit/c2e09bf86e8c2386294f932a7356d0b8084c060a))

* Merge pull request #127 from ral-facilities/feature/configurable-backend-#125

Enable backend to be configurable ([`e4db23b`](https://github.com/ral-facilities/datagateway-api/commit/e4db23b42fc6b8b15db08cd5d3dfcbd1158edbf8))

* Merge branch &#39;master&#39; into feature/configurable-backend-#125 ([`108256f`](https://github.com/ral-facilities/datagateway-api/commit/108256fda0a0e5df82f7bd8722641f298b560527))

* #125 - extract out backends into seperate files ([`8a2f6a2`](https://github.com/ral-facilities/datagateway-api/commit/8a2f6a2a2b41aad210fc3331b5b5b5b26b9ad021))

* #125 - use non-decorator version of error handler registerer ([`54e50ce`](https://github.com/ral-facilities/datagateway-api/commit/54e50ce18c7309ee0d6726ee0120cef56eea6f58))

* Merge branch &#39;id-endpoints-404-#129&#39;

Conflicts:
	src/swagger/openapi.yaml ([`016ce7b`](https://github.com/ral-facilities/datagateway-api/commit/016ce7bff672ebeee6f842ca6614cb1b99ab29d9))

* Merge branch &#39;include-filter-count-endpoints-swagger-#128&#39;

Conflicts:
	src/swagger/openapi.yaml ([`d330972`](https://github.com/ral-facilities/datagateway-api/commit/d33097299736587c48cbf1ed6c2f38f7f08d4a7a))

* Merge pull request #130 from ral-facilities/remove-userinvestigations-query-#126

Remove unused users investigation endpoints ([`948b4dd`](https://github.com/ral-facilities/datagateway-api/commit/948b4ddc0b446a57ef62fbabba0762eb9ea7f80b))

*  #129: Add rebuilt openapi.yaml for Swagger docs ([`821680d`](https://github.com/ral-facilities/datagateway-api/commit/821680d34bfffc2bcace462181604fce72c5dadd))

*  #126: Add rebuilt openapi.yaml for Swagger docs ([`215c0dc`](https://github.com/ral-facilities/datagateway-api/commit/215c0dc4d27715b27388b1e621ac3251f54fff6b))

*  #128: Add rebuilt openapi.yaml for Swagger docs ([`8a7a47f`](https://github.com/ral-facilities/datagateway-api/commit/8a7a47fe02a8f1f089073fd402f867ef5b1efec1))

*  #128: Make INCLUDE filters visible to all count endpoints for Swagger web UI ([`d31ac7a`](https://github.com/ral-facilities/datagateway-api/commit/d31ac7a97627dfe6541e15478c957111f0191c90))

*  #129: Correct other customer user input parameters so they work in Swagger ([`8f1c409`](https://github.com/ral-facilities/datagateway-api/commit/8f1c409f22e267a267273072a35e334b71d1b61c))

*  #129: Change name of ID parameters to correct case for Swagger docs

- Swagger is case sensitive when using parameters
- This change means endpoints with an ID parameter (e.g. /users/{id}) will now work using the Swagger UI user input for said ID ([`203707f`](https://github.com/ral-facilities/datagateway-api/commit/203707f76457daac2f56744e6ae073c7ae5f1a13))

* Remove unused users investigation endpoints

- Removing /users/{id}/investigations and /users/{id}/investigations/count
- These endpoints are being removed because equivalent behaviour can be achieved by the respective endpoints in /investigations by using WHERE and INCLUDE filters ([`9bba91c`](https://github.com/ral-facilities/datagateway-api/commit/9bba91ca590c0e0036a3c36d607f509c9dc05180))

* #125 - fix duplicated `to_dict` in get_id_endpoint ([`755e85f`](https://github.com/ral-facilities/datagateway-api/commit/755e85fde9cef703810b82f396ab7f83d8fcea85))

* Merge branch &#39;master&#39; into feature/configurable-backend-#125 ([`3862d11`](https://github.com/ral-facilities/datagateway-api/commit/3862d11474fca55c28b1934b5d8aa4ee9d8f0d17))

* Merge pull request #121 from ral-facilities/feature/set-session-info-#120

#120 - set username + expiredatetime on POST /session ([`05ad009`](https://github.com/ral-facilities/datagateway-api/commit/05ad009f0c946797aa53fc3ce8b242953f23c035))

* Merge pull request #124 from ral-facilities/feature/improve-openpi-spec-gen-#123

Improve OpenAPI spec generation ([`130a736`](https://github.com/ral-facilities/datagateway-api/commit/130a73672fc1c344ba1b5bf7bff0a7f5047e6ffa))

* #125 - add abstract &#34;backend&#34; class and move database specific code in endpoints to there.

Also, an change in that errors are no longer caught, and are translated by flask into error codes. ([`5ae2cc8`](https://github.com/ral-facilities/datagateway-api/commit/5ae2cc84876149f05600767f93ae9f6aa49c3ed0))

* #123 - complete OpenAPI spec documentation ([`03d768f`](https://github.com/ral-facilities/datagateway-api/commit/03d768fc65145b6219b16970bb44da0b26a2cad9))

* #123 - document using apispec
- initialise spec
- adds models
- filters documented
- base entity endpoint fully documented
- sessions endpoint fully documented ([`dfebf55`](https://github.com/ral-facilities/datagateway-api/commit/dfebf557464bff3a1ddf1575f14b4ddab4e92ac0))

* set username to simple/root to give root access on default install ([`206a78f`](https://github.com/ral-facilities/datagateway-api/commit/206a78fae4513c5fa340fca9271a6487df1490c0))

* #120 - set username + expiredatetime on POST /session ([`f7f9b74`](https://github.com/ral-facilities/datagateway-api/commit/f7f9b7447b4b47fb1d98b78852434e49daeb3295))

* Revert to bb164ae (committed to wrong branch) ([`1d84c39`](https://github.com/ral-facilities/datagateway-api/commit/1d84c39022f450660ea8080ea64d8a3f0aaaa994))

* Include &#39;findone&#39; endpoints in generated openapi.yaml ([`bc55c74`](https://github.com/ral-facilities/datagateway-api/commit/bc55c7417c6d2b28a991d549a3e9d5cf76083188))

* Merge pull request #117 from ral-facilities/feature/schema-references-#116

Feature/schema references #116 ([`bb164ae`](https://github.com/ral-facilities/datagateway-api/commit/bb164aef826747dd378e9431ececf4b769b1101f))

* Updated openapi.yaml with entries in insertion order ([`351f7e8`](https://github.com/ral-facilities/datagateway-api/commit/351f7e870823dfbea5cf91e13ca7a7f4d55f7f2c))

* Retain insertion order when dumping to YAML ([`889e84a`](https://github.com/ral-facilities/datagateway-api/commit/889e84a575a262aeab7f49bbbbed7e92161159c8))

* Updating openapi.yaml to version with named schemas ([`97cbb72`](https://github.com/ral-facilities/datagateway-api/commit/97cbb72abbf28a0f01287f1c17b36e8a833d2daf))

* Update swagger generator to reference named schemas instead of inlining them. Fixes #116 ([`762f490`](https://github.com/ral-facilities/datagateway-api/commit/762f4903ad85c8b781d1ced367b9746feae148bf))

* Merge pull request #112 from ral-facilities/111_create_count_queries_for_table

111 create count queries for table ([`274c0c1`](https://github.com/ral-facilities/datagateway-api/commit/274c0c1b74e416eb998965c209272b5211f0d7c4))

* Merge pull request #91 from ral-facilities/87_improve_readme

Improve README ([`7140077`](https://github.com/ral-facilities/datagateway-api/commit/71400774a9b28646eb077e9d6dfb23632fe41ebe))

* #87: Split class diagram into 2 diagrams ([`9e7a5ee`](https://github.com/ral-facilities/datagateway-api/commit/9e7a5ee9f93e2ce9f3e0e82b10c09d0bcda00337))

* #111: Create count queries ([`b9293c8`](https://github.com/ral-facilities/datagateway-api/commit/b9293c88a5c26ca65d2a3eb9a2bce98e0d738935))

* #111: Match style guides ([`5721181`](https://github.com/ral-facilities/datagateway-api/commit/572118122a83034e302b4246fa713644caa5c8cc))

* Merge pull request #110 from ral-facilities/109_add_example_responses

Add example responses to swagger spec ([`5df83d9`](https://github.com/ral-facilities/datagateway-api/commit/5df83d9587408db7a6e2ef5f9eda41539d3ac449))

* #87: Add Query Docstring ([`c4b46fb`](https://github.com/ral-facilities/datagateway-api/commit/c4b46fbabd46bef6b568f4ccdde720832b18978a))

* #87: Update example ([`0b45c2a`](https://github.com/ral-facilities/datagateway-api/commit/0b45c2a82e5912e9b4706f8ca39ef72d63b24a39))

* Merge branch &#39;master&#39; into 87_improve_readme ([`95a1601`](https://github.com/ral-facilities/datagateway-api/commit/95a1601c38568e4af0c9ee877d45c3b2511502c1))

* #87: Fix typo ([`f427cb2`](https://github.com/ral-facilities/datagateway-api/commit/f427cb2a5c7f00891c0d4b28dd2554124c897a74))

* #109: Regenerate swagger ([`7aa7cd0`](https://github.com/ral-facilities/datagateway-api/commit/7aa7cd01fb61587a37f69d1f473e42f5b5f6c19e))

* #109: Add examples to endpoints ([`8052f44`](https://github.com/ral-facilities/datagateway-api/commit/8052f446f9679b4a79b9a695be276b9b1be4a6b2))

* #109: Create dictionary to store examples ([`e9d37c7`](https://github.com/ral-facilities/datagateway-api/commit/e9d37c7fefed47dbc7eb042f868d90ca1ec43ae2))

* #109: Add function to map types ([`0df043e`](https://github.com/ral-facilities/datagateway-api/commit/0df043e4fd3467749b363b766d231896fe15f8ad))

* Merge pull request #104 from ral-facilities/93_add_tests

Test EntityHelper ([`ce639cf`](https://github.com/ral-facilities/datagateway-api/commit/ce639cfef21e4018c4e42d20845b3a75c16bb695))

* Merge pull request #106 from ral-facilities/105_problem_with_returning_decimals

Problem with returning decimals ([`1c99cac`](https://github.com/ral-facilities/datagateway-api/commit/1c99cac80f79f8e934046f1b7c23ee42b899febf))

* Merge pull request #108 from ral-facilities/107_add_distinct_count_to_swagger

107 add distinct count to swagger ([`4f15e86`](https://github.com/ral-facilities/datagateway-api/commit/4f15e86199c93601f921fb779f0731366e63c9bb))

* #107: Regenerate swagger ([`b8e40c7`](https://github.com/ral-facilities/datagateway-api/commit/b8e40c749de0106ed3efc16e1af76e9e79b02029))

* #107: Add distinct parameter to count in generator ([`70e8674`](https://github.com/ral-facilities/datagateway-api/commit/70e8674cf96a96cdd7e0674abb36b9735a9c6233))

* #105: Use method ([`b78d251`](https://github.com/ral-facilities/datagateway-api/commit/b78d25106d99404f08cde8ff337a7970470ecd17))

* #105: Create serializer method ([`d294df4`](https://github.com/ral-facilities/datagateway-api/commit/d294df4761d3ba226005afa4181108e37cc46cc5))

* #93: Test dictionary include ([`22b1838`](https://github.com/ral-facilities/datagateway-api/commit/22b1838a86cd2b9c5d4a9c84527bc723404239c5))

* #93: Add investigation ([`1f55522`](https://github.com/ral-facilities/datagateway-api/commit/1f555225254b19ff6a84ba9e3443d13b2c94a711))

* #93: Test EntityHelper ([`5271333`](https://github.com/ral-facilities/datagateway-api/commit/527133363388e4ce295adc050602ef4be5dd3cbb))

* Merge pull request #103 from ral-facilities/102_add_bracket

#102: Add bracket ([`69b7939`](https://github.com/ral-facilities/datagateway-api/commit/69b7939e9431a86f11ccba1f2080eb679020e58b))

* #102: Add bracket ([`0974012`](https://github.com/ral-facilities/datagateway-api/commit/09740125f78c5782dedde36a8dc1d50e6540a4fe))

* Merge pull request #101 from ral-facilities/100_generate_2_datasets

Generate 2 datasets ([`78799d5`](https://github.com/ral-facilities/datagateway-api/commit/78799d5984fc41aa8ff9ffec2982b912adfbecda))

* #100: Style changes ([`ae9d342`](https://github.com/ral-facilities/datagateway-api/commit/ae9d3421037d55c32a3ea6fb514da5b70f31ea26))

* #100: Reduce the number of datafiles ([`6a52ea9`](https://github.com/ral-facilities/datagateway-api/commit/6a52ea97474003e1dfbe01261347f2bbd2ec9f8b))

* #100: Generate datasets per investigation ([`4d163b2`](https://github.com/ral-facilities/datagateway-api/commit/4d163b25f4a1a1d3a4ac3d1d334946e44dc5b173))

* Merge pull request #94 from ral-facilities/92_refactor_endpoints

Proposed refactoring for 92 ([`72248a8`](https://github.com/ral-facilities/datagateway-api/commit/72248a8692f567eb0c69095089e1c2912d95502d))

* Merge branch &#39;master&#39; into 92_refactor_endpoints ([`2c6a862`](https://github.com/ral-facilities/datagateway-api/commit/2c6a8626b65f44bae69ddcaeee63de81e24c9802))

* Merge pull request #99 from ral-facilities/83_add_dev_requirements

Add dev requirements ([`0478a45`](https://github.com/ral-facilities/datagateway-api/commit/0478a450c4545ac192b492e6eff33851857d72a6))

* Merge pull request #98 from ral-facilities/80_debug_mode_is_not_applied

Debug mode is not applied ([`0a269e3`](https://github.com/ral-facilities/datagateway-api/commit/0a269e377e8a7c59ad699f72ef2340447f0a913f))

* #83: Remove pyyaml ([`a68f1f5`](https://github.com/ral-facilities/datagateway-api/commit/a68f1f5f2eff8dbda2cdd4e6d5fd76f22ad978bc))

* #83: Actually fix it this time ([`9920385`](https://github.com/ral-facilities/datagateway-api/commit/99203856fdfea61422e7d7e4a8edda932599520e))

* #83: Fix line spacing ([`3b37b96`](https://github.com/ral-facilities/datagateway-api/commit/3b37b96c1657bcc49714fc7a9c4ca053cce55c1e))

* #83: Update readme ([`07fbc76`](https://github.com/ral-facilities/datagateway-api/commit/07fbc76dd5a014abd711f2bac97c7b2052223eb9))

* #83: Update and split requirements ([`1a78b60`](https://github.com/ral-facilities/datagateway-api/commit/1a78b60a16bce22b6a4a92355f7bc5c018839017))

* #80: Update readme ([`0386de2`](https://github.com/ral-facilities/datagateway-api/commit/0386de22676043c001f76abb9e22a644f6fb505e))

* #80: move debug option ([`611dd2a`](https://github.com/ral-facilities/datagateway-api/commit/611dd2ad1b3bd5d53a864e16941f7fe463ff29e1))

* Merge pull request #97 from ral-facilities/95_logging_nothing

Remove empty log line ([`9e624a1`](https://github.com/ral-facilities/datagateway-api/commit/9e624a1952374e11e04b54c07a323ab42f5a1e1e))

* #95: Remove line that was logging nothing ([`c936c2e`](https://github.com/ral-facilities/datagateway-api/commit/c936c2e464e593cc4cab46f85f75bd3c24b5c011))

* Merge pull request #96 from ral-facilities/42_add_filtering_to_includes

Add way to filter included entities ([`8191110`](https://github.com/ral-facilities/datagateway-api/commit/8191110c5faab0d5c534beedcdd743ebb286460c))

* #42: Add attributes to constructor ([`cb7fbf2`](https://github.com/ral-facilities/datagateway-api/commit/cb7fbf28599f28d43d2ef9c07f040ab2803ebcf8))

* #92: Add docstrings ([`18832dc`](https://github.com/ral-facilities/datagateway-api/commit/18832dcc59aff011491eb26aa35b6428751029f6))

* #92: Update readme ([`7d4b1b0`](https://github.com/ral-facilities/datagateway-api/commit/7d4b1b0ed3b9521cc28c691b42e8e41ff3cd8ae0))

* #42: Add level 2 include filtering ([`e410825`](https://github.com/ral-facilities/datagateway-api/commit/e410825ce61374f4deaeb2e6c1d4830be887803b))

* #42: Add private method to set fields and tables ([`22d0be1`](https://github.com/ral-facilities/datagateway-api/commit/22d0be1efa533ac05c80c8cc006b92e7655b145e))

* #42: Add way to filter included entities ([`f1e6e8a`](https://github.com/ral-facilities/datagateway-api/commit/f1e6e8ac1978b0703fac5ed072574fc092aef1eb))

* #92: Add findone and count ([`067873c`](https://github.com/ral-facilities/datagateway-api/commit/067873c310fefb792a3fc5be9b89a8832683e074))

* #92: Fix typo ([`77d36ce`](https://github.com/ral-facilities/datagateway-api/commit/77d36ce7e78223c9152896d6670390fd5e969a9b))

* #92: Update swagger generator ([`b5e4a6b`](https://github.com/ral-facilities/datagateway-api/commit/b5e4a6b5095e158f2aec033d11399fb3cdc5d1a6))

* #92: Update main to use generated endpoints ([`3b1e5f7`](https://github.com/ral-facilities/datagateway-api/commit/3b1e5f7a2e4ff2a36e647952b4c750aeb9544ed0))

* #92: Add entity map ([`12c4353`](https://github.com/ral-facilities/datagateway-api/commit/12c435363c41ddf03bdc0c4fbe23b0273ccf010b))

* #92: Create way to generate endpoints at startup ([`5e2a25d`](https://github.com/ral-facilities/datagateway-api/commit/5e2a25deeb585f689e9e2c7a2c81942c8e6dd513))

* #92: Delete old endpoint modules ([`8540d39`](https://github.com/ral-facilities/datagateway-api/commit/8540d394b9fe77523bbb9be4a6dcef955d801739))

* #87: Add authentication ([`6bde478`](https://github.com/ral-facilities/datagateway-api/commit/6bde478eadb7661238ce7c13ccd0f74a28ef3369))

* #87: Update main.py ([`b7d473f`](https://github.com/ral-facilities/datagateway-api/commit/b7d473f436ea7c33186d1b61f4deee3c03d86cf8))

* #87: Add swagger to contents ([`791c993`](https://github.com/ral-facilities/datagateway-api/commit/791c99365c857beb57efcc6e025bf6b45e7ff82a))

* #87: Add querying and filtering ([`f96f152`](https://github.com/ral-facilities/datagateway-api/commit/f96f1522b705dc91a563bd3b32fdd8c8e7c05b95))

* #87:Add swagger generation ([`58faa46`](https://github.com/ral-facilities/datagateway-api/commit/58faa46b2c416b0189b1361d218b99920b3ac801))

* #87: Remove debugging line ([`2763929`](https://github.com/ral-facilities/datagateway-api/commit/27639290573af9eb2ac4a1f8bda0fe36ed3474cd))

* Merge pull request #84 from ral-facilities/70_add_db_creation_script

Add db creation script ([`c74c0cf`](https://github.com/ral-facilities/datagateway-api/commit/c74c0cf050cf87262d1e46d46c44756ff583d8b8))

* #70: rename function ([`d6d550a`](https://github.com/ral-facilities/datagateway-api/commit/d6d550a7fafdb5c382a4b26dfcf699e0e8974039))

* #70: Update running instructions ([`bc34eb9`](https://github.com/ral-facilities/datagateway-api/commit/bc34eb94aa79a4631c3e89dc3fcf175526254b4a))

* Merge pull request #90 from ral-facilities/89_use_json

Correct response types ([`5b1f878`](https://github.com/ral-facilities/datagateway-api/commit/5b1f878792c54d1a8c17b053d74aad6387c521f4))

* #89: Update column types ([`d5f0e31`](https://github.com/ral-facilities/datagateway-api/commit/d5f0e31f9a7b1c7b5d86d77fa18ab55a6e921e20))

* #89: Only convert to string for datetime ([`a99cc3a`](https://github.com/ral-facilities/datagateway-api/commit/a99cc3ad24c92003825670a86356e77678a8d74b))

* #70: Update readme ([`5bb9cf2`](https://github.com/ral-facilities/datagateway-api/commit/5bb9cf21fb75d8c99df2973acbdea28bc91893e8))

* #70: Add argument passing ([`15693c1`](https://github.com/ral-facilities/datagateway-api/commit/15693c1ec7ce3f1db6a044b174eab325b4a16e13))

* Merge branch &#39;master&#39; into 70_add_db_creation_script ([`77a2c6f`](https://github.com/ral-facilities/datagateway-api/commit/77a2c6fe0a773a3319733d6e2eb28afdfabdd901))

* #70: add datafile location ([`c9b41ec`](https://github.com/ral-facilities/datagateway-api/commit/c9b41ec42ac30c21ce95f4ecdd3ab975174072ea))

* Merge pull request #86 from ral-facilities/85_add_in_filter

#85: Add in filter ([`6ae5616`](https://github.com/ral-facilities/datagateway-api/commit/6ae5616b58d84b21a3ad3b600a37eb765d5b17fa))

* #85: Add test ([`f37081f`](https://github.com/ral-facilities/datagateway-api/commit/f37081f46f513c213fe2450c5fbe1fae4ef399dc))

* #85: Regenerate swagger ([`d555156`](https://github.com/ral-facilities/datagateway-api/commit/d5551568ecea8be403859cada4647ac1d8c20054))

* #85: Add in filter ([`5caed7f`](https://github.com/ral-facilities/datagateway-api/commit/5caed7fa57ff7e6d949386926f4589e563c3aa52))

* Merge pull request #77 from ral-facilities/75_fix_paths

#75: Change paths ([`71393af`](https://github.com/ral-facilities/datagateway-api/commit/71393af800341d63245d8ffb41f606b4d535eae7))

* #70: Update requirements ([`5a6a348`](https://github.com/ral-facilities/datagateway-api/commit/5a6a34855d3fdd11b840e846f3995c36d5f08282))

* #70: Add db creation script ([`eeb0de3`](https://github.com/ral-facilities/datagateway-api/commit/eeb0de3d6bf69425b6acff8c8cf7552d9d1dff0a))

* #70: Add util package ([`22a30bd`](https://github.com/ral-facilities/datagateway-api/commit/22a30bdf0e9b0aad5895ac11caecfa3421cb5f37))

* #75: Use __file__ to get relative paths ([`6d1f323`](https://github.com/ral-facilities/datagateway-api/commit/6d1f323c39a17424d42bcada9b31e3ba39e4c533))

* Merge branch &#39;master&#39; into 75_fix_paths ([`620a248`](https://github.com/ral-facilities/datagateway-api/commit/620a248dfb2c2bd2c6f1438e3eb322a9017dd435))

* Merge pull request #82 from ral-facilities/81_enable_cors

Enable Cors ([`1cf7dd9`](https://github.com/ral-facilities/datagateway-api/commit/1cf7dd929397d9f24ab6d21f3a2225e11fb42b39))

* #81: Use cors ([`24c782a`](https://github.com/ral-facilities/datagateway-api/commit/24c782a414aa24d5eee63ccd29d2324ff8ea6c3f))

* #81: Update requirements for flask-cors ([`2c36559`](https://github.com/ral-facilities/datagateway-api/commit/2c365591e5982b6ed245f2b34492e9413a546820))

* Merge pull request #76 from ral-facilities/72_add_requirements_file

Add requirements file ([`87e7bbb`](https://github.com/ral-facilities/datagateway-api/commit/87e7bbb1936070cd2189b22c521644964fa18a63))

* Merge pull request #79 from ral-facilities/49_fix_post_on_entities

Fix post on entities ([`beff0de`](https://github.com/ral-facilities/datagateway-api/commit/beff0dea5c4c2f16340a6ce029d00f257ab176fe))

* Merge pull request #69 from ral-facilities/68_specify_host_and_port_in_config

Specify host and port in config ([`e69981d`](https://github.com/ral-facilities/datagateway-api/commit/e69981d6ae50421be6fbc7ff443173f0d34f83a1))

* Merge pull request #66 from ral-facilities/39_only_one_include_filter

Allow only one include ([`0d97b57`](https://github.com/ral-facilities/datagateway-api/commit/0d97b578206140af74d81162955518ad1fd64ba9))

* #49: Update endpoints ([`846607b`](https://github.com/ral-facilities/datagateway-api/commit/846607b4f02c9c336ffa906f511b07be856af49f))

* #49: Allow insertion of multiple rows ([`f752db5`](https://github.com/ral-facilities/datagateway-api/commit/f752db5740d5daac6ad960b5f1cfcfd91d4a3b3d))

* #49: Make create_row return the inserted row ([`0be6159`](https://github.com/ral-facilities/datagateway-api/commit/0be6159b09ab8ecdf9da6c42ff50d5263c98d58c))

* #49: Add refresh to inserted entities ([`4d81ab9`](https://github.com/ral-facilities/datagateway-api/commit/4d81ab9bfc2b3c3add8dd7034d801b4f7bc616fc))

* Update README.md ([`a3b9551`](https://github.com/ral-facilities/datagateway-api/commit/a3b95515ee3b91c19f9fc28f36872a46fca7ca8a))

* Merge pull request #74 from ral-facilities/21_improve_testing

Improve testing ([`991210a`](https://github.com/ral-facilities/datagateway-api/commit/991210a0d3c83d7c05df6adf0f347c5af177b6ed))

* #21: Test Pascal to normal case ([`db4c1b9`](https://github.com/ral-facilities/datagateway-api/commit/db4c1b9218a6d389efe1e9e70577f13d1557a6c1))

* #21: Test helpers.py ([`3494989`](https://github.com/ral-facilities/datagateway-api/commit/3494989c2c2184cd5049bc2b73d5e9ab8ee97940))

* #21: Test FilterFactory ([`edad675`](https://github.com/ral-facilities/datagateway-api/commit/edad6751351578c07715fe0205d696e6cfc3ed6e))

* #21: Create Base FlaskAppTest ([`1fdf883`](https://github.com/ral-facilities/datagateway-api/commit/1fdf883e6dce627ddea0b7ab4a3e0cffd593f8d2))

* Merge branch &#39;master&#39; into 75_fix_paths ([`03c015b`](https://github.com/ral-facilities/datagateway-api/commit/03c015bacba545f6963ed2dc180ec39b5f358033))

* #75: Change paths ([`36ec26c`](https://github.com/ral-facilities/datagateway-api/commit/36ec26cfe94947d489bcf5a5f9f9b8792fc1605e))

* #72: Add versions and remove pip-tools ([`da0622f`](https://github.com/ral-facilities/datagateway-api/commit/da0622f2e5a693c2057af567874a37fd57ac521b))

* #72: Generate requirements.txt ([`96441b3`](https://github.com/ral-facilities/datagateway-api/commit/96441b32ab7570ad9259a909fad3ad118ed83e09))

* #72: Add requirements.in ([`b7bfc48`](https://github.com/ral-facilities/datagateway-api/commit/b7bfc48b49b1bd75c8a59a4b2462abc885d769cf))

* #72: Update README.md ([`780dee6`](https://github.com/ral-facilities/datagateway-api/commit/780dee633cc1e9b6bebeb8131440b60cc7c1fe8b))

* Merge pull request #73 from ral-facilities/71_change_file_paths

Use pathlib for config and logger ([`e2cf13d`](https://github.com/ral-facilities/datagateway-api/commit/e2cf13d609388a23c59872fdb1cc380d54472632))

* #21: Create helper tests ([`48000de`](https://github.com/ral-facilities/datagateway-api/commit/48000de4bc24c39afa8baebfe0f3ec0920ab8fa3))

* #21: Fix is_valid_json ([`d031885`](https://github.com/ral-facilities/datagateway-api/commit/d031885792b79f85a22fa34b7e960e8129c7199f))

* #21: Remove redundant tests ([`f537c5d`](https://github.com/ral-facilities/datagateway-api/commit/f537c5d1a15c996a7d5c50f796b0cf953a679412))

* #71: use pathlib ([`c2eb214`](https://github.com/ral-facilities/datagateway-api/commit/c2eb2141ccbd084cb158f18354a4e7e7aa92dfef))

* Update README.md ([`ac62218`](https://github.com/ral-facilities/datagateway-api/commit/ac62218215342c3c33192a373abad002be5fb8a5))

* #68: Specify port and host in main.py ([`6cbb1ae`](https://github.com/ral-facilities/datagateway-api/commit/6cbb1ae71b9f0ef482cdd8f113fd0d9499831746))

* #68: Update config.py ([`3a34c3b`](https://github.com/ral-facilities/datagateway-api/commit/3a34c3be7bf528c86aadb611e1b33f8a65f7ee6e))

* #68: Update example config ([`5fb2bd6`](https://github.com/ral-facilities/datagateway-api/commit/5fb2bd641198bb6b0a1c98f7bc875737a49c814e))

* #39: Regenerate swagger ([`3702328`](https://github.com/ral-facilities/datagateway-api/commit/37023288cc9750c84902d22a5acbc9a270689639))

* #39: Update swagger ([`c7031f2`](https://github.com/ral-facilities/datagateway-api/commit/c7031f250caec5db187f30c1804339af9fbf768e))

* Merge branch &#39;master&#39; into 39_only_one_include_filter ([`2e8e41d`](https://github.com/ral-facilities/datagateway-api/commit/2e8e41d80f9cf1df535a79cc35770645a09e6b63))

* Merge pull request #67 from ral-facilities/48_change_session_handling

Change handling of session ([`c6ddda4`](https://github.com/ral-facilities/datagateway-api/commit/c6ddda49bb5a5d8d8f2ae1a37658d9bfac46eb1b))

* Merge pull request #65 from ral-facilities/50_update_swagger

Update swagger generation ([`444342a`](https://github.com/ral-facilities/datagateway-api/commit/444342a5f762965ec58f981c208e920e821ff67d))

* Create LICENSE ([`663b68c`](https://github.com/ral-facilities/datagateway-api/commit/663b68cc68fabf62c00b197b8d912f516fc6b974))

* Merge branch &#39;master&#39; into 50_update_swagger ([`9d5962c`](https://github.com/ral-facilities/datagateway-api/commit/9d5962ca65e00c2a82bafa3577eafa70e765dca3))

* Update README.md ([`3a0cf98`](https://github.com/ral-facilities/datagateway-api/commit/3a0cf98a43b2aacb02c5ad3b07246d9abc848c17))

* #48: Move to using with ([`f6de8e2`](https://github.com/ral-facilities/datagateway-api/commit/f6de8e2422005f1d19434119dd56ef94d1ef78eb))

* #48: Remove old closing of sessions ([`77aeb54`](https://github.com/ral-facilities/datagateway-api/commit/77aeb54667194b77b04a14e9e12a251b51c88799))

* #48: Allow use of with keyword with Queries ([`ee9265a`](https://github.com/ral-facilities/datagateway-api/commit/ee9265a6f9711250f541fedf5cd6bffaf5d9e7a5))

* #39: Handle exception and send response ([`b755af3`](https://github.com/ral-facilities/datagateway-api/commit/b755af3d18feef84241d655699a76172cc8e1a09))

* #39: Raise exception if multiple includes applied ([`31e5b6e`](https://github.com/ral-facilities/datagateway-api/commit/31e5b6e871a1d1e9d70040175b8fa2e10ec5634d))

* #39: Add MultipleIncludeError ([`13ac77e`](https://github.com/ral-facilities/datagateway-api/commit/13ac77ebffebdfbdf45efe0a033f8c4365204c66))

* #50: Regenerate openapi.yaml ([`b2acf40`](https://github.com/ral-facilities/datagateway-api/commit/b2acf4036660c95b235de10722a81c9ba7474a98))

* #50: Use pyyaml to write to file ([`0f759ba`](https://github.com/ral-facilities/datagateway-api/commit/0f759bab3361ebfdbc6864b256e0f8b542c24f39))

* #50: Create SwaggerSpec class ([`e2c2c8f`](https://github.com/ral-facilities/datagateway-api/commit/e2c2c8f544d880c36ff5e41bc82cc2f1f094f8b5))

* #50: Create an entity class ([`412a895`](https://github.com/ral-facilities/datagateway-api/commit/412a8952802d7e45f54234e68c652b0897b8f1cb))

* #50: Create a parameter class ([`d34cef8`](https://github.com/ral-facilities/datagateway-api/commit/d34cef84295fe2a316c04964e1c3c2b503dfb0fb))

* #50: Use pyyaml instead of f strings ([`abe4252`](https://github.com/ral-facilities/datagateway-api/commit/abe4252bd59cb03047dd7bde0fb572d2dc5ad0d2))

* #50: Remove unused import ([`bb2f913`](https://github.com/ral-facilities/datagateway-api/commit/bb2f913e4f829036fdf81698d5761276f87c0fd2))

* Merge pull request #64 from ral-facilities/61_return_401_for_no_credentials

Handle no credentials ([`40a3463`](https://github.com/ral-facilities/datagateway-api/commit/40a346325ec4d79117218e11e99f6b7231c8ba30))

* Merge branch &#39;master&#39; into 61_return_401_for_no_credentials ([`8e46366`](https://github.com/ral-facilities/datagateway-api/commit/8e46366d86611a1b040e35d0c15f60cd36a1f94f))

* #61: Handle no credentials ([`e1cda06`](https://github.com/ral-facilities/datagateway-api/commit/e1cda06acf35c4eee9899c92150dcba5ec786e85))

* #61: Add missing credentials exception ([`ccef03e`](https://github.com/ral-facilities/datagateway-api/commit/ccef03eb21a4598bcb43ca44ccc17e977b0567f4))

* Merge pull request #57 from ral-facilities/51_refactoring_filters

Refactor getting filters ([`bd206b1`](https://github.com/ral-facilities/datagateway-api/commit/bd206b1b680802ce49363607e0cf4f0205d6a9c4))

* #51: Update _get_results_with_include ([`1b2a389`](https://github.com/ral-facilities/datagateway-api/commit/1b2a3898acc17daa432aa3721de2dfb1b5a54a7a))

* Merge pull request #63 from ral-facilities/59_handle_trailing_slashes

Handle trailing slashes ([`c3eb99f`](https://github.com/ral-facilities/datagateway-api/commit/c3eb99f6b564d3261739f156bf2b9318c74bf623))

* Merge pull request #62 from ral-facilities/60_remove_config

Remove config from repo ([`ca0a466`](https://github.com/ral-facilities/datagateway-api/commit/ca0a4660c4acddaec0a68928ed6e70c8c7911602))

* #59: Handle trailing slashses ([`3b6d8c6`](https://github.com/ral-facilities/datagateway-api/commit/3b6d8c622154270606a4282f8ae62947aa3a45e0))

* #60: Update gitignore ([`f912dd8`](https://github.com/ral-facilities/datagateway-api/commit/f912dd804854ebf1731207fed3610fb71ceffabe))

* #60: Delete config ([`857263c`](https://github.com/ral-facilities/datagateway-api/commit/857263c48d841ca3cf3ac4694ce64a1e92d45954))

* Merge branch &#39;master&#39; into 51_refactoring_filters ([`01c0a1c`](https://github.com/ral-facilities/datagateway-api/commit/01c0a1ce4eb16185ce80f4ea957c7fb231641a5d))

* Merge pull request #58 from ral-facilities/54_use_enum_for_parameter_type

Use enum for parameter type ([`db5330d`](https://github.com/ral-facilities/datagateway-api/commit/db5330d46302bccd8d7e3ca549ce6ddbb65f4d07))

* Merge pull request #56 from ral-facilities/41_add_ability_to_get_distinct_values

Add ability to get distinct values ([`5695e3f`](https://github.com/ral-facilities/datagateway-api/commit/5695e3f0b67d6fc9d0632ffcf1df7b979332ac89))

* #54: Use EnumAsInteger Column type ([`ba49d1e`](https://github.com/ral-facilities/datagateway-api/commit/ba49d1ef2800f2d62963bde4c7812987d3945f6b))

* #54: Fix docstring ([`10f974e`](https://github.com/ral-facilities/datagateway-api/commit/10f974e0b998833663a5837c0eb47b919bf1acc3))

* #54: Extend TypeDecorator ([`4cec6df`](https://github.com/ral-facilities/datagateway-api/commit/4cec6df2feddc52f2926d68ed0bcbfe525ceaf33))

* #54: Create ValueTypeEnum ([`9360b8b`](https://github.com/ral-facilities/datagateway-api/commit/9360b8b62ea90674d04e939c6bae64222f107db8))

* #54: Add DatabaseError exception ([`0eb5d9d`](https://github.com/ral-facilities/datagateway-api/commit/0eb5d9d076eddc4487072eb4ed8871e269936a87))

* #41: Whitespace changes ([`12adcab`](https://github.com/ral-facilities/datagateway-api/commit/12adcab1c8b912db69eb255f4e79e9f872627484))

* Merge branch &#39;master&#39; into 41_add_ability_to_get_distinct_values ([`d8a8499`](https://github.com/ral-facilities/datagateway-api/commit/d8a8499850b92073727105b9a690855df9a98ed4))

* #41: Add and use function for distinct fields ([`2f85368`](https://github.com/ral-facilities/datagateway-api/commit/2f853683a8a13b38570d283990574d87e22659b5))

* #41: Extract include into function ([`eebf29a`](https://github.com/ral-facilities/datagateway-api/commit/eebf29af4826c16ef5b13cdc9d58cc500d2a6536))

* #41: Update Factory ([`1b76f38`](https://github.com/ral-facilities/datagateway-api/commit/1b76f38782e0e33bb2812e9567380f42b5b121ca))

* #41: Add implementation to filter ([`2a496a0`](https://github.com/ral-facilities/datagateway-api/commit/2a496a0e082062600e813cd43eba8812fdc00f6d))

* #41: Add is_distinct bool to ReadQuery ([`cc2459a`](https://github.com/ral-facilities/datagateway-api/commit/cc2459affb724a9b6fbeca97427bb213f6c6e728))

* Merge pull request #55 from ral-facilities/52_fix_isis_queries

#52 - fix accidentally pluralised entities ([`bb0a2a3`](https://github.com/ral-facilities/datagateway-api/commit/bb0a2a3fe671b7978a55bc8dcd5614033374301b))

* #52 - fix accidentally pluralised entities ([`9a3c8c9`](https://github.com/ral-facilities/datagateway-api/commit/9a3c8c9e800a1266c7fe1c39ce2501c5dcd3e446))

* Merge pull request #44 from ral-facilities/43_allow_many_to_many_includes

Allow many to many includes ([`82e7dcb`](https://github.com/ral-facilities/datagateway-api/commit/82e7dcb836e8202ead51d73519916141155bb640))

* Merge pull request #53 from ral-facilities/52_fix_isis_queries

Fix ISIS facility cycles &amp; ISIS investigations queries ([`fb16374`](https://github.com/ral-facilities/datagateway-api/commit/fb16374a1b300251c72a526b3497faef8b976dc4))

* #51: Use updated include filter ([`ce6beb7`](https://github.com/ral-facilities/datagateway-api/commit/ce6beb7182ae87eb326351ebc7e5ef313aec572d))

* #51: Change include filter ([`958da33`](https://github.com/ral-facilities/datagateway-api/commit/958da331dcc1e1e7f470258ddf17f5a8deab127c))

* #51: Use add filters method ([`147ec49`](https://github.com/ral-facilities/datagateway-api/commit/147ec4911e4a9ffb76cd4f4e3ff9ccf411b13539))

* #51: Add method to add a list of filters to filter handler ([`9c6cfb1`](https://github.com/ral-facilities/datagateway-api/commit/9c6cfb1e0bc546e275a4e875262d93a87edb6d7c))

* #51: Make Querystring filter method return filter objects ([`33ea947`](https://github.com/ral-facilities/datagateway-api/commit/33ea9478c875b81c3be87d2fc0c2e5cdbc10aa97))

* #52: fix ISIS facility cycles &amp; ISIS investigations queries ([`609ce2a`](https://github.com/ral-facilities/datagateway-api/commit/609ce2a7c1707c876e58bc6e7f19981450b46f3a))

* Merge branch &#39;master&#39; into 43_allow_many_to_many_includes ([`7ec4f3f`](https://github.com/ral-facilities/datagateway-api/commit/7ec4f3fe99759ea8bb8abb3b3a500dcd3ecf2693))

* #43: Move included entities to nested array ([`100d004`](https://github.com/ral-facilities/datagateway-api/commit/100d0046e63ba8c1963acefa553789e98d5ed818))

* Merge pull request #38 from ral-facilities/34_add_table_specific_endpoints

34 add table specific endpoints ([`43638e2`](https://github.com/ral-facilities/datagateway-api/commit/43638e2a3e8ba964c65730215dab86a93f3a6000))

* #34: Fix indent ([`5511c5c`](https://github.com/ral-facilities/datagateway-api/commit/5511c5cd243344d31442bf0af14606c7d5cdbbd3))

* #34: Remove table method from where filter ([`8b81ea4`](https://github.com/ral-facilities/datagateway-api/commit/8b81ea47f3eb0d45c873e9c4531ba406f78e4de4))

* #34: Use joins on investigation user queries ([`266c644`](https://github.com/ral-facilities/datagateway-api/commit/266c64489ac6164ba509d95f96568357d8a2aac1))

* #34: Minor refactor ([`957cf3a`](https://github.com/ral-facilities/datagateway-api/commit/957cf3acc14fbdbd93dae2e35f12cb6d9d3610d3))

* #34: Use joins for cycle investigations query ([`0c9046a`](https://github.com/ral-facilities/datagateway-api/commit/0c9046ac93d5b0e3c47c4997cd843a38f9fd9e25))

* #34: Use joins ([`9c1393b`](https://github.com/ral-facilities/datagateway-api/commit/9c1393b865753cd44992b95367c53b4e15a72371))

* #34: Add way to close all sessions in queries ([`697c042`](https://github.com/ral-facilities/datagateway-api/commit/697c04255e081999b5b42b272f9a3c33f9192b55))

* #34: Change how filters are set ([`6bbabda`](https://github.com/ral-facilities/datagateway-api/commit/6bbabda3f382c0e80de72da5e092c56a923308b3))

* #34: Make method non static ([`cd95508`](https://github.com/ral-facilities/datagateway-api/commit/cd95508332fb3f8befb8fd1b66f6832c3f46e962))

* #34: Override get_all_results ([`ae5aad6`](https://github.com/ral-facilities/datagateway-api/commit/ae5aad6411375ab3ab9b34762224af6d70021b8d))

* #34: Update function ([`957542f`](https://github.com/ral-facilities/datagateway-api/commit/957542fe2db4df4bf319ba8367bf340ce7850a82))

* #34: Add new method of getting facility cycles ([`a8c68cb`](https://github.com/ral-facilities/datagateway-api/commit/a8c68cb2623d7ffffde3795449c1069511762970))

* #34: Change to only filter the start dates ([`e0ea0c4`](https://github.com/ral-facilities/datagateway-api/commit/e0ea0c41faed763c695fd2134f21502cd03f3d13))

* #34: Change class name ([`2d51bc0`](https://github.com/ral-facilities/datagateway-api/commit/2d51bc042bf2f2e080feff3668a2ab5d1aa2201c))

* #34: Change class name ([`fb2666e`](https://github.com/ral-facilities/datagateway-api/commit/fb2666ec441581207c099ecfb42dbf399c431bba))

* #41: Add Distinct field filter and update precedence ([`cb67f07`](https://github.com/ral-facilities/datagateway-api/commit/cb67f076a2a45af9ef8a7e52e5cf317da2301e85))

* #41: Make precedence a required property ([`a217699`](https://github.com/ral-facilities/datagateway-api/commit/a2176990c8a34c3bf41f2c995cb085407cd7da9d))

* #34: Add missing filter params ([`1f6a915`](https://github.com/ral-facilities/datagateway-api/commit/1f6a915f5902183a0aaa6aa8108b966cba9b150c))

* #34: Update docstring ([`cbec9d2`](https://github.com/ral-facilities/datagateway-api/commit/cbec9d2d5886eb0fe99807b4e5ff0032db3d93fd))

* #34: Add missing filter param ([`d8156fb`](https://github.com/ral-facilities/datagateway-api/commit/d8156fb1efaf11bd508718457256fd7e5a0b82e7))

* #34: Update endpoints ([`c7026b3`](https://github.com/ral-facilities/datagateway-api/commit/c7026b349711d9e335f1a0b45783fbb5cc99b4eb))

* #34: Update count function ([`7b32a1f`](https://github.com/ral-facilities/datagateway-api/commit/7b32a1f24ad6d6df50eb78316ff119eeb563415b))

* #34: Use InstrumentCycleInvestigation query ([`98121f8`](https://github.com/ral-facilities/datagateway-api/commit/98121f842d59d7bd24ac113a9161bc12143315f1))

* #34: Create instrumentInCycleInvestigationsQuery ([`30af58c`](https://github.com/ral-facilities/datagateway-api/commit/30af58ce501bd81760b13b252331fe0ac197e7ad))

* #34: Update endpoint ([`c68d930`](https://github.com/ral-facilities/datagateway-api/commit/c68d930de4408ef60ce4fae51bc94e55363f0325))

* #34: Update docstring ([`83754b4`](https://github.com/ral-facilities/datagateway-api/commit/83754b4a1b1926797454a9969b56db91ecf87153))

* #34: Add filters ([`b7648e2`](https://github.com/ral-facilities/datagateway-api/commit/b7648e252731b17b24b208840471dc4caff0fda4))

* #34: Refactor and allow filters ([`013adbf`](https://github.com/ral-facilities/datagateway-api/commit/013adbf3095ae4d4a8625792cd163cbdf677e691))

* #34: Create InstrumentFacilityCyclesQuery ([`fc9ce04`](https://github.com/ral-facilities/datagateway-api/commit/fc9ce0428070e37a3d751644a8c8eb0f3cb667c8))

* #34: Refactor get_investigations_for_user ([`2676563`](https://github.com/ral-facilities/datagateway-api/commit/2676563a81a353de6458f80726a02a545c46c055))

* #34: Refactor get rows_by_filter ([`452ce6d`](https://github.com/ral-facilities/datagateway-api/commit/452ce6dddf536c84b9f3d42ba900c0d79afd3522))

* #34: Rename to UserInvestigations ([`bf29c0b`](https://github.com/ral-facilities/datagateway-api/commit/bf29c0b79de95db9f5c5bf276ad35b9b372e5007))

* #34: Change case ([`2613ed3`](https://github.com/ral-facilities/datagateway-api/commit/2613ed3024cb587bc2f9ae40cf153085542ccdc3))

* #34: Add resources to api ([`3ffa3fa`](https://github.com/ral-facilities/datagateway-api/commit/3ffa3fa3f9dafbcf83ffcc2a837e5599c4894814))

* #34: Add count ([`127e6be`](https://github.com/ral-facilities/datagateway-api/commit/127e6be9cc89d29eb7494155a21f2904d8018814))

* #34: Add final resources ([`cfc9b8d`](https://github.com/ral-facilities/datagateway-api/commit/cfc9b8db4c4058aff6e884b0b84abfad5cc09317))

* #34: Add investigations for instruments in cycle ([`c709dd6`](https://github.com/ral-facilities/datagateway-api/commit/c709dd6bceee267bb08ac5e398351fafae3684fe))

* #34: Temporary fix of 48 ([`225f182`](https://github.com/ral-facilities/datagateway-api/commit/225f182d69e15890b07a94179584ae4ea76e2d4c))

* Merge branch &#39;master&#39; into 34_add_table_specific_endpoints ([`bd06b89`](https://github.com/ral-facilities/datagateway-api/commit/bd06b8963e270558e3f318f6ec695e38b0a9ced1))

* Merge pull request #45 from ral-facilities/23_improve_logging

Improve logging ([`26b15dc`](https://github.com/ral-facilities/datagateway-api/commit/26b15dcac0d5cfb97add5e3342f5cbc78def61a1))

* Merge pull request #47 from ral-facilities/46_change_to_int_on_endpoint_id

Change endpoint ID type to int ([`38c8d4a`](https://github.com/ral-facilities/datagateway-api/commit/38c8d4aab242cc781e5eee50016afb18caca5d2e))

* #34: Update resource class for count ([`de74984`](https://github.com/ral-facilities/datagateway-api/commit/de749844914c8dedd9c9b1b7c7ad21498a168e69))

* #34: Add cycles count function ([`2a08152`](https://github.com/ral-facilities/datagateway-api/commit/2a081527ffd233ea43d6ce32df7628a3fdce1895))

* #34: Update endpoint resource ([`8256c1d`](https://github.com/ral-facilities/datagateway-api/commit/8256c1d36dcabd81f17371d010e39f36ef32450a))

* #34: Add get cycles for instrument ([`e5180cd`](https://github.com/ral-facilities/datagateway-api/commit/e5180cd0e4f12b642bc3261673bb71c80ac05c65))

* #34: Use get investigations count in resource ([`ccdec3b`](https://github.com/ral-facilities/datagateway-api/commit/ccdec3b6ce8f93848adef0e12849acc3151f336d))

* #34: Update _get_table_to_filter ([`3261184`](https://github.com/ral-facilities/datagateway-api/commit/3261184346cc243a6e1014ce9d0b2deb3dc6bf2c))

* #34: Add get investigation count function ([`9e8e0e5`](https://github.com/ral-facilities/datagateway-api/commit/9e8e0e52ab46eacb34b72cf5360d7ceee2679110))

* #34: Add ISISInvestigationsCountQuery ([`31677c3`](https://github.com/ral-facilities/datagateway-api/commit/31677c33fc0177838adcac229569e19932ba9e61))

* #34: Add Missing docstring ([`455bfdd`](https://github.com/ral-facilities/datagateway-api/commit/455bfdde61e9d9b3254170e3988ff8e255b2c6ce))

* #34: Add ISIS User Investigations endpoint ([`ccfb01e`](https://github.com/ral-facilities/datagateway-api/commit/ccfb01e85cbc1766a73358e878a6f6194c16d567))

* #34: create get_investigations_for_user ([`885ba6f`](https://github.com/ral-facilities/datagateway-api/commit/885ba6f08430e5c9c955cfccecba7668f187266f))

* #34: Change how table is selected for filtering ([`f0dd894`](https://github.com/ral-facilities/datagateway-api/commit/f0dd894c852536a81bd9377940617ef926dae73e))

* Merge branch &#39;master&#39; into 34_add_table_specific_endpoints ([`9016789`](https://github.com/ral-facilities/datagateway-api/commit/9016789d9fd0cab4b7a25eb8d07cf02e3223a3e6))

* #34: Add _get_table_to_filter method ([`ac2b923`](https://github.com/ral-facilities/datagateway-api/commit/ac2b92316477a9cfe2f93d88e12f92564dbe91df))

* #34: Create ISISInvestigationsQuery class ([`c8e85c4`](https://github.com/ral-facilities/datagateway-api/commit/c8e85c4e73bf8e44aa508223396acb72db85d51e))

* #34: Change type of endpoint id to int ([`f55879c`](https://github.com/ral-facilities/datagateway-api/commit/f55879c45c3d664686d9747ca8a4d6c87bae6457))

* #46: Update README.md ([`968aa0c`](https://github.com/ral-facilities/datagateway-api/commit/968aa0c92e58dd3e7d3d6909bd144a87a5fcaa5d))

* #46: Change to int ([`cea1d05`](https://github.com/ral-facilities/datagateway-api/commit/cea1d053f70ca313b2bb1adac54591f51a3a1a77))

* #23: Change to show traceback ([`e763ebb`](https://github.com/ral-facilities/datagateway-api/commit/e763ebb72954c6dfde6d31db519dcd2a9adca6cb))

* #43: Refactor for readability ([`f88b6bc`](https://github.com/ral-facilities/datagateway-api/commit/f88b6bc6b93388f38c6449f13fa10174b61c28e7))

* #43: Allow many to many includes ([`107e7c6`](https://github.com/ral-facilities/datagateway-api/commit/107e7c6517254b35f3291734f689506df1b33fde))

* Merge pull request #40 from ral-facilities/32_improve_include_filtering

Improve include filtering ([`60c668d`](https://github.com/ral-facilities/datagateway-api/commit/60c668d2018f23cc93f224b4fc2dfcddac5e05a7))

* #32: User ternary ([`b60e2d1`](https://github.com/ral-facilities/datagateway-api/commit/b60e2d146f7e3650819c8a8ad152e72ba23a1010))

* #32: Change to_nested_dict ([`cdd1133`](https://github.com/ral-facilities/datagateway-api/commit/cdd1133535f9583634866bfd4cc5294b7e042261))

* #32: Add get_related_entity ([`6e8c8c1`](https://github.com/ral-facilities/datagateway-api/commit/6e8c8c1d9e2817e9dde50ea7e854340dcdfe0f2b))

* Merge pull request #37 from ral-facilities/18_add_more_where_filtering_types

Add Like, less than and greater than where filtering. ([`7b6adef`](https://github.com/ral-facilities/datagateway-api/commit/7b6adef85a59dc824e70672eab09e5a0d04fc1e6))

* #18: Fix typo ([`b2d2750`](https://github.com/ral-facilities/datagateway-api/commit/b2d27500d32b56b7b82602f2a7bfdb5021e3f60b))

* #18: Change to lte and gte ([`a9fb2fa`](https://github.com/ral-facilities/datagateway-api/commit/a9fb2fa68e2146bc2ed77e7c63016fc921a7ad87))

* #34: Add resources to api ([`8fbbaeb`](https://github.com/ral-facilities/datagateway-api/commit/8fbbaebb4de5f0ce5cad442e62971070d66eb002))

* #34: Add table specific resource classes ([`7f13768`](https://github.com/ral-facilities/datagateway-api/commit/7f13768e0b8a7bd02e953f85f41a4cb01b978cb6))

* #18: Implement greater than and less than filters ([`03f603c`](https://github.com/ral-facilities/datagateway-api/commit/03f603c958510e4fe9ce5074c46dd49378c05037))

* #18: Correct entity handling on update ([`086478c`](https://github.com/ral-facilities/datagateway-api/commit/086478cca9cd13fcab4ef58fcb9141a550d9a88b))

* #18: Update get_row_by_id ([`171ad98`](https://github.com/ral-facilities/datagateway-api/commit/171ad980715586114c49bc26969c15cd049f635f))

* #18: Update filter factory ([`f7335c3`](https://github.com/ral-facilities/datagateway-api/commit/f7335c388b9f602a8d5b5f50917f613af1179545))

* #18: Add like filtering ([`1382e9b`](https://github.com/ral-facilities/datagateway-api/commit/1382e9bfd6535556ee223303cb2eeb0193d84990))

* Merge pull request #36 from ral-facilities/31_change_format_of_query_filters

Change format of accepted query strings ([`fa374f7`](https://github.com/ral-facilities/datagateway-api/commit/fa374f73ffebbd37dec179eb57f233c5ed92d721))

* #31: Change format of accepted query strings ([`63aa305`](https://github.com/ral-facilities/datagateway-api/commit/63aa3054feebd8b051fee0c38093d6c0b6a1ee1f))

* Merge pull request #35 from ral-facilities/30_use_order_of_operations

Use order of operations for filtering ([`2f59010`](https://github.com/ral-facilities/datagateway-api/commit/2f59010298d5092e005453a40e78500ff66abe90))

* Merge pull request #29 from ral-facilities/use_classes_for_queries_and_filters

Use classes for queries and filters, and create SessionManager ([`c6f0b87`](https://github.com/ral-facilities/datagateway-api/commit/c6f0b876ae922202d9000271db51c0d3cc055661))

* #30: Remove is_limited ([`38b9ec0`](https://github.com/ral-facilities/datagateway-api/commit/38b9ec087909e3a7bb22a5a73953b122e7d0574b))

* #30: Use filter handler ([`288b21b`](https://github.com/ral-facilities/datagateway-api/commit/288b21b322c07bfb86d92e334cab53b6f5849d28))

* #30: Add precedence to filters ([`31fbe83`](https://github.com/ral-facilities/datagateway-api/commit/31fbe8343fb2b6e9429ad0455154d093a03b6c74))

* #30: Create order handler ([`bac726e`](https://github.com/ral-facilities/datagateway-api/commit/bac726e9ea1196bfa9511a8be6627e50f3933a36))

* Merge branch &#39;master&#39; into use_classes_for_queries_and_filters ([`70844ce`](https://github.com/ral-facilities/datagateway-api/commit/70844cec5d9aac0bb629be30ff2de12bebb7a993))

* Merge pull request #27 from ral-facilities/15_generate_swagger

Generation of openapi.yaml ([`22bfd1e`](https://github.com/ral-facilities/datagateway-api/commit/22bfd1e6bfd195ac155f8956eef00fec4dec8c52))

* Remove try added in error ([`3728d89`](https://github.com/ral-facilities/datagateway-api/commit/3728d89df5eb23f429a4ba32927a4a11b6a31afe))

* Fix Indentation ([`37b28be`](https://github.com/ral-facilities/datagateway-api/commit/37b28be0e66f8e3ffbf3f8a2fbf4fced64bdc817))

* Move session closing ([`eff2931`](https://github.com/ral-facilities/datagateway-api/commit/eff2931abaf257df38d35921099f770241c5ad07))

* Move the closing of the session ([`1f38a3c`](https://github.com/ral-facilities/datagateway-api/commit/1f38a3c69176303b2e9ae08c33bef3772a7dc913))

* #15: Use config to control generation ([`735eda4`](https://github.com/ral-facilities/datagateway-api/commit/735eda40118a1d9b49af085775c520f2d8705703))

* #15: Add is_generate_swagger to config class ([`cd1668d`](https://github.com/ral-facilities/datagateway-api/commit/cd1668dc5beb0e5dc5a813d26398c2157ca03327))

* #15: Add swagger generation to config files ([`468bf73`](https://github.com/ral-facilities/datagateway-api/commit/468bf73e4a24b3305b81c79958b13730bad6b126))

* #15: Fix merge conflict ([`fb9972e`](https://github.com/ral-facilities/datagateway-api/commit/fb9972ebaf8fc8b881014f29c89cc11f775e9dde))

* #15: Fix crash when not generating ([`6dcdc7b`](https://github.com/ral-facilities/datagateway-api/commit/6dcdc7b263284e1acc429bc5f7a705cb8d67803b))

* #15: Regenerate Swagger ([`0e4a7c0`](https://github.com/ral-facilities/datagateway-api/commit/0e4a7c0c800724901327872cb5defc9fe2227c5d))

* #15: Remove limit filter from findOne ([`5a50472`](https://github.com/ral-facilities/datagateway-api/commit/5a504729b9bd580c22ba52a257e0d68a7ab2449c))

* #15: Remove unused filters from count ([`56fdfe9`](https://github.com/ral-facilities/datagateway-api/commit/56fdfe907c2a3e031e5b52d807fe45c03bf4bb7d))

* Merge pull request #28 from ral-facilities/13_setup_config_file

Use a config file ([`251d2bd`](https://github.com/ral-facilities/datagateway-api/commit/251d2bd32c17061b4b6147bc3f58185b6011226b))

* Fix indentation ([`1d1092f`](https://github.com/ral-facilities/datagateway-api/commit/1d1092f25dcf3c879d85dfcb99d2cfdcc10ff2db))

* Make sure session is closed correctly ([`075f476`](https://github.com/ral-facilities/datagateway-api/commit/075f4768504306acc6c0197c984196275a06bc54))

* Add pool_size and only create 1 engine/factory ([`beb9df8`](https://github.com/ral-facilities/datagateway-api/commit/beb9df8d9703029a1cc13ff67cb39aba0bb907fb))

* Increase pool size ([`85304fc`](https://github.com/ral-facilities/datagateway-api/commit/85304fc6455884daee7358046c6ec014d2b0ca4c))

* Change filtered row count function ([`e6f53da`](https://github.com/ral-facilities/datagateway-api/commit/e6f53da4e9054983a96508d217b4ea692ef14405))

* Remove duplicated queries ([`b246805`](https://github.com/ral-facilities/datagateway-api/commit/b2468056c47a7b40d6ba1f06960b36b1ccb9d5c7))

* Create a count query class ([`b6897fb`](https://github.com/ral-facilities/datagateway-api/commit/b6897fbbd56092bc45fab5d2d8c7fabde1f1b2e3))

* Use the new scoped_session SessionManager ([`12affc7`](https://github.com/ral-facilities/datagateway-api/commit/12affc7bf81989a61b454729a9605e0ed438c9bd))

* Move the session manager and use scoped_session ([`3106203`](https://github.com/ral-facilities/datagateway-api/commit/31062038b4fd368a743a0f198487d22dd0a88828))

* Fix order filter ([`7841559`](https://github.com/ral-facilities/datagateway-api/commit/7841559f44d08738364757da7a047484a7319098))

* Use SessionManager ([`719aed7`](https://github.com/ral-facilities/datagateway-api/commit/719aed7cdb0304c3a43dfedc25f58262493999c8))

* Create SessionManager ([`0e7dfa4`](https://github.com/ral-facilities/datagateway-api/commit/0e7dfa443eecdbba134d2cc2d53fdf96a4df61cb))

* update get_rows_by_filter ([`27a977c`](https://github.com/ral-facilities/datagateway-api/commit/27a977c592176bc80e9b5f46b292a80102ee574c))

* Update update_row_from_id ([`d874231`](https://github.com/ral-facilities/datagateway-api/commit/d8742314ced508babf677220115ffb271a3eb1e8))

* Update delete_row_by_id ([`62eb47e`](https://github.com/ral-facilities/datagateway-api/commit/62eb47e2a3fd5f1af5f27a28dacf76112dce6dcb))

* Update get_row_by_id ([`630f683`](https://github.com/ral-facilities/datagateway-api/commit/630f6832dec5d3f3c959ec166a239b29ff6f640a))

* Update insert_row_into_table ([`60b3c98`](https://github.com/ral-facilities/datagateway-api/commit/60b3c985fad73b4f4e17fb0294dd46a2b34a76e4))

* Update Create Row from JSON ([`58e4dba`](https://github.com/ral-facilities/datagateway-api/commit/58e4dbaf8dce8275b6d020af0811218c0770ef45))

* Create QueryFilterFactory ([`a2d8050`](https://github.com/ral-facilities/datagateway-api/commit/a2d8050c0961c4fbd5c6175834210260a809a8bf))

* Create SkipFilter ([`f9600ec`](https://github.com/ral-facilities/datagateway-api/commit/f9600ece981d7d6f159af01c2cd4cbc313e26361))

* Create IncludeFilter ([`7e855ce`](https://github.com/ral-facilities/datagateway-api/commit/7e855ceb8d3891a6df69f87ddfc425b6e8514ed9))

* Create LimitFilter ([`a0b18a8`](https://github.com/ral-facilities/datagateway-api/commit/a0b18a88ed1d798e8256aa6a9e6594c04d158c47))

* Create OrderFilter ([`67bf964`](https://github.com/ral-facilities/datagateway-api/commit/67bf9641bbe3dad06d4c216bcec497aba49e525d))

* Create WhereFilter ([`202c009`](https://github.com/ral-facilities/datagateway-api/commit/202c009d15d360ac9b4dc73a916af70af8133106))

* Create QueryFilter ([`40af194`](https://github.com/ral-facilities/datagateway-api/commit/40af1941207b21de5c923e9415d540a35a1b6c34))

* Create DeleteQuery ([`af62c14`](https://github.com/ral-facilities/datagateway-api/commit/af62c1490acf191c32ec4316ce9a2f9b2c0cc530))

* Create UpdateQuery ([`0c63010`](https://github.com/ral-facilities/datagateway-api/commit/0c630109f28bc60d9be912137a807eed77f3b502))

* Create CreateQuery ([`e3bf3b3`](https://github.com/ral-facilities/datagateway-api/commit/e3bf3b34e2dd8dc714f98f84d9f08f80ecfe66a9))

* Create Read Query ([`d8f5ab8`](https://github.com/ral-facilities/datagateway-api/commit/d8f5ab848735fd233963ab0dd07ebc78a50fc407))

* Create abstract base query class ([`b6b92b5`](https://github.com/ral-facilities/datagateway-api/commit/b6b92b50065b9db38aea55b69f361d172ef23610))

* #15: Allow generator to be disabled ([`33ef610`](https://github.com/ral-facilities/datagateway-api/commit/33ef610f9a310582165da54afcda78fd9df60aa2))

* #15: Change path ([`e6e418a`](https://github.com/ral-facilities/datagateway-api/commit/e6e418ade496a08aefcd39e4d8076b148ca69ba1))

* #13: Add example config ([`fb96925`](https://github.com/ral-facilities/datagateway-api/commit/fb96925c810f81c93b8835e806727dcb232f39f7))

* #13: Exit on missing config values ([`eec6821`](https://github.com/ral-facilities/datagateway-api/commit/eec6821b7aca62769d00c8e23ecfef4a9eeaa967))

* #13: Update README.md ([`ff81709`](https://github.com/ral-facilities/datagateway-api/commit/ff81709b074247194b0554e01764f7fda79e9221))

* #13: Use config class ([`4b6f0e9`](https://github.com/ral-facilities/datagateway-api/commit/4b6f0e93769a34d3e18b41558f594adbf4f3b416))

* #13: Create config class ([`c6bcff6`](https://github.com/ral-facilities/datagateway-api/commit/c6bcff624aded513e6646dff92f13616a4bbf627))

* #13: Add config file ([`8e414f6`](https://github.com/ral-facilities/datagateway-api/commit/8e414f6dd30dd6001ce61b2cafc390d2459b7de4))

* #15: Output of generator ([`b6e2f66`](https://github.com/ral-facilities/datagateway-api/commit/b6e2f66aaac7c6f8baf53204cb59102095b23403))

* #15: Import generator and write to file ([`8c6b525`](https://github.com/ral-facilities/datagateway-api/commit/8c6b525ef89d4ae5aa0325b3eb4c5c48d19992ca))

* #15: Apply decorator to resources ([`166fcdd`](https://github.com/ral-facilities/datagateway-api/commit/166fcddc377ddd2e2b7f024e7fe7df9426645538))

* #15: Create method to write to the file ([`a6df922`](https://github.com/ral-facilities/datagateway-api/commit/a6df922b6b3c29865871453866d1c52dcc9d75e4))

* #15: Create method to write paths ([`3687e82`](https://github.com/ral-facilities/datagateway-api/commit/3687e823ee209c5f7f1e081e2539b63f81197c7c))

* #15: Create method to write top part ([`5b0c8a0`](https://github.com/ral-facilities/datagateway-api/commit/5b0c8a0bf7c3c677077ed600cb00610f43ae8842))

* #15: Create method for converting from PascalCase ([`a6c90ce`](https://github.com/ral-facilities/datagateway-api/commit/a6c90ce9850b0614b7446e3e29328d1ec4a174f2))

* #15: Add filepath for openapi.yaml ([`6a7c575`](https://github.com/ral-facilities/datagateway-api/commit/6a7c575fd841b0decbf4b02c9ec4026cfcf01788))

* #15: Create class wrapper to collect endpoints ([`c955db0`](https://github.com/ral-facilities/datagateway-api/commit/c955db045e874ddf2ead87d04cf012e686823143))

* #15: Create init and endpoints list for SwaggerGen ([`134e74f`](https://github.com/ral-facilities/datagateway-api/commit/134e74f7e29f994fdf59e55f5557466ae0b9281f))

* #15: Create SwaggerGenerator class ([`3d4abfa`](https://github.com/ral-facilities/datagateway-api/commit/3d4abfa76d085ce80283eed9e4b0ca7b54ea6184))

* Merge pull request #16 from ral-facilities/2_add_include_and_order_filters

Add filtering ([`27cfed0`](https://github.com/ral-facilities/datagateway-api/commit/27cfed073ea8467af760865a2ab5c434e3e9bf2c))

* #2: Remove repeated arg ([`ed6ebd8`](https://github.com/ral-facilities/datagateway-api/commit/ed6ebd802df7f93ef1696fc5133d86c9f6ea0ece))

* #2: Add docstring to method ([`a9c83d7`](https://github.com/ral-facilities/datagateway-api/commit/a9c83d7c2ff1f585ae368aaf879aaf21d510f2ea))

* Merge branch &#39;master&#39; into 2_add_include_and_order_filters ([`3415ce5`](https://github.com/ral-facilities/datagateway-api/commit/3415ce51f59443cdab40541f55746b2f8c9ce4cf))

* #2: Remove print statement ([`d9716af`](https://github.com/ral-facilities/datagateway-api/commit/d9716afcd22ac99adee6f6bbbc95b3af4cc62d0f))

* #2: Use nested dict method ([`fb0fb90`](https://github.com/ral-facilities/datagateway-api/commit/fb0fb90e4621a6b1c09df587c1d21a673a673bbe))

* #2: Add nested dict method ([`875fe03`](https://github.com/ral-facilities/datagateway-api/commit/875fe035e90b73d9adf7e243a9e84ecc5a94493a))

* #2: Remove function ([`be24106`](https://github.com/ral-facilities/datagateway-api/commit/be24106e87c0e778114f7154e0b7b4ae62f3cf07))

* #2: Rename shadow named vars ([`af5c0c2`](https://github.com/ral-facilities/datagateway-api/commit/af5c0c28191d0cc06ddbf6b67c12e9b60e9d6c6a))

* #2: Change name ([`e72561d`](https://github.com/ral-facilities/datagateway-api/commit/e72561d571d396d90f392275b0f05a90673fc818))

* #2: Pull out including to func for readability ([`e305449`](https://github.com/ral-facilities/datagateway-api/commit/e305449f06ffe1d169f4ba2db1841ebd2cc6550b))

* #2: Allow includes from dictionary ([`d0a2313`](https://github.com/ral-facilities/datagateway-api/commit/d0a23134e6c757ab0ed5ed162023339ffb1225d5))

* #2: Allow including multiple relations ([`e7485a6`](https://github.com/ral-facilities/datagateway-api/commit/e7485a6e88e26568f4a48372eb406f1f8e154bb7))

* #2: Allow a single include ([`21a6e5f`](https://github.com/ral-facilities/datagateway-api/commit/21a6e5f147304be8c0a236f0e3e16dae4d812574))

* #2: Update backref on db models ([`bf00f23`](https://github.com/ral-facilities/datagateway-api/commit/bf00f23db7df0371e86868c1fbee0acfb01ce448))

* Merge pull request #20 from ral-facilities/17_allow_empty_filters

Allow empty filters ([`457630e`](https://github.com/ral-facilities/datagateway-api/commit/457630ed9de916f9da8d76d3a96e9cd0e028508b))

* #17: Allow empty filters ([`2862b7c`](https://github.com/ral-facilities/datagateway-api/commit/2862b7c9ac9583091a19e74aa8c17bcff99907c1))

* #17: Whitspace ([`c97b70a`](https://github.com/ral-facilities/datagateway-api/commit/c97b70aaf71ecdd97cf9f8f9f59a9ecaa4648e10))

* #17: throw exception if filter is empty ([`76d756b`](https://github.com/ral-facilities/datagateway-api/commit/76d756bfb9fe3b043e12ee84670d8a6f744b64f3))

* #2: Add limit and order filters ([`8f776cd`](https://github.com/ral-facilities/datagateway-api/commit/8f776cd296117473c92c89d6db8b727411a7ad6d))

* #2: Change how exceptions are logged ([`c45075a`](https://github.com/ral-facilities/datagateway-api/commit/c45075ae199b83d6e35511a419001a3f4c3260e1))

* #2: Allow ordering before limit and vise versa ([`36352dc`](https://github.com/ral-facilities/datagateway-api/commit/36352dcb3da72d688546c6baf043e2c973a39df5))

* Merge branch &#39;master&#39; into 2_add_include_and_order_filters ([`7970165`](https://github.com/ral-facilities/datagateway-api/commit/79701652561ad1b29885017b52cfb5e4b955bd01))

* Merge pull request #14 from ral-facilities/11_add_logging

Add Logging ([`47d33c8`](https://github.com/ral-facilities/datagateway-api/commit/47d33c88bfea8459796050211e768f84b14cf507))

* #11: Add logging ([`766221e`](https://github.com/ral-facilities/datagateway-api/commit/766221e983c089b32202f00b4c24cbaf2a2e7aa0))

* #11: Set up logger ([`d14d14c`](https://github.com/ral-facilities/datagateway-api/commit/d14d14c89a73bf39b3eaf7892645800464ff9c4d))

* #11: Create logger setup ([`0a079c2`](https://github.com/ral-facilities/datagateway-api/commit/0a079c2566cdd72dee6030b01ef6b99636dafd31))

* #11: Update git ignore ([`b9d9585`](https://github.com/ral-facilities/datagateway-api/commit/b9d95850852791b484f1a59a1ef07b7bfa552329))

* #11: Update gitignore ([`40461f2`](https://github.com/ral-facilities/datagateway-api/commit/40461f295015c7978ff89ae52fa0b34c024f2487))

* #11: Remove unused functions ([`463ebf8`](https://github.com/ral-facilities/datagateway-api/commit/463ebf84d850092ee3121329aa8e9a74e991c422))

* #2: Add order filtering ([`b243897`](https://github.com/ral-facilities/datagateway-api/commit/b243897c27571fb5afa5584561780404f4c9a81d))

* #2: Fix typo ([`8599c5e`](https://github.com/ral-facilities/datagateway-api/commit/8599c5e54c0b9a6ed50fdab8f335cfc504842857))

* Merge pull request #12 from ral-facilities/1_add_patch_http_method_for_non_id_endpoints

Add patch method to entity endpoints ([`2cfd027`](https://github.com/ral-facilities/datagateway-api/commit/2cfd027b8d6386c91412bd9b06b10fcce526e746))

* #1: Fix type check and get_row_id args ([`9870458`](https://github.com/ral-facilities/datagateway-api/commit/9870458199ad89e68549df3e1cb5ec28e3edf55b))

* #1: Catch BadRequestError in query wrapper ([`3986258`](https://github.com/ral-facilities/datagateway-api/commit/3986258834e1264153fce6b36464b470964b5981))

* #1: Allow single dictionary in patch function ([`07d29d4`](https://github.com/ral-facilities/datagateway-api/commit/07d29d42f18eadae29483e9ae332dce1b4d78ce4))

* #1: Add bad request exception ([`fc6b12e`](https://github.com/ral-facilities/datagateway-api/commit/fc6b12ed0e8fbddaf1c5fb936fae3a6161129b67))

* #1: Add patch to endpoints ([`02e44d2`](https://github.com/ral-facilities/datagateway-api/commit/02e44d2f34b144af4610b766244c44deba3c8984))

* #1: Add patch function ([`9b08dc6`](https://github.com/ral-facilities/datagateway-api/commit/9b08dc68b272b7c84feff5ea4b9124fb5684aa6d))

* Merge pull request #8 from ral-facilities/4_post_sessions_take_data_in_body

#4: Move credentials checking to post body ([`e58f162`](https://github.com/ral-facilities/datagateway-api/commit/e58f162cb43aff1776ed57db6974ac112e97bea2))

* Update README.md ([`542e86f`](https://github.com/ral-facilities/datagateway-api/commit/542e86f8528c0d8768a9da53bc1b8e7668102913))

* Merge pull request #10 from ral-facilities/3_imporve_instructions_on_running_app

Update instructions to run api in README.md ([`fab7fab`](https://github.com/ral-facilities/datagateway-api/commit/fab7fab7e3919aa37830de03a95c4b641b5670cd))

* #3: Update README.md with better instructions for running the api ([`9a59889`](https://github.com/ral-facilities/datagateway-api/commit/9a59889063c5758132e3319dffcaa0b860d77189))

* Merge pull request #9 from ral-facilities/5_add_bearer_authentication_type_to_auth_header

Use bearer type in authorisation header ([`2ec57a9`](https://github.com/ral-facilities/datagateway-api/commit/2ec57a9fadb9bd5cef8ddc1bbeb2e67520b00cd8))

* #5: Move to using Bearer type Authorization header ([`b3440ed`](https://github.com/ral-facilities/datagateway-api/commit/b3440ed0f2213c43a07eb253e1068f821a5536f0))

* #5: Create AuthenticationError Exception ([`fcc5ec7`](https://github.com/ral-facilities/datagateway-api/commit/fcc5ec7cbd80c709fff83b6cd3922086b2169c9a))

* #5: Update test Constant ([`de8969a`](https://github.com/ral-facilities/datagateway-api/commit/de8969a77e7bd61208f0dc2c661972b87305ceae))

* #4: Whitespace changes ([`d2fa4fc`](https://github.com/ral-facilities/datagateway-api/commit/d2fa4fcf2175431c59fc5f741bd3697332883c9a))

* #4: Update session post tests. ([`f00d46b`](https://github.com/ral-facilities/datagateway-api/commit/f00d46b41c17be34b681be5c48b342186a6dee1c))

* #4: Change how POST checks are done. ([`0cc96d2`](https://github.com/ral-facilities/datagateway-api/commit/0cc96d2cc59eccc625e9583f95d5994a858dfbcd))

* #4: Move credentials checking to post body ([`08fc3e6`](https://github.com/ral-facilities/datagateway-api/commit/08fc3e6c41a702ead09da882b578d466c0d4ab70))

* Merge pull request #7 from ral-facilities/6_entities_endpoints_dont_work

Fixes broken get method on entities endpoints ([`647dde6`](https://github.com/ral-facilities/datagateway-api/commit/647dde6eff3734ae46a47b175724fdd9dc410250))

* #6: remove unused import ([`7895d73`](https://github.com/ral-facilities/datagateway-api/commit/7895d73462263045f9b253c444b8958fbd1cd671))

* #6: Get filters from querystring ([`c4301a5`](https://github.com/ral-facilities/datagateway-api/commit/c4301a5fbdb9c338aabb6ed470d5b6429ac0347e))

* Update README.md ([`fc93eaa`](https://github.com/ral-facilities/datagateway-api/commit/fc93eaaefc23a721d939966366c6e1d304e99928))

* Update README.md ([`3506adb`](https://github.com/ral-facilities/datagateway-api/commit/3506adb7857e4b3761f383b87fb6fef2d1ed139f))

* Add test package ([`83a7699`](https://github.com/ral-facilities/datagateway-api/commit/83a769974bcfcb34c0a4682150b5931623554af9))

* Add src package ([`468e2d9`](https://github.com/ral-facilities/datagateway-api/commit/468e2d913617e909234646b1487df57420a3b0fa))

* Add common package ([`b60fb4f`](https://github.com/ral-facilities/datagateway-api/commit/b60fb4f690c96857eeed01fec7a8f29ec792145f))

* Add requirements to README.md ([`b25e8dc`](https://github.com/ral-facilities/datagateway-api/commit/b25e8dc5e49b4812e9593cdf5dcb6c98e8d8c49e))

* Add .gitignore ([`ef93915`](https://github.com/ral-facilities/datagateway-api/commit/ef9391541a53b53aa822eaa16e6694e0d9340111))

* Initial commit ([`75d60b1`](https://github.com/ral-facilities/datagateway-api/commit/75d60b1bac12d38b4fe6afa5db576373877f6141))
