import hashlib
import json
import pathlib
import re
import subprocess
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
REPOSITORY = "logdns/imyemail-cloud"
FINGERPRINT = "476ea6e573714e9c46a43471b5938d791e1c3851beb7b3eef8269cf084f48548"


def command(*arguments, **kwargs):
    return subprocess.run(arguments, check=True, capture_output=True, timeout=300, **kwargs).stdout


def release_for(releases, prefix):
    candidates = []
    for release in releases:
        match = re.fullmatch(re.escape(prefix) + r"(\d+)\.(\d+)\.(\d+)", release["tag_name"])
        if not match or release["draft"] or (prefix == "native-v" and release["prerelease"]):
            continue
        candidates.append((tuple(int(value) for value in match.groups()), release))
    if not candidates:
        raise ValueError("No published release for " + prefix)
    return max(candidates, key=lambda item: item[0])[1]


def verified_hashes(release, patterns):
    names = [asset["name"] for asset in release["assets"]]
    packages = []
    for pattern in patterns:
        matches = [name for name in names if re.fullmatch(pattern, name)]
        if len(matches) != 1:
            raise ValueError("Expected exactly one package: " + pattern)
        packages.append(matches[0])
    with tempfile.TemporaryDirectory(prefix="edition-release-") as temporary:
        directory = pathlib.Path(temporary)
        arguments = ["gh", "release", "download", release["tag_name"], "--repo", REPOSITORY, "--dir", temporary]
        for name in packages + ["SHA256SUMS", "SHA256SUMS.sig", "release-cert.pem"]:
            arguments.extend(["--pattern", name])
        command(*arguments)
        certificate = directory / "release-cert.pem"
        der = command("openssl", "x509", "-in", str(certificate), "-outform", "DER")
        if hashlib.sha256(der).hexdigest() != FINGERPRINT:
            raise ValueError("Unexpected release certificate")
        public = directory / "verified-public.pem"
        public.write_bytes(command("openssl", "x509", "-in", str(certificate), "-pubkey", "-noout"))
        command("openssl", "dgst", "-sha256", "-verify", str(public), "-signature", str(directory / "SHA256SUMS.sig"), str(directory / "SHA256SUMS"))
        manifest = {}
        for line in (directory / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
            digest, name = line.split("  ", 1)
            if not re.fullmatch(r"[a-f0-9]{64}", digest) or name in manifest:
                raise ValueError("Invalid or duplicate signed manifest entry")
            manifest[name] = digest
        result = {}
        for name in packages:
            with (directory / name).open("rb") as package:
                digest = hashlib.file_digest(package, "sha256").hexdigest()
            if manifest.get(name) != digest:
                raise ValueError("Signed package hash mismatch: " + name)
            result[name] = digest
        return result


def cask_native(version, asset, digest):
    return f'''cask "imyemail-cloud-native" do
  version "{version}"
  sha256 "{digest}"

  url "https://github.com/{REPOSITORY}/releases/download/native-v#{{version}}/{asset}"
  name "imyemail-cloud-native"
  desc "Platform-native open-source email client"
  homepage "https://imy.email/"

  livecheck do
    url "https://github.com/{REPOSITORY}/releases/latest"
    regex(/^native-v(\\d+(?:\\.\\d+)+)$/i)
    strategy :github_latest
  end

  conflicts_with cask: "logdns/imyemail-cloud/imyemail-cloud"
  depends_on arch: :arm64
  depends_on macos: :sonoma

  app "imyemail-cloud-native.app"
  binary "#{{appdir}}/imyemail-cloud-native.app/Contents/MacOS/imyemail-cloud", target: "imyemail-cloud-native"

  uninstall quit: "email.imy.cloud"

  caveats <<~EOS
    Self-signed, not Apple-notarized or publicly trusted. Verify the publisher
    fingerprint before approving the app in System Settings > Privacy & Security.
    Existing native users: close the old app and back up profile/Keychain first.
    Uninstall the legacy cask without --zap and install this cask; do not run both.
    MyGo is a separate cask and does not share this edition's account data.
    https://github.com/{REPOSITORY}/blob/main/docs/INSTALL.md
  EOS
end
'''


def cask_mygo(version, hashes):
    arm = hashes[f"imyemail-cloud-mygo-{version}-darwin-arm64-selfsigned.zip"]
    intel = hashes[f"imyemail-cloud-mygo-{version}-darwin-amd64-selfsigned.zip"]
    return f'''cask "imyemail-cloud-mygo" do
  arch arm: "arm64", intel: "amd64"

  version "{version}"
  sha256 arm:   "{arm}",
         intel: "{intel}"

  url "https://github.com/{REPOSITORY}/releases/download/mygo-v#{{version}}/imyemail-cloud-mygo-#{{version}}-darwin-#{{arch}}-selfsigned.zip"
  name "imyemail-cloud-mygo"
  desc "Go-native email desktop preview with a bundled Rust core"
  homepage "https://imy.email/"

  livecheck do
    skip "Preview releases are independently verified by the tap sync workflow"
  end

  depends_on macos: :sonoma

  app "imyemail-cloud-mygo.app"
  binary "#{{appdir}}/imyemail-cloud-mygo.app/Contents/MacOS/imyemail-cloud-mygo"

  uninstall quit: "email.imy.cloud.mygo"

  caveats <<~EOS
    Desktop preview, not feature-equivalent to imyemail-cloud-native.
    Self-signed, not Apple-notarized or publicly trusted. Verify the publisher
    fingerprint before approving the app in System Settings > Privacy & Security.
    Native and MyGo accounts/data remain independent; there is no auto-migration.
    https://github.com/{REPOSITORY}/blob/main/docs/INSTALL.md
  EOS
end
'''


def updated_readme(content, native_version, mygo_version):
    for token, version in [("imyemail-cloud-native", native_version), ("imyemail-cloud-mygo", mygo_version)]:
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ValueError("Invalid edition version")
        pattern = r"(^\| `" + re.escape(token) + r"` \| )\d+\.\d+\.\d+"
        content, matches = re.subn(pattern, lambda match: match[1] + version, content, flags=re.MULTILINE)
        if matches != 1:
            raise ValueError("Missing or duplicate README edition row: " + token)
    return content


def main():
    pages = json.loads(command("gh", "api", "--paginate", "--slurp", "repos/" + REPOSITORY + "/releases?per_page=100"))
    releases = [release for page in pages for release in page]
    native = release_for(releases, "native-v")
    native_hashes = verified_hashes(native, [r"imyemail-cloud-native-macos-arm64-\d{8}-selfsigned\.zip"])
    native_asset, native_hash = next(iter(native_hashes.items()))
    mygo = release_for(releases, "mygo-v")
    version = mygo["tag_name"].removeprefix("mygo-v")
    mygo_hashes = verified_hashes(mygo, [rf"imyemail-cloud-mygo-{re.escape(version)}-darwin-{arch}-selfsigned\.zip" for arch in ["arm64", "amd64"]])
    updates = {
        "imyemail-cloud-native.rb": cask_native(native["tag_name"].removeprefix("native-v"), native_asset, native_hash),
        "imyemail-cloud-mygo.rb": cask_mygo(version, mygo_hashes),
    }
    for name, content in updates.items():
        path = ROOT / "Casks" / name
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")
            print("Verified update: " + name)
    for name in ["README.md", "README.zh-CN.md"]:
        path = ROOT / name
        original = path.read_text(encoding="utf-8")
        updated = updated_readme(original, native["tag_name"].removeprefix("native-v"), version)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print("Updated verified edition versions: " + name)


if __name__ == "__main__":
    main()
