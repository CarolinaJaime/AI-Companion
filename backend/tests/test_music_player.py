import os
import sys
import tempfile
import unittest
from unittest import mock

# Ensure backend package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import music_player


class TestMusicPlayer(unittest.TestCase):
    def setUp(self):
        # Create a temporary music directory with a small dummy file
        self.tmpdir = tempfile.TemporaryDirectory()
        self.orig_music_dir = music_player.MUSIC_DIR
        music_player.MUSIC_DIR = self.tmpdir.name
        # create dummy mp3 files used by MUSIC_MAP
        for fname in set(music_player.MUSIC_MAP.values()):
            open(os.path.join(self.tmpdir.name, fname), "wb").write(b"ID3")

    def tearDown(self):
        music_player.MUSIC_DIR = self.orig_music_dir
        self.tmpdir.cleanup()

    def test_find_player_none(self):
        with mock.patch("shutil.which", return_value=None):
            self.assertIsNone(music_player.find_player())

    def test_find_player_priority(self):
        def fake_which(cmd):
            if cmd == "afplay":
                return "/usr/bin/afplay"
            return None

        with mock.patch("shutil.which", side_effect=fake_which):
            self.assertEqual(music_player.find_player(), "afplay")

    def test_play_file_calls_player(self):
        # Patch shutil.which and subprocess.run to capture calls
        calls = []

        def fake_run(cmd, *a, **kw):
            calls.append(cmd)
            return 0

        with mock.patch("shutil.which", return_value="/usr/bin/afplay"), \
             mock.patch("subprocess.run", side_effect=fake_run):
            path = os.path.join(music_player.MUSIC_DIR, music_player.MUSIC_MAP["lofi"])
            music_player.play_file(path)

        self.assertTrue(calls)
        self.assertEqual(calls[0], ["afplay", path])

    def test_queue_and_play_without_intro(self):
        # synthesize intro returns None -> only play track
        played = []

        def fake_play_file(p):
            played.append(p)

        with mock.patch.object(music_player, "synthesize_intro", return_value=None), \
             mock.patch.object(music_player, "play_file", side_effect=fake_play_file):
            music_player.queue_and_play("lofi")

        # only the track should be played
        expected = os.path.join(music_player.MUSIC_DIR, music_player.MUSIC_MAP["lofi"])
        self.assertEqual(played, [expected])

    def test_synthesize_intro_with_fake_elevenlabs(self):
        # Inject a fake elevenlabs module into sys.modules
        class FakeVoice:
            def __init__(self, name):
                self.name = name

        def fake_voices():
            return [FakeVoice("alloy")]

        def fake_text_to_speech(text, voice):
            return b"FAKEAUDIO"

        fake_mod = mock.MagicMock()
        fake_mod.voices = fake_voices
        fake_mod.text_to_speech = fake_text_to_speech

        sys.modules["elevenlabs"] = fake_mod
        intro_path = None
        try:
            intro_path = music_player.synthesize_intro("lofi")
            self.assertIsNotNone(intro_path)
            self.assertTrue(os.path.exists(intro_path))
            # file should contain the fake bytes
            with open(intro_path, "rb") as f:
                data = f.read()
            self.assertEqual(data, b"FAKEAUDIO")
        finally:
            # cleanup
            if intro_path and os.path.exists(intro_path):
                os.remove(intro_path)
            del sys.modules["elevenlabs"]


if __name__ == "__main__":
    unittest.main()
