# Artifact Manager Resource

This concourse plugin allows artifacts to be uploaded and retrieved based on path built from external inputs.

Currently only S3 is supported.



## Source Configuration
* `driver` : _Required_. The driver used to access the the file containing the version.


### s3 Driver
* `bucket` : _Required_. The name of the bucket.
* `region_name` : _Required_. The s3 region being targeted.
* `access_key_id` : _Required_. The AWS Key used to access the bucket.
* `secret_access_key` : _Required_. The AWS access key used to access the bucket.

## Params Configuration
* `local_path`: _Required for get._ local path to upload from.
* `remote_path`: _Required for get and put._ remote path to upload to or download from

### Path Building



## Example

Configuration with a build on patch:
```
resource_types:
- name: artifactManager-resource
  type: docker-image
  source:
    repository: lukaszz/artifact-manager-resource
    tag: 0.0.6

resources:
- name: store-files
  type: artifactManager-resource
  source:
    driver: s3
    region_name: us-west-2
    bucket: axiom.builds
    access_key_id: ((s3-key-id))
    secret_access_key: ((s3-access-key))

job:
- name: get-put-artifacts
  - get: store-files
    params:
      remote_path:
      - artifact-manager
      - type: s3
        bucket: axiom.config
        key: testing/version/api.txt
      - files
  - task: something-to-do
    file: location/of/something-to-do.yml
  - put: store-files
    params:
      local_path:
      - generated-files
      remote_path:
      - artifact-manager
      - type: file
        path: test-version/version
      - files
```

## Behavior

The path is built from passed in params. `in` takes a `remote_path` while `out` takes both a `remote_path` and `local_path`.

__`check` : Provide a timestamp__

* Provides a timestamp for the download. Currently does not actually check if the artifact exists. Since the artifacts it is getting are identified at runtime

__`in` : Download the files indicated in params__

_note_: in does not have access to local inputs, it can only build paths from remote resources and strings.

```
  - get: store-files
    params:
      remote_path:
      - artifact-manager
      - type: s3
        bucket: app.config
        key: testing/version/api.txt
      - files
```
Assuming the file in s3://app.config/testing/version/api.txt contains:
`0.0.2`

The following would create a path containing:
`artifact-manager/0.0.2/files`

the contents of `artifact-manager/0.0.2/files` would be downloaded locally into the input `store-files`

__`out`: Upload the files indicated in params__

```
  - put: store-files
    params:
      local_path:
      - generated-files
      remote_path:
      - artifact-manager
      - type: file
        path: test-version/version
      - files
```

Assuming ths file in `test-version/version` contains:
`0.0.2`

The following would create a path containing:
`artifact-manager/0.0.2/files`

The contents of the local_path `generated-files` would be uploaded to the s3 path `artifact-manager/0.0.2/files`

## Contributing

Please see Contrib.md