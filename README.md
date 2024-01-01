# PASSBOX 安装使用

## 安装
- 确保Python版本 >=3.7
- ` pip3  install   passbox@git+https://github.com/summerlove66/passbox.git `
- 环境初始化 终端执行 `passbox init`

## 配置

- 迁移和同步配置
  - 如果你想方便 迁移和同步，你需要配置 settings.json文件 (路径：*home*/.passbox/settings.json)
  - 纯本地设置(默认)
    - *onlyLocal* 为true ，后面的不用配置
    - 建议: onlyLocal 的话，本项目代码 最好存在如dropbox，百度云等类似云盘的本地文件夹，与云端定期同步，也能达到迁移目的
  
  - 非本地设置
    - *onlyLocal* 为false
    - *pass*: 加密后密文存储地址，默认为git ，需配置 *remote(仓库地址)* , *branch(分支)* ,*localBranch(本地分支)*
    - *rsa* : RSA密钥存储地址,默认为git ,同上
    - 注意 :仓库最好为Private 仓库
- 密钥配置
  - 考虑安全，强烈推荐 设置私钥密码 : `passbox reset - ${aesKey}` *aesKey*为你个人的aes 密钥,默认没有aes密钥，解密时没有aes密钥,用 *-* 替代

## 使用

- 程序都基于命令行方便操作
- 重设私钥密码:`passbox reset ${oldKey} ${newKey}`

- 加密
  - 加密命令行: `passbox enc ${domain} ${msg}` *domain* (域名或其他，主要起标记作用) *msg* (待加密的信息)
  - 加密文件: `passbox encfile ${filepath}` *filepath* 为文件路径
  - 在非*onlyLocal* 情况下 ，以上命令后添加`--upload=false` ,则不上传密文到远程仓库
- 解密: `passbox dec ${domain} ${aeskey}`  *domain* (域名或文件名或其他) 没有aeskey时用 *-* 替代

- 迁移
  - 配置 settings.json ,参照 配置部分
  - 如果*onlyLocal* 为false ，只需执行`passbox pull`,从仓库拉下 我们的加密文件(存入文件夹*pass_repo*) 公私钥文件(存入文件夹 *key_pair*)