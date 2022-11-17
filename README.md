## PASSBOX

### 初始化程序

- 配置 *settings.json*
  - 纯本地设置
    - *onlyLocal* 为true ，后面的不用配置
    - 建议: onlyLocal 的话，本项目代码 最好存在如dropbox，百度云等类似云盘的本地文件夹，与云端定期同步，也能达到迁移目的
  - 非本地设置
    - *onlyLocal* 为false
    - *pass*: 加密后密文存储地址，默认为git ，需配置 *remote(仓库地址)* , *branch(分支)* ,*localBranch(本地分支)*
    - *rsa* : RSA密钥存储地址,默认为git ,同上
    - 注意 :仓库最好为Private 仓库

  <br>
- 安装python(版本>=3) 库, `pip intsall -r requirements.txt`
  <br>
- 配置环境变量
  - windows环境
    - 配置环境变量 PASSBOX(值本代码的目录),后将 %PASSBOX%添加到PATH
  - linux / mac 环境下
    - 在/etc/profile 文件中声明 `export PASSBOX=<代码的目录> ; export PATH= $PATH:$PASSBOX`
    - 执行 `chmox +x passbox` 添加可执行权限
    - 修改 *passbox* 文件第一行(即:`#!/opt/conda/bin/python`)为您的python 解释器路径(终端运行`which python`,即可得到)
<br>

- 初次使用: 命令行 运行 `passbox init`  生成密钥和相关文件夹
  - 去 *pass_repo* 和 *key_pair*文件夹中,初始化git仓库，如果非*onlyLocal*配置的话, 需添加相对应的远程仓库(settings.json中配置好的)，配置验证信息,尝试push,确保通过
  - 考虑安全，强烈推荐 设置私钥密码 : `passbox reset - ${aesKey}` *aesKey*为你个人的aes 密钥
  <br>

- 迁移：则只需执行`passbox pull`,从仓库拉下 我们的加密文件(存入文件夹*pass_repo*) 公私钥文件(存入文件夹 *key_pair*)
  
### 使用

- 程序都基于命令行方便操作
  - 重设私钥密码:`passbox reset ${oldKey} ${newKey}`
  
  - 加密
    - 加密命令行: `passbox enc ${domain} ${msg}` *domain* (域名或其他，主要起标记作用) *msg* (待加密的信息)
    - 加密文件: `passbox encfile ${filepath}` *filepath* 为文件路径
    - 在非*onlyLocal* 情况下 ，以上命令后添加`--upload=false` ,则不上传密文到远程仓库
  - 解密: `passbox dec ${domain} ${aeskey}`  *domain* (域名或文件名或其他) 密码为空时用 *-* 替代
