import { DemoScenario, ScenarioCatalogDTO } from '../types/scenarios';

export type SimulationScenario =
  | 'ACCIDENT_CASCADE'
  | 'STADIUM_EVENT_EGRESS'
  | 'CUSTOM_INCIDENT'
  | 'HISTORICAL_REPLAY'
  | 'LIVE_REPLAY';

export const SIMULATION_SCENARIOS: Record<SimulationScenario, SimulationScenario> = {
  ACCIDENT_CASCADE: 'ACCIDENT_CASCADE',
  STADIUM_EVENT_EGRESS: 'STADIUM_EVENT_EGRESS',
  CUSTOM_INCIDENT: 'CUSTOM_INCIDENT',
  HISTORICAL_REPLAY: 'HISTORICAL_REPLAY',
  LIVE_REPLAY: 'LIVE_REPLAY',
} as const;

// ---------------------------------------------------------------------------
// Unplanned incidents (preserved from original DemoControls)
// ---------------------------------------------------------------------------
const UNPLANNED: DemoScenario[] = [
  { id: 'SCENARIO_1', name: 'Peenya Truck Stall', category: 'UNPLANNED', subtype: 'Vehicle Stall', description: 'LCV breakdown on Highway', sim_type: 'CUSTOM_INCIDENT', icon: 'Car', payload: { lat: 13.0400, lng: 77.5180, gori: 85, hvi: true, rush: true }, expected_outcome: 'CRITICAL. Maximum officers, barricades, heavy tow, graph diversion.' },
  { id: 'SCENARIO_2', name: 'HSR Heavy Vehicle', category: 'UNPLANNED', subtype: 'Heavy Vehicle Blockage', description: 'Heavy vehicle blockage', sim_type: 'ACCIDENT_CASCADE', icon: 'AlertTriangle', payload: { lat: 12.9218, lng: 77.6451, gori: 65, hvi: true, rush: false }, expected_outcome: 'MODERATE/HIGH. Barricades due to heavy vehicle, moderate officers.' },
  { id: 'SCENARIO_3', name: 'Wilson Garden Traffic', category: 'UNPLANNED', subtype: 'Non-Corridor Incident', description: 'Non-corridor incident', sim_type: 'CUSTOM_INCIDENT', icon: 'Car', payload: { lat: 12.9556, lng: 77.5857, gori: 45, hvi: false, rush: false }, expected_outcome: 'LOW. Standard dispatch, no barricades.' },
  { id: 'SCENARIO_4', name: 'Sadashiva Tree Fall', category: 'UNPLANNED', subtype: 'Obstruction', description: 'Tree blocking road', sim_type: 'CUSTOM_INCIDENT', icon: 'Wind', payload: { lat: 13.0061, lng: 77.5794, gori: 75, hvi: false, rush: true }, expected_outcome: 'CRITICAL. High spread velocity, diversion prioritized.' },
  { id: 'SCENARIO_5', name: 'Lalbagh Bus Break', category: 'UNPLANNED', subtype: 'Equipment Failure', description: 'Private bus stalled', sim_type: 'LIVE_REPLAY', icon: 'AlertTriangle', payload: { lat: 12.9539, lng: 77.5852, gori: 35, hvi: true, rush: false }, expected_outcome: 'LOW GORI but Barricades triggered — buses need towing.' },
  { id: 'SCENARIO_6', name: 'Jakkur Multi-Crash', category: 'UNPLANNED', subtype: 'Multi-Crash Cascade', description: 'Amruthahalli accident', sim_type: 'ACCIDENT_CASCADE', icon: 'Zap', payload: { lat: 13.0664, lng: 77.5998, gori: 96, hvi: true, rush: true }, expected_outcome: 'CATASTROPHIC. 3 cascading incidents, total resource exhaustion.' },
  { id: 'SCENARIO_7', name: 'Kengeri BMTC Fail', category: 'UNPLANNED', subtype: 'Equipment Failure', description: 'BMTC bus broken down', sim_type: 'CUSTOM_INCIDENT', icon: 'Construction', payload: { lat: 12.9328, lng: 77.4879, gori: 55, hvi: true, rush: false }, expected_outcome: 'MODERATE. Standard heavy-vehicle recovery.' },
  { id: 'SCENARIO_9', name: 'Whitefield Flood', category: 'UNPLANNED', subtype: 'Weather Event', description: 'Underpass water logging', sim_type: 'HISTORICAL_REPLAY', icon: 'Droplets', payload: { lat: 13.0008, lng: 77.6813, gori: 92, hvi: false, rush: true }, expected_outcome: 'CRITICAL. Underpass failure, immediate rerouting.' },
  { id: 'SCENARIO_10', name: 'Hebbal Flyover Stall', category: 'UNPLANNED', subtype: 'Vehicle Stall', description: 'Vehicle starting problem', sim_type: 'LIVE_REPLAY', icon: 'Thermometer', payload: { lat: 13.0418, lng: 77.5947, gori: 25, hvi: false, rush: false }, expected_outcome: 'NOMINAL. Minimal officers, no over-reaction.' },
];

// ---------------------------------------------------------------------------
// Planned events (NEW — closes Gap 1)
// ---------------------------------------------------------------------------
const PLANNED: DemoScenario[] = [
  { id: 'SCENARIO_8', name: 'Chinnaswamy Match', category: 'PLANNED', subtype: 'Sports Egress', description: 'Cricket match egress', sim_type: 'STADIUM_EVENT_EGRESS', icon: 'Shield', payload: { lat: 12.9788, lng: 77.5995, gori: 82, hvi: false, rush: true }, expected_outcome: 'CRITICAL. Event-driven congestion, rapid clearance prioritized.' },
  { id: 'SCENARIO_11', name: 'Mall Bench Political Rally', category: 'PLANNED', subtype: 'Political Rally', description: '50K-attendee rally egress', sim_type: 'STADIUM_EVENT_EGRESS', icon: 'Users', payload: { lat: 12.9756, lng: 77.6071, gori: 90, hvi: false, rush: true }, expected_outcome: 'CRITICAL. Pedestrian-vehicle conflict, surge officers, full corridor diversion.' },
  { id: 'SCENARIO_12', name: 'Lalbagh Flower Festival', category: 'PLANNED', subtype: 'Festival', description: 'Weekend flower show crowd surge', sim_type: 'STADIUM_EVENT_EGRESS', icon: 'Flower2', payload: { lat: 12.9508, lng: 77.5848, gori: 78, hvi: false, rush: true }, expected_outcome: 'HIGH. Recurring hotspot, staged parking diversion.' },
  { id: 'SCENARIO_13', name: 'Outer Ring Road Marathon', category: 'PLANNED', subtype: 'Public Gathering', description: 'City marathon road closure', sim_type: 'HISTORICAL_REPLAY', icon: 'Activity', payload: { lat: 12.9352, lng: 77.6245, gori: 70, hvi: false, rush: true }, expected_outcome: 'HIGH. Scheduled corridor closure, time-boxed diversion.' },
  { id: 'SCENARIO_14', name: 'Silk Board Construction', category: 'PLANNED', subtype: 'Construction', description: 'Flyover construction lane closure', sim_type: 'CUSTOM_INCIDENT', icon: 'HardHat', payload: { lat: 12.9177, lng: 77.6223, gori: 68, hvi: true, rush: true }, expected_outcome: 'HIGH. Persistent capacity reduction, long-duration diversion.' },
  { id: 'SCENARIO_15', name: 'Palace Ground Summit', category: 'PLANNED', subtype: 'Political Summit', description: 'VIP movement + delegate egress', sim_type: 'STADIUM_EVENT_EGRESS', icon: 'Crown', payload: { lat: 13.0067, lng: 77.5803, gori: 84, hvi: false, rush: true }, expected_outcome: 'CRITICAL. VIP security, corridor sterilization, maximum officers.' },
];

/** Static fallback catalog — mirrors backend/app/scenarios/scenario_catalog.py. */
export const FALLBACK_CATALOG: ScenarioCatalogDTO = {
  planned: PLANNED,
  unplanned: UNPLANNED,
  counts: {
    PLANNED: PLANNED.length,
    UNPLANNED: UNPLANNED.length,
    TOTAL: PLANNED.length + UNPLANNED.length,
  },
};
