import hashlib
import importlib.util
import pathlib
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock


SPEC = importlib.util.spec_from_file_location("sync_editions", pathlib.Path(__file__).with_name("sync-editions.py"))
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


class SyncTests(unittest.TestCase):
    def test_bilingual_readme_versions_keep_preview_labels(self):
        for label in ["preview", "预览"]:
            content = "| `imyemail-cloud-native` | 0.2.1 | Mac |\n| `imyemail-cloud-mygo` | 0.3.0 " + label + " | Mac |\n"
            updated = SYNC.updated_readme(content, "0.2.4", "0.3.4")
            self.assertIn("| 0.2.4 |", updated)
            self.assertIn("| 0.3.4 " + label + " |", updated)
        with self.assertRaises(ValueError):
            SYNC.updated_readme("missing rows", "0.2.4", "0.3.4")
        with self.assertRaises(ValueError):
            SYNC.updated_readme(content, "invalid", "0.3.4")

    def test_tracks_choose_numeric_versions_and_ignore_drafts(self):
        releases = [
            {"tag_name": "native-v0.2.9", "draft": False, "prerelease": False},
            {"tag_name": "native-v0.2.10", "draft": False, "prerelease": False},
            {"tag_name": "native-v9.0.0", "draft": False, "prerelease": True},
            {"tag_name": "mygo-v0.3.1", "draft": False, "prerelease": True},
            {"tag_name": "mygo-v9.0.0", "draft": True, "prerelease": True},
            {"tag_name": "v9.0.0", "draft": False, "prerelease": False},
        ]
        self.assertEqual(SYNC.release_for(releases, "native-v")["tag_name"], "native-v0.2.10")
        self.assertEqual(SYNC.release_for(releases, "mygo-v")["tag_name"], "mygo-v0.3.1")
        with self.assertRaises(ValueError):
            SYNC.release_for([], "native-v")

    def test_casks_do_not_collide(self):
        digest = "a" * 64
        native = SYNC.cask_native("0.2.2", "imyemail-cloud-native-macos-arm64-20261011-selfsigned.zip", digest)
        mygo = SYNC.cask_mygo("0.3.1", {f"imyemail-cloud-mygo-0.3.1-darwin-{arch}-selfsigned.zip": digest for arch in ["amd64", "arm64"]})
        self.assertIn('target: "imyemail-cloud-native"', native)
        self.assertIn('uninstall quit: "email.imy.cloud"', native)
        self.assertIn('uninstall quit: "email.imy.cloud.mygo"', mygo)
        self.assertNotIn("conflicts_with", mygo)
        self.assertIn("native-v#{version}", native)
        self.assertIn("mygo-v#{version}", mygo)

    def test_signed_fixture_rejects_package_manifest_and_certificate_tampering(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = pathlib.Path(temporary)
            package = directory / "fixture.zip"
            package.write_bytes(b"local fixture, no executable")
            key = directory / "fixture.key"
            certificate = directory / "release-cert.pem"
            SYNC.command("openssl", "genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:2048", "-out", str(key))
            SYNC.command("openssl", "req", "-new", "-x509", "-key", str(key), "-subj", "/CN=Fixture", "-days", "1", "-out", str(certificate))
            der = SYNC.command("openssl", "x509", "-in", str(certificate), "-outform", "DER")
            fingerprint = hashlib.sha256(der).hexdigest()
            digest = hashlib.sha256(package.read_bytes()).hexdigest()
            manifest = directory / "SHA256SUMS"
            manifest.write_text(digest + "  fixture.zip\n")
            SYNC.command("openssl", "dgst", "-sha256", "-sign", str(key), "-out", str(directory / "SHA256SUMS.sig"), str(manifest))
            real_command = SYNC.command

            def fixture_command(*arguments, **kwargs):
                if arguments[0] == "gh":
                    destination = pathlib.Path(arguments[arguments.index("--dir") + 1])
                    for name in ["fixture.zip", "SHA256SUMS", "SHA256SUMS.sig", "release-cert.pem"]:
                        shutil.copyfile(directory / name, destination / name)
                    return b""
                return real_command(*arguments, **kwargs)

            release = {"tag_name": "fixture", "assets": [{"name": "fixture.zip"}]}
            with mock.patch.object(SYNC, "command", fixture_command), mock.patch.object(SYNC, "FINGERPRINT", fingerprint):
                self.assertEqual(SYNC.verified_hashes(release, [r"fixture\.zip"]), {"fixture.zip": digest})
                package.write_bytes(b"altered fixture")
                with self.assertRaisesRegex(ValueError, "hash mismatch"):
                    SYNC.verified_hashes(release, [r"fixture\.zip"])
                package.write_bytes(b"local fixture, no executable")
                original = manifest.read_text()
                manifest.write_text(original + "altered\n")
                with self.assertRaises(subprocess.CalledProcessError):
                    SYNC.verified_hashes(release, [r"fixture\.zip"])
                manifest.write_text(original)
                with mock.patch.object(SYNC, "FINGERPRINT", "0" * 64):
                    with self.assertRaisesRegex(ValueError, "certificate"):
                        SYNC.verified_hashes(release, [r"fixture\.zip"])


if __name__ == "__main__":
    unittest.main()
