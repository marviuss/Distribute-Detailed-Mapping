# Distribute-Detailed-Mapping

Welcome to the Autonomous Transport Map project! This web application provides an interactive mapping solution for street robots, enabling route planning, dangerous junction identification, and more. The project uses Flask for backend API communication and Mapbox for rendering the interactive map and various layers.

## Objective
To construct an optimized and detailed mapping solution for street robots capable of filtering route based on transport robot accessibility and route planning factors.

## Features
- **Interactive Map**: Utilizes Mapbox JS to provide an interactive map interface.
- **Server-Side Integration**: Implements a Flask server for backend logic, API endpoints, and data handling. The backend includes the `BackEndAPI.py` module responsible for API communication with the frontend.
- **Shortest Route Algorithm**: Computes the shortest route between two points using Dijkstra routing algorithm based on the selected transportation mode (e.g., walking, cycling, driving or combinations of them). Our route planning system will automatically avoid roads that are under construction.
- **Dangerous Junction Identification**: Identifies and highlights junctions with a higher risk of accidents or safety concerns by checking for specific properties indicative of a dangerous junction, such as traffic signals, high speeds, roundabouts, etc.
- **Safest Route Algorithm**: Determines the safest route by avoiding as little dangerous junctions as possible.
- **Layer Rendering**: Renders various layers, including routes for differnt mode of transportation, roads under construction, and points of interest (such as dangerous junctions).
- **Estimated Arrival Time**: Calculates the estimated arrival time for street robots when following the shortest route.
## Mapbox Integration
The project integrates with Mapbox services for map rendering and data visualization.

## Getting Started
To get started with the project, follow these steps:

1. **Install Flask**:
   - Set up a virtual environment and install Flask: `python -m pip install flask`.
   - Install the geojson package: `pip install geojson`.

2. **Run the Flask Server**:
   - Right-click on `BackEndAPI.py` and select "Run Code" to start the server.
   - Open your browser and navigate to `http://localhost:8000`.
   - Copy the access token from your own Mapbox account and replace the value of `mapboxgl.accessToken` in `script.js` with your token.

## Usage
To use the application:

1. **Load Routes**:
   - Click "Load Route" and choose a transportation mode you want to visualize. The map will then display all possible routes for that mode with orange line strings.

2. **Finding Routes**:
   - **Set Start and End Points**: Click on the map to set your starting point and then click again to set your end point. This will activate these buttons "Find Shortest Route" and "Find Safest Route."
   - **Calculate Route**: Enter the starting time and click "Find Shortest Route" to find the quickest path (shown in blue line) or "Find Safest Route" to find the safest path (shown in green line).
     
     **Note**: If no route layers have been loaded, you won't be able to find any routes. Make sure to load a transportation mode first.
3. **Additional Features**:
   - **Show Dangerous Junctions**: Click this button to display all dangerous junctions within the campus area on the map. It may take 5-10 seconds to load. Hover over a point to see more information.
   - **Display Roads Under Construction**: Click this button to view roads currently under construction, represented by red line on the map. 

4. **Resetting**:
   - Click "Reset" to clear the map and start over.

## Limitations
No information available about the traffic density on campus.

## Improvements
- **Live Tracking Data**: Adding live tracking data would enable real-time navigation and tracking of robot locations within the campus.

## Contributing
We welcome contributions! To contribute, please:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/new-feature`.
3. Make your changes and commit them: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin feature/new-feature`.

Submit a pull request, and our team will review it. Thank you for your interest in contributing to the project!

## Contact and Support
If you encounter issues or have questions, please contact our support team via email [t.astashov@student.utwente.nl](mailto:t.astashov@student.utwente.nl), [nguyenngocminhchau@student.utwente.nl](mailto:nguyenngocminhchau@student.utwente.nl). We're happy to help!
