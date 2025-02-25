class TaskLocationRouter:
    """
    A database router to manage cross-database relations between Tasks (default DB) and Locations (location_db).
    """

    route_app_labels = {'tasks', 'Checkin'}

    def db_for_read(self, model, **hints):
        """Point to the correct database when reading"""
        if model._meta.app_label == 'Checkin':  # Location model is in Checkin app
            return 'location_db'  # Read from location_db
        return 'default'  # Read from db.sqlite3

    def db_for_write(self, model, **hints):
        """Point to the correct database when writing"""
        if model._meta.app_label == 'Checkin':
            return 'location_db'  # Write to location_db
        return 'default'  # Write to db.sqlite3

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a Task references a Location.
        """
        if obj1._meta.app_label in self.route_app_labels and obj2._meta.app_label in self.route_app_labels:
            return True  # Allow relations between Checkin and Tasks
        return None  # Otherwise, follow default behavior

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure models go to their respective databases.
        """
        if app_label == 'Checkin':
            return db == 'location_db'  # Only migrate Checkin models in location_db
        elif app_label == 'tasks':
            return db == 'default'  # Only migrate Tasks models in default DB
        return None