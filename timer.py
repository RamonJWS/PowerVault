import sched
from datetime import datetime
import time 
import threading
from typing import Callable

def callbackfunc(foo: str):
    """
    Used to test that a call back function works
    """
    print(f"Testing Callback: {foo}")

class timer:
  """
  Use: To start a timer and check its running, can be used to stop the timer prematurely.

  Attributes:
  - None

  Methods:
  - start_timer(timeout: int)
        Starts the timer.
  
  - timer_check()
        Checks to see if the timer is still running.

  - stop_timer()
        Checks to see if the timer has stopped.
  """
  def __init__(self, callback: Callable) -> None:
    """
    Constructs instance attributes.

    Attributes:
    - callback
        a callback function to be called once the timer matures.
    - scheduler
        An interface for scheduling events.
    - timer
        The timer event (currently None but assigned in start_timer(...))
    """
    self.callback = callback
    self.scheduler = sched.scheduler(time.time, time.sleep)
    self.timer = None

  def start_timer(self, timeout: int) -> None:
    """
    Used to start a timer that runs concurrently
    """
    start_time = datetime.now()
    self.timer = self.scheduler.enter(timeout, 1, self._print_event, (start_time,))
    t = threading.Thread(target=self.scheduler.run)
    t.start()

  def timer_check(self) -> None:
    """
    Used to check if the timer is running, the scheduler should be empty if the timer has stopped
    """
    if self.scheduler.empty() == True:
        print("Timer not running")
    elif self.scheduler.empty() == False:
        print("Timer is running")

  def stop_timer(self) -> None:
    """
    Used to stop the timer if its running, except used to catch value error.
    """
    try:
        self.scheduler.cancel(self.timer)
        print("Timer stopped")
    except ValueError:
        print("No timer to stop")

  def _print_event(self, start_time: datetime) -> None:
    """
    Used to return information about the timer once it finishes.
    """
    print(f"Timer started at: {start_time} and finished at {datetime.now()}")

if __name__ == "__main__":
    # Test: start timer, check to see if the timer is running, use callback, stop timer before it finishes.
    print("Test instance A:")
    a = timer(callbackfunc)
    a.start_timer(5)
    a.timer_check()
    a.callback("Ran correctly")
    a.stop_timer()

    # Test: start timer, stop timer, check to see if timer is running.
    print("\n","Test instance B:")
    b = timer(callbackfunc)
    b.start_timer(1)
    b.stop_timer()
    b.timer_check()

    # Test: start timer, check to see if the timer is running, use callback, check output when timer ends. 
    print("\n","Test instance C:")
    c = timer(callbackfunc)
    c.start_timer(5)
    c.timer_check()
    c.callback("Ran correctly")