class Observer():
	def __init__(self):
		self.name = __name__
		self.signalObservers: dict[str, Observer] = {}
		self.signalHandlers: dict[str, function] = {}

	def attach(self, observer, signalId: str) -> None:
		observers: list[Observer] = self.signalObservers.get(signalId, [])
		if len(observers) == 0:
			self.signalObservers[signalId] = observers
		
		if observer not in observers:
			observers.append(observer)

	def detach(self, observer, signalId: str) -> int:
		observers: list[Observer] = self.signalObservers.get(signalId, None)
		if observers == None or observer not in observers:
			return -1
		
		observers.remove(observer)

	def notify(self, signalId: str, payload = None) -> None:
		observers: list[Observer] = self.signalObservers.get(signalId, None)
		if observers == None:
			return
		
		for observer in observers:
			observer.notified(signalId, payload)
	
	def notified(self, signalId: int, payload = None) -> None:
		signalHandler: function = self.signalHandlers.get(signalId, None)
		if signalHandler is not None:
			signalHandler(payload)
	