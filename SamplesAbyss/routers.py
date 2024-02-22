class SamplesRouter:
    """
    A router to control all database operations on models in the 'samples' application.
    """
    route_app_labels = {'samples',}

    def db_for_read(self, model, **hints):
        """
        Attempts to read models from the 'samples' app from the 'samples' database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'samples'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write models from the 'samples' app to the 'samples' database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'samples'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the 'samples' app.
        """
        if obj1._meta.app_label in self.route_app_labels and obj2._meta.app_label in self.route_app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the 'samples' app only appears in the 'samples' database.
        """
        if app_label in self.route_app_labels:
            return db == 'samples'
        return None
