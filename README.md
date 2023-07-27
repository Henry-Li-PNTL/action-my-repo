# dev-github-action-auto-update-helm

此 Custom Github Action 提供下列指令:

| subcommand | desc |
| --- | --- |
| mavis-helm-update-action | 微服務 將 branch merge 進 master (微服務的master) 時，使用此 github action 會自動將 mavis helmfile.yaml 的 docker 版本號修改至最新版本號以後發 PR 到 mavis master|


The technology stack of this project:
- Python 3.11
- Typer
- Pydantic
- Pygithub
- Pydantic-settings

## Example

**mavis-helm-update-action**
```yaml=
jobs:
  your_job:
    runs-on: general
    env:
      GITHUB_ACCESS_TOKEN: ${{ secrest.GITHUB_ACCESS_TOKEN }}
    steps:
    - name: < Update Mavis Helmfile >
      if: github.event.pull_request.merged == true
      uses: pnetwork/dev-github-action-auto-update-helm@v1
      with:
        action: "mavis-helm-update-action"
        base: ${{ github.BASE_REF }}
        head: ${{ github.HEAD_REF }}
        target_repo: pare-example
        target_repo_app_version: v0.0.0
```


## Folder Structure

```
.
├── example                # Example yaml file which demonstrate usage of this custom github action
├── src                    # Custom Github Action Source Code
│   ├── application        # Application level of this github action
│   │   ├── cli            # Entry point of cli
│   │   └── usecase        # Usecases of this application(cli), such as manager or usecase. Manager or usecase use infra and domain model to make actions.
│   ├── common             # Shared code to whole project
│   ├── domain             # Domain tier
│   │   └── model          # Domain Model
│   ├── infra              # implementation of repository
│   └── repository         # Interfaces
└── tests                  # test file
```

### Prerequisites:

Python 3.11.3





----
## Build develop environment

### Develop on Local [Build]

```shell
make install
```
----

## Below is frequently used command and it is optional

### How to use formatter to format code

```shell
make format
```

### How to check whether coding style is fit the team style or not

```shell
make check-coding-style
```

### How to check whether static type is fit the team style or not

```shell
make check-static-type
```

### How to test code

```shell
make test
```

### How to install pre-commit hooks

```shell
make install-pre-commit-hooks
```
