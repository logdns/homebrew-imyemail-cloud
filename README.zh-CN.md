# imyemail-cloud Homebrew 源：双版本

[English](README.md) · [简体中文](README.zh-CN.md) · [看截图选择下载](https://github.com/logdns/imyemail-cloud/blob/main/README.zh-CN.md)

| 包名 | 版本 | macOS 支持 | app / 命令 |
| --- | --- | --- | --- |
| `imyemail-cloud-native` | 0.2.4 | Apple Silicon、macOS 14+ | `imyemail-cloud-native.app` / `imyemail-cloud-native` |
| `imyemail-cloud-mygo` | 0.3.4 预览 | Intel / Apple Silicon、macOS 14+ | `imyemail-cloud-mygo.app` / `imyemail-cloud-mygo` |

## 选择安装

```bash
brew tap logdns/imyemail-cloud
brew trust --tap logdns/imyemail-cloud
brew install imyemail-cloud-native
# 选择 MyGo，或与原生版并存：
brew install imyemail-cloud-mygo
```

Homebrew 7 首次信任第三方源一次。两版均 MIT 开源；MyGo 是桌面预览，不等于原生版全部功能。两版账号/数据独立，不自动迁移或覆盖另一版。

```bash
brew update
brew upgrade imyemail-cloud-native
brew upgrade imyemail-cloud-mygo
HOMEBREW_NO_INSTALL_CLEANUP=1 brew uninstall imyemail-cloud-native
HOMEBREW_NO_INSTALL_CLEANUP=1 brew uninstall imyemail-cloud-mygo
```

只执行所选版本的命令。普通卸载保留邮件和系统凭据，不用 `--zap`、purge、autoremove 升级。

## 旧原生用户

旧 `imyemail-cloud` cask 固定保留 0.2.1，与新原生 cask 互斥，不与 MyGo 冲突。先关闭旧 app、备份数据库/Keychain，执行 `HOMEBREW_NO_INSTALL_CLEANUP=1 brew uninstall --cask imyemail-cloud`，再 `brew install imyemail-cloud-native`。原生 Bundle ID/数据/钥匙库不变，不同时启动旧/新原生 app。

## 校验、同步与维护

两 cask 独立固定实际 Release URL 和 SHA-256。新包采用固定证书自签，**不是 Apple Developer ID、公证或默认公信**。先核对发布者指纹，再按系统正常方式允许启动，不关闭 Gatekeeper。见[安装与回滚](https://github.com/logdns/imyemail-cloud/blob/main/docs/INSTALL.zh-CN.md)、[验签](https://github.com/logdns/imyemail-cloud/blob/main/docs/SIGNING.md)。

每日/手动同步分别选择 `native-v*` 稳定版和 `mygo-v*` 预览版，不依赖单一 Latest 选择两版。固定证书指纹、验签清单、下载复算后提出更新 PR，并显式为该分支触发 cask 检查（机器人 PR 不自动触发 push/PR 工作流）。CI 对支持架构安装、检查版本/身份/架构/签名/CLI 后卸载，禁用 cleanup，不读取真实邮箱。维护者确认分支检查后再合并，不自动合并；旧包/标签不重写。

## Brewfile

```ruby
tap "logdns/imyemail-cloud"
cask "imyemail-cloud-native"
cask "imyemail-cloud-mygo"
```

选择一项或保留两项。[MIT](LICENSE)。
