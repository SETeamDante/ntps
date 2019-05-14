class Queueue():
    def __init__(self):
        self.curr = 0
        self.Max = 100

    def QueueSizePrint(self):
        return self.Max

    def OverFlow(self):
        if self.curr >= self.Max:
            ##Insert Alert box here
            return False
        return True

    def add(self):
        if self.curr >= self.Max:
            ##Insert Alert box here
            return
        self.curr += 1

    def ChangeQueueSize(self, NewMax):
        self.Max = NewMax

    def RemoveQueue(self):
        self.curr -= 1