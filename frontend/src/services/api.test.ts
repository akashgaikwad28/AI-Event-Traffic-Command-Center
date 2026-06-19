// @ts-nocheck
import { api } from './api';
import { SIMULATION_SCENARIOS } from '../constants/scenarios';

// Mock global fetch for testing
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ status: 'Simulation triggered' }),
  })
) as jest.Mock;

describe('API Service - Simulation Scenarios', () => {
  beforeEach(() => {
    (global.fetch as jest.Mock).mockClear();
  });

  it('should throw an error for invalid scenarios before calling fetch', async () => {
    // @ts-expect-error - Testing invalid input bypassing types
    await expect(api.triggerSimulation('INVALID_SCENARIO')).rejects.toThrow(
      'Invalid simulation scenario: INVALID_SCENARIO'
    );
    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('should call fetch with a valid enum scenario', async () => {
    await api.triggerSimulation(SIMULATION_SCENARIOS.ACCIDENT_CASCADE);
    
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/stream/start-simulation/ACCIDENT_CASCADE'),
      expect.objectContaining({ method: 'POST' })
    );
  });

  it('should map LIVE_REPLAY correctly without errors', async () => {
    await api.triggerSimulation(SIMULATION_SCENARIOS.LIVE_REPLAY);
    
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/stream/start-simulation/LIVE_REPLAY'),
      expect.objectContaining({ method: 'POST' })
    );
  });
});
