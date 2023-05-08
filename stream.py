import threading

class Stream:
    def __init__(self):
        self.items = []
        self.operation = None
        self.thread = threading.Thread(target=self.run)
        self.stop_requested = False
        self.thread.start()
        
    def add(self, item):
        self.items.append(item)
        
    def forEach(self, func):
        self.operation = lambda x: func(x)
        
    def apply(self, func):
        self.operation = func
        new_stream = Stream()
        for item in self.items:
            result = self.operation(item)
            if result == True:
                new_stream.add(item)
            else:
                new_stream.add(result)
        return new_stream
        
    def run(self):
        while not self.stop_requested:
            if self.operation and self.items:
                item = self.items.pop(0)
                result = self.operation(item)
                if result == True:
                    continue
                elif result == False:
                    break
                else:
                    self.add(result)
            else:
                continue
        
    def stop(self):
        self.add(False)
        self.stop_requested = True
        self.thread.join()
        self.operation = None
        del self.items[:]
