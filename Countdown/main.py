"""MIT License

Copyright (c) 2024 ``

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
from datetime import datetime, timedelta
from pathlib import Path

from gtts import gTTS
from playsound import playsound
from pytz import timezone


def text_to_speech(text: str, file_path: str) -> None:
    """Converts text to speech and plays the audio.

    Args:
    ----
        text (str): The text to convert to speech.
        file_path (str): The path to save the temporary audio file.

    """
    tts = gTTS(text=text, lang="en")
    tts.save(file_path)
    playsound(file_path)
    Path(file_path).unlink()


def countdown(seconds: int) -> None:
    """Performs a countdown from the specified number of seconds.

    Args:
    ----
        seconds (int): The number of seconds to count down from.

    """
    for i in range(seconds, 0, -1):
        text_to_speech(str(i), f"temp_{i}.mp3")
    text_to_speech("Time's up!", "temp_final.mp3")


def wait_until(target_hour: int, target_minute: int, countdown_seconds: int) -> None:
    """Waits until the specified time and then performs a countdown.

    Args:
    ----
        target_hour (int): The hour to wait until.
        target_minute (int): The minute to wait until.
        countdown_seconds (int): The number of seconds to count down once the target time is reached.

    """
    while True:
        now = datetime.now(tz=timezone("Asia/Taipei"))
        target_time = now.replace(
            hour=target_hour,
            minute=target_minute,
            second=0,
            microsecond=0,
        )

        if now >= target_time:
            target_time += timedelta(days=1)

        countdown_start_time = target_time - timedelta(seconds=countdown_seconds)
        time_to_wait = (countdown_start_time - now).total_seconds()
        if time_to_wait < 0:
            print("Target time has already passed.")
            return

        print(
            f"Waiting for {time_to_wait} seconds until {countdown_start_time.time()}.",
        )
        while time_to_wait > 0:
            sleep_duration = min(time_to_wait, 60)
            time.sleep(sleep_duration)
            time_to_wait -= sleep_duration

        countdown(countdown_seconds)
        return


if __name__ == "__main__":
    wait_until(0, 5, 10)
