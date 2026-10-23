# 财务SA-CCR｜管理员准备与检查

13个公开CSV逐字节保留，openpyxl写工作簿；无需指定Office服务。

原/app/inputs映射到workspace/inputs；原/app/output映射到workspace/output。交付sa_ccr_results.csv与sa_ccr_workings.xlsx，遵守原题公式与底稿要求。

将TASK.md、EXECUTION.md与workspace交给受测agent。RUN.md及顶层管理文档留在隔离外。每题1800秒。

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

基础环境只需Python与openpyxl。公式与缓存存在不等于公式正确重算，CSV代数自洽也不证明金融规则正确。独立原判器须管理员按固定来源准备。三项额外增强交付谓词不作为本V6.0.0新增合同。
