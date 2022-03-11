from abc import ABC

class Flow(ABC):
    ...

class SourceFlow(Flow):
    ...

class SinkFlow(Flow):
    ...

class DuplexFlow(Flow):
    ...

class UnknownFlow(Flow):
    ...

class Kind(ABC):
    ...

class PortKind(Kind):
    ...