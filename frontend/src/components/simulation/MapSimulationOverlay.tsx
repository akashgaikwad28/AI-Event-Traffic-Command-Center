import React from 'react';
import { useDemoStore } from '../../store/demo.store';
import { Circle, Marker, Popup, Polyline } from 'react-leaflet';
import L from 'leaflet';

// Custom icons
const incidentIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

const unitIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

const barricadeIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

export const MapSimulationOverlay: React.FC = () => {
  const { simulationResult, playbackFrameIndex } = useDemoStore();

  if (!simulationResult) return null;

  const frame = simulationResult.optimized_state.timeline_frames[playbackFrameIndex];
  if (!frame) return null;

  return (
    <>
      {frame.map_entities.map((entity: any) => {
        if (entity.type === 'hotspot') {
          return (
            <Circle
              key={entity.id}
              center={[entity.lat, entity.lng]}
              radius={entity.radius || 100}
              pathOptions={{
                color: '#ef4444',
                fillColor: '#ef4444',
                fillOpacity: 0.3,
                weight: 2,
                className: 'animate-pulse' // CSS animation class
              }}
            >
              <Popup>Spread Radius: {Math.round(entity.radius || 100)}m</Popup>
            </Circle>
          );
        }

        let icon = incidentIcon;
        if (entity.type === 'unit') icon = unitIcon;
        if (entity.type === 'barricade') icon = barricadeIcon;

        if (['incident', 'unit', 'barricade'].includes(entity.type)) {
          return (
            <Marker key={entity.id} position={[entity.lat, entity.lng]} icon={icon}>
              <Popup className="uppercase font-bold text-xs">{entity.type}</Popup>
            </Marker>
          );
        }

        if (entity.type === 'diversion' && entity.metadata?.points) {
           return (
             <Polyline
               key={entity.id}
               positions={entity.metadata.points}
               pathOptions={{ color: '#3b82f6', weight: 4, dashArray: '10, 10', className: 'animate-[dash_1s_linear_infinite]' }}
             />
           );
        }

        return null;
      })}
    </>
  );
};
