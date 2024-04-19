
mapboxgl.accessToken = 'pk.eyJ1IjoiY2hhdW5ndXllbjIxMDkiLCJhIjoiY2x1OGdyZ2ZvMGNraDJvcnh4eTl1ODMzdiJ9.2BXRagNWxycExWQ2gfhqNw';
    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v12',
        
        zoom: 15,
        center: [6.8498, 52.2397]
    });
    
    let startPoint = null;
    let endPoint = null;

    map.on('load', () => {
        map.addSource('route', {
            type: 'geojson',
            data: {
                type: 'FeatureCollection',
                features: []
            }
        });
        map.addSource('shortest-route-source', {
            type: 'geojson',
            data: {
                type: 'FeatureCollection',
                features: [] 
            }
        });
        
        map.addSource('safest-route-source', {
            type: 'geojson',
            data: {
                type: 'FeatureCollection',
                features: [] 
            }
        });
        map.addLayer({
            'id': 'route',
            'type': 'line',
            'source': 'route',
            'layout': {
                'visibility': 'visible'
            },
            'paint': {
                'line-color': '#FFA500',
                'line-width': 3
            }
        });
        map.addLayer({
            'id': 'shortest-route', 
            'type': 'line',
            'source': 'shortest-route-source',
            'layout': {
                'visibility': 'visible'
            },
            'paint': {
                'line-color': '#1E90FF', 
                'line-width': 5
            }
        });
        
        map.addLayer({
            'id': 'safest-route', 
            'type': 'line',
            'source': 'safest-route-source',
            'layout': {
                'visibility': 'visible'
            },
            'paint': {
                'line-color': '#52a447',
                'line-width': 5
            }
        });


        

        const dropdownBtn = document.getElementById('dropdownBtn');
        dropdownBtn.addEventListener('click', toggleDropdown);
        const routeOptions = document.querySelectorAll('.routeOption');
        routeOptions.forEach(option => {
            option.addEventListener('click', function() {
                loadRoute(this.textContent);
            });
        });
    });

    function toggleDropdown() {
        const dropdownContent = document.getElementById('dropdownContent');
        dropdownContent.style.display = dropdownContent.style.display === 'none' ? 'block' : 'none';
    }
    function loadRoute(routeName) {
        const routeURLs = {
            'Load Cycle Route': { url: '/load-route?type=cycling', routeType: 'cycling' },
            'Load Car Route': { url: '/load-route?type=car', routeType: 'driving' },
            'Load Walking': { url: '/load-route?type=walking', routeType: 'walking' },
            'Load Walking+Car': { url: '/load-route?type=walking-car', routeType: 'walking' },
            'Load Walking+Cycling': { url: '/load-route?type=walking-cycling', routeType: 'walking' },
            'Load Cycling+Car': { url: '/load-route?type=cycling-car', routeType: 'cycling' }
        };
    
        const routeInfo = routeURLs[routeName];
        if (!routeInfo) return;
    
        fetch(routeInfo.url)
            .then(response => response.json())
            .then(data => {
                map.getSource('route').setData(data);
            })
            .catch(error => {
                console.error('Error loading route:', error);
            });
    
        const routeOptions = document.querySelectorAll('.routeOption');
        routeOptions.forEach(option => {
            option.classList.toggle('active', option.textContent === routeName);
        });
    
        // Set the active route type for later use when finding the shortest route
        document.getElementById('shortestRouteBtn').setAttribute('data-route-type', routeInfo.routeType);
        document.getElementById('safestRouteBtn').setAttribute('data-route-type', routeInfo.routeType);

        document.getElementById('dropdownContent').style.display = 'none';
    }
    

    map.on('click', function(e) {
        const coordinates = e.lngLat;

        if (!startPoint) {
            startPoint = new mapboxgl.Marker({ color: 'red' }).setLngLat(coordinates).addTo(map);
        } else if (!endPoint) {
            endPoint = new mapboxgl.Marker().setLngLat(coordinates).addTo(map);
            document.getElementById('shortestRouteBtn').style.display = 'block';
            document.getElementById('safestRouteBtn').style.display = 'block';
        } else {
            endPoint.setLngLat(coordinates);
        }
    });

    // document.getElementById('shortestRouteBtn').addEventListener('click', function() {
    //     const routeType = document.querySelector('.active').textContent;
    //     displayShortestRoute(routeType.toLowerCase()); 
    //     this.classList.add('active');
    // });
    
    document.getElementById('shortestRouteBtn').addEventListener('click', function() {
        const routeType = document.querySelector('.active').textContent;
        const startTimeInput = document.getElementById('start-time').value;
        if (!startTimeInput) {
            alert('Hey, enter the departure time.');
            return;
        }
        // Make API request to find shortest route with start time
        // displayShortestRoute(routeType.toLowerCase(), startTimeInput);
        displayShortestRoute(startTimeInput);
        this.classList.add('active')
    });
    document.getElementById('safestRouteBtn').addEventListener('click', function() {
        const routeType = document.querySelector('.active').textContent;
        displaySafestRoute(routeType.toLowerCase()); 
        this.classList.add('active');
    });



    // function displayShortestRoute(routeType) {
    //     fetch('/shortest-route', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({
    //             start_point: startPoint.getLngLat().toArray(),
    //             end_point: endPoint.getLngLat().toArray(),
    //             route_type: routeType 
    //         })
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         const shortestRoute = data.shortest_route;
    //         map.getSource('shortest-route-source').setData(shortestRoute);

    //         const startCoords = startPoint.getLngLat().toArray().join(',');
    //         const endCoords = endPoint.getLngLat().toArray().join(',');

    //         fetch(`https://api.mapbox.com/directions/v5/mapbox/driving/${startCoords};${endCoords}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`)
    //         .then(response => response.json())
    //         .then(data => {
    //             if (data.routes && data.routes.length > 0 && data.routes[0].legs && data.routes[0].legs.length > 0) {
    //                 const steps = data.routes[0].legs[0].steps;
    //                 const instructions = steps.map(step => step.maneuver.instruction).join('<br>');
    //                 document.getElementById('instructions').innerHTML = instructions;
    //                 document.getElementById('myModal').style.display = 'block';
    //             } else {
    //                 console.error('No navigation directions found');
    //             }
    //         })
    //         .catch(error => {
    //             console.error('Error fetching navigation directions:', error);
    //         });
    //     })
    //     .catch(error => {
    //         console.error('Error loading shortest route:', error);
    //     });
    // }

    //Newest one
    function displayShortestRoute(startTime) {
        const routeType = document.getElementById('shortestRouteBtn').getAttribute('data-route-type');

        if (!routeType) {
            console.error('Route type not specified.');
            return;
        }
    
        fetch('/shortest-route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_point: startPoint.getLngLat().toArray(),
                end_point: endPoint.getLngLat().toArray(),
                start_time: startTime,
                route_type: routeType
                
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Distance of the shortest route:', data.shortest_route.features[0].properties.distance);
            const shortestRoute = data.shortest_route;
            map.getSource('shortest-route-source').setData(shortestRoute);
            const startCoords = startPoint.getLngLat().toArray().join(',');
            const endCoords = endPoint.getLngLat().toArray().join(',');
            distance = data.shortest_route.features[0].properties.distance
            const estimatedArrivalTime = calculateArrivalTime(startTime, distance);
            console.log(estimatedArrivalTime)
            // Display estimated arrival time to user
            alert(`Total distance: ${distance}\nEstimated Arrival Time: ${estimatedArrivalTime}`); 
            fetch(`https://api.mapbox.com/directions/v5/mapbox/${routeType}/${startCoords};${endCoords}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`)
            .then(response => response.json())
            .then(data => {
                if (data.routes && data.routes.length > 0 && data.routes[0].legs && data.routes[0].legs.length > 0) {
                    const steps = data.routes[0].legs[0].steps;
                    const instructions = steps.map(step => step.maneuver.instruction).join('<br>');
                    document.getElementById('instructions').innerHTML = instructions;
                    document.getElementById('myModal').style.display = 'block';
                } else {
                    console.error('No navigation directions found');
                }
            })
            .catch(error => {
                console.error('Error fetching navigation directions:', error);
            });
        })
        .catch(error => {
            console.error('Error loading shortest route:', error);
        });
    }
    function calculateArrivalTime(startTime, distance) {
        // Assuming velocity is 20 km/h
        const velocity = 5; // km/h
        const travelTimeHours = distance / velocity; // hours
    
        console.log('Travel time (hours):', travelTimeHours);
    
        // Convert travel time to milliseconds
        const travelTimeMs = travelTimeHours * 60 * 60 * 1000; 
    
        console.log('Travel time (milliseconds):', travelTimeMs);
    
        // Convert start time to milliseconds
        const startTimeMs = Date.parse(`01/01/1970 ${startTime}`); 
    
        console.log('Start time:', startTime);
        console.log('Start time (milliseconds):', startTimeMs);
    
        if (isNaN(startTimeMs)) {
            console.error('Invalid start time:', startTime);
            return 'Invalid start time';
        }
        // Calculate arrival time in milliseconds
        const arrivalTimeMs = startTimeMs + travelTimeMs;
        console.log('Arrival time (milliseconds):', arrivalTimeMs);
        // Format arrival time
        const arrivalDate = new Date(arrivalTimeMs);
        const hours = arrivalDate.getHours().toString().padStart(2, '0');
        const minutes = arrivalDate.getMinutes().toString().padStart(2, '0');
    
        return `${hours}:${minutes}`;
    }
    



    function displaySafestRoute() {
        const routeType = document.getElementById('safestRouteBtn').getAttribute('data-route-type');
    
        if (!routeType) {
            console.error('Route type not specified.');
            return;
        }
        fetch('/safest-route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_point: startPoint.getLngLat().toArray(),
                end_point: endPoint.getLngLat().toArray(),
                route_type: routeType
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Safest", data)
            const safestRoute = data.safest_route;
            map.getSource('safest-route-source').setData(safestRoute);
            const startCoords = startPoint.getLngLat().toArray().join(',');
            const endCoords = endPoint.getLngLat().toArray().join(',');
            fetch(`https://api.mapbox.com/directions/v5/mapbox/${routeType}/${startCoords};${endCoords}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`)
            .then(response => response.json())
            .then(data => {
                if (data.routes && data.routes.length > 0 && data.routes[0].legs && data.routes[0].legs.length > 0) {
                    const steps = data.routes[0].legs[0].steps;
                    const instructions = steps.map(step => step.maneuver.instruction).join('<br>');
                    document.getElementById('instructions').innerHTML = instructions;
                    document.getElementById('myModal').style.display = 'block';
                } else {
                    console.error('No navigation directions found');
                }
            })
            .catch(error => {
                console.error('Error fetching navigation directions:', error);
            });
        })
        .catch(error => {
            console.error('Error loading shortest route:', error);
        });
    }

    const modal = document.getElementById('myModal');
    const span = document.getElementsByClassName('close')[0];
    span.onclick = function() {
        modal.style.display = 'none';
    };
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

let dangerousJunctionMarkers = [];

// Function to fetch and display dangerous junctions

function fetchDangerousJunctionsData() {
    fetch('/get-dangerous-junctions')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error fetching dangerous junctions');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response from server:', data);
            if (data && data.features) {
                // Clear existing dangerous junctions markers
                clearDangerousJunctionMarkers();
                // Display new dangerous junctions
                displayDangerousJunctions(data.features);
            } else {
                throw new Error('Unexpected data structure received from server');
            }
        })
        .catch(error => {
            console.error('Error fetching dangerous junctions:', error);
        });
}

function displayDangerousJunctions(features) {
    features.forEach(feature => {
        const { geometry, properties } = feature;
        if (geometry.type === 'Point') {
            const coordinates = geometry.coordinates;
            const popupContent = getPopupContent(properties);
            const markerElement = document.createElement('div');
            markerElement.className = 'danger-marker';
            markerElement.style.backgroundImage = 'url(/static/danger.png)';
            const marker = new mapboxgl.Marker(markerElement)
                .setLngLat(coordinates)
                .setPopup(new mapboxgl.Popup().setHTML(popupContent))
                .addTo(map);
            dangerousJunctionMarkers.push(marker);
            marker.getElement().addEventListener('mouseenter', () => marker.getPopup().addTo(map));
            marker.getElement().addEventListener('mouseleave', () => marker.getPopup().remove());
        } else {
            console.error('Invalid geometry type. Expected "Point", got:', geometry.type);
        }
    });
}

function clearDangerousJunctionMarkers() {
    dangerousJunctionMarkers.forEach(marker => marker.remove());
    dangerousJunctionMarkers = [];
}

document.getElementById('showDangerousJunctionsBtn').addEventListener('click', function() {
    if (dangerousJunctionMarkers.length > 0) {
        clearDangerousJunctionMarkers();
    } else {
        fetchDangerousJunctionsData();
    }
});

// Function to generate popup content for dangerous junctions
function getPopupContent(properties) {
    let content = '<h3>Dangerous Junction</h3>';
    for (const [key, value] of Object.entries(properties)) {
        if (value === true) {
            content += `<p>${key}: ${value}</p>`;
        }
    }
    return content;
}

// Event listener to the button
document.getElementById('displayRoadsUnderConstructionBtn').addEventListener('click', function() {
    displayRoadsUnderConstruction();
});


// Function displayRoadsUnderConstruction to display the road under construction
function displayRoadsUnderConstruction() {
    fetch('/get-roads-under-construction')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error fetching roads under construction');
            }
            return response.json();
        })
        .then(data => {
            // Add the road under construction to the map as a source and layer
            map.addSource('roads-under-construction', {
                type: 'geojson',
                data: data
            });

            map.addLayer({
                id: 'roads-under-construction-layer',
                type: 'line',
                source: 'roads-under-construction',
                layout: {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                paint: {
                    'line-color': 'red',
                    'line-width': 3
                }
            });
        })
        .catch(error => {
            console.error('Error fetching roads under construction:', error);
        });
}
