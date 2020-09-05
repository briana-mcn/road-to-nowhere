from road_to_nowhere import app
import os

if __name__ == '_main _':
    app.run(host='0.0.0.0', port=os.getenv('ROAD_TO_NOWHERE_PORT'),  debug=True)
