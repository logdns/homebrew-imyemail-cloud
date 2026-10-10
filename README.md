# Homebrew tap for imyemail-cloud — two editions

[English](README.md) · [简体中文](README.zh-CN.md) · [Choose with screenshots](https://github.com/logdns/imyemail-cloud#choose-your-edition)

| Package | Version | Macs | Application / CLI |
| --- | --- | --- | --- |
| `imyemail-cloud-native` | 0.2.4 | Apple Silicon, macOS 14+ | `imyemail-cloud-native.app` / `imyemail-cloud-native` |
| `imyemail-cloud-mygo` | 0.3.4 preview | Intel / Apple Silicon, macOS 14+ | `imyemail-cloud-mygo.app` / `imyemail-cloud-mygo` |

## Choose and install

```bash
brew tap logdns/imyemail-cloud
brew trust --tap logdns/imyemail-cloud
brew install imyemail-cloud-native  # platform-native edition
# OR, or install alongside native:
brew install imyemail-cloud-mygo    # Go-native desktop preview
```

Homebrew 7 requires one-time third-party tap trust. Both are MIT licensed; MyGo is a preview, not feature-equivalent to native. The applications and data are separate; installing one never migrates or replaces the other.

```bash
brew update
brew upgrade imyemail-cloud-native
brew upgrade imyemail-cloud-mygo
HOMEBREW_NO_INSTALL_CLEANUP=1 brew uninstall imyemail-cloud-native
HOMEBREW_NO_INSTALL_CLEANUP=1 brew uninstall imyemail-cloud-mygo
```

Only use the commands for your chosen edition. Normal uninstall retains profiles and OS-vault credentials. Never use `--zap` as an upgrade step.

## Existing native users

The legacy `imyemail-cloud` cask remains pinned to 0.2.1 and conflicts only with the new native cask. Close the old app and back up its database and Keychain; then `HOMEBREW_NO_INSTALL_CLEANUP=1 brew uninstall --cask imyemail-cloud` followed by `brew install imyemail-cloud-native`. Native Bundle ID/data/vault remain unchanged; do not run the old/new native app together. MyGo remains independent.

## Verification and independent updates

Casks pin actual release URLs and SHA-256. New macOS apps use the stable self-signed release certificate, **not Apple Developer ID/notarization or public trust**. Verify the publisher fingerprint before normal System Settings approval; do not disable Gatekeeper. See [install/upgrade/rollback](https://github.com/logdns/imyemail-cloud/blob/main/docs/INSTALL.md) and [signature verification](https://github.com/logdns/imyemail-cloud/blob/main/docs/SIGNING.md).

Daily/manual sync selects native `native-v*` stable and MyGo `mygo-v*` preview releases independently. It verifies the pinned certificate, signed checksum manifest and recomputed package hashes before proposing a PR, then explicitly dispatches cask checks for that branch (bot-created PRs do not automatically trigger push/PR workflows). CI installs/verifies/uninstalls both casks on supported architectures without cleanup or real mail data. Review the branch's checks before merging; no automatic merge. Legacy release assets and tags are never rewritten.

## Brewfile

```ruby
tap "logdns/imyemail-cloud"
cask "imyemail-cloud-native"
cask "imyemail-cloud-mygo"
```

Choose one or retain both lines. [MIT](LICENSE).
