import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, Polyline, Circle, useMap, Marker } from 'react-leaflet';
import { useIncidentStore } from '../../store/incident.store';
import { useSimulationStore } from '../../store/simulation.store';
import { ShieldAlert } from 'lucide-react';
import L from 'leaflet';

// Fix Leaflet Marker Icon bug
let DefaultIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const barricadeIcon = L.divIcon({
  className: 'custom-barricade-icon',
  html: '<div style="font-size: 16px; background: rgba(0,0,0,0.5); border-radius: 50%; padding: 2px;">🚧</div>',
  iconSize: [24, 24],
  iconAnchor: [12, 12]
});

// Helper component to center and zoom map dynamically
const MapController: React.FC<{ center: [number, number]; zoom: number }> = ({ center, zoom }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center, zoom, { animate: true, duration: 1.5 });
  }, [center, zoom, map]);
  return null;
};

export const CommandMap: React.FC = () => {
  const incidents = useIncidentStore((state) => Object.values(state.incidents));
  const selectedId = useIncidentStore((state) => state.selectedIncidentId);
  const selectedIncident = useIncidentStore((state) => selectedId ? state.incidents[selectedId] : null);
  const operationalPlans = useSimulationStore((state) => state.operationalPlans);
  const selectIncident = useIncidentStore((state) => state.setSelectedIncidentId);

  const [mapCenter, setMapCenter] = useState<[number, number]>([12.9716, 77.5946]); // Default to Bangalore
  const [mapZoom, setMapZoom] = useState<number>(13);

  // Sync center with selected incident
  useEffect(() => {
    if (selectedIncident) {
      setMapCenter([selectedIncident.latitude, selectedIncident.longitude]);
      setMapZoom(15);
    }
  }, [selectedIncident]);

  // Cinematic Auto-focus: if a new incident arrives and nothing is selected, select it.
  useEffect(() => {
    if (!selectedId && incidents.length > 0) {
      // Prioritize critical incidents, otherwise just pick the first one
      const criticalIncident = incidents.find(i => i.gori_score > 70) || incidents[0];
      if (criticalIncident) {
        selectIncident(criticalIncident.incident_id);
      }
    }
  }, [incidents, selectedId, selectIncident]);

  return (
    <div className="w-full h-full relative rounded-xl overflow-hidden border border-dark-border shadow-xl">
      <MapContainer
        center={mapCenter}
        zoom={mapZoom}
        zoomControl={false}
        style={{ height: '100%', width: '100%', background: '#0B0D17' }} // dark space background
      >
        {/* CartoDB Dark Matter tiles */}
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
        />

        {/* Dynamic center control */}
        <MapController center={mapCenter} zoom={mapZoom} />

        {/* Render Incidents */}
        {incidents.map((incident) => {
          const isSelected = incident.incident_id === selectedId;
          const isCritical = incident.gori_score > 70;
          const plan = operationalPlans[incident.incident_id];
          
          // Color based on GORI score severity
          const markerColor = isCritical ? '#ef4444' : (incident.gori_score > 45 ? '#f59e0b' : '#3b82f6');
          
          return (
            <React.Fragment key={incident.incident_id}>
              {/* Hotspot congestion spread radius */}
              <Circle
                center={[incident.latitude, incident.longitude]}
                radius={isCritical ? 450 : 250}
                pathOptions={{
                  fillColor: markerColor,
                  fillOpacity: isSelected ? 0.22 : 0.08,
                  color: markerColor,
                  weight: 1.5,
                  dashArray: isSelected ? '6,6' : '3,3',
                  className: isCritical ? 'animate-pulse-slow' : ''
                }}
              />

              {/* Pulsing ring for critical events */}
              {isCritical && (
                <CircleMarker
                  center={[incident.latitude, incident.longitude]}
                  radius={isSelected ? 18 : 12}
                  pathOptions={{
                    fillColor: markerColor,
                    fillOpacity: 0.15,
                    color: markerColor,
                    weight: 1,
                    className: 'animate-ping'
                  }}
                />
              )}

              {/* Core Incident marker */}
              <CircleMarker
                center={[incident.latitude, incident.longitude]}
                radius={isSelected ? 10 : 7}
                eventHandlers={{
                  click: () => {
                    selectIncident(incident.incident_id);
                  },
                }}
                pathOptions={{
                  fillColor: markerColor,
                  fillOpacity: 0.95,
                  color: isSelected ? '#ffffff' : markerColor,
                  weight: isSelected ? 2.5 : 1,
                }}
              >
                <Popup className="custom-popup">
                  <div className="p-2 min-w-[200px] text-gray-100 bg-[#121626] border border-dark-border rounded shadow-glow-critical">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-bold text-brand-primary">{incident.incident_id}</span>
                      <span className={`text-xxs px-2 py-0.5 rounded font-bold ${
                        isCritical ? 'bg-red-500/20 text-red-400' : 'bg-blue-500/20 text-blue-400'
                      }`}>
                        GORI: {Math.round(incident.gori_score)}
                      </span>
                    </div>
                    <h4 className="font-semibold text-sm mb-1 text-gray-200">{incident.type}</h4>
                    <p className="text-xxs text-gray-400 mb-2">
                      Lat: {incident.latitude.toFixed(4)}, Lng: {incident.longitude.toFixed(4)}
                    </p>
                    {incident.deployment_recommendation && (
                      <div className="bg-[#181C2E] border border-dark-border p-1.5 rounded text-xxs flex items-start space-x-1.5">
                        <ShieldAlert className="w-3.5 h-3.5 text-brand-accent shrink-0 mt-0.5" />
                        <div>
                          <p className="font-bold text-gray-300 leading-none">Recommend Plan</p>
                          <p className="text-gray-400 mt-1">{incident.deployment_recommendation}</p>
                        </div>
                      </div>
                    )}
                  </div>
                </Popup>
              </CircleMarker>

              {/* Barricade Overlay for Closed Roads */}
              {incident.heavy_vehicle && (
                <Marker position={[incident.latitude + 0.0005, incident.longitude + 0.0005]} icon={barricadeIcon}>
                  <Popup>
                    <div className="text-xxs font-bold text-yellow-500 bg-black/80 px-2 py-1 rounded">HEAVY VEHICLE BARRICADE</div>
                  </Popup>
                </Marker>
              )}

              {/* Diversion Polyline Route (if plan available) */}
              {plan?.diversion_plan?.points && (
                <Polyline
                  positions={plan.diversion_plan.points}
                  pathOptions={{
                    color: '#6366F1', // brand-accent
                    weight: 4,
                    dashArray: '10,10',
                    opacity: isSelected ? 0.9 : 0.4,
                    className: 'animate-pulse' // dynamic flowing path
                  }}
                >
                  <Popup>
                    <div className="p-1 text-xxs font-semibold bg-[#121626] text-purple-400 border border-purple-500/30 rounded shadow-glow-emergency">
                      Diversion Path: {plan.diversion_plan.description}
                    </div>
                  </Popup>
                </Polyline>
              )}
            </React.Fragment>
          );
        })}
      </MapContainer>

      {/* Floating Map Legend */}
      <div className="absolute bottom-4 right-4 z-[400] bg-dark-card/90 backdrop-blur-sm border border-dark-border px-4 py-3 rounded-lg shadow-tactical text-xs flex flex-col space-y-2 pointer-events-none">
        <h5 className="font-bold text-gray-300 uppercase tracking-wider text-[10px]">Command Legends</h5>
        <div className="flex items-center space-x-2">
          <span className="w-3 h-3 rounded-full bg-severity-high shadow-glow-critical"></span>
          <span className="text-gray-400 font-medium">Critical GORI Spike (&gt;70)</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-3 h-3 rounded-full bg-severity-elevated shadow-glow-elevated"></span>
          <span className="text-gray-400 font-medium">Moderate Incidents (45-70)</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-3 h-3 rounded-full bg-brand-primary"></span>
          <span className="text-gray-400 font-medium">Minor Road Blockages (&lt;45)</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-6 h-0.5 border-t-2 border-dashed border-brand-accent"></span>
          <span className="text-gray-400 font-medium">AI Graph Diversion Route</span>
        </div>
        <div className="flex items-center space-x-2 mt-1">
          <span className="text-[14px]">🚧</span>
          <span className="text-gray-400 font-medium text-xs">Road Barricade Overlay</span>
        </div>
      </div>
    </div>
  );
};
