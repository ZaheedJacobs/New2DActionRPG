class Entity:
    def __init__(self, *components, x=0, y=0):
        self.components = []
        self.x = x
        self.y = y

        for component in components:
            self.add(component, False)
        for component in components:
            setup = getattr(component, "setup", None)
            if callable(setup):
                component.setup()

    def add(self, component, perform_setup=True):
        component.entity = self
        self.components.append(component)
        if perform_setup:
            setup = getattr(component, "setup", None)
            if callable(setup):
                component.setup()

    def remove(self, kind):
        component = self.get(kind)
        self.remove_component(component)

    def remove_component(self, component):
        if component is not None:
            breakdown = getattr(component, "breakdown", None)
            if callable(breakdown):
                component.breakdown()
            component.entity = None
            self.components.remove(component)

    def has(self, kind):
        for component in self.components:
            if isinstance(component, kind):
                return True
        return None
    
    def get(self, kind):
        for component in self.components:
            if isinstance(component, kind):
                return component
        return None