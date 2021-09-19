class Observer():
	def __init__(self):
		self.name = __name__
		self.signalObservers = {}

	def attach(self, observer, signalId: int) -> None:
		observers = self.signalObservers.get(signalId, [])
		if len(observers) == 0:
			self.signalObservers[signalId] = observers
		
		if observer not in observers:
			observers.append(observer)

	def detach(self, observer, signalId: int) -> int:
		observers = self.signalObservers.get(signalId, None)
		if observers == None or observer not in observers:
			return -1
		
		observers.remove(observer)

	def notify(self, signalId: int) -> None:
		observers = self.signalObservers.get(signalId, None)
		if observers == None:
			return
		
		for observer in observers:
			observer.notified(signalId)
	
	def notified(self, signalId: int) -> None:
		print(self.name + " notified of signal " + str(signalId))
	