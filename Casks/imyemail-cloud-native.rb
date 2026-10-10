cask "imyemail-cloud-native" do
  version "0.2.4"
  sha256 "3e4ca86398ecfec379ac06b165129339f6863e514755cbea2284ddc7850dd32f"

  url "https://github.com/logdns/imyemail-cloud/releases/download/native-v#{version}/imyemail-cloud-native-macos-arm64-20261011-selfsigned.zip"
  name "imyemail-cloud-native"
  desc "Platform-native open-source email client"
  homepage "https://imy.email/"

  livecheck do
    url "https://github.com/logdns/imyemail-cloud/releases/latest"
    regex(/^native-v(\d+(?:\.\d+)+)$/i)
    strategy :github_latest
  end

  depends_on arch: :arm64
  depends_on macos: :sonoma
  conflicts_with cask: "logdns/imyemail-cloud/imyemail-cloud"

  app "imyemail-cloud-native.app"
  binary "#{appdir}/imyemail-cloud-native.app/Contents/MacOS/imyemail-cloud", target: "imyemail-cloud-native"

  uninstall quit: "email.imy.cloud"

  caveats <<~EOS
    Self-signed, not Apple-notarized or publicly trusted. Verify the publisher
    fingerprint before approving the app in System Settings > Privacy & Security.
    Existing native users: close the old app and back up profile/Keychain first.
    Uninstall the legacy cask without --zap and install this cask; do not run both.
    MyGo is a separate cask and does not share this edition's account data.
    https://github.com/logdns/imyemail-cloud/blob/main/docs/INSTALL.md
  EOS
end
