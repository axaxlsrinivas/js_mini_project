import os
if os.path.exists('equipment.db'):
    os.remove('equipment.db')
print('equipment.db deleted. Restart the app to re-initialize the database with sample data.')
