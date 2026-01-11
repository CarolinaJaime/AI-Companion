import vlc
import yt_dlp
import logging
from typing import Optional
import threading
import time

logger = logging.getLogger(__name__)

# Predetermined YouTube URLs for each preference
MUSIC_URLS = {
    'lofi': {
        'url': 'https://www.youtube.com/watch?v=jfKfPfyJRdk',
        'title': 'Lofi Hip Hop Radio - Beats to Study/Relax'
    },
    'classical': {
        'url': 'https://www.youtube.com/watch?v=_--bUrLfBFI',
        'title': 'Classical Music for Studying'
    },
    'ambient': {
        'url': 'https://www.youtube.com/watch?v=lTRiuFIWV54',
        'title': 'Peaceful Ambient Nature Sounds'
    },
    'jazz': {
        'url': 'https://www.youtube.com/watch?v=Dx5qFachd3A',
        'title': 'Relaxing Jazz Music'
    },
    'piano': {
        'url': 'https://www.youtube.com/watch?v=5qap5aO4i9A',
        'title': 'Beautiful Piano Music'
    },
    'rain': {
        'url': 'https://www.youtube.com/watch?v=mPZkdNFkNps',
        'title': 'Rain Sounds for Sleeping'
    },
    'cafe': {
        'url': 'https://www.youtube.com/watch?v=gaGltwHXPqM',
        'title': 'Coffee Shop Ambience'
    },
    'white_noise': {
        'url': 'https://www.youtube.com/watch?v=nMfPqeZjc2c',
        'title': 'White Noise for Concentration'
    },
    'brown_noise': {
        'url': 'https://www.youtube.com/watch?v=RqzGzwTY-6w',
        'title': 'Brown Noise for Focus'
    }
}

class LocalMusicService:
    def __init__(self):
        self.player = None
        self.current_preference = None
        self.current_url = None
        self._lock = threading.Lock()
    
    def _get_audio_stream_url(self, youtube_url: str) -> Optional[str]:
        """Extract direct audio stream URL from YouTube video"""
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                return info['url']
        except Exception as e:
            logger.error(f"Error extracting audio URL: {e}")
            return None
    
    def play_music(self, preference: str = 'lofi', volume: float = 0.5):
        """Play music from YouTube on laptop speakers"""
        with self._lock:
            if preference not in MUSIC_URLS:
                logger.warning(f"Unknown preference '{preference}', defaulting to 'lofi'")
                preference = 'lofi'
            
            music_info = MUSIC_URLS[preference]
            youtube_url = music_info['url']
            title = music_info['title']
            
            try:
                # Stop current playback if any
                if self.player:
                    self.player.stop()
                
                # Get audio stream URL
                logger.info(f"Loading: {title}")
                audio_url = self._get_audio_stream_url(youtube_url)
                
                if not audio_url:
                    return {
                        'success': False,
                        'error': 'Failed to extract audio stream'
                    }
                
                # Create VLC player and play
                self.player = vlc.MediaPlayer(audio_url)
                self.player.audio_set_volume(int(volume * 100))
                self.player.play()
                
                self.current_preference = preference
                self.current_url = youtube_url
                
                logger.info(f"Now playing: {title}")
                
                return {
                    'success': True,
                    'title': title,
                    'preference': preference,
                    'volume': volume
                }
            except Exception as e:
                logger.error(f"Error playing music: {e}")
                return {
                    'success': False,
                    'error': str(e)
                }
    
    def stop(self):
        """Stop music playback"""
        with self._lock:
            try:
                if self.player:
                    self.player.stop()
                    logger.info("Music stopped")
                    return {'success': True}
                return {'success': True, 'message': 'No music playing'}
            except Exception as e:
                logger.error(f"Error stopping music: {e}")
                return {'success': False, 'error': str(e)}
    
    def pause(self):
        """Pause music playback"""
        with self._lock:
            try:
                if self.player:
                    self.player.pause()
                    logger.info("Music paused")
                    return {'success': True}
                return {'success': False, 'error': 'No music playing'}
            except Exception as e:
                logger.error(f"Error pausing music: {e}")
                return {'success': False, 'error': str(e)}
    
    def resume(self):
        """Resume music playback"""
        with self._lock:
            try:
                if self.player:
                    self.player.play()
                    logger.info("Music resumed")
                    return {'success': True}
                return {'success': False, 'error': 'No music playing'}
            except Exception as e:
                logger.error(f"Error resuming music: {e}")
                return {'success': False, 'error': str(e)}
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        with self._lock:
            try:
                if self.player:
                    self.player.audio_set_volume(int(volume * 100))
                    logger.info(f"Volume set to {int(volume * 100)}%")
                    return {'success': True, 'volume': volume}
                return {'success': False, 'error': 'No music playing'}
            except Exception as e:
                logger.error(f"Error setting volume: {e}")
                return {'success': False, 'error': str(e)}
    
    def get_status(self):
        """Get current playback status"""
        with self._lock:
            if not self.player:
                return {
                    'is_playing': False,
                    'current_preference': None,
                    'current_title': None
                }
            
            is_playing = self.player.is_playing()
            current_title = MUSIC_URLS.get(self.current_preference, {}).get('title')
            
            return {
                'is_playing': is_playing,
                'current_preference': self.current_preference,
                'current_title': current_title,
                'volume': self.player.audio_get_volume() / 100.0
            }

# Singleton instance
music = LocalMusicService()