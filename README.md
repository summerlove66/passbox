## PASSBOX

### 初始化程序
- 配置 *settings.json*
    - *pass*: 加密后密文存储地址，默认为git ，需配置 *remote(仓库地址)* , *branch(分支)*
    - *rsa* : RSA密钥存储地址,默认为git ,同上
    - 注意 :仓库最好为Private 仓库
  <br>
- 安装python(>3) 库, `pip intsall -r requirements.txt`
  <br>
-  配置环境变量
    - windows 下 配置环境变量 PASSBOX(值本代码的目录),后将 %PASSBOX%添加到PATH
    - linux / mac 环境下
      - 在/etc/profile 文件中声明 `export PATHBOX=<代码的目录> ; export PATH= $PATH:$PASSBOX`
      - 将 passbox_linux.sh 重命名为 passbox ,并执行 `chmox +x passbox` 添加可执行权限
<br>
-  第一次使用该工具的话 :命令行 运行 *passbox init*  生成密钥和相关文件夹
    - 去 *pass_repo* 和 *key_pair*文件夹中,初始化git仓库 添加相对应的远程仓库(settings.json中配置好的)，配置验证信息,尝试push,确保通过
  <br>
-  之前使用过，则只需执行*passbox pull*,从仓库拉下 我们的加密文件(存入文件夹*pass_repo*) 公私钥文件(存入文件夹 *key_pair*)
  
### 使用
   - 程序都基于命令行方便操作
     - 重设私钥密码 passbox reset oldKey(原密码 ) newKey(新密码)
     - 加密 passbox enc *name*(网站域名或其他) *pass*(网站用户名密码信息 或者其他) *aeskey*(私钥密码)
     - 解密 passbox dec *name* *aeskey*
     - 考虑安全，强烈推荐 设置私钥密码 : passbox reset - *${aesKey}*(私钥密码) 将对私钥进行aes加密 ，因为初始时无密码 所以*oldKey*为 -
     - 注意: 私钥密码无时 请写 -

### 视频
- https://www.bilibili.com/video/BV1YG411F7c2/?vd_source=47e46f193d221683448c4f1464a82252