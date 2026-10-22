import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'cloudflared/rootfs/usr/local/bin/run-cloudflared'


class StartupTests(unittest.TestCase):
    def run_startup(self, options):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / 'options.json').write_text(json.dumps(options))
            stub = path / 'cloudflared'
            stub.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n'
                            'test "$TUNNEL_TOKEN" = "test-secret-token"\n')
            stub.chmod(0o755)
            return subprocess.run(['sh', str(SCRIPT)], env={
                **os.environ, 'OPTIONS_FILE': str(path / 'options.json'),
                'PATH': directory + os.pathsep + os.environ['PATH'],
            }, capture_output=True, text=True)

    def test_token_forwarded_without_command_line_exposure(self):
        result = self.run_startup({'tunnel_token': 'test-secret-token',
                                   'log_level': 'warn', 'protocol': 'http2'})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), [
            'tunnel', '--no-autoupdate', '--loglevel', 'warn',
            '--protocol', 'http2', 'run'])
        self.assertNotIn('test-secret-token', result.stdout + result.stderr)

    def test_defaults(self):
        result = self.run_startup({'tunnel_token': 'test-secret-token'})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('info\n--protocol\nauto', result.stdout)

    def test_invalid_options_fail_without_exposing_token(self):
        for options in [{}, {'tunnel_token': ''}, {'tunnel_token': 'bad token'},
                        {'tunnel_token': 123},
                        {'tunnel_token': 'test-secret-token', 'protocol': 'invalid'},
                        {'tunnel_token': 'test-secret-token', 'log_level': 'invalid'}]:
            with self.subTest(options=options):
                result = self.run_startup(options)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('test-secret-token', result.stdout + result.stderr)

    def test_manifest(self):
        config = json.loads((ROOT / 'cloudflared/config.json').read_text())
        self.assertEqual(set(config['options']), set(config['schema']))
        self.assertEqual(config['schema']['tunnel_token'], 'password')
        self.assertTrue(config['init'])
        self.assertEqual(config['arch'], ['amd64', 'aarch64'])
        for permission in ['docker_api', 'host_network', 'hassio_api', 'privileged']:
            self.assertFalse(config.get(permission))


if __name__ == '__main__':
    unittest.main()
