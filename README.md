# dev-github-action-auto-update-helm

此 Custom Github Action 提供下列指令:

| subcommand | desc |
| --- | --- |
| amavis-helm-update-actiondasd | 微服務 將 branch merge 進 master (微服務的master) 時，使用此 github action 會自動將 mavis helmfile.yaml 的 docker 版本號修改至最新版本號以後發 PR 到 mavis master|


## Example 

**amavis-helm-update-actiondasd**
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
